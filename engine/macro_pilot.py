"""Fixed exploratory macro ablation over frozen publication-v2 evidence.
Run: python3 -m engine.macro_pilot [--offline] [--publish]
No model promotion, original study mutations, paid calls or outcome-based tuning.
"""
import argparse
import csv
import hashlib
import io
import json
import math
from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from .store import ROOT, now, digest
from .model import fit, predict, score

DIRECTORY=ROOT/'data/cohorts/macro-pilot-v2'
BASE=ROOT/'data/cohorts/seeded-publication-v2'
SERIES=('UNRATE','CPIAUCSL')

def write_once(path,value):
    payload=json.dumps(value,sort_keys=True,indent=2)+'\n'
    if path.exists():
        if json.loads(path.read_text())!=value:raise ValueError('Frozen artifact differs: '+path.name)
    else:
        with path.open('x') as f:f.write(payload)

def vintage(cutoff):
    # Previous month-end is strictly earlier, including on the first of a month.
    d=date.fromisoformat(cutoff[:10]);return (d.replace(day=1)-timedelta(days=1)).isoformat()

def parse_csv(raw,series,asof):
    rows=list(csv.reader(io.StringIO(raw.decode('utf-8-sig'))))
    if not rows or rows[0]!=['observation_date',series+'_'+asof.replace('-','')]:
        raise ValueError('ALFRED did not identify the requested historical vintage')
    values={}
    for row in rows[1:]:
        if len(row)!=2:raise ValueError('Malformed ALFRED row')
        day=date.fromisoformat(row[0]).isoformat()
        if day>asof:raise ValueError('Future observation in vintage response')
        if row[1] in ('','.'):continue
        number=float(row[1])
        if not math.isfinite(number):raise ValueError('Nonfinite macro observation')
        if day in values:raise ValueError('Duplicate observation')
        values[day]=number
    if not values:raise ValueError('No vintage observations')
    return values

def macro_features(values,asof):
    unemployment=values['UNRATE'];prices=values['CPIAUCSL']
    ud=max(unemployment);pd=max(prices);d=date.fromisoformat(pd)
    prior=d.replace(year=d.year-1).isoformat()
    if prior not in prices or prices[prior]<=0:raise ValueError('Missing year-earlier price observation')
    if any((date.fromisoformat(asof)-date.fromisoformat(x)).days>100 for x in (ud,pd)):
        raise ValueError('Macro observation too stale for fixed protocol')
    return [unemployment[ud],100*(prices[pd]/prices[prior]-1)],dict(unemployment_month=ud,cpi_month=pd,prior_cpi_month=prior,vintage=asof)

def fetch(directory,series,asof,offline):
    key=series+'-'+asof;raw_path=directory/'sources'/(key+'.csv');meta_path=directory/'sources'/(key+'.json')
    if raw_path.exists() and meta_path.exists():
        raw=raw_path.read_bytes();meta=json.loads(meta_path.read_text())
        if hashlib.sha256(raw).hexdigest()!=meta['sha256']:raise ValueError('Cached macro source hash mismatch')
    elif offline:raise ValueError('Missing frozen macro source: '+key)
    else:
        start=(date.fromisoformat(asof).replace(day=1)-timedelta(days=800)).isoformat()
        url='https://alfred.stlouisfed.org/graph/alfredgraph.csv?'+urlencode(dict(id=series,cosd=start,coed=asof,vintage_date=asof))
        with urlopen(url,timeout=15) as response:raw=response.read()
        parse_csv(raw,series,asof)
        meta=dict(url=url,series=series,vintage=asof,sha256=hashlib.sha256(raw).hexdigest(),retrieved_at=now())
        raw_path.write_bytes(raw);write_once(meta_path,meta)
    return parse_csv(raw,series,asof),meta

