import unittest
from engine.paper_evaluation import seal
from scripts.mechanism_rubric_v2_audit import validate_primary,validate_peer


class RubricV2Tests(unittest.TestCase):
    def setUp(self):
        self.text='Findings: may act. Operative: may act.'
        self.effect=dict(mechanism='authorize',operation='create',dimension='authority_scope',actor=None,target='power',conditions=None,quote='may act',start=30,end=37,rationale='Operative permission.')
        self.spec=dict(rubric_sha256='rubric',batches={'agent_a':['113-hr1']},mechanisms=['authorize','repeal'],statuses=['present','absent','uncertain'],operations=['create','remove'],dimensions=['authority_scope'],effect_fields=list(self.effect),record_fields=['bill_id','source_view_hash','summary','mechanisms','uncertainties','unresolved_effects','effects'])
        self.inputs=[dict(bill_id='113-hr1',view_hash='view',text=self.text)]
        self.review=dict(reviewer='agent_a',registration_hash='reg',rubric_sha256='rubric',human_certified=False,historical_feature_eligible=False,
                         records=[dict(bill_id='113-hr1',source_view_hash='view',summary='Proposes permission.',mechanisms={'authorize':'present','repeal':'uncertain'},uncertainties={'repeal':'Displaced text unavailable.'},unresolved_effects=[],effects=[self.effect])])

    def test_selected_occurrence_and_unknown_preserved(self):
        self.assertEqual(validate_primary(self.review,self.spec,self.inputs,'reg','agent_a'),1)
        self.assertEqual(self.text[self.effect['start']:self.effect['end']],'may act')
        self.assertNotEqual(self.effect['start'],self.text.find('may act'))

    def test_wrong_offsets_direction_and_unbacked_status_rejected(self):
        self.effect['start']=0
        with self.assertRaisesRegex(ValueError,'Quote/offset'):validate_primary(self.review,self.spec,self.inputs,'reg','agent_a')
        self.effect['start']=30;self.effect['operation']='invented'
        with self.assertRaisesRegex(ValueError,'direction'):validate_primary(self.review,self.spec,self.inputs,'reg','agent_a')
        self.effect['operation']='create';self.review['records'][0]['effects']=[]
        with self.assertRaisesRegex(ValueError,'lacks effect'):validate_primary(self.review,self.spec,self.inputs,'reg','agent_a')

    def test_missing_uncertainty_and_false_eligibility_rejected(self):
        self.review['records'][0]['uncertainties']={}
        with self.assertRaisesRegex(ValueError,'Uncertainty'):validate_primary(self.review,self.spec,self.inputs,'reg','agent_a')
        self.review['human_certified']=True
        with self.assertRaisesRegex(ValueError,'certification'):validate_primary(self.review,self.spec,self.inputs,'reg','agent_a')

    def test_peer_requires_complete_bound_coverage(self):
        original=seal(self.review)
        peer=dict(reviewer='agent_b',registration_hash='reg',primary_review_hash=original['hash'],human_certified=False,historical_feature_eligible=False,records=[dict(bill_id='113-hr1',decision='supported',findings=[])])
        self.assertEqual(validate_peer(peer,original,self.spec,self.inputs,'reg','agent_b'),0)
        peer['records'][0]['decision']='corrections_requested'
        with self.assertRaisesRegex(ValueError,'findings'):validate_peer(peer,original,self.spec,self.inputs,'reg','agent_b')
        peer['records'][0]['findings']=[dict(mechanism='repeal',effect_index=0,issue='Wrong attachment',proposed_change='Reclassify',quote=None,start=None,end=None)]
        with self.assertRaisesRegex(ValueError,'mechanism/index'):validate_peer(peer,original,self.spec,self.inputs,'reg','agent_b')
        peer['historical_feature_eligible']=True
        with self.assertRaisesRegex(ValueError,'certification'):validate_peer(peer,original,self.spec,self.inputs,'reg','agent_b')
        peer['historical_feature_eligible']=False
        peer['records']=[]
        with self.assertRaisesRegex(ValueError,'coverage'):validate_peer(peer,original,self.spec,self.inputs,'reg','agent_b')


if __name__=='__main__':unittest.main()
