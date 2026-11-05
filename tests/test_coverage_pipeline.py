import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from engine.store import Store, digest
from engine import sampling, coverage_pipeline as coverage


class CoverageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = Store(Path(self.tmp.name)/'engine.sqlite')
        coverage.initialize(self.store)

    def tearDown(self):
        self.store.close()
        self.tmp.cleanup()

    def inventory(self, count=10074):
        ids = [f'114-hr{i}' for i in range(1,count+1)] + ['116-s1']
        inv = dict(id='inventory', hash=digest(ids), bill_ids=ids+ids[:1], congresses=[114,116],
                   total=len(ids), discovered_at='2026-01-01T00:00:00Z', status='directory_complete',
                   strata=[dict(congress=c,type=k,source_url='https://www.govinfo.gov/bulkdata/BILLSTATUS/',
                                raw_hash='fixture',retrieved_at='2026-01-01T00:00:00Z') for c,k in [(114,'hr'),(116,'s')]])
        with self.store.db:
            self.store.db.execute('INSERT INTO sample_inventories VALUES (?,?)',(inv['id'],json.dumps(inv)))
        return inv

    def plan(self,count=3,batch=2):
        self.inventory(count)
        return coverage.plan_import(self.store,dict(inventory_id='inventory',congresses=[114],batch_size=batch))

    def complete(self,job,fail=False):
        with patch('engine.sampling.ingest_bill',side_effect=RuntimeError('no') if fail else None,
                   return_value={'status':'imported'}):
            return sampling.run_bulk_job(self.store.path,job['id'])

    def test_exact_complete_population_dedup_bounded_and_idempotent(self):
        inv=self.inventory()
        plan=coverage.plan_import(self.store,dict(inventory_id=inv['id'],congresses=[114]))
        self.assertEqual(plan['total'],10074)
        self.assertEqual(len(plan['batches']),41)
        self.assertEqual([b for batch in plan['batches'] for b in batch['bill_ids']],plan['bill_ids'])
        self.assertNotIn('116-s1',plan['bill_ids'])
        self.assertEqual(coverage.plan_import(self.store,dict(inventory_id=inv['id'],congresses=[114]))['id'],plan['id'])
        with self.assertRaises(ValueError): coverage.plan_import(self.store,dict(inventory_id=inv['id'],congresses=[118]))

    def test_pause_resume_sequential_batches_without_overlap(self):
        plan=self.plan()
        first=coverage.advance(self.store,launch=False)
        self.assertIsNone(coverage.advance(self.store,launch=False))
        coverage.update_plan(self.store,plan['id'],{'action':'pause'})
        self.complete(first)
        self.assertIsNone(coverage.advance(self.store,launch=False))
        coverage.update_plan(self.store,plan['id'],{'action':'resume'})
        second=coverage.advance(self.store,launch=False)
        self.assertFalse(set(first['bill_ids']) & set(second['bill_ids']))
        self.complete(second)
        coverage.advance(self.store,launch=False)
        finished=coverage.get_plan(self.store,plan['id'])
        self.assertEqual(finished['status'],'completed')
        self.assertEqual(finished['progress']['imported'],3)

    def test_restart_recovers_same_linked_batch(self):
        plan=self.plan()
        first=coverage.advance(self.store,launch=False)
        sampling.recover_bulk_jobs(self.store)
        resumed=coverage.advance(self.store,launch=False)
        self.assertEqual(first['id'],resumed['id'])
        self.assertEqual(len(coverage.get_plan(self.store,plan['id'])['jobs']),1)
        self.complete(resumed)
        self.assertNotEqual(coverage.advance(self.store,launch=False)['id'],first['id'])

    def test_errors_block_until_explicit_retry(self):
        plan=self.plan()
        first=coverage.advance(self.store,launch=False)
        self.complete(first,fail=True)
        self.assertIsNone(coverage.advance(self.store,launch=False))
        self.assertEqual(coverage.get_plan(self.store,plan['id'])['status'],'blocked')
        coverage.update_plan(self.store,plan['id'],{'action':'resume'})
        retry=coverage.advance(self.store,launch=False)
        self.assertEqual(retry['id'],first['id'])
        self.complete(retry)
        self.assertIsNotNone(coverage.advance(self.store,launch=False))

    def test_summary_unknown_not_zero_and_audit_dedup(self):
        self.plan()
        base=dict(dataset='official',bill_id='114-hr1',family_id='114-hr1',source_url='https://www.govinfo.gov',source_name='fixture',
                  effective_at='2015-01-05',observed_at='2026-01-01',introduced_at='2015-01-05',type='hr',congress=114,
                  title='Example',topic='Unclassified',family_status='unadjudicated singleton')
        self.store.add('bill',base)
        for i,status in enumerate(['passed','needs_correction']):
            audit=dict(id=str(i),bill_id='114-hr1',status=status)
            with self.store.db:
                self.store.db.execute('INSERT INTO sample_audits VALUES (?,?,?,?)',(str(i),'sample','114-hr1',json.dumps(audit)))
        result=coverage.summary(self.store)
        self.assertEqual(result['imported'],1)
        self.assertEqual(result['audited'],1)
        self.assertEqual(result['audit_passed'],0)
        self.assertEqual(result['historical_metadata_eligible'],0)
        for key in ['downloaded','historical_eligible','training_eligible','evaluation_ready']:
            self.assertIsNone(result[key])
        self.assertEqual(result['field_coverage']['title'],1)
        self.assertEqual(result['field_coverage']['topic'],0)
        self.assertEqual(result['outcomes_unknown'],1)
        self.assertEqual(result['field_coverage']['adjudicated_family'],0)


if __name__=='__main__':
    unittest.main()
