import copy
import hashlib
import unittest
from scripts.run_mechanism_context_filter import audit_decisions,overlap,review_sample


class FilterRunnerTests(unittest.TestCase):
    def fixture(self):
        output={'source_view_hash':'a'*64,'candidates':[{'candidate_id':'c','mechanism':'reporting','hits':[{'start':0,'end':6,'quote':'report'}]}]}
        decision=dict(mechanism='reporting',start=0,end=6,status='flagged',quote='report',candidate_id='c',reasons=['heading_only'],evidence=[dict(start=0,end=6,quote='report')])
        result=dict(bill_id='b',source_view_hash='a'*64,input_text_sha256=hashlib.sha256(b'report').hexdigest(),decisions=[decision],human_certified=False,historical_feature_eligible=False,semantic_accuracy_verified=False)
        return output,result,{'text':'report','bill_id':'b','view_hash':'a'*64}

    def test_flag_keeps_rawhit_and_lost_intersection_is_counted(self):
        output,result,view=self.fixture();decisions=audit_decisions(result,output,view)
        ref={'effects':[dict(mechanism='reporting',start=0,end=6)]}
        counts,lost=overlap(ref,set(decisions),decisions)
        self.assertEqual(counts['reporting'],dict(reference_effects=1,raw_overlap=1,retained_overlap=0,lost=1))
        self.assertEqual(lost,[0]);self.assertEqual(len(output['candidates'][0]['hits']),1)

    def test_missing_duplicate_boolean_evidence_and_certification_reject(self):
        for mode in ('missing','duplicate','boolean','evidence','certification','reason','binding'):
            output,result,view=self.fixture()
            if mode=='missing':result['decisions']=[]
            if mode=='duplicate':result['decisions'].append(copy.deepcopy(result['decisions'][0]))
            if mode=='boolean':result['decisions'][0]['start']=False
            if mode=='evidence':result['decisions'][0]['evidence'][0]['quote']='wrong'
            if mode=='certification':result['human_certified']=True
            if mode=='reason':result['decisions'][0]['reasons']=[]
            if mode=='binding':result['bill_id']='wrong'
            with self.assertRaises(ValueError):audit_decisions(result,output,view)

    def test_sampling_excludes_prior_and_keeps_shortfall(self):
        added=[dict(bill_id='b',mechanism='reporting',start=i,end=i+1) for i in range(30)]
        decisions={('b','reporting',i,i+1):dict(status='flagged' if i<3 else 'retain',reasons=[]) for i in range(30)}
        selected,quotas=review_sample(added,decisions,{('b','reporting',0,1)})
        self.assertEqual(quotas['flagged'],dict(eligible=2,selected=2,requested=12,shortfall=10))
        self.assertEqual(quotas['retain']['selected'],12)
        self.assertNotIn(0,[r['start'] for r in selected]);self.assertEqual(len(selected),14)
        self.assertEqual((selected,quotas),review_sample(list(reversed(added)),decisions,{('b','reporting',0,1)}))
