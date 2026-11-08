"""Bounded offline locator run on the immutable corrected forty design bills.

This reports lexical trigger overlap only, never semantic accuracy. No quality
text, outcomes, network calls, model fitting, or compatibility graph construction.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from engine.paper_evaluation import require, seal, unseal
from engine.store import ROOT
from scripts.mechanism_design_extractor import extract, MECHANISMS

BASE = ROOT / 'data/research-runs'
INPUTS = BASE / 'mechanism-rubric-v2-20261108/inputs.json'
REFERENCE = BASE / 'mechanism-corrections-20261108-v1/corrected-dataset.json'
PILOT = BASE / 'bill-context-20261108-v1/registration.json'
VIEWS = BASE / 'context-peer-audit-20261108/design-text-v2'
EXPECTED_REFERENCE = '041ad00ca21d623b68771d5e81e9dab8d3965f5585232fe688c8804ecb2a5a57'
EXPECTED_PILOT = '318eca5e2797e8d09c14f5d8efe66bbe69e556b05e3861c3ea3f9f3f52fd0c5a'


def read(path):
    envelope = json.loads(path.read_text())
    return envelope, unseal(envelope)


def persist(path, body):
    envelope = seal(body)
    if path.exists():
        require(json.loads(path.read_text()) == envelope, f'Immutable artifact differs: {path}')
    else:
        path.write_text(json.dumps(envelope, indent=2, sort_keys=True) + '\n')
    return envelope


def locator_diagnostic(output, reference, text):
    """Same-mechanism trigger/quote intersection, not matched semantic effects."""
    counts = {m: {'reference_effects': 0, 'effects_with_trigger_overlap': 0} for m in MECHANISMS}
    for effect in reference['effects']:
        a, b = effect['start'], effect['end']
        require(type(a) is int and type(b) is int and 0 <= a < b <= len(text), 'Invalid reference span')
        require(text[a:b] == effect['quote'], 'Reference quote mismatch')
        entry = counts[effect['mechanism']]
        entry['reference_effects'] += 1
        entry['effects_with_trigger_overlap'] += int(any(
            h['start'] < b and a < h['end']
            for c in output['candidates'] if c['mechanism'] == effect['mechanism']
            for h in c['hits']))
    return counts


def run(directory):
    ie, inputs = read(INPUTS)
    re, reference = read(REFERENCE)
    pe, pilot = read(PILOT)
    require(re['hash'] == EXPECTED_REFERENCE and pe['hash'] == EXPECTED_PILOT, 'Frozen identity changed')
    ids = [v['bill_id'] for v in inputs]
    refs = {r['bill_id']: r for r in reference['records']}
    require(len(ids) == len(set(ids)) == len(refs) == len(reference['records']) == 40, 'Design population mismatch')
    require(set(ids) == set(refs), 'Reference population mismatch')
    design = {r['bill_id'] for r in pilot['selection'] if r['partition'] == 'design'}
    quality = {r['bill_id'] for r in pilot['selection'] if r['partition'] == 'quality'}
    require(set(ids) <= design and set(ids).isdisjoint(quality), 'Quality firewall violation')
    paths = [INPUTS, REFERENCE, PILOT]
    views = []
    for item in inputs:
        path = VIEWS / (item['bill_id'] + '.json')
        ve, view = read(path)
        require(ve['hash'] == item['view_hash'] == refs[item['bill_id']]['source_view_hash'], 'View binding mismatch')
        require(all(view[k] == item[k] for k in ('bill_id', 'text', 'spans', 'source')), 'Input view content mismatch')
        views.append(dict(view, view_hash=ve['hash']))
        paths.append(path)
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    files = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    code = {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in (
        'scripts/run_mechanism_design_extractor.py', 'scripts/mechanism_design_extractor.py',
        'engine/paper_evaluation.py', 'engine/store.py')}
    registration = persist(directory/'registration.json', dict(scope='design_only_locator',
        input_hash=ie['hash'], reference_hash=re['hash'], pilot_hash=pe['hash'],
        bill_ids=ids, input_files=files, code_sha256=code, quality_text_access=False,
        diagnostic='same-mechanism lexical trigger intersects provisional effect quote; not semantic recall',
        semantic_matching=False, model_fitting=False, historical_feature_eligible=False))
    totals = Counter()
    per_mechanism = {m: Counter() for m in MECHANISMS}
    outputs = {}
    for view in views:
        result = extract(view)
        require(result == extract(view), 'Nondeterministic extraction')
        for candidate in result['candidates']:
            for span in [candidate, *candidate['hits']]:
                require(view['text'][span['start']:span['end']] == span['quote'], 'Candidate offset mismatch')
        diagnostic = locator_diagnostic(result, refs[view['bill_id']], view['text'])
        outputs[view['bill_id']] = persist(directory/(view['bill_id']+'.json'), result)['hash']
        totals.update(bills=1, characters=len(view['text']), candidates=len(result['candidates']),
                      lexical_hits=sum(len(c['hits']) for c in result['candidates']),
                      unvalidated_suggestions=len(result['proposals']), abstentions=len(result['assessments']))
        for m, count in diagnostic.items():
            per_mechanism[m].update(count)
    require(all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest() == h for p, h in {**files, **code}.items()), 'Source or code changed during run')
    return persist(directory/'result.json', dict(registration_hash=registration['hash'],
        outputs=outputs, totals=dict(totals), locator_diagnostic={m: dict(c) for m,c in per_mechanism.items()},
        semantic_accuracy=None, accepted_labels=0, human_certified=False,
        historical_feature_eligible=False, quality_text_access=False, trained_model=False,
        deterministic_replay=True, source_inputs_preserved=True))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = run(args.output)
    print(json.dumps({'hash': result['hash'], 'totals': result['body']['totals']}))
