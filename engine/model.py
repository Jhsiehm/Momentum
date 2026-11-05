"""Deterministic, auditable baselines. No claim of validated calibration."""
import math
from datetime import datetime, timedelta
from .store import available, congress_end, digest, now, timestamp

MODEL_VERSION = 'structured-l2-v1'
FEATURE_VERSION = 'temporal-v1'
STAGES = ['Introduced', 'Committee', 'Passed origin', 'Bicameral', 'Enacted']

def date(value):
    return datetime.fromisoformat(timestamp(value).replace('Z', '+00:00'))

def snapshot(store, dataset, bill_id, cutoff):
    cutoff = timestamp(cutoff)
    bill = store.bill(dataset, bill_id, cutoff)
    if not bill:
        return None
    events = store.records('event', dataset, bill_id, cutoff)
    events.sort(key=lambda e: (e['effective_at'], e['id']))
    stage = max([0] + [e.get('stage', 0) for e in events])
    age = max(0, (date(cutoff) - date(bill['introduced_at'])).days)
    last = max([bill['introduced_at']] + [e['effective_at'] for e in events])
    recent = sum((date(cutoff) - date(e['effective_at'])).days <= 30 for e in events)
    features = [stage / 4, min(age, 730) / 730, min(len(events), 30) / 30,
                min((date(cutoff) - date(last)).days, 730) / 730,
                int(bill['type'] == 's'), min(recent, 10) / 10]
    ids = [bill['id']] + [e['id'] for e in events]
    return {'bill': bill, 'cutoff': cutoff, 'events': events, 'stage': stage,
            'stage_name': STAGES[stage], 'age_days': age, 'features': features,
            'snapshot_hash': digest({'ids': ids, 'cutoff': cutoff, 'version': FEATURE_VERSION}),
            'evidence_ids': ids}

def resolution(store, dataset, bill_id, cutoff=None):
    rows = store.records('resolution', dataset, bill_id, cutoff or now())
    return rows[-1] if rows else None

def training_rows(store, target):
    bill, cutoff = target['bill'], target['cutoff']
    rows, families = [], set()
    for other in store.bills(bill['dataset'], cutoff):
        if other['congress'] >= bill['congress'] or other['family_id'] == bill['family_id']:
            continue
        outcome = resolution(store, bill['dataset'], other['bill_id'], cutoff)
        if not outcome or outcome['family_id'] in families:
            continue
        # Match age prospectively, bounded by the outcome and session end.
        candidate = date(other['introduced_at']) + timedelta(days=target['age_days'])
        if candidate >= date(outcome['effective_at']) or candidate >= date(congress_end(other['congress'])):
            continue
        snap = snapshot(store, bill['dataset'], other['bill_id'], candidate.isoformat())
        if not snap or snap['stage'] == 4:
            continue
        families.add(outcome['family_id'])
        rows.append({'bill_id': other['bill_id'], 'family_id': other['family_id'],
                     'congress': other['congress'], 'type': snap['bill']['type'],
                     'topic': snap['bill'].get('topic'), 'stage': snap['stage'],
                     'title': snap['bill']['title'], 'x': snap['features'], 'y': outcome['value'],
                     'source_url': other['source_url'], 'cutoff': snap['cutoff'],
                     'snapshot_hash': snap['snapshot_hash'], 'resolution_id': outcome['id']})
    return sorted(rows, key=lambda r: r['bill_id'])

def sigmoid(z):
    return 1 / (1 + math.exp(-max(-35, min(35, z))))

def fit(rows):
    count, width = len(rows), len(rows[0]['x'])
    means = [sum(r['x'][j] for r in rows) / count for j in range(width)]
    scales = [max(0.1, math.sqrt(sum((r['x'][j] - means[j]) ** 2 for r in rows) / count)) for j in range(width)]
    xs = [[1.] + [(r['x'][j] - means[j]) / scales[j] for j in range(width)] for r in rows]
    rate = (sum(r['y'] for r in rows) + 1) / (count + 2)
    weights = [math.log(rate / (1 - rate))] + [0.] * width
    for _ in range(300):
        gradient = [0.] * (width + 1)
        for row, x in zip(rows, xs):
            error = sigmoid(sum(a * b for a, b in zip(weights, x))) - row['y']
            for j in range(width + 1):
                gradient[j] += error * x[j] / count
        for j in range(width + 1):
            weights[j] -= 0.12 * (gradient[j] + (0.05 * weights[j] if j else 0))
    return {'weights': weights, 'means': means, 'scales': scales, 'iterations': 300, 'l2': 0.05}

def predict(artifact, features):
    x = [1.] + [(v - m) / s for v, m, s in zip(features, artifact['means'], artifact['scales'])]
    return sigmoid(sum(a * b for a, b in zip(artifact['weights'], x)))

