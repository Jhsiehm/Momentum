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
from scripts.run_mechanism_context_filter import EXPANDED, EXPANDED_HASH, audit_decisions
from scripts.mechanism_design_extractor import MECHANISMS
from scripts.mechanism_design_extractor_v2 import extract as extract_v2
from scripts.mechanism_design_extractor_v4 import extract, RULES
from scripts.mechanism_context_filter_v2 import classify, RULES as FILTER_RULES
from scripts.mechanism_validity_guard import validate_output, validate_reference

FILTER = BASE / 'mechanism-context-filter-20261108'
FILTER_HASH = '9079f2fba97f912c0950cd8070e728539d283a8f94c86d0d0a2328f39243810b'
CODE = [
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


def compare(reference, old, new, old_decisions, new_decisions):
    """Count identities and quote intersections, never infer semantic correctness."""
    oh, nh = hit_map(old), hit_map(new)
    counts = {m: Counter(dict(old_hits=0, new_hits=0, removed_hits=0, added_hits=0,
        old_flagged=0, new_flagged=0, common_flag_to_retain=0, common_retain_to_flag=0,
        reference_effects=0, old_raw_overlap=0, new_raw_overlap=0, raw_lost=0,
        raw_recovered=0, old_retained_overlap=0, new_retained_overlap=0,
        retained_lost=0, retained_recovered=0)) for m in MECHANISMS}
    for keys, decisions, prefix in ((oh, old_decisions, 'old'), (nh, new_decisions, 'new')):
        require(set(keys) == set(decisions), 'Comparison decision coverage mismatch')
        for k in keys:
            counts[k[0]][prefix + '_hits'] += 1
            counts[k[0]][prefix + '_flagged'] += int(decisions[k]['status'] == 'flagged')
    for k in set(oh) - set(nh): counts[k[0]]['removed_hits'] += 1
    for k in set(nh) - set(oh): counts[k[0]]['added_hits'] += 1
    for k in set(oh) & set(nh):
        a, b = old_decisions[k]['status'], new_decisions[k]['status']
        counts[k[0]]['common_flag_to_retain'] += int(a == 'flagged' and b == 'retain')
        counts[k[0]]['common_retain_to_flag'] += int(a == 'retain' and b == 'flagged')
    effects = []
    for i, effect in enumerate(reference['effects']):
        row = dict(effect_index=i, mechanism=effect['mechanism'])
        for keys, decisions, prefix in ((oh, old_decisions, 'old'), (nh, new_decisions, 'new')):
            matched = [k for k in keys if k[0] == effect['mechanism'] and k[1] < effect['end'] and effect['start'] < k[2]]
            row[prefix + '_raw_overlap'] = bool(matched)
            row[prefix + '_retained_overlap'] = any(decisions[k]['status'] == 'retain' for k in matched)
        c = counts[effect['mechanism']]; c['reference_effects'] += 1
        for metric in ('raw', 'retained'):
            a, b = row['old_' + metric + '_overlap'], row['new_' + metric + '_overlap']
            c['old_' + metric + '_overlap'] += int(a); c['new_' + metric + '_overlap'] += int(b)
            c[metric + '_lost'] += int(a and not b); c[metric + '_recovered'] += int(b and not a)
        effects.append(row)
    return dict(by_mechanism={m: dict(c) for m, c in counts.items()}, reference_intersections=effects,
        removed_hit_identities=[list(k) for k in sorted(set(oh)-set(nh))],
        added_hit_identities=[list(k) for k in sorted(set(nh)-set(oh))],
        old_active_proposals=len(old['proposals']), new_active_proposals=len(new['proposals']),
        quarantined_proposals=len(new.get('legacy_proposals', [])))


def check_legacy_preservation(baseline, output):
    old_hits, new_hits = hit_map(baseline), hit_map(output)
    require(set(old_hits) <= set(new_hits), 'Frozen v2 hit lost')
    candidates = {c['candidate_id']: c for c in output['candidates']}
    for candidate in baseline['candidates']:
        current = candidates.get(candidate['candidate_id'])
        require(current is not None, 'Frozen v2 candidate lost')
        require(all(current.get(k) == v for k, v in candidate.items() if k != 'hits'), 'Frozen v2 candidate changed')
    for key, (_, hit) in old_hits.items():
        current = new_hits[key][1]
        require(all(current.get(k) == v for k, v in hit.items()), 'Frozen v2 hit field changed')
    require(output['proposals'] == [], 'Active legacy proposal remains')
    require([p['proposal'] for p in output.get('legacy_proposals', [])] == baseline['proposals'], 'Legacy quarantine is not exact')


def run(directory):
    ee, expanded = read(EXPANDED/'result.json'); fe, filtered = read(FILTER/'result.json')
    re, reference = read(REFERENCE); ie, inputs = read(INPUTS); pe, pilot = read(PILOT)
    require((ee['hash'], fe['hash'], re['hash'], pe['hash']) ==
            (EXPANDED_HASH, FILTER_HASH, REFERENCE_HASH, EXPECTED_PILOT), 'Frozen identity mismatch')
    ids = [r['bill_id'] for r in inputs]; refs = {r['bill_id']: r for r in reference['records']}
    require(len(ids) == len(set(ids)) == 40 and set(ids) == set(refs) == set(expanded['outputs']) == set(filtered['outputs']), 'Design population mismatch')
    design = {r['bill_id'] for r in pilot['selection'] if r['partition'] == 'design'}
    quality = {r['bill_id'] for r in pilot['selection'] if r['partition'] == 'quality'}
    require(set(ids) <= design and set(ids).isdisjoint(quality), 'Quality firewall violation')
    paths = [EXPANDED/'result.json', FILTER/'result.json', REFERENCE, INPUTS, PILOT]
    views, old, prior = {}, {}, {}
    for item in inputs:
        bid = item['bill_id']; vp = VIEWS/(bid+'.json'); op = EXPANDED/(bid+'.json'); fp = FILTER/(bid+'.json')
        ve, v = read(vp); oe, o = read(op); fbe, f = read(fp)
        require(oe['hash'] == expanded['outputs'][bid] and fbe['hash'] == filtered['outputs'][bid], 'Old output binding mismatch')
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
        scope='bounded_exploratory_40_design_validity_v4', bill_ids=ids, input_files=files, code_sha256=codes,
        reference_hash=re['hash'], expanded_hash=ee['hash'], filter_hash=fe['hash'], pilot_hash=pe['hash'],
        input_hash=ie['hash'], python_version=sys.version,
        sampling='No new sampling; all 40 fixed design bills; complete changed-case audit follows separately', lexical_rules=RULES, filter_rules=FILTER_RULES,
        hypothesis='Leaf-local expansion and narrow subject/provenance guards reduce known design defects; record locator losses as well as recoveries',
        metric='Same-mechanism half-open quote intersection; retained means not flagged, never semantically approved',
        exposure='Design sources, prior reviews and adversarial examples informed changes; no held-out accuracy claim',
        quality_text_access=False, model_fitting=False, human_certified=False, historical_feature_eligible=False))
    outputs, filters, comparisons = {}, {}, []
    totals = Counter(); categories = {m: Counter() for m in MECHANISMS}
    for bid in ids:
        view = views[bid]; before = digest(view); output = extract(view)
        require(output == extract(view) and digest(view) == before, 'Extraction nondeterminism or mutation')
        validate_output(view, output); check_legacy_preservation(extract_v2(view), output); before_pair = (digest(view), digest(output)); triage = classify(view, output)
        require(triage == classify(view, output) and before_pair == (digest(view), digest(output)), 'Triage nondeterminism or mutation')
        decisions = audit_decisions(triage, output, view)
        comparison = compare(refs[bid], old[bid], output, audit_decisions(prior[bid], old[bid], view), decisions)
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
