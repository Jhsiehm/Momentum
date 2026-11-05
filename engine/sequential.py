"""Development-only, forward Congress benchmark for originating-chamber passage."""
import argparse
import json
from datetime import timedelta
from pathlib import Path
from .store import Store, congress_end, digest, timestamp, now
from .model import date, snapshot, fit, predict, score
from .learning import _select, features

VERSION = 'origin-passage-day30-v1'
TARGET = 'originating_chamber_passage_by_congress_end'


def prepare(store, dataset, labels, as_of):
    """Labels are separately adjudicated; enactment resolutions are never reused."""
    rows, exclusions, seen = [], [], set()
    as_of = timestamp(as_of)
    bills = {b['bill_id']: b for b in store.bills(dataset, as_of)}
    for label in labels:
        bid = label['bill_id']
        if bid in seen:
            raise ValueError('Duplicate label: ' + bid)
        seen.add(bid)
        if label.get('target') != TARGET or type(label.get('value')) is not int or label['value'] not in (0, 1):
            raise ValueError('Explicit binary passage target required')
        if not all(label.get(k) for k in ('source_url', 'source_hash', 'audit_note')):
            raise ValueError('Label requires source URL, source hash and adjudication note')
        known, effective = timestamp(label['available_at']), timestamp(label['effective_at'])
        bill = bills.get(bid)
        reason = None
        if not bill:
            reason = 'metadata_unavailable'
        elif known > as_of or effective > as_of:
            reason = 'label_pending'
        else:
            end = congress_end(bill['congress'])
            cutoff = timestamp((date(bill['introduced_at']) + timedelta(days=30)).isoformat())
            if label['value'] == 0 and (label.get('complete_coverage') is not True or effective < end or timestamp(label.get('coverage_through', '1900-01-01')) < end):
                raise ValueError('Negative passage label requires complete action coverage through Congress end')
            if label['value'] == 1 and not (timestamp(bill['introduced_at']) <= effective <= end):
                raise ValueError('Passage date outside Congress bill lifetime')
            snap = snapshot(store, dataset, bid, cutoff)
            if cutoff >= end:
                reason = 'checkpoint_after_congress'
            elif not snap:
                reason = 'checkpoint_evidence_unavailable'
            elif snap['stage'] >= 2 or effective <= cutoff:
                reason = 'already_passed_at_checkpoint'
            else:
                lid = digest(label)
                rows.append(dict(bill_id=bid, family_id=bill['family_id'], congress=bill['congress'],
                                 cutoff=cutoff, x=snap['features'], title=snap['bill']['title'],
                                 topic=snap['bill'].get('topic'), y=label['value'],
                                 resolution_id=lid, available_at=known, effective_at=effective,
                                 snapshot_hash=snap['snapshot_hash'], evidence_ids=snap['evidence_ids']))
        if reason:
            exclusions.append(dict(bill_id=bid, reason=reason))
    exclusions.extend(dict(bill_id=bid, reason='missing_passage_label') for bid in sorted(bills.keys() - seen))
    return sorted(rows, key=lambda r: (r['congress'], r['bill_id'])), exclusions


def eligible(rows, cutoff, families):
    selected = {}
    for r in rows:
        if r['family_id'] not in families and r['available_at'] <= cutoff and r['effective_at'] <= cutoff:
            selected.setdefault(r['family_id'], r)
    return list(selected.values())


def sufficient(rows):
    return len(rows) >= 20 and len({r['y'] for r in rows}) == 2


