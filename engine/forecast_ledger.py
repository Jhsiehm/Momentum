"""Local source capture and paired forecast receipts; never research certification.

This separate ledger does not fit models or call the legacy prospective recorder.
Exact bytes and a SQLite append chain make ordinary corruption detectable. They
do not provide an independent timestamp or protect against rewriting the entire
local ledger. Certified issuance is deliberately unavailable in this version.
"""
import argparse
import hashlib
import http.client
import json
import math
import os
import re
import sqlite3
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import uuid
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

VERSION = 'forecast-ledger-v1'
TARGET = 'originating_chamber_passage_within_90_days_at_day_30'
HOSTS = {'www.govinfo.gov', 'govinfo.gov', 'www.congress.gov', 'congress.gov'}
MAX_BYTES = 10_000_000


def require(value, message):
    if not value:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def fingerprint(value):
    return sha256(canonical(value))


def instant(value):
    require(isinstance(value, str) and 'T' in value, 'Timestamp must include time and timezone')
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    require(result.tzinfo is not None, 'Timestamp must have a timezone')
    return result.astimezone(timezone.utc)


def now():
    # Preserve microseconds: truncation can admit post-cutoff evidence.
    return datetime.now(timezone.utc).isoformat(timespec='microseconds').replace('+00:00', 'Z')


def bill_identity(value):
    require(isinstance(value, str), 'Bill identity must be a string')
    match = re.fullmatch(r'(hr|s)([1-9][0-9]*)-([1-9][0-9]*)', value)
    require(match is not None, 'Expected canonical bill identity such as hr1-118')
    return match.group(1), int(match.group(2)), int(match.group(3))


def source_url(url, bill_id, source_kind):
    require(isinstance(url, str), 'URL must be a string')
    parsed = urllib.parse.urlsplit(url)
    require(parsed.scheme == 'https' and parsed.hostname in HOSTS,
            'Only official GovInfo or Congress HTTPS hosts are allowed')
    require(not parsed.username and not parsed.password and parsed.port in (None, 443)
            and not parsed.query and not parsed.fragment, 'Credentials, queries and fragments are prohibited')
    require(parsed.netloc in HOSTS or parsed.netloc in {h + ':443' for h in HOSTS}, 'Noncanonical host')
    if source_kind == 'inventory':
        require(bill_id is None and parsed.hostname in {'www.govinfo.gov', 'govinfo.gov'}
                and re.fullmatch(r'/bulkdata/BILLSTATUS/[1-9][0-9]*/(?:hr|s)/?', parsed.path),
                'Inventory requires an exact GovInfo chamber directory and no bill identity')
    else:
        require(source_kind == 'billstatus', 'Unsupported source kind')
        chamber, number, congress = bill_identity(bill_id)
        expected = f'/bulkdata/BILLSTATUS/{congress}/{chamber}/BILLSTATUS-{congress}{chamber}{number}.xml'
        require(parsed.hostname in {'www.govinfo.gov', 'govinfo.gov'} and parsed.path == expected,
                'Bill-status URL does not match bill identity')
    return url


def _billstatus_identity(data, bill_id):
    try:
        require(b'<!DOCTYPE' not in data.upper() and b'<!ENTITY' not in data.upper(), 'DTD/entity declarations are prohibited')
        root = ET.fromstring(data)
        for node in root.iter():
            node.tag = node.tag.rsplit('}', 1)[-1]
        require(root.tag == 'billStatus' and len(root.findall('bill')) == 1,
                'Expected billStatus root and exactly one bill')
        bill = root.find('bill')
        require(not bill.findall('billType') and not bill.findall('billNumber'),
                'Legacy or mixed identity schema requires a separately reviewed adapter')

        def scalar(name):
            elements = bill.findall(name)
            require(len(elements) == 1 and len(elements[0]) == 0 and elements[0].text is not None,
                    'Missing or ambiguous XML identity field: ' + name)
            return elements[0].text.strip()

        chamber, number, congress = bill_identity(bill_id)
        require(scalar('type').lower() == chamber and scalar('number') == str(number)
                and scalar('congress') == str(congress), 'XML bill identity mismatch')
    except (ET.ParseError, ValueError, TypeError) as exc:
        return False, str(exc)
    return True, None


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, file, code, message, headers, newurl):
        return None


