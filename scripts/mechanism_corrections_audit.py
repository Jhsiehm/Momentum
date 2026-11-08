"""Validate separate corrected annotations against immutable source reviews.

Integrity and correction coverage only; no claim of semantic truth.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from engine.paper_evaluation import require, seal, unseal
from engine.store import ROOT, digest
from scripts.mechanism_rubric_v2_audit import check_quote, validate_primary
from scripts.paper_review_packet import persist_or_compare


def expected_findings(subset, methods, bill_ids):
    result = {}
    for row in subset['records']:
        if row['bill_id'] in bill_ids:
            for i, finding in enumerate(row['findings']):
                result[f"subset:{row['bill_id']}:{i}"] = row['bill_id']
    for finding in methods['findings']:
        bid = finding['bill_id']
        if bid in bill_ids:
            result[f"peer:{finding['peer_reviewer']}:{bid}:{finding['finding_index']}"] = bid
    for i, finding in enumerate(methods['additional_findings']):
        if finding['bill_id'] in bill_ids:
            result[f"additional:{finding['bill_id']}:{i}"] = finding['bill_id']
    return result


def validate_changes(original, corrected, changes, expected):
    before = {r['bill_id']: r for r in original['records']}
    after = {r['bill_id']: r for r in corrected['records']}
    require(set(before) == set(after), 'Correction population changed')
    seen, documented = set(), set()
    for change in changes:
        bid = change['bill_id']
        require(bid in before and isinstance(change['description'], str) and change['description'].strip(), 'Invalid change description')
        require(bool(change['source_finding_ids']), 'Unbound correction')
        for finding_id in change['source_finding_ids']:
            require(finding_id in expected and expected[finding_id] == bid, 'Wrong finding reference')
            require(finding_id not in seen, 'Duplicate finding disposition')
            seen.add(finding_id)
        documented.add(bid)
    require(seen == set(expected), 'Incomplete finding disposition')
    changed = {bid for bid in before if before[bid] != after[bid]}
    require(changed <= documented, 'Undocumented changed bill')
    return len(changed)


def run(original_directory, corrected_directory, a_file="corrected-agent-a.json", b_file="corrected-agent-b.json"):
    original_directory, corrected_directory = Path(original_directory), Path(corrected_directory)
    read = lambda directory, name: json.loads((directory/name).read_text())
    registration = read(original_directory, 'registration.json'); spec = unseal(registration)
    inputs = unseal(read(original_directory, 'inputs.json'))
    require(digest(inputs) == spec['inputs_hash'], 'Inputs hash mismatch')
    byid = {row['bill_id']: row for row in inputs}
    require(hashlib.sha256((ROOT/spec['rubric_path']).read_bytes()).hexdigest() == spec['rubric_sha256'], 'Frozen rubric changed')
    subset = read(original_directory, 'methods-subset-audit.json'); methods = read(original_directory, 'methods-peer-audit.json')
    sb, mb = unseal(subset), unseal(methods)
    require(sb['registration_hash'] == mb['registration_hash'] == registration['hash'], 'Methods registration mismatch')
    require(mb['subset_audit_hash'] == subset['hash'], 'Methods subset mismatch')
    counts, records, hashes, changed = Counter(), [], {}, 0
    dispositions = 0
    for reviewer in ('agent_a', 'agent_b'):
        primary = read(original_directory, reviewer+'.json'); original = unseal(primary)
        require(mb['primary_hashes'][reviewer] == primary['hash'], 'Methods primary mismatch')
        filename = a_file if reviewer == 'agent_a' else b_file
        require(Path(filename).name == filename, 'Correction filename must be local')
        envelope = read(corrected_directory, filename); body = unseal(envelope)
        require(body['original_primary_hash'] == primary['hash'] and body['registration_hash'] == registration['hash'], 'Original binding mismatch')
        require(body['methods_subset_hash'] == subset['hash'] and body['methods_peer_hash'] == methods['hash'], 'Correction methods mismatch')
        require(body['human_certified'] is False and body['historical_feature_eligible'] is False, 'Certification forbidden')
        review = body['corrected_review']
        validate_primary(original, spec, inputs, registration['hash'], reviewer)
        validate_primary(review, spec, inputs, registration['hash'], reviewer)
        expected = expected_findings(sb, mb, set(spec['batches'][reviewer]))
        for finding in body.get('additional_findings', []):
            bid, fid = finding['bill_id'], finding['id']
            require(bid in spec['batches'][reviewer] and fid.startswith('self:'+bid+':') and fid not in expected, 'Invalid additional finding')
            require(isinstance(finding['description'], str) and finding['description'].strip(), 'Missing additional rationale')
            check_quote(finding, byid[bid]['text'])
            expected[fid] = bid
        changed += validate_changes(original, review, body['changes'], expected)
        dispositions += len(expected)
        records.extend(review['records']); hashes[reviewer] = envelope['hash']
        for row in review['records']: counts.update(row['mechanisms'].values())
    result = seal(dict(corrected_hashes=hashes, cases=len(records), changed_cases=changed,
                       status_counts=dict(counts), effect_count=sum(len(r['effects']) for r in records),
                       finding_dispositions=dispositions,
                       human_certified=False, historical_feature_eligible=False, semantic_accuracy_verified=False))
    by_bill = {row['bill_id']: row for row in records}
    dataset = seal(dict(schema='mechanism-corrected-design-v1',
                        original_registration_hash=registration['hash'], corrected_hashes=hashes,
                        methods_subset_hash=subset['hash'], methods_peer_hash=methods['hash'],
                        records=[by_bill[row['bill_id']] for row in inputs],
                        human_certified=False, historical_feature_eligible=False,
                        purpose='Provisional corrected design annotations; not predictive-ready ground truth'))
    persist_or_compare(corrected_directory/'corrected-dataset.json', dataset)
    persist_or_compare(corrected_directory/'integrity-audit.json', result)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('original_directory', type=Path); parser.add_argument('corrected_directory', type=Path)
    parser.add_argument('--a-file', default='corrected-agent-a.json'); parser.add_argument('--b-file', default='corrected-agent-b.json')
    args = parser.parse_args()
    print(json.dumps(run(args.original_directory, args.corrected_directory, args.a_file, args.b_file), indent=2))
