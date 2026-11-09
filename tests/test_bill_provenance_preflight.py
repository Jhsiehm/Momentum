import hashlib
import json
import unittest
from pathlib import Path

from scripts.bill_provenance_preflight import (day180_cutoff, feature_eligibility,
    run_manifest, select_schedule_vintage, utc, validate_identity, verify_bytes)

FIXTURE = Path(__file__).parent / 'fixtures/bill_provenance_preflight_v1.json'


class ProvenancePreflightTests(unittest.TestCase):
    def test_registered_synthetic_cases(self):
        result = run_manifest(json.loads(FIXTURE.read_text()))
        for case in result['cases']:
            with self.subTest(case=case['id']):
                self.assertTrue(case['passed'], case)
        self.assertFalse(result['historical_source_certified'])
        self.assertFalse(result['predictive_test'])

    def test_bytes_binding(self):
        identity = dict(congress=117, type='hr', number=1, version='ih',
                        raw_sha256=hashlib.sha256(b'raw').hexdigest(),
                        view_sha256=hashlib.sha256(b'view').hexdigest())
        self.assertTrue(verify_bytes(identity, b'raw', b'view'))
        for raw, view in [(b'wrong', b'view'), (b'raw', b'wrong')]:
            with self.assertRaises(ValueError):
                verify_bytes(identity, raw, view)

    def test_invalid_identity(self):
        identity = json.loads(FIXTURE.read_text())['cases'][0]['args'][0]
        for key, val in [('congress', True), ('number', 0), ('type', 'HR'),
                         ('version', ''), ('view_sha256', 'a'*63)]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate_identity(dict(identity, **{key: val}), identity)

    def test_aware_only(self):
        for stamp in ['2021-06-30', '2021-06-30T00:00:00', 'bad', None]:
            with self.subTest(stamp=stamp), self.assertRaises(ValueError):
                utc(stamp)
        self.assertEqual(utc('2021-06-29T20:00:00-04:00'), utc('2021-06-30T00:00:00Z'))

    def test_known_cancellation(self):
        record = dict(kind='scheduled_event', event_id='h', known_at='2021-06-28T00:00:00Z',
                      source_available_at='2021-06-28T00:00:00Z', version_available_at='2021-06-28T00:00:00Z',
                      event_at='2021-07-01T00:00:00Z')
        cancellation = dict(record, kind='cancellation', known_at='2021-06-29T00:00:00Z',
                            event_at='2021-06-29T00:00:00Z')
        result = select_schedule_vintage([record, cancellation], '2021-06-30T00:00:00Z')
        self.assertEqual(result['status'], 'cancelled')
        with self.assertRaises(ValueError):
            select_schedule_vintage([record, dict(cancellation, event_id='other')], '2021-06-30T00:00:00Z')

    def test_no_silent_defaulting(self):
        with self.assertRaises(ValueError):
            feature_eligibility({}, '2021-06-30T00:00:00Z')
        with self.assertRaises(ValueError):
            select_schedule_vintage([], '2021-06-30T00:00:00Z')
        with self.assertRaises(ValueError):
            run_manifest({'synthetic_only': False, 'cases': []})
