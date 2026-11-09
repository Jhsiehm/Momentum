"""Freeze and build structural sidecars for the fixed forty exposed design bills."""
import argparse
import sys
from collections import Counter
from pathlib import Path
from engine.paper_evaluation import require
from engine.store import ROOT, digest
from scripts.run_mechanism_design_extractor import BASE, INPUTS, PILOT, VIEWS, EXPECTED_PILOT, read, persist
from scripts.run_bill_readiness_audit_v2 import authenticate_source, population, sha, INPUT_HASH, CODE as PRIOR_CODE
from scripts.bill_structural_input_v1 import build, validate

CODE = sorted(set(PRIOR_CODE + ['scripts/run_bill_structural_input_v1.py',
    'scripts/bill_structural_input_v1.py', 'tests/test_bill_structural_input_v1.py',
    'tests/test_bill_structural_input_independent.py']))
PREVIOUS = BASE/'readiness-coverage-v2-20261108/result.json'
PREVIOUS_HASH = '9c82fc612cef6d480d6afcaa7c18e41431c9fbc806f885acd1aadff0b178b9c6'


def run(directory):
    ie, inputs = read(INPUTS); pe, pilot = read(PILOT); previous, _ = read(PREVIOUS)
    require(ie['hash'] == INPUT_HASH and pe['hash'] == EXPECTED_PILOT, 'Population binding changed')
    require(previous['hash'] == PREVIOUS_HASH, 'Prior audit changed')
    ids = population(inputs, pilot)
    paths = [INPUTS, PILOT, PREVIOUS]; loaded = {}
    for item in inputs:
        bid = item['bill_id']; vp = VIEWS/(bid+'.json'); ve, view = read(vp)
        require(ve['hash'] == item['view_hash'], 'View binding mismatch')
        require(all(view[k] == item[k] for k in ('bill_id','source','text','spans')), 'View contents mismatch')
        rp = PILOT.parent/'sources'/(sha(view['source']['url'].encode())+'.raw')
        raw = rp.read_bytes(); authenticate_source(view['source'], raw)
        paths.extend([vp, rp]); loaded[bid] = (raw, view, ve['hash'])
    bound = {str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in paths}
    code = {p:sha((ROOT/p).read_bytes()) for p in CODE}
    directory = Path(directory).resolve()
    require(ROOT/'data' in directory.parents, 'Output must be runtime data')
    directory.mkdir(parents=True, exist_ok=True)
    registration = persist(directory/'registration.json', dict(
        version='structural-input-v1', question='Can a separate input preserve parser-visible structure and exact existing view offsets without migrating labels?',
        bill_ids=ids, input_files=bound, code_sha256=code, python_version=sys.version,
        prior_result_hash=previous['hash'], budget='Exactly forty fixed exposed design bills; no substitutions; failures retained',
        offset_contract='Zero-based half-open Unicode code points in frozen reading view, not XML byte offsets',
        interpretation='Structural fidelity only; no semantic, historical or predictive qualification',
        quality_access=False, model_fitting=False))
    outputs = {}; failures = []; counts = Counter(); rows = []
    for bid in ids:
        raw, view, vh = loaded[bid]; before = digest(view)
        try:
            result = build(raw, bid, view, vh)
            validate(result, raw, bid, view, vh)
            require(digest(view) == before, 'View mutated')
            nodes = result['nodes']
            measured = dict(nodes=len(nodes), attribute_nodes=sum(bool(n['attributes']) for n in nodes),
                attributes=sum(len(n['attributes']) for n in nodes),
                tables=len(result['tables']), rows=sum(n['row'] for n in nodes), cells=sum(n['cell'] for n in nodes),
                fractions=len(result['fractions']), text_segments=len(result['segments']),
                rendered_characters=len(result['text']))
            counts.update(measured); rows.append(dict(bill_id=bid,status='passed',**measured))
        except ValueError as error:
            result = dict(bill_id=bid,status='failed',error=str(error))
            failures.append(dict(bill_id=bid,error=str(error))); rows.append(result)
        outputs[bid] = persist(directory/(bid+'.json'), result)['hash']
    require(all(sha((ROOT/p).read_bytes()) == h for p,h in {**bound,**code}.items()), 'Frozen files changed')
    return persist(directory/'result.json',dict(registration_hash=registration['hash'], outputs=outputs,
        bills=len(ids), failures=failures, per_bill=rows, counts=dict(counts), quality_access=False,
        model_fitting=False, semantic_accuracy_verified=False, historical_feature_eligible=False,
        reference_migration=False, interpretation='Structural input design validation only'))


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--output', type=Path, required=True)
    result = run(p.parse_args().output)
    print(result['hash']); print({k:v for k,v in result['body'].items() if k not in ('outputs','per_bill')})
