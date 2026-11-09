import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import numpy as np
from scripts import official_context_diagnostic_v1 as run


def row(bid='hr1-113', congress=113, context=None):
    start=1789+2*(congress-1)
    return {'bill_id':bid,'congress':congress,'cutoff':f'{start}-07-01','congress_end':f'{start+2}-01-03',
            'anchor':[0.,180/730,1/30,180/730,0.,0.],'stage':0,'context':context or [1.,2.,.5],
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
        self.assertEqual(raw.shape,(1,12));self.assertEqual(raw[0,6],2.)
        self.assertEqual(raw[0,9:].tolist(),[1.,0.,0.]);self.assertEqual(adapter,before)
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


class OrderingTests(unittest.TestCase):
    def test_feature_seal_before_labels_predictions_before_metrics_two_fit_calls(self):
        with tempfile.TemporaryDirectory() as temp:
            base=Path(temp)/'data';source=base/'source';out=base/'result'
            (source/'features').mkdir(parents=True);(source/'sources').mkdir()
            rows=[row(),row('hr2-113'),row('hr1-117',117),row('hr1-118',118)]
            cases=[{'bill_id':r['bill_id'],'congress':r['congress'],'bill_type':'hr','bill_number':1 if r['bill_id']!='hr2-113' else 2} for r in rows]
            run.save(source/'registration.json',{'inputs':{},'selected':cases,'protected':protected()})
            run.save(source/'result.json',{'labels_read':False,'model_fits':0,'selected':4,'dispositions':{'features_saved':4}});run.save(source/'population-ledger.json',[{'bill_id':r['bill_id'],'disposition':'features_saved'} for r in rows])
            lookup={r['bill_id']:r for r in rows}
            for r in rows:
                path=source/'sources'/(r['bill_id']+'.xml');path.write_bytes(b'fixture')
                run.save(source/'sources'/(r['bill_id']+'-receipt.json'),{'status':200,'sha256':run.sha(path)})
                run.save(source/'features'/(r['bill_id']+'.json'),dict(r,source_sha256=run.sha(path)))
            def label(raw,case,cutoff):
                self.assertTrue((out/'feature-population.json').exists())
                r=lookup[case['bill_id']]
                return {'bill_id':r['bill_id'],'y':int(r['bill_id']=='hr1-113'),'reason':'proxy','label_matured_at':r['congress_end']}
            widths=[]
            def fit(X,y):
                self.assertTrue((out/'fit-inputs.json').exists());self.assertTrue((out/'label-counts.json').exists())
                widths.append(X.shape[1]);return {'accepted':True,'parameters':[0.]*(X.shape[1]+1)}
            original_metric=run.metric
            def metric(p,y):
                self.assertTrue((out/'probabilities.json').exists());return original_metric(p,y)
            with patch.object(run.feature_api,'extract_features',side_effect=lambda raw,case:lookup[case['bill_id']]),patch.object(run.feature_api,'resolve_outcome',side_effect=label),patch.object(run.solver,'fit',side_effect=fit),patch.object(run,'metric',side_effect=metric),patch.object(run,'context_bootstrap',return_value={}):
                run.run(source,out)
            self.assertEqual(widths,[6,12]);self.assertEqual(json.loads((out/'result.json').read_text())['fits_started'],2)

if __name__=='__main__':unittest.main()
