"""Fixed, source-only passage feasibility pilot; no labels, fits or forecasts."""
import argparse
from collections import Counter
from datetime import date, timedelta
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from engine.forecast_ledger import Ledger
from scripts import bicam_official_inventory_offline_v2 as inventory
from scripts import official_billstatus_readiness_v1 as metadata

VERSION = 'passage90-source-pilot-v1'
CONGRESS = 118
PER_CHAMBER = 10


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    raw = json.dumps(value, sort_keys=True, indent=2, allow_nan=False).encode() + b'\n'
    with path.open('xb') as out:
        out.write(raw)
    return sha(raw)


def select(ids, chamber):
    if len(ids) < PER_CHAMBER or len(set(ids)) != len(ids):
        raise ValueError('Insufficient or duplicate inventory identities')
    if any(not re.fullmatch(chamber + r'[1-9][0-9]*-118', bid) for bid in ids):
        raise ValueError('Inventory identity outside frozen scope')
    return sorted(ids, key=lambda bid: sha((VERSION + '\n' + bid).encode()))[:PER_CHAMBER]


def inspect(raw, case):
    """Describe exact current-record passage evidence; never certify a label."""
    parsed = metadata.inspect_xml(raw, case)
    if not parsed['identity_valid'] or not parsed['introduction_in_calendar_congress']:
        raise ValueError('Source identity/introduction validation failed: ' + str(parsed['errors']))
    introduced = date.fromisoformat(parsed['introduced_at'])
    checkpoint = introduced + timedelta(days=30)
    horizon = checkpoint + timedelta(days=90)
    root = ET.fromstring(raw)
    bill = root.find('bill')
    kind = case['bill_type']
    code, chamber = ('8000', 'House') if kind == 'hr' else ('17000', 'Senate')
    matched, ambiguous = [], []
    actions = bill.findall('actions/item')
    for position, action in enumerate(actions):
        codes = action.findall('actionCode')
        if not any((node.text or '').strip() == code for node in codes):
            continue
        fields = {name: action.findall(path) for name, path in
                  [('code', 'actionCode'), ('source', 'sourceSystem/code'),
                   ('date', 'actionDate'), ('text', 'text')]}
        if any(len(nodes) != 1 or len(nodes[0]) for nodes in fields.values()):
            ambiguous.append(dict(position=position, reason='ambiguous_action_fields'))
            continue
        values = {name: (nodes[0].text or '').strip() for name, nodes in fields.items()}
        if values['source'] != '9' or not values['text'].startswith('Passed/agreed to in ' + chamber + ':'):
            ambiguous.append(dict(position=position, reason='uncorroborated_passage_code'))
            continue
        if not metadata.date_check(values['date']):
            ambiguous.append(dict(position=position, reason='invalid_passage_date'))
            continue
        when = date.fromisoformat(values['date'])
        if not introduced <= when < date(2025, 1, 3):
            ambiguous.append(dict(position=position, reason='passage_outside_bill_lifetime'))
            continue
        matched.append(dict(position=position, date=when.isoformat(), code=code,
                            source='9', text=values['text']))
    matched.sort(key=lambda row: (row['date'], row['position']))
    first = date.fromisoformat(matched[0]['date']) if matched else None
    # Date-only boundary cases remain ambiguous, even if a different action fits.
    if horizon >= date(2025, 1, 3):
        disposition = 'excluded_incomplete_congress_window'
    elif ambiguous:
        disposition = 'unresolved_action_semantics'
    elif first in (checkpoint, horizon):
        disposition = 'unresolved_boundary_day'
    elif first and first < checkpoint:
        disposition = 'excluded_already_passed'
    elif first and checkpoint < first < horizon:
        disposition = 'candidate_within_window_passage'
    elif first:
        disposition = 'later_passage_negative_coverage_unverified'
    else:
        disposition = 'unresolved_no_recognized_passage'
    return dict(bill_id=case['bill_id'], introduced_at=introduced.isoformat(),
                checkpoint_date=checkpoint.isoformat(), horizon_date=horizon.isoformat(),
                full_window=horizon < date(2025, 1, 3), disposition=disposition,
                recognized_passage_actions=matched, ambiguous_actions=ambiguous,
                action_count=len(actions), certified_label=None,
                historical_feature_eligibility=False)


