"""Offline supplemental claim checks; preserve the registered acquisition code."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from engine.paper_evaluation import require, seal
from engine.store import ROOT
from scripts.mechanism_training_expansion_v2 import baseline, validate_current_record
from scripts.mechanism_training_coverage import coverage, fingerprints, read_sealed
from scripts.paper_review_packet import persist_or_compare

RECEIPT = 'supplemental-claims-verification.json'


def false_flags(body, names):
    require(all(body.get(k) is False for k in names), 'False audit flags changed: '+','.join(names))


def check_claims(spec, registration_hash, result, records, cycles, manifest, baseline_ids):
    """Pure claim replay from independently validated source inputs."""
    false_flags(spec, ('historical_feature_eligible', 'human_certified', 'quality_texts_opened'))
    false_flags(result, ('historical_feature_eligible', 'human_certified', 'quality_texts_opened'))
    require(result.get('registration_hash') == registration_hash, 'Result registration binding changed')
    selected = spec['selection']; ids = [s['bill_id'] for s in selected]
    require(len(ids) == len(set(ids)) and set(records) == set(ids), 'Record coverage differs')
    require(len(baseline_ids) == len(set(baseline_ids)) == 232, 'Baseline identities differ')
    require(spec['baseline_available_ids'] == baseline_ids and spec['baseline']['ids'] == baseline_ids, 'Baseline binding changed')
    require(not set(ids).intersection(baseline_ids), 'Baseline/expansion overlap')
    good = set(); failures = []
    for s in selected:
        r = records[s['bill_id']]['body']
        require(all(r.get(k) == v for k, v in s.items()), 'Selected record identity changed')
        require(r.get('registration_hash') == registration_hash, 'Record registration changed')
        false_flags(r, ('historical_feature_eligible', 'human_certified'))
        require(type(r.get('mechanism_labels_created')) is int and r['mechanism_labels_created'] == 0, 'Record label claim changed')
        if r['status'] == 'metadata_dated_current_xml':
            require(r.get('historical_rendition_identity') == 'uncertified', 'Rendition identity claim changed')
            good.add(s['bill_id'])
        else:
            require(r['status'] == 'blocked' and isinstance(r.get('error'), str) and r['error'], 'Invalid blocked record')
            failures.append(dict(bill_id=s['bill_id'], error=r['error']))
    expected = dict(selected=len(ids), attempted=len(ids), completed_cycles=len(spec['cycles']),
                    baseline_unique=len(baseline_ids), total_unique=len(set(baseline_ids)|good),
                    usable_metadata_dated_current_xml=len(good), downloaded_documents=len(manifest),
                    source_bytes=sum(r['bytes'] for r in manifest))
    for key, value in expected.items():
        require(type(result.get(key)) is int and result[key] == value, 'Result count differs: '+key)
    for key in ('certified_historical', 'models_fitted', 'outcomes_scored', 'mechanism_labels_created'):
        require(type(result.get(key)) is int and result[key] == 0, 'Unapproved claim: '+key)
    require(result.get('frozen_artifacts_unchanged') is True, 'Frozen artifact claim changed')
    require(result['failures'] == failures, 'Failure ledger differs')
    require(result['usable_by_congress'] == dict(Counter(str(s['congress']) for s in selected if s['bill_id'] in good)), 'Congress counts differ')
    for key, values in (('coverage_before', baseline_ids), ('coverage_after', set(baseline_ids)|good), ('coverage_increment', good)):
        require(result[key] == coverage(spec['memberships'], values), 'Coverage differs: '+key)
    require(len(cycles) == len(spec['cycles']), 'Cycle count differs')
    require([bid for c in spec['cycles'] for bid in c['bill_ids']] == ids, 'Cycle selection coverage differs')
    for plan, (registration, envelope) in zip(spec['cycles'], cycles):
        require(registration['body'] == dict(**plan, registration_hash=registration_hash), 'Cycle registration differs')
        require(0 < len(plan['bill_ids']) <= 100 and plan['acquisition_cap'] == 100, 'Cycle cap differs')
        c = envelope['body']; hashes = {bid:records[bid]['hash'] for bid in plan['bill_ids']}
        require(c['cycle_registration_hash'] == registration['hash'] and c['registration_hash'] == registration_hash, 'Cycle binding differs')
        require(c['cycle'] == plan['cycle'] and c['record_hashes'] == hashes, 'Cycle records differ')
        require(type(c['attempted']) is int and c['attempted'] == len(hashes) and type(c['usable']) is int and c['usable'] == len(good.intersection(hashes)), 'Cycle counts differ')
        require(c['failures'] == [f for f in failures if f['bill_id'] in hashes], 'Cycle failures differ')
        false_flags(c, ('historical_feature_eligible',))
        require(c['frozen_files_unchanged'] is True, 'Cycle preservation claim differs')
    return expected


def verify(directory):
    directory = Path(directory)
    reg, spec = read_sealed(directory/'registration.json'); result, body = read_sealed(directory/'result.json')
    require(fingerprints([ROOT/p for p in spec['implementation_hashes']]) == spec['implementation_hashes'], 'Registered implementation changed')
    require(fingerprints([ROOT/p for p in spec['frozen_files']]) == spec['frozen_files'], 'Frozen sources changed')
    # The registered verifier's receipt binds its source, selection and preservation replay.
    verification, checked = read_sealed(directory/'verification.json')
    require(checked['registration_hash'] == reg['hash'] and checked['result_hash'] == result['hash'], 'Registered verification binding differs')
    false_flags(checked, ('historical_feature_eligible', 'quality_texts_opened', 'outcome_values_read'))
    require(checked['frozen_files_unchanged'] is True, 'Registered preservation check missing')
    base = baseline(); require(base == spec['baseline'], 'Baseline replay differs')
    records = {}
    for s in spec['selection']:
        validate_current_record(directory, s, reg['hash'], spec['registered_at'])
        envelope, _ = read_sealed(directory/'records'/(s['bill_id']+'.json')); records[s['bill_id']] = envelope
    require({p.stem for p in (directory/'records').glob('*.json')} == set(records), 'Unexpected record files')
    manifest = []
    source_dir = directory/'sources'
    require({p.stem for p in source_dir.glob('*.raw')} == {p.stem for p in source_dir.glob('*.json')}, 'Source file pairing differs')
    for path in sorted(source_dir.glob('*.json')):
        receipt = json.loads(path.read_text()); raw = path.with_suffix('.raw').read_bytes()
        require(path.stem == hashlib.sha256(receipt['url'].encode()).hexdigest(), 'Source URL key differs')
        require(type(receipt['bytes']) is int and receipt['bytes'] == len(raw) and receipt['sha256'] == hashlib.sha256(raw).hexdigest(), 'Source bytes differ')
        manifest.append(receipt)
    cycles = []
    for c in spec['cycles']:
        stem = f"cycle-{c['cycle']:02d}"
        cycles.append((read_sealed(directory/'cycles'/(stem+'-registration.json'))[0], read_sealed(directory/'cycles'/(stem+'-result.json'))[0]))
    counts = check_claims(spec, reg['hash'], body, records, cycles, manifest, base['ids'])
    require(checked['baseline_sources_validated'] == counts['baseline_unique'] and checked['selected_replayed'] == counts['selected'] and checked['sources_replayed'] == counts['usable_metadata_dated_current_xml'] and checked['blocked'] == len(body['failures']), 'Registered verification counts differ')
    receipt = seal(dict(registration_hash=reg['hash'], result_hash=result['hash'], registered_verification_hash=verification['hash'],
                        verifier_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), counts=counts,
                        manifest_sha256=hashlib.sha256(json.dumps(manifest,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
                        historical_feature_eligible=False, human_certified=False, quality_texts_opened=False, outcome_values_read=False))
    persist_or_compare(directory/RECEIPT, receipt)
    return receipt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.directory), indent=2))
