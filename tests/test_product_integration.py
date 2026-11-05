import json
import tempfile
import threading
import unittest
import urllib.request
import urllib.error
from pathlib import Path
from unittest.mock import patch
from http.server import ThreadingHTTPServer
from engine import server, workspace, product_tools, collections, sessions
from engine.store import Store
from engine.fixtures import seed

class ProductIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name)/'workspace.sqlite'
        self.store=Store(self.path);seed(self.store);workspace.initialize(self.store)
        self.patch=patch('engine.server.Store',side_effect=lambda:Store(self.path));self.patch.start()
        self.http=ThreadingHTTPServer(('127.0.0.1',0),server.Handler)
        self.thread=threading.Thread(target=self.http.serve_forever,daemon=True);self.thread.start()
        self.url='http://127.0.0.1:'+str(self.http.server_port)
    def tearDown(self):
        self.http.shutdown();self.http.server_close();self.thread.join();self.patch.stop();self.store.close();self.tmp.cleanup()
    def request(self,path,body=None,origin=None):
        headers={'Content-Type':'application/json'}
        if origin:headers['Origin']=origin
        req=urllib.request.Request(self.url+'/api/'+path,data=json.dumps(body).encode() if body is not None else None,headers=headers)
        with urllib.request.urlopen(req,timeout=15) as r:return json.load(r)
    def test_http_collection_session_roundtrip(self):
        c=self.request('collections',{'name':'Integration demo','dataset':'demo','bill_ids':['demo-118-hr101','demo-118-hr102']})
        p=self.request('sessions/propose',{'collection_id':c['id'],'title':'Integration session','hypothesis':'Compare the frozen model with its historical-rate baseline.'})
        self.assertEqual(p['preflight']['target_count'],2)
        r=self.request('sessions/execute',{'id':p['id']});self.assertEqual(r['result']['attempted'],2)
        bundle=self.request('session/export?id='+p['id']);self.assertNotIn('OPENROUTER_API_KEY',json.dumps(bundle))
        self.assertTrue(self.request('sessions/reproduce',{'id':p['id']})['matches'])
        child=self.request('sessions/replicate',{'id':p['id']});run=self.request('sessions/execute',{'id':child['id']})
        self.assertNotEqual(r['id'],run['id']);self.assertEqual(r['result']['reproducibility_hash'],run['result']['reproducibility_hash'])
    def test_chat_tool_artifacts_and_computed_summary(self):
        c,_=product_tools.execute(self.store,'save_collection',{'name':'Chat demo','dataset':'demo','bill_ids':['demo-118-hr101']})
        p,a=workspace.execute_tool(self.store,'propose_research_session',{'collection_id':c['id'],'title':'Chat proposal','hypothesis':'Check the selected synthetic bill against the baseline.'})
        self.assertEqual(a['view'],'session');self.assertEqual(a['id'],p['id'])
        r,a=workspace.execute_tool(self.store,'run_research_session',{'id':p['id']})
        self.assertIn('Synthetic demonstration',product_tools.session_summary(r))
        self.assertNotIn('model_artifact',r['result']['results'][0])
        self.assertEqual(self.request('session?id='+p['id'])['result']['attempted'],1)
    def test_monitoring_opt_in_and_write_boundary(self):
        self.assertFalse(self.request('monitoring')['settings']['enabled'])
        with self.assertRaises(urllib.error.HTTPError) as caught:
            self.request('monitoring/settings',{'enabled':True},origin='https://untrusted.example')
        self.assertEqual(caught.exception.code,403)
        self.assertFalse(self.request('monitoring')['settings']['enabled'])
        with self.assertRaises(urllib.error.HTTPError):self.request('sessions/propose',[])
        with self.assertRaises(urllib.error.HTTPError):self.request('monitoring/settings',{'interval_minutes':1})
        self.assertEqual(self.request('monitoring/refresh',{})['status'],'completed')

    def test_background_research_settings_http_and_chat(self):
        self.assertFalse(self.request('autoresearch')['settings']['enabled'])
        result=self.request('autoresearch/settings',{'daily_run_limit':8,'interval_minutes':30})
        self.assertEqual(result['settings']['daily_run_limit'],8)
        with self.assertRaises(urllib.error.HTTPError):
            self.request('autoresearch/settings',{'enabled':True})
        with self.assertRaises(urllib.error.HTTPError) as caught:
            self.request('autoresearch/settings',{'daily_run_limit':99},origin='https://untrusted.example')
        self.assertEqual(caught.exception.code,403)
        brief,artifact=product_tools.execute(self.store,'inspect_background_research',{})
        self.assertEqual(brief['settings']['daily_run_limit'],8)
        self.assertEqual(artifact['view'],'autoresearch')
    def test_sample_http_workflow_and_audit_download(self):
        from test_sampling import directory
        def fetch(url):
            c,k=url.rsplit('/',2)[-2:];return directory(int(c),k,30)
        with patch('engine.sampling.fetch',side_effect=fetch),patch('engine.sampling.retain',return_value='fixture'):
            inv=self.request('sampling/inventory',{'congresses':[114,118]})
        sample=self.request('sampling/samples',{'inventory_id':inv['id'],'size':30,'audit_size':5,'seed':'http-test','name':'HTTP sample'})
        campaign=self.request('campaigns',{'name':'HTTP campaign','goal':'Check reproducible evidence and candidate development.','sample_ids':[sample['id']]})
        self.assertEqual(campaign['state'],'draft')
        active=self.request('campaign/update',{'id':campaign['id'],'state':'active'})
        self.assertEqual(active['state'],'active')
        self.assertEqual(self.request('campaign?id='+campaign['id'])['sample_ids'],[sample['id']])
        self.assertIsNone(self.request('coverage')['training_eligible'])
        prefs=self.request('priorities',{'issues':['energy'],'organizations':[]})
        self.assertEqual(prefs['preferences']['issues'],['energy'])
        self.assertIn('items',self.request('activity'))
        self.assertEqual(len(self.request('sampling/samples')),1)
        proposal=self.request('sampling/propose',{'sample_id':sample['id']})
        self.assertEqual(proposal['status'],'blocked')
        self.assertEqual(proposal['preflight']['target_count'],sum(b.startswith('118-') for b in sample['bill_ids']))
        updated=self.request('sampling/audit',dict(sample_id=sample['id'],bill_id=sample['audit_bill_ids'][0],status='needs_correction',checks={k:False for k in ('identity','source','availability','family','outcome')},notes='Source provenance needs review.'))
        self.assertEqual(updated['readiness']['audited'],1)
        with urllib.request.urlopen(self.url+'/api/sampling/audit.csv?id='+sample['id']) as r:
            self.assertIn('text/csv',r.headers['Content-Type']);csv_body=r.read().decode('utf-8-sig')
            self.assertIn('Source provenance needs review.',csv_body)
            self.assertIn('sample-audit.csv',r.headers['Content-Disposition'])
        with patch('engine.sampling.run_bulk_job'):
            job=self.request('sampling/import',{'sample_id':sample['id']})
        self.assertEqual(job['total'],30)
        self.assertEqual(self.request('sampling/job?id='+job['id'])['status'],'queued')