def forecast(store, dataset, bill_id, cutoff, persist=True):
    cutoff = timestamp(cutoff)
    saved = store.saved(dataset, bill_id, cutoff, MODEL_VERSION)
    if saved:
        return saved
    snap = snapshot(store, dataset, bill_id, cutoff)
    if not snap:
        return {'status': 'unavailable', 'reason': 'No bill metadata demonstrably available at this cutoff.'}
    if snap['stage'] == 4 or resolution(store, dataset, bill_id, cutoff) or cutoff >= congress_end(snap['bill']['congress']):
        return {'status': 'unavailable', 'reason': 'Target already resolved or Congress ended at this cutoff. Choose an earlier date.'}
    rows = training_rows(store, snap)
    if len(rows) < 20 or len(set(r['y'] for r in rows)) < 2:
        return {'status': 'unavailable', 'reason': 'Need at least 20 resolved prior families, both outcomes, and eligible historical snapshots.', 'training_count': len(rows)}
    artifact = fit(rows)
    base = (sum(r['y'] for r in rows) + 1) / (len(rows) + 2)
    broad = [r for r in rows if r['type'] == snap['bill']['type'] and r['stage'] == snap['stage']]
    narrow = [r for r in broad if r['topic'] == snap['bill'].get('topic')]
    cohort = narrow if len(narrow) >= 10 else broad if len(broad) >= 10 else rows
    rule = 'Earlier Congresses, same chamber, topic and stage, matched age' if cohort is narrow else 'Earlier Congresses, same chamber and stage, matched age' if cohort is broad else 'Earlier Congresses, matched age; sparse matches broadened'
    successes = sum(r['y'] for r in cohort)
    issued = now()
    record = {'status': 'available', 'bill_id': bill_id, 'family_id': snap['bill']['family_id'],
              'dataset': dataset, 'cutoff': cutoff, 'issued_at': issued,
              'track': 'synthetic demonstration' if dataset == 'demo' else 'prospective shadow' if cutoff[:10] == issued[:10] and issued < congress_end(snap['bill']['congress']) and not resolution(store, dataset, bill_id, issued) else 'retrospective reconstruction',
              'target': 'Enactment by Congress end', 'deadline': congress_end(snap['bill']['congress']),
              'model_version': MODEL_VERSION, 'feature_version': FEATURE_VERSION, 'code_version': 'engine-v1',
              'calibration_version': 'none — experimental', 'prompt_version': 'not used',
              'probability': predict(artifact, snap['features']), 'baseline_probability': base,
              'reference_probability': (successes + 5 * base) / (len(cohort) + 5),
              'uncertainty': None, 'uncertainty_note': 'No validated probability interval is available.',
              'snapshot_hash': snap['snapshot_hash'], 'evidence_ids': snap['evidence_ids'],
              'input_snapshot': snap, 'features': snap['features'], 'stage': snap['stage'], 'training_count': len(rows),
              'training_manifest': [{'bill_id': r['bill_id'], 'snapshot_hash': r['snapshot_hash'], 'resolution_id': r['resolution_id']} for r in rows],
              'model_artifact': artifact,
              'cohort': {'rule': rule, 'resolved': len(cohort), 'successes': successes, 'pending': 0,
                         'pending_note': 'Eligibility requires resolved labels; unresolved candidates excluded.',
                         'observed_rate': successes / len(cohort), 'rows': cohort}}
    record['id'] = digest(record)
    return store.save(record) if persist else record

def score(probabilities, labels):
    if not probabilities or len(probabilities) != len(labels):
        raise ValueError('Scoring needs equally sized nonempty probabilities and labels')
    if any(not isinstance(p, (float, int)) or not math.isfinite(p) or not 0 <= p <= 1 for p in probabilities) or any(y not in (0, 1) for y in labels):
        raise ValueError('Invalid probabilities or binary labels')
    n = len(labels)
    bins = []
    for low in range(0, 100, 10):
        pairs = [(p, y) for p, y in zip(probabilities, labels) if low / 100 <= p < (low + 10) / 100 or (low == 90 and p == 1)]
        if pairs:
            bins.append({'lower': low / 100, 'n': len(pairs), 'predicted': sum(p for p, _ in pairs) / len(pairs), 'observed': sum(y for _, y in pairs) / len(pairs)})
    return {'n': n, 'brier': sum((p - y) ** 2 for p, y in zip(probabilities, labels)) / n,
            'log_loss': -sum(y * math.log(max(p, 1e-12)) + (1 - y) * math.log(max(1 - p, 1e-12)) for p, y in zip(probabilities, labels)) / n,
            'base_rate': sum(labels) / n, 'reliability': bins}

def research(store, dataset):
    records = store.ledger(dataset)
    pairs = [(f, resolution(store, dataset, f['bill_id'])) for f in records]
    resolved = [(f, r) for f, r in pairs if r]
    # One earliest locked snapshot per bill prevents heavily covered bills dominating.
    unique = {}
    for f, r in sorted(resolved, key=lambda x: x[0]['cutoff']):
        unique.setdefault(f['bill_id'], (f, r))
    selected = list(unique.values())
    labels = [r['value'] for _, r in selected]
    return {'dataset': dataset, 'ledger_count': len(records), 'pending': sum(r is None for _, r in pairs),
            'resolved_snapshots': len(resolved), 'bills': len(selected),
            'families': len(set(f['family_id'] for f, _ in selected)),
            'metrics': score([f['probability'] for f, _ in selected], labels) if selected else None,
            'baseline': score([f['baseline_probability'] for f, _ in selected], labels) if selected else None,
            'note': 'Development diagnostics; earliest saved snapshot per bill. Not an untouched holdout. Demo results measure synthetic fixtures only.'}


def locked_snapshot(store, record):
    if record.get('input_snapshot'):
        return record['input_snapshot']
    # Compatibility for initial ledger records: resolve exact immutable input IDs.
    rows = []
    for identity in record['evidence_ids']:
        row = store.db.execute('SELECT kind,body FROM records WHERE id=?', (identity,)).fetchone()
        if row:
            import json
            rows.append((row['kind'], json.loads(row['body'])))
    bill = next(body for kind, body in rows if kind == 'bill')
    events = sorted([body for kind, body in rows if kind == 'event'], key=lambda e:(e['effective_at'], e['id']))
    return {'bill': bill, 'events': events, 'cutoff': record['cutoff'], 'stage': record['stage'],
            'stage_name': STAGES[record['stage']], 'features': record['features'],
            'evidence_ids': record['evidence_ids'], 'snapshot_hash': record['snapshot_hash']}
