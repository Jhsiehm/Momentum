import copy
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from engine import learning
from engine.store import Store


class LearningTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.store=Store(Path(self.tmp.name)/'test.sqlite')
        self.store.db.execute('CREATE TABLE research_sessions(id TEXT PRIMARY KEY,evidence TEXT)')
        self.rows=[]; self.evidence=[]
        for congress,n in ((114,24),(116,12)):
            for i in range(n):
                identity=f'{congress}-{i}'
                self.rows.append({'bill_id':identity,'family_id':identity,'congress':congress,
                                  'cutoff':f'{2015 if congress==114 else 2019}-07-01T00:00:00Z',
                                  'title':'Health bill' if i%2 else 'Transport bill','topic':'Health' if i%2 else 'Transport',
                                  'x':[i%2,i/n],'y':i%2,'resolution_id':'r'+identity})
                self.evidence.append({'id':'r'+identity,'kind':'resolution',
                                      'available_at':f'{2017 if congress==114 else 2021}-01-03T00:00:00Z',
                                      'effective_at':f'{2017 if congress==114 else 2021}-01-03T00:00:00Z'})
        self.session={'id':'one','config':{'dataset':'demo'},'evidence_hash':'fixed',
                      'result':{'status':'completed','results':[{'bill_id':'target','status':'available',
                       'cutoff':'2023-07-01T00:00:00Z','training_manifest':self.rows,
                       'input_snapshot':{'features':[1,.5],'bill':{'title':'Health bill','topic':'Health'}},'probability':.5,'outcome':1}]}}
        self.save(self.session)

    def save(self,session):
        self.store.db.execute('INSERT INTO research_sessions VALUES (?,?)',(session['id'],json.dumps(self.evidence)))
        self.store.db.commit()

    def tearDown(self):
        self.store.close(); self.tmp.cleanup()

    def test_chronological_selection_artifact_and_immutable_idempotence(self):
        result=learning.process(self.store,self.session)
        self.assertEqual(result,learning.process(self.store,self.session))
        case=result['cases'][0]
        self.assertIn(case['status'],('adjusted','retained'))
        self.assertEqual(len(case['inner_validation']['trials']),6)
        self.assertFalse(set(case['inner_validation']['train_families']) & set(case['inner_validation']['validation_families']))
        self.assertTrue(all(x.startswith('114') for x in case['inner_validation']['train_ids']))
        self.assertFalse(result['release_eligible'])
        with self.assertRaises(sqlite3.IntegrityError): self.store.db.execute('DELETE FROM learning_records')

    def test_target_labels_do_not_change_training_or_predictions(self):
        first=learning.process(self.store,self.session)['cases'][0]
        changed=copy.deepcopy(self.session); changed['id']='two'; changed['result']['results'][0]['outcome']=0
        self.save(changed)
        second=learning.process(self.store,changed)['cases'][0]
        for key in ('artifact','probability','selected_l2','inner_validation'):
            self.assertEqual(first[key],second[key])

    def test_repeated_evidence_reuses_not_new_learning(self):
        first=learning.process(self.store,self.session)
        other=copy.deepcopy(self.session); other['id']='two'; self.save(other)
        repeat=learning.process(self.store,other)
        self.assertEqual(repeat['status'],'reused')
        self.assertFalse(repeat['new_learning'])
        self.assertEqual(repeat['source_learning_id'],first['id'])

    def test_late_training_labels_cannot_enter_inner_split(self):
        for r in self.evidence: r['available_at']='2022-01-01T00:00:00Z'
        self.store.db.execute('UPDATE research_sessions SET evidence=?',(json.dumps(self.evidence),)); self.store.db.commit()
        case=learning.process(self.store,self.session)['cases'][0]
        self.assertEqual(case['status'],'no_adjustment')
        self.assertEqual(case['inner_validation']['train_ids'],[])
        self.assertEqual(case['probability'],.5)

    def test_sparse_or_overlapping_families_do_not_tune(self):
        self.session['result']['results'][0]['training_manifest'][1]['family_id']=self.rows[0]['family_id']
        result=learning.process(self.store,self.session)
        self.assertEqual(result['status'],'no_adjustment')
        self.assertFalse(result['new_learning'])

    def test_dataset_and_checkpoint_isolation(self):
        first=learning.process(self.store,self.session)
        other=copy.deepcopy(self.session); other['id']='two'; other['config']['dataset']='official'; self.save(other)
        self.assertNotEqual(first['evidence_identity'],learning.process(self.store,other)['evidence_identity'])
        third=copy.deepcopy(self.session); third['id']='three'; third['result']['results'][0]['cutoff']='2023-08-01T00:00:00Z'; self.save(third)
        self.assertNotEqual(first['evidence_identity'],learning.process(self.store,third)['evidence_identity'])

    def test_context_features_fixed_width_and_frozen_metadata_only(self):
        row={'x':[.5,.1,.2,.3,1.,.4],'title':'Health Bill','topic':'Health'}
        transformed=learning.features(row,'structured_context')
        self.assertEqual(len(transformed),40)
        self.assertEqual(transformed[-2:],[.2,.15])
        self.assertEqual(transformed,learning.features(dict(row,title='HEALTH BILL'),'structured_context'))
        self.assertEqual(len(learning.features({'x':row['x']},'structured_context')),40)
        self.assertNotEqual(transformed,learning.features(dict(row,title='Transport Bill',topic='Transport'),'structured_context'))
        self.assertEqual(transformed,learning.features(dict(row,outcome=0,future_title='A later title'),'structured_context'))

    def test_context_fit_records_transformation_and_uses_inner_train_normalization(self):
        result=learning.process(self.store,self.session)
        artifact=result['cases'][0]['artifact']
        self.assertEqual(artifact['feature_version'],learning.FEATURE_VERSION)
        self.assertEqual(len(artifact['means']),2 if artifact['feature_policy']=='structured' else 36)
        trials=result['cases'][0]['inner_validation']['trials']
        self.assertEqual({t['feature_policy'] for t in trials},{'structured','structured_context'})
        for trial in trials: self.assertEqual(len(trial['transformed_training_hash']),64)


if __name__=='__main__': unittest.main()
