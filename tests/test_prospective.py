import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from engine import prospective, fixtures
from engine.store import Store


class ProspectiveTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.store=Store(Path(self.temp.name)/'db')
    def tearDown(self):self.store.close();self.temp.cleanup()
    def bill(self,congress=119):
        bid=f'{congress}-hr1'
        self.store.add('bill',dict(bill_id=bid,family_id=bid,dataset='official',source_url='https://www.govinfo.gov/example',source_name='Test official source',effective_at='2025-01-10',observed_at='2025-01-10',congress=congress,type='hr',title='Test',introduced_at='2025-01-10'))
        return bid
    def test_live_snapshot_without_forecast_is_honest_and_deduplicates(self):
        bid=self.bill()
        with patch('engine.prospective.now',return_value='2026-10-26T12:00:00Z'):
            a=prospective.capture(self.store,'official',bid);b=prospective.capture(self.store,'official',bid)
        self.assertTrue(a['prospective_eligible']);self.assertEqual(a['status'],'unavailable');self.assertIn('20 resolved',a['reason'])
        self.assertEqual(a['id'],b['id']);self.assertTrue(b['reused']);self.assertIsNone(a['outcome_at_issue'])
        self.assertEqual(len(prospective.list_receipts(self.store,'official',bid)),1)
        self.assertTrue(all(r['available_at']<=a['issued_at'] for r in a['source_records']))
        with self.assertRaises(Exception):self.store.db.execute('DELETE FROM prospective_receipts')
    def test_ended_and_missing_are_not_prospective(self):
        bid=self.bill(118)
        with patch('engine.prospective.now',return_value='2026-10-26T12:00:00Z'):
            a=prospective.capture(self.store,'official',bid);b=prospective.capture(self.store,'official','119-hr999')
        self.assertEqual(a['status'],'ineligible');self.assertFalse(a['prospective_eligible']);self.assertFalse(b['prospective_eligible'])
    def test_future_source_not_in_capture_and_new_evidence_creates_receipt(self):
        bid=self.bill()
        event=dict(bill_id=bid,family_id=bid,dataset='official',source_url='https://www.govinfo.gov/example',source_name='Test',effective_at='2026-10-25',observed_at='2026-10-27',stage=1,text='Committee action')
        self.store.add('event',event)
        with patch('engine.prospective.now',return_value='2026-10-26T12:00:00Z'):a=prospective.capture(self.store,'official',bid)
        self.assertEqual(len(a['source_records']),1)
        with patch('engine.prospective.now',return_value='2026-10-28T12:00:00Z'):b=prospective.capture(self.store,'official',bid)
        self.assertNotEqual(a['id'],b['id']);self.assertEqual(len(b['source_records']),2)
    def test_available_forecast_saved_and_demo_cannot_claim_real_prospective(self):
        fixtures.seed(self.store)
        with patch('engine.prospective.now',return_value='2023-07-01T12:00:00Z'),patch('engine.model.now',return_value='2023-07-01T12:00:00Z'):
            a=prospective.capture(self.store,'demo','demo-118-s100');b=prospective.capture(self.store,'demo','demo-118-s100')
        self.assertEqual(a['status'],'captured');self.assertFalse(a['prospective_eligible']);self.assertTrue(a['synthetic']);self.assertTrue(b['reused'])
        self.assertEqual(self.store.db.execute('SELECT count(*) FROM forecasts').fetchone()[0],1)
        self.assertTrue(a['forecast_hash']);self.assertTrue(a['forecast']['training_manifest'])
    def test_validation(self):
        for dataset,bid in [('bad','119-hr1'),('official',None)]:
            with self.assertRaises(ValueError):prospective.capture(self.store,dataset,bid)
        with self.assertRaises(ValueError):prospective.list_receipts(self.store,limit=True)
