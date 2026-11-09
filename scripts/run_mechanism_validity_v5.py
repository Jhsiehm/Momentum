"""Bounded design-only rerun; overlap and triage diagnostics are not accuracy."""
import argparse
import sys
from collections import Counter
from pathlib import Path
from engine.paper_evaluation import require
from engine.store import ROOT, digest
from scripts.run_mechanism_design_extractor import BASE, INPUTS, PILOT, VIEWS, EXPECTED_PILOT, read, persist
from scripts.run_mechanism_context_v2 import hash_file
from scripts.run_mechanism_expansion_v3 import hit_map, REFERENCE, REFERENCE_HASH
from scripts.run_mechanism_context_filter import audit_decisions
from scripts.mechanism_design_extractor import MECHANISMS
from scripts.mechanism_design_extractor_v2 import extract as extract_v2
from scripts.mechanism_design_extractor_v5 import extract, RULES
from scripts.mechanism_design_extractor_v4 import RULES as BASE_RULES
from scripts.mechanism_context_filter_v3 import classify, RULES as FILTER_RULES
from scripts.mechanism_validity_guard import validate_output, validate_reference

PREVIOUS = BASE / 'mechanism-validity-v4-20261108'
PREVIOUS_HASH = '950af33a265164374f41651dbd3bfdaf6f72bb8759626e602ccb4b3e82867178'
CODE = [
    'scripts/run_mechanism_validity_v5.py', 'scripts/mechanism_design_extractor_v5.py',
    'scripts/mechanism_context_filter_v3.py', 'tests/test_mechanism_design_extractor_v5.py',
    'tests/test_mechanism_context_filter_v3.py', 'tests/test_mechanism_validity_v5_runner.py',
    'tests/test_mechanism_v5_independent.py',
    'scripts/run_mechanism_validity_v4.py', 'scripts/mechanism_validity_guard.py',
    'scripts/mechanism_design_extractor_v4.py', 'scripts/mechanism_context_filter_v2.py',
    'scripts/mechanism_design_extractor_v3.py', 'scripts/mechanism_design_extractor_v2.py',
    'scripts/mechanism_design_extractor.py', 'scripts/mechanism_context_filter.py',
    'scripts/run_mechanism_context_filter.py', 'scripts/run_mechanism_expansion_v3.py',
    'scripts/run_mechanism_context_v2.py', 'scripts/run_mechanism_design_extractor.py',
    'scripts/mechanism_effect_evaluation.py', 'scripts/mechanism_rubric_v2_audit.py',
    'scripts/mechanism_reference_v3.py',
    'engine/paper_evaluation.py', 'engine/store.py',
    'scripts/bill_context_design_text_v2.py', 'scripts/paper_review_packet.py',
    'tests/test_mechanism_design_extractor.py',
    'tests/test_mechanism_validity_v4_runner.py', 'tests/test_mechanism_design_extractor_v4.py',
    'tests/test_mechanism_context_filter_v2.py', 'tests/test_experiment_validity_adversarial.py',
]


from scripts.run_mechanism_validity_v4 import compare, check_legacy_preservation


def check_v4_preservation(old,new):
    require(set(hit_map(old))<=set(hit_map(new)), 'Prior v4 locator lost')
    require(new['legacy_proposals']==old['legacy_proposals'] and new['proposals']==[], 'Prior quarantine changed')


def decision_changes(old, new):
    fields=('status','reasons','evidence')
    return [dict(mechanism=k[0],start=k[1],end=k[2],before={f:old[k][f] for f in fields},
                 after={f:new[k][f] for f in fields}) for k in sorted(set(old)&set(new))
            if any(old[k][f]!=new[k][f] for f in fields)]


