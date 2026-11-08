"""Offline integrity replay; requires retained runtime evidence, never fetches it."""
import json, hashlib
from pathlib import Path
from engine.paper_evaluation import seal, unseal, require
from engine.store import ROOT, digest
from scripts.mechanism_training_coverage import select_training, read_sealed, introduced_evidence, fingerprints, frozen_paths, coverage, PILOT
from scripts.bill_context_design_text_v2 import render
from scripts.paper_review_packet import persist_or_compare
import argparse
parser = argparse.ArgumentParser(description='Offline replay of retained training source coverage; no acquisition or outcomes.')
parser.add_argument('directory', type=Path)
p = parser.parse_args().directory
(reg, spec) = read_sealed(p / 'registration.json')
(res, result) = read_sealed(p / 'result.json')
(_, population) = read_sealed(p / 'selection-population.json')
(_, ledger) = read_sealed(p / 'selection-ledger.json')
require(digest(population) == spec['selection_population_hash'], "Verification failed: digest(population) == spec['selection_population_hash']")
require(digest(ledger) == spec['selection_ledger_hash'], "Verification failed: digest(ledger) == spec['selection_ledger_hash']")
(_, pilot) = read_sealed(PILOT / 'registration.json')
groups = {r['bill_id']: r['family_id'] for r in population}
require(digest(groups) == spec['family_graph_hash'], 'Family graph mismatch')
require(result['registration_hash'] == reg['hash'], 'Result registration mismatch')
(selection, replayed) = select_training(population, groups, spec['memberships'], pilot['selection'], spec['quota_per_congress'])
require(selection == spec['selection'] and replayed == ledger, "Verification failed: selection == spec['selection'] and replayed == ledger")
require(fingerprints([ROOT / x for x in spec['implementation_hashes']]) == spec['implementation_hashes'], "Verification failed: fingerprints([ROOT / x for x in spec['implementation_hashes']]) == spec['implementation_hashes']")
require(fingerprints(frozen_paths()) == spec['frozen_files'], "Verification failed: fingerprints(frozen_paths()) == spec['frozen_files']")
good = set()
failures = []
for selected in selection:
    bid = selected['bill_id']
    (_, record) = read_sealed(p / 'records' / (bid + '.json'))
    require(all((record[k] == v for (k, v) in selected.items())), 'Verification failed: all((record[k] == v for (k, v) in selected.items()))')
    require(record['registration_hash'] == reg['hash'] and record['historical_feature_eligible'] is False and (record['human_certified'] is False), "Verification failed: record['registration_hash'] == reg['hash'] and record['historical_feature_eligible'] is False and (record['human_certified'] is False)")
    if record['status'] == 'blocked':
        failures.append(dict(bill_id=bid, error=record['error']))
        continue
    (_, packet) = read_sealed(p / 'packets' / (bid + '.json'))
    require(packet['bill_id'] == bid, 'Packet identity mismatch')
    (package, url, proof) = introduced_evidence(packet)
    require(record['package'] == package and record['publication_metadata'] == proof, "Verification failed: record['package'] == package and record['publication_metadata'] == proof")
    key = hashlib.sha256(url.encode()).hexdigest()
    raw = (p / 'sources' / (key + '.raw')).read_bytes()
    receipt = json.loads((p / 'sources' / (key + '.json')).read_text())
    require(receipt == record['source'] and receipt['sha256'] == hashlib.sha256(raw).hexdigest() and (receipt['bytes'] == len(raw)), "Verification failed: receipt == record['source'] and receipt['sha256'] == hashlib.sha256(raw).hexdigest() and (receipt['bytes'] == len(raw))")
    require(receipt['retrieved_at'] >= spec['registered_at'], "Verification failed: receipt['retrieved_at'] >= spec['registered_at']")
    (view, body) = read_sealed(p / 'views' / (bid + '.json'))
    require(view['hash'] == record['source_view_hash'], "Verification failed: view['hash'] == record['source_view_hash']")
    require(body == dict(**render(raw, bid), source=receipt, registration_hash=reg['hash'], historical_feature_eligible=False), "Verification failed: body == dict(**render(raw, bid), source=receipt, registration_hash=reg['hash'], historical_feature_eligible=False)")
    good.add(bid)
require(failures == result['failures'], "Verification failed: failures == result['failures']")
require(result['coverage_after'] == coverage(spec['memberships'], set(spec['baseline_design_ids']) | good), "Verification failed: result['coverage_after'] == coverage(spec['memberships'], set(spec['baseline_design_ids']) | good)")
require(result['coverage_before'] == coverage(spec['memberships'], spec['baseline_design_ids']), "Verification failed: result['coverage_before'] == coverage(spec['memberships'], spec['baseline_design_ids'])")
require(result['coverage_increment'] == coverage(spec['memberships'], good), "Verification failed: result['coverage_increment'] == coverage(spec['memberships'], good)")
require(result['usable_metadata_dated_current_xml'] == len(good) and result['selected'] == result['attempted'] == len(selection), 'Result acquisition counts mismatch')
require(result['models_fitted'] == result['outcomes_scored'] == result['mechanism_labels_created'] == result['certified_historical'] == 0, "Verification failed: result['models_fitted'] == result['outcomes_scored'] == result['mechanism_labels_created'] == result['certified_historical'] == 0")
verification = seal(dict(registration_hash=reg['hash'], result_hash=res['hash'], selected_replayed=len(selection), sources_replayed=len(good), all_view_offsets_reconstructed=True, frozen_files_unchanged=True, outcome_values_read=False, quality_texts_opened=False, certified_historical=0))
persist_or_compare(p / 'verification.json', verification)
print(json.dumps(dict(hash=verification['hash'], **verification['body']), indent=2))
