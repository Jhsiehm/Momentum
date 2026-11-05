import csv
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from engine.store import Store
from engine import sampling


def directory(c,k,n=20):
    rows=''.join(f'<tr data-name="BILLSTATUS-{c}{k}{i}.xml"><a href="/bulkdata/BILLSTATUS/{c}/{k}/BILLSTATUS-{c}{k}{i}.xml">file</a></tr>' for i in range(1,n+1))
    return ('<html><table>'+rows+'</table></html>').encode()

class SamplingTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.store=Store(Path(self.tmp.name)/'db.sqlite')
    def tearDown(self): self.store.close(); self.tmp.cleanup()
    def inventory(self):
        def fetched(url):
            c,k=url.rsplit('/',2)[-2:]; return directory(int(c),k)
        with patch('engine.sampling.fetch',side_effect=fetched),patch('engine.sampling.retain',return_value='fixture'):
            return sampling.discover_inventory(self.store,{})
    def sample(self):
        inv=self.inventory(); return sampling.create_sample(self.store,dict(inventory_id=inv['id'],size=30,audit_size=10,seed='fixed'))
    def test_directory_requires_full_matching_rows_and_rejects_pagination(self):
        self.assertEqual(sampling.parse_directory(directory(118,'hr',3),118,'hr'),['118-hr1','118-hr2','118-hr3'])
        for raw in [directory(118,'hr')[:-7],b'<html><table><a href="/bulkdata/BILLSTATUS/118/hr/BILLSTATUS-118hr1.xml"></a></table></html>',directory(118,'hr').replace(b'</table>',b'<a href="?page=2">next</a></table>')]:
            with self.assertRaises(ValueError): sampling.parse_directory(raw,118,'hr')
    def test_frozen_seeded_sample_and_chronological_evaluation_collection(self):
        inv=self.inventory(); args=dict(inventory_id=inv['id'],size=30,audit_size=10,seed='fixed')
        a=sampling.create_sample(self.store,args); b=sampling.create_sample(self.store,args)
        self.assertEqual(a['bill_ids'],b['bill_ids']); self.assertEqual(a['audit_bill_ids'],b['audit_bill_ids'])
        self.assertEqual(len(a['bill_ids']),30); self.assertEqual(len(set(a['bill_ids'])),30)
        test=sampling.collections.get_collection(self.store,a['evaluation_collection_id'])
        self.assertTrue(all(bid.startswith('118-') for bid in test['bill_ids']))
        self.assertEqual(a['readiness']['audited'],0)
        with self.assertRaises(Exception): self.store.db.execute("UPDATE research_samples SET body='{}'")
    def test_cache_prevents_repeat_discovery_and_bounds_validation(self):
        self.inventory()
        with patch('engine.sampling.fetch') as fetch:
            sampling.discover_inventory(self.store,{})
            fetch.assert_not_called()
        for args in [{'congresses':[999]},{'congresses':[True]}]:
            with self.assertRaises(ValueError): sampling.discover_inventory(self.store,args)
    def test_human_audit_append_only_and_csv_formula_safety(self):
        sample=self.sample(); bid=sample['audit_bill_ids'][0]
        args=dict(sample_id=sample['id'],bill_id=bid,status='passed',checks={k:True for k in ('identity','source','availability','family','outcome')},notes='=danger()')
        checked=sampling.save_audit(self.store,args)
        self.assertEqual(checked['readiness']['audit_passed'],1)
        self.assertIsNone(checked['readiness']['historical_eligible'])
        rows=list(csv.DictReader(io.StringIO(sampling.export_audit_csv(self.store,sample['id']))))
        self.assertEqual(rows[0]['review_notes'],"'=danger()")
        args['checks']['availability']=False
        with self.assertRaises(ValueError): sampling.save_audit(self.store,args)
        args['status']='needs_correction'; sampling.save_audit(self.store,args)
        with self.assertRaises(Exception): self.store.db.execute('DELETE FROM sample_audits')
        self.store.db.rollback()
        self.assertEqual(self.store.db.execute('SELECT COUNT(*) FROM sample_audits').fetchone()[0],2)
    def test_bulk_restart_and_retry_preserve_success_without_duplicate_download(self):
        job=sampling.start_bulk_job(self.store,{'bill_ids':['118-hr1','118-s2']},launch=False)
        with patch('engine.sampling.ingest_bill',side_effect=[{'status':'imported'},RuntimeError('secret')]):
            done=sampling.run_bulk_job(self.store.path,job['id'])
        self.assertEqual(done['parsed'],1); self.assertEqual(done['failed'],1); self.assertNotIn('secret',str(done))
        retry=sampling.retry_bulk_job(self.store,job['id'],launch=False)
        self.assertEqual(retry['completed'],1)
        sampling.recover_bulk_jobs(self.store)
        self.assertEqual(sampling.get_bulk_job(self.store,job['id'])['status'],'interrupted')
        sampling.retry_bulk_job(self.store,job['id'],launch=False)
        with patch('engine.sampling.ingest_bill',return_value={'status':'imported'}) as ingest:
            done=sampling.run_bulk_job(self.store.path,job['id']); self.assertEqual(ingest.call_count,1)
        self.assertEqual(done['status'],'completed'); self.assertEqual(done['parsed'],2)
        self.assertEqual(len(done['previous_attempts']),2)
        with self.assertRaises(ValueError): sampling.retry_bulk_job(self.store,job['id'],launch=False)
    def test_large_sample_batched_and_not_silently_restricted_to_first_eval_batch(self):
        def fetched(url):
            c,k=url.rsplit('/',2)[-2:]; return directory(int(c),k,200)
        with patch('engine.sampling.fetch',side_effect=fetched),patch('engine.sampling.retain',return_value='fixture'):
            inv=sampling.discover_inventory(self.store,{})
        sample=sampling.create_sample(self.store,dict(inventory_id=inv['id'],size=600,audit_size=25))
        self.assertEqual(len(sample['collection_ids']),6)
        self.assertIsNone(sample['evaluation_collection_id'])
        self.assertEqual(len(sample['evaluation_collection_ids']),2)
