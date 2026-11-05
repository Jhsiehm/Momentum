"""Descriptive, exposed-data audit; no feature fitting, selection or promotion."""
import json, math
from collections import defaultdict, Counter
from engine.store import ROOT, digest, now, congress_end
from engine.model import predict, score, date
from engine.three_model_experiment import calibrate
from engine.survivor_batch import save
from scripts.cross_congress_evaluate import load_rows, D as SCALE
from scripts.diagnose_transfer import raw, NAMES, SURVIVOR_HASH

D=ROOT/'data/research-runs/granular-transfer-v2-20261105'
SOURCE=ROOT/'data/research-runs/chronological-weight-updates-20261105/result.json'


def metrics(rows):
    n=len(rows);y=[r['outcome'] for r in rows]
    a=score([r['anchor'] for r in rows],y);b=score([r['full_update'] for r in rows],y)
    return dict(n=n,positives=sum(y),observed=sum(y)/n,anchor=a,update=b,
                expected_anchor=sum(r['anchor'] for r in rows),expected_update=sum(r['full_update'] for r in rows),
                delta_sum=sum(r['delta'] for r in rows),delta_mean=sum(r['delta'] for r in rows)/n,
                sparse_positive_count=sum(y)<10)


def collisions(rows):
    cells=defaultdict(list)
    for r in rows:cells[tuple(r['features'])].append(r)
    mixed=[v for v in cells.values() if 0<sum(r['outcome'] for r in v)<len(v)]
    largest=sorted(cells.values(),key=lambda v:(-len(v),v[0]['bill_id']))[:10]
    return dict(unique_vectors=len(cells),rows=len(rows),mixed_cells=len(mixed),mixed_rows=sum(map(len,mixed)),
                positives_in_mixed_cells=sum(sum(r['outcome'] for r in v) for v in mixed),
                largest_cells=[dict(features=v[0]['features'],n=len(v),positive=sum(r['outcome'] for r in v),examples=[r['bill_id'] for r in v[:5]]) for v in largest])


def summarize_profile(rows):
    return dict(n=len(rows),positive=sum(r['y'] for r in rows),rate=sum(r['y'] for r in rows)/len(rows),
                feature_mean=[sum(r['x'][j] for r in rows)/len(rows) for j in range(6)],
                feature_unique=[len({r['x'][j] for r in rows}) for j in range(6)],
                stage=dict(Counter(str(r['x'][0]*4) for r in rows)),chamber=dict(Counter(r['type'] for r in rows)))


def objective_gradient(model, rows):
    n=len(rows);weights=model['weights'];data=[0.]*len(weights)
    for row in rows:
        x=[1.]+[(v-m)/s for v,m,s in zip(row['x'],model['means'],model['scales'])]
        error=predict(model,row['x'])-row['y']
        for j,v in enumerate(x):data[j]+=error*v/n
    penalty=[0.]+[model['l2']*w for w in weights[1:]]
    total=[a+b for a,b in zip(data,penalty)]
    return dict(n=n,l2=model['l2'],iterations=model['iterations'],data_gradient=data,penalty_gradient=penalty,
                objective_gradient=total,max_absolute_gradient=max(map(abs,total)),
                note='Gradient at saved fit under its stated penalized training objective; not a convergence proof or causal attribution.')


