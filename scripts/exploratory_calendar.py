"""Nine predeclared exploratory fits; never change frozen paper artifacts."""
import argparse
import hashlib
import json
import math
import signal
from pathlib import Path
import numpy as np

from engine.cohort import family_groups
from engine.model import predict, score
from engine.paper_evaluation import seal, unseal, require
from engine.research_lease import lease
from engine.store import ROOT, Store, digest, now
from engine.three_model_experiment import calibrate, fit_calibration
from scripts.bill_context_execution import calendar_features
from scripts.convergence_experiment import fit_converged
from scripts.cross_congress_evaluate import D, load_rows, make_split
from scripts.granular_transfer_audit import objective_gradient
from scripts.paper_readiness_audit import audit
from scripts.paper_review_packet import persist_or_compare
from scripts.verify_bill_context_execution import verify

ARMS=('control','time','interaction')
PROTOCOL=ROOT/'docs/research/EXPLORATORY_CALENDAR_PROTOCOL_V1.md'


def metrics(values, outcomes):
    result=score(values,outcomes)
    result.update(n=len(values),positives=sum(outcomes),expected=sum(values))
    result['by_outcome']={str(y):dict(n=len(v),brier=sum((p-y)**2 for p in v)/len(v) if v else None)
                          for y in (0,1) for v in [[p for p,t in zip(values,outcomes) if t==y]]}
    result['reliability']=[dict(bin=i,n=len(pairs),predicted=sum(p for p,y in pairs)/len(pairs) if pairs else None,
                               observed=sum(y for p,y in pairs)/len(pairs) if pairs else None)
                           for i in range(10) for pairs in [[(p,y) for p,y in zip(values,outcomes) if min(9,int(p*10))==i]]]
    return result


def summarize(folds):
    require(len(folds)==3,'All three folds required')
    names=list(ARMS)+[a+'_raw' for a in ARMS]+['rate','stage']
    means={name:sum(f['metrics'][name]['brier'] for f in folds)/3 for name in names}
    leads=[a for a in ARMS[1:] if all(f['metrics'][a]['brier']<f['metrics']['control']['brier'] and f['metrics'][a]['log_loss']<=f['metrics']['control']['log_loss'] for f in folds)]
    lead=None
    for a in leads:
        if lead is None or means[a]<means[lead]-1e-12:lead=a
    return dict(mean_brier=means,skill_vs_rate={a:1-means[a]/means['rate'] for a in ARMS},
                skill_vs_stage={a:1-means[a]/means['stage'] for a in ARMS},
                relative_gain_vs_control={a:1-means[a]/means['control'] for a in ARMS[1:]},
                exploratory_lead=lead,independent_validation=False)


def intervals(folds, draws=10000):
    families=sorted({r['family_id'] for f in folds for r in f['predictions']});index={v:i for i,v in enumerate(families)}
    contrasts=[(a,b) for a in ARMS for b in ('rate','stage')]+[(a,'control') for a in ARMS[1:]]
    counts=np.zeros((len(families),3));sums=np.zeros((len(families),3,len(contrasts)))
    for j,f in enumerate(folds):
        for r in f['predictions']:
            i=index[r['family_id']];counts[i,j]+=1
            for k,(a,b) in enumerate(contrasts):sums[i,j,k]+=(r[a]-r['outcome'])**2-(r[b]-r['outcome'])**2
    rng=np.random.default_rng(20261108);values=[];invalid=0
    for _ in range(draws):
        weights=rng.multinomial(len(families),np.full(len(families),1/len(families)))
        n=np.einsum('i,ij->j',weights,counts,optimize=False)
        if np.any(n==0):invalid+=1;continue
        values.append(np.mean(np.einsum('i,ijk->jk',weights,sums,optimize=False)/n[:,None],axis=0))
    require(len(values)>=.9*draws,'Fewer than 90% valid bootstrap draws')
    bounds=np.quantile(np.array(values),[.025,.975],axis=0)
    return dict(draws=draws,invalid=invalid,seed=20261108,global_families=len(families),
                intervals={a+'_minus_'+b:bounds[:,k].tolist() for k,(a,b) in enumerate(contrasts)},
                interpretation='Conditional exposed-period descriptive paired-family intervals; unadjusted for selection/multiplicity')


