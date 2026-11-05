import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from engine.store import Store
from engine.collections import save_collection
from engine.explore import collection_view


class ExploreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = Store(Path(self.tmp.name) / 'test.sqlite')
        self.collection = save_collection(self.store, dict(name='Evidence test', dataset='official', bill_ids=['118-hr1', '118-s2']))
        self.base = dict(dataset='official', bill_id='118-hr1', family_id='118-hr1',
                         source_url='https://www.govinfo.gov/test', source_name='GovInfo',
                         effective_at='2023-01-01', observed_at='2023-01-02')
        self.store.add('bill', dict(self.base, source_key='bill', title='Original title', topic='Health', type='hr', congress=118, introduced_at='2023-01-01'))
    def tearDown(self):
        self.store.close()
        self.tmp.cleanup()
    def view(self, cutoff='2023-06-01', **kwargs):
        return collection_view(self.store, self.collection['id'], cutoff, **kwargs)
    def test_late_arrival_is_knowledge_not_recent_action(self):
        self.store.add('event', dict(self.base, source_key='action', stage=1, observed_at='2023-05-01'))
        row = self.view()['rows'][0]
        self.assertEqual(row['new_event_count'], 1)
        self.assertEqual(row['effective_event_count'], 0)
        self.assertEqual(row['stage_change'], 1)
        self.assertEqual(self.view('2023-04-01')['rows'][0]['event_count'], 0)
    def test_refresh_does_not_create_changes(self):
        event = dict(self.base, source_key='action', stage=1)
        self.store.add('event', event)
        self.store.add('event', dict(event, observed_at='2023-05-01', raw_hash='updated-fetch'))
        row = self.view()['rows'][0]
        self.assertEqual(row['event_count'], 1)
        self.assertEqual(row['new_event_count'], 0)
        self.assertEqual(row['stage_change'], 0)
    def test_missing_and_future_metadata_never_leak(self):
        self.store.add('bill', dict(self.base, bill_id='118-s2', source_key='future-bill', observed_at='2024-01-01', title='Secret later title', topic='Future topic', type='s', congress=118, introduced_at='2023-01-01'))
        self.store.add('event', dict(self.base, bill_id='118-s2', stage=4, observed_at='2024-01-01'))
        page = self.view()
        row = page['rows'][1]
        self.assertFalse(row['available'])
        self.assertEqual(row['title'], 'Metadata unavailable at cutoff')
        self.assertEqual(row['topic'], 'Unavailable')
        self.assertIsNone(row['stage'])
        self.assertIsNone(row['type'])
        self.assertNotIn('Secret later title', str(page))
        self.assertEqual(page['collection']['coverage']['imported'], 1)
    def test_future_cutoff_clamped(self):
        with patch('engine.explore.now', return_value='2025-01-01T12:00:00Z'):
            page = self.view('2030-01-01')
            self.assertEqual(page['as_of'], '2025-01-01T12:00:00Z')
            self.assertEqual(page['date_bounds']['max'], '2025-01-01')
    def test_exact_collection_and_validation(self):
        self.store.add('bill', dict(self.base, bill_id='118-hr999', source_key='foreign', title='Unrelated', topic='Other', type='hr', congress=118, introduced_at='2023-01-01'))
        self.assertEqual([r['bill_id'] for r in self.view()['rows']], self.collection['bill_ids'])
        with self.assertRaises(ValueError):
            collection_view(self.store, 'not-a-collection')
        for window in [True, 0, 731, 2.5, 'invalid']:
            with self.assertRaises(ValueError):
                self.view(window_days=window)
    def test_effective_future_event_excluded_and_watch_is_current(self):
        self.store.add('event', dict(self.base, effective_at='2024-01-01', stage=4))
        self.store.watch('official', '118-hr1', True)
        row = self.view()['rows'][0]
        self.assertEqual(row['stage'], 0)
        self.assertEqual(row['event_count'], 0)
        self.assertTrue(row['watched'])

    def test_version_pins_saved_membership(self):
        changed = save_collection(self.store, dict(id=self.collection['id'], expected_version=1,
            name='Changed', dataset='official', bill_ids=['118-s2']))
        latest = self.view()
        original = self.view(collection_version=1)
        self.assertEqual(latest['collection']['version'], changed['version'])
        self.assertEqual([r['bill_id'] for r in latest['rows']], ['118-s2'])
        self.assertEqual(original['collection']['version'], 1)
        self.assertEqual([r['bill_id'] for r in original['rows']], ['118-hr1', '118-s2'])
        with self.assertRaises(ValueError):
            self.view(collection_version=999)

    def test_comparison_preserves_timestamp_precision(self):
        page = self.view('2023-06-01T12:34:56Z', window_days=1)
        self.assertEqual(page['previous_as_of'], '2023-05-31T12:34:56Z')
