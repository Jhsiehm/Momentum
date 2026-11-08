import copy
import unittest
from scripts.run_mechanism_expansion_v3 import compare, sample_key
from scripts.mechanism_design_extractor import MECHANISMS


class ExpansionRunnerTests(unittest.TestCase):
    def fixture(self):
        text='No individual may act. Report annually.'
        def candidate(hits):
            return dict(candidate_id='c',mechanism='prohibit',start=0,end=len(text),quote=text,hits=hits)
        flags=dict(proposals=[],suppressed_proposals=[],assessments={m:{'status':'abstain','candidate_count':int(m=='prohibit')} for m in MECHANISMS},
                   accepted_v2_labels_created=0,human_certified=False,historical_feature_eligible=False,trained_model=False)
        old=dict(flags,candidates=[candidate([dict(start=14,end=17,quote='may')])])
        new=copy.deepcopy(old);new['candidates'][0]['hits'].append(dict(start=0,end=13,quote='No individual',rule_ids=['actor_bar']))
        ref={'effects':[dict(mechanism='prohibit',start=0,end=13,quote='No individual')]}
        return old,new,ref,text

    def test_recovery_and_workload_not_false_positive(self):
        old,new,ref,text=self.fixture();out=compare(old,new,ref,text)
        self.assertEqual(out['recovered_effect_indices'],[0]);self.assertEqual(out['lost_effect_indices'],[])
        self.assertEqual(out['added_hits_outside_reference_quotes'],0)
        ref['effects'][0]=dict(mechanism='require',start=0,end=13,quote='No individual')
        out=compare(old,new,ref,text);self.assertEqual(out['added_hits_outside_reference_quotes'],1)
        self.assertEqual(out['recovered_effect_indices'],[])

    def test_duplicate_lost_tampered_and_promoted_hits_reject(self):
        for mode in ('duplicate','lost','quote','promotion','context','count','model'):
            old,new,ref,text=self.fixture()
            if mode=='duplicate':new['candidates'][0]['hits'].append(new['candidates'][0]['hits'][0])
            if mode=='lost':new['candidates'][0]['hits'].pop(0)
            if mode=='quote':new['candidates'][0]['hits'][1]['quote']='wrong'
            if mode=='promotion':new['assessments']['require']['status']='present'
            if mode=='context':new['candidates'][0]['candidate_id']='changed'
            if mode=='count':new['assessments']['require']['candidate_count']=1
            if mode=='model':new['trained_model']=True
            with self.assertRaises(ValueError):compare(old,new,ref,text)

    def test_sample_ranking_stable_and_identity_sensitive(self):
        row=dict(bill_id='x',mechanism='require',start=1,end=2)
        self.assertEqual(sample_key(row),sample_key(dict(row)))
        self.assertNotEqual(sample_key(row),sample_key(dict(row,end=3)))
