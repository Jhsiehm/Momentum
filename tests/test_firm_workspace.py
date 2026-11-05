import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from engine import firm_workspace as firm, monitoring
from engine.store import Store, digest


class FirmWorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.store=Store(Path(self.tmp.name)/'db')
        self.bill=dict(bill_id='119-hr1',dataset='official',family_id='119-hr1',source_url='https://www.govinfo.gov/example',source_name='GovInfo',effective_at='2025-01-03',observed_at='2025-01-04',introduced_at='2025-01-03',title='Energy Research Act',topic='Energy',congress=119,type='hr',source_key='119-hr1')
        self.store.add('bill',self.bill)
        self.profile=firm.save_profile(self.store,dict(name='Client A',issues=['Energy'],congresses=[119]))
    def tearDown(self):self.store.close();self.tmp.cleanup()
    def test_profile_validation_and_concurrency(self):
        p=self.profile
        with self.assertRaises(ValueError):firm.save_profile(self.store,dict(id=p['id'],name='Changed'))
        updated=firm.save_profile(self.store,dict(id=p['id'],name='Changed',expected_version=1))
        self.assertEqual(updated['version'],2)
        with self.assertRaises(ValueError):firm.save_profile(self.store,dict(id=p['id'],name='Stale',expected_version=1))
        for args in [dict(name='x',congresses=[True]),dict(name='x',issues='Energy'),dict(name='x',surprise=True)]:
            with self.assertRaises(ValueError):firm.save_profile(self.store,args)
        self.assertEqual(len(firm.profiles(self.store)),1)
    def test_matching_reasons_exclusions_and_empty_interest(self):
        result=firm.dashboard(self.store,self.profile['id'])
        self.assertEqual(result['matches'][0]['matching_reasons'],[dict(field='title',term='Energy'),dict(field='topic',term='Energy')])
        self.assertFalse(result['matches'][0]['following'])
        p=firm.save_profile(self.store,dict(name='Excluded',issues=['Energy'],excluded_terms=['research']))
        self.assertEqual(firm.dashboard(self.store,p['id'])['matches'],[])
        p=firm.save_profile(self.store,dict(name='Empty'))
        self.assertEqual(firm.dashboard(self.store,p['id'])['matches'],[])
    def test_work_isolation_validation_and_version(self):
        args=dict(profile_id=self.profile['id'],bill_id='119-hr1',owner='Alex',priority='high',impact='high',notes='Internal context')
        w=firm.save_work_item(self.store,args)
        self.assertNotIn('probability',w)
        with self.assertRaises(ValueError):firm.save_work_item(self.store,args)
        w=firm.save_work_item(self.store,dict(args,expected_version=1,notes='Updated'))
        self.assertEqual(w['version'],2)
        other=firm.save_profile(self.store,dict(name='Client B'))
        self.assertEqual(firm.dashboard(self.store,other['id'])['work_items'],[])
        for update in [dict(bill_id='119-hr999'),dict(due_date='2025-02-30'),dict(status='invented')]:
            with self.assertRaises(ValueError):firm.save_work_item(self.store,dict(args,expected_version=2,**update))
    def test_positions_require_real_citation_and_never_verify(self):
        args=dict(profile_id=self.profile['id'],bill_id='119-hr1',organization='Trade group',position='support',statement='We support this bill.',source_url='https://example.org/statement',published_at='2025-01-01')
        p=firm.add_position(self.store,args)
        self.assertEqual(p['verification_status'],'user_recorded_unverified')
        self.assertNotIn('probability',p)
        for update in [dict(source_url='javascript:alert(1)'),dict(source_url='https://user:pass@example.org'),dict(published_at='2999-01-01'),dict(statement=''),dict(verification_status='verified')]:
            with self.assertRaises(ValueError):firm.add_position(self.store,dict(args,**update))
    def test_brief_immutable_sources_noise_filter_and_export(self):
        self.store.watch('official','119-hr1',True);monitoring.initialize(self.store)
        monitoring._event(self.store,'119-hr1','changed','Action updated',['events'])
        monitoring._event(self.store,'119-hr1','failed','Refresh failed')
        monitoring._event(self.store,'119-hr1','changed','Initial import',['initial_import'])
        b=firm.create_brief(self.store,dict(profile_id=self.profile['id']))
        self.assertEqual([e['message'] for e in b['snapshot']['changes']],['Action updated'])
        self.assertEqual(b['hash'],digest(b['snapshot']))
        self.assertIn('govinfo',b['markdown'])
        firm.save_profile(self.store,dict(id=self.profile['id'],name='New name',expected_version=1))
        self.assertEqual(firm.get_brief(self.store,b['id']),b)
        self.assertEqual(firm.export_brief(self.store,b['id']),b['markdown'])
        with self.assertRaises(sqlite3.IntegrityError):
            with self.store.db:self.store.db.execute('UPDATE firm_briefs SET body=? WHERE id=?',(json.dumps({}),b['id']))
        self.assertEqual(firm.get_brief(self.store,b['id']),b)
    def test_bounded_matches_and_markdown_escape(self):
        for i in range(2,103):self.store.add('bill',dict(self.bill,bill_id=f'119-hr{i}',source_key=f'119-hr{i}'))
        r=firm.dashboard(self.store,self.profile['id'])
        self.assertEqual(r['counts']['matches'],102);self.assertEqual(len(r['matches']),100);self.assertTrue(r['truncated']['matches'])
        firm.save_work_item(self.store,dict(profile_id=self.profile['id'],bill_id='119-hr1',notes='<script>alert(1)</script>\n# Fake heading'))
        text=firm.create_brief(self.store,dict(profile_id=self.profile['id']))['markdown']
        self.assertNotIn('<script>',text);self.assertNotIn('\n# Fake',text)

    def test_same_bill_profiles_keep_work_and_positions_separate(self):
        other=firm.save_profile(self.store,dict(name='Client B'))
        for profile,owner,position in [(self.profile,'Owner A','support'),(other,'Owner B','oppose')]:
            firm.save_work_item(self.store,dict(profile_id=profile['id'],bill_id='119-hr1',owner=owner))
            firm.add_position(self.store,dict(profile_id=profile['id'],bill_id='119-hr1',organization=profile['name'],position=position,statement='Recorded position',source_url='https://example.org/position',published_at='2025-01-01'))
        a=firm.dashboard(self.store,' '+self.profile['id']+' ')
        b=firm.dashboard(self.store,other['id'])
        self.assertEqual(a['work_items'][0]['owner'],'Owner A')
        self.assertEqual(b['work_items'][0]['owner'],'Owner B')
        self.assertEqual(a['positions'][0]['position'],'support')
        self.assertEqual(b['positions'][0]['position'],'oppose')
        for fn,args in [(firm.save_work_item,dict(profile_id=self.profile['id'],bill_id='119-hr1',bogus=True)),(firm.create_brief,dict(profile_id=self.profile['id'],bogus=True))]:
            with self.assertRaises(ValueError):fn(self.store,args)

    def test_brief_replacement_and_deletion_rejected(self):
        brief=firm.create_brief(self.store,dict(profile_id=self.profile['id']))
        for sql,params in [('DELETE FROM firm_briefs WHERE id=?',(brief['id'],)),('INSERT OR REPLACE INTO firm_briefs VALUES (?,?,?)',(brief['id'],self.profile['id'],'{}'))]:
            with self.assertRaises(sqlite3.IntegrityError):
                with self.store.db:self.store.db.execute(sql,params)
        self.assertEqual(firm.get_brief(self.store,brief['id']),brief)