def run(directory=DIRECTORY,offline=False):
    directory.mkdir(parents=True,exist_ok=True);(directory/'sources').mkdir(exist_ok=True)
    audit=json.loads((BASE/'cohort.json').read_text());original=json.loads((BASE/'result.json').read_text())
    if digest(audit['rows'])!=audit['cohort_hash'] or original['cohort_hash']!=audit['cohort_hash']:raise ValueError('Frozen bill cohort hash mismatch')
    if original['status']!='completed' or audit['failures']:raise ValueError('Original bill evidence is blocked')
    rows=[r for r in audit['rows'] if not r['exclusion']];train=[r for r in rows if r['congress']!=118];test=[r for r in rows if r['congress']==118]
    if {r['family_id'] for r in train}&{r['family_id'] for r in test}:raise ValueError('Family overlap')
    if len(train)<20 or {r['y'] for r in train}!={0,1} or not test:raise ValueError('Insufficient baseline evidence')
    if max(p['available_at'] for p in audit['training_label_provenance'])>min(r['cutoff'] for r in test):raise ValueError('Training labels unavailable at evaluation time')
    protocol=dict(version='macro-pilot-v2',transport_amendment='v1 timed out before receiving data or scores; use default Python transport. Same features and evaluation.',base_cohort_hash=audit['cohort_hash'],base_result_hash=original['reproducibility_hash'],series=list(SERIES),features=['latest released unemployment percent','latest released CPI year-over-year percent'],vintage_policy='Previous calendar month-end, strictly before bill cutoff',split='114+116 train;118 evaluation; original exclusions unchanged',model='Same fit, L2=.05,300 iterations; training-only standardization; append two features',primary_metric='Paired Brier difference against publication-only model',design='Exploratory reuse of previously inspected evaluation outcomes. No tuning, promotion, causal inference or new holdout claim.',code_hash=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),model_hash=hashlib.sha256((ROOT/'engine/model.py').read_bytes()).hexdigest())
    write_once(directory/'protocol.json',protocol)
    if not (directory/'registration.json').exists():write_once(directory/'registration.json',dict(registered_at=now(),protocol_hash=digest(protocol)))
    keys=sorted({(s,vintage(r['cutoff'])) for r in rows for s in SERIES})
    def get(k):return k,fetch(directory,*k,offline)
    sources={}
    with ThreadPoolExecutor(max_workers=2) as pool:
        for i,(k,v) in enumerate(pool.map(get,keys),1):
            sources[k]=v
            if i%10==0:print(f'Archived {i}/{len(keys)} macro vintages',flush=True)
    joined=[]
    for r in rows:
        v=vintage(r['cutoff']);x,dates=macro_features({s:sources[s,v][0] for s in SERIES},v)
        joined.append(dict(bill_id=r['bill_id'],family_id=r['family_id'],congress=r['congress'],cutoff=r['cutoff'],title=r['title'],x=r['x'],macro=x,macro_dates=dates,y=r['y']))
    train=[r for r in joined if r['congress']!=118];test=[r for r in joined if r['congress']==118]
    base=fit([dict(x=r['x'],y=r['y']) for r in train]);candidate=fit([dict(x=r['x']+r['macro'],y=r['y']) for r in train])
    reference=(sum(r['y'] for r in train)+1)/(len(train)+2)
    predictions=[dict(bill_id=r['bill_id'],title=r['title'],family_id=r['family_id'],cutoff=r['cutoff'],outcome=r['y'],probability=predict(candidate,r['x']+r['macro']),publication_probability=predict(base,r['x']),baseline_probability=reference,macro=r['macro'],macro_dates=r['macro_dates']) for r in test]
    labels=[r['outcome'] for r in predictions];metrics=score([r['probability'] for r in predictions],labels);comparison=score([r['publication_probability'] for r in predictions],labels);baseline=score([reference]*len(labels),labels)
    if abs(comparison['brier']-original['metrics']['brier'])>1e-12:raise ValueError('Publication baseline failed to reproduce')
    manifest=[sources[k][1] for k in keys]
    identity=digest(dict(protocol=protocol,rows=joined,source_hashes=[m['sha256'] for m in manifest],predictions=predictions))
    result=dict(id='macro-'+identity,kind='macro_pilot',title='Macro context · fixed exploratory comparison',status='completed',config=dict(dataset='official',congress=118,age_days=180),metrics=metrics,baseline=baseline,publication_metrics=comparison,brier_difference_vs_publication=metrics['brier']-comparison['brier'],training_count=len(train),training_positives=sum(r['y'] for r in train),evaluation_positives=sum(labels),attempted=len(test),available=len(test),results=predictions,release_eligible=False,model_artifact=candidate,publication_model=base,protocol=protocol,source_manifest=manifest,reproducibility_hash=identity,limitations=original['limitations']+['Previously inspected sample reused for an exploratory fixed comparison.','National macro conditions shared across bills; 33 rows are not 33 independent economic environments.','No evaluation enactments; cannot assess ability to identify successful bills.','ALFRED vintage metadata identifies historical releases, not independently archived original release bytes.'],note='Exploratory macro comparison, not validated accuracy. No model promotion. The unchanged baseline must reproduce; macro features use prior-month-end releases. Evaluation has zero enactments, so lower error cannot establish identifying bills that pass.')
    write_once(directory/'joined.json',joined);write_once(directory/'result.json',result)
    return result

def publish(result):
    from . import workspace
    from .store import Store
    store=Store();workspace.initialize(store)
    try:
        existing=store.db.execute('SELECT id FROM experiments WHERE id=?',(result['id'],)).fetchone()
        if not existing:workspace.save_experiment(store,dict(result,created_at=now(),completed_at=now()))
    finally:store.close()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--offline',action='store_true');p.add_argument('--publish',action='store_true');a=p.parse_args()
    r=run(offline=a.offline)
    if a.publish:publish(r)
    print(json.dumps({k:r[k] for k in ('id','metrics','baseline','publication_metrics','brier_difference_vs_publication','training_count','training_positives','evaluation_positives','reproducibility_hash')},indent=2))
