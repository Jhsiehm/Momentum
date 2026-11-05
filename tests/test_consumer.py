import tempfile
import unittest
from pathlib import Path
from engine import consumer
from engine.store import Store

class ConsumerTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.store=Store(Path(self.tmp.name)/'db')
        self.bill=dict(bill_id='119-hr1',dataset='official',family_id='119-hr1',source_url='https://www.govinfo.gov/example',source_name='GovInfo',effective_at='2025-01-03',observed_at='2025-01-04',introduced_at='2025-01-03',title='Energy Research Act',topic='Energy',congress=119,type='hr',source_key='119-hr1')
        self.store.add('bill',self.bill)
    def tearDown(self):self.store.close();self.tmp.cleanup()
    def test_priorities_saved_matches_not_organization_relationships(self):
        r=consumer.priorities(self.store,{'issues':[' energy ','energy'],'organizations':['Example Company']})
        self.assertEqual(r['preferences']['issues'],['energy'])
        self.assertEqual(r['matches'][0]['bill_id'],'119-hr1')
        self.assertNotIn('organization',r['matches'][0])
        self.store.watch('official','119-hr1',True)
        self.assertEqual(consumer.priorities(self.store)['watched'][0]['title'],'Energy Research Act')
        with self.assertRaises(ValueError):consumer.priorities(self.store,{'issues':'not a list'})
    def test_activity_actual_snapshot_and_stable_identity(self):
        from engine import prospective
        r=prospective.capture(self.store,'official','119-hr1')
        prospective.capture(self.store,'official','119-hr1')
        items=consumer.activity(self.store)['items']
        captures=[i for i in items if i['type']=='forecast']
        self.assertEqual(len(captures),1)
        self.assertEqual(captures[0]['id'],r['id'])
        self.assertEqual(captures[0]['view'],'bill')

    def test_home_excludes_operational_noise_and_unfollowed_changes(self):
        from engine import monitoring
        monitoring.initialize(self.store)
        self.store.watch('official','119-hr1',True)
        monitoring._event(self.store,'119-hr1','changed','Title updated')
        monitoring._event(self.store,'119-hr1','failed','Network failure')
        monitoring._event(self.store,'119-hr1','recovered','Network recovered')
        monitoring._event(self.store,'119-hr2','changed','Another bill updated')
        result=consumer.priorities(self.store)
        self.assertEqual([e['message'] for e in result['changes']],['Title updated'])
        self.assertEqual(result['monitoring']['failed_bills'],0)
        self.assertFalse(result['monitoring']['enabled'])
        self.assertEqual(len(consumer.activity(self.store)['items']),4)

    def test_discovery_search_filters_pagination_and_official_scope(self):
        for i in range(2,26):
            self.store.add('bill',{**self.bill,'bill_id':f'119-hr{i}','source_key':f'119-hr{i}','title':f'Housing Act {i}','topic':'Housing'})
        self.store.add('bill',{**self.bill,'dataset':'demo','bill_id':'119-s99','source_key':'119-s99'})
        self.store.watch('official','119-hr1',True)
        self.assertEqual(consumer.browse(self.store,{'q':'H.R. 1'})['bills'][0]['bill_id'],'119-hr1')
        self.assertEqual(consumer.browse(self.store,{'q':'energy'})['total'],1)
        self.assertEqual(consumer.browse(self.store,{'following':'1'})['total'],1)
        self.assertEqual(consumer.browse(self.store,{'congress':'118'})['total'],0)
        page=consumer.browse(self.store,{'q':'Housing','limit':10,'page':2})
        self.assertEqual((page['total'],page['pages'],len(page['bills'])),(24,3,10))
        self.assertEqual(page['imported'],25)
        self.assertEqual(consumer.browse(self.store,{'limit':1000})['limit'],50)
        self.assertEqual(consumer.browse(self.store,{'page':99})['page'],2)
        with self.assertRaises(ValueError):consumer.browse(self.store,{'q':'a'*201})
        with self.assertRaises(ValueError):consumer.browse(self.store,{'page':'invalid'})
