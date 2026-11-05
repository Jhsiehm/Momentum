import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from engine.store import Store
from engine import collections


class CollectionTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.store=Store(Path(self.tmp.name)/'test.sqlite')
    def tearDown(self):
        self.store.close(); self.tmp.cleanup()
    def create(self):
        return collections.save_collection(self.store,{'name':'Energy','dataset':'official','bill_ids':['119-HR22','119-hr22','118-s50']})
    def test_versions_freeze_membership_and_reject_lost_update(self):
        a=self.create()
        self.assertEqual(len(a['bill_ids']),2)
        b=collections.save_collection(self.store,dict(a,expected_version=1,bill_ids=['119-hr22']))
        self.assertEqual(b['version'],2)
        self.assertEqual(collections.get_collection(self.store,a['id'],1)['bill_ids'],a['bill_ids'])
        with self.assertRaises(ValueError):
            collections.save_collection(self.store,dict(a,expected_version=1))
        self.assertEqual(len(collections.list_collections(self.store)),1)
        self.assertEqual(b['coverage']['missing'],1)
    def test_identifiers_bounds_and_namespace(self):
        for ids in [['https://evil.test'],['119-hr0'],['92-s1'],['119-hr1']*101]:
            with self.assertRaises(ValueError):
                collections.save_collection(self.store,{'name':'Bad','bill_ids':ids})
        with self.assertRaises(ValueError):
            collections.save_collection(self.store,{'name':'Bad','dataset':'demo','bill_ids':['119-hr1']})
    def test_import_preserves_partial_failure_and_is_claimed_once(self):
        job=collections.start_import_job(self.store,{'bill_ids':['119-hr22','118-s50']},launch=False)
        with patch('engine.collections.ingest_bill',side_effect=[{'status':'imported'},RuntimeError('secret URL')]) as ingest:
            done=collections.run_import_job(self.store.path,job['id'])
            self.assertEqual(done['status'],'completed_with_errors')
            self.assertEqual(done['completed'],2)
            self.assertNotIn('secret',str(done))
            collections.run_import_job(self.store.path,job['id'])
            self.assertEqual(ingest.call_count,2)
    def test_active_bound_and_startup_recovery(self):
        for _ in range(2):
            collections.start_import_job(self.store,{'bill_ids':['119-hr22']},launch=False)
        with self.assertRaises(ValueError):
            collections.start_import_job(self.store,{'bill_ids':['119-hr22']},launch=False)
        collections.recover_import_jobs(self.store)
        self.assertTrue(all(j['status']=='interrupted' for j in collections.list_import_jobs(self.store)))
