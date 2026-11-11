"""Two frozen retrospective fits; source-feature population is sealed before labels."""
import argparse
from collections import Counter
import datetime as dt
import hashlib
import json
from pathlib import Path
import signal

import numpy as np
import scipy
from scipy import sparse
from scipy.special import expit

from scripts import action_context_features_v1 as feature_api
from scripts import action_outcome_resolver_v1 as outcome_api
from scripts import matched_text_sparse_v1 as solver
from scripts.retrospective_text_diagnostic_v1 import metric, bootstrap

VERSION = 'action-context-diagnostic-v2'
FAMILY_SELECTION_VERSION = 'official-context-diagnostic-v1'
ARMS = ('anchor', 'context')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, value):
    raw = json.dumps(value, sort_keys=True, indent=2, allow_nan=False).encode()
    with Path(path).open('xb') as stream:
        stream.write(raw)
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def role(row):
    c = row['congress']
    require(type(c) is int and 113 <= c <= 118, 'Unsupported Congress')
    return 'train' if c <= 116 else str(c)


def valid_feature(row):
    require(isinstance(row['bill_id'], str), 'Identity must be string')
    anchor = row.get('anchor')
    if anchor is None or row.get('feature_errors'):
        return False
    require(len(anchor) == 2 and all(type(x) in (int, float) and np.isfinite(x) for x in anchor), 'Two finite anchor columns required')
    require(type(row['stage']) is int and row['stage'] in range(4) and abs(anchor[0] * 3 - row['stage']) < 1e-12, 'Stage/anchor disagreement')
    context, missing = row['context'], row['missing']
    require(len(context) == len(missing) == 3, 'Three context values/indicators required')
    for x, m in zip(context, missing):
        require(type(m) is int and m in (0, 1) and m == int(x is None), 'Missingness disagreement')
        require(x is None or (type(x) in (int, float) and np.isfinite(x)), 'Context must be finite or null')
    cutoff = dt.date.fromisoformat(row['cutoff'])
    end = dt.date.fromisoformat(row['congress_end'])
    require(cutoff.isoformat() == row['cutoff'] and cutoff < end, 'Invalid cutoff')
    role(row)
    return True


def family_population(rows, protected):
    """Build all known edges before selecting one representative per component."""
    lookup = {r['bill_id']: r for r in rows}
    require(len(lookup) == len(rows), 'Duplicate feature identities')
    parent = {}
    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        a, b = find(a), find(b)
        if a != b:
            parent[max(a, b)] = min(a, b)
    for row in rows:
        find(row['bill_id'])
        for related in row.get('related', []):
            union(row['bill_id'], related)
    for bid, family in protected['known_family_assignments'].items():
        union(bid, 'known-family:' + family)
    forbidden = set(protected['excluded_ids']) | {'known-family:' + f for f in protected['banned_family_ids']}
    banned_roots = {find(x) for x in forbidden}
    groups = {}
    for node in sorted(parent):
        groups.setdefault(find(node), []).append(node)
    graph = [{'family_id': root, 'nodes': nodes, 'protected': root in banned_roots} for root, nodes in sorted(groups.items())]
    accepted, exclusions = [], []
    candidates = {}
    priority = {'train': 0, '117': 1, '118': 2}
    component_priority = {}
    for row in rows:
        family = find(row['bill_id'])
        component_priority[family] = max(component_priority.get(family, -1), priority[role(row)])
    for row in rows:
        bid = row['bill_id']; family = find(bid)
        if family in banned_roots:
            exclusions.append({'bill_id': bid, 'reason': 'protected_or_exposed_family', 'family_id': family})
        elif not valid_feature(row):
            exclusions.append({'bill_id': bid, 'reason': 'source_feature_ineligible', 'family_id': family})
        else:
            candidates.setdefault(family, []).append(row)
    for family, members in sorted(candidates.items()):
        top = component_priority[family]
        available = [r for r in members if priority[role(r)] == top]
        if not available:
            exclusions.extend({'bill_id': r['bill_id'], 'family_id': family, 'reason': 'family_later_period_source_feature_ineligible'} for r in members)
            continue
        winner = min(available, key=lambda r: hashlib.sha256((FAMILY_SELECTION_VERSION+'\n'+r['bill_id']).encode()).hexdigest())
        accepted.append(dict(winner, family_id=family, role=role(winner)))
        for r in members:
            if r['bill_id'] != winner['bill_id']:
                exclusions.append({'bill_id': r['bill_id'], 'family_id': family,
                                   'reason': 'family_later_period_priority' if priority[role(r)] < top else 'within_role_family_representative',
                                   'representative': winner['bill_id']})
    return {'rows': sorted(accepted, key=lambda r: (r['role'], r['bill_id'])), 'exclusions': exclusions, 'graph': graph}


