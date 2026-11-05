import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from engine import rigor as r, workspace as w
from engine.store import Store
from engine.fixtures import seed
from engine.model import forecast


class RigorTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.store=Store(Path(self.temp.name)/'test.sqlite')
        w.initialize(self.store);seed(self.store)

    def tearDown(self):
        self.store.close();self.temp.cleanup()

    def protocol(self, **extra):
        return r.register_protocol(self.store,dict(title='Structured baseline test',hypothesis='Structured signals improve over earlier base rates.',dataset='demo',congress=118,age_days=180,**extra))

    def test_document_retrieval_exact_heading_and_allowlist(self):
        index=r.read_document('plan')
        section=r.read_document('plan','4.6 AI contamination and three separate evaluation tracks')
        self.assertIn('pretraining',section['content'])
        self.assertEqual(index['hash'],section['hash'])
        with self.assertRaises(ValueError):r.read_document('../../.env')
        with self.assertRaises(ValueError):r.read_document('plan','invented section')

    def test_protocol_immutable_and_posthoc_registration_disclosed(self):
        first=self.protocol()
        self.assertEqual(first['status'],'registered_development')
        with self.assertRaises(sqlite3.IntegrityError):self.store.db.execute("UPDATE research_protocols SET body='{}'")
        self.store.db.rollback()
        w.execute_experiment(self.store,w.create_experiment(self.store,first['config']))
        second=self.protocol(supersedes=first['id'])
        self.assertIn('post hoc',second['registration_note'])
        self.assertTrue(second['prior_matching_runs'])
        self.assertNotEqual(first['id'],second['id'])

    def test_unsupported_design_recorded_but_cannot_execute(self):
        protocol=self.protocol(target='committee_passage_90d',candidate='D',track='final_holdout',feature_families=['macro'])
        self.assertEqual(protocol['status'],'blocked')
        self.assertEqual(len(protocol['unsupported']),4)
        result,_=w.execute_tool(self.store,'run_registered_protocol',{'protocol_id':protocol['id']})
        self.assertEqual(result['status'],'blocked')
        self.assertEqual(w.experiment_list(self.store),[])
        with self.assertRaises(ValueError):w.validate_experiment({'target':'survival'})
        with self.assertRaises(ValueError):w.validate_experiment({'calibration':'invented'})

    def test_changed_data_cannot_silently_run_registered_protocol(self):
        protocol=self.protocol()
        bill=self.store.bill('demo','demo-118-hr101')
        self.store.add('bill',dict(bill,title='Corrected title',observed_at='2026-10-01',verified_available_at='2026-10-01'))
        result,_=w.execute_tool(self.store,'run_registered_protocol',{'protocol_id':protocol['id']})
        self.assertEqual(result['status'],'blocked')
        self.assertIn('changed',result['blockers'][0])

    def test_registered_rerun_preserves_protocol_and_rejects_data_drift(self):
        protocol=self.protocol()
        first=w.create_experiment(self.store,protocol['config'],protocol_id=protocol['id'])
        rerun=w.create_experiment(self.store,first['config'],parent_id=first['id'])
        self.assertEqual(rerun['protocol_id'],protocol['id'])
        bill=self.store.bill('demo','demo-118-hr101')
        self.store.add('bill',dict(bill,title='New evidence',observed_at='2026-10-01',verified_available_at='2026-10-01'))
        with self.assertRaises(ValueError):w.create_experiment(self.store,first['config'],parent_id=first['id'])
        finished=w.execute_experiment(self.store,rerun)
        self.assertEqual(finished['status'],'failed')
        self.assertNotIn('metrics',finished)
        self.assertIn('changed during execution',finished['error'])

    def test_preflight_blocks_official_without_history(self):
        run=w.execute_experiment(self.store,w.create_experiment(self.store,{'dataset':'official','congress':119,'age_days':180}))
        self.assertEqual(run['status'],'blocked')
        self.assertIsNone(run['metrics'])
        self.assertFalse(run['preflight']['release_eligible'])

    def test_comparison_detects_replication_and_mismatched_design(self):
        a=w.execute_experiment(self.store,w.create_experiment(self.store,{'dataset':'demo','congress':118,'age_days':180}))
        b=w.execute_experiment(self.store,w.create_experiment(self.store,a['config'],a['id']))
        result=r.compare_runs(self.store,a['id'],b['id'])
        self.assertTrue(result['same_locked_forecasts']);self.assertEqual(result['brier_difference_right_minus_left'],0)
        self.assertEqual(result['pairs'],15)
        c=w.create_experiment(self.store,{'dataset':'demo','congress':117,'age_days':90})
        self.assertEqual(r.compare_runs(self.store,a['id'],c['id'])['status'],'not_comparable')

    def test_readiness_never_promotes_from_synthetic_scores(self):
        ready=r.readiness(self.store,'demo')
        self.assertFalse(ready['release_eligible'])
        self.assertEqual(ready['source_audit']['counts']['bills'],315)
        statuses={c['id']:c['status'] for c in ready['capabilities']}
        self.assertEqual(statuses['advanced'],'not_implemented')
        self.assertEqual(statuses['release'],'not_passed')

    def test_saved_forecast_audit_has_bounded_claim(self):
        f=forecast(self.store,'demo','demo-118-hr101','2023-07-01')
        report=r.audit_forecast(self.store,f['id'])
        self.assertEqual(report['status'],'checked_rules_pass')
        self.assertEqual(report['inputs_checked'],len(f['evidence_ids']))
        self.assertTrue(report['limitations'])

    def test_large_tool_outputs_remain_valid_json_with_disclosure(self):
        text=w.tool_payload({'content':'x'*100000,'document':'plan'})
        parsed=json.loads(text)
        self.assertEqual(parsed['status'],'output_truncated')
        self.assertLess(len(text),60000)
        self.assertIn('omitted',parsed['note'])

    def test_context_has_all_plan_areas_and_document_hashes(self):
        manifest=r.context_manifest(self.store,'demo')
        self.assertEqual(set(manifest['documents']),set(r.DOCUMENTS))
        self.assertEqual(len(manifest['capabilities']),15)
        self.assertTrue(manifest['rules'])

if __name__=='__main__':unittest.main()