def run(directory):
    directory=Path(directory)
    require(ROOT/'data' in directory.resolve().parents,'Output must be under ignored data')
    directory.mkdir(parents=True,exist_ok=False)
    store=Store();owner='exploratory-calendar-'+directory.name
    require(lease(store,'acquire',owner)['granted'],'Research lease unavailable')
    previous_handler=signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('Six-hour study cap reached')))
    signal.alarm(21600)
    try:
        before=audit();pilot=ROOT/'data/research-runs/bill-context-20261108-v1';verify(pilot)
        inputs=unseal(json.loads((pilot/'e1-unapproved-inputs.json').read_text()))
        rows=load_rows();groups=family_groups(rows);lookup={r['bill_id']:r for r in rows}
        previous=json.loads((ROOT/'data/research-runs/convergence-einsum-20261105/result.json').read_text())
        require(digest({k:v for k,v in previous.items() if k!='hash'})==previous['hash'],'Prior result hash mismatch')
        for c in (115,116,117):
            f=inputs[str(c)];train,test=make_split(rows,c,groups)
            require(f['evaluation_ids']==[r['bill_id'] for r in test],'Evaluation IDs mismatch')
            partitions=[[lookup[i] for i in f[key]] for key in ('core_ids','calibration_ids','evaluation_ids')]
            familysets=[{groups[r['bill_id']] for r in part} for part in partitions]
            require(all(len(fs)==len(part) for fs,part in zip(familysets,partitions)),'Repeated family in partition')
            require(all(not familysets[i]&familysets[j] for i in range(3) for j in range(i+1,3)),'Family overlap')
            require(all({r['y'] for r in part}=={0,1} for part in partitions[:2]),'Missing training classes')
            require(max(r['congress'] for r in train)<c and max(r['label_available_at'] for r in train)<min(r['cutoff'] for r in test),'Temporal leakage')
        paths=sorted(str(p.relative_to(ROOT)) for folder in ('engine','scripts') for p in (ROOT/folder).glob('*.py'))
        spec=dict(registered_at=now(),protocol_sha256=hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
                  code={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},
                  numpy=np.__version__,input_hash=digest(inputs),population_hash=digest(rows),family_hash=digest(groups),
                  memberships={c:{k:f[k] for k in ('core_ids','calibration_ids','evaluation_ids')} for c,f in inputs.items()},
                  previous_result_hash=previous['hash'],arms=ARMS,fit_cap=9,wallclock_cap_seconds=21600,
                  stopping=dict(l2=.05,learning_rate=.12,minimum=300,maximum=20000,gradient=1e-6),
                  waived_for_this_exploratory_study=['human source/family/outcome certification','reviewed positive-family minimum floors'],
                  frozen_audit=before,release_eligible=False,independent_validation=False)
        registration=seal(spec);persist_or_compare(directory/'registration.json',registration)
        folds=[]
        for c in (115,116,117):
            f=inputs[str(c)];core=[lookup[i] for i in f['core_ids']];cal=[lookup[i] for i in f['calibration_ids']];test=[lookup[i] for i in f['evaluation_ids']]
            models={};diagnostics={}
            for arm in ARMS:
                require(lease(store,'renew',owner)['granted'],'Lost research lease')
                transformed=[dict(r,x=calendar_features(r,arm)) for r in core]
                base,diag,_=fit_converged(transformed,.05)
                max_logit=max(abs(base['weights'][0]+sum(w*(v-m)/s for w,v,m,s in zip(base['weights'][1:],r['x'],base['means'],base['scales']))) for r in transformed)
                require(max_logit<35,'Training logit clipping active; comparison blocked')
                diag['max_absolute_training_logit']=max_logit
                scalar=objective_gradient(base,transformed)['max_absolute_gradient']
                require(all(math.isfinite(v) for v in base['weights']),'Nonfinite model')
                require(diag['converged'] and scalar<=1e-6 and abs(scalar-diag['max_absolute_gradient'])<1e-12,'Convergence gate failed')
                if arm=='control':
                    prior=next(v for v in previous['folds'] if v['congress']==c)['models']['weaker_l2']['base']
                    require(base==prior,'Exact control artifact reproduction failed')
                adjust=fit_calibration([predict(base,calendar_features(r,arm)) for r in cal],[r['y'] for r in cal])
                models[arm]=dict(base=base,calibration=adjust);diagnostics[arm]=dict(**diag,scalar_gradient=scalar)
                persist_or_compare(directory/f'fit-{c}-{arm}.json',seal(dict(registration_hash=registration['hash'],model=models[arm],diagnostics=diagnostics[arm])))
                print(json.dumps(dict(congress=c,arm=arm,iterations=diag['iterations'],gradient=scalar)),flush=True)
            training=core+cal;rate=(sum(r['y'] for r in training)+1)/(len(training)+2)
            stages={s:(sum(r['y'] for r in training if r['x'][0]*4==s)+5*rate)/(sum(r['x'][0]*4==s for r in training)+5) for s in range(4)}
            pairs=[]
            for r in test:
                p=dict(bill_id=r['bill_id'],family_id=groups[r['bill_id']],outcome=r['y'],rate=rate,stage=stages[int(r['x'][0]*4)])
                for arm in ARMS:
                    p[arm+'_raw']=predict(models[arm]['base'],calendar_features(r,arm));p[arm]=calibrate(models[arm]['calibration'],p[arm+'_raw'])
                pairs.append(p)
            names=list(ARMS)+[a+'_raw' for a in ARMS]+['rate','stage']
            fold=dict(congress=c,core_ids=f['core_ids'],calibration_ids=f['calibration_ids'],models=models,diagnostics=diagnostics,predictions=pairs,
                      counts=dict(core=len(core),calibration=len(cal),evaluation=len(test),training_positive=sum(r['y'] for r in training),evaluation_positive=sum(r['y'] for r in test)),
                      metrics={name:metrics([r[name] for r in pairs],[r['outcome'] for r in pairs]) for name in names})
            persist_or_compare(directory/f'fold-{c}.json',seal(fold));folds.append(fold)
        result=seal(dict(registration_hash=registration['hash'],folds=folds,summary=summarize(folds),bootstrap=intervals(folds),
                         models_fitted=9,release_eligible=False,independent_validation=False))
        require(audit()==before,'Frozen artifacts changed')
        persist_or_compare(directory/'result.json',result)
        return result
    except Exception as error:
        persist_or_compare(directory/'failure.json',seal(dict(error=str(error),release_eligible=False)))
        raise
    finally:
        signal.alarm(0);signal.signal(signal.SIGALRM,previous_handler)
        lease(store,'release',owner);store.close()


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True)
    result=run(p.parse_args().output);print(json.dumps(result['body']['summary'],indent=2))
