import copy
import unittest
from scripts.mechanism_reference_v3 import QUESTIONS, apply_decisions, indexed


class ReferenceV3Tests(unittest.TestCase):
    def fixture(self):
        effect=dict(mechanism='deadline',operation='create',dimension='procedure',actor=None,target='report',conditions=None,quote='annually',start=0,end=8,rationale='Timing')
        bids={bid for bid,i in QUESTIONS}
        parent={'records':[{'bill_id':bid,'effects':[copy.deepcopy(effect) for _ in range(40)]} for bid in bids]}
        decisions=[];reviews=[]
        for bid,i in QUESTIONS:
            after=dict(effect,dimension='duration')
            decisions.append(dict(bill_id=bid,effect_index=i,before=effect,after=after,disposition='correct',rationale='Time window',evidence=[dict(start=0,end=8,quote='annually')]))
            reviews.append(dict(bill_id=bid,effect_index=i,disposition='agree',rationale='Reviewed timing',evidence=dict(start=0,end=8,quote='annually')))
        flags=dict(human_certified=False,historical_feature_eligible=False)
        return parent,dict(flags,decisions=decisions),dict(flags,decisions=reviews),{bid:{'text':'annually'} for bid in bids}

    def test_only_selected_effects_change_parent_untouched(self):
        parent,a,r,v=self.fixture();before=copy.deepcopy(parent);out,changes=apply_decisions(parent,a,r,v)
        self.assertEqual(parent,before);self.assertEqual(len(changes),8)
        for row in out['records']:
            for i,e in enumerate(row['effects']):self.assertEqual(e['dimension'],'duration' if (row['bill_id'],i) in QUESTIONS else 'procedure')

    def test_duplicate_missing_boolean_identity(self):
        _,a,_,_=self.fixture()
        for transform in (lambda x:x.pop(),lambda x:x.append(x[0]),lambda x:x[0].update(effect_index=True)):
            rows=copy.deepcopy(a['decisions']);transform(rows)
            with self.assertRaises(ValueError):indexed(rows)

    def test_peer_challenge_quote_or_before_tampering_blocks_export(self):
        for change in ('peer','quote','before','flags','uncertain'):
            parent,a,r,v=self.fixture()
            if change=='peer':r['decisions'][0]['disposition']='challenge'
            if change=='quote':a['decisions'][0]['after']['quote']='incorrect'
            if change=='before':a['decisions'][0]['before']=dict(a['decisions'][0]['before'],operation='remove')
            if change=='flags':a['human_certified']=True
            if change=='uncertain':a['decisions'][0]['disposition']='uncertain'
            with self.assertRaises(ValueError):apply_decisions(parent,a,r,v)
