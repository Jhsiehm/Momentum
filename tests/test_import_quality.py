import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from engine.import_quality import audit, historical_quality
from engine.store import Store


class ImportQualityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.raw = self.root/'raw'
        self.raw.mkdir()
        payload = b'retained official source fixture'
        self.sha = hashlib.sha256(payload).hexdigest()
        (self.raw/self.sha).write_bytes(payload)
        self.store = Store(self.root/'audit.sqlite')
        self.store.add('bill', dict(bill_id='114-hr1', dataset='official', family_id='114-hr1',
            source_url='https://www.govinfo.gov/example', source_name='fixture',
            effective_at='2015-01-06', observed_at='2026-10-26T00:00:00Z',
            congress=114, type='hr', title='Example', topic='Unclassified', sponsor='Someone',
            introduced_at='2015-01-06', raw_hash=self.sha, family_status='unadjudicated singleton',
            coverage='current bulk snapshot; historical availability unverified'))
        self.store.checkpoint('raw:114-hr1:'+self.sha,
            dict(hash=self.sha, retrieved_at='2026-10-26T00:00:00Z'))

    def tearDown(self):
        self.store.close()
        self.temp.cleanup()

    def test_integrity_does_not_certify_eligibility_or_negative_outcomes(self):
        before = self.store.db.total_changes
        result = audit(self.store.path, self.raw)
        self.assertEqual(result['integrity']['invalid_record_ids'], [])
        self.assertEqual(result['integrity']['missing_bulk_receipts'], [])
        self.assertEqual(result['integrity']['invalid_bulk_receipts'], [])
        self.assertEqual(result['official_population']['outcomes']['unresolved'], 1)
        self.assertEqual(result['official_population']['outcomes']['negative'], 0)
        self.assertEqual(result['official_population']['historically_verified_metadata'], 0)
        self.assertEqual(result['official_population']['missing_fields']['topic'], 1)
        self.assertEqual(self.store.db.total_changes, before)

    def test_corrupt_source_and_receipt_are_detected(self):
        (self.raw/self.sha).write_bytes(b'corrupt')
        self.store.checkpoint('raw:114-hr1:'+self.sha, dict(hash='wrong', retrieved_at='2026-10-26T00:00:00Z'))
        result = audit(self.store.path, self.raw)
        self.assertEqual(result['integrity']['corrupt_raw'], [self.sha])
        self.assertEqual(result['integrity']['invalid_bulk_receipts'], ['114-hr1'])

    def test_historical_breakdown_is_read_only_and_does_not_certify_positives(self):
        before = list(self.store.db.iterdump())
        result = audit(self.store.path, self.raw)
        quality = result['historical_quality']
        self.assertIsNone(quality['eligible_positive_families'])
        self.assertEqual(quality['by_congress'][0]['unresolved'], 1)
        self.assertEqual(quality['by_congress'][0]['metadata_available_by_checkpoint'], 0)
        self.assertEqual(list(self.store.db.iterdump()), before)


class HistoricalQualityTests(unittest.TestCase):
    def bill(self, bid='118-hr1', **extra):
        return ('id', 'bill', dict(bill_id=bid, congress=118, type='hr', family_id=bid,
            introduced_at='2023-01-03', effective_at='2023-01-03',
            observed_at='2026-11-05', **extra))

    def label(self, bid, date, value=1, family=None):
        return ('id', 'resolution', dict(bill_id=bid, family_id=family or bid,
            effective_at=date, value=value))

    def test_deadline_checkpoint_and_missing_labels_are_distinct(self):
        records = [self.bill(f'118-hr{i}') for i in range(1, 7)]
        records += [self.label('118-hr1', '2024-01-01'),
                    self.label('118-hr2', '2025-01-04'),
                    self.label('118-hr3', '2025-01-03'),
                    self.label('118-hr4', '2023-02-01'),
                    self.label('118-hr5', '2025-01-03', value=0)]
        counts = historical_quality(records)['by_congress'][0]
        self.assertEqual(counts['positive_before_deadline'], 2)
        self.assertEqual(counts['positive_after_checkpoint_before_deadline'], 1)
        self.assertEqual(counts['positive_after_deadline'], 1)
        self.assertEqual(counts['positive_endpoint_day_review'], 1)
        self.assertEqual(counts['recorded_negative'], 1)
        self.assertEqual(counts['unresolved'], 1)

    def test_conflicts_and_orphans_are_not_silently_resolved(self):
        records = [self.bill(), self.bill('118-hr2'),
            self.label('118-hr1', '2024-01-01'), self.label('118-hr1', '2025-01-03', 0, 'other'),
            self.label('118-hr2', '2024-01-01'), self.label('118-hr2', '2024-02-01'),
            self.label('118-hr3', '2024-01-01')]
        result = historical_quality(records)
        counts = result['by_congress'][0]
        self.assertEqual(counts['conflicting'], 1)
        self.assertEqual(counts['positive_date_conflict'], 1)
        self.assertEqual(counts['family_identity_conflicts'], 1)
        self.assertEqual(counts['positive_before_deadline'], 0)
        self.assertEqual(result['orphan_resolution_bill_ids'], ['118-hr3'])

    def test_all_metadata_versions_and_effective_time_are_checked(self):
        earlier = self.bill(verified_available_at='2023-02-01', archive_proof='fixture')
        current = self.bill()
        counts = historical_quality([earlier, current])['by_congress'][0]
        self.assertEqual(counts['metadata_available_by_checkpoint'], 1)
        future = self.bill(verified_available_at='2024-01-01', archive_proof='fixture')
        counts = historical_quality([future, current])['by_congress'][0]
        self.assertEqual(counts['metadata_available_by_checkpoint'], 0)
        earlier[2]['effective_at'] = '2024-01-01'
        counts = historical_quality([earlier, current])['by_congress'][0]
        self.assertEqual(counts['metadata_available_by_checkpoint'], 0)

    def test_invalid_metadata_and_age_fail_closed(self):
        row = self.bill()
        row[2]['introduced_at'] = 'invalid'
        self.assertEqual(historical_quality([row])['by_congress'][0]['invalid_checkpoint_metadata'], 1)
        for age in (-1, True, 1.5):
            with self.assertRaises(ValueError):
                historical_quality([], age)


if __name__ == '__main__':
    unittest.main()
