"""Optional NumPy research runner; same GD objective, training-only stopping."""
import json, math
import numpy as np
from engine.store import ROOT, digest, now, Store
from engine.research_lease import lease
from engine.model import predict, score
from engine.three_model_experiment import fit_calibration, calibrate
from engine.survivor_batch import save
from scripts.cross_congress_evaluate import D as SOURCE, load_rows
from scripts.stage_regularization_experiment import D as PREVIOUS
from scripts.diagnose_transfer import SURVIVOR_HASH
from scripts.granular_transfer_audit import objective_gradient

D=ROOT/'data/research-runs/convergence-einsum-20261105'
OWNER='convergence-20261105'
TOL=1e-6
CAP=20000


def fit_converged(rows,l2,tolerance=TOL,cap=CAP):
    n=len(rows);width=len(rows[0]['x'])
    means=[sum(r['x'][j] for r in rows)/n for j in range(width)]
    scales=[max(.1,math.sqrt(sum((r['x'][j]-means[j])**2 for r in rows)/n)) for j in range(width)]
    x=np.array([[1.]+[(r['x'][j]-means[j])/scales[j] for j in range(width)] for r in rows],dtype=np.float64)
    y=np.array([r['y'] for r in rows],dtype=np.float64)
    rate=(sum(r['y'] for r in rows)+1)/(n+2)
    weights=np.array([math.log(rate/(1-rate))]+[0.]*width)
    trace=[];snapshot=None
    for step in range(cap+1):
        p=1/(1+np.exp(-np.clip(np.einsum('ij,j->i',x,weights,optimize=False),-35,35)))
        gradient=np.einsum('ij,i->j',x,p-y,optimize=False)/n+np.r_[0.,l2*weights[1:]]
        assert np.all(np.isfinite(gradient)) and np.all(np.isfinite(weights))
        norm=float(np.max(np.abs(gradient)))
        if step in (300,1500,5000,10000,cap):trace.append(dict(iterations=step,max_absolute_gradient=norm))
        if step==300:snapshot=dict(weights=weights.tolist(),means=means,scales=scales,l2=l2,iterations=step)
        if step>=300 and norm<=tolerance:break
        if step<cap:weights-=.12*gradient
    model=dict(weights=weights.tolist(),means=means,scales=scales,l2=l2,iterations=step)
    return model,dict(converged=norm<=tolerance,max_absolute_gradient=norm,iterations=step,trace=trace),snapshot


def trained(core,calibration,l2):
    model,diagnostics,snapshot=fit_converged(core,l2)
    adjustment=fit_calibration([predict(model,r['x']) for r in calibration],[r['y'] for r in calibration])
    direct=objective_gradient(model,core)
    assert abs(direct['max_absolute_gradient']-diagnostics['max_absolute_gradient'])<1e-12
    return dict(base=model,calibration=adjustment),diagnostics,snapshot


