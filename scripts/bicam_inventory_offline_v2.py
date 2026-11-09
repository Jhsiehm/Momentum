"""Registered offline identity projection with explicit LF-record dialect assumption."""
import argparse
import csv
import io
import json
import pathlib
import re
from scripts import bicam_inventory_audit_v1 as v1

VERSION = 'bicam-inventory-offline-v2'
SOURCE = pathlib.Path('data/research-runs/bicam-inventory-audit-v1-20261108')
SOURCE_HASH = 'b1c21c729eedcc9868424d9f8813bf8d40c074d120445428ea90bbca99025832'


def escape_title_cr(raw):
    """Escape only unquoted bare CR in zero-based title column four."""
    output = bytearray()
    ledger = []
    quoted = False
    field = 0
    field_start = True
    i = 0
    while i < len(raw):
        byte = raw[i]
        if byte == 34:
            if quoted and i + 1 < len(raw) and raw[i+1] == 34:
                output.extend(b'""'); i += 2; continue
            if quoted:
                quoted = False
            elif field_start:
                quoted = True
            else:
                raise ValueError('Unquoted interior quote')
        elif not quoted:
            if byte == 44:
                field += 1; field_start = True
                output.append(byte); i += 1; continue
            if byte == 10:
                field = 0; field_start = True
                output.append(byte); i += 1; continue
            if byte == 13 and not (i + 1 < len(raw) and raw[i+1] == 10):
                if field != 4:
                    raise ValueError('Bare CR outside title field')
                ledger.append({'source_offset': i, 'projected_offset': len(output), 'source_byte': 13, 'replacement_hex': '5c72'})
                output.extend(b'\\r'); field_start = False; i += 1; continue
        output.append(byte)
        field_start = False
        i += 1
    if quoted:
        raise ValueError('Unclosed quote')
    transformed = bytes(output)
    restored = bytearray(transformed)
    for item in reversed(ledger):
        p = item['projected_offset']
        if restored[p:p+2] != b'\\r':
            raise ValueError('Reversal marker mismatch')
        restored[p:p+2] = b'\r'
    if bytes(restored) != raw:
        raise ValueError('Reversal mismatch')
    return transformed, ledger


def integral_congress(value):
    if not re.fullmatch(r'[1-9][0-9]*(?:\.0+)?', value):
        raise ValueError('Congress not exact positive integral decimal')
    return str(int(value.split('.')[0]))


def project(raw):
    escaped, ledger = escape_title_cr(raw)
    reader = csv.reader(io.StringIO(escaped.decode('utf-8-sig'), newline=''), strict=True)
    header = next(reader)
    fields = ('bill_id', 'bill_type', 'bill_number', 'congress', 'introduced_at')
    if len(header) != 24 or len(set(header)) != 24 or header[4] != 'title' or not set(fields) <= set(header):
        raise ValueError('Unexpected schema')
    indexes = [header.index(f) for f in fields]
    output = io.StringIO(newline='')
    writer = csv.writer(output)
    writer.writerow(fields)
    converted = 0
    count = 0
    for row in reader:
        count += 1
        if len(row) != 24:
            raise ValueError('Unresolved CSV row width')
        identity = [row[i] for i in indexes]
        congress = integral_congress(identity[3])
        converted += int(congress != identity[3])
        identity[3] = congress
        writer.writerow(identity)
    return output.getvalue().encode(), ledger, count, converted, v1.digest(escaped)


def run(output):
    output.mkdir(parents=True, exist_ok=False)
    source = SOURCE / 'bills.csv'
    if v1.digest(source.read_bytes()) != SOURCE_HASH:
        raise ValueError('Source hash mismatch')
    registration = dict(version=VERSION, source_sha256=SOURCE_HASH,
        previous_registration_sha256=v1.digest((SOURCE/'registration.json').read_bytes()),
        previous_failure_sha256=v1.digest((SOURCE/'failure.json').read_bytes()),
        code_sha256=v1.digest(pathlib.Path(__file__).read_bytes()),
        imported_v1_sha256=v1.digest(pathlib.Path(v1.__file__).read_bytes()),
        tests_sha256=v1.digest(pathlib.Path('tests/test_bicam_inventory_offline_v2.py').read_bytes()),
        independent_tests_sha256=v1.digest(pathlib.Path('tests/test_bicam_offline_independent.py').read_bytes()),
        protocol_sha256=v1.digest(pathlib.Path('docs/research/BICAM_INVENTORY_OFFLINE_V2.md').read_bytes()),
        network_requests=0, source_exposure='v1 structural diagnosis; no labels/text inspection',
        dialect='LF or CRLF record separator; unquoted bare CR only in title is reversibly escaped',
        sample_rule='first100 ascending SHA256(version+newline+canonicalbillid), only if no issues')
    v1.save(output/'registration.json', registration)
    try:
        projection, ledger, count, converted, escaped_hash = project(source.read_bytes())
        v1.save(output/'title-cr-offsets.json', ledger)
        with (output/'identity-projection.csv').open('xb') as stream:
            stream.write(projection)
        result = v1.inventory(projection)
        sample = sorted(result['rows'], key=lambda x: v1.digest((VERSION+'\n'+x['bill_id']).encode()))[:100] if not result['issues'] else []
        result.pop('sample')
        census_hash = v1.save(output/'identity-census.json', result)
        sample_hash = v1.save(output/'sample.json', sample)
        reference_raw = (SOURCE/'ref_bill_version_codes.csv').read_bytes()
        if v1.digest(reference_raw) != '903dc1df42f67b401228efb5ec25adbac283ed5c8c8573f0ed24c133f0783f66':
            raise ValueError('Reference hash mismatch')
        reference = list(csv.DictReader(io.StringIO(reference_raw.decode(), newline='')))
        v1.save(output/'version-reference.json', reference)
        v1.save(output/'result.json', dict(version=VERSION, source_rows=count, congress_normalizations=converted,
            title_cr_escapes=len(ledger), reversible=True, escaped_sha256=escaped_hash,
            projection_sha256=v1.digest(projection), census_sha256=census_hash, sample_sha256=sample_hash,
            disposition='inventory_complete_under_declared_dialect' if not result['issues'] else 'issues_block_sample',
            counts=result['counts'], issues=len(result['issues']), sampled=len(sample), reference_rows=len(reference),
            network_requests=0, model_fits=0, labels_examined=0, historical_eligibility_established=False))
    except Exception as exc:
        v1.save(output/'failure.json', dict(error_type=type(exc).__name__, error=str(exc)))
        raise


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output', required=True, type=pathlib.Path)
    run(parser.parse_args().output)