def population_changes(previous, current):
    """Report source-only adaptive membership changes; never influence selection."""
    old = {r['family_id']: r for r in previous['rows']}
    new = {r['family_id']: r for r in current['rows']}
    require(len(old) == len(previous['rows']) and len(new) == len(current['rows']), 'Repeated family representatives')
    entries = []
    for family in sorted(set(old) | set(new)):
        a, b = old.get(family), new.get(family)
        before = {'bill_id': a['bill_id'], 'role': a['role']} if a else None
        after = {'bill_id': b['bill_id'], 'role': b['role']} if b else None
        if before == after:
            continue
        disposition = 'added' if a is None else 'removed' if b is None else 'representative_or_role_changed'
        entries.append({'family_id': family, 'before': before, 'after': after, 'disposition': disposition,
                        'design_change': 'New action-anchor eligibility replaces publication-anchor eligibility; labels unused',
                        'prior_family_exclusions': [r for r in previous['exclusions'] if r.get('family_id') == family],
                        'new_family_exclusions': [r for r in current['exclusions'] if r.get('family_id') == family]})
    old_ids = {r['bill_id'] for r in previous['rows']}; new_ids = {r['bill_id'] for r in current['rows']}
    return {'previous_n': len(old_ids), 'current_n': len(new_ids), 'added_ids': sorted(new_ids-old_ids),
            'removed_ids': sorted(old_ids-new_ids), 'family_changes': entries, 'labels_used': False}


def label_delta(before, after, cases, population_rows):
    """Complete case ledger; only corroborated prior unknowns may gain labels."""
    require(set(before) == set(after), 'Label population changed')
    contract = {r['bill_id']: r for r in cases}
    require(len(contract) == len(cases), 'Duplicate contract case')
    require(set(contract) <= set(before), 'Contract identity outside population')
    approved = {bid for bid, r in contract.items() if
                r['all_problem_dates_match_concordant'] is True
                and r['concordant_date_count'] == 1
                and r['concordant_numbers_equal_law_list'] is True
                and r['public_law_identity_count'] == 1
                and r['concordant_assertion_count'] > 0}
    features = {r['bill_id']:r for r in population_rows}
    require(set(features) == set(before), 'Delta feature population mismatch')
    rows, violations = [], []
    for bid in sorted(before):
        old, new = before[bid], after[bid]
        require(old['bill_id'] == new['bill_id'] == bid, 'Delta identity mismatch')
        reason = None
        if bid in contract and old['y'] is not None:
            reason = 'contract_case_not_previously_unknown'
        elif bid not in contract and new != old:
            reason = 'outside_contract_changed'
        elif old['y'] is not None and new != old:
            reason = 'previously_resolved_label_changed'
        elif old['y'] is None and new['y'] is not None and (bid not in approved or new['y'] != 1):
            reason = 'uncorroborated_or_negative_transition'
        if old['y'] is None and new['y'] == 1:
            enacted = new.get('enacted_at')
            if not isinstance(enacted, str) or not features[bid]['cutoff'] < enacted < features[bid]['congress_end'] or new.get('label_matured_at') != enacted:
                reason = 'positive_horizon_or_maturity_violation'
        if reason:
            violations.append({'bill_id': bid, 'reason': reason})
        rows.append({'bill_id': bid, 'before': old, 'after': new,
                     'contract_case': bid in contract, 'corroborated_contract': bid in approved,
                     'label_changed': old['y'] != new['y'], 'record_changed': old != new})
    return {'population_n': len(rows), 'contract_n': len(contract), 'corroborated_n': len(approved),
            'uncorroborated_n': len(contract)-len(approved), 'rows': rows, 'violations': violations,
            'label_changes': sum(r['label_changed'] for r in rows)}


