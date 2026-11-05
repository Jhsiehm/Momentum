"""Arithmetic/source verifier separate from the experiment scoring implementation.
Run from repository root: python3 -m scripts.verify_three_model
"""
import hashlib
import json
import math
import random
from pathlib import Path
from engine.store import ROOT,digest
from engine.three_model_experiment import DEFAULT
from engine.survivor_batch import save


def verify(directory=DEFAULT):
    directory=Path(directory)
    load=lambda name:json.loads((directory/(name+'.json')).read_text())
    protocol=load('protocol');spec=protocol['spec'];result=load('result');models=load('models');acquisition=load('acquisition')
    assert digest(spec)==protocol['hash']==result['protocol_hash']
    assert digest({k:v for k,v in result.items() if k!='hash'})==result['hash']
    assert all(digest(load(name))==expected for name,expected in spec['hashes'].items())
    assert models['original']==json.loads((ROOT/'data/research-runs/survivor1000-20261105/artifact.json').read_text())
    rows=result['predictions'];ys=[r['outcome'] for r in rows]
    assert len(rows)==len({r['bill_id'] for r in rows})==len({r['family_id'] for r in rows})
    assert [r['bill_id'] for r in rows]==load('selection')['selected_ids']
    def sigmoid(z):return 1/(1+math.exp(-min(35,max(-35,z))))
    def direct(artifact,x):
        terms=[artifact['weights'][0]]+[w*(v-m)/s for w,v,m,s in zip(artifact['weights'][1:],x,artifact['means'],artifact['scales'])]
        return sigmoid(sum(terms))
    for row in rows:
        assert spec['label_available_at']<row['cutoff']
        p=direct(models['original'],row['input_features'])
        c=models['calibrated'];q=sigmoid(c['intercept']+c['slope']*math.log(p/(1-p)))
        for key,value in dict(original=p,calibrated=q,retrained=direct(models['retrained'],row['input_features'])).items():
            assert abs(value-row[key])<1e-14
    direct_metrics={}
    for key in models:
        ps=[row[key] for row in rows]
        brier=sum((p-y)**2 for p,y in zip(ps,ys))/len(rows)
        loss=-sum(y*math.log(max(1e-12,min(1-1e-12,p)))+(1-y)*math.log(1-max(1e-12,min(1-1e-12,p))) for p,y in zip(ps,ys))/len(rows)
        assert abs(brier-result['metrics'][key]['brier'])<1e-14
        assert abs(loss-result['metrics'][key]['log_loss'])<1e-14
        direct_metrics[key]=dict(brier=brier,log_loss=loss)
    for key in ('calibrated','retrained'):
        ordered=sorted(rows,key=lambda r:r['family_id'])
        differences=[(r[key]-r['outcome'])**2-(r['original']-r['outcome'])**2 for r in ordered]
        rng=random.Random(20261024)
        draws=sorted(sum(rng.choice(differences) for _ in differences)/len(differences) for _ in range(2000))
        interval=result['comparisons'][key]['interval']
        assert abs(draws[50]-interval['lower_95'])<1e-14
        assert abs(draws[1950]-interval['upper_95'])<1e-14
    for source in acquisition['sources']:
        raw=(directory/'sources'/(hashlib.sha256(source['url'].encode()).hexdigest()+'.raw')).read_bytes()
        assert len(raw)==source['bytes'] and hashlib.sha256(raw).hexdigest()==source['sha256']
    # Verify previously audited training-label availability, without changing it.
    previous=ROOT/'data/research-runs/expanded-experiments-20261105'
    frozen=json.loads((previous/'frozen-inputs.json').read_text())
    oldacq=json.loads((previous/'acquisition.json').read_text())
    training_ids={r['bill_id'] for r in load('training')}
    latest=max([frozen['label_available_at']]+[p['available_at'] for bid,p in oldacq['positive_proofs'].items() if bid in training_ids])
    assert latest==spec['label_available_at']
    assert load('training')==frozen['training'] and load('original_training')==frozen['original_training']
    report=dict(status='passed',result_hash=result['hash'],protocol_hash=protocol['hash'],verified_predictions=len(rows)*3,
        verified_sources=len(acquisition['sources']),training_label_latest=latest,direct_metrics=direct_metrics,
        checks=['Frozen hashes and original survivor identity','Separate direct probability/Brier/log-loss arithmetic','Separate paired-bootstrap arithmetic','Source bytes and SHA256','Training label-time evidence','Unique shared evaluation families'],
        human_certified=False,release_eligible=False)
    save(directory,'verification.json',report)
    print(json.dumps(report,indent=2))
    return report


if __name__=='__main__':verify()
