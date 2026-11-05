import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from engine import autoresearch, sampling, workspace, sessions
from engine.store import Store


class AutomaticResearchTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.store=Store(Path(self.temp.name)/'db');workspace.initialize(self.store)
        def fetch(url):
            congress,kind=url.rsplit('/',2)[-2:]
            return ('<html><table>'+''.join(f'<tr data-name="BILLSTATUS-{congress}{kind}{i}.xml"><a href="/bulkdata/BILLSTATUS/{congress}/{kind}/BILLSTATUS-{congress}{kind}{i}.xml">x</a></tr>' for i in range(1,11))+'</table></html>').encode()
        with patch('engine.sampling.fetch',side_effect=fetch),patch('engine.sampling.retain',return_value='fixture'):
            inventory=sampling.discover_inventory(self.store,{'congresses':[114,118]})
        self.sample=sampling.create_sample(self.store,dict(inventory_id=inventory['id'],size=20,audit_size=5,seed='auto-test'))
    def tearDown(self):self.store.close();self.temp.cleanup()
    def enable(self,**kwargs):
        return autoresearch.configure(self.store,dict(enabled=True,sample_ids=[self.sample['id']],**kwargs))
    def test_default_off_and_validation(self):
        self.assertFalse(autoresearch.summary(self.store)['settings']['enabled'])
        self.assertEqual(autoresearch.tick(self.store)['tick_status'],'paused')
        for args in ({'enabled':True},{'interval_minutes':14},{'daily_run_limit':101},{'max_runs_per_cycle':0},{'enabled':1},{'sample_ids':[self.sample['id']]*2}):
            with self.assertRaises(ValueError):autoresearch.configure(self.store,args)
    def test_blocked_deduplicates_and_never_executes(self):
        self.enable()
        with patch('engine.autoresearch.sessions.execute') as execute:
            result=autoresearch.tick(self.store)
            self.assertEqual(len(result['jobs']),3)
            self.assertTrue(all(j['status']=='blocked' for j in result['jobs']))
            self.assertEqual({j['age_days'] for j in result['jobs']},{90,180,365})
            self.assertTrue(all(j['session_id'] for j in result['jobs']))
            autoresearch.tick(self.store);execute.assert_not_called()
        self.assertEqual(len(autoresearch.summary(self.store)['jobs']),3)
        for job in result['jobs']:
            session=sessions.get_session(self.store,job['session_id'])
            self.assertEqual(session['sample_context']['sample_id'],self.sample['id'])
            self.assertFalse(session['release_eligible'])
    def test_daily_budget_and_changed_audit(self):
        self.enable(daily_run_limit=2,max_runs_per_cycle=1)
        autoresearch.tick(self.store);autoresearch.tick(self.store);result=autoresearch.tick(self.store)
        self.assertEqual(len(result['jobs']),2);self.assertEqual(result['daily_remaining'],0)
        autoresearch.configure(self.store,{'daily_run_limit':10,'max_runs_per_cycle':3})
        autoresearch.tick(self.store)
        sampling.save_audit(self.store,dict(sample_id=self.sample['id'],bill_id=self.sample['audit_bill_ids'][0],status='needs_correction',checks={k:False for k in ['identity','source','availability','family','outcome']},notes='Missing provenance.'))
        result=autoresearch.tick(self.store)
        self.assertEqual(len(result['jobs']),6)
    def test_pause_between_jobs(self):
        self.enable();original=autoresearch._run
        def pausing(store,job):
            original(store,job);autoresearch.configure(store,{'enabled':False})
        with patch('engine.autoresearch._run',side_effect=pausing):result=autoresearch.tick(self.store)
        self.assertEqual(sum(j['status']=='blocked' for j in result['jobs']),1)
        self.assertEqual(sum(j['status']=='queued' for j in result['jobs']),2)
        self.assertEqual(result['last_cycle']['status'],'paused')
        self.enable();result=autoresearch.tick(self.store)
        self.assertTrue(all(j['status']=='blocked' for j in result['jobs']))
    def test_recovery_reuses_saved_session(self):
        self.enable(max_runs_per_cycle=1)
        result=autoresearch.tick(self.store);job=result['jobs'][0];session_id=job['session_id']
        count=self.store.db.execute('SELECT count(*) FROM research_sessions').fetchone()[0]
        job.update(status='running',session_id=None);autoresearch._save(self.store,job)
        result=autoresearch.recover(self.store);self.assertEqual(result['jobs'][0]['status'],'recovered')
        with patch('engine.autoresearch.sample_research.propose',side_effect=AssertionError('Must reuse frozen proposal')):
            result=autoresearch.tick(self.store)
        self.assertEqual(result['jobs'][0]['session_id'],session_id)
        self.assertEqual(self.store.db.execute('SELECT count(*) FROM research_sessions').fetchone()[0],count)
    def test_changed_sample_evidence_allows_new_identity_foreign_evidence_does_not(self):
        self.enable();autoresearch.tick(self.store)
        def add(bid):
            self.store.add('bill',dict(bill_id=bid,family_id=bid,dataset='official',source_url='https://www.govinfo.gov/example',source_name='Fixture',effective_at='2015-01-01',observed_at='2026-01-01',type='hr',congress=int(bid[:3]),title='Fixture',introduced_at='2015-01-01',source_key=bid))
        add('114-hr999');self.assertEqual(len(autoresearch.tick(self.store)['jobs']),3)
        add(self.sample['bill_ids'][0]);self.assertEqual(len(autoresearch.tick(self.store)['jobs']),6)

    def campaign(self,sample=None,**kwargs):
        from engine import campaigns
        return campaigns.create(self.store,dict(name='Campaign controls',goal='Compare frozen samples under explicit run budgets.',sample_ids=[(sample or self.sample)['id']],**kwargs))

    def test_paused_campaign_suppresses_global_sample_and_queued_runs(self):
        from engine import campaigns
        self.enable(max_runs_per_cycle=3)
        campaign=self.campaign(state='paused')
        self.assertEqual(autoresearch.tick(self.store)['jobs'],[])
        campaigns.update(self.store,campaign['id'],{'state':'active','max_runs_per_cycle':1})
        result=autoresearch.tick(self.store)
        self.assertEqual(sum(j['status']=='blocked' for j in result['jobs']),1)
        self.assertEqual(sum(j['status']=='queued' for j in result['jobs']),2)
        campaigns.update(self.store,campaign['id'],{'state':'paused'})
        result=autoresearch.tick(self.store)
        self.assertEqual(sum(j['status']=='blocked' for j in result['jobs']),1)
        self.assertEqual(sum(j['status']=='queued' for j in result['jobs']),2)

    def test_campaign_cycle_and_daily_caps_then_resume(self):
        from engine import campaigns
        self.enable()
        campaign=self.campaign(state='active',daily_run_limit=1,max_runs_per_cycle=1)
        result=autoresearch.tick(self.store)
        self.assertEqual(sum(j['status']=='blocked' for j in result['jobs']),1)
        self.assertEqual(sum(j['status']=='blocked' for j in autoresearch.tick(self.store)['jobs']),1)
        campaigns.update(self.store,campaign['id'],{'state':'paused','daily_run_limit':3})
        self.assertEqual(sum(j['status']=='blocked' for j in autoresearch.tick(self.store)['jobs']),1)
        campaigns.update(self.store,campaign['id'],{'state':'active'})
        self.assertEqual(sum(j['status']=='blocked' for j in autoresearch.tick(self.store)['jobs']),2)
        self.assertEqual(sum(j['status']=='blocked' for j in autoresearch.tick(self.store)['jobs']),3)

    def test_active_campaign_sample_outside_global_selection_is_included(self):
        other=sampling.create_sample(self.store,dict(inventory_id=self.sample['inventory_id'],size=20,audit_size=5,seed='campaign-union'))
        self.enable(max_runs_per_cycle=10)
        self.campaign(sample=other,state='active')
        result=autoresearch.tick(self.store)
        self.assertEqual({j['sample_id'] for j in result['jobs']},{self.sample['id'],other['id']})
        self.assertTrue(all(j['status']=='blocked' for j in result['jobs']))
        self.assertEqual(result['settings']['sample_ids'],[self.sample['id']])
        from engine import campaigns
        detail=campaigns.list_campaigns(self.store)[0]
        self.assertEqual(detail['runner']['unselected_sample_ids'],[])
        self.assertNotIn('Add the campaign samples',detail['next_action'])

    def test_active_campaign_can_enable_runner_without_global_sample_selection(self):
        self.campaign(state='active')
        result=autoresearch.configure(self.store,{'enabled':True})
        self.assertEqual(result['settings']['sample_ids'],[])
        self.assertTrue(autoresearch.tick(self.store)['jobs'])
