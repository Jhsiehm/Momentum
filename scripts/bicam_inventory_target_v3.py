"""Offline outcome-blind target inventory with explicit evidence-backed sidecars."""
import argparse
import collections
import csv
import datetime
import io
import json
import pathlib
import re
from scripts import bicam_inventory_audit_v1 as v1
from scripts import bicam_inventory_offline_v2 as v2

VERSION = 'bicam-inventory-target-v3'
RECONCILIATION = pathlib.Path('data/research-runs/bicam-five-record-20261109/reconciliation.json')
RECONCILIATION_HASH = '8df8d519dc6206033a3130fd784de818c7ab3fa26eaedf1039d62f1531f88a67'
REFERENCE_HASH = '903dc1df42f67b401228efb5ec25adbac283ed5c8c8573f0ed24c133f0783f66'
FIELDS = ('bill_id', 'bill_type', 'bill_number', 'congress', 'introduced_at')
TYPES = ('hr', 's', 'hres', 'sres', 'hjres', 'sjres', 'hconres', 'sconres')
EXPECTED_REPAIRS = {'s4653-116', 's4899-117', 's5314-118', 's5543-118', 's5575-118'}


def repair_map(reconciliation):
    cases = reconciliation['cases']
    result = {}
    for case in cases:
        bid = case['bill_id']
        if bid in result or case['original'] != {'congress': '', 'introduced_at': ''}:
            raise ValueError('Invalid/duplicate reconciliation')
        if case['historical_byte_availability'] is not False or case['source_values_overwritten'] is not False:
            raise ValueError('Invalid reconciliation claims')
        if not re.fullmatch('[0-9a-f]{64}', case['evidence_sha256']):
            raise ValueError('Missing evidence hash')
        result[bid] = case
    if set(result) != EXPECTED_REPAIRS:
        raise ValueError('Unexpected repair identity set')
    return result


def target_inventory(raw, repairs):
    escaped, offsets = v2.escape_title_cr(raw)
    reader = csv.reader(io.StringIO(escaped.decode('utf-8-sig'), newline=''), strict=True)
    header = next(reader)
    if len(header) != 24 or len(set(header)) != 24 or header[4] != 'title' or not set(FIELDS) <= set(header):
        raise ValueError('Unexpected schema')
    indexes = [header.index(f) for f in FIELDS]
    counts = collections.Counter()
    errors, quarantine, rows, applied = [], [], [], []
    seen = set()
    for row_number, values in enumerate(reader, 2):
        counts['source_rows'] += 1
        if len(values) != 24:
            errors.append({'row': row_number, 'issue': 'invalid_width', 'width': len(values)})
            continue
        original = dict(zip(FIELDS, [values[i] for i in indexes]))
        bid, kind, number = original['bill_id'].lower(), original['bill_type'].lower(), original['bill_number']
        base = {'row': row_number, 'original': original}
        match = re.fullmatch(r'([a-z]+)([1-9][0-9]*)-([1-9][0-9]*)', bid)
        if not match or kind not in TYPES or kind != match[1] or number != match[2]:
            errors.append(dict(base, issue='invalid_identity')); continue
        if bid in seen:
            errors.append(dict(base, issue='duplicate_canonical_identity')); continue
        seen.add(bid)
        id_congress = int(match[3])
        target = kind in ('hr', 's') and 113 <= id_congress <= 118
        congress_value = original['congress']
        date_value = original['introduced_at']
        if congress_value == '':
            counts['missing_congress_rows'] += 1
            if not target:
                quarantine.append(dict(base, bill_id=bid, identifier_congress=id_congress,
                                       scope='outside_target_by_validated_identifier', issue='missing_congress'))
                counts['outside_target_quarantined'] += 1
                continue
            if bid not in repairs or {'congress': congress_value, 'introduced_at': date_value} != repairs[bid]['original']:
                errors.append(dict(base, issue='unhandled_target_missing_metadata')); continue
            proposed = repairs[bid]['proposed']
            if type(proposed['congress']) is not int or proposed['congress'] != id_congress:
                errors.append(dict(base, issue='repair_identity_conflict')); continue
            congress_value = str(proposed['congress'])
            date_value = proposed['introduced_at']
            applied.append(dict(base, bill_id=bid, proposed=proposed, evidence_sha256=repairs[bid]['evidence_sha256']))
        elif bid in repairs:
            errors.append(dict(base, issue='repair_original_not_missing')); continue
        try:
            congress = int(v2.integral_congress(congress_value))
        except ValueError:
            errors.append(dict(base, issue='invalid_congress')); continue
        if congress != id_congress:
            errors.append(dict(base, issue='congress_identity_conflict')); continue
        if not target:
            counts['outside_target_valid_identity'] += 1
            continue
        try:
            date = datetime.date.fromisoformat(date_value[:10])
            if date.isoformat() != date_value and not re.fullmatch(r'\d{4}-\d{2}-\d{2}[ T]00:00:00(?:\.0+)?', date_value):
                raise ValueError('Unsupported date form')
            start = datetime.date(1789 + 2*(congress-1), 1, 3)
            if not start <= date < datetime.date(start.year+2, 1, 3):
                raise ValueError('Outside Congress')
        except (ValueError, TypeError):
            errors.append(dict(base, issue='invalid_target_introduction')); continue
        day180 = date + datetime.timedelta(days=180)
        before_end = day180 < datetime.date(start.year+2, 1, 3)
        counts[f'{congress}-day180_before_end' if before_end else f'{congress}-day180_on_or_after_end'] += 1
        rows.append(dict(bill_id=bid, bill_type=kind, bill_number=int(number), congress=congress,
                         introduced_at=date.isoformat(), original=original, metadata_reconciled=bid in repairs,
                         day180_date=day180.isoformat(), day180_before_congress_end=before_end,
                         evaluation_exposure='source_readiness_only_not_untouched_confirmatory_evaluation'))
        counts[f'{congress}-{kind}'] += 1
    if {r['bill_id'] for r in applied} != set(repairs):
        errors.append({'issue': 'repair_cases_not_all_applied'})
    if not rows:
        errors.append({'issue': 'empty_target'})
    rows.sort(key=lambda r: (r['congress'], r['bill_type'], r['bill_number']))
    sample = sorted(rows, key=lambda r: v1.digest((VERSION+'\n'+r['bill_id']).encode()))[:100] if not errors else []
    return dict(rows=rows, errors=errors, quarantine=quarantine, applied_repairs=applied,
                title_cr_offsets=offsets, counts=dict(counts), sample=sample,
                target_internal_consistency=not errors, official_coverage_complete=False,
                sample_shortfall=100-len(sample), labels_examined=0)


