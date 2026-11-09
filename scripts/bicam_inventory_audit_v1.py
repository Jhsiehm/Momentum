"""Bounded identity-only BICAM inventory. Runtime source bytes stay ignored."""
import argparse
import collections
import csv
import datetime
import hashlib
import io
import json
import pathlib
import re
import struct
import time
import urllib.request
import zipfile
import zlib

VERSION = 'bicam-inventory-audit-v1'
URL = 'https://downloads.bicam.net/bills/bicam_bills.zip'
MEMBERS = ('bills.csv', 'ref_bill_version_codes.csv')
PRIOR = pathlib.Path('data/research-runs/historical-dataset-options-20261108')
TAIL_HASH = '8fa40bc106615a3243e505e6d44d8bd4a02119c957412880175ff71166d68a49'
COMPRESSED_CAP = 50_000_000
OUTPUT_CAP = 300_000_000


def digest(data):
    return hashlib.sha256(data).hexdigest()


def save(path, value):
    data = (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()
    with path.open('xb') as stream:
        stream.write(data)
    return digest(data)


def directory(tail, size):
    if digest(tail) != TAIL_HASH:
        raise ValueError('Prior tail hash mismatch')
    archive = zipfile.ZipFile(io.BytesIO(tail))
    names = archive.namelist()
    if len(names) != len(set(names)):
        raise ValueError('Duplicate ZIP member names')
    result = []
    for name in MEMBERS:
        info = archive.getinfo(name)
        offset = info.header_offset + size - len(tail)
        if info.compress_type != 8 or info.flag_bits & 1 or offset < 0:
            raise ValueError('Unsupported ZIP entry')
        result.append(dict(name=name, offset=offset, compressed=info.compress_size,
                           uncompressed=info.file_size, crc=info.CRC, flags=info.flag_bits))
    if sum(x['compressed'] for x in result) > COMPRESSED_CAP or sum(x['uncompressed'] for x in result) > OUTPUT_CAP:
        raise ValueError('Member sizes exceed caps')
    return result


def local_header(raw, entry):
    if len(raw) != 30:
        raise ValueError('Wrong local header size')
    sig, version, flags, method, mtime, mdate, crc, compressed, uncompressed, nlen, elen = struct.unpack('<IHHHHHIIIHH', raw)
    if sig != 0x04034b50 or flags != entry['flags'] or method != 8 or flags & 1:
        raise ValueError('Invalid local header')
    if not flags & 8 and (crc, compressed, uncompressed) != (entry['crc'], entry['compressed'], entry['uncompressed']):
        raise ValueError('Local/directory disagreement')
    if nlen == 0 or nlen + elen > 131070:
        raise ValueError('Invalid filename/extra length')
    return nlen, elen


def inflate(raw, entry):
    if len(raw) != entry['compressed'] or entry['uncompressed'] > OUTPUT_CAP:
        raise ValueError('Compressed length or output cap violation')
    decoder = zlib.decompressobj(-15)
    value = decoder.decompress(raw, entry['uncompressed'] + 1)
    if not decoder.eof or decoder.unused_data or decoder.unconsumed_tail or len(value) != entry['uncompressed']:
        raise ValueError('Incomplete/oversized deflate stream')
    if zlib.crc32(value) & 0xffffffff != entry['crc']:
        raise ValueError('CRC mismatch')
    return value


def inventory(data):
    # CSV parsing necessarily traverses other bytes; only allowlisted fields are retained or examined.
    reader = csv.DictReader(io.StringIO(data.decode('utf-8-sig'), newline=''))
    fields = ('bill_id', 'bill_type', 'bill_number', 'congress', 'introduced_at')
    if not reader.fieldnames or len(reader.fieldnames) != len(set(reader.fieldnames)) or not set(fields) <= set(reader.fieldnames):
        raise ValueError('Missing/duplicate required columns')
    seen = set()
    rows, issues = [], []
    counts = collections.Counter()
    for index, raw in enumerate(reader, 2):
        if None in raw or any(raw.get(f) is None for f in fields):
            raise ValueError('Malformed CSV row')
        row = {f: raw[f] for f in fields}
        counts['source_rows'] += 1
        bid = row['bill_id'].lower()
        if not bid or bid in seen:
            issues.append({'row': index, 'bill_id': bid, 'issue': 'missing_or_duplicate_id'})
            continue
        seen.add(bid)
        try:
            congress = int(row['congress'])
        except ValueError:
            issues.append({'row': index, 'bill_id': bid, 'issue': 'invalid_congress'})
            continue
        kind = row['bill_type'].lower()
        number = row['bill_number']
        if kind not in ('hr', 's', 'hres', 'sres', 'hjres', 'sjres', 'hconres', 'sconres'):
            issues.append({'row': index, 'bill_id': bid, 'issue': 'invalid_bill_type'})
            continue
        if not re.fullmatch('[1-9][0-9]*', number) or bid != f'{kind}{number}-{congress}':
            issues.append({'row': index, 'bill_id': bid, 'issue': 'identity_disagreement'})
            continue
        if congress not in range(113, 119) or kind not in ('hr', 's'):
            counts['outside_scope'] += 1
            continue
        date = row['introduced_at']
        try:
            parsed = datetime.date.fromisoformat(date[:10])
            if date != parsed.isoformat() and not re.fullmatch(r'\d{4}-\d{2}-\d{2}[ T]00:00:00(?:\.0+)?', date):
                raise ValueError('Unexpected date format')
            start = datetime.date(1789 + 2 * (congress - 1), 1, 3)
            end = datetime.date(start.year + 2, 1, 3)
            if not start <= parsed < end:
                raise ValueError('Date outside Congress')
        except ValueError:
            issues.append({'row': index, 'bill_id': bid, 'issue': 'invalid_introduction_date'})
            continue
        rows.append(dict(bill_id=bid, bill_type=kind, bill_number=int(number), congress=congress, introduced_at=parsed.isoformat()))
        counts[f'{congress}-{kind}'] += 1
    if not rows:
        issues.append({'issue': 'empty_selected_population'})
    rows.sort(key=lambda x: (x['congress'], x['bill_type'], x['bill_number']))
    return {'rows': rows, 'counts': dict(counts), 'issues': issues,
            'complete_identity_census': not issues, 'sample_target': 100, 'sample_shortfall': 100 if issues else max(0, 100-len(rows)),
            'sample': sorted(rows, key=lambda x: digest((VERSION + '\n' + x['bill_id']).encode()))[:100] if not issues else []}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def run(output):
    output.mkdir(parents=True, exist_ok=False)
    prior = json.loads((PRIOR / 'zip-result.json').read_text())
    size = int(prior[0]['headers']['Content-Length'])
    etag = prior[0]['headers']['ETag']
    source_version = prior[0]['headers']['x-amz-version-id']
    if etag.startswith('W/') or not etag.startswith(chr(34)):
        raise ValueError('Strong ETag required')
    entries = directory((PRIOR / 'zip-tail.bin').read_bytes(), size)
    code = pathlib.Path(__file__)
    plan = dict(version=VERSION, url=URL, size=size, etag=etag, tail_sha256=TAIL_HASH,
                source_version=source_version, prior_result_sha256=digest((PRIOR / 'zip-result.json').read_bytes()),
                members=entries, max_requests=6, max_compressed_bytes=COMPRESSED_CAP,
                max_output_bytes=OUTPUT_CAP, socket_seconds=20, wall_seconds=180,
                sample_rule='first 100 ascending SHA256(version + newline + bill_id), only if census has no issues',
                population='Congress 113 through 118 inclusive, HR/S only',
                code_sha256=digest(code.read_bytes()), tests_sha256=digest(pathlib.Path('tests/test_bicam_inventory_audit_v1.py').read_bytes()),
                independent_tests_sha256=digest(pathlib.Path('tests/test_bicam_inventory_independent.py').read_bytes()),
                protocol_sha256=digest(pathlib.Path('docs/research/BICAM_INVENTORY_AUDIT_V1.md').read_bytes()))
    save(output / 'registration.json', plan)
    start = time.monotonic()
    requests = []
    opener = urllib.request.build_opener(NoRedirect)

    def fetch(lo, count, name):
        if len(requests) >= 6 or count <= 0 or lo < 0 or lo + count > size or time.monotonic() - start >= 180:
            raise ValueError('Request bound exceeded')
        record = dict(name=name, start=lo, count=count, requested_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
        requests.append(record)
        save(output / f'request-{len(requests):02d}-intent.json', record)
        body = bytearray()
        req = urllib.request.Request(URL, headers={'Range': f'bytes={lo}-{lo+count-1}', 'If-Match': etag, 'Accept-Encoding': 'identity', 'User-Agent': 'Momentum-bounded-inventory/1'})
        try:
            with opener.open(req, timeout=min(20, 180 - (time.monotonic()-start))) as response:
                record.update(status=response.status, headers=dict(response.headers))
                if response.status != 206 or response.headers.get('ETag') != etag or response.headers.get('x-amz-version-id') != source_version or response.headers.get('Content-Range') != f'bytes {lo}-{lo+count-1}/{size}' or response.headers.get('Content-Length') != str(count):
                    raise ValueError('HTTP range identity mismatch')
                body = bytearray()
                while len(body) < count:
                    if time.monotonic() - start >= 180:
                        raise TimeoutError('Whole-run deadline')
                    chunk = response.read(min(65536, count-len(body)))
                    if not chunk:
                        raise ValueError('Truncated range')
                    body.extend(chunk)
                record.update(bytes=len(body), sha256=digest(body))
                with (output / name).open('xb') as stream:
                    stream.write(body)
                return bytes(body)
        finally:
            if body and not (output / name).exists():
                with (output / (name + '.partial')).open('xb') as stream:
                    stream.write(body)
                record.update(partial_bytes=len(body), partial_sha256=digest(body))
            save(output / f'request-{len(requests):02d}.json', record)

    try:
        member_hashes = {}
        for entry in entries:
            name = entry['name']
            header = fetch(entry['offset'], 30, name + '.header.bin')
            nlen, elen = local_header(header, entry)
            extra = fetch(entry['offset'] + 30, nlen + elen, name + '.name-extra.bin')
            if extra[:nlen].decode('utf-8') != name:
                raise ValueError('Local filename mismatch')
            compressed = fetch(entry['offset'] + 30 + nlen + elen, entry['compressed'], name + '.deflate.bin')
            value = inflate(compressed, entry)
            with (output / name).open('xb') as stream:
                stream.write(value)
            member_hashes[name] = digest(value)
        result = inventory((output / 'bills.csv').read_bytes())
        census_hash = save(output / 'identity-census.json', {k:v for k,v in result.items() if k != 'sample'})
        sample_hash = save(output / 'sample.json', result['sample'])
        reference = list(csv.DictReader(io.StringIO((output / MEMBERS[1]).read_text())))
        save(output / 'version-reference.json', reference)
        save(output / 'result.json', dict(version=VERSION, disposition='inventory_complete' if result['complete_identity_census'] else 'identity_issues_block_sample',
             member_sha256=member_hashes, census_sha256=census_hash, sample_sha256=sample_hash,
             counts=result['counts'], issues=len(result['issues']), sampled=len(result['sample']),
             reference_rows=len(reference), request_count=len(requests), downloaded_bytes=sum(r.get('bytes', 0) for r in requests),
             model_fits=0, labels_examined=0, historical_eligibility_established=False))
    except Exception as exc:
        save(output / 'failure.json', {'error_type': type(exc).__name__, 'error': str(exc), 'request_count': len(requests)})
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=pathlib.Path, required=True)
    run(parser.parse_args().output)