def fit_adapter(training):
    require(training and all(r['role'] == 'train' for r in training), 'Training-only adapter required')
    require(all(valid_feature(r) for r in training), 'Invalid training feature')
    medians = []
    for j in range(3):
        values = [r['context'][j] for r in training if r['context'][j] is not None]
        require(values, 'Entirely missing training context field '+str(j))
        medians.append(float(np.median(values)))
    raw = raw_matrix(training, medians)
    means, scales = raw.mean(axis=0), np.maximum(raw.std(axis=0, ddof=0), .1)
    require(np.isfinite(means).all() and np.isfinite(scales).all(), 'Scaling overflow')
    return {'version': VERSION, 'columns': 8, 'training_ids': [r['bill_id'] for r in training],
            'medians': medians, 'means': means.tolist(), 'scales': scales.tolist(), 'floor': .1, 'ddof': 0}


def raw_matrix(rows, medians):
    require(rows and len(medians) == 3 and all(valid_feature(r) for r in rows), 'Invalid transform rows')
    matrix = np.array([r['anchor'] + [medians[j] if x is None else x for j, x in enumerate(r['context'])] + r['missing'] for r in rows], dtype=np.float64)
    require(matrix.shape == (len(rows), 8) and np.isfinite(matrix).all(), 'Invalid eight-column matrix')
    return matrix


def transform(rows, adapter):
    require(adapter['version'] == VERSION and adapter['columns'] == 8 and adapter['floor'] == .1 and adapter['ddof'] == 0, 'Invalid adapter')
    raw = raw_matrix(rows, adapter['medians'])
    means, scales = np.asarray(adapter['means']), np.asarray(adapter['scales'])
    require(means.shape == scales.shape == (8,) and np.isfinite(means).all() and np.isfinite(scales).all() and (scales >= .1).all(), 'Invalid scaler parameters')
    return raw, sparse.csr_matrix((raw-means)/scales)


def resolve_population(population, labels):
    kept, exclusions = [], []
    for row in population['rows']:
        label = labels[row['bill_id']]
        require(label['bill_id'] == row['bill_id'], 'Outcome identity mismatch')
        if label['y'] is None:
            exclusions.append({'bill_id': row['bill_id'], 'reason': 'unknown_or_out_of_risk_label', 'label_reason': label['reason']})
            continue
        require(type(label['y']) is int and label['y'] in (0, 1), 'Invalid outcome')
        matured = dt.date.fromisoformat(label['label_matured_at'])
        require(matured.isoformat() == label['label_matured_at'], 'Invalid maturity date')
        kept.append(dict(row, y=label['y'], label=label))
    for group in ('train', '117', '118'):
        require(any(r['role'] == group for r in kept), 'Empty role after labels: '+group)
    earliest = min(r['cutoff'] for r in kept if r['role'] != 'train')
    require(all(r['label']['label_matured_at'] < earliest for r in kept if r['role'] == 'train'), 'Training labels not matured before evaluation')
    require({r['y'] for r in kept if r['role'] == 'train'} == {0, 1}, 'Both training classes required')
    return kept, exclusions


def context_bootstrap(folds):
    # Frozen implementation uses the name text; only this adapter renames it.
    mapped = [{'predictions': [dict(r, text=r['context']) for r in f['predictions']]} for f in folds]
    result = bootstrap(mapped)
    if result['intervals'] is not None:
        result['intervals'] = {k.replace('text_', 'context_'): v for k, v in result['intervals'].items()}
    return result


