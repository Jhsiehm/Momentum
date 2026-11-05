import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from engine.store import Store, now
from engine.fixtures import seed
from engine import workspace as w


class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.store=Store(Path(self.tmp.name)/'engine.sqlite')
        w.initialize(self.store);seed(self.store)

    def tearDown(self):
        self.store.close();self.tmp.cleanup()

    def test_run_reports_are_scoped_and_reruns_preserve_original(self):
        first=w.execute_experiment(self.store,w.create_experiment(self.store,{'dataset':'demo','congress':118,'age_days':180}))
        second=w.execute_experiment(self.store,w.create_experiment(self.store,first['config'],first['id']))
        self.assertEqual(first['status'],'completed')
        self.assertEqual(first['attempted'],15)
        self.assertEqual(first['metrics']['n'],15)
        self.assertEqual(first['metrics'],second['metrics'])
        self.assertNotEqual(first['id'],second['id'])
        self.assertEqual(w.get_experiment(self.store,first['id']),first)
        self.assertEqual(second['parent_id'],first['id'])
        self.assertEqual(first['input_hash'],second['input_hash'])

    def test_official_without_data_never_invents_metrics(self):
        run=w.execute_experiment(self.store,w.create_experiment(self.store,{'dataset':'official','congress':119,'age_days':180}))
        self.assertEqual(run['attempted'],0)
        self.assertIsNone(run['metrics'])
        self.assertEqual(run['available'],0)

    def test_invalid_tools_and_experiments_rejected(self):
        with self.assertRaises(ValueError):w.validate_experiment({'dataset':'all','congress':118,'age_days':180})
        with self.assertRaises(ValueError):w.validate_experiment({'dataset':'demo','age_days':99999})
        with self.assertRaises(ValueError):w.execute_tool(self.store,'execute_shell',{'command':'anything'})
        with self.assertRaises(ValueError):w.execute_tool(self.store,'open_view',{'view':'https://example.com'})

    def test_submission_idempotence_and_same_chat_serialization(self):
        chat=w.new_chat(self.store)
        with patch('engine.workspace.threading.Thread') as thread:
            first=w.submit_message(self.store,chat['id'],'Inspect the sources','demo','test-request-123')
            second=w.submit_message(self.store,chat['id'],'Inspect the sources','demo','test-request-123')
            self.assertEqual(len(first['messages']),2)
            self.assertEqual(first,second)
            self.assertEqual(thread.call_count,1)
            with self.assertRaises(ValueError):w.submit_message(self.store,chat['id'],'Another request','demo','test-request-456')

    def test_chat_worker_tool_results_persist_as_artifacts(self):
        chat=w.new_chat(self.store)
        with patch('engine.workspace.threading.Thread'):
            result=w.submit_message(self.store,chat['id'],'Show available sources','demo','test-request-tool')
        response_id=result['messages'][-1]['id']
        responses=[{'choices':[{'message':{'role':'assistant','content':None,'tool_calls':[{'id':'c1','type':'function','function':{'name':'list_sources','arguments':'{"dataset":"demo"}'}}]}}]},
                   {'choices':[{'message':{'role':'assistant','content':'The synthetic collection contains 315 fictional records.'}}]}]
        with patch('engine.workspace.completion',side_effect=responses):
            w.chat_worker(self.store.path,chat['id'],response_id,'demo')
        final=w.get_chat(self.store,chat['id'])['messages'][-1]
        self.assertEqual(final['status'],'completed')
        self.assertEqual(final['artifacts'][0]['view'],'sources')
        self.assertEqual(self.store.db.execute('SELECT COUNT(*) FROM ai_runs').fetchone()[0],1)

    def test_provider_failure_recorded_and_retry_possible(self):
        chat=w.new_chat(self.store)
        with patch('engine.workspace.threading.Thread'):
            result=w.submit_message(self.store,chat['id'],'Hello','demo','test-request-fail')
        with patch('engine.workspace.completion',side_effect=RuntimeError('Provider unavailable')):
            w.chat_worker(self.store.path,chat['id'],result['messages'][-1]['id'],'demo')
        final=w.get_chat(self.store,chat['id'])['messages'][-1]
        self.assertEqual(final['status'],'failed')
        self.assertIn('Provider unavailable',final['content'])
        with patch('engine.workspace.threading.Thread'):
            retry=w.submit_message(self.store,chat['id'],'Hello again','demo','test-request-retry')
        self.assertEqual(retry['messages'][-1]['status'],'running')

    def test_restart_recovers_pending_work(self):
        chat=w.new_chat(self.store)
        with patch('engine.workspace.threading.Thread'):
            w.submit_message(self.store,chat['id'],'Hello','demo','test-request-restart')
        run=w.create_experiment(self.store,{'dataset':'demo'})
        w.recover_interrupted(self.store)
        self.assertEqual(w.get_chat(self.store,chat['id'])['messages'][-1]['status'],'failed')
        self.assertEqual(w.get_experiment(self.store,run['id'])['status'],'failed')

    def test_experiment_summary_is_computed_not_model_interpretation(self):
        run={'status':'completed','config':{'dataset':'demo','congress':118,'age_days':180},'available':15,'attempted':15,
             'metrics':{'n':15,'brier':.227},'baseline':{'brier':.256},'note':'Synthetic only.'}
        summary=w.run_summary(run)
        self.assertIn('0.227',summary);self.assertIn('0.256',summary)
        self.assertIn('synthetic demo',summary)
        self.assertNotIn('lower than',summary)

    def test_credential_paste_rejected_before_storage(self):
        chat=w.new_chat(self.store)
        with self.assertRaises(ValueError):
            w.submit_message(self.store,chat['id'],'set key sk-or-exampleabcdefghijklmnop','demo','credential-test-123')
        self.assertEqual(len(w.get_chat(self.store,chat['id'])['messages']),0)

    def test_settings_never_disclose_saved_key(self):
        with patch.dict('os.environ',{'OPENROUTER_API_KEY':'private-test-key','OPENROUTER_MODEL':'test/model'}):
            response=w.settings()
            self.assertTrue(response['configured'])
            self.assertNotIn('private-test-key',json.dumps(response))
            self.assertNotIn('key',response)
        with self.assertRaises(ValueError):w.save_settings({'model':'bad\nmodel','key':''})

if __name__=='__main__':unittest.main()
