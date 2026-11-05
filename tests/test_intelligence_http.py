import json
import tempfile
import threading
import unittest
import urllib.request
import urllib.error
from pathlib import Path
from unittest.mock import patch
from http.server import ThreadingHTTPServer
from engine import server
from engine.store import Store

class IntelligenceHTTPTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name)/'db'
        with_store=Store(self.path)
        with_store.add('bill',dict(bill_id='119-hr1',dataset='official',family_id='119-hr1',source_url='https://www.govinfo.gov/example',source_name='GovInfo',effective_at='2025-01-03',observed_at='2025-01-04',introduced_at='2025-01-03',title='Energy Research Act',topic='Energy',congress=119,type='hr',source_key='119-hr1'))
        with_store.close()
        self.mock=patch('engine.server.Store',side_effect=lambda:Store(self.path));self.mock.start()
        self.http=ThreadingHTTPServer(('127.0.0.1',0),server.Handler)
        self.thread=threading.Thread(target=self.http.serve_forever,daemon=True);self.thread.start()
        self.url='http://127.0.0.1:'+str(self.http.server_port)+'/api/'
    def tearDown(self):
        self.http.shutdown();self.http.server_close();self.thread.join();self.mock.stop();self.tmp.cleanup()
    def request(self,path,body=None):
        req=urllib.request.Request(self.url+path,data=json.dumps(body).encode() if body is not None else None,headers={'Content-Type':'application/json'})
        with urllib.request.urlopen(req,timeout=15) as r:return json.load(r)
    def test_organization_assignment_position_brief_roundtrip(self):
        p=self.request('firm/profiles',{'name':'Test organization','issues':['Energy']})
        d=self.request('firm/dashboard?profile_id='+p['id']);self.assertEqual(d['counts']['matches'],1)
        self.request('firm/work-item',{'profile_id':p['id'],'bill_id':'119-hr1','owner':'Analyst','next_action':'Read committee evidence'})
        self.request('firm/positions',{'profile_id':p['id'],'bill_id':'119-hr1','organization':'Test stakeholder','position':'support','statement':'Test source statement','source_url':'https://example.org/position','published_at':'2025-01-01'})
        b=self.request('firm/brief',{'profile_id':p['id']})
        self.assertEqual(self.request('firm/brief?id='+b['id'])['hash'],b['hash'])
        self.assertEqual(b['snapshot']['positions'][0]['verification_status'],'user_recorded_unverified')
        with self.assertRaises(urllib.error.HTTPError) as error:self.request('firm/work-item',{'profile_id':p['id'],'bill_id':'119-hr1'})
        self.assertEqual(error.exception.code,400)
    def test_analysis_rank_scenario_and_validation(self):
        r=self.request('intelligence/analyze',{'filters':{'query':'energy'},'groups':[{'name':'Energy','filters':{'query':'energy'}}]})
        self.assertEqual(r['summary']['unknown'],1);self.assertIsNone(r['summary']['observed_rate'])
        self.assertEqual(sum(x['total'] for x in r['overlaps']),r['summary']['total'])
        self.assertEqual(self.request('intelligence/report?id='+r['id'])['content_hash'],r['content_hash'])
        self.assertTrue(self.request('intelligence/reports'))
        rank=self.request('intelligence/rank',{});self.assertEqual(rank['eligible'],0)
        scenario=self.request('intelligence/scenario',{'question':'What if control changes?','assumptions':['Control changes']})
        self.assertIsNone(scenario['probability'])
        self.assertTrue(self.request('intelligence/capabilities')['unsupported'])
        with self.assertRaises(urllib.error.HTTPError):self.request('intelligence/analyze',{'filters':{'influence':1}})