def run(output):
    output.mkdir(parents=True, exist_ok=False)
    source = v2.SOURCE/'bills.csv'
    reference = v2.SOURCE/'ref_bill_version_codes.csv'
    if v1.digest(source.read_bytes()) != v2.SOURCE_HASH or v1.digest(reference.read_bytes()) != REFERENCE_HASH or v1.digest(RECONCILIATION.read_bytes()) != RECONCILIATION_HASH:
        raise ValueError('Input binding mismatch')
    paths = [pathlib.Path(__file__), pathlib.Path(v1.__file__), pathlib.Path(v2.__file__),
             pathlib.Path('tests/test_bicam_inventory_target_v3.py'),
             pathlib.Path('tests/test_bicam_target_independent.py'),
             pathlib.Path('docs/research/BICAM_INVENTORY_TARGET_V3.md')]
    registration = dict(version=VERSION, files={str(p):v1.digest(p.read_bytes()) for p in paths},
        source_sha256=v2.SOURCE_HASH, reference_sha256=REFERENCE_HASH, reconciliation_sha256=RECONCILIATION_HASH,
        population='Congress113-118 inclusive HR/S', network_requests=0, model_fits=0,
        sample_rule='first100 ascending SHA256(version+newline+canonicalbillid) if target internally consistent',
        exposure='Adaptive source-readiness audit after v1/v2 failures and official-record review; procedural outcomes incidentally visible, not untouched confirmatory evaluation')
    v1.save(output/'registration.json', registration)
    try:
        # Independent schema reference inspection must not depend on sample/census success.
        reference_rows = list(csv.DictReader(io.StringIO(reference.read_text(), newline=''), strict=True))
        v1.save(output/'version-reference.json', reference_rows)
        repairs = repair_map(json.loads(RECONCILIATION.read_text()))
        result = target_inventory(source.read_bytes(), repairs)
        hashes = {}
        for key, name in [('title_cr_offsets','title-cr-offsets.json'), ('errors','errors.json'),
                          ('quarantine','quarantine.json'), ('applied_repairs','applied-repairs.json'),
                          ('rows','identity-census.json'), ('sample','sample.json')]:
            hashes[name] = v1.save(output/name, result[key])
        v1.save(output/'result.json', dict(version=VERSION, counts=result['counts'],
            target_rows=len(result['rows']), errors=len(result['errors']), quarantined=len(result['quarantine']),
            applied_repairs=len(result['applied_repairs']), title_cr_escapes=len(result['title_cr_offsets']),
            sample_rows=len(result['sample']), sample_shortfall=result['sample_shortfall'],
            target_internal_consistency=result['target_internal_consistency'], official_coverage_complete=False,
            reference_rows=len(reference_rows), artifact_sha256=hashes, network_requests=0, model_fits=0,
            historical_eligibility_established=False, labels_examined=0))
    except Exception as exc:
        v1.save(output/'failure.json', {'error_type':type(exc).__name__, 'error':str(exc)})
        raise

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',required=True,type=pathlib.Path)
    run(parser.parse_args().output)
