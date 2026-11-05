import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from engine.store import Store
from engine import monitoring


class MonitoringTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.store=Store(Path(self.tmp.name)/'test.sqlite')
        self.record={'bill_id':'119-hr22','dataset':'official','family_id':'119-hr22','source_url':'https://www.govinfo.gov/example','source_name':'GovInfo','effective_at':'2025-01-03','introduced_at':'2025-01-03','observed_at':'2025-01-04','title':'Original','congress':119,'type':'hr','source_key':'119-hr22','raw_hash':'a'*64}
        self.store.add('bill',self.record)
        self.store.watch('official','119-hr22',True)
    def tearDown(self):
        self.store.close();self.tmp.cleanup()
    def test_default_off_and_settings_persist_and_validate(self):
        self.assertFalse(monitoring.summary(self.store)['settings']['enabled'])
        with self.assertRaises(ValueError):monitoring.configure(self.store,{'interval_minutes':1})
        with self.assertRaises(ValueError):monitoring.configure(self.store,{'enabled':'yes'})
        monitoring.configure(self.store,{'enabled':True,'interval_minutes':15,'notifications':False})
        reopened=Store(self.store.path)
        self.assertEqual(monitoring.summary(reopened)['settings'],{'enabled':True,'interval_minutes':15,'notifications':False})
        reopened.close()
    def test_retrieval_only_change_does_not_emit_semantic_change(self):
        def refresh(store,*args,**kwargs):
            store.add('bill',dict(self.record,observed_at='2025-02-01',raw_hash='b'*64))
        with patch('engine.monitoring.ingest_bill',side_effect=refresh):
            result=monitoring.refresh_watched(self.store)
        self.assertEqual(result['results'][0]['status'],'unchanged')
        self.assertEqual(monitoring.summary(self.store)['feed'],[])
        self.assertEqual(self.store.bill('official','119-hr22','2025-01-10')['raw_hash'],'a'*64)
    def test_change_failure_recovery_and_notification_preferences(self):
        monitoring.configure(self.store,{'notifications':False})
        def change(store,*args,**kwargs):
            store.add('bill',dict(self.record,title='Revised',observed_at='2025-02-01'))
        with patch('engine.monitoring.ingest_bill',side_effect=change):
            monitoring.refresh_watched(self.store)
        feed=monitoring.summary(self.store)['feed']
        self.assertEqual(feed[0]['changes'],['bill'])
        self.assertFalse(feed[0]['notify'])
        with patch('engine.monitoring.ingest_bill',side_effect=RuntimeError('private message')):
            monitoring.refresh_watched(self.store)
        state=monitoring.summary(self.store)['watched'][0]
        self.assertTrue(state['last_success'])
        self.assertTrue(state['last_error'])
        self.assertNotIn('private',state['last_error'])
        with patch('engine.monitoring.ingest_bill',return_value={}):
            monitoring.refresh_watched(self.store)
        self.assertEqual(monitoring.summary(self.store)['feed'][0]['kind'],'recovered')
    def test_disabled_scheduler_does_not_fetch_and_stops(self):
        with patch('engine.monitoring.ingest_bill') as fetch:
            stop=monitoring.start_scheduler(self.store.path)
            self.assertIs(stop,monitoring.start_scheduler(self.store.path))
            stop.set()
            # Join boundedly so the temporary database remains until thread exit.
            import threading
            for thread in threading.enumerate():
                if thread.name=='bill-watch-scheduler':thread.join(2)
            fetch.assert_not_called()
    def test_demo_watch_excluded_and_never_refreshed(self):
        self.store.watch('official','119-hr22',False)
        self.store.watch('demo','demo-118-hr101',True)
        with patch('engine.monitoring.ingest_bill') as fetch:
            monitoring.refresh_watched(self.store)
            fetch.assert_not_called()
        self.assertEqual(monitoring.summary(self.store)['watched'],[])

    def test_out_of_band_import_detected_against_last_success(self):
        with patch('engine.monitoring.ingest_bill',return_value={}):
            monitoring.refresh_watched(self.store)
            self.store.add('bill',dict(self.record,title='Imported by another tool',observed_at='2025-02-01'))
            cycle=monitoring.refresh_watched(self.store)
            self.assertEqual(cycle['results'][0]['changes'],['bill'])
            cycle=monitoring.refresh_watched(self.store)
            self.assertEqual(cycle['results'][0]['status'],'unchanged')
        self.assertEqual(len(monitoring.summary(self.store)['feed']),1)

    def test_oversized_watchlist_backs_off_without_network(self):
        monitoring.configure(self.store,{'enabled':True,'interval_minutes':15})
        for number in range(1,102):
            self.store.watch('official','119-hr'+str(number),True)
        with patch('engine.monitoring.ingest_bill') as fetch:
            cycle=monitoring.refresh_watched(self.store)
            fetch.assert_not_called()
        self.assertEqual(cycle['status'],'failed')
        saved=self.store.checkpoint('monitoring:last_cycle')
        self.assertEqual(saved,cycle)
        self.assertFalse(monitoring._is_due(monitoring.summary(self.store)['settings'],saved))

    def test_startup_recovery_preserves_partial_results_and_runs_once(self):
        partial={'id':'old-cycle','status':'running','started_at':'2025-01-01T00:00:00Z','results':[{'bill_id':'119-hr22','status':'unchanged'}]}
        self.store.checkpoint('monitoring:last_cycle',partial)
        recovered=monitoring.recover_monitoring(self.store)
        self.assertEqual(recovered['status'],'interrupted')
        self.assertEqual(recovered['results'],partial['results'])
        monitoring.recover_monitoring(self.store)
        self.assertEqual(len(monitoring.summary(self.store)['feed']),1)
