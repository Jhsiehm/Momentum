import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from engine import campaigns, sampling, autoresearch, workspace, sessions
from engine.store import Store


class CampaignTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.store=Store(Path(self.temp.name)/'db');workspace.initialize(self.store)
        def fetch(url):
            congress,kind=url.rsplit('/',2)[-2:]
            return ('<html><table>'+''.join(f'<tr data-name="BILLSTATUS-{congress}{kind}{i}.xml"><a href="/bulkdata/BILLSTATUS/{congress}/{kind}/BILLSTATUS-{congress}{kind}{i}.xml">x</a></tr>' for i in range(1,11))+'</table></html>').encode()
        with patch('engine.sampling.fetch',side_effect=fetch),patch('engine.sampling.retain',return_value='fixture'):
            inv=sampling.discover_inventory(self.store,{'congresses':[114,118]})
        self.sample=sampling.create_sample(self.store,dict(inventory_id=inv['id'],size=20,audit_size=5,seed='campaign-test'))
    def tearDown(self):self.store.close();self.temp.cleanup()
    def create(self,**kw):
        return campaigns.create(self.store,dict(name='Historical progress',goal='Test early legislative activity on frozen sampled bills.',sample_ids=[self.sample['id']],**kw))
    def test_persistence_no_silent_runner_changes(self):
        before=autoresearch.summary(self.store)['settings'];c=self.create(state='active')
        self.assertEqual(autoresearch.summary(self.store)['settings'],before)
        self.assertIn('Enable background',c['next_action']);self.assertTrue(c['blockers'])
        self.assertEqual(c['samples'][0]['imported_count'],0)
        updated=campaigns.update(self.store,c['id'],{'state':'paused','daily_run_limit':4})
        self.assertEqual(updated['version'],2);self.assertEqual(len(updated['events']),2)
        other=Store(self.store.path)
        try:self.assertEqual(campaigns.list_campaigns(other)[0]['state'],'paused')
        finally:other.close()
    def test_validation_membership_immutable(self):
        c=self.create()
        for args in ({'name':'x'},{'state':[]},{'notification_preference':{}},{'daily_run_limit':True},{'max_runs_per_cycle':11},{'unknown':1},{'sample_ids':[]}):
            with self.assertRaises(ValueError):campaigns.update(self.store,c['id'],args)
        other=sampling.create_sample(self.store,dict(inventory_id=self.sample['inventory_id'],size=10,audit_size=2,seed='other'))
        with self.assertRaisesRegex(ValueError,'membership is frozen'):campaigns.update(self.store,c['id'],{'sample_ids':[other['id']]})
        self.assertEqual(campaigns.detail(self.store,c['id'])['version'],1)
    def test_scheduler_policy_pause_and_shared_budget(self):
        self.assertTrue(campaigns.scheduling_policy(self.store,self.sample['id'])['allowed'])
        c=self.create(state='active',daily_run_limit=1,max_runs_per_cycle=1)
        self.assertEqual(campaigns.active_sample_ids(self.store),[self.sample['id']])
        autoresearch.configure(self.store,dict(enabled=True,sample_ids=[self.sample['id']],max_runs_per_cycle=1))
        autoresearch.tick(self.store)
        p=campaigns.scheduling_policy(self.store,self.sample['id']);self.assertFalse(p['allowed']);self.assertEqual(p['campaigns'][0]['daily_remaining'],0)
        campaigns.update(self.store,c['id'],{'daily_run_limit':10,'state':'paused'})
        self.assertFalse(campaigns.scheduling_policy(self.store,self.sample['id'])['allowed'])
        campaigns.update(self.store,c['id'],{'state':'active'})
        self.assertTrue(campaigns.scheduling_policy(self.store,self.sample['id'])['allowed'])
    def test_monitoring_groups_distinct_checkpoints_not_improvement(self):
        c=self.create(state='active')
        autoresearch.configure(self.store,dict(enabled=True,sample_ids=[self.sample['id']]))
        autoresearch.tick(self.store)
        detail=campaigns.detail(self.store,c['id'])
        self.assertEqual(len(detail['jobs']),3)
        self.assertEqual(detail['progress']['job_counts'],{'blocked':3})
        self.assertEqual(detail['progress']['completed_runs'],0)
        self.assertEqual(detail['progress']['distinct_evaluation_contexts'],0)
        self.assertEqual(len(detail['comparison_groups']),0)
        self.assertEqual(len(detail['runs']),3)
        self.assertTrue(all(r['metrics'] is None for r in detail['runs']))
        self.assertFalse(detail['release_eligible']);self.assertIn('Resolve',detail['next_action'])
    def test_comparison_requires_same_scored_membership_and_evidence(self):
        c=self.create(state='active');autoresearch.configure(self.store,dict(enabled=True,sample_ids=[self.sample['id']],max_runs_per_cycle=1));autoresearch.tick(self.store)
        p=json.loads(self.store.db.execute('SELECT body FROM research_sessions ORDER BY rowid DESC LIMIT 1').fetchone()[0])
        a=campaigns._session_brief(p,None)
        b=campaigns._session_brief(dict(p,evidence_hash='changed'),None)
        self.assertNotEqual(a['comparison_group'],b['comparison_group'])
        b=campaigns._session_brief(p,{'results':[{'bill_id':'118-hr1','status':'available','outcome':1}]})
        self.assertNotEqual(a['comparison_group'],b['comparison_group'])
        with self.assertRaises(Exception):self.store.db.execute('DELETE FROM campaign_events')

    def test_notifications_respect_preferences_and_stable_job_identity(self):
        c=self.create(state='active')
        autoresearch.configure(self.store,dict(enabled=True,sample_ids=[self.sample['id']]))
        autoresearch.tick(self.store)
        detail=campaigns.detail(self.store,c['id'])
        self.assertEqual(len(detail['notifications']),3)
        self.assertEqual(len({n['id'] for n in detail['notifications']}),3)
        self.assertTrue(all(n['status']=='blocked' for n in detail['notifications']))
        self.assertEqual(campaigns.update(self.store,c['id'],{'notification_preference':'quiet'})['notifications'],[])
        job=autoresearch._jobs(self.store)[0];job.update(status='completed');autoresearch._save(self.store,job)
        self.assertEqual(len(campaigns.update(self.store,c['id'],{'notification_preference':'attention'})['notifications']),2)
        self.assertEqual(len(campaigns.update(self.store,c['id'],{'notification_preference':'all_results'})['notifications']),3)

    def test_only_scored_completed_results_enter_comparison_groups(self):
        c=self.create(state='active')
        autoresearch.configure(self.store,dict(enabled=True,sample_ids=[self.sample['id']]))
        autoresearch.tick(self.store)
        jobs=autoresearch._jobs(self.store)
        for i,job in enumerate(jobs[:2]):
            result=dict(status='completed',scored=i,metrics={'brier':.2} if i else None,baseline={'brier':.25} if i else None,
                        results=[{'bill_id':self.sample['bill_ids'][0],'status':'available','outcome':1}] if i else [])
            with self.store.db:self.store.db.execute('INSERT INTO session_results VALUES (?,?)',(job['session_id'],json.dumps(result)))
        detail=campaigns.detail(self.store,c['id'])
        self.assertEqual(detail['progress']['completed_runs'],2)
        self.assertEqual(detail['progress']['distinct_evaluation_contexts'],1)
        self.assertEqual(len(detail['comparison_groups']),1)
        self.assertEqual(detail['comparison_groups'][0]['runs'][0]['scored'],1)

    def test_adaptive_metrics_read_from_saved_learning_without_artifacts(self):
        c=self.create(state='active')
        autoresearch.configure(self.store,dict(enabled=True,sample_ids=[self.sample['id']],max_runs_per_cycle=1))
        autoresearch.tick(self.store)
        job=autoresearch._jobs(self.store)[0]
        saved=dict(status='adjusted',version='adaptive-test',metrics={'n':2,'brier':.1},fixed_metrics={'n':2,'brier':.2},
                   selection_policy={'feature_version':'context-test'},cases=[{'probability':.4,'selected_feature_policy':'structured_context','artifact':{'secret':'not returned'}},{'probability':.2,'selected_feature_policy':'structured'}])
        # Campaign detail creates the read-only learning table before joining it.
        campaigns.detail(self.store,c['id'])
        with self.store.db:self.store.db.execute('INSERT INTO learning_records VALUES (?,?,?)',(job['session_id'],'test-evidence',json.dumps(saved)))
        run=campaigns.detail(self.store,c['id'])['runs'][0]
        self.assertEqual(run['adaptive_metrics']['brier'],.1)
        self.assertEqual(run['fixed_paired_metrics']['brier'],.2)
        self.assertEqual(run['feature_policy_counts'],{'structured_context':1,'structured':1})
        self.assertEqual(run['learning_status'],'adjusted')
        self.assertEqual(run['learning_feature_version'],'context-test')
        self.assertNotIn('artifact',json.dumps(run))
