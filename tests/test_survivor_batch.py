import copy,tempfile,unittest
from pathlib import Path
from engine.survivor_batch import select,save

class SurvivorBatchTests(unittest.TestCase):
    def row(self,bid,related=None,y=0,exclusion=None,title=None):
        return dict(bill_id=bid,related=related or [],title=title or bid,versions=[{}],exclusion=exclusion,y=y)
    def test_keeps_all_eligible_without_outcome_enrichment(self):
        rows=[self.row('a'),self.row('b',y=1),self.row('c')];selected,excluded=select(rows,[],[]);self.assertEqual([r['bill_id'] for r in selected],['a','b','c']);self.assertEqual(excluded,[])
        flipped=copy.deepcopy(rows)
        for row in flipped:row['y']=1-row['y']
        self.assertEqual([r['bill_id'] for r in select(flipped,[],[])[0]],['a','b','c'])
    def test_transitive_prior_family_overlap_is_removed(self):
        old=[self.row('old',['bridge'])];rows=[self.row('new',['bridge']),self.row('safe')]
        self.assertEqual([r['bill_id'] for r in select(rows,[],old)[0]],['safe'])
    def test_training_overlap_is_removed_without_refit(self):
        training=[self.row('train')];before=copy.deepcopy(training);chosen,_=select([self.row('new',['train'])],training,[]);self.assertEqual(chosen,[]);self.assertEqual(training,before)
    def test_first_family_member_chosen_in_registered_order(self):
        rows=[self.row('b',['a']),self.row('a',y=1)];chosen,excluded=select(rows,[],[]);self.assertEqual(chosen[0]['bill_id'],'b');self.assertEqual(excluded[0]['reason'],'Duplicate selected family')
    def test_source_eligibility_exclusions_preserved(self):
        chosen,excluded=select([self.row('a',exclusion='late')],[],[]);self.assertEqual(chosen,[]);self.assertEqual(excluded,[dict(bill_id='a',reason='late')])
    def test_frozen_artifacts_reject_changed_values(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);save(p,'x.json',{'a':1,'b':2});save(p,'x.json',{'b':2,'a':1})
            with self.assertRaises(AssertionError):save(p,'x.json',{'a':2})