def benchmark(store, dataset, labels, start, first_test, last_test, as_of):
    if not 1 <= start < first_test <= last_test:
        raise ValueError('Require start < first test <= last test')
    rows, exclusions = prepare(store, dataset, labels, as_of)
    # Reserve all evaluation families before fitting any model, including frozen.
    families = {r['family_id'] for r in rows if first_test <= r['congress'] <= last_test}
    first_origin = congress_end(first_test - 1)
    initial = eligible([r for r in rows if start <= r['congress'] < first_test], first_origin, families)
    frozen = fit(initial) if sufficient(initial) else None
    folds = []
    for congress in range(first_test, last_test + 1):
        origin = congress_end(congress - 1)
        test = [r for r in rows if r['congress'] == congress]
        train = eligible([r for r in rows if start <= r['congress'] < congress], origin,
                         {r['family_id'] for r in rows if congress <= r['congress'] <= last_test})
        fold = dict(congress=congress, training_origin=origin, training_count=len(train),
                    test_count=len(test), training_manifest=train)
        if congress_end(congress) > timestamp(as_of):
            fold.update(status='blocked', reason='Evaluation Congress has not ended as of the audit date')
            folds.append(fold)
            continue
        if frozen is None or not sufficient(train) or not test:
            fold.update(status='blocked', reason='Need 20 initial and current prior families, both training classes, and eligible test cases')
            folds.append(fold)
            continue
        fixed = fit(train)
        selection = _select(train, {r['resolution_id']: r for r in train})
        adaptive = selection.get('artifact', fixed)
        policy = selection['selected_feature_policy']
        rate = (sum(r['y'] for r in train) + 1) / (len(train) + 2)
        predictions = []
        for r in test:
            predictions.append(dict(bill_id=r['bill_id'], family_id=r['family_id'], cutoff=r['cutoff'],
                                    snapshot_hash=r['snapshot_hash'], evidence_ids=r['evidence_ids'],
                                    input_features=r['x'], label_id=r['resolution_id'], outcome=r['y'],
                                    frozen=predict(frozen, r['x']), retrained=predict(fixed, r['x']),
                                    adaptive=predict(adaptive, features(r, policy)), historical_rate=rate))
        metrics = {name: score([p[name] for p in predictions], [p['outcome'] for p in predictions])
                   for name in ('frozen', 'retrained', 'adaptive', 'historical_rate')}
        for name, metric in metrics.items():
            metric['events'] = sum(p['outcome'] for p in predictions)
            metric['true_positives_at_0_5'] = sum(p[name] >= .5 and p['outcome'] == 1 for p in predictions)
            metric['false_positives_at_0_5'] = sum(p[name] >= .5 and p['outcome'] == 0 for p in predictions)
        fold.update(status='completed', predictions=predictions, metrics=metrics, selection=selection,
                    artifacts=dict(retrained=fixed, adaptive=adaptive),
                    paired_brier_delta={name: metrics[name]['brier'] - metrics['frozen']['brier']
                                        for name in ('retrained', 'adaptive', 'historical_rate')})
        folds.append(fold)
    report = dict(version=VERSION, target=TARGET, dataset=dataset, as_of=timestamp(as_of),
                  config=dict(start=start, first_test=first_test, last_test=last_test, checkpoint_days=30),
                  status='completed' if all(f['status'] == 'completed' for f in folds) else 'incomplete',
                  release_eligible=False, labels_hash=digest(labels), label_manifest=labels, exclusions=exclusions,
                  frozen_artifact=frozen, frozen_training_manifest=initial, folds=folds,
                  code_hashes={name: digest(Path(__file__).with_name(name).read_text())
                               for name in ('sequential.py', 'model.py', 'learning.py', 'store.py')},
                  note='Development replay only. Label provenance is an operator assertion. No untouched final holdout, clustered uncertainty or validated improvement claim. Synthetic data establish software behavior only.')
    report['id'] = digest(report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('labels', help='Adjudicated passage labels, JSONL')
    parser.add_argument('--database', required=True)
    parser.add_argument('--dataset', choices=('official', 'demo'), default='official')
    parser.add_argument('--start', type=int, default=110)
    parser.add_argument('--first-test', type=int, default=113)
    parser.add_argument('--last-test', type=int, default=118)
    parser.add_argument('--as-of', default=now())
    parser.add_argument('--output-dir', default='data/sequential')
    args = parser.parse_args()
    labels = [json.loads(line) for line in Path(args.labels).read_text().splitlines() if line.strip()]
    store = Store(args.database)
    try:
        report = benchmark(store, args.dataset, labels, args.start, args.first_test, args.last_test, args.as_of)
    finally:
        store.close()
    directory = Path(args.output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output = directory / (report['id'] + '.json')
    body = json.dumps(report, indent=2) + '\n'
    try:
        with output.open('x') as handle:
            handle.write(body)
    except FileExistsError:
        if output.read_text() != body:
            raise ValueError('Existing report content differs from immutable identity')
    print(json.dumps(dict(status=report['status'], path=str(output), id=report['id'])))


if __name__ == '__main__':
    main()