def run(output):
    output.mkdir(parents=True, exist_ok=False)
    paths = [Path(__file__), Path('engine/forecast_ledger.py'), Path(metadata.__file__),
             Path(inventory.__file__), Path(inventory.v1.__file__),
             Path('tests/test_passage90_source_pilot.py'),
             Path('docs/research/FORECASTING_FIRST_PLAN_V1.md')]
    bindings = {str(path): sha(path.read_bytes()) for path in paths}
    spec = dict(version=VERSION, mode='collection', congress=CONGRESS,
                protocol_sha256=bindings[str(paths[-1])], bindings=bindings,
                per_chamber=PER_CHAMBER, max_requests=22, retries=0, redirects=0,
                inventory_byte_cap=5_000_000, bill_byte_cap=2_000_000, timeout_seconds=20,
                selection='First ten per chamber by SHA256(version + newline + bill_id)',
                scope='Current-source feasibility only; no negative labels or historical certification',
                model_fits=0, forecasts=0)
    registration_hash = save(output / 'registration.json', spec)
    def check_bindings():
        if any(sha(Path(path).read_bytes()) != digest for path, digest in bindings.items()):
            save(output / 'blocked.json', dict(reason='registered_code_or_protocol_changed'))
            raise ValueError('Registered code/protocol changed during acquisition')
    with Ledger(output / 'ledger') as ledger:
        registration = ledger.register(spec)
        inventories, sample, rows = [], [], []
        for chamber in ('hr', 's'):
            check_bindings()
            url = f'https://www.govinfo.gov/bulkdata/BILLSTATUS/{CONGRESS}/{chamber}'
            receipt = ledger.capture(url, source_kind='inventory', max_bytes=5_000_000, timeout=20,
                                     registration_id=registration['id'])
            body = receipt['body']
            if body['disposition'] != 'complete':
                save(output / 'blocked.json', dict(reason='inventory_capture_failed', receipt=receipt))
                return dict(status='blocked', reason='inventory_capture_failed', output=str(output))
            raw = (ledger.root / body['raw_path']).read_bytes()
            try:
                parsed = inventory.parse(raw, CONGRESS, chamber, url)
                selected = select(parsed['ids'], chamber) if parsed['accepted_index'] else []
            except (ValueError, UnicodeError) as exc:
                save(output / 'blocked.json', dict(reason='inventory_parse_or_selection_failed',
                                                   receipt_id=receipt['id'], error=str(exc)))
                return dict(status='blocked', reason='inventory_parse_or_selection_failed', output=str(output))
            inventories.append(dict(receipt_id=receipt['id'], byte_count=body['byte_count'], parsed=parsed))
            if not parsed['accepted_index']:
                save(output / 'blocked.json', dict(reason='inventory_parse_failed', inventories=inventories))
                return dict(status='blocked', reason='inventory_parse_failed', output=str(output))
            for bid in selected:
                number = int(re.fullmatch(r'(?:hr|s)([1-9][0-9]*)-118', bid)[1])
                sample.append(dict(bill_id=bid, congress=CONGRESS, bill_type=chamber,
                                   bill_number=number,
                                   url=url + f'/BILLSTATUS-{CONGRESS}{chamber}{number}.xml'))
        # The sample is sealed before any bill body is requested, without outcome filtering.
        save(output / 'sample.json', dict(inventories=inventories, sample=sample,
                                          registration_id=registration['id']))
        for case in sample:
            check_bindings()
            receipt = ledger.capture(case['url'], bill_id=case['bill_id'], timeout=20,
                                     registration_id=registration['id'])
            row = dict(case=case, receipt_id=receipt['id'], capture=receipt['body'])
            if receipt['body']['disposition'] == 'complete':
                try:
                    raw = (ledger.root / receipt['body']['raw_path']).read_bytes()
                    row['inspection'] = inspect(raw, case)
                except (ValueError, ET.ParseError) as exc:
                    row['inspection_error'] = str(exc)
            rows.append(row)
        verification = ledger.verify()
        check_bindings()
        summary = dict(status='completed', version=VERSION, registration_sha256=registration_hash,
                       inventory_identities=sum(i['parsed']['unique_count'] for i in inventories),
                       selected=len(sample), requests=2 + len(rows),
                       captured=sum(r['capture']['disposition'] == 'complete' for r in rows),
                       inspected=sum('inspection' in r for r in rows),
                       dispositions=dict(Counter(r.get('inspection', {}).get('disposition', 'source_or_inspection_failure') for r in rows)),
                       full_windows=sum(r.get('inspection', {}).get('full_window', False) for r in rows),
                       bill_response_bytes=sum(r['capture'].get('byte_count', 0) for r in rows),
                       inventory_response_bytes=sum(i['byte_count'] for i in inventories),
                       response_bytes=sum(r['capture'].get('byte_count', 0) for r in rows) + sum(i['byte_count'] for i in inventories),
                       certified_positive_labels=0, certified_negative_labels=0,
                       historical_eligible=0, model_fits=0, forecasts=0, predictive_scores=0,
                       externally_attested=0, release_eligible=False)
        save(output / 'result.json', dict(summary=summary, rows=rows, verification=verification))
        return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.output), indent=2))
