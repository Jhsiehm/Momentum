"""Resumable official ingestion. Retrieval never backdates public availability."""
import hashlib
import json
import os
import random
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from .store import ROOT, congress_end, digest, now, timestamp


def fetch(url, attempts=4):
    for attempt in range(attempts):
        try:
            request = urllib.request.Request(url, headers={'User-Agent': 'LegislativeResearchPrototype/1.0'})
            with urllib.request.urlopen(request, timeout=30) as response:
                return response.read()
        except urllib.error.HTTPError as error:
            if error.code not in (429, 500, 502, 503, 504) or attempt == attempts - 1:
                raise RuntimeError(f'Source request failed (HTTP {error.code})') from None
            retry = error.headers.get('Retry-After', '')
            time.sleep(min(30, float(retry) if retry.isdigit() else 2 ** attempt + random.random()))
        except (urllib.error.URLError, TimeoutError):
            if attempt == attempts - 1:
                raise RuntimeError('Source request timed out or could not connect') from None
            time.sleep(2 ** attempt + random.random())


def retain(raw):
    sha = hashlib.sha256(raw).hexdigest()
    path = ROOT / 'data' / 'raw' / sha
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_bytes(raw)
    return sha


def stage_for(code, text, kind):
    # Conservative mapping; unknown actions never imply advancement.
    if code == '36000' or 'Became Public Law' in text:
        return 4
    if code in ('28000', '38000'):
        return 3
    if (kind == 'hr' and code == 'H30000') or (kind == 's' and code == '17000'):
        return 2
    if code in ('H10000', '14000', '1000') and ('Reported' in text or 'reported' in text):
        return 1
    return 0


def import_xml(store, raw, source_url, observed=None):
    if b'<!DOCTYPE' in raw.upper() or b'<!ENTITY' in raw.upper():
        raise ValueError('DTD/entity declarations are not accepted')
    root = ET.fromstring(raw)
    bill = root.find('bill')
    if bill is None:
        raise ValueError('Expected GovInfo billStatus/bill XML')
    congress, kind, number = int(bill.findtext('congress')), bill.findtext('type', '').lower(), bill.findtext('number', '')
    if kind not in ('hr', 's') or not number.isdigit():
        raise ValueError('Initial universe supports H.R. and S. public bills only')
    bill_id = f'{congress}-{kind}{number}'
    sha = retain(raw)
    checkpoint = f'raw:{bill_id}:{sha}'
    if store.checkpoint(checkpoint):
        return {'bill_id': bill_id, 'status': 'unchanged', 'hash': sha}
    retrieved = timestamp(observed or now())
    introduced = timestamp(bill.findtext('introducedDate'))
    common = {'bill_id': bill_id, 'family_id': bill_id, 'dataset': 'official',
              'source_name': 'GovInfo / Library of Congress', 'source_url': source_url,
              'observed_at': retrieved, 'published_at': None, 'raw_hash': sha,
              'family_status': 'unadjudicated singleton', 'coverage': 'current bulk snapshot; historical availability unverified'}
    title = bill.findtext('title') or 'Untitled measure'
    store.add('bill', dict(common, source_key=bill_id, congress=congress, type=kind, title=title,
                          topic=bill.findtext('policyArea/name') or 'Unclassified',
                          sponsor=bill.findtext('sponsors/item/fullName') or 'Unknown',
                          introduced_at=introduced, effective_at=introduced,
                          official_url=f'https://www.congress.gov/bill/{congress}th-congress/{"house" if kind == "hr" else "senate"}-bill/{number}'))
    for action in bill.findall('actions/item'):
        action_date = action.findtext('actionDate')
        if not action_date:
            continue
        text = action.findtext('text', '')
        code = action.findtext('actionCode', '')
        effective = timestamp(action_date)
        key = digest({'bill': bill_id, 'date': action_date, 'code': code, 'text': text})
        stage = stage_for(code, text, kind)
        store.add('event', dict(common, source_key=key, effective_at=effective, text=text, action_code=code, stage=stage))
        if stage == 4:
            store.add('resolution', dict(common, source_key=bill_id + '-enactment', effective_at=effective,
                                         value=1, complete_coverage=False, definition='Official own-bill public-law action'))
    # Absence of a public-law action is not proof of failure; adjudicate negatives separately.
    store.checkpoint(checkpoint, {'retrieved_at': retrieved, 'hash': sha})
    return {'bill_id': bill_id, 'status': 'imported', 'hash': sha}


def ingest_bill(store, congress, kind, number, refresh=False):
    if kind not in ('hr', 's') or not 93 <= int(congress) <= 200 or int(number) <= 0:
        raise ValueError('Invalid bill identifier')
    url = f'https://www.govinfo.gov/bulkdata/BILLSTATUS/{int(congress)}/{kind}/BILLSTATUS-{int(congress)}{kind}{int(number)}.xml'
    key = f'fetch:{congress}:{kind}:{number}'
    cached = store.checkpoint(key)
    if cached and not refresh:
        return dict(cached, status='cached')
    result = import_xml(store, fetch(url), url)
    store.checkpoint(key, result)
    return result


def sync_congress(store, congress, limit=20):
    key = os.environ.get('CONGRESS_API_KEY')
    if not key:
        raise ValueError('CONGRESS_API_KEY is required for incremental discovery; GovInfo single-bill import needs no key.')
    cursor_key = f'congress-sync:{congress}'
    checkpoint = store.checkpoint(cursor_key) or {'offset': 0}
    offset = checkpoint.get('offset', 0)
    params = {'api_key': key, 'format': 'json', 'limit': min(250, limit), 'offset': offset, 'sort': 'updateDate+asc'}
    if checkpoint.get('watermark'):
        params['fromDateTime'] = checkpoint['watermark']
    payload = json.loads(fetch(f'https://api.congress.gov/v3/bill/{int(congress)}?' + urllib.parse.urlencode(params)))
    retain(json.dumps(payload, sort_keys=True).encode())
    results = []
    bills = payload.get('bills', [])
    for bill in bills:
        kind = bill['type'].lower()
        if kind in ('hr', 's'):
            results.append(ingest_bill(store, congress, kind, int(bill['number']), refresh=True))
    # Commit page cursor only after the entire page succeeds. Content hashes deduplicate retries.
    if payload.get('pagination', {}).get('next'):
        checkpoint['offset'] = offset + len(bills)
    else:
        checkpoint = {'offset': 0, 'watermark': max([b.get('updateDate', '') for b in bills] + [checkpoint.get('watermark', '')])}
    checkpoint['last_success'] = now()
    store.checkpoint(cursor_key, checkpoint)
    return results


def import_audited_records(store, path):
    """Operator-reviewed canonical JSONL; archive claims remain human assertions."""
    raw = Path(path).read_bytes()
    file_hash = retain(raw)
    checkpoint_key = 'audited:' + file_hash
    checkpoint = store.checkpoint(checkpoint_key) or {'next_line': 0}
    lines = raw.decode().splitlines()
    for index in range(checkpoint['next_line'], len(lines)):
        if lines[index].strip():
            item = json.loads(lines[index])
            record = item['record']
            if record.get('dataset') != 'official':
                raise ValueError('Audited imports must use the official namespace')
            record['import_hash'] = file_hash
            store.add(item['kind'], record)
        store.checkpoint(checkpoint_key, {'next_line': index + 1, 'file_hash': file_hash})
    return {'lines': len(lines), 'file_hash': file_hash, 'status': 'imported'}
