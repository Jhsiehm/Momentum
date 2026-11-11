import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import numpy as np
from scripts import action_context_diagnostic_v2 as run


def row(bid='hr1-113', congress=113, context=None):
    start=1789+2*(congress-1)
    return {'bill_id':bid,'congress':congress,'cutoff':f'{start}-07-01','congress_end':f'{start+2}-01-03',
            'anchor':[0.,0.],'stage':0,'context':context or [1.,2.,.5],
            'missing':[int(v is None) for v in (context or [1.,2.,.5])],'feature_errors':[], 'related':[],'role':'train' if congress<=116 else str(congress)}


def protected():
    return {'known_family_assignments':{},'excluded_ids':[],'banned_family_ids':[]}


class AdapterTests(unittest.TestCase):
    def test_training_median_scaler_and_heldout(self):
        train=[row(context=[1.,2.,.5]),row('hr2-113',context=[3.,None,.7])]
        adapter=run.fit_adapter(train);before=copy.deepcopy(adapter)
        self.assertEqual(adapter['medians'],[2.,2.,.6])
        heldout=row('hr1-117',117,[None,1000.,.9])
        raw,X=run.transform([heldout],adapter)
        self.assertEqual(raw.shape,(1,8));self.assertEqual(raw[0,2],2.)
        self.assertEqual(raw[0,5:].tolist(),[1.,0.,0.]);self.assertEqual(adapter,before)
        self.assertTrue(np.isfinite(X.data).all())
    def test_no_allmissing_or_heldout_fit(self):
        with self.assertRaises(ValueError):run.fit_adapter([row(context=[None,1.,2.])])
        with self.assertRaises(ValueError):run.fit_adapter([row('hr1-117',117)])
    def test_invalid_flags_and_stage(self):
        r=row();r['missing'][0]=1
        with self.assertRaises(ValueError):run.fit_adapter([r])
        r=row();r['stage']=1
        with self.assertRaises(ValueError):run.fit_adapter([r])


class FamilyTests(unittest.TestCase):
    def test_population_changes_source_only(self):
        old={'rows':[{'bill_id':'a','family_id':'f','role':'train'}],'exclusions':[]}
        new={'rows':[{'bill_id':'b','family_id':'f','role':'117'},{'bill_id':'c','family_id':'g','role':'118'}],'exclusions':[]}
        result=run.population_changes(old,new)
        self.assertEqual(result['added_ids'],['b','c']);self.assertEqual(result['removed_ids'],['a'])
        self.assertEqual(result['family_changes'][0]['disposition'],'representative_or_role_changed')
        self.assertFalse(result['labels_used'])

    def test_family_selection_unchanged_from_v1(self):
        from scripts import official_context_diagnostic_v1 as original
        rows=[row('hr'+str(i)+'-113') for i in range(1,8)]
        for r in rows:r['related']=['hjres9-114']
        old_rows=copy.deepcopy(rows)
        for r in old_rows:r['anchor']=[r['stage']/4,180/730,1/30,180/730,0.,0.]
        new=run.family_population(rows,protected());old=original.family_population(old_rows,protected())
        self.assertEqual([r['bill_id'] for r in new['rows']],[r['bill_id'] for r in old['rows']])
        self.assertEqual(new['exclusions'],old['exclusions'])

    def test_external_node_connects_roles_later_wins(self):
        rows=[row(),row('s1-117',117),row('s2-118',118)]
        for r in rows:r['related']=['hjres9-114']
        pop=run.family_population(rows,protected())
        self.assertEqual([r['bill_id'] for r in pop['rows']],['s2-118'])
        self.assertEqual(len(pop['exclusions']),2)
    def test_ineligible_later_still_excludes_train(self):
        a,b=row(),row('s1-117',117);a['related']=['s1-117'];b['anchor']=None
        self.assertEqual(run.family_population([a,b],protected())['rows'],[])
    def test_known_family_and_banned_external(self):
        p=protected();p['known_family_assignments']={'hr1-113':'f','s1-119':'f'};p['excluded_ids']=['s1-119']
        self.assertEqual(run.family_population([row()],p)['rows'],[])
    def test_deterministic_representative_and_duplicate_guard(self):
        a,b=row(),row('hr2-113');a['related']=['hr2-113']
        self.assertEqual(run.family_population([a,b],protected())['rows'],run.family_population([b,a],protected())['rows'])
        with self.assertRaises(ValueError):run.family_population([a,a],protected())


