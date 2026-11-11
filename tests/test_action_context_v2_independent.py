import copy
import unittest
import numpy as np
from scripts import action_context_diagnostic_v2 as m
from tests.test_action_context_fit_independent import row,protected
class IndependentAmendedRunnerTests(unittest.TestCase):
    def contract(self,bid='hr1-113',ok=True):
        return dict(bill_id=bid,all_problem_dates_match_concordant=ok,concordant_date_count=int(ok),concordant_numbers_equal_law_list=ok,public_law_identity_count=1,concordant_assertion_count=int(ok))
    def label(self,y=None,reason='before',bid='hr1-113'):
        r=dict(bill_id=bid,y=y,reason=reason)
        if y==1:r.update(enacted_at='2013-12-01',label_matured_at='2013-12-01')
        return r
    def delta(self,before,after,cases):return m.label_delta(before,after,cases,[row()])
    def test_only_approved_unknown_to_one(self):
        before={'hr1-113':self.label()};after={'hr1-113':self.label(1,'concordant')}
        self.assertFalse(self.delta(before,after,[self.contract()])['violations'])
        self.assertTrue(self.delta(before,after,[self.contract(ok=False)])['violations'])
        after['hr1-113']['y']=0
        self.assertTrue(self.delta(before,after,[self.contract()])['violations'])
    def test_old_negative_record_immutable(self):
        before={'hr1-113':self.label(0)}
        for after in [self.label(1),self.label(0,'different'),self.label()]:
            self.assertTrue(self.delta(before,{'hr1-113':after},[self.contract()])['violations'])
    def test_outside_contract_reason_cannot_change(self):
        self.assertTrue(self.delta({'hr1-113':self.label()},{'hr1-113':self.label(None,'changed')},[])['violations'])
    def test_uncorroborated_reason_change_stays_unknown(self):
        d=self.delta({'hr1-113':self.label()},{'hr1-113':self.label(None,'uncorroborated')},[self.contract(ok=False)])
        self.assertFalse(d['violations']);self.assertEqual(d['label_changes'],0);self.assertTrue(d['rows'][0]['record_changed'])
    def test_population_and_duplicates_rejected(self):
        with self.assertRaises(ValueError):self.delta({'hr1-113':self.label()},{},[])
        with self.assertRaises(ValueError):self.delta({'hr1-113':self.label()},{'hr1-113':self.label()},[self.contract(),self.contract()])
    def test_fixed_family_and_transform_identical_except_version(self):
        from scripts import action_context_diagnostic_v1 as old
        rows=[row(),row('hr2-113',values=[None,8.,.3]),row('hr3-113',values=[3.,None,.7])]
        self.assertEqual(m.family_population(rows,protected()),old.family_population(rows,protected()))
        a=m.fit_adapter(rows);b=old.fit_adapter(rows)
        for key in a:
            if key!='version':self.assertEqual(a[key],b[key])
        ar,ax=m.transform(rows,a);br,bx=old.transform(rows,b);np.testing.assert_array_equal(ar,br);np.testing.assert_array_equal(ax.toarray(),bx.toarray())
        self.assertEqual(ax.shape[1],8);self.assertIs(m.solver,old.solver);self.assertEqual(m.ARMS,old.ARMS)
if __name__=='__main__':unittest.main()
