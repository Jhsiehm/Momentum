"""Day-30 / next-90-days passage research primitives, never live certification.

Inputs are explicit adjudication assertions. This module does not discover labels,
certify historical source availability, train a challenger, or promote a model.
"""
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
import math
import random
import re

from .store import congress_end, digest

VERSION = 'passage90-v1'
TARGET = 'originating_chamber_passage_within_90_days_at_day_30'
STAGES = ('introduced', 'reported', 'unknown')
TIME_BANDS = ('90_to_365_days', 'over_365_days')
PRACTICAL_REDUCTION = 0.02


def _time(value):
    if not isinstance(value, str) or not value:
        raise ValueError('Timestamp must be a nonempty string')
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        value += 'T23:59:59Z'
    try:
        parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError as exc:
        raise ValueError('Invalid timestamp') from exc
    if parsed.tzinfo is None:
        raise ValueError('Timestamp must include a timezone')
    return parsed.astimezone(timezone.utc)


def _stamp(value):
    return value.isoformat().replace('+00:00', 'Z')


def _text(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(name + ' must be a nonempty string')
    return value


def _probability(value):
    if type(value) not in (int, float) or not math.isfinite(value) or not 0 <= value <= 1:
        raise ValueError('Probability must be finite and between zero and one')
    return float(value)


def window(candidate):
    """Validate identity/lifetime and compute a full, untruncated forecast window."""
    if not isinstance(candidate, dict):
        raise ValueError('Candidate must be an object')
    congress = candidate.get('congress')
    if type(congress) is not int or not 1 <= congress <= 500:
        raise ValueError('Invalid Congress')
    kind = candidate.get('type')
    bid = candidate.get('bill_id')
    if kind not in ('hr', 's') or not isinstance(bid, str) or not re.fullmatch(rf'{kind}[1-9][0-9]*-{congress}', bid):
        raise ValueError('Bill identity, type and Congress must agree; H.R./S. only')
    introduced = _time(candidate.get('introduced_at'))
    start, end = _time(congress_end(congress - 1)), _time(congress_end(congress))
    if not start <= introduced < end:
        raise ValueError('Introduction outside Congress')
    cutoff = introduced + timedelta(days=30)
    horizon = cutoff + timedelta(days=90)
    return dict(checkpoint=_stamp(cutoff), horizon=_stamp(horizon), congress_end=_stamp(end),
                full_window=horizon < end)


def _index(items, name):
    if not isinstance(items, list):
        raise ValueError(name + ' must be a list')
    result = {}
    for item in items:
        if not isinstance(item, dict):
            raise ValueError(name + ' entries must be objects')
        bid = _text(item.get('bill_id'), 'bill_id')
        if bid in result:
            raise ValueError('Duplicate ' + name + ' identity: ' + bid)
        result[bid] = item
    return result


def _label(candidate, label, bounds, as_of):
    if label.get('target') != TARGET or type(label.get('value')) is not int or label['value'] not in (0, 1):
        raise ValueError('Explicit binary passage90 target required')
    if not re.fullmatch(r'[0-9a-f]{64}', str(label.get('source_hash', ''))):
        raise ValueError('Label requires a raw source SHA-256')
    for field in ('source_url', 'audit_note'):
        _text(label.get(field), field)
    if not label['source_url'].startswith('https://'):
        raise ValueError('Label source URL must use HTTPS')
    if label.get('complete_coverage') is not True or label.get('first_passage_verified') is not True:
        raise ValueError('Complete action coverage and first-passage adjudication required')
    begin, through = _time(label.get('coverage_from')), _time(label.get('coverage_through'))
    introduced = _time(candidate['introduced_at'])
    checkpoint, horizon, end = (_time(bounds[k]) for k in ('checkpoint', 'horizon', 'congress_end'))
    known = _time(label.get('available_at'))
    passage_raw = label.get('first_passage_at')
    passage = _time(passage_raw) if passage_raw is not None else None
    if begin > introduced or through < begin or known < through:
        raise ValueError('Invalid action-coverage bounds or availability')
    if passage is not None:
        if passage < introduced or passage >= end or through < passage:
            raise ValueError('First passage outside bill lifetime or action coverage')
        if len(passage_raw) == 10 and passage.date() in (checkpoint.date(), horizon.date()):
            return 'boundary_ambiguous', None
        if passage <= checkpoint:
            return 'already_passed', None
    if known > as_of:
        return 'label_pending', None
    if horizon > as_of:
        return 'horizon_pending', None
    if label['value'] == 1:
        if passage is None or not checkpoint < passage <= horizon:
            raise ValueError('Positive requires first passage inside the exact forecast window')
        effective = passage
    else:
        if through < horizon or (passage is not None and passage <= horizon):
            raise ValueError('Negative requires complete horizon coverage and no in-window first passage')
        effective = horizon
    return 'eligible', dict(y=label['value'], label_available_at=_stamp(known),
                            label_effective_at=_stamp(effective), label_hash=digest(label))


def prepare(candidates, labels, as_of, mode='retrospective'):
    """Retain a disposition for every inventory candidate; never infer negatives.

Retrospective rows may use current-rendition assertions and are never certified
historical or prospective evidence. Source review remains an external obligation.
"""
    if mode not in ('retrospective', 'synthetic'):
        raise ValueError('Only retrospective development or synthetic preparation is supported')
    at = _time(as_of)
    inventory, outcomes = _index(candidates, 'candidate'), _index(labels, 'label')
    if outcomes.keys() - inventory.keys():
        raise ValueError('Label identities must belong to the frozen candidate inventory')
    rows, dispositions = [], []
    for bid, candidate in sorted(inventory.items()):
        disposition = dict(bill_id=bid)
        try:
            bounds = window(candidate)
            disposition.update(bounds)
            if not bounds['full_window']:
                disposition['status'] = 'incomplete_90_day_window'
            else:
                family = _text(candidate.get('family_id'), 'family_id')
                stage = candidate.get('stage', 'unknown')
                if stage not in STAGES:
                    raise ValueError('Stage must be introduced, reported, or unknown at checkpoint')
                known = candidate.get('feature_available_at')
                availability = _time(known) if known is not None else None
                if bid not in outcomes:
                    disposition['status'] = 'missing_label'
                else:
                    status, outcome = _label(candidate, outcomes[bid], bounds, at)
                    disposition['status'] = status
                    if status == 'eligible':
                        row = dict(bill_id=bid, family_id=family, congress=candidate['congress'],
                                   chamber='house' if candidate['type'] == 'hr' else 'senate', stage=stage,
                                   checkpoint=bounds['checkpoint'], horizon=bounds['horizon'],
                                   feature_available_at=_stamp(availability) if availability else None,
                                   availability_asserted_by_checkpoint=bool(availability and availability <= _time(bounds['checkpoint'])),
                                   evidence_mode=mode, **outcome)
                        rows.append(row)
        except (ValueError, TypeError, KeyError, OverflowError) as exc:
            disposition.update(status='invalid_evidence', reason=str(exc))
        dispositions.append(disposition)
    counts = dict(sorted(Counter(d['status'] for d in dispositions).items()))
    return dict(version=VERSION, target=TARGET, evidence_mode=mode, as_of=_stamp(at),
                inventory_count=len(inventory), candidates_hash=digest(candidates), labels_hash=digest(labels),
                dispositions=dispositions, counts=counts, rows=rows, release_eligible=False,
                certified_historical=False, certified_prospective=False)


def _rows(rows):
    indexed = _index(rows, 'row')
    for row in indexed.values():
        _text(row.get('family_id'), 'family_id')
        if type(row.get('congress')) is not int or not 1 <= row['congress'] <= 500:
            raise ValueError('Row requires Congress')
        if row.get('chamber') not in ('house', 'senate') or row.get('stage') not in STAGES:
            raise ValueError('Invalid chamber or stage')
        kind = 'hr' if row['chamber'] == 'house' else 's'
        if not re.fullmatch(rf"{kind}[1-9][0-9]*-{row['congress']}", row['bill_id']):
            raise ValueError('Row identity/chamber/Congress mismatch')
        if type(row.get('y')) is not int or row['y'] not in (0, 1):
            raise ValueError('Row outcome must be explicit integer zero or one')
        checkpoint = _time(row.get('checkpoint'))
        horizon = _time(row.get('horizon'))
        if checkpoint < _time(congress_end(row['congress'] - 1)) + timedelta(days=30):
            raise ValueError('Checkpoint precedes the earliest day-30 checkpoint in Congress')
        if horizon - checkpoint != timedelta(days=90):
            raise ValueError('Row must retain the full 90-day window')
        if _time(row['horizon']) >= _time(congress_end(row['congress'])):
            raise ValueError('Row horizon must precede Congress end')
        effective = _time(row.get('label_effective_at'))
        known = _time(row.get('label_available_at'))
        if known < effective:
            raise ValueError('Label availability precedes its effective time')
        if (row['y'] == 0 and effective != horizon) or (row['y'] == 1 and not checkpoint < effective <= horizon):
            raise ValueError('Row label effective time contradicts its target window')
        if row.get('evidence_mode') not in ('retrospective', 'synthetic'):
            raise ValueError('Unsupported row evidence mode')
    if len({r['evidence_mode'] for r in rows}) > 1:
        raise ValueError('Synthetic and real rows cannot be mixed')
    return indexed


def chronological_split(rows, test_congress):
    """A development fold; purge evaluation families before choosing train reps."""
    _rows(rows)
    if type(test_congress) is not int or not 2 <= test_congress <= 500:
        raise ValueError('Invalid evaluation Congress')
    origin = _time(congress_end(test_congress - 1))
    test = [r for r in rows if r['congress'] == test_congress]
    # Reserve current and future evaluation families before any train selection.
    reserved = {r['family_id'] for r in rows if r['congress'] >= test_congress}
    selected, exclusions = {}, []
    for row in sorted(rows, key=lambda r: (r['congress'], r['bill_id'])):
        if row['congress'] >= test_congress:
            continue
        if row['family_id'] in reserved:
            reason = 'evaluation_family_overlap'
        elif _time(row['label_available_at']) > origin or _time(row['label_effective_at']) > origin:
            reason = 'label_unavailable_at_training_origin'
        elif row['family_id'] in selected:
            reason = 'duplicate_training_family'
        else:
            selected[row['family_id']] = row
            continue
        exclusions.append(dict(bill_id=row['bill_id'], reason=reason))
    return dict(training_origin=_stamp(origin), train=list(selected.values()), test=test,
                exclusions=exclusions, release_eligible=False)


def remaining_time_band(row):
    remaining = _time(congress_end(row['congress'])) - _time(row['checkpoint'])
    if remaining <= timedelta(days=90):
        raise ValueError('Full 90-day window must end strictly before Congress end')
    return TIME_BANDS[0] if remaining <= timedelta(days=365) else TIME_BANDS[1]


def fit_reference(train):
    """Fixed Beta(1,1) rate and stage/chamber shrinkage; training rows only."""
    _rows(train)
    if not train or len({r['y'] for r in train}) != 2:
        raise ValueError('Reference experiment requires nonempty training with both classes')
    if len({r['family_id'] for r in train}) != len(train):
        raise ValueError('Use one training representative per family')
    rate = (sum(r['y'] for r in train) + 1) / (len(train) + 2)
    counts, bands = {}, {}
    for chamber in ('house', 'senate'):
        for stage in STAGES:
            group = [r for r in train if r['chamber'] == chamber and r['stage'] == stage]
            n, events = len(group), sum(r['y'] for r in group)
            key = chamber + ':' + stage
            stage_rate = (events + 5 * rate) / (n + 5)
            counts[key] = dict(n=n, events=events, probability=stage_rate)
            for band in TIME_BANDS:
                subgroup = [r for r in group if remaining_time_band(r) == band]
                sub_n, sub_events = len(subgroup), sum(r['y'] for r in subgroup)
                bands[key + ':' + band] = dict(n=sub_n, events=sub_events,
                    probability=(sub_events + 5 * stage_rate) / (sub_n + 5))
    artifact = dict(version=VERSION, target=TARGET, evidence_mode=train[0]['evidence_mode'],
                    global_rate=rate, groups=counts, time_groups=bands,
                    training_ids=sorted(r['bill_id'] for r in train),
                    training_families=sorted(r['family_id'] for r in train),
                    training_hash=digest(train), max_training_congress=max(r['congress'] for r in train),
                    latest_label_available_at=max(_time(r['label_available_at']) for r in train).isoformat(),
                    latest_label_effective_at=max(_time(r['label_effective_at']) for r in train).isoformat())
    artifact['id'] = digest(artifact)
    return artifact


def predict_reference(artifact, row):
    """Reject changed artifacts, same/future-period fitting and family leakage."""
    _rows([row])
    body = {k: v for k, v in artifact.items() if k != 'id'}
    if artifact.get('id') != digest(body) or artifact.get('target') != TARGET or artifact.get('version') != VERSION:
        raise ValueError('Reference artifact integrity or target mismatch')
    if artifact.get('evidence_mode') != row['evidence_mode']:
        raise ValueError('Reference training/evaluation evidence modes must match')
    origin = _time(congress_end(row['congress'] - 1))
    if artifact['max_training_congress'] >= row['congress'] or row['family_id'] in artifact['training_families']:
        raise ValueError('Reference training crosses time or family boundary')
    if any(_time(artifact[key]) > origin for key in ('latest_label_available_at', 'latest_label_effective_at')):
        raise ValueError('Reference training labels were not available at fold origin')
    key = row['chamber'] + ':' + row['stage'] + ':' + remaining_time_band(row)
    return _probability(artifact['time_groups'][key]['probability'])


def _metric(rows, probabilities, top_k):
    n = len(rows)
    events = sum(r['y'] for r in rows)
    brier = sum((p - r['y']) ** 2 for r, p in zip(rows, probabilities)) / n
    clipped = [min(1 - 1e-15, max(1e-15, p)) for p in probabilities]
    log_loss = -sum(r['y'] * math.log(p) + (1 - r['y']) * math.log(1 - p) for r, p in zip(rows, clipped)) / n
    bins = []
    for index in range(10):
        selected = [(r, p) for r, p in zip(rows, probabilities) if min(int(p * 10), 9) == index]
        bins.append(dict(lower=index / 10, upper=(index + 1) / 10, n=len(selected),
                         events=sum(r['y'] for r, _ in selected),
                         mean_probability=sum(p for _, p in selected) / len(selected) if selected else None,
                         event_rate=sum(r['y'] for r, _ in selected) / len(selected) if selected else None))
    classes = {}
    for outcome, name in ((0, 'negative'), (1, 'positive')):
        selected = [(r, probability) for r, probability in zip(rows, probabilities) if r['y'] == outcome]
        classes[name] = dict(n=len(selected),
            brier=sum((probability - r['y']) ** 2 for r, probability in selected) / len(selected) if selected else None)
    ranked = sorted(zip(rows, probabilities), key=lambda pair: (-pair[1], pair[0]['bill_id']))[:top_k]
    hits = sum(r['y'] for r, _ in ranked)
    precision = hits / len(ranked)
    return dict(n=n, events=events, brier=brier, log_loss=log_loss,
                expected_events=sum(probabilities), reliability_bins=bins, class_metrics=classes,
                top_k=dict(requested=top_k, n=len(ranked), events=hits, precision=precision,
                           recall=hits / events if events else None,
                           lift=precision / (events / n) if events else None,
                           bill_ids=[r['bill_id'] for r, _ in ranked]))


def _quantile(values, p):
    ordered = sorted(values)
    location = p * (len(ordered) - 1)
    lower, upper = math.floor(location), math.ceil(location)
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (location - lower)


def evaluate_paired(rows, predictions, challenger='structured', reference='stage_reference',
                    top_k=20, bootstrap_draws=10000, evaluation_as_of=None):
    """Descriptive development evaluation; never an independent success verdict.

Predictions are {model: [{bill_id, probability, checkpoint, target}, ...]}; every
arm must cover exactly the same supplied, already-frozen row population.
"""
    indexed = _rows(rows)
    if not rows:
        raise ValueError('Cannot evaluate an empty population')
    actual_now = datetime.now(timezone.utc)
    evaluation_time = _time(evaluation_as_of) if evaluation_as_of is not None else actual_now.replace(microsecond=0)
    if rows[0]['evidence_mode'] == 'retrospective':
        if evaluation_time > actual_now:
            raise ValueError('Real evaluation cutoff cannot be in the future')
        if any(_time(row[key]) > evaluation_time for row in rows
               for key in ('horizon', 'label_available_at', 'label_effective_at')):
            raise ValueError('All real evaluation horizons and labels must be available by the evaluation cutoff')
    if type(top_k) is not int or top_k < 1 or type(bootstrap_draws) is not int or not 1 <= bootstrap_draws <= 100000:
        raise ValueError('Invalid prioritization or bootstrap configuration')
    if not isinstance(predictions, dict) or challenger == reference or not {challenger, reference} <= predictions.keys():
        raise ValueError('Distinct paired challenger and reference required')
    matrices = {}
    for name, items in predictions.items():
        _text(name, 'model name')
        values = _index(items, 'prediction')
        if values.keys() != indexed.keys():
            raise ValueError('Every model must predict the identical full case population')
        for bid, value in values.items():
            if value.get('target') != TARGET or _time(value.get('checkpoint')) != _time(indexed[bid]['checkpoint']):
                raise ValueError('Prediction target or checkpoint mismatch')
        matrices[name] = [_probability(values[r['bill_id']].get('probability')) for r in rows]
    periods = sorted({r['congress'] for r in rows})
    by_period = {}
    for period in periods:
        positions = [i for i, r in enumerate(rows) if r['congress'] == period]
        by_period[str(period)] = {name: _metric([rows[i] for i in positions], [ps[i] for i in positions], top_k)
                                  for name, ps in matrices.items()}
    means = {name: {key: sum(by_period[str(c)][name][key] for c in periods) / len(periods)
                    for key in ('brier', 'log_loss')} for name in matrices}
    base_loss = means[reference]['brier']
    contrast = means[challenger]['brier'] - .98 * base_loss
    groups = defaultdict(list)
    for i, row in enumerate(rows):
        groups[row['family_id']].append(i)
    families = sorted(groups)
    rng = random.Random(20261112)
    deltas, practical = [], []
    for _ in range(bootstrap_draws):
        positions = [i for family in rng.choices(families, k=len(families)) for i in groups[family]]
        period_values = []
        for period in periods:
            selected = [i for i in positions if rows[i]['congress'] == period]
            if not selected:
                break
            c = sum((matrices[challenger][i] - rows[i]['y']) ** 2 for i in selected) / len(selected)
            b = sum((matrices[reference][i] - rows[i]['y']) ** 2 for i in selected) / len(selected)
            period_values.append((c - b, c - .98 * b))
        if len(period_values) == len(periods):
            deltas.append(sum(x[0] for x in period_values) / len(periods))
            practical.append(sum(x[1] for x in period_values) / len(periods))
    intervals = {name: [_quantile(values, .025), _quantile(values, .975)] if values else None
                 for name, values in (('ordinary_difference', deltas), ('practical_2pct_contrast', practical))}
    return dict(version=VERSION, target=TARGET, evidence_mode=rows[0]['evidence_mode'],
                n=len(rows), events=sum(r['y'] for r in rows), family_count=len(groups),
                evaluation_as_of=_stamp(evaluation_time),
                by_period=by_period, equal_period_means=means,
                pooled_metrics={name: _metric(rows, ps, top_k) for name, ps in matrices.items()},
                paired_brier_difference=means[challenger]['brier'] - base_loss,
                brier_skill=1 - means[challenger]['brier'] / base_loss if base_loss else None,
                practical_2pct_contrast=contrast,
                bootstrap=dict(seed=20261112, requested=bootstrap_draws, valid=len(deltas),
                               intervals_95pct=intervals, registered_draw_count=bootstrap_draws == 10000,
                               valid_draw_floor_met=len(deltas) >= 9000),
                coverage_note='Paired coverage of supplied rows only; consult the entire preparation inventory for exclusions.',
                diagnostic_status='inconclusive_one_class' if len({r['y'] for r in rows}) < 2 else 'descriptive_only',
                independent_success=False, release_eligible=False,
                limitation='Descriptive development comparison; source truth, training, selection, period and future-Congress uncertainty are not certified.')