def run():
    D.mkdir(parents=True,exist_ok=True)
    source=json.loads(SOURCE.read_text());assert digest({k:v for k,v in source.items() if k!='hash'})==source['hash']
    assert digest(json.loads((ROOT/'data/research-runs/survivor1000-20261105/artifact.json').read_text()))==SURVIVOR_HASH
    spec=dict(source_hash=source['hash'],purpose='Exposed descriptive granular audit; no tuning or causal claims',
              strata=['outcome','chamber','publication_stage','chamber_stage','publication_count','recency','recent_publications','remaining_days','anchor_probability'],
              sensitivity='Remove top 1,5,10 absolute error-change cases for sensitivity only; retain all cases in reported main result',
              additional_diagnostics=['Saved-fit objective gradients','Training-stage outcome rates'],
              decomposition='Two-factor symmetric attribution: base model versus calibration; includes allocation/standardization changes in base factor',
              release_eligible=False)
    if (D/'protocol.json').exists():assert json.loads((D/'protocol.json').read_text())['spec']==spec
    else:save(D,'protocol.json',dict(spec=spec,hash=digest(spec),registered_at=now()))
    allrows={r['bill_id']:r for r in load_rows()};folds=[]
    for f in source['folds']:
        c=f['congress'];rows=[]
        for r in f['predictions']:
            meta=allrows[r['bill_id']];assert meta['x']==r['features'] and meta['y']==r['outcome']
            delta=(r['full_update']-r['outcome'])**2-(r['anchor']-r['outcome'])**2
            rows.append(dict(r,delta=delta,title=meta['title'],cutoff=meta['cutoff'],remaining_days=(date(congress_end(c))-date(meta['cutoff'])).days))
        keys=dict(outcome=lambda r:str(r['outcome']),chamber=lambda r:'Senate' if r['features'][4] else 'House',
                  publication_stage=lambda r:str(r['features'][0]*4),
                  chamber_stage=lambda r:('S' if r['features'][4] else 'H')+'_'+str(r['features'][0]*4),
                  publication_count=lambda r:'1' if r['features'][2]*30<1.5 else '2' if r['features'][2]*30<2.5 else '3+',
                  recency=lambda r:'0-30' if r['features'][3]*730<=30 else '31-90' if r['features'][3]*730<=90 else '91+',
                  recent_publications=lambda r:'none' if r['features'][5]==0 else 'one_plus',
                  remaining_days=lambda r:'0-180' if r['remaining_days']<=180 else '181-365' if r['remaining_days']<=365 else '366+',
                  anchor_probability=lambda r:'0-2%' if r['anchor']<.02 else '2-5%' if r['anchor']<.05 else '5-10%' if r['anchor']<.1 else '10%+')
        strata={name:{v:metrics([r for r in rows if fn(r)==v]) for v in sorted({fn(r) for r in rows})} for name,fn in keys.items()}
        total=metrics(rows)
        for groups in strata.values():
            assert sum(v['n'] for v in groups.values())==len(rows)
            assert abs(sum(v['delta_sum'] for v in groups.values())-total['delta_sum'])<1e-12
        ordered=sorted(rows,key=lambda r:(-abs(r['delta']),r['bill_id']))
        sensitivity={str(k):metrics([r for r in rows if r['bill_id'] not in {x['bill_id'] for x in ordered[:k]}]) for k in (1,5,10)}
        train=[allrows[i] for i in f['training_ids']];old=[allrows[i] for i in f['anchor_training_ids']];oldids=set(f['anchor_training_ids']);added=[r for r in train if r['bill_id'] not in oldids]
        update=json.loads((SCALE/f'fold-{c}-models.json').read_text())['calibrated_all_history'];anchor=f['anchor_fit']
        cells={};probabilities={}
        for b,base in [('old',anchor['base']),('new',update['base'])]:
            for a,calibration in [('old',anchor['calibration']),('new',update['calibration'])]:
                key=b+'_'+a;p=[calibrate(calibration,predict(base,r['features'])) for r in rows];probabilities[key]=p
                cells[key]=score(p,[r['outcome'] for r in rows])
        for i,r in enumerate(rows):
            assert abs(probabilities['old_old'][i]-r['anchor'])<1e-12
            assert abs(probabilities['new_new'][i]-r['full_update'])<1e-12
        decomposition={}
        for metric in ['brier','log_loss']:
            a,b,d,e=[cells[k][metric] for k in ['old_old','new_old','old_new','new_new']]
            base=.5*((b-a)+(e-d));cal=.5*((d-a)+(e-b))
            assert abs(base+cal-(e-a))<1e-12
            decomposition[metric]=dict(base_model=base,calibration=cal,total=e-a)
        coefs={k:dict(zip(['intercept']+NAMES,raw(f['models'][k]))) for k in ['anchor','full_update']}
        coefficients_delta=[b-a for a,b in zip(raw(f['models']['anchor']),raw(f['models']['full_update']))]
        logit_contributions={str(y):dict(zip(['intercept']+NAMES,[coefficients_delta[0]]+[coefficients_delta[j+1]*sum(r['features'][j] for r in rows if r['outcome']==y)/sum(r['outcome']==y for r in rows) for j in range(6)])) for y in (0,1)}
        folds.append(dict(congress=c,total=total,strata=strata,sensitivity=sensitivity,
                          top_harmed=sorted(rows,key=lambda r:-r['delta'])[:20],top_helped=sorted(rows,key=lambda r:r['delta'])[:20],
                          profiles={k:summarize_profile(v) for k,v in [('anchor_training',old),('added_training',added),('all_training',train),('evaluation',[allrows[r['bill_id']] for r in rows])]},
                          collisions=collisions(rows),coefficients=coefs,logit_contributions=logit_contributions,
                          factorial_metrics=cells,error_decomposition=decomposition,
                          calibration_parameters=dict(anchor=anchor['calibration'],update=update['calibration']),
                          calibration_set_overlap=len(set(anchor['calibration_ids'])&set(update['calibration_ids'])),
                          optimization={name:objective_gradient(m['base'],[allrows[i] for i in m['core_ids']]) for name,m in [('anchor',anchor),('update',update)]},
                          training_stage_profiles={name:{str(stage):dict(n=len(sub),positive=sum(r['y'] for r in sub),rate=sum(r['y'] for r in sub)/len(sub)) for stage in sorted({r['x'][0]*4 for r in group}) for sub in [[r for r in group if r['x'][0]*4==stage]]} for name,group in [('anchor',old),('added',added),('all',train)]}))
    result=dict(title='Granular period-shift and feature audit',protocol_hash=digest(spec),folds=folds,
                limitations=['All analyses are post-hoc on exposed outcomes; no independent validation.',
                             'Overlapping subgroups are not independent; sparse groups are flagged, not significance-tested.',
                             'Hybrid calibration swaps are diagnostic, not fitted deployable candidates.',
                             'Feature collisions show representational limits in this sample, not a population accuracy ceiling.',
                             'Publication-stage and recency are document proxies, not complete legislative actions.',
                             'Potential new predictors need historical availability checks before model use.'],release_eligible=False)
    result['hash']=digest(result)
    if (D/'result.json').exists():assert json.loads((D/'result.json').read_text())==result
    else:save(D,'result.json',result)
    print(json.dumps([dict(congress=f['congress'],total=f['total']['delta_sum'],decomposition=f['error_decomposition'],collisions={k:v for k,v in f['collisions'].items() if k!='largest_cells'},profiles={k:dict(n=v['n'],rate=v['rate']) for k,v in f['profiles'].items()},strata={k:{a:dict(n=b['n'],positive=b['positives'],delta=b['delta_sum']) for a,b in v.items()} for k,v in f['strata'].items() if k in ['outcome','chamber_stage','remaining_days']},sensitivity={k:v['delta_mean'] for k,v in f['sensitivity'].items()}) for f in folds],indent=2))
    return result

if __name__=='__main__':run()
