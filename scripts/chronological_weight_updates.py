"""Fixed exposed-development tests of a chronological weight-update rule."""
import json
from engine import cohort
from engine.store import ROOT, digest, now, Store
from engine.research_lease import lease
from engine.survivor_batch import save
from engine.model import predict, score
from engine.three_model_experiment import fit_calibration, calibrate
from scripts.cross_congress_evaluate import D as SOURCE, load_rows, make_split, fit
from scripts.diagnose_transfer import raw, artifact, blend, SURVIVOR_HASH

D = ROOT/'data/research-runs/chronological-weight-updates-20261105'
OWNER = 'chronological-weight-updates-20261105'


def calibrated_fit(rows):
    ordered = sorted(rows,key=lambda r:digest(r['bill_id']))
    core = [r for i,r in enumerate(ordered) if i%5!=0]
    calibration = [r for i,r in enumerate(ordered) if i%5==0]
    if any(len({r['y'] for r in group})!=2 for group in (core,calibration)):
        raise ValueError('Both classes required in core and calibration')
    base = fit(core)
    adjustment = fit_calibration([predict(base,r['x']) for r in calibration],[r['y'] for r in calibration])
    return dict(base=base,calibration=adjustment,core_ids=[r['bill_id'] for r in core],calibration_ids=[r['bill_id'] for r in calibration])


def effective(model):
    coefficients = [v*model['calibration']['slope'] for v in raw(model['base'])]
    coefficients[0] += model['calibration']['intercept']
    return artifact(coefficients)


def partitions(training,test):
    latest = max(r['congress'] for r in training)
    older = [r for r in training if r['congress']<latest]
    assert len(older)>=200 and sum(r['y'] for r in older)>=5
    assert max(r['label_available_at'] for r in training)<min(r['cutoff'] for r in test)
    assert not {r['family_id'] for r in training}&{r['family_id'] for r in test}
    assert max(r['congress'] for r in training)<min(r['congress'] for r in test)
    return older


def run():
    D.mkdir(parents=True,exist_ok=True)
    originalpath=ROOT/'data/research-runs/survivor1000-20261105/artifact.json'
    assert digest(json.loads(originalpath.read_text()))==SURVIVOR_HASH
    spec=dict(folds=[115,116,117],fractions=[.25,.5],anchor='Calibrated model trained excluding latest eligible training Congress',
              update='Same calibrated fitting procedure with latest eligible Congress added',
              comparison=['anchor','shrink25','shrink50','full_update','historical_rate'],
              consistency='Report every fold; a restrained update must beat anchor in Brier and not worsen log loss in all three folds to be a consistent lead.',
              exposure='All evaluation periods previously exposed; exploratory development only.',release_eligible=False,
              source_hashes={str(c):digest(json.loads((SOURCE/f'fold-{c}.json').read_text())) for c in [115,116,117]})
    if (D/'protocol.json').exists():assert json.loads((D/'protocol.json').read_text())['spec']==spec
    else:save(D,'protocol.json',dict(spec=spec,hash=digest(spec),registered_at=now()))
    rows=load_rows();groups=cohort.family_groups(rows);folds=[]
    for c in spec['folds']:
        train,test=make_split(rows,c,groups);older=partitions(train,test)
        source=json.loads((SOURCE/f'fold-{c}.json').read_text())
        assert [r['bill_id'] for r in train]==source['training_ids']
        assert [r['bill_id'] for r in test]==[r['bill_id'] for r in source['predictions']]
        source_models=json.loads((SOURCE/f'fold-{c}-models.json').read_text())
        assert digest(source_models)==source['models_hash']
        anchor_fit=calibrated_fit(older);update_fit=source_models['calibrated_all_history']
        anchor,update=effective(anchor_fit),effective(update_fit)
        models=dict(anchor=anchor,shrink25=blend(anchor,update,.25),shrink50=blend(anchor,update,.5),full_update=update)
        rate=(sum(r['y'] for r in train)+1)/(len(train)+2)
        pairs=[]
        for row,previous in zip(test,source['predictions']):
            values={k:predict(m,row['x']) for k,m in models.items()}
            assert abs(values['full_update']-previous['calibrated_all_history'])<1e-12
            assert abs(values['anchor']-calibrate(anchor_fit['calibration'],predict(anchor_fit['base'],row['x'])))<1e-12
            pairs.append(dict(bill_id=row['bill_id'],family_id=row['family_id'],outcome=row['y'],features=row['x'],historical_rate=rate,**values))
        metrics={k:score([r[k] for r in pairs],[r['outcome'] for r in pairs]) for k in [*models,'historical_rate']}
        fold=dict(congress=c,anchor_n=len(older),anchor_positive=sum(r['y'] for r in older),training_n=len(train),test_n=len(test),test_positive=sum(r['y'] for r in test),
                  training_ids=[r['bill_id'] for r in train],anchor_training_ids=[r['bill_id'] for r in older],
                  latest_label=max(r['label_available_at'] for r in train),first_checkpoint=min(r['cutoff'] for r in test),
                  anchor_fit=anchor_fit,models=models,metrics=metrics,predictions=pairs)
        folds.append(fold)
        print(json.dumps(dict(congress=c,metrics={k:v['brier'] for k,v in metrics.items()})),flush=True)
    comparisons={k:dict(mean_relative_brier_gain=sum(1-f['metrics'][k]['brier']/f['metrics']['anchor']['brier'] for f in folds)/len(folds),
                        brier_wins=sum(f['metrics'][k]['brier']<f['metrics']['anchor']['brier'] for f in folds),
                        joint_wins=sum(f['metrics'][k]['brier']<f['metrics']['anchor']['brier'] and f['metrics'][k]['log_loss']<=f['metrics']['anchor']['log_loss'] for f in folds)) for k in ['shrink25','shrink50','full_update']}
    result=dict(title='Chronological constrained-weight update tests',protocol_hash=digest(spec),folds=folds,comparisons=comparisons,
                consistent_leads=[k for k in ['shrink25','shrink50'] if comparisons[k]['joint_wins']==3],release_eligible=False,independent_validation=False,
                note='Period-specific anchors are not the original survivor. Cross-fold cases/families may recur; do not pool as independent trials. Historical evidence limits persist.')
    result['hash']=digest(result)
    if (D/'result.json').exists():assert json.loads((D/'result.json').read_text())==result,'Replay changed'
    else:save(D,'result.json',result)
    assert digest(json.loads(originalpath.read_text()))==SURVIVOR_HASH
    print(json.dumps(comparisons),flush=True)
    return result


if __name__=='__main__':
    store=Store()
    try:
        if not lease(store,'acquire',OWNER)['granted']:raise RuntimeError('Research lease unavailable')
        try:run()
        finally:lease(store,'release',OWNER)
    finally:store.close()
