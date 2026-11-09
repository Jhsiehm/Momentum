import copy
import json
from pathlib import Path
import tempfile
from unittest.mock import patch
import unittest
import numpy as np
from scripts import official_context_diagnostic_v2 as m

def row(bid='hr1-113',c=113,values=None):
    values=[1.,2.,.5] if values is None else values
    year=1789+2*(c-1)
    return dict(bill_id=bid,congress=c,cutoff=f'{year}-07-02',congress_end=f'{year+2}-01-03',anchor=[0.,180/730,1/30,180/730,float(bid.startswith('s')),0.],stage=0,context=values,missing=[int(v is None) for v in values],related=[],feature_errors=[],role='train' if c<=116 else str(c))
def protected():return dict(known_family_assignments={},excluded_ids=[],banned_family_ids=[])

class IndependentFitV2Tests(unittest.TestCase):
    def test_training_only_median_and_population_scaling(self):
        rows=[row(values=[1.,2.,.2]),row('hr2-113',values=[3.,None,.8]),row('hr3-113',values=[None,8.,.5])]
        a=m.fit_adapter(rows);self.assertEqual(a['medians'],[2.,5.,.5])
        raw=m.raw_matrix(rows,a['medians']);np.testing.assert_allclose(a['means'],raw.mean(axis=0));np.testing.assert_allclose(a['scales'],np.maximum(raw.std(axis=0,ddof=0),.1))
        original=copy.deepcopy(a);held=row('hr1-118',118,[None,900.,None]);matrix,_=m.transform([held],a)
        self.assertEqual(matrix[0,6:].tolist(),[2.,900.,.5,1.,0.,1.]);self.assertEqual(a,original)
    def test_entirely_missing_training_stops(self):
        with self.assertRaises(ValueError):m.fit_adapter([row(values=[None,2.,.5])])
    def test_external_bridge_to_protected_family_blocks(self):
        a=row();a['related']=['s500-119'];p=protected();p['known_family_assignments']={'s500-119':'f','s501-119':'f'};p['excluded_ids']=['s501-119']
        result=m.family_population([a],p);self.assertEqual(result['rows'],[]);self.assertEqual(result['exclusions'][0]['reason'],'protected_or_exposed_family')
    def test_later_ineligible_family_blocks_earlier(self):
        a=row();b=row('s1-118',118);a['related']=['s1-118'];b['anchor']=None
        result=m.family_population([a,b],protected());self.assertEqual(result['rows'],[])
    def test_boolean_outcome_rejected(self):
        rows=[row(),row('hr2-113'),row('hr1-117',117),row('hr1-118',118)]
        labels={r['bill_id']:dict(bill_id=r['bill_id'],y=int(i==0),reason='fixture',label_matured_at=r['congress_end']) for i,r in enumerate(rows)}
        labels[rows[0]['bill_id']]['y']=True
        with self.assertRaises(ValueError):m.resolve_population({'rows':rows},labels)
    def test_same_date_training_maturity_not_prior(self):
        rows=[row(),row('hr2-113'),row('hr1-117',117),row('hr1-118',118)]
        labels={r['bill_id']:dict(bill_id=r['bill_id'],y=int(i==0),reason='fixture',label_matured_at=r['congress_end']) for i,r in enumerate(rows)}
        labels[rows[0]['bill_id']]['label_matured_at']=rows[2]['cutoff']
        with self.assertRaises(ValueError):m.resolve_population({'rows':rows},labels)
    def setup_source(self,base):
        source=base/'source';(source/'features').mkdir(parents=True);(source/'sources').mkdir()
        rows=[row(),row('hr2-113'),row('hr3-113'),row('hr1-117',117),row('hr1-118',118)]
        cases=[dict(bill_id=r['bill_id'],congress=r['congress'],bill_type='hr',bill_number=int(r['bill_id'].split('-')[0][2:])) for r in rows]
        m.save(source/'registration.json',dict(inputs={},selected=cases,protected=protected()))
        m.save(source/'result.json',dict(labels_read=False,model_fits=0,selected=5,dispositions={'features_saved':5}))
        m.save(source/'population-ledger.json',[dict(bill_id=r['bill_id'],disposition='features_saved') for r in rows])
        for r in rows:
            raw=source/'sources'/(r['bill_id']+'.xml');raw.write_bytes(b'fixture')
            m.save(source/'sources'/(r['bill_id']+'-receipt.json'),dict(status=200,sha256=m.sha(raw)))
            m.save(source/'features'/(r['bill_id']+'.json'),dict(r,source_sha256=m.sha(raw)))
        amendment=base/'features_v2';(amendment/'features').mkdir(parents=True)
        hashes={}
        for r in rows:
            name=r['bill_id']+'.json';(amendment/'features'/name).write_bytes((source/'features'/name).read_bytes());hashes[r['bill_id']]=m.sha(source/'sources'/(r['bill_id']+'.xml'))
        m.save(amendment/'registration.json',dict(original_acquisition=str(source),selected=cases,inputs={},source_hashes=hashes,network_requests=0,labels_read=False,model_fits=0))
        m.save(amendment/'result.json',dict(labels_read=False,model_fits=0,selected=5,dispositions={'features_saved':5}))
        m.save(amendment/'population-ledger.json',m.read(source/'population-ledger.json'));m.save(amendment/'changes.json',[])
        return source,{r['bill_id']:r for r in rows}
    def test_missing_feature_file_stops_before_labels(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp)/'data';source,rows=self.setup_source(base);(base/'features_v2/features/hr1-113.json').unlink()
            with patch.object(m.feature_api,'resolve_outcome') as labels:
                with self.assertRaisesRegex(ValueError,'Missing/extra feature'):m.run(source,base/'out',base/'features_v2')
                labels.assert_not_called()
    def test_fake_solver_acceptance_fails_recomputed_gradient(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp)/'data';source,rows=self.setup_source(base)
            def label(raw,case,cutoff):
                r=rows[case['bill_id']]
                return dict(bill_id=r['bill_id'],y=int(r['bill_id']=='hr1-113'),reason='proxy',label_matured_at=r['congress_end'])
            def fakefit(X,y):return dict(accepted=True,parameters=[0.]*(X.shape[1]+1))
            with patch.object(m.feature_api,'extract_features',side_effect=lambda raw,case:rows[case['bill_id']]),patch.object(m.feature_api,'resolve_outcome',side_effect=label),patch.object(m.solver,'fit',side_effect=fakefit) as fits:
                with self.assertRaises(ValueError):m.run(source,base/'out',base/'features_v2')
                self.assertEqual(fits.call_count,1)
            fitted=m.read(base/'out/anchor-fit.json');self.assertFalse(fitted['runner_verification']['accepted'])
            self.assertGreater(fitted['runner_verification']['gradient_infinity_norm'],1e-6)
            self.assertFalse((base/'out/probabilities.json').exists())
    def test_family_choice_salt_unchanged_from_v1(self):
        from scripts import official_context_diagnostic_v1 as old
        rows=[row('hr'+str(i)+'-113') for i in range(1,20)]
        for r in rows:r['related']=['s999-114']
        self.assertEqual(m.family_population(rows,protected()),old.family_population(rows,protected()))
    def test_changed_amendment_population_stops_before_labels(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp)/'data';source,rows=self.setup_source(base);path=base/'features_v2/registration.json';reg=m.read(path);reg['selected']=reg['selected'][1:];path.write_text(json.dumps(reg))
            with patch.object(m.feature_api,'resolve_outcome') as labels:
                with self.assertRaisesRegex(ValueError,'changed selected population'):m.run(source,base/'out',base/'features_v2')
                labels.assert_not_called()
if __name__=='__main__':unittest.main()
