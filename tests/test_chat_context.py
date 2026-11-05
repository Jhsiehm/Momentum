import copy,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from engine.store import Store
from engine.fixtures import seed
from engine import collections,chat_context,workspace

class ContextTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.store=Store(Path(self.tmp.name)/'test.sqlite');seed(self.store);workspace.initialize(self.store)
        self.c=collections.save_collection(self.store,{'name':'Research view','dataset':'demo','bill_ids':['demo-118-hr101','demo-118-hr102']})
        self.context=dict(collection_id=self.c['id'],collection_version=1,collection_name='Forged client title',dataset='demo',bill_id='demo-118-hr101',cutoff='2023-07-01',window_days=90,filter={'query':'Health','topic':'','watched_only':False},visible_bill_ids=['demo-118-hr102'])
    def tearDown(self):self.store.close();self.tmp.cleanup()
    def test_server_recomputes_labels_and_filtered_membership(self):
        r=chat_context.validate(self.store,self.context,'demo')
        self.assertEqual(r['collection_name'],'Research view')
        self.assertEqual(r['visible_bill_ids'],['demo-118-hr101'])
    def test_membership_version_pinned_and_future_metadata_hidden(self):
        collections.save_collection(self.store,dict(self.c,name='New version',bill_ids=['demo-118-s103'],expected_version=1))
        r=chat_context.validate(self.store,self.context,'demo');self.assertEqual(r['collection_version'],1)
        c=copy.deepcopy(self.context);c['cutoff']='2020-01-01';c['filter']['query']='hospital'
        self.assertEqual(chat_context.validate(self.store,c,'demo')['visible_bill_ids'],[])
    def test_invalid_context_rejected(self):
        for key,value in [('bill_id','demo-118-s103'),('dataset','official'),('cutoff','2099-01-01'),('collection_version',0),('visible_bill_ids',['foreign'])]:
            with self.subTest(key=key),self.assertRaises(ValueError):chat_context.validate(self.store,dict(self.context,**{key:value}),'demo')
    def test_context_persisted_and_passed_to_model(self):
        c=workspace.new_chat(self.store)
        with patch('engine.workspace.threading.Thread'):
            chat=workspace.submit_message(self.store,c['id'],'Explain this view','demo','context-request-test',self.context)
        self.assertEqual(chat['messages'][0]['research_context']['visible_bill_ids'],['demo-118-hr101'])
        result={'choices':[{'message':{'content':'This is a synthetic historical view.'}}]}
        with patch('engine.workspace.completion',return_value=result) as completion:
            workspace.chat_worker(self.store.path,c['id'],chat['messages'][-1]['id'],'demo')
            messages=completion.call_args.args[0]
            self.assertIn('Server-validated research context',messages[-1]['content'])
            self.assertIn('2023-07-01T23:59:59Z',messages[-1]['content'])
        self.assertEqual(workspace.get_chat(self.store,c['id'])['messages'][-1]['status'],'completed')

    def test_explore_tool_keeps_view_scope_and_artifact(self):
        from engine import product_tools
        context=chat_context.validate(self.store,self.context,'demo')
        args=product_tools.contextual_arguments('explore_collection',{'collection_id':self.c['id']},context)
        result,artifact=product_tools.execute(self.store,'explore_collection',args)
        self.assertEqual([r['bill_id'] for r in result['rows']],['demo-118-hr101'])
        self.assertEqual(result['summary']['total'],1)
        self.assertEqual(result['collection_summary']['total'],2)
        self.assertEqual(artifact['filter'],context['filter'])
        self.assertEqual(artifact['bill_id'],context['bill_id'])
        explicit=product_tools.contextual_arguments('explore_collection',dict(collection_id=self.c['id'],filter={'query':''}),context)
        self.assertEqual(explicit['filter'],{'query':''})
