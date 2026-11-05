import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from engine import sessions, learning_workspace as lab
from engine.store import Store
from engine.fixtures import seed
from engine.collections import save_collection


class LearningWorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.store=Store(Path(self.tmp.name)/'test.sqlite')
        seed(self.store)
        c=save_collection(self.store,dict(name='Learning test',dataset='demo',bill_ids=['demo-118-hr101']))
        self.session=sessions.propose(self.store,dict(collection_id=c['id'],hypothesis='Test the frozen learner.'))

    def tearDown(self):
        self.store.close(); self.tmp.cleanup()

    def test_training_inspection_and_dataset_separation(self):
        self.assertEqual(lab.summary(self.store)['sessions'],[])
        self.assertEqual(len(lab.summary(self.store,'demo')['sessions']),1)
        result=lab.train(self.store,self.session['id'])
        self.assertFalse(result['release_eligible'])
        self.assertEqual(result,lab.train(self.store,self.session['id']))
        saved=sessions.get_session(self.store,self.session['id'])
        self.assertEqual(result['reproducibility_hash'],saved['learning']['reproducibility_hash'])
        self.assertEqual(result['cases'][0]['fixed_weights'][0]['coefficient'],saved['result']['results'][0]['model_artifact']['weights'][0])
        self.assertEqual(result['metrics']['n'],result['fixed_metrics']['n'])

    def test_code_gate_cannot_be_bypassed(self):
        with patch('engine.sessions._code',return_value={'changed':True}):
            with self.assertRaisesRegex(ValueError,'Implementation changed'):
                lab.train(self.store,self.session['id'])
        self.assertIsNone(sessions.get_session(self.store,self.session['id'])['result'])

    def test_feature_names_and_scaling(self):
        a=dict(weights=[0]*41,means=[0]*40,scales=[1]*40,feature_policy='structured_context',feature_manifest={'base_width':6})
        rows=lab.weights(a)
        self.assertEqual(len(rows),41)
        self.assertEqual(rows[-1]['feature'],'Stage × inactivity')
        self.assertEqual(rows[5]['feature'],'Senate bill')
        with self.assertRaises(ValueError):lab.summary(self.store,'mixed')
