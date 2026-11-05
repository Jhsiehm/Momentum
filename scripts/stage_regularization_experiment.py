"""Fixed one-factor development experiments; no survivor modification."""
import json
from engine import cohort, learning
from engine.model import predict, score
from engine.store import ROOT, digest, now, Store
from engine.research_lease import lease
from engine.survivor_batch import save
from engine.three_model_experiment import calibrate, fit_calibration
from scripts.cross_congress_evaluate import D as SOURCE, load_rows, make_split
from scripts.diagnose_transfer import SURVIVOR_HASH
from scripts.granular_transfer_audit import objective_gradient

D=ROOT/'data/research-runs/stage-regularization-20261105'
OWNER='stage-regularization-20261105'
CONFIGS={'control':('linear',.2),'weaker_l2':('linear',.05),'categorical_stage':('categorical',.2)}


def encode(x,kind):
    if len(x)!=6 or x[0] not in (0,.25,.5,.75):
        raise ValueError('Expected six features and unresolved publication stage 0–3')
    if kind=='linear':return list(x)
    if kind!='categorical':raise ValueError('Unknown encoding')
    return [float(x[0]==stage/4) for stage in (1,2,3)]+list(x[1:])


def evaluate():
    D.mkdir(parents=True,exist_ok=True)
    original=ROOT/'data/research-runs/survivor1000-20261105/artifact.json'
    assert digest(json.loads(original.read_text()))==SURVIVOR_HASH
    spec=dict(folds=[115,116,117],configs=CONFIGS,iterations=300,learning_rate=.12,
              split='Reuse exact core/calibration/test membership of existing chronological folds',
              primary='Calibrated Brier; also report uncalibrated scores, log loss, stage groups and objective gradients',
              lead_gate='Brier improves and log loss does not worsen against control in every fold. Rank eligible leads by equal-fold mean relative Brier improvement.',
              categorical='Three stage indicators with introduced stage omitted; retain other five features. Same scaler and L2 rule; changed representation also changes penalty geometry.',
              exposure='Previously exposed development periods. No independent confirmation or automatic promotion.',
              source_hashes={str(c):digest(json.loads((SOURCE/f'fold-{c}.json').read_text())) for c in [115,116,117]},release_eligible=False)
    spec=json.loads(json.dumps(spec))
    if (D/'protocol.json').exists():assert json.loads((D/'protocol.json').read_text())['spec']==spec
    else:save(D,'protocol.json',dict(spec=spec,hash=digest(spec),registered_at=now()))
    rows=load_rows();groups=cohort.family_groups(rows);folds=[]
    for c in spec['folds']:
        store=Store()
        try:assert lease(store,'acquire',OWNER)['granted']
        finally:store.close()
        train,test=make_split(rows,c,groups)
        prior=json.loads((SOURCE/f'fold-{c}.json').read_text());oldmodels=json.loads((SOURCE/f'fold-{c}-models.json').read_text())
        assert digest(oldmodels)==prior['models_hash']
        old=oldmodels['calibrated_all_history'];lookup={r['bill_id']:r for r in train}
        assert [r['bill_id'] for r in train]==prior['training_ids']
        assert [r['bill_id'] for r in test]==[r['bill_id'] for r in prior['predictions']]
        core=[lookup[i] for i in old['core_ids']];calibration=[lookup[i] for i in old['calibration_ids']]
        assert set(old['core_ids']).isdisjoint(old['calibration_ids']) and set(old['core_ids'])|set(old['calibration_ids'])==set(lookup)
        assert {r['family_id'] for r in train}.isdisjoint(r['family_id'] for r in test)
        assert max(r['label_available_at'] for r in train)<min(r['cutoff'] for r in test)
        models={};predictions=[dict(bill_id=r['bill_id'],family_id=r['family_id'],stage=r['x'][0]*4,x=r['x'],outcome=r['y']) for r in test];gradients={}
        for name,(kind,l2) in CONFIGS.items():
            transformed=[dict(r,x=encode(r['x'],kind)) for r in core]
            base=learning._fit(transformed,l2)
            adjust=fit_calibration([predict(base,encode(r['x'],kind)) for r in calibration],[r['y'] for r in calibration])
            models[name]=dict(base=base,calibration=adjust,encoding=kind)
            gradients[name]=objective_gradient(base,transformed)
            if name=='control':assert base==old['base'] and adjust==old['calibration']
            for r,p in zip(test,predictions):
                probability=predict(base,encode(r['x'],kind));p[name+'_raw']=probability;p[name]=calibrate(adjust,probability)
        for p,previous in zip(predictions,prior['predictions']):assert abs(p['control']-previous['calibrated_all_history'])<1e-12
        names=[k for name in CONFIGS for k in (name,name+'_raw')]
        metrics={name:score([r[name] for r in predictions],[r['outcome'] for r in predictions]) for name in names}
        stages={str(stage):dict(n=len(sub),positive=sum(r['outcome'] for r in sub),expected={name:sum(r[name] for r in sub) for name in CONFIGS},brier={name:sum((r[name]-r['outcome'])**2 for r in sub)/len(sub) for name in CONFIGS}) for stage in sorted({r['stage'] for r in predictions}) for sub in [[r for r in predictions if r['stage']==stage]]}
        fold=dict(congress=c,core_ids=old['core_ids'],calibration_ids=old['calibration_ids'],test_n=len(test),test_positive=sum(r['y'] for r in test),models=models,gradients=gradients,metrics=metrics,stages=stages,predictions=predictions)
        folds.append(fold);print(json.dumps(dict(congress=c,brier={k:metrics[k]['brier'] for k in CONFIGS})),flush=True)
    comparisons={k:dict(mean_relative_brier_gain=sum(1-f['metrics'][k]['brier']/f['metrics']['control']['brier'] for f in folds)/len(folds),joint_wins=sum(f['metrics'][k]['brier']<f['metrics']['control']['brier'] and f['metrics'][k]['log_loss']<=f['metrics']['control']['log_loss'] for f in folds)) for k in ['weaker_l2','categorical_stage']}
    leads=[k for k,v in comparisons.items() if v['joint_wins']==len(folds)]
    selected=max(leads,key=lambda k:comparisons[k]['mean_relative_brier_gain']) if leads else None
    result=dict(title='Controlled regularization and stage-encoding experiments',protocol_hash=digest(spec),folds=folds,comparisons=comparisons,development_lead=selected,release_eligible=False,independent_validation=False,
                limitations=['All evaluation outcomes exposed; not evidence of independent performance.', 'Fixed 300-iteration runs; gradients reported, convergence not guaranteed.', 'Categorical encoding changes dimensionality/scaling and penalty geometry.', 'Calibrators refitted by the same rule on identical calibration rows; report raw scores to separate effects.', 'No combined weaker-penalty/categorical variant tested.', 'Historical publication and family-linkage limitations remain.'])
    result['hash']=digest(result)
    if (D/'result.json').exists():assert json.loads((D/'result.json').read_text())==result
    else:save(D,'result.json',result)
    assert digest(json.loads(original.read_text()))==SURVIVOR_HASH
    print(json.dumps(dict(comparisons=comparisons,selected=selected)),flush=True)
    return result


if __name__=='__main__':
    s=Store()
    try:
        if not lease(s,'acquire',OWNER)['granted']:raise RuntimeError('Research lease unavailable')
        try:evaluate()
        finally:lease(s,'release',OWNER)
    finally:s.close()