def run():
    D.mkdir(parents=True,exist_ok=True)
    previous=json.loads((PREVIOUS/'result.json').read_text())
    assert digest({k:v for k,v in previous.items() if k!='hash'})==previous['hash']
    spec=dict(folds=[115,116,117],penalties=[.2,.05],features='unchanged linear stage, six inputs',
              stopping=dict(minimum_iterations=300,maximum_iterations=CAP,max_absolute_penalized_gradient=TOL,learning_rate=.12),
              calibration='Unchanged 2000-iteration calibration procedure, same disjoint rows; convergence claim applies to base only',
              membership='Identical prior core/calibration/test rows; 300-step NumPy/scalar probability equivalence required within 1e-12',
              selection='Weaker L2 must improve Brier and not worsen log loss in all three folds; both fits must reach gradient tolerance in all folds',
              freeze='If selection passes, fit weaker L2 on earlier campaign final-training core/calibration split. Freeze only if its base reaches tolerance; no 118 outcomes used in final fitting.',
              source_hash=previous['hash'],arithmetic='float64 einsum without BLAS; finite weights/gradient each step',numpy=np.__version__,exposure='Previously exposed development outcomes; no independent validation',release_eligible=False)
    if (D/'protocol.json').exists():assert json.loads((D/'protocol.json').read_text())['spec']==spec
    else:save(D,'protocol.json',dict(spec=spec,hash=digest(spec),registered_at=now()))
    lookup={r['bill_id']:r for r in load_rows()};folds=[]
    for prior in previous['folds']:
        core=[lookup[i] for i in prior['core_ids']];cal=[lookup[i] for i in prior['calibration_ids']]
        testids={r['bill_id'] for r in prior['predictions']};families={r['family_id'] for r in prior['predictions']}
        from engine import cohort
        grouped=cohort.family_groups(list(lookup.values()))
        assert not {grouped[r['bill_id']] for r in core+cal}&families
        assert not set(prior['core_ids'])&set(prior['calibration_ids'])
        assert not testids&set(prior['core_ids']+prior['calibration_ids'])
        assert max(r['label_available_at'] for r in core+cal)<min(lookup[i]['cutoff'] for i in testids)
        models={};diagnostics={};pairs=[dict(r) for r in prior['predictions']]
        for name,l2 in [('control',.2),('weaker_l2',.05)]:
            model,diag,snapshot=trained(core,cal,l2)
            for r in prior['predictions']:assert abs(predict(snapshot,r['x'])-r[name+'_raw'])<1e-12
            models[name]=model;diagnostics[name]=diag
            for r in pairs:
                r[name+'_raw']=predict(model['base'],r['x']);r[name]=calibrate(model['calibration'],r[name+'_raw'])
        metrics={name:score([r[name] for r in pairs],[r['outcome'] for r in pairs]) for name in ('control','weaker_l2','control_raw','weaker_l2_raw')}
        folds.append(dict(congress=prior['congress'],core_ids=prior['core_ids'],calibration_ids=prior['calibration_ids'],models=models,diagnostics=diagnostics,metrics=metrics,predictions=pairs))
        print(json.dumps(dict(congress=prior['congress'],diagnostics=diagnostics,brier={k:metrics[k]['brier'] for k in models})),flush=True)
    passed=all(all(d['converged'] for d in f['diagnostics'].values()) and f['metrics']['weaker_l2']['brier']<f['metrics']['control']['brier'] and f['metrics']['weaker_l2']['log_loss']<=f['metrics']['control']['log_loss'] for f in folds)
    gain=sum(1-f['metrics']['weaker_l2']['brier']/f['metrics']['control']['brier'] for f in folds)/len(folds)
    result=dict(title='Training convergence and fixed weaker-penalty candidate',protocol_hash=digest(spec),folds=folds,development_gate_passed=passed,mean_relative_brier_gain=gain,release_eligible=False,independent_validation=False)
    result['hash']=digest(result)
    if (D/'result.json').exists():assert json.loads((D/'result.json').read_text())==result
    else:save(D,'result.json',result)
    if passed:
        train=json.loads((SOURCE/'final-training.json').read_text());oldlock=json.loads((SOURCE/'challenger-lock.json').read_text())
        assert digest(train)==oldlock['training_rows_hash']
        byid={r['bill_id']:r for r in train};core=[byid[i] for i in oldlock['artifact']['core_ids']];cal=[byid[i] for i in oldlock['artifact']['calibration_ids']]
        assert not {r['family_id'] for r in core}&{r['family_id'] for r in cal}
        model,diag,_=trained(core,cal,.05)
        if diag['converged']:
            priorlock=json.loads((D/'candidate-lock.json').read_text()) if (D/'candidate-lock.json').exists() else None
            lock=dict(model=model,diagnostics=diag,core_ids=[r['bill_id'] for r in core],calibration_ids=[r['bill_id'] for r in cal],training_hash=digest(train),latest_training_label=max(r['label_available_at'] for r in train),locked_at=priorlock['locked_at'] if priorlock else now(),protocol_hash=digest(spec),development_result_hash=result['hash'],release_eligible=False,independent_validation=False,scope='Research-only candidate; trained on 113–117; not deployed or validated against survivor on fresh evidence')
            lock['hash']=digest(lock)
            if priorlock:assert priorlock==lock
            else:save(D,'candidate-lock.json',lock)
        else:save(D,'freeze-blocked.json',diag)
    assert digest(json.loads((ROOT/'data/research-runs/survivor1000-20261105/artifact.json').read_text()))==SURVIVOR_HASH
    print(json.dumps(dict(passed=passed,mean_relative_brier_gain=gain,candidate_frozen=(D/'candidate-lock.json').exists())),flush=True)


if __name__=='__main__':
    store=Store()
    try:
        if not lease(store,'acquire',OWNER)['granted']:raise RuntimeError('Lease unavailable')
        try:run()
        finally:lease(store,'release',OWNER)
    finally:store.close()
