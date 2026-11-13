"""Contract tests; mocked transport is not a real-source certification."""
import copy
import io
import http.client
import json
import sqlite3
import subprocess
import sys
import tempfile
import threading
import unittest
import urllib.error
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import Mock, patch

from engine import forecast_ledger as fl


URL = 'https://www.govinfo.gov/bulkdata/BILLSTATUS/120/hr/BILLSTATUS-120hr1.xml'
XML = b'<billStatus><bill><congress>120</congress><type>HR</type><number>1</number></bill></billStatus>'
BEFORE = '2027-03-02T12:00:00.000000Z'
CUTOFF = '2027-03-03T00:00:00.000000Z'


class Response(io.BytesIO):
    def __init__(self, data=XML, status=200, url=URL, headers=None):
        super().__init__(data)
        self.status = status
        self.url = url
        self.headers = headers or {'Content-Type': 'application/xml', 'Content-Length': str(len(data))}

    def geturl(self):
        return self.url


class ForecastLedgerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.ledger = fl.Ledger(self.root)

    def tearDown(self):
        self.ledger.close()
        self.temp.cleanup()

    def capture(self, data=XML, at=BEFORE, **kwargs):
        response = Response(data, **kwargs)
        with patch.object(fl, 'now', return_value=at), patch.object(fl.urllib.request, 'build_opener', return_value=Mock(open=Mock(return_value=response))):
            return self.ledger.capture(URL, 'hr1-120')

    def pair_fixture(self):
        spec = dict(mode='local_forecast', protocol_sha256='a' * 64, target=fl.TARGET,
                    checkpoint_days=30, horizon_days=90, issuance_tolerance_seconds=60,
                    models={'challenger': {'weights': [0.2, 0.3]}, 'stage_reference': {'rates': {'0': 0.1}}})
        with patch.object(fl, 'now', return_value=BEFORE):
            registration = self.ledger.register(spec)
        source = self.capture()
        case = dict(bill_id='hr1-120', congress=120, target=fl.TARGET,
                    introduced_at='2027-02-01T00:00:00Z', cutoff=CUTOFF,
                    horizon='2027-06-01T00:00:00Z', at_risk=True,
                    risk_check='Synthetic complete history reviewed through cutoff',
                    family_id='synthetic-1', features={'stage': 0, 'chamber': 'hr'},
                    features_effective_at=BEFORE, features_available_at=BEFORE, source_ids=[source['id']])
        predictions = {name: dict(bill_id=case['bill_id'], target=case['target'], cutoff=case['cutoff'],
                                 feature_hash=fl.fingerprint(case['features']), artifact_hash=fl.fingerprint(artifact),
                                 probability=0.2) for name, artifact in spec['models'].items()}
        return registration, case, predictions

    def issue(self, registration, case, predictions, at=CUTOFF, **kwargs):
        with patch.object(fl, 'now', return_value=at):
            return self.ledger.issue_pair(registration['id'], case, predictions, **kwargs)

    def test_capture_retains_exact_bytes_and_untrusted_observation(self):
        receipt = self.capture()
        body = receipt['body']
        self.assertEqual((self.root / body['raw_path']).read_bytes(), XML)
        self.assertEqual(body['disposition'], 'complete')
        self.assertTrue(body['identity_valid'])
        self.assertEqual(body['attestation'], 'local_observation_only')
        self.assertFalse(body['certified'])
        self.assertEqual(self.ledger.verify()['sources'], 1)

    def test_identity_mismatch_and_malformed_xml_retained(self):
        for data in (XML.replace(b'<number>1', b'<number>2'), b'not xml'):
            receipt = self.capture(data)
            self.assertEqual(receipt['body']['disposition'], 'identity_or_parse_failure')
            self.assertFalse(receipt['body']['identity_valid'])
            self.assertEqual((self.root / receipt['body']['raw_path']).read_bytes(), data)

    def test_ambiguous_identity_root_cardinality_and_entities_rejected(self):
        bad = [XML.replace(b'</number>', b'</number><number>2</number>'),
               XML.replace(b'</billStatus>', b'<bill><number>2</number></bill></billStatus>'),
               XML.replace(b'</bill>', b'<billType>S</billType><billNumber>2</billNumber></bill>'),
               XML.replace(b'<billStatus>', b'<other>').replace(b'</billStatus>', b'</other>'),
               b'<!DOCTYPE billStatus [<!ENTITY x "1">]>' + XML.replace(b'<number>1', b'<number>&x;'),
               XML.replace(b'<number>1</number>', b'<number><value>1</value></number>')]
        for data in bad:
            with self.subTest(data=data):
                receipt = self.capture(data)
                self.assertEqual(receipt['body']['disposition'], 'identity_or_parse_failure')
                self.assertFalse(receipt['body']['identity_valid'])

    def test_namespaced_valid_identity_control(self):
        receipt = self.capture(XML.replace(b'<billStatus>', b'<billStatus xmlns="https://example.test/bill-status">'))
        self.assertEqual(receipt['body']['disposition'], 'complete')

    def test_reject_url_before_request_or_receipt(self):
        for url in ('http://www.govinfo.gov/test', URL + '?api_key=secret', URL + '#x',
                    URL.replace('govinfo.gov', 'govinfo.gov.evil'), URL.replace('120hr1', '120hr2'),
                    URL.replace('https://', 'https://user:secret@')):
            with self.subTest(url=url), self.assertRaises(ValueError):
                self.ledger.capture(url, 'hr1-120')
        self.assertEqual(self.ledger.verify()['receipts'], 0)

    def test_inventory_requires_exact_directory_and_html(self):
        url = 'https://www.govinfo.gov/bulkdata/BILLSTATUS/118/hr'
        response = Response(b'<html>directory</html>', url=url, headers={'Content-Type': 'text/html'})
        with patch.object(fl.urllib.request, 'build_opener', return_value=Mock(open=Mock(return_value=response))):
            receipt = self.ledger.capture(url, source_kind='inventory')
        self.assertEqual(receipt['body']['disposition'], 'complete')
        with self.assertRaises(ValueError):
            self.ledger.capture(url, bill_id='hr1-118', source_kind='inventory')

    def test_timeout_and_http_error_are_receipts(self):
        with patch.object(fl.urllib.request, 'build_opener', return_value=Mock(open=Mock(side_effect=TimeoutError('secret remote diagnostic')))):
            failed = self.ledger.capture(URL, 'hr1-120')
        self.assertEqual(failed['body']['error'], 'TimeoutError')
        self.assertNotIn('secret', json.dumps(failed))
        self.assertEqual(failed['body']['byte_count'], 0)
        response = Response(b'unavailable', status=503)
        with patch.object(fl.urllib.request, 'build_opener', return_value=Mock(open=Mock(return_value=response))):
            failed = self.ledger.capture(URL, 'hr1-120')
        self.assertEqual(failed['body']['disposition'], 'http_error')
        self.assertEqual(failed['body']['http_status'], 503)
        self.assertEqual(self.ledger.verify()['sources'], 2)

    def test_partial_response_survives_read_failure(self):
        response = Response()
        response.read = Mock(side_effect=[b'<bill', TimeoutError()])
        with patch.object(fl.urllib.request, 'build_opener', return_value=Mock(open=Mock(return_value=response))):
            failed = self.ledger.capture(URL, 'hr1-120')
        self.assertEqual(failed['body']['disposition'], 'request_failed')
        self.assertEqual((self.root / failed['body']['raw_path']).read_bytes(), b'<bill')
        response = Response()
        response.read = Mock(side_effect=http.client.IncompleteRead(b'partial'))
        with patch.object(fl.urllib.request, 'build_opener', return_value=Mock(open=Mock(return_value=response))):
            failed = self.ledger.capture(URL, 'hr1-120')
        self.assertEqual(failed['body']['disposition'], 'incomplete')
        self.assertEqual((self.root / failed['body']['raw_path']).read_bytes(), b'partial')

    def test_oversize_and_length_mismatch_are_not_complete(self):
        response = Response(XML)
        with patch.object(fl.urllib.request, 'build_opener', return_value=Mock(open=Mock(return_value=response))):
            oversized = self.ledger.capture(URL, 'hr1-120', max_bytes=10)
        self.assertEqual(oversized['body']['disposition'], 'oversize')
        self.assertEqual(oversized['body']['byte_count'], 11)
        mismatch = self.capture(headers={'Content-Length': '99999'})
        self.assertEqual(mismatch['body']['disposition'], 'incomplete')

    def test_redirect_is_disabled(self):
        self.assertIsNone(fl._NoRedirect().redirect_request(None, None, 302, '', {}, 'https://evil.test'))

    def test_tampered_or_missing_bytes_reject_read_verify_and_append(self):
        receipt = self.capture()
        raw = self.root / receipt['body']['raw_path']
        raw.write_bytes(b'changed')
        for call in (lambda: self.ledger.read(receipt['id']), self.ledger.verify,
                     lambda: self.ledger.register(dict(mode='collection', protocol_sha256='a' * 64))):
            with self.assertRaisesRegex(ValueError, 'digest/size'):
                call()
        raw.unlink()
        with self.assertRaisesRegex(ValueError, 'Missing raw'):
            self.ledger.verify()

    def test_existing_content_addressed_object_cannot_be_overwritten(self):
        path = self.root / 'objects' / fl.sha256(XML)
        path.write_bytes(b'wrong')
        with self.assertRaisesRegex(ValueError, 'differs'):
            self.capture()
        self.assertEqual(path.read_bytes(), b'wrong')
        self.assertEqual(len(self.ledger.verify()['pending_captures']), 1)

    def test_interrupted_persistence_leaves_detectable_pending_attempt(self):
        with patch.object(self.ledger, '_retain', side_effect=OSError('disk full')):
            with self.assertRaises(OSError):
                self.capture()
        result = self.ledger.verify()
        self.assertEqual(result['receipts'], 1)
        self.assertEqual(len(result['pending_captures']), 1)
        self.assertEqual(result['sources'], 0)

    def test_atomic_object_write_never_exposes_partial_bytes(self):
        with patch.object(fl.os, 'link', side_effect=OSError('interrupted')):
            with self.assertRaises(OSError):
                self.ledger._retain(XML)
        self.assertEqual(list((self.root / 'objects').iterdir()), [])

    def test_database_update_and_delete_are_rejected(self):
        self.capture()
        for sql in ('UPDATE receipts SET body=body', 'DELETE FROM receipts'):
            with self.assertRaises(sqlite3.IntegrityError):
                self.ledger.db.execute(sql)

    def test_clock_rollback_leaves_pending_capture(self):
        with patch.object(fl, 'now', side_effect=[BEFORE, '2027-03-01T00:00:00Z']), patch.object(fl.urllib.request, 'build_opener', return_value=Mock(open=Mock(return_value=Response()))):
            with self.assertRaisesRegex(ValueError, 'rollback'):
                self.ledger.capture(URL, 'hr1-120')
        self.assertEqual(len(self.ledger.verify()['pending_captures']), 1)

    def test_positive_pair_control_and_duplicate(self):
        registration, case, predictions = self.pair_fixture()
        receipt = self.issue(registration, case, predictions)
        self.assertEqual(receipt['kind'], 'forecast_pair')
        self.assertFalse(receipt['body']['certified'])
        self.assertFalse(receipt['body']['release_eligible'])
        self.assertEqual(self.ledger.verify()['forecast_pairs'], 1)
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            self.issue(registration, case, predictions)

    def test_equivalent_timestamp_spelling_cannot_duplicate_pair(self):
        registration, case, predictions = self.pair_fixture()
        self.issue(registration, case, predictions)
        case['cutoff'] = '2027-03-03T00:00:00+00:00'
        for prediction in predictions.values():
            prediction['cutoff'] = case['cutoff']
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            self.issue(registration, case, predictions)

    def test_capture_can_bind_collection_registration(self):
        registration = self.ledger.register(dict(mode='collection', protocol_sha256='a' * 64))
        with patch.object(fl.urllib.request, 'build_opener', return_value=Mock(open=Mock(return_value=Response()))):
            receipt = self.ledger.capture(URL, 'hr1-120', registration_id=registration['id'])
        self.assertEqual(receipt['body']['registration_id'], registration['id'])
        self.assertEqual(self.ledger.verify()['sources'], 1)
        with self.assertRaisesRegex(ValueError, 'Unknown collection'):
            self.ledger.capture(URL, 'hr1-120', registration_id='unregistered')

    def test_certified_issuance_cannot_be_asserted(self):
        registration, case, predictions = self.pair_fixture()
        with self.assertRaisesRegex(ValueError, 'independently verified timestamp'):
            self.issue(registration, case, predictions, certified=True)

    def test_early_late_and_microsecond_late_issuance_rejected(self):
        registration, case, predictions = self.pair_fixture()
        for at in ('2027-03-02T23:59:59.999999Z', '2027-03-03T00:01:00.000001Z'):
            with self.subTest(at=at), self.assertRaisesRegex(ValueError, 'Early or late'):
                self.issue(registration, case, predictions, at=at)

    def test_case_guards_and_unresolved_risk(self):
        registration, case, predictions = self.pair_fixture()
        changes = [dict(at_risk=False), dict(at_risk=None), dict(risk_check=''), dict(source_ids=[]),
                   dict(source_ids=[case['source_ids'][0]] * 2), dict(family_id=''),
                   dict(features_available_at='2027-03-03T00:00:00.000001Z'),
                   dict(features_effective_at='2027-03-03T00:00:00.000001Z'),
                   dict(features_available_at='2027-03-01T00:00:00Z'),
                   dict(horizon='2027-06-02T00:00:00Z'), dict(target='enactment'), dict(congress=119)]
        for change in changes:
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.issue(registration, dict(case, **change), predictions)
        self.assertEqual(self.ledger.verify()['forecast_pairs'], 0)

    def test_source_observed_one_microsecond_after_cutoff_is_rejected(self):
        registration, case, predictions = self.pair_fixture()
        later = self.capture(at='2027-03-03T00:00:00.000001Z')
        case['source_ids'] = [later['id']]
        case['features_available_at'] = CUTOFF
        with self.assertRaisesRegex(ValueError, 'predates observed bytes'):
            self.issue(registration, case, predictions, at='2027-03-03T00:00:01Z')

    def test_bad_pairing_and_nonfinite_probabilities(self):
        registration, case, predictions = self.pair_fixture()
        for field, value in [('probability', float('nan')), ('probability', float('inf')),
                             ('probability', -0.01), ('probability', 1.01), ('probability', True),
                             ('artifact_hash', 'bad'), ('feature_hash', 'bad'), ('bill_id', 'hr2-120'),
                             ('target', 'enactment'), ('cutoff', '2027-03-04T00:00:00Z')]:
            changed = copy.deepcopy(predictions)
            changed['challenger'][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                self.issue(registration, case, changed)
        with self.assertRaisesRegex(ValueError, 'Missing or extra'):
            self.issue(registration, case, {'challenger': predictions['challenger']})

    def test_two_process_connections_cannot_double_issue(self):
        registration, case, predictions = self.pair_fixture()
        gate = threading.Barrier(2)

        def worker():
            with fl.Ledger(self.root) as ledger:
                gate.wait()
                try:
                    ledger.issue_pair(registration['id'], case, predictions)
                    return 'issued'
                except ValueError as exc:
                    return str(exc)

        with patch.object(fl, 'now', return_value=CUTOFF), ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda _: worker(), range(2)))
        self.assertEqual(sorted(results), ['Duplicate forecast pair', 'issued'])
        self.assertEqual(self.ledger.verify()['forecast_pairs'], 1)

    def test_registration_and_source_clock_precision_and_naive_times(self):
        self.assertLess(fl.instant('2027-03-03T00:00:00.000000Z'), fl.instant('2027-03-03T00:00:00.000001Z'))
        for value in ('2027-03-03', '2027-03-03T00:00:00'):
            with self.assertRaises(ValueError):
                fl.instant(value)

    def test_unknown_ledger_verify_does_not_create_empty_success(self):
        with self.assertRaisesRegex(ValueError, 'does not exist'):
            fl.Ledger(self.root / 'absent', create=False)

    def test_cli_registration_and_verification_across_processes(self):
        spec = self.root / 'plan.json'
        spec.write_text(json.dumps(dict(mode='collection', protocol_sha256='a' * 64)))
        root = self.root / 'cli-ledger'
        cwd = Path(__file__).resolve().parents[1]
        command = [sys.executable, '-m', 'engine.forecast_ledger']
        registered = subprocess.run(command + ['register', str(root), str(spec)], cwd=cwd,
                                    text=True, capture_output=True, check=True)
        self.assertEqual(json.loads(registered.stdout)['kind'], 'registration')
        checked = subprocess.run(command + ['verify', str(root)], cwd=cwd,
                                 text=True, capture_output=True, check=True)
        self.assertEqual(json.loads(checked.stdout)['receipts'], 1)
        absent = subprocess.run(command + ['verify', str(root / 'missing')], cwd=cwd,
                                text=True, capture_output=True)
        self.assertNotEqual(absent.returncode, 0)


if __name__ == '__main__':
    unittest.main()
