import json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from engine import sampling,sample_research,collections,workspace,product_tools
from engine.store import Store


def listing(c,k):
    return ('<html><table>'+''.join(f'<tr data-name="BILLSTATUS-{c}{k}{i}.xml"><a href="/bulkdata/BILLSTATUS/{c}/{k}/BILLSTATUS-{c}{k}{i}.xml">x</a></tr>' for i in range(1,201))+'</table></html>').encode()

class SampleResearchTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.store=Store(Path(self.temp.name)/'db');workspace.initialize(self.store)
        def fetch(url):
            c,k=url.rsplit('/',2)[-2:];return listing(c,k)
        with patch('engine.sampling.fetch',side_effect=fetch),patch('engine.sampling.retain',return_value='fixture'):
            self.inv=sampling.discover_inventory(self.store,{'congresses':[114,118]})
    def tearDown(self):self.store.close();self.temp.cleanup()
    def sample(self,size=100):return sampling.create_sample(self.store,dict(inventory_id=self.inv['id'],size=size,audit_size=25,seed='integration'))
    def test_proposal_pins_membership_and_blocks_unaudited_sample(self):
        sample=self.sample();c=collections.get_collection(self.store,sample['evaluation_collection_id'])
        collections.save_collection(self.store,dict(c,expected_version=1,bill_ids=['118-hr999']))
        r=sample_research.propose(self.store,{'sample_id':sample['id']})
        self.assertEqual(r['collection']['bill_ids'],c['bill_ids'])
        self.assertNotIn('118-hr999',r['collection']['bill_ids'])
        self.assertEqual(r['status'],'blocked')
        self.assertIn('human audit',' '.join(r['preflight']['blockers']))
    def test_large_sample_includes_all_evaluation_batches(self):
        sample=self.sample(600);r=sample_research.propose(self.store,{'sample_id':sample['id']})
        self.assertEqual(len(r['collection']['bill_ids']),300)
        self.assertEqual(r['preflight']['target_count'],300)
    def test_training_excludes_every_recorded_test_family_and_foreign_records(self):
        sample=self.sample();test=[b for b in sample['bill_ids'] if b.startswith('118-')];train=[b for b in sample['bill_ids'] if b.startswith('114-')]
        for bid,family in [(test[0],'family-x'),(test[1],'family-y'),(train[0],'family-x'),('114-hr999','foreign')]:
            self.store.add('bill',dict(bill_id=bid,family_id=family,dataset='official',source_url='https://www.govinfo.gov/example',source_name='Fixture',effective_at='2015-01-01',observed_at='2026-01-01',type='hr',congress=int(bid[:3]),title='Fixture',introduced_at='2015-01-01',source_key=bid))
        r=sample_research.propose(self.store,{'sample_id':sample['id']})
        self.assertEqual(r['sample_context']['excluded_training_ids'],[train[0]])
        saved=json.loads(self.store.db.execute('SELECT evidence FROM research_sessions WHERE id=?',(r['id'],)).fetchone()[0])
        self.assertEqual({row['bill_id'] for row in saved},set(test[:2]))
    def test_chat_briefs_retain_ids_and_counts_at_scale(self):
        sample=self.sample(600)
        r,a=product_tools.execute(self.store,'list_audited_samples',{})
        self.assertEqual(r['samples'][0]['id'],sample['id']);self.assertNotIn('bill_ids',r['samples'][0])
        self.assertLess(len(json.dumps(r)),6000)
        result=product_tools.bulk_brief(dict(id='job',status='running',total=10000,completed=100,parsed=99,failed=1,results=[dict(bill_id='118-hr1',status='failed')]))
        self.assertEqual(result['completed'],100);self.assertEqual(result['failures'][0]['bill_id'],'118-hr1')