def run(source, output, features_source, predecessor_population, stopped_run, contract_audit):
    require(np.__version__ == '2.0.2' and scipy.__version__ == '1.13.1', 'Pinned environment required')
    require('data' in output.resolve().parts, 'Ignored runtime output required')
    output.mkdir(parents=True, exist_ok=False)
    fit_count = 0
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError('Six-hour fit-stage cap')))
    signal.alarm(21600)
    try:
        acquisition = read(source/'registration.json')
        acquisition_result = read(source/'result.json')
        require(acquisition_result['labels_read'] is False and acquisition_result['model_fits'] == 0, 'Acquisition must be source-only')
        amendment = read(features_source/'registration.json')
        require(Path(amendment['original_acquisition']).resolve() == source.resolve(), 'Wrong amendment source acquisition')
        require(amendment['selected'] == acquisition['selected'], 'Amendment changed selected population')
        require(amendment.get('network_requests') == 0 and amendment.get('labels_read') is False and amendment.get('model_fits') == 0, 'Amendment registration is not source-only offline')
        for path, expected in amendment['inputs'].items():
            require(sha(path) == expected, 'Amendment binding changed: '+path)
        result = read(features_source/'result.json')
        require(result['labels_read'] is False and result['model_fits'] == 0, 'Amendment must be source-only')
        for path, expected in acquisition['inputs'].items():
            require(sha(path) == expected, 'Acquisition binding changed: '+path)
        cases = {r['bill_id']: r for r in acquisition['selected']}
        require(len(cases) == len(acquisition['selected']), 'Duplicate registered source case')
        paths = [source/'registration.json', source/'result.json', source/'population-ledger.json',
                 features_source/'registration.json', features_source/'result.json', features_source/'population-ledger.json', features_source/'changes.json', predecessor_population,
                 stopped_run/'registration.json', stopped_run/'feature-population.json', stopped_run/'label-ledger.json', stopped_run/'failure.json',
                 contract_audit/'registration.json', contract_audit/'result.json', contract_audit/'cases.json', contract_audit/'independent-review.json']
        ledger = read(features_source/'population-ledger.json')
        require(len(ledger) == len(cases) and {r['bill_id'] for r in ledger} == set(cases), 'Incomplete/duplicate acquisition ledger')
        require(result['selected'] == len(cases) and dict(Counter(r['disposition'] for r in ledger)) == result['dispositions'], 'Acquisition ledger/result mismatch')
        expected_features = {r['bill_id']+'.json' for r in ledger if r['disposition'] in ('features_saved', 'feature_ineligible')}
        observed_features = {p.name for p in (features_source/'features').iterdir()}
        require(observed_features == expected_features, 'Missing/extra feature artifacts')
        rows = []
        for path in sorted((features_source/'features').glob('*.json')):
            row = read(path); bid = row['bill_id']
            require(bid in cases and row['congress'] == cases[bid]['congress'], 'Unregistered feature identity')
            raw_path = source/'sources'/(bid+'.xml')
            receipt_path = source/'sources'/(bid+'-receipt.json')
            require(sha(raw_path) == row['source_sha256'] == amendment['source_hashes'].get(bid), 'Feature/amendment source hash mismatch')
            receipt = read(receipt_path)
            require(receipt.get('sha256') == row['source_sha256'] and receipt.get('status') == 200, 'Source receipt mismatch')
            require(feature_api.extract_features(raw_path.read_bytes(), cases[bid]) == {k: v for k, v in row.items() if k != 'source_sha256'}, 'Feature replay mismatch')
            paths.extend([path, raw_path, receipt_path]); rows.append(row)
        code_paths = [Path(__file__), Path(feature_api.__file__), Path(outcome_api.__file__), Path(solver.__file__),
                      Path('scripts/retrospective_text_diagnostic_v1.py'), Path('scripts/official_context_acquisition_v1.py'),
                      Path('scripts/action_context_prepare_v1.py'), Path('scripts/official_context_diagnostic_v2.py'),
                      Path('tests/test_action_context_diagnostic_v2.py'), Path('tests/test_action_context_fit_independent.py'), Path('tests/test_action_outcome_independent.py'), Path('tests/test_action_outcome_resolver_v1.py'), Path('tests/test_action_context_v2_independent.py'), Path('scripts/action_context_diagnostic_v1.py'),
                      Path('docs/research/ACTION_CONTEXT_DIAGNOSTIC_FIT_V1.md'), Path('docs/research/ACTION_CONTEXT_DIAGNOSTIC_FIT_V2.md'), Path('docs/research/20261111-action-outcome-resolver-v1.md'), Path('docs/research/20261109-action-context-successor-proposal.md')]
        registration = {'version': VERSION, 'source': str(source), 'features_source': str(features_source), 'inputs': {str(p): sha(p) for p in paths},
                        'code_protocol_hashes': {str(p): sha(p) for p in code_paths}, 'fit_cap': 2,
                        'calibration_fits': 0, 'stage_reference_name': 'action-milestone', 'historical_eligibility': False, 'release_eligible': False}
        registration_hash = save(output/'registration.json', registration)
        stopped_registration = read(stopped_run/'registration.json')
        for group in ('inputs', 'code_protocol_hashes'):
            for path, expected in stopped_registration[group].items():
                require(sha(path) == expected, 'Stopped-run binding changed: '+path)
        require(read(stopped_run/'failure.json')['fits_started'] == 0, 'Predecessor was not zero-fit failure')
        contract_registration = read(contract_audit/'registration.json')
        for path, expected in contract_registration['inputs'].items():
            require(sha(path) == expected, 'Contract-audit binding changed: '+path)
        for bid, expected in contract_registration['source_hashes'].items():
            require(sha(source/'sources'/(bid+'.xml')) == expected, 'Contract audited source changed: '+bid)
        contract_review = read(contract_audit/'independent-review.json')
        require(contract_review['all_bindings_and_rows_verified'] is True, 'Contract independent review missing')
        require(contract_review['registration_sha256'] == sha(contract_audit/'registration.json') and contract_review['cases_sha256'] == sha(contract_audit/'cases.json') and contract_review['result_sha256'] == sha(contract_audit/'result.json'), 'Contract review hash mismatch')
        population = family_population(rows, acquisition['protected'])
        require(population == read(stopped_run/'feature-population.json'), 'Feature population changed from stopped run')
        require(len(population['rows']) == 8205, 'Registered population must remain 8205')
        population_hash = save(output/'feature-population.json', population)
        changes = population_changes(read(predecessor_population), population)
        changes['predecessor_population_sha256'] = sha(predecessor_population)
        save(output/'predecessor-population-changes.json', changes)
        # This boundary is durable before the first call that reads outcome fields.
        labels = {}
        for row in population['rows']:
            bid = row['bill_id']
            labels[bid] = outcome_api.resolve_outcome((source/'sources'/(bid+'.xml')).read_bytes(), cases[bid], row['cutoff'])
        labels_hash = save(output/'label-ledger.json', labels)
        delta = label_delta(read(stopped_run/'label-ledger.json'), labels, read(contract_audit/'cases.json'), population['rows'])
        save(output/'label-delta.json', delta)
        counts = {group: dict(Counter('unknown' if labels[r['bill_id']]['y'] is None else str(labels[r['bill_id']]['y']) for r in population['rows'] if r['role'] == group)) for group in ('train', '117', '118')}
        save(output/'label-counts.json', counts)
        exclusions = [{'bill_id': r['bill_id'], 'reason': 'unknown_or_out_of_risk_label', 'label_reason': labels[r['bill_id']]['reason']}
                      for r in population['rows'] if labels[r['bill_id']]['y'] is None]
        save(output/'label-exclusions.json', exclusions)
        require(delta['contract_n'] == 231 and delta['corroborated_n'] == 224 and delta['uncorroborated_n'] == 7, 'Contract case counts changed')
        require(not delta['violations'], 'Label amendment violated fixed contract: '+str(delta['violations']))
        accepted, checked_exclusions = resolve_population(population, labels)
        require(exclusions == checked_exclusions, 'Outcome exclusion ledger mismatch')
        split = {group: [r for r in accepted if r['role'] == group] for group in ('train', '117', '118')}
        adapter = fit_adapter(split['train'])
        matrices = {}; input_rows = {}
        for group, group_rows in split.items():
            raw, matrix = transform(group_rows, adapter)
            matrices[group] = matrix
            input_rows[group] = {'ids': [r['bill_id'] for r in group_rows], 'raw_eight': raw.tolist(), 'standardized_eight': matrix.toarray().tolist(), 'labels': [r['y'] for r in group_rows]}
        rate = (sum(r['y'] for r in split['train'])+1)/(len(split['train'])+2)
        stage_rate = {s: (sum(r['y'] for r in split['train'] if r['stage'] == s)+5*rate)/(sum(r['stage'] == s for r in split['train'])+5) for s in range(4)}
        fit_inputs_hash = save(output/'fit-inputs.json', {'adapter': adapter, 'groups': input_rows, 'rate': rate, 'stage_rates': stage_rate,
                                                       'feature_population_sha256': population_hash, 'labels_sha256': labels_hash})
        fits = {}
        y = np.array(input_rows['train']['labels'], dtype=float)
        for arm in ARMS:
            fit_count += 1
            save(output/(arm+'-fit-intent.json'), {'fit_number': fit_count, 'arm': arm, 'fit_inputs_sha256': fit_inputs_hash})
            X = matrices['train'][:, :2] if arm == 'anchor' else matrices['train']
            fitted = solver.fit(X, y)
            try:
                objective, gradient = solver.objective_gradient(fitted['parameters'], X, y)
                maximum = float(np.max(np.abs(gradient)))
                independently_accepted = bool(np.isfinite(objective) and np.isfinite(gradient).all() and maximum <= 1e-6)
                fitted['runner_verification'] = {'objective': objective, 'gradient_infinity_norm': maximum, 'accepted': independently_accepted}
            except (ValueError, TypeError, KeyError) as error:
                independently_accepted = False
                fitted['runner_verification'] = {'accepted': False, 'error': str(error)}
            save(output/(arm+'-fit.json'), fitted)
            require(fitted['accepted'] and independently_accepted, 'Nonconvergence or independent numerical check: '+arm)
            fits[arm] = fitted
        predictions = []
        for group in ('117', '118'):
            values = {}
            for arm in ARMS:
                X = matrices[group][:, :2] if arm == 'anchor' else matrices[group]
                theta = np.asarray(fits[arm]['parameters'])
                values[arm] = expit(X@theta[1:]+theta[0]).tolist()
            for i, row in enumerate(split[group]):
                predictions.append({'bill_id': row['bill_id'], 'family_id': row['family_id'], 'congress': row['congress'], 'cutoff': row['cutoff'],
                                    'anchor': values['anchor'][i], 'context': values['context'][i], 'rate': rate, 'stage': stage_rate[row['stage']]})
        probabilities_hash = save(output/'probabilities.json', predictions)
        folds = []
        for group in ('117', '118'):
            scored = [dict(p, outcome=labels[p['bill_id']]['y']) for p in predictions if str(p['congress']) == group]
            outcomes = [r['outcome'] for r in scored]
            folds.append({'fold': int(group), 'metrics': {arm: metric([r[arm] for r in scored], outcomes) for arm in ('anchor', 'context', 'rate', 'stage')}, 'predictions': scored})
        means = {arm: {name: float(np.mean([f['metrics'][arm][name] for f in folds])) for name in ('brier', 'log_loss')} for arm in ('anchor', 'context', 'rate', 'stage')}
        summary = {'version': VERSION, 'registration_sha256': registration_hash, 'probabilities_sha256': probabilities_hash,
                   'fits_started': fit_count, 'folds': folds, 'means': means, 'label_counts': counts,
                   'brier_skill': {arm: {reference: 1-means[arm]['brier']/means[reference]['brier'] if means[reference]['brier'] else None for reference in ('rate', 'stage')} for arm in ARMS},
                   'bootstrap': context_bootstrap(folds), 'historical_eligibility': False, 'release_eligible': False,
                   'stage_reference_name': 'action-milestone', 'negative_labels': 'uncertified_current_official_record_proxy', 'training_n': len(split['train'])}
        save(output/'result.json', summary)
        print(json.dumps({'fits_started': fit_count, 'means': means, 'label_counts': counts}, indent=2))
    except Exception as error:
        save(output/'failure.json', {'error_type': type(error).__name__, 'error': str(error), 'fits_started': fit_count})
        raise
    finally:
        signal.alarm(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--features', type=Path, required=True)
    parser.add_argument('--predecessor', type=Path, required=True)
    parser.add_argument('--stopped-run', type=Path, required=True)
    parser.add_argument('--contract-audit', type=Path, required=True)
    args = parser.parse_args()
    run(args.source, args.output, args.features, args.predecessor, args.stopped_run, args.contract_audit)
