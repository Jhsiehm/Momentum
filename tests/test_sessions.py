import copy
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from engine.store import Store, available, timestamp, digest
from engine.fixtures import seed
from engine import sessions

class SessionTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.store=Store(Path(self.tmp.name)/'test.sqlite')
        seed(self.store)
        self.collection={'id':'selected','name':'Two selected targets','dataset':'demo','bill_ids':['demo-118-hr101','demo-118-hr102'],'version':1}
        self.getter=patch('engine.collections.get_collection',return_value=self.collection)
        self.getter.start()
    def tearDown(self):
        self.getter.stop(); self.store.close(); self.tmp.cleanup()
    def proposal(self):
        return sessions.propose(self.store,{'collection_id':'selected','hypothesis':'Structured signals improve the historical rate.','age_days':180})
    def test_selected_population_and_prior_training(self):
        p=self.proposal(); r=sessions.execute(self.store,p['id'])['result']
        self.assertEqual(set(self.collection['bill_ids']),{v['bill_id'] for v in r['results']})
        self.assertEqual(r['attempted'],2)
        for row in r['results']:
            if row['status']=='available':
                self.assertTrue(all(t['congress']<118 for t in row['training_manifest']))
                self.assertTrue(any(t['bill_id'] not in self.collection['bill_ids'] for t in row['training_manifest']))
        self.assertEqual(r['metrics']['n'],r['scored'])
        for row in r['results']:
            for training in row.get('training_manifest',[]):
                label = self.store.db.execute('SELECT body FROM records WHERE id=?',(training['resolution_id'],)).fetchone()
                import json
                self.assertLessEqual(available(json.loads(label[0])), timestamp(row['cutoff']))
                self.assertLess(timestamp(training['cutoff']), timestamp(json.loads(label[0])['effective_at']))

    def test_automatic_learning_lifecycle_and_reproduction(self):
        p=self.proposal()
        first=sessions.execute(self.store,p['id'])
        self.assertIsNotNone(first['learning'])
        self.assertFalse(first['learning']['release_eligible'])
        self.assertEqual(first['learning'],sessions.execute(self.store,p['id'])['learning'])
        reproduced=sessions.reproduce_bundle(sessions.export_bundle(self.store,p['id']))
        self.assertTrue(reproduced['matches'])
        self.assertTrue(reproduced['learning_matches'])
        child=sessions.replicate(self.store,p['id'])
        repeated=sessions.execute(self.store,child['id'])
        self.assertEqual(repeated['learning']['status'],'reused')
        self.assertFalse(repeated['learning']['new_learning'])

    def test_old_completed_run_does_not_gain_current_code_adaptation(self):
        p=self.proposal()
        with patch('engine.learning.process'):
            sessions.execute(self.store,p['id'])
        with patch('engine.sessions._code',return_value={'different':'implementation'}), patch('engine.learning.process') as learn:
            result=sessions.execute(self.store,p['id'])
            learn.assert_not_called()
            self.assertIsNone(result['learning'])
    def test_frozen_data_survives_collection_and_record_changes(self):
        p=self.proposal()
        self.collection['bill_ids'].append('demo-118-hr103')
        b=self.store.bill('demo','demo-118-hr101')
        self.store.add('bill',dict(b,title='Later correction',source_key='later',observed_at='2026-10-24'))
        r=sessions.execute(self.store,p['id'])
        self.assertEqual(r['result']['attempted'],2)
        self.assertEqual(r['evidence_hash'],p['evidence_hash'])
        self.assertNotEqual(r['result']['results'][0]['title'],'Later correction')
    def test_late_metadata_correction_cannot_move_checkpoint_or_title(self):
        original=self.store.bill('demo','demo-118-hr101','2023-07-01')
        correction=dict(original,introduced_at='2023-07-10',title='Hindsight revised title',
                        observed_at='2026-01-01',verified_available_at='2026-01-01')
        self.store.add('bill',correction)
        p=self.proposal(); run=sessions.execute(self.store,p['id'])
        row=next(r for r in run['result']['results'] if r['bill_id']=='demo-118-hr101')
        self.assertEqual(row['status'],'available')
        self.assertEqual(row['input_snapshot']['age_days'],180)
        self.assertEqual(row['title'],original['title'])
        from datetime import timedelta
        self.assertEqual(row['cutoff'],(sessions.date(original['introduced_at'])+timedelta(days=180)).isoformat())

    def test_conflicting_historical_introduction_fails_closed(self):
        original=self.store.bill('demo','demo-118-hr101','2023-07-01')
        correction=dict(original,introduced_at='2023-02-01',observed_at='2023-03-01',verified_available_at='2023-03-01')
        self.store.add('bill',correction)
        p=self.proposal()
        row=next(r for r in p['preflight']['cases'] if r['bill_id']=='demo-118-hr101')
        self.assertEqual(row['status'],'unavailable')
        self.assertIn('conflicts',row['reason'])

    def test_export_reproduces_and_tampering_fails(self):
        p=self.proposal(); first=sessions.execute(self.store,p['id'])
        self.assertEqual(first,sessions.execute(self.store,p['id']))
        bundle=sessions.export_bundle(self.store,p['id'])
        reproduced=sessions.reproduce_bundle(bundle)
        self.assertTrue(reproduced['matches'])
        bundle['evidence'][0]['body']='{}'
        with self.assertRaises(ValueError): sessions.reproduce_bundle(bundle)
    def test_rehashed_bundle_rejects_altered_scores_and_aggregates(self):
        p=self.proposal(); sessions.execute(self.store,p['id'])
        original=sessions.export_bundle(self.store,p['id'])
        def rehash(bundle):
            bundle['bundle_hash']=digest({k:v for k,v in bundle.items() if k!='bundle_hash'})
        bad=copy.deepcopy(original)
        bad['session']['result']['metrics']['brier']=999
        rehash(bad)
        with self.assertRaisesRegex(ValueError,'reproducibility hash'):
            sessions.reproduce_bundle(bad)
        # Even replacing both advertised hashes cannot conceal inconsistent scoring.
        bad['session']['result']['reproducibility_hash']=sessions._result_hash(bad['session'],bad['session']['result'])
        rehash(bad)
        with self.assertRaisesRegex(ValueError,'aggregate'):
            sessions.reproduce_bundle(bad)
        for field in ('available','scored','families','attempted','brier_difference'):
            with self.subTest(field=field):
                bad=copy.deepcopy(original)
                bad['session']['result'][field]=999
                rehash(bad)
                with self.assertRaisesRegex(ValueError,'aggregate'):
                    sessions.reproduce_bundle(bad)

    def test_revision_is_one_change_and_comparison_discloses_checkpoint(self):
        p=self.proposal(); sessions.execute(self.store,p['id'])
        revised=sessions.revise(self.store,p['id'],{'age_days':200})
        self.assertEqual(revised['parent_id'],p['id'])
        self.assertEqual(revised['evidence_hash'],p['evidence_hash'])
        sessions.execute(self.store,revised['id'])
        self.assertEqual(sessions.compare(self.store,p['id'],revised['id'])['status'],'not_comparable')
        with self.assertRaises(ValueError): sessions.revise(self.store,p['id'],{'age_days':200,'hypothesis':'different question'})
        with self.assertRaises(sqlite3.IntegrityError): self.store.db.execute('UPDATE research_sessions SET created_at=?',('bad',))
        self.store.db.rollback()
    def test_replication_preserves_inputs_and_metrics(self):
        p=self.proposal(); original=sessions.execute(self.store,p['id'])
        child=sessions.replicate(self.store,p['id'])
        self.assertNotEqual(p['id'],child['id'])
        self.assertEqual(child['evidence_hash'],p['evidence_hash'])
        self.assertEqual(child['change'],{'replication':True})
        repeated=sessions.execute(self.store,child['id'])
        self.assertEqual(original['result']['reproducibility_hash'],repeated['result']['reproducibility_hash'])
        self.assertEqual(sessions.compare(self.store,p['id'],child['id'])['brier_difference_right_minus_left'],0)

    def test_missing_historical_metadata_blocks_instead_of_zero(self):
        self.collection['bill_ids']=['not-imported']
        p=self.proposal()
        self.assertEqual(p['status'],'blocked')
        self.assertIsNone(p['preflight']['cases'][0]['outcome'])
        with self.assertRaises(ValueError): sessions.execute(self.store,p['id'])
    def test_sample_audit_blockers_are_frozen_and_survive_revision_and_replication(self):
        records=[dict(row) for row in self.store.db.execute("SELECT * FROM records WHERE dataset='demo' ORDER BY id")]
        context={'sample_id':'sample-one','sample_hash':'frozen-hash','blockers':['Human audit incomplete.']}
        p=sessions._save_proposal(self.store,'Sample comparison','Structured signals improve the historical rate.',180,self.collection,records,sample_context=context)
        self.assertGreater(p['preflight']['scoreable_count'],0)
        self.assertEqual(p['status'],'blocked')
        self.assertIn('Human audit incomplete.',p['preflight']['blockers'])
        context['blockers'].clear()
        self.assertEqual(sessions.get_session(self.store,p['id'])['sample_context']['blockers'],['Human audit incomplete.'])
        for child in [sessions.revise(self.store,p['id'],{'age_days':200}),sessions.replicate(self.store,p['id'])]:
            self.assertEqual(child['sample_context'],p['sample_context'])
            self.assertEqual(child['status'],'blocked')
            with self.assertRaisesRegex(ValueError,'Human audit incomplete'):
                sessions.execute(self.store,child['id'])
        with self.assertRaisesRegex(ValueError,'frozen membership'):
            sessions.revise(self.store,p['id'],{'collection_id':'other-collection'})
        with self.assertRaisesRegex(ValueError,'Human audit incomplete'):
            sessions.execute(self.store,p['id'])
        saved=sessions._row(self.store,p['id'])[0]
        self.assertEqual(saved['proposal_hash'],digest({k:v for k,v in saved.items() if k!='proposal_hash'}))
        with self.assertRaises(ValueError):
            sessions._save_proposal(self.store,'Invalid context','A valid hypothesis statement.',180,self.collection,records,sample_context={'blockers':'not a list'})

    def test_unsupported_design_rejected(self):
        with self.assertRaises(ValueError): sessions.propose(self.store,{'collection_id':'selected','hypothesis':'A causal outcome experiment','candidate':'D'})

if __name__=='__main__': unittest.main()