class Ledger:
    """Bounded local ledger. Call close(), or use it as a context manager."""

    def __init__(self, root, create=True):
        self.root = Path(root)
        if create:
            self.root.mkdir(parents=True, exist_ok=True)
            (self.root / 'objects').mkdir(exist_ok=True)
        else:
            require((self.root / 'ledger.sqlite').is_file(), 'Ledger does not exist')
        self.db = sqlite3.connect(str(self.root / 'ledger.sqlite'), timeout=30, isolation_level=None)
        self.db.row_factory = sqlite3.Row
        self.db.execute('PRAGMA synchronous=FULL')
        if create:
            self.db.executescript('''
                CREATE TABLE IF NOT EXISTS receipts(
                    sequence INTEGER PRIMARY KEY, id TEXT UNIQUE NOT NULL,
                    kind TEXT NOT NULL, created_at TEXT NOT NULL, previous TEXT,
                    body TEXT NOT NULL);
                CREATE TRIGGER IF NOT EXISTS receipts_no_update BEFORE UPDATE ON receipts
                    BEGIN SELECT RAISE(ABORT,'Receipts are immutable'); END;
                CREATE TRIGGER IF NOT EXISTS receipts_no_delete BEFORE DELETE ON receipts
                    BEGIN SELECT RAISE(ABORT,'Receipts are immutable'); END;
            ''')

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        self.db.close()

    @staticmethod
    def _envelope(row):
        return dict(sequence=row['sequence'], id=row['id'], kind=row['kind'],
                    created_at=row['created_at'], previous=row['previous'], body=json.loads(row['body']))

    def _rows(self):
        return [self._envelope(r) for r in self.db.execute('SELECT * FROM receipts ORDER BY sequence')]

    def _retain(self, data):
        digest = sha256(data)
        path = self.root / 'objects' / digest
        if path.exists():
            require(path.is_file() and path.read_bytes() == data, 'Existing content-addressed object differs')
            return digest, 'objects/' + digest
        handle, temp = tempfile.mkstemp(prefix='.pending-', dir=str(self.root / 'objects'))
        try:
            with os.fdopen(handle, 'wb') as out:
                out.write(data)
                out.flush()
                os.fsync(out.fileno())
            try:
                # Atomic exclusive link; an interrupted write never exposes partial final bytes.
                os.link(temp, path)
            except FileExistsError:
                require(path.read_bytes() == data, 'Concurrent object differs')
            directory = os.open(str(path.parent), os.O_RDONLY)
            try:
                os.fsync(directory)
            finally:
                os.close(directory)
        finally:
            os.unlink(temp)
        return digest, 'objects/' + digest

    def _validate_rows(self, rows):
        previous, clock = None, None
        by_id, starts, finished, issued = {}, set(), set(), set()
        for seq, item in enumerate(rows, 1):
            require(item['sequence'] == seq and item['previous'] == previous, 'Receipt sequence/chain mismatch')
            require(item['id'] == fingerprint({k: v for k, v in item.items() if k != 'id'}), 'Receipt digest mismatch')
            timestamp = instant(item['created_at'])
            require(clock is None or timestamp >= clock, 'Ledger clock moved backward')
            body, kind = item['body'], item['kind']
            require(body.get('version') == VERSION, 'Unknown ledger version')
            if kind == 'capture_started':
                source_url(body['url'], body['bill_id'], body['source_kind'])
                registration_id = body.get('registration_id')
                if registration_id is not None:
                    require(registration_id in by_id and by_id[registration_id]['kind'] == 'registration'
                            and by_id[registration_id]['body']['spec']['mode'] == 'collection', 'Unknown collection registration')
                    require(body['implementation_sha256'] == by_id[registration_id]['body']['implementation_sha256'],
                            'Collector implementation changed after registration')
                starts.add(item['id'])
            elif kind == 'source':
                start_id = body['start_id']
                require(start_id in starts and start_id not in finished, 'Missing/duplicate capture start')
                start = by_id[start_id]
                for field in ('url', 'bill_id', 'source_kind', 'registration_id'):
                    require(body.get(field) == start['body'].get(field), 'Source identity changed during capture')
                require(body['request_started_at'] == start['created_at'], 'Request start time changed')
                require(instant(body['completed_at']) >= instant(start['created_at'])
                        and instant(body['completed_at']) <= timestamp, 'Invalid source completion time')
                require(body['raw_path'] == 'objects/' + body['raw_sha256'], 'Noncanonical raw path')
                path = self.root / body['raw_path']
                require(path.is_file(), 'Missing raw source bytes')
                data = path.read_bytes()
                require(len(data) == body['byte_count'] and sha256(data) == body['raw_sha256'], 'Raw source digest/size mismatch')
                require(body['attestation'] == 'local_observation_only' and body['certified'] is False, 'Unsupported certification')
                if body['disposition'] == 'complete' and body['source_kind'] == 'billstatus':
                    require(_billstatus_identity(data, body['bill_id'])[0], 'Raw source identity mismatch')
                finished.add(start_id)
            elif kind == 'registration':
                require(body['spec_hash'] == fingerprint(body['spec']), 'Registration hash mismatch')
            elif kind == 'forecast_pair':
                require(body['certified'] is False and body['release_eligible'] is False, 'Unsupported certification')
                key = (body['registration_id'], body['case']['bill_id'], instant(body['case']['cutoff']))
                require(key not in issued, 'Duplicate forecast pair')
                issued.add(key)
                self._validate_pair(body['registration_id'], body['case'], body['predictions'], by_id,
                                    item['created_at'], verify=True)
            else:
                raise ValueError('Unknown receipt kind')
            by_id[item['id']] = item
            previous, clock = item['id'], timestamp
        return dict(version=VERSION, receipts=len(rows), sources=len(finished),
                    pending_captures=sorted(starts - finished), forecast_pairs=len(issued),
                    head=previous, integrity='verified', certified=False,
                    limitation='Local chain only; no independently attested timestamp or protection against total rewrite.')

    def verify(self):
        # The read transaction gives one consistent chain snapshot across processes.
        self.db.execute('BEGIN')
        try:
            return self._validate_rows(self._rows())
        finally:
            self.db.execute('ROLLBACK')

    def read(self, receipt_id):
        self.verify()
        row = self.db.execute('SELECT * FROM receipts WHERE id=?', (receipt_id,)).fetchone()
        require(row is not None, 'Receipt not found')
        return self._envelope(row)

    def _append(self, kind, body, validate=None):
        # Explicit SQLite write transaction serializes competing appenders.
        self.db.execute('BEGIN IMMEDIATE')
        try:
            rows = self._rows()
            self._validate_rows(rows)
            created_at = now()
            require(not rows or instant(created_at) >= instant(rows[-1]['created_at']), 'Ledger clock moved backward')
            if validate is not None:
                validate(rows, created_at)
            body = json.loads(canonical(dict(body, version=VERSION)))
            item = dict(sequence=len(rows) + 1, kind=kind, created_at=created_at,
                        previous=rows[-1]['id'] if rows else None, body=body)
            item['id'] = fingerprint(item)
            self._validate_rows(rows + [item])
            self.db.execute('INSERT INTO receipts VALUES (?,?,?,?,?,?)',
                            (item['sequence'], item['id'], kind, created_at, item['previous'], canonical(body).decode()))
            self.db.execute('COMMIT')
            return item
        except BaseException:
            self.db.execute('ROLLBACK')
            raise

    def register(self, spec):
        """Freeze a collection plan or local paired-forecast plan before use."""
        spec = json.loads(canonical(spec))
        require(spec.get('mode') in ('collection', 'local_forecast'), 'Unsupported registration mode')
        require(isinstance(spec.get('protocol_sha256'), str) and re.fullmatch('[0-9a-f]{64}', spec['protocol_sha256']),
                'Registration requires protocol SHA-256')
        if spec['mode'] == 'local_forecast':
            require(spec.get('target') == TARGET and spec.get('checkpoint_days') == 30
                    and spec.get('horizon_days') == 90, 'Wrong target/checkpoint/horizon')
            require(type(spec.get('issuance_tolerance_seconds')) is int
                    and 0 <= spec['issuance_tolerance_seconds'] <= 60, 'Invalid issuance tolerance')
            require(isinstance(spec.get('models'), dict) and len(spec['models']) >= 2
                    and 'stage_reference' in spec['models'], 'Require paired models including stage_reference')
            require(all(isinstance(k, str) and k and isinstance(v, dict) and v
                        for k, v in spec['models'].items()), 'Empty or invalid model artifact')
        return self._append('registration', dict(spec=spec, spec_hash=fingerprint(spec),
                            implementation_sha256=sha256(Path(__file__).read_bytes())))

    def capture(self, url, bill_id=None, source_kind='billstatus', max_bytes=2_000_000, timeout=20, registration_id=None):
        """Perform exactly one HTTP request. Failure receipts retain received bytes.

        Timeout is the socket-operation timeout, not a guaranteed wall-time cap.
        A killed process leaves an immutable capture_started receipt; verification
        reports it as pending instead of inventing a successful completion.
        """
        source_url(url, bill_id, source_kind)
        require(type(max_bytes) is int and 1 <= max_bytes <= MAX_BYTES, 'Invalid byte budget')
        require(type(timeout) in (int, float) and math.isfinite(timeout) and 0 < timeout <= 60, 'Invalid timeout')
        start = self._append('capture_started', dict(request_id=str(uuid.uuid4()), url=url,
                             bill_id=bill_id, source_kind=source_kind, max_bytes=max_bytes,
                             timeout_seconds=timeout, timeout_scope='socket_operation',
                             implementation_sha256=sha256(Path(__file__).read_bytes()),
                             registration_id=registration_id, retries=0, redirects=False))
        chunks, count, status, headers, error, disposition = [], 0, None, {}, None, 'complete'
        opener = urllib.request.build_opener(_NoRedirect)
        response = None
        try:
            request = urllib.request.Request(url, headers={'User-Agent': 'Momentum-source-capture/1.0', 'Accept-Encoding': 'identity'})
            try:
                response = opener.open(request, timeout=timeout)
            except urllib.error.HTTPError as exc:
                response = exc
                disposition = 'http_error'
            with response:
                status = response.status
                require(response.geturl() == url, 'Unexpected final URL')
                headers = {key.lower(): response.headers[key] for key in ('Content-Type', 'Content-Length', 'Date', 'Last-Modified', 'ETag') if response.headers.get(key) is not None}
                while True:
                    try:
                        chunk = response.read(min(65536, max_bytes + 1 - count))
                    except http.client.IncompleteRead as exc:
                        chunks.append(exc.partial)
                        count += len(exc.partial)
                        disposition, error = 'incomplete', 'IncompleteRead'
                        break
                    if not chunk:
                        break
                    chunks.append(chunk)
                    count += len(chunk)
                    if count > max_bytes:
                        disposition, error = 'oversize', 'Byte budget exceeded; retained bounded prefix'
                        break
                declared = headers.get('content-length')
                if disposition == 'complete' and declared is not None and (not declared.isdigit() or int(declared) != count):
                    disposition, error = 'incomplete', 'Content-Length mismatch'
                if status != 200:
                    disposition = 'http_error'
        except Exception as exc:
            # Never serialize exception messages, which may include credentials or remote text.
            disposition, error = 'request_failed', type(exc).__name__
        data = b''.join(chunks)
        identity_valid = None
        if disposition == 'complete':
            if source_kind == 'billstatus':
                identity_valid, identity_error = _billstatus_identity(data, bill_id)
                if not identity_valid:
                    disposition, error = 'identity_or_parse_failure', identity_error
            elif not data or 'html' not in headers.get('content-type', '').lower():
                disposition, error = 'unexpected_content', 'Inventory response is not HTML'
        completed_at = now()
        require(instant(completed_at) >= instant(start['created_at']), 'Clock rollback during acquisition; capture remains pending')
        digest, path = self._retain(data)
        return self._append('source', dict(start_id=start['id'], url=url, bill_id=bill_id,
                            source_kind=source_kind, registration_id=registration_id,
                            request_started_at=start['created_at'], completed_at=completed_at,
                            http_status=status, headers=headers, disposition=disposition, error=error,
                            identity_valid=identity_valid, raw_sha256=digest, raw_path=path, byte_count=len(data),
                            attestation='local_observation_only', certified=False))

    def _validate_pair(self, registration_id, case, predictions, by_id, issued_at, verify=False):
        require(registration_id in by_id and by_id[registration_id]['kind'] == 'registration', 'Unknown registration')
        registration = by_id[registration_id]
        spec = registration['body']['spec']
        require(spec.get('mode') == 'local_forecast', 'Registration is not a forecast plan')
        if not verify:
            require(registration['body']['implementation_sha256'] == sha256(Path(__file__).read_bytes()), 'Implementation changed after registration')
        chamber, number, congress = bill_identity(case['bill_id'])
        require(case.get('target') == spec['target'] and case.get('congress') == congress, 'Case target/identity mismatch')
        introduced, cutoff, horizon = (instant(case[k]) for k in ('introduced_at', 'cutoff', 'horizon'))
        opening = datetime(1787 + 2 * congress, 1, 3, 17, tzinfo=timezone.utc)
        closing = datetime(1789 + 2 * congress, 1, 3, 17, tzinfo=timezone.utc)
        require(opening <= introduced < closing and cutoff == introduced + timedelta(days=30)
                and horizon == cutoff + timedelta(days=90) and horizon < closing, 'Invalid checkpoint/horizon or Congress boundary')
        issued = instant(issued_at)
        require(instant(registration['created_at']) < cutoff, 'Registration must precede cutoff')
        require(cutoff <= issued <= cutoff + timedelta(seconds=spec['issuance_tolerance_seconds']), 'Early or late issuance')
        require(case.get('at_risk') is True and isinstance(case.get('risk_check'), str) and case['risk_check'].strip(),
                'Missing at-risk check; unknown/resolved cases cannot be issued')
        require(isinstance(case.get('family_id'), str) and case['family_id'], 'Missing family identity')
        require(instant(case['features_effective_at']) <= cutoff
                and instant(case['features_available_at']) <= cutoff, 'Future feature evidence')
        features = case.get('features')
        require(isinstance(features, (dict, list)) and features, 'Missing feature snapshot')
        feature_hash = fingerprint(features)
        sources = case.get('source_ids')
        require(isinstance(sources, list) and sources and len(sources) == len(set(sources)), 'Missing/duplicate source receipts')
        for source_id in sources:
            require(source_id in by_id and by_id[source_id]['kind'] == 'source', 'Unknown source receipt')
            source = by_id[source_id]['body']
            require(source['bill_id'] == case['bill_id'] and source['source_kind'] == 'billstatus'
                    and source['disposition'] == 'complete', 'Invalid or mismatched source')
            require(instant(source['completed_at']) <= instant(case['features_available_at']), 'Feature availability predates observed bytes')
        require(isinstance(predictions, dict) and set(predictions) == set(spec['models']), 'Missing or extra paired model')
        for name, prediction in predictions.items():
            require(all(prediction.get(key) == case[key] for key in ('bill_id', 'target', 'cutoff')), 'Prediction case mismatch')
            require(prediction.get('feature_hash') == feature_hash, 'Different paired feature snapshot')
            require(prediction.get('artifact_hash') == fingerprint(spec['models'][name]), 'Frozen model artifact mismatch')
            p = prediction.get('probability')
            require(type(p) in (int, float) and math.isfinite(p) and 0 <= p <= 1, 'Invalid probability')

    def issue_pair(self, registration_id, case, predictions, certified=False):
        """Atomically record caller-computed paired probabilities as local-only.

        Artifact/source/time bindings are validated; statistical validity, family
        completeness and risk assertions are not automatically certified here.
        """
        require(certified is False, 'Certified issuance unavailable: no independently verified timestamp adapter')
        case, predictions = json.loads(canonical(case)), json.loads(canonical(predictions))

        def validate(rows, issued_at):
            by_id = {row['id']: row for row in rows}
            self._validate_pair(registration_id, case, predictions, by_id, issued_at)
            require(not any(row['kind'] == 'forecast_pair' and row['body']['registration_id'] == registration_id
                            and row['body']['case']['bill_id'] == case['bill_id']
                            and instant(row['body']['case']['cutoff']) == instant(case['cutoff']) for row in rows), 'Duplicate forecast pair')
        return self._append('forecast_pair', dict(registration_id=registration_id, case=case,
                            predictions=predictions, certified=False, release_eligible=False,
                            attestation='local_observation_only', prediction_origin='caller_computed_frozen_artifact'), validate)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    capture = sub.add_parser('capture')
    capture.add_argument('root')
    capture.add_argument('url')
    capture.add_argument('--bill-id')
    capture.add_argument('--source-kind', choices=('inventory', 'billstatus'), default='billstatus')
    capture.add_argument('--max-bytes', type=int, default=2_000_000)
    capture.add_argument('--timeout', type=float, default=20)
    capture.add_argument('--registration-id')
    verify = sub.add_parser('verify')
    verify.add_argument('root')
    register = sub.add_parser('register')
    register.add_argument('root')
    register.add_argument('spec')
    args = parser.parse_args()
    with Ledger(args.root, create=args.command != 'verify') as ledger:
        if args.command == 'capture':
            result = ledger.capture(args.url, args.bill_id, args.source_kind, args.max_bytes, args.timeout, args.registration_id)
        elif args.command == 'register':
            result = ledger.register(json.loads(Path(args.spec).read_text()))
        else:
            result = ledger.verify()
    print(json.dumps(result, sort_keys=True, allow_nan=False))


if __name__ == '__main__':
    main()