def run(directory):
    ee, expanded = read(PREVIOUS/'result.json'); fe, filtered = ee, expanded
    re, reference = read(REFERENCE); ie, inputs = read(INPUTS); pe, pilot = read(PILOT)
    require((ee['hash'], fe['hash'], re['hash'], pe['hash']) ==
            (PREVIOUS_HASH, PREVIOUS_HASH, REFERENCE_HASH, EXPECTED_PILOT), 'Frozen identity mismatch')
    ids = [r['bill_id'] for r in inputs]; refs = {r['bill_id']: r for r in reference['records']}
    require(len(ids) == len(set(ids)) == 40 and set(ids) == set(refs) == set(expanded['outputs']) == set(filtered['filters']), 'Design population mismatch')
    design = {r['bill_id'] for r in pilot['selection'] if r['partition'] == 'design'}
    quality = {r['bill_id'] for r in pilot['selection'] if r['partition'] == 'quality'}
    require(set(ids) <= design and set(ids).isdisjoint(quality), 'Quality firewall violation')
    paths = [PREVIOUS/'result.json', REFERENCE, INPUTS, PILOT]
    views, old, prior = {}, {}, {}
    for item in inputs:
        bid = item['bill_id']; vp = VIEWS/(bid+'.json'); op = PREVIOUS/(bid+'.json'); fp = PREVIOUS/(bid+'-filter.json')
        ve, v = read(vp); oe, o = read(op); fbe, f = read(fp)
        require(oe['hash'] == expanded['outputs'][bid] and fbe['hash'] == filtered['filters'][bid], 'Old output binding mismatch')
        require(ve['hash'] == item['view_hash'] == refs[bid]['source_view_hash'] == o['source_view_hash'], 'Source binding mismatch')
        require(all(item[k] == v[k] for k in ('bill_id', 'text', 'spans', 'source')), 'Input changed')
        views[bid] = dict(v, view_hash=ve['hash']); old[bid] = o; prior[bid] = f; paths.extend([vp, op, fp])
    validate_reference(reference, views)
    for bid in ids:
        validate_output(views[bid], old[bid]); audit_decisions(prior[bid], old[bid], views[bid])
    files = {str(p.relative_to(ROOT)): hash_file(p) for p in paths}
    codes = {p: hash_file(ROOT/p) for p in CODE}
    directory = Path(directory); directory.mkdir(parents=True, exist_ok=True)
    registration = persist(directory/'registration.json', dict(
        scope='bounded_exploratory_40_design_validity_v5', bill_ids=ids, input_files=files, code_sha256=codes,
        reference_hash=re['hash'], expanded_hash=ee['hash'], filter_hash=fe['hash'], pilot_hash=pe['hash'],
        input_hash=ie['hash'], python_version=sys.version,
        sampling='No new sampling; all 40 fixed design bills; complete changed-case audit follows separately', lexical_rules=RULES, base_lexical_rules=BASE_RULES, filter_rules=FILTER_RULES,
        hypothesis='Bounded subject supplements and qualified amendment prefixes recover exposed v4 regressions without reintroducing known counterexamples; report all changes and failures',
        metric='Same-mechanism half-open quote intersection; retained means not flagged, never semantically approved',
        decision='No semantic promotion; report all deltas regardless of improvement; any next change requires separate registration',
        scope_note='Additional exposed-design regression-recovery iteration before parser/provenance readiness work; renderer coverage remains unresolved',
        exposure='Design sources, prior reviews and adversarial examples informed changes; no held-out accuracy claim',
        quality_text_access=False, model_fitting=False, human_certified=False, historical_feature_eligible=False))
    outputs, filters, comparisons = {}, {}, []
    totals = Counter(); categories = {m: Counter() for m in MECHANISMS}
    for bid in ids:
        view = views[bid]; before = digest(view); output = extract(view)
        require(output == extract(view) and digest(view) == before, 'Extraction nondeterminism or mutation')
        validate_output(view, output); check_v4_preservation(old[bid], output); check_legacy_preservation(extract_v2(view), output); before_pair = (digest(view), digest(output)); triage = classify(view, output)
        require(triage == classify(view, output) and before_pair == (digest(view), digest(output)), 'Triage nondeterminism or mutation')
        decisions = audit_decisions(triage, output, view)
        comparison = compare(refs[bid], old[bid], output, audit_decisions(prior[bid], old[bid], view), decisions)
        comparison['common_decision_changes']=decision_changes(audit_decisions(prior[bid], old[bid], view), decisions)
        comparisons.append(dict(bill_id=bid, **comparison))
        for m, counts in comparison['by_mechanism'].items(): categories[m].update(counts); totals.update(counts)
        totals.update(bills=1, quarantined_proposals=comparison['quarantined_proposals'],
                      old_active_proposals=comparison['old_active_proposals'], new_active_proposals=comparison['new_active_proposals'])
        outputs[bid] = persist(directory/(bid+'.json'), output)['hash']
        filters[bid] = persist(directory/(bid+'-filter.json'), triage)['hash']
    require(all(hash_file(ROOT/p) == h for p, h in {**files, **codes}.items()), 'Frozen code or inputs changed')
    return persist(directory/'result.json', dict(registration_hash=registration['hash'], outputs=outputs, filters=filters,
        totals=dict(totals), by_mechanism={m: dict(c) for m, c in categories.items()}, comparisons=comparisons,
        semantic_accuracy=None, predictive_accuracy=None, accepted_labels=0, trained_model=False,
        human_certified=False, historical_feature_eligible=False, quality_text_access=False,
        interpretation='Design diagnostics only; overlap is not effect correctness, retain is not approval, and quarantine is intentional policy rather than measured accuracy'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--output', type=Path, required=True)
    result = run(parser.parse_args().output)
    print(result['hash']); print(result['body']['totals'])
