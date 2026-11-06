import copy
import hashlib
import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from decimal import Decimal, localcontext
from engine import paper_evaluation as p
from engine.store import digest, congress_end


class PaperEvaluationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root/'proof').write_bytes(b'synthetic evidence, never official')
        self.source = {'path':'proof', 'sha256':hashlib.sha256(b'synthetic evidence, never official').hexdigest(), 'url':'fixture://proof'}
        self.training = [self.row(117,i+1, i%4) for i in range(24)]
        for i,r in enumerate(self.training):
            r['label'] = self.outcome(r,int(i%5==0))
        self.cases = [self.row(120,i+1,i%4) for i in range(8)]
        self.labels = [self.outcome(r,int(i%3==0)) for i,r in enumerate(self.cases)]
        base = {'weights':[-2.,.4,.1,.1,.1,.1,.1], 'means':[0.]*6, 'scales':[1.]*6}
        self.models = {'survivor':{'artifact':base,'training':self.training},
                       'challenger':{'artifact':{'model':{'base':base,'calibration':{'intercept':.2,'slope':1.2}}},'training':self.training}}
        self.spec = dict(target=p.TARGET, feature_version=p.FEATURES, mode='synthetic', periods=[120],
                         candidates=[r['bill_id'] for r in self.cases], paper_protocol_sha256='fixture',
                         baseline_training_hash=digest(self.training),
                         models={k:dict(artifact_hash=digest(v['artifact']),training_hash=digest(v['training'])) for k,v in self.models.items()})
        self.reg = p.register(self.spec,self.root/'registration.json')

    def review(self, row):
        row['review'] = dict(subject_hash=digest(row),decision='pass',reviewer='synthetic fixture',evidence=[self.source])
        return row

    def row(self,c,i,stage):
        intro = datetime(1787+2*c,1,4,23,59,59,tzinfo=timezone.utc)
        return self.review(dict(bill_id=f'{c}-hr{i}',congress=c,type='hr',target=p.TARGET,feature_version=p.FEATURES,
            dataset='demo',introduced_at=intro.isoformat(),cutoff=(intro+timedelta(days=180)).isoformat(),family_id=f'f{c}-{i}',at_risk=True,
            x=[stage/4,180/730,.1,.1,0,.1],stage=stage,sources=[self.source],
            features_available_at=intro.isoformat(),features_effective_at=intro.isoformat()))

    def outcome(self,r,y):
        effective = (datetime.fromisoformat(r['cutoff'])+timedelta(days=2)).isoformat() if y else congress_end(r['congress'])
        return self.review(dict(bill_id=r['bill_id'],target=p.TARGET,value=y,effective_at=effective,
            available_at=effective,complete_coverage=True,coverage_through=congress_end(r['congress']),sources=[self.source]))

    def prepare(self):
        return p.prepare(self.reg,self.cases,[],self.models,self.training,self.root)

    def test_exact_replay_and_independent_decimal_arithmetic(self):
        prepared=self.prepare()
        result=p.evaluate(self.reg,prepared,self.labels,self.root)
        self.assertEqual(result,p.evaluate(self.reg,self.prepare(),self.labels,self.root))
        report=p.unseal(result)['periods']['120']
        with localcontext() as ctx:
            ctx.prec=45
            def dec(value):return Decimal(str(value))
            def logistic(z):return 1/(1+(-max(dec(-35),min(dec(35),z))).exp())
            def probability(artifact,x):
                z=dec(artifact['weights'][0])
                for j in range(6):
                    z+=dec(artifact['weights'][j+1])*(dec(x[j])-dec(artifact['means'][j]))/dec(artifact['scales'][j])
                return logistic(z)
            for row,pair in zip(self.cases,p.unseal(prepared)['predictions']):
                original=probability(self.models['survivor']['artifact'],row['x'])
                candidate=self.models['challenger']['artifact']['model']
                raw=probability(candidate['base'],row['x'])
                adjusted=logistic(dec(candidate['calibration']['intercept'])+dec(candidate['calibration']['slope'])*(raw/(1-raw)).ln())
                self.assertAlmostEqual(float(original),pair['probabilities']['survivor'],places=14)
                self.assertAlmostEqual(float(adjusted),pair['probabilities']['challenger'],places=14)
            for name in p.NAMES:
                probs=[Decimal(str(r['probabilities'][name])) for r in p.unseal(prepared)['predictions']]
                ys=[Decimal(r['value']) for r in self.labels]
                b=sum((x-y)**2 for x,y in zip(probs,ys))/len(ys)
                l=-sum(y*x.ln()+(1-y)*(1-x).ln() for x,y in zip(probs,ys))/len(ys)
                self.assertAlmostEqual(float(b),report[name]['brier'],places=14)
                self.assertAlmostEqual(float(l),report[name]['log_loss'],places=14)
                bins=report[name]['calibration']
                self.assertEqual(sum(x['n'] for x in bins),len(ys))
                self.assertAlmostEqual(report[name]['brier_skill_vs_rate'],1-float(b)/report['rate']['brier'],places=14)
        rate=(5+1)/(24+2)
        self.assertEqual(p.unseal(prepared)['rate'],rate)
        self.assertEqual(p.unseal(prepared)['stage_rates']['0'],(2+5*rate)/(6+5))

    def test_immutable_files_and_tamper(self):
        with self.assertRaises(FileExistsError):p.save(self.root/'registration.json',self.reg)
        corrupt=copy.deepcopy(self.reg);corrupt['body']['spec']['periods']=[118]
        with self.assertRaisesRegex(ValueError,'hash'):p.unseal(corrupt)

    def test_duplicate_missing_extra_labels(self):
        prepared=self.prepare()
        for labels in (self.labels+[self.labels[0]],self.labels[:-1],self.labels+[self.outcome(self.row(120,99,0),0)]):
            with self.assertRaises(ValueError):p.evaluate(self.reg,prepared,labels,self.root)

    def test_candidate_integrity_and_label_separation(self):
        self.cases.append(self.cases[0])
        with self.assertRaisesRegex(ValueError,'Duplicate'):self.prepare()
        self.cases.pop();self.cases[0]['y']=0
        with self.assertRaisesRegex(ValueError,'separate'):self.prepare()

    def test_missing_corrupt_sources(self):
        (self.root/'proof').write_text('corrupt')
        with self.assertRaisesRegex(ValueError,'Source hash'):self.prepare()
        (self.root/'proof').unlink()
        with self.assertRaisesRegex(ValueError,'Missing source'):self.prepare()

    def test_future_features_and_wrong_age(self):
        self.cases[0]['features_available_at']='2030-01-01T00:00:00Z'
        with self.assertRaisesRegex(ValueError,'Future'):self.prepare()
        self.cases[0]=self.row(120,1,0);self.cases[0]['cutoff']='2027-09-01T00:00:00Z'
        with self.assertRaisesRegex(ValueError,'checkpoint'):self.prepare()

    def test_family_and_review_gates(self):
        self.cases[0]['review']['decision']='pending'
        with self.assertRaisesRegex(ValueError,'review'):self.prepare()
        r=self.row(120,1,0);r.pop('review');r['family_id']=self.training[0]['family_id'];self.cases[0]=self.review(r)
        with self.assertRaisesRegex(ValueError,'overlap'):self.prepare()

    def test_model_changes_and_invalid_dimensions(self):
        self.models['survivor']['artifact']['weights'][0]=-1
        with self.assertRaisesRegex(ValueError,'artifact'):self.prepare()

    def test_negative_coverage_and_boundary_positive(self):
        for index in (0,1):
            labels=copy.deepcopy(self.labels)
            if index==1:labels[index]['complete_coverage']=False
            else:labels[index]['effective_at']=self.cases[index]['cutoff']
            with self.assertRaises(ValueError):p.evaluate(self.reg,self.prepare(),labels,self.root)

    def test_temporal_offsets_are_normalized(self):
        r=self.cases[0];r.pop('review')
        instant=datetime.fromisoformat(r['cutoff']).astimezone(timezone(timedelta(hours=-4)))
        r['cutoff']=instant.isoformat();self.review(r)
        self.prepare()

    def test_prospective_and_historical_cannot_be_mislabeled(self):
        spec=copy.deepcopy(self.spec);spec['mode']='historical'
        with self.assertRaisesRegex(ValueError,'historical'):p.register(spec,self.root/'bad.json')
        spec['mode']='prospective';reg=p.register(spec,self.root/'future.json')
        with self.assertRaisesRegex(ValueError,'Dataset'):p.prepare(reg,self.cases,[],self.models,self.training,self.root)
        for row in self.cases+self.training:
            row.pop('review');lab=row.pop('label',None);row['dataset']='official';self.review(row)
            if lab:row['label']=lab
        spec['baseline_training_hash']=digest(self.training)
        for item in spec['models'].values():item['training_hash']=digest(self.training)
        reg=p.register(spec,self.root/'official.json')
        prepared=p.prepare(reg,self.cases,[],self.models,self.training,self.root)
        with self.assertRaisesRegex(ValueError,'custodian'):p.evaluate(reg,prepared,self.labels,self.root)
        review=dict(subject_hash=prepared['hash'],decision='pass',reviewer='fixture',evidence=[self.source],independence_confirmed=True)
        with self.assertRaisesRegex(ValueError,'ledger'):p.evaluate(reg,prepared,self.labels,self.root,review)

    def test_training_time_gate_even_with_registered_membership(self):
        row=self.training[0]
        label=row['label'];label.pop('review');label['available_at']='2030-01-01T00:00:00Z';self.review(label)
        self.spec['baseline_training_hash']=digest(self.training)
        for item in self.spec['models'].values():item['training_hash']=digest(self.training)
        self.reg=p.register(self.spec,self.root/'late-label.json')
        with self.assertRaisesRegex(ValueError,'knowable'):self.prepare()

    def test_bad_dimensions_do_not_silently_zip(self):
        self.models['survivor']['artifact']['weights'].pop()
        self.spec['models']['survivor']['artifact_hash']=digest(self.models['survivor']['artifact'])
        self.spec['models']['challenger']['artifact_hash']=digest(self.models['challenger']['artifact'])
        self.reg=p.register(self.spec,self.root/'short-model.json')
        with self.assertRaisesRegex(ValueError,'dimensions'):self.prepare()

    def test_full_candidate_disposition_and_code_lock(self):
        excluded=self.cases.pop()
        disposition=self.review(dict(bill_id=excluded['bill_id'],reason='synthetic missing evidence'))
        prepared=p.prepare(self.reg,self.cases,[disposition],self.models,self.training,self.root)
        self.assertEqual(len(p.unseal(prepared)['predictions']),7)
        with self.assertRaisesRegex(ValueError,'disposition'):self.prepare()
        body=copy.deepcopy(p.unseal(self.reg));body['code_hashes']['model.py']='changed'
        with self.assertRaisesRegex(ValueError,'implementation'):
            p.prepare(p.seal(body),self.cases,[disposition],self.models,self.training,self.root)

    def test_nan_and_bad_probabilities(self):
        for probability in (float('nan'),float('inf'),-1,2):
            with self.assertRaises(ValueError):p.metrics([probability],[0])
        with self.assertRaises(ValueError):p.seal({'x':float('nan')})
        self.assertEqual(p.metrics([0,1],[0,1])['brier'],0)
        self.assertEqual(sum(b['n'] for b in p.metrics([0,1],[0,1])['calibration']),2)


if __name__=='__main__':unittest.main()
