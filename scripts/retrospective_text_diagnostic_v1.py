"""Four fixed retrospective association fits; never a certified forecast test."""
import argparse
import hashlib
import json
import signal
from pathlib import Path
import numpy as np
import scipy
from scipy.special import expit
from engine.store import ROOT
from engine.paper_evaluation import require, seal
from scripts.run_mechanism_design_extractor import read,persist
from scripts.bill_context_design_text_v2 import render
from scripts.bill_structural_input_v1 import build
from scripts.matched_text_preprocessing_v1 import prepare_document,CoreTfidf
from scripts.matched_text_sparse_v1 import fit,fit_structured_scaler,transform_structured,combine_features

BASE=ROOT/'data/research-runs'
PROTOCOL=ROOT/'docs/research/RETROSPECTIVE_TEXT_DIAGNOSTIC_V1.md'
BATCHES=['mechanism-training-coverage-20261108-v2','mechanism-training-expansion-20261108-v1']
ARMS=('anchor','text')

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def select_memberships(memberships,sources,banned_ids,banned_families):
    allowed={bid for bid,r in sources.items() if bid not in banned_ids and r['family_id'] not in banned_families}
    result={}
    for fold in ('115','116'):
        m=memberships[fold]
        result[fold]={role:[bid for bid in ids if bid in allowed] for role,ids in [('train',m['core_ids']+m['calibration_ids']),('evaluation',m['evaluation_ids'])]}
        a,b=result[fold]['train'],result[fold]['evaluation']
        require(all(sources[bid]['bill_id']==bid and sources[bid]['congress']<int(fold) for bid in a),'Training source identity/Congress')
        require(all(sources[bid]['bill_id']==bid and sources[bid]['congress']==int(fold) for bid in b),'Evaluation source identity/Congress')
        require(len(set(a+b))==len(a+b),'Duplicate/overlapping identities')
        fa,fb=[{sources[bid]['family_id'] for bid in ids} for ids in (a,b)]
        require(len(fa)==len(a) and len(fb)==len(b) and not fa&fb,'Provisional family overlap')
    return result

def metric(p,y):
    p=np.asarray(p,dtype=float);y=np.asarray(y,dtype=float)
    require(p.ndim==y.ndim==1 and p.shape==y.shape and len(p)>0,'Metric shape')
    require(np.all(np.isfinite(p)) and np.all((p>=0)&(p<=1)) and np.all((y==0)|(y==1)),'Invalid metric values')
    clipped=np.clip(p,1e-15,1-1e-15)
    return dict(n=len(y),positives=int(y.sum()),brier=float(np.mean((p-y)**2)),log_loss=float(-np.mean(y*np.log(clipped)+(1-y)*np.log1p(-clipped))),expected_events=float(p.sum()),
        by_outcome={str(k):dict(n=int((y==k).sum()),brier=float(np.mean((p[y==k]-k)**2)) if np.any(y==k) else None) for k in (0,1)},
        reliability=[dict(bin=i,n=int(mask.sum()),predicted=float(p[mask].mean()) if mask.any() else None,observed=float(y[mask].mean()) if mask.any() else None) for i in range(10) for mask in [np.minimum(9,(p*10).astype(int))==i]])

def bootstrap(folds,draws=10000):
    require(type(draws) is int and draws>0 and folds and all(f.get('predictions') for f in folds),'Nonempty folds and positive draw count required')
    for f in folds:
        require(len({r['family_id'] for r in f['predictions']})==len(f['predictions']),'Repeated within-fold family')
        for r in f['predictions']:
            require(isinstance(r['family_id'],str) and r['family_id'] and r['outcome'] in (0,1),'Invalid bootstrap identity/outcome')
            require(all(type(r[a]) in (int,float) and np.isfinite(r[a]) and 0<=r[a]<=1 for a in ('anchor','text','rate','stage')),'Invalid bootstrap probability')
    families=sorted({r['family_id'] for f in folds for r in f['predictions']});index={v:i for i,v in enumerate(families)}
    counts=np.zeros((len(families),len(folds)));values=np.zeros((len(families),len(folds),3))
    for j,f in enumerate(folds):
        for r in f['predictions']:
            i=index[r['family_id']];counts[i,j]+=1
            for k,b in enumerate(('anchor','rate','stage')):values[i,j,k]+=(r['text']-r['outcome'])**2-(r[b]-r['outcome'])**2
    rng=np.random.default_rng(20261108);samples=[];invalid=0
    for _ in range(draws):
        w=rng.multinomial(len(families),np.full(len(families),1/len(families)));n=w@counts
        if np.any(n==0):invalid+=1;continue
        samples.append(np.mean(np.einsum('i,ijk->jk',w,values)/n[:,None],axis=0))
    return dict(draws=draws,invalid=invalid,valid=len(samples),global_families=len(families),seed=20261108,
        intervals={b:np.quantile(np.asarray(samples)[:,k],[.025,.975]).tolist() for k,b in enumerate(('text_minus_anchor','text_minus_rate','text_minus_stage'))} if len(samples)>=.9*draws else None,
        interpretation='Descriptive exposed-source-conditioned paired-family intervals; no significance/promotion claim')

