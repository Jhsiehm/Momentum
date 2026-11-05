"""Read-only, snapshot-scoped import integrity audit; never certifies eligibility.

Run: python3 -m engine.import_quality --output data/audits/import-quality.json
"""
import argparse
from collections import Counter
from datetime import datetime, timedelta
import hashlib
import json
from pathlib import Path
import sqlite3
from .store import ROOT, available, congress_end, digest, now, timestamp


def historical_quality(records, age_days=180):
    """Diagnostics only: neither retained positive labels nor timestamps certify eligibility.

    Inspect all metadata versions, so a current import cannot hide an earlier
    snapshot. Conflicting labels and family identities remain visible; never
    resolve them by choosing the latest row or silently create negative labels.
    """
    if type(age_days) is not int or age_days < 0:
        raise ValueError('age_days must be a nonnegative integer')
    bills, labels, identities = {}, {}, {}
    for _, kind, body in records:
        bid = body['bill_id']
        identities.setdefault(bid, set()).add(body.get('family_id'))
        if kind == 'bill':
            bills.setdefault(bid, []).append(body)
        elif kind == 'resolution':
            labels.setdefault(bid, []).append(body)
    groups = {}
    for bid, versions in sorted(bills.items()):
        latest = versions[-1]
        congress = latest['congress']
        counts = groups.setdefault(congress, Counter())
        counts['imported'] += 1
        counts['family_identity_conflicts'] += len(identities[bid]) > 1
        counts['metadata_identity_conflicts'] += len({(b['congress'], b['type'], b.get('introduced_at')) for b in versions}) > 1
        outcomes = labels.get(bid, [])
        values = {r['value'] for r in outcomes}
        category = 'unresolved'
        if len(values) > 1:
            category = 'conflicting'
        elif values == {0}:
            category = 'recorded_negative'
        elif values == {1}:
            dates = {timestamp(r['effective_at']) for r in outcomes}
            if len(dates) > 1:
                category = 'positive_date_conflict'
            else:
                enacted = next(iter(dates))
                end = congress_end(congress)
                # Date-only inputs have been normalized by Store to end of day.
                # All endpoint-day records conservatively need precision review.
                category = ('positive_endpoint_day_review' if enacted[:10] == end[:10]
                            else 'positive_before_deadline' if enacted < end
                            else 'positive_after_deadline')
        counts[category] += 1
        try:
            cutoff = (datetime.fromisoformat(timestamp(latest['introduced_at']).replace('Z', '+00:00'))
                      + timedelta(days=age_days)).isoformat().replace('+00:00', 'Z')
            before_end = cutoff < congress_end(congress)
            counts['checkpoint_before_end'] += before_end
            has_metadata = any(available(b) <= cutoff and timestamp(b['effective_at']) <= cutoff for b in versions)
            counts['metadata_available_by_checkpoint'] += before_end and has_metadata
            if category == 'positive_before_deadline':
                counts['positive_after_checkpoint_before_deadline'] += before_end and cutoff[:10] < enacted[:10]
        except (KeyError, TypeError, ValueError):
            counts['invalid_checkpoint_metadata'] += 1
    fields = ('imported', 'unresolved', 'conflicting', 'recorded_negative',
              'positive_before_deadline', 'positive_after_deadline', 'positive_endpoint_day_review',
              'positive_date_conflict', 'positive_after_checkpoint_before_deadline',
              'checkpoint_before_end', 'metadata_available_by_checkpoint',
              'invalid_checkpoint_metadata', 'family_identity_conflicts', 'metadata_identity_conflicts')
    return dict(age_days=age_days, by_congress=[dict(congress=c, **{k: counts[k] for k in fields})
                for c, counts in sorted(groups.items())],
                orphan_resolution_bill_ids=sorted(set(labels)-set(bills)),
                eligible_positive_families=None,
                note='Eligible positive families are not certified by this audit. Counts do not verify source contents, complete negative coverage, action history, historical label availability, or adjudicated family separation. After-deadline positives are not converted to negatives.')


