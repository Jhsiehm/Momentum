"""Fail-closed, label-separated paper evaluation. No acquisition or promotion.

Reviews are externally supplied attestations, not automatic human certification.
Only synthetic fixtures are exercised during research preparation.
"""
import hashlib
import json
import math
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .model import predict
from .store import congress_end, digest, timestamp
from .three_model_experiment import calibrate

TARGET = 'own_bill_public_law_by_congress_end'
FEATURES = 'publication_v2_six_day180'
NAMES = ('survivor', 'challenger', 'rate', 'stage')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def seal(body):
    # JSON roundtrip detaches the object and rejects NaN/Infinity.
    body = json.loads(json.dumps(body, allow_nan=False))
    return {'body': body, 'hash': digest(body)}


def unseal(envelope):
    require(digest(envelope['body']) == envelope['hash'], 'Manifest hash mismatch')
    return envelope['body']


def save(path, envelope):
    unseal(envelope)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation: divergent AND identical overwrites are refused.
    with path.open('x') as out:
        json.dump(envelope, out, sort_keys=True, indent=2, allow_nan=False)
        out.write('\n')


def unique(rows):
    ids = [r['bill_id'] for r in rows]
    require(len(ids) == len(set(ids)), 'Duplicate bill identity')
    return set(ids)