class OutcomeTests(unittest.TestCase):
    def test_maturity_and_class_checks(self):
        rows=[row(),row('hr2-113'),row('hr1-117',117),row('hr1-118',118)]
        labels={r['bill_id']:{'bill_id':r['bill_id'],'y':int(i==0),'reason':'proxy','label_matured_at':r['congress_end']} for i,r in enumerate(rows)}
        kept,excluded=run.resolve_population({'rows':rows},labels)
        self.assertEqual(len(kept),4);self.assertEqual(excluded,[])
        labels['hr1-113']['label_matured_at']='2024-01-01'
        with self.assertRaises(ValueError):run.resolve_population({'rows':rows},labels)
    def test_unknown_never_replaced(self):
        r=row();labels={r['bill_id']:{'bill_id':r['bill_id'],'y':None,'reason':'unknown'}}
        with self.assertRaises(ValueError):run.resolve_population({'rows':[r]},labels)


class DeltaTests(unittest.TestCase):
    def fixture(self):
        before={bid:{'bill_id':bid,'y':None,'reason':'old'} for bid in ('a','b')}
        before['c']={'bill_id':'c','y':0,'reason':'negative'}
        cases=[{'bill_id':bid,'all_problem_dates_match_concordant':bid=='a','concordant_date_count':1 if bid=='a' else 0,'concordant_numbers_equal_law_list':bid=='a','public_law_identity_count':1,'concordant_assertion_count':1 if bid=='a' else 0} for bid in ('a','b')]
        rows=[{'bill_id':bid,'cutoff':'2020-01-01','congress_end':'2021-01-03'} for bid in before]
        return before,copy.deepcopy(before),cases,rows
    def test_only_corroborated_positive_and_reason_only_unknown(self):
        before,after,cases,rows=self.fixture()
        after['a'].update(y=1,enacted_at='2020-06-01',label_matured_at='2020-06-01',reason='corroborated')
        after['b']['reason']='uncorroborated_signing'
        result=run.label_delta(before,after,cases,rows)
        self.assertEqual(result['violations'],[]);self.assertEqual(result['label_changes'],1)
        self.assertEqual(len(result['rows']),3);self.assertTrue(result['rows'][1]['record_changed'])
    def test_no_negative_flip(self):
        before,after,cases,rows=self.fixture();after['c']['y']=1
        self.assertTrue(run.label_delta(before,after,cases,rows)['violations'])
    def test_uncorroborated_positive_rejected(self):
        before,after,cases,rows=self.fixture();after['b'].update(y=1,enacted_at='2020-06-01',label_matured_at='2020-06-01')
        self.assertTrue(run.label_delta(before,after,cases,rows)['violations'])
    def test_corroborated_outside_risk_stays_unknown(self):
        before,after,cases,rows=self.fixture();after['a']['reason']='already_enacted'
        self.assertEqual(run.label_delta(before,after,cases,rows)['violations'],[])
    def test_horizon_enforced(self):
        for when in ('2020-01-01','2021-01-03'):
            before,after,cases,rows=self.fixture();after['a'].update(y=1,enacted_at=when,label_matured_at=when)
            self.assertTrue(run.label_delta(before,after,cases,rows)['violations'])
    def test_population_mismatch_and_contract_duplicate(self):
        before,after,cases,rows=self.fixture();after.pop('a')
        with self.assertRaises(ValueError):run.label_delta(before,after,cases,rows)
        before,after,cases,rows=self.fixture()
        with self.assertRaises(ValueError):run.label_delta(before,after,cases+cases[:1],rows)

if __name__=='__main__':unittest.main()