def audit(database, raw_directory):
    started = now()
    db = sqlite3.connect(Path(database).resolve().as_uri() + '?mode=ro', uri=True)
    try:
        db.execute('BEGIN')
        tables = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        def bodies(table):
            return [json.loads(r[0]) for r in db.execute('SELECT body FROM ' + table)] if table in tables else []
        records = [(r[0], r[1], json.loads(r[2])) for r in db.execute(
            "SELECT id,kind,body FROM records WHERE dataset='official' ORDER BY available_at,effective_at,id")]
        plans = bodies('coverage_plans')
        inventories = bodies('sample_inventories')
        jobs = {j['id']: j for j in bodies('bulk_import_jobs')}
        receipts = {r[0]: json.loads(r[1]) for r in db.execute('SELECT name,body FROM checkpoints')}
        snapshot = now()
    finally:
        db.close()
    latest = {}
    kind_counts = Counter()
    record_failures = []
    raw_hashes = set()
    for ident, kind, body in records:
        kind_counts[kind] += 1
        if ident != digest({k: v for k, v in body.items() if k != 'id'}) or body.get('id') != ident:
            record_failures.append(ident)
        if body.get('raw_hash'):
            raw_hashes.add(body['raw_hash'])
        if kind == 'bill':
            latest[body['bill_id']] = body
    for inv in inventories:
        raw_hashes.update(s['raw_hash'] for s in inv['strata'])
    missing_raw, corrupt_raw = [], []
    for sha in sorted(raw_hashes):
        if len(sha) != 64 or any(c not in '0123456789abcdef' for c in sha):
            corrupt_raw.append(sha)
            continue
        path = Path(raw_directory) / sha
        if not path.is_file():
            missing_raw.append(sha)
        elif hashlib.sha256(path.read_bytes()).hexdigest() != sha:
            corrupt_raw.append(sha)
    missing_receipts, bad_receipts = [], []
    # Current bulk snapshots have fetch/raw receipts; archived pilot sources use
    # a different provenance contract, and are counted separately.
    bulk_bills = {b: r for b, r in latest.items() if 'current bulk snapshot' in r.get('coverage', '')}
    for bill_id, body in sorted(bulk_bills.items()):
        sha = body['raw_hash']
        receipt = receipts.get(f'raw:{bill_id}:{sha}')
        if not receipt:
            missing_receipts.append(bill_id)
        elif receipt.get('hash') != sha or receipt.get('retrieved_at') != body['observed_at']:
            bad_receipts.append(bill_id)
    resolutions = {}
    actions = set()
    for _, kind, body in records:
        if kind == 'resolution':
            resolutions.setdefault(body['bill_id'], set()).add(body['value'])
        if kind == 'event':
            actions.add(body['bill_id'])
    def population_stats(ids):
        imported = set(ids) & latest.keys()
        return dict(population=len(set(ids)), imported=len(imported), missing_ids=sorted(set(ids)-latest.keys()),
            missing_fields={field: sum(not latest[b].get(field) or latest[b].get(field) in
                                      ('Unknown', 'Unclassified', 'Untitled measure') for b in imported)
                            for field in ('title', 'topic', 'sponsor', 'introduced_at', 'raw_hash')},
            without_actions=len(imported-actions),
            outcomes=dict(positive=sum(resolutions.get(b)=={1} for b in imported),
                          negative=sum(resolutions.get(b)=={0} for b in imported),
                          conflicting=sum(len(resolutions.get(b,set()))>1 for b in imported),
                          unresolved=sum(b not in resolutions for b in imported)),
            family_unadjudicated=sum(not latest[b].get('family_status') or
                                     'unadjudicated' in latest[b]['family_status'].lower() for b in imported),
            historically_verified_metadata=sum(bool(latest[b].get('verified_available_at') and
                                                    latest[b].get('archive_proof')) for b in imported))
    plan_reports = []
    for plan in plans:
        job_list = [jobs[b['job_id']] for b in plan['batches'] if b.get('job_id') in jobs]
        batch_ids = [bid for batch in plan['batches'] for bid in batch['bill_ids']]
        inv = next((i for i in inventories if i['id']==plan['inventory_id']), None)
        expected = {b for b in inv['bill_ids'] if int(b.split('-')[0]) in plan['congresses']} if inv else set()
        pop = {k: plan[k] for k in ('inventory_id','inventory_hash','congresses','bill_ids')}
        plan_reports.append(dict(id=plan['id'], status=plan['status'], congresses=plan['congresses'],
            finished_at=plan.get('finished_at'), population_hash=plan['population_hash'],
            population_hash_valid=digest(pop)==plan['population_hash'], inventory_found=bool(inv),
            exact_inventory_population=bool(inv) and set(plan['bill_ids'])==expected,
            population_duplicates=len(plan['bill_ids'])-len(set(plan['bill_ids'])),
            batch_duplicates=len(batch_ids)-len(set(batch_ids)), batches_exact=set(batch_ids)==set(plan['bill_ids']),
            batches=len(plan['batches']), completed_batches=sum(j['status']=='completed' for j in job_list),
            job_completed=sum(j['completed'] for j in job_list), job_failed=sum(j['failed'] for j in job_list),
            **population_stats(plan['bill_ids'])))
    report = dict(schema_version=2, started_at=started, database_snapshot_at=snapshot, finished_at=now(),
        database=str(Path(database).resolve()), scope='Official local records and saved inventory/coverage plans in one read-only SQLite snapshot.',
        record_counts=dict(kind_counts), unique_bills=len(latest), extra_bill_versions=kind_counts['bill']-len(latest),
        official_population=population_stats(latest), plans=plan_reports,
        historical_quality=historical_quality(records),
        integrity=dict(record_ids_checked=len(records), invalid_record_ids=record_failures,
            raw_hashes_checked=len(raw_hashes), missing_raw=missing_raw, corrupt_raw=corrupt_raw,
            bulk_receipts_checked=len(bulk_bills), other_provenance_bills=len(latest)-len(bulk_bills),
            missing_bulk_receipts=missing_receipts, invalid_bulk_receipts=bad_receipts,
            inventories=[dict(id=i['id'], hash_valid=digest({k:v for k,v in i.items() if k not in ('id','hash')})==i['hash']) for i in inventories]),
        interpretation='Presence, content hashes and retrieval receipts establish retained-source integrity, not historical availability, correct outcome adjudication, or training/evaluation eligibility. Unresolved outcomes must not be treated as negative labels.')
    report['report_hash'] = digest(report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database', type=Path, default=ROOT/'data'/'engine.sqlite')
    parser.add_argument('--raw-directory', type=Path, default=ROOT/'data'/'raw')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.database, args.raw_directory)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(output=str(args.output.resolve()), report_hash=result['report_hash'], unique_bills=result['unique_bills'], plans=result['plans']), indent=2))


if __name__ == '__main__':
    main()