def proofs(items, root):
    require(bool(items), 'Missing source evidence')
    for item in items:
        path = Path(root) / item['path']
        require(path.is_file(), 'Missing source bytes')
        require(hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256'], 'Source hash mismatch')
        require(bool(item.get('url')), 'Missing source URL')


def reviewed(review, subject_hash, root):
    require(review.get('subject_hash') == subject_hash, 'Review subject mismatch')
    require(review.get('decision') == 'pass' and bool(review.get('reviewer')), 'Missing independent review')
    proofs(review.get('evidence', []), root)


def case(row, root):
    require(row['target'] == TARGET and row['feature_version'] == FEATURES, 'Wrong target/features')
    require(type(row['congress']) is int and row['type'] in ('hr', 's'), 'Invalid population')
    prefix = f"{row['congress']}-{row['type']}"
    require(row['bill_id'].startswith(prefix) and row['bill_id'][len(prefix):].isdigit(), 'Identity mismatch')
    cutoff = timestamp(row['cutoff'])
    intro = datetime.fromisoformat(timestamp(row['introduced_at']).replace('Z', '+00:00'))
    require(f'{1787 + 2 * row["congress"]:04d}-01-03T17:00:00Z' <= timestamp(row['introduced_at']) < congress_end(row['congress']), 'Introduction outside Congress')
    require(cutoff == timestamp((intro + timedelta(days=180)).isoformat()), 'Wrong checkpoint')
    require(cutoff < congress_end(row['congress']), 'Checkpoint after Congress horizon')
    require(row.get('at_risk') is True and bool(row.get('family_id')), 'Missing risk/family audit')
    x = row['x']
    require(len(x) == 6 and all(type(v) in (int, float) and math.isfinite(v) and 0 <= v <= 1 for v in x), 'Invalid feature vector')
    require(type(row['stage']) is int and row['stage'] in range(4), 'Invalid stage')
    require(x[0] == row['stage']/4 and x[1] == 180/730 and x[4] == int(row['type'] == 's'), 'Inconsistent features')
    proofs(row.get('sources', []), root)
    require(timestamp(row['features_available_at']) <= cutoff and timestamp(row['features_effective_at']) <= cutoff, 'Future feature evidence')
    reviewed(row['review'], digest({k:v for k,v in row.items() if k != 'review'}), root)


def label(row, value, root):
    require(value['bill_id'] == row['bill_id'] and value['target'] == TARGET, 'Wrong label identity/target')
    require(type(value['value']) is int and value['value'] in (0, 1), 'Invalid binary outcome')
    effective, available = timestamp(value['effective_at']), timestamp(value['available_at'])
    require(available >= effective, 'Label available before effective time')
    end = congress_end(row['congress'])
    if value['value']:
        require(timestamp(row['cutoff']) < effective < end, 'Positive outside risk horizon')
        require(effective[:10] not in (timestamp(row['cutoff'])[:10], end[:10]), 'Ambiguous boundary-day enactment')
    else:
        require(value.get('complete_coverage') is True and timestamp(value['coverage_through']) >= end and effective >= end, 'Unproven negative')
    proofs(value.get('sources', []), root)
    reviewed(value['review'], digest({k:v for k,v in value.items() if k != 'review'}), root)


def implementation_hashes():
    return {name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
            for name in ('paper_evaluation.py', 'model.py', 'store.py', 'three_model_experiment.py')}


def validate_model(artifact):
    require(len(artifact['weights']) == 7 and len(artifact['means']) == 6 and len(artifact['scales']) == 6,
            'Invalid model dimensions')
    require(all(type(v) in (int, float) and math.isfinite(v)
                for key in ('weights', 'means', 'scales') for v in artifact[key]), 'Invalid model numbers')
    require(all(v > 0 for v in artifact['scales']), 'Invalid model scales')


def register(spec, path):
    require(spec['target'] == TARGET and spec['feature_version'] == FEATURES, 'Wrong protocol target')
    require(spec['mode'] in ('synthetic', 'prospective'), 'No unexposed historical period established')
    require(spec['candidates'] and len(spec['candidates']) == len(set(spec['candidates'])), 'Invalid candidate census')
    require(spec['periods'] == sorted(set(spec['periods'])), 'Invalid periods')
    require(set(spec['models']) == {'survivor', 'challenger'}, 'Require both frozen models')
    require(bool(spec['paper_protocol_sha256']), 'Missing paper protocol hash')
    exposure = spec.get('exposure_registry')
    require(isinstance(exposure, dict), 'Missing exposed-development registry')
    for key in ('bill_ids', 'family_ids'):
        values = exposure.get(key)
        require(isinstance(values, list) and all(isinstance(v, str) and v for v in values)
                and len(values) == len(set(values)), 'Invalid exposure registry identities')
    require(bool(exposure.get('scope')) and bool(exposure.get('review')), 'Unreviewed exposure registry')
    result = seal(dict(spec=spec, code_hashes=implementation_hashes(), registered_at=datetime.now(timezone.utc).isoformat()))
    save(path, result)
    return result


def prepare(registration, cases, exclusions, models, baseline_training, root):
    """Freeze identical predictions before evaluation labels are supplied.

    models[name] = {artifact, training}; training rows contain a separate label.
    Artifact hashes and training hashes must match the registered specification.
    No model is retrained, and this function does not inspect evaluation labels.
    """
    registered = unseal(registration)
    spec = registered['spec']
    require(registered['code_hashes'] == implementation_hashes(), 'Registered implementation changed')
    require(not any('label' in r or 'y' in r or 'outcome' in r for r in cases), 'Evaluation labels must be separate')
    selected, excluded = unique(cases), unique(exclusions)
    require(not selected & excluded and selected | excluded == set(spec['candidates']), 'Incomplete candidate disposition')
    require(cases and all(r.get('reason') and r.get('review') for r in exclusions), 'Empty or unaudited disposition')
    for row in exclusions:
        reviewed(row['review'], digest({k:v for k,v in row.items() if k != 'review'}), root)
    require(set(models) == {'survivor', 'challenger'}, 'Missing model')
    expected_dataset = 'demo' if spec['mode'] == 'synthetic' else 'official'
    for row in cases:
        require(row.get('dataset') == expected_dataset, 'Dataset/mode mismatch')
        case(row, root)
        require(row['congress'] in spec['periods'], 'Unregistered period')
    exposure = spec['exposure_registry']
    reviewed(exposure['review'], digest({k:v for k,v in exposure.items() if k != 'review'}), root)
    families = {r['family_id'] for r in cases}
    require(not selected.intersection(exposure['bill_ids']) and not families.intersection(exposure['family_ids']),
            'Evaluation overlaps exposed development evidence')
    origin = min(timestamp(r['cutoff']) for r in cases)
    train_sets = [baseline_training] + [models[n]['training'] for n in ('survivor', 'challenger')]
    require(digest(baseline_training) == spec['baseline_training_hash'], 'Baseline membership changed')
    for rows in train_sets:
        require(len(rows) >= 20 and {r['label']['value'] for r in rows} == {0, 1}, 'Training computation floor unmet')
        unique(rows)
        require(len({r['family_id'] for r in rows}) == len(rows), 'Duplicate training family')
        for r in rows:
            require(r.get('dataset') == expected_dataset, 'Dataset/mode mismatch')
            case({k:v for k,v in r.items() if k != 'label'}, root)
            label(r, r['label'], root)
            require(r['family_id'] not in families and r['bill_id'] not in selected, 'Training/evaluation overlap')
            require(r['congress'] < min(spec['periods']) and timestamp(r['label']['available_at']) < origin, 'Training not earlier/knowable')
    for name in ('survivor', 'challenger'):
        item = models[name]
        require(digest(item['artifact']) == spec['models'][name]['artifact_hash'], 'Frozen artifact mismatch')
        require(digest(item['training']) == spec['models'][name]['training_hash'], 'Model training changed')
    validate_model(models['survivor']['artifact'])
    validate_model(models['challenger']['artifact']['model']['base'])
    adjustment = models['challenger']['artifact']['model']['calibration']
    require(all(type(adjustment[k]) in (int,float) and math.isfinite(adjustment[k]) for k in ('intercept','slope')) and adjustment['slope'] >= 0, 'Invalid calibration')
    # All baselines are frozen once, using the registered earlier risk set.
    rate = (sum(r['label']['value'] for r in baseline_training)+1)/(len(baseline_training)+2)
    stages = {}
    for s in range(4):
        group = [r for r in baseline_training if r['stage'] == s]
        stages[str(s)] = (sum(r['label']['value'] for r in group)+5*rate)/(len(group)+5)
    pairs = []
    for row in cases:
        original = models['survivor']['artifact']
        challenger = models['challenger']['artifact']['model']
        p = {'survivor': predict(original, row['x']),
             'challenger': calibrate(challenger['calibration'], predict(challenger['base'], row['x'])),
             'rate': rate, 'stage': stages[str(row['stage'])]}
        require(all(math.isfinite(v) and 0 <= v <= 1 for v in p.values()), 'Nonfinite prediction')
        pairs.append(dict(bill_id=row['bill_id'], family_id=row['family_id'], congress=row['congress'], probabilities=p))
    return seal(dict(registration_hash=registration['hash'], cases=cases, exclusions=exclusions,
                     models=models, baseline_training=baseline_training, rate=rate, stage_rates=stages,
                     predictions=pairs, release_eligible=False))


def metrics(probabilities, outcomes):
    require(len(probabilities) == len(outcomes) and bool(outcomes), 'Unpaired/empty score')
    require(all(type(y) is int and y in (0, 1) for y in outcomes), 'Invalid outcome')
    require(all(type(p) in (int,float) and math.isfinite(p) and 0 <= p <= 1 for p in probabilities), 'Invalid probability')
    n = len(outcomes)
    brier = math.fsum((p-y)**2 for p,y in zip(probabilities,outcomes))/n
    clipped = [min(1-1e-12,max(1e-12,p)) for p in probabilities]
    loss = -math.fsum(y*math.log(p)+(1-y)*math.log1p(-p) for p,y in zip(clipped,outcomes))/n
    bins = []
    for i in range(10):
        group = [(p,y) for p,y in zip(probabilities,outcomes) if min(9,int(p*10)) == i]
        bins.append(dict(lower=i/10, upper=(i+1)/10, n=len(group),
                         mean_probability=math.fsum(p for p,y in group)/len(group) if group else None,
                         event_rate=sum(y for p,y in group)/len(group) if group else None))
    return dict(n=n, positives=sum(outcomes), expected_events=math.fsum(probabilities),
                mean_probability=math.fsum(probabilities)/n, event_rate=sum(outcomes)/n,
                brier=brier, log_loss=loss, calibration=bins,
                event_brier={str(y):math.fsum((p-v)**2 for p,v in zip(probabilities,outcomes) if v==y)/outcomes.count(y) if y in outcomes else None for y in (0,1)})


def evaluate(registration, prepared, labels, root, authorization=None):
    """Future custodian entrypoint; no real evaluation is run in preparation.

    The local receipt gate is not an access-control system. A custodian must
    protect labels and attest independence outside this process.
    """
    registered = unseal(registration)
    spec = registered['spec']
    require(registered['code_hashes'] == implementation_hashes(), 'Registered implementation changed')
    body = unseal(prepared)
    require(body['registration_hash'] == registration['hash'], 'Wrong registration')
    # Recompute features-to-predictions and all source gates, never trust a report.
    require(prepare(registration, body['cases'], body['exclusions'], body['models'], body['baseline_training'], root) == prepared, 'Prediction replay mismatch')
    if spec['mode'] != 'synthetic':
        require(authorization is not None, 'Protected scoring requires custodian release')
        reviewed(authorization, prepared['hash'], root)
        require(authorization.get('independence_confirmed') is True, 'Exposure not certified')
        # Prospective paired issuance is deliberately not inferred from historic cutoffs.
        raise ValueError('Prospective issuance adapter and externally attested ledger not yet certified')
    require(unique(labels) == {r['bill_id'] for r in body['cases']}, 'Missing/extra labels')
    lookup = {r['bill_id']:r for r in labels}
    for row in body['cases']:
        label(row, lookup[row['bill_id']], root)
    reports = {}
    for c in spec['periods']:
        pairs = [p for p in body['predictions'] if p['congress']==c]
        require(pairs, 'Empty registered evaluation period')
        ys = [lookup[p['bill_id']]['value'] for p in pairs]
        report = {name:metrics([p['probabilities'][name] for p in pairs],ys) for name in NAMES}
        for value in report.values():
            value['brier_skill_vs_rate'] = 1-value['brier']/report['rate']['brier'] if report['rate']['brier'] else None
            value['brier_skill'] = {name: 1-value['brier']/report[name]['brier'] if report[name]['brier'] else None for name in NAMES}
        reports[str(c)] = report
    equal = {name:math.fsum(r[name]['brier'] for r in reports.values())/len(reports) for name in NAMES}
    return seal(dict(prepared_hash=prepared['hash'], labels_hash=digest(labels), periods=reports,
                     equal_period_brier=equal,
                     equal_period_challenger_brier_skill={name:1-equal['challenger']/equal[name] if equal[name] else None for name in NAMES},
                     synthetic=True, release_eligible=False, uncertainty='No population inference from synthetic checks'))