def run(directory):
    directory=Path(directory).resolve();require(ROOT/'data' in directory.parents,'Ignored output required');directory.mkdir(exist_ok=False)
    require(np.__version__=='2.0.2' and scipy.__version__=='1.13.1','Pinned environment required')
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('Six-hour cap')));signal.alarm(21600)
    sources={};paths=[PROTOCOL,ROOT/'requirements-research-text-v1.txt',ROOT/'tests/test_retrospective_text_diagnostic_v1.py'];prepared={};failures=[];fits_started=0
    try:
        pilot_path=BASE/'bill-context-20261108-v1/registration.json';calendar_path=BASE/'exploratory-calendar-20261108-v1/registration.json'
        _,pilot=read(pilot_path);_,calendar=read(calendar_path);paths.extend([pilot_path,calendar_path])
        for name in BATCHES:
            batch=BASE/name;_,registration=read(batch/'registration.json');paths.extend([batch/'registration.json',batch/'result.json'])
            for path in sorted((batch/'records').glob('*.json')):
                _,r=read(path)
                require(r['registration_hash']==read(batch/'registration.json')[0]['hash'],'Source registration binding')
                if r['status']!='metadata_dated_current_xml':continue
                raw=batch/'sources'/(hashlib.sha256(r['source']['url'].encode()).hexdigest()+'.raw')
                require(sha(raw)==r['source']['sha256'],'Raw source digest')
                require(r['bill_id'] not in sources,'Duplicate source identity')
                sources[r['bill_id']]=dict(r,raw_path=str(raw.relative_to(ROOT)),record_path=str(path.relative_to(ROOT)))
                paths.extend([path,raw])
        banned={r['bill_id'] for r in pilot['selection']};families={r['family_id'] for r in pilot['selection']}
        members=select_memberships(calendar['memberships'],sources,banned,families)
        selected=sorted({bid for m in members.values() for ids in m.values() for bid in ids})
        code={str(p.relative_to(ROOT)):sha(p) for folder in ('scripts','engine') for p in (ROOT/folder).glob('*.py')}
        for name in ['acquisition.json','positive-date-evidence.json','label-evidence.json','expansion-decision.json']:
            p=BASE/'cross-congress-scale-20261105'/name
            if p.exists():paths.append(p)
        for name in ['acquisition.json','positive-date-evidence.json']:
            p=BASE/'cross-congress-reserve-20261105'/name
            if p.exists():paths.append(p)
        reg=persist(directory/'registration.json',dict(version='retrospective-text-diagnostic-v1',protocol_hash=sha(PROTOCOL),inputs={str(p.relative_to(ROOT)):sha(p) for p in paths},code=code,candidate_memberships=members,selected_ids=selected,excluded_pilot_ids=sorted(banned),excluded_pilot_families=sorted(families),fit_cap=4,calibration_fits=0,historical_eligibility=False,independent_validation=False,release_eligible=False))
        (directory/'prepared').mkdir()
        for bid in selected:
            try:
                raw=(ROOT/sources[bid]['raw_path']).read_bytes();view=render(raw,bid);vh=seal(view)['hash'];side=build(raw,bid,view,vh)
                doc=prepare_document(raw,bid,view,vh,side);persist(directory/'prepared'/(bid+'.json'),doc);prepared[bid]=doc
            except Exception as error:failures.append(dict(bill_id=bid,error=type(error).__name__+': '+str(error)))
        final={fold:{role:[bid for bid in ids if bid in prepared] for role,ids in m.items()} for fold,m in members.items()}
        population=persist(directory/'population.json',dict(registration_hash=reg['hash'],memberships=final,preparation_failures=failures,prepared_hashes={bid:seal(doc)['hash'] for bid,doc in prepared.items()},labels_read=False))
        print(json.dumps({'population':{f:{r:len(ids) for r,ids in m.items()} for f,m in final.items()},'preparation_failures':len(failures)}),flush=True)
        from scripts.cross_congress_evaluate import load_rows
        from engine.cohort import family_groups
        rows=load_rows();groups=family_groups(rows);lookup={r['bill_id']:r for r in rows};folds=[]
        require(len(lookup)==len(rows),'Duplicate historical rows')
        used={bid for m in final.values() for ids in m.values() for bid in ids}
        for bid in used:
            r=lookup[bid];require(not r['exclusion'] and type(r['y']) in (int,float) and r['y'] in (0,1),'Invalid historical label/eligibility')
            stage=r['x'][0]*4;require(stage in (0,1,2,3),'Invalid publication stage');lookup[bid]=dict(r,stage=int(stage))
        for fold,m in final.items():
            train=[lookup[bid] for bid in m['train']];evaluation=[lookup[bid] for bid in m['evaluation']]
            require(train and evaluation,'Empty partition')
            for bid in m['train']+m['evaluation']:require(groups[bid]==sources[bid]['family_id'],'Family graph changed')
            require(max(r['congress'] for r in train)<int(fold) and all(r['congress']==int(fold) for r in evaluation),'Congress split')
            require(max(r['label_available_at'] for r in train)<min(r['cutoff'] for r in evaluation),'Training label availability')
            y=np.array([r['y'] for r in train]);require(set(y)=={0,1},'Training classes')
            X=np.array([r['x'] for r in train]);Z=np.array([r['x'] for r in evaluation]);scaler=fit_structured_scaler(X)
            vectorizer=CoreTfidf().fit([prepared[bid] for bid in m['train']],m['train'],['core']*len(train))
            T=vectorizer.transform([prepared[bid] for bid in m['train']]);U=vectorizer.transform([prepared[bid] for bid in m['evaluation']])
            persist(directory/(fold+'-representation.json'),dict(population_hash=population['hash'],scaler=scaler,vocabulary=vectorizer.manifest(),training_text_shape=list(T.shape),training_text_nnz=T.nnz,evaluation_text_nnz=U.nnz))
            designs={'anchor':(transform_structured(X,scaler),transform_structured(Z,scaler)),'text':(combine_features(X,scaler,T),combine_features(Z,scaler,U))};probabilities={}
            for arm,(A,B) in designs.items():
                fits_started+=1;require(fits_started<=4,'Fit cap');persist(directory/(fold+'-'+arm+'-intent.json'),dict(fit_number=fits_started,rows=A.shape[0],columns=A.shape[1]))
                model=fit(A,y);persist(directory/(fold+'-'+arm+'-fit.json'),model);require(model['accepted'],'Nonconverged fit')
                theta=np.asarray(model['parameters']);probabilities[arm]=expit(B@theta[1:]+theta[0]).tolist()
            rate=float((y.sum()+1)/(len(y)+2));stages={s:float((y[[r['stage']==s for r in train]].sum()+5*rate)/(sum(r['stage']==s for r in train)+5)) for s in range(4)}
            predictions=[dict(bill_id=r['bill_id'],family_id=groups[r['bill_id']],anchor=probabilities['anchor'][i],text=probabilities['text'][i],rate=rate,stage=stages[r['stage']]) for i,r in enumerate(evaluation)]
            persist(directory/(fold+'-predictions.json'),dict(population_hash=population['hash'],predictions=predictions))
            ey=[r['y'] for r in evaluation];scored=[dict(r,outcome=y) for r,y in zip(predictions,ey)]
            result=dict(fold=fold,training_n=len(train),training_positives=int(y.sum()),evaluation_n=len(evaluation),evaluation_positives=int(sum(ey)),metrics={a:metric([r[a] for r in predictions],ey) for a in ('anchor','text','rate','stage')},predictions=scored)
            persist(directory/(fold+'-metrics.json'),result);folds.append(result);print(json.dumps({k:v for k,v in result.items() if k!='predictions'}),flush=True)
        means={a:{metric_name:float(np.mean([f['metrics'][a][metric_name] for f in folds])) for metric_name in ('brier','log_loss')} for a in ('anchor','text','rate','stage')}
        for p,h in reg['body']['inputs'].items():require(sha(ROOT/p)==h,'Input changed')
        for p,h in code.items():require(sha(ROOT/p)==h,'Code changed')
        result=persist(directory/'result.json',dict(registration_hash=reg['hash'],population_hash=population['hash'],fits_started=fits_started,folds=folds,means=means,skill={a:{b:1-means[a]['brier']/means[b]['brier'] if means[b]['brier'] else None for b in ('rate','stage')} for a in ARMS},bootstrap=bootstrap(folds),preparation_failures=failures,historical_eligibility=False,independent_validation=False,release_eligible=False))
        print('RESULT',result['hash'],flush=True);return result
    except BaseException as error:
        persist(directory/'failure.json',dict(error=type(error).__name__+': '+str(error),fits_started=fits_started,prepared=len(prepared),preparation_failures=failures));raise
    finally:signal.alarm(0)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('directory',type=Path);args=parser.parse_args();run(args.directory)
