"""Independent, read-only replay of the bounded passage90 source pilot.

Does not import the collector, pilot, inventory parser, or forecasting modules.
No network, fitting, scoring, or certification is performed.
"""
import argparse
from collections import Counter
from datetime import date, datetime, timedelta
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sqlite3
from urllib.parse import urljoin, urlsplit
import xml.etree.ElementTree as ET


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def seal(value):
    return digest(json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode())


def instant(value):
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    require(result.tzinfo is not None, 'Missing timezone')
    return result


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []
        self.closed = False

    def handle_starttag(self, tag, attributes):
        if tag.lower() == 'a':
            self.hrefs.extend(value for key, value in attributes if key.lower() == 'href' and value)

    def handle_endtag(self, tag):
        if tag.lower() == 'html':
            self.closed = True


def scalar(node, path):
    items = node.findall(path)
    require(len(items) == 1 and len(items[0]) == 0, 'Ambiguous scalar: ' + path)
    return (items[0].text or '').strip()


def replay(run, repository):
    registration = json.loads((run / 'registration.json').read_text())
    sample = json.loads((run / 'sample.json').read_text())
    result = json.loads((run / 'result.json').read_text())
    require(registration['version'] == 'passage90-source-pilot-v1', 'Unexpected pilot version')
    require(registration['max_requests'] == 22 and registration['per_chamber'] == 10
            and registration['congress'] == 118 and registration['retries'] == registration['redirects'] == 0,
            'Unexpected registered scope')
    for name, expected in registration['bindings'].items():
        path = Path(name)
        if path.is_absolute():
            # Registered absolute paths are portable when their repository suffix is retained.
            suffix = next((part for part in ('scripts/', 'engine/', 'tests/', 'docs/') if part in name), None)
            require(suffix is not None, 'Unknown absolute binding')
            path = Path(suffix + name.split(suffix, 1)[1])
        require(digest((repository / path).read_bytes()) == expected, 'Registered binding changed: ' + name)

    with sqlite3.connect((run / 'ledger' / 'ledger.sqlite').resolve().as_uri() + '?mode=ro', uri=True) as connection:
        connection.row_factory = sqlite3.Row
        receipts = [dict(row) for row in connection.execute('SELECT * FROM receipts ORDER BY sequence')]
    previous, prior_time, by_id, sources, starts = None, None, {}, [], {}
    for index, item in enumerate(receipts, 1):
        item['body'] = json.loads(item['body'])
        require(item['sequence'] == index and item['previous'] == previous, 'Broken receipt chain')
        require(item['id'] == seal({key: value for key, value in item.items() if key != 'id'}), 'Receipt hash mismatch')
        current = instant(item['created_at'])
        require(prior_time is None or current >= prior_time, 'Clock rollback')
        body = item['body']
        if item['kind'] == 'registration':
            require(index == 1 and body['spec'] == registration and body['spec_hash'] == seal(registration),
                    'Registration differs from frozen file')
            require(item['id'] == sample['registration_id'], 'Sample registration mismatch')
        elif item['kind'] == 'capture_started':
            require(body['registration_id'] == receipts[0]['id'], 'Capture not bound to registration')
            require(body['implementation_sha256'] == registration['bindings']['engine/forecast_ledger.py'], 'Collector changed')
            require(body['retries'] == 0 and body['redirects'] is False, 'Unexpected retry/redirect')
            starts[item['id']] = item
        elif item['kind'] == 'source':
            require(body['start_id'] in starts, 'Missing capture start')
            start = starts.pop(body['start_id'])
            require(body['request_started_at'] == start['created_at'], 'Start time mismatch')
            require(instant(start['created_at']) <= instant(body['completed_at']) <= current, 'Invalid source times')
            for field in ('url', 'bill_id', 'source_kind', 'registration_id'):
                require(body[field] == start['body'][field], 'Source binding mismatch')
            require(body['raw_path'] == 'objects/' + body['raw_sha256'], 'Unexpected raw path')
            raw = (run / 'ledger' / body['raw_path']).read_bytes()
            require(digest(raw) == body['raw_sha256'] and len(raw) == body['byte_count'], 'Raw bytes/hash mismatch')
            require(body['http_status'] == 200 and body['disposition'] == 'complete', 'This replay expects the recorded successful acquisition')
            require(body['certified'] is False and body['attestation'] == 'local_observation_only', 'False certification')
            require(len(raw) <= start['body']['max_bytes'], 'Response exceeds cap')
            sources.append(item)
        else:
            raise ValueError('Unexpected receipt type: ' + item['kind'])
        by_id[item['id']] = item
        previous, prior_time = item['id'], current
    require(len(receipts) == 45 and len(sources) == 22 and not starts, 'Incomplete or excess requests')
    require(len({item['body']['url'] for item in sources}) == 22, 'Repeated request')

    reconstructed, inventory_counts = [], {}
    for entry in sample['inventories']:
        receipt = by_id[entry['receipt_id']]
        body = receipt['body']
        chamber = entry['parsed']['bill_type']
        url = f'https://www.govinfo.gov/bulkdata/BILLSTATUS/118/{chamber}'
        require(body['source_kind'] == 'inventory' and body['url'] == url and chamber in ('hr', 's'), 'Inventory mismatch')
        raw = (run / 'ledger' / body['raw_path']).read_bytes()
        parser = Links()
        parser.feed(raw.decode('utf-8'))
        require(parser.closed, 'Unclosed inventory')
        ids = set()
        for href in parser.hrefs:
            link = urlsplit(urljoin(url + '/', href))
            name = link.path.rsplit('/', 1)[-1]
            if not name.startswith('BILLSTATUS-'):
                continue
            if link.path == f'/bulkdata/BILLSTATUS/118/{chamber}/BILLSTATUS-118-{chamber}.zip':
                continue
            match = re.fullmatch(rf'BILLSTATUS-118{chamber}([1-9][0-9]*)\.xml', name)
            require(match is not None and link.scheme == 'https' and link.netloc == 'www.govinfo.gov'
                    and not link.query and not link.fragment and link.path == f'/bulkdata/BILLSTATUS/118/{chamber}/{name}',
                    'Unexpected inventory bill link')
            ids.add(f'{chamber}{match[1]}-118')
        require(sorted(ids) == entry['parsed']['ids'], 'Inventory membership mismatch')
        inventory_counts[chamber] = len(ids)
        selected = sorted(ids, key=lambda identity: digest(('passage90-source-pilot-v1\n' + identity).encode()))[:10]
        reconstructed.extend(selected)
    require(set(inventory_counts) == {'hr', 's'} and len(sample['inventories']) == 2, 'Missing chamber inventory')
    require(reconstructed == [case['bill_id'] for case in sample['sample']], 'Frozen sample differs from independent hash selection')
    require(reconstructed == [row['case']['bill_id'] for row in result['rows']], 'Result population changed')
    first_bill_start = min(instant(by_id[item['body']['start_id']]['created_at']) for item in sources if item['body']['source_kind'] == 'billstatus')
    require(all(instant(item['body']['completed_at']) <= first_bill_start for item in sources if item['body']['source_kind'] == 'inventory'), 'Bills requested before inventories complete')

    checked = []
    for case, row in zip(sample['sample'], result['rows']):
        require(case == row['case'], 'Case manifest changed')
        receipt = by_id[row['receipt_id']]
        body = receipt['body']
        require(body == row['capture'] and body['bill_id'] == case['bill_id'] and body['url'] == case['url'], 'Result source binding mismatch')
        raw = (run / 'ledger' / body['raw_path']).read_bytes()
        root = ET.fromstring(raw)
        require(root.tag == 'billStatus' and len(root.findall('bill')) == 1, 'Invalid bill root')
        bill = root.find('bill')
        require(scalar(bill, 'congress') == '118' and scalar(bill, 'type').lower() == case['bill_type']
                and scalar(bill, 'number') == str(case['bill_number']), 'Bill identity mismatch')
        introduced = date.fromisoformat(scalar(bill, 'introducedDate'))
        checkpoint, horizon = introduced + timedelta(days=30), introduced + timedelta(days=120)
        require(date(2023, 1, 3) <= introduced < date(2025, 1, 3), 'Introduction outside Congress')
        code, chamber = ('8000', 'House') if case['bill_type'] == 'hr' else ('17000', 'Senate')
        recognized = []
        for index, action in enumerate(bill.findall('actions/item')):
            if not any((node.text or '').strip() == code for node in action.findall('actionCode')):
                continue
            require(scalar(action, 'actionCode') == code and scalar(action, 'sourceSystem/code') == '9', 'Ambiguous recognized passage')
            when, text = scalar(action, 'actionDate'), scalar(action, 'text')
            require(text.startswith('Passed/agreed to in ' + chamber + ':'), 'Unsupported passage wording')
            require(introduced <= date.fromisoformat(when) < date(2025, 1, 3), 'Passage outside lifetime')
            recognized.append(dict(position=index, date=when, code=code, source='9', text=text))
        recognized.sort(key=lambda item: (item['date'], item['position']))
        first = date.fromisoformat(recognized[0]['date']) if recognized else None
        if horizon >= date(2025, 1, 3):
            disposition = 'excluded_incomplete_congress_window'
        elif first in (checkpoint, horizon):
            disposition = 'unresolved_boundary_day'
        elif first and first < checkpoint:
            disposition = 'excluded_already_passed'
        elif first and first < horizon:
            disposition = 'candidate_within_window_passage'
        elif first:
            disposition = 'later_passage_negative_coverage_unverified'
        else:
            disposition = 'unresolved_no_recognized_passage'
        inspection = row['inspection']
        require(inspection['recognized_passage_actions'] == recognized and not inspection['ambiguous_actions'], 'Passage evidence mismatch')
        require(inspection['checkpoint_date'] == checkpoint.isoformat() and inspection['horizon_date'] == horizon.isoformat()
                and inspection['introduced_at'] == introduced.isoformat() and inspection['disposition'] == disposition
                and inspection['action_count'] == len(bill.findall('actions/item'))
                and inspection['full_window'] == (horizon < date(2025, 1, 3)), 'Derived case mismatch')
        require(inspection['certified_label'] is None and inspection['historical_feature_eligibility'] is False, 'Unsupported eligibility claim')
        checked.append(dict(bill_id=case['bill_id'], first_recognized_origin_passage=first.isoformat() if first else None,
                            disposition=disposition, raw_sha256=body['raw_sha256']))
    summary = result['summary']
    require(summary['registration_sha256'] == digest((run / 'registration.json').read_bytes()), 'Registration raw hash mismatch')
    require(summary['dispositions'] == dict(Counter(row['disposition'] for row in checked)), 'Disposition counts mismatch')
    require(summary['inventory_identities'] == sum(inventory_counts.values()) and summary['requests'] == 22
            and summary['selected'] == summary['captured'] == summary['inspected'] == summary['full_windows'] == 20, 'Incorrect denominator')
    require(summary['response_bytes'] == sum(item['body']['byte_count'] for item in sources), 'Response total mismatch')
    for key in ('certified_positive_labels', 'certified_negative_labels', 'historical_eligible', 'externally_attested', 'model_fits', 'forecasts', 'predictive_scores'):
        require(summary[key] == 0, 'Unsupported result: ' + key)
    require(summary['release_eligible'] is False, 'Unsupported release')
    return dict(status='verified', verifier_sha256=digest(Path(__file__).read_bytes()),
                input_sha256={name: digest((run / name).read_bytes()) for name in ('registration.json', 'sample.json', 'result.json')},
                registered_bindings_checked=len(registration['bindings']), ledger_receipts_checked=len(receipts),
                raw_sources_checked=len(sources), inventory_counts=inventory_counts,
                selected_cases_checked=len(checked), cases=checked, source_requests=0, model_fits=0,
                limitation='Independent agent replay of recorded current-source evidence only; no historical, negative-label or prospective certification.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run', type=Path)
    parser.add_argument('--repository', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', type=Path)
    arguments = parser.parse_args()
    report = replay(arguments.run, arguments.repository)
    if arguments.output:
        with arguments.output.open('x') as handle:
            json.dump(report, handle, indent=2, sort_keys=True, allow_nan=False)
            handle.write('\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'cases'}, sort_keys=True))
