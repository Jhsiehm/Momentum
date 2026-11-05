import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from engine.import_quality import audit
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


if __name__ == '__main__':
    unittest.main()
