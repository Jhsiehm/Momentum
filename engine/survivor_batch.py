"""Preregistered fixed-survivor batch; score every eligible case without tuning."""
import argparse,copy,hashlib,json,random,re,time
from collections import Counter
from pathlib import Path
from . import cohort,learning,sample_publication_v2 as pub
from .model import predict,score
from .store import ROOT,digest,now

def save(directory,name,value):
    path=directory/name;body=json.dumps(value,indent=2,sort_keys=True)+'\n'
    if path.exists():assert json.loads(path.read_text())==value,'Frozen artifact mismatch: '+name
    else:path.write_text(body)

def select(rows,training,exposed):
    groups=cohort.family_groups(training+exposed+rows);forbidden={groups[r['bill_id']] for r in training+exposed};selected=[];excluded=[];used=set()
    for original in rows:
        row=copy.deepcopy(original);row['family_id']=groups[row['bill_id']];reason=row['exclusion']
        if not reason and row['family_id'] in forbidden:reason='Known prior/training family overlap'
        if not reason and row['family_id'] in used:reason='Duplicate selected family'
        if reason:excluded.append(dict(bill_id=row['bill_id'],reason=reason));continue
        selected.append(row);used.add(row['family_id'])
    return selected,excluded

def run(directory,offline=False):
    directory=Path(directory);p=json.loads((directory/'protocol.json').read_text());s=p['spec'];assert digest(s)==p['hash']
    population=json.loads((directory/'population.json').read_text());assert digest(population)==s['population_hash'];assert random.Random(s['seed']).sample(population,len(s['candidate_ids']))==s['candidate_ids']
    artifact=json.loads((directory/'artifact.json').read_text());training=json.loads((directory/'training.json').read_text());exposed=json.loads((directory/'exposed.json').read_text());assert digest(artifact)==s['model_hash'] and digest(training)==s['training_hash'] and digest(exposed)==s['exposed_rows_hash']
    transformed=[dict(r,x=learning.features(r,'structured')) for r in training];check=learning._fit(transformed,.2);check.update(policy='structured',training_hash=digest(transformed));assert check==artifact
    dependencies={str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted((ROOT/'engine').glob('*.py'))};save(directory,'dependencies.json',dependencies)
    laws,lawproofs=pub.law_census(cohort.Sources(pub.DIRECTORY,True),118,274);labels={r['bill_id']:r for r in laws};sources=pub.Sources(directory,offline);rows=[];failures=[]
    for i,bid in enumerate(s['candidate_ids'],1):
        try:
            m=re.fullmatch(r'(118)-(hr|s)(\d+)',bid);assert m;rows.append(pub.sample_bill(sources,118,m[2],int(m[3]),{'age_days':s['age_days']},labels))
        except Exception as e:failures.append(dict(bill_id=bid,error=str(e)))
        if not offline:
            (directory/'progress.json').write_text(json.dumps(dict(completed=i,total=len(s['candidate_ids']),failures=failures,updated_at=now())))
            if i%25==0:print('Audited',i,'/',len(s['candidate_ids']),'failures',len(failures),flush=True)
            time.sleep(.05)
    acquisition=dict(rows=rows,failures=failures,sources=sources.manifest(),law_sources=lawproofs)
    if failures:
        (directory/'acquisition-failed.json').write_text(json.dumps(acquisition,indent=2,sort_keys=True));raise ValueError('Source failures block all scoring; retain cache and retry same identities')
    save(directory,'acquisition.json',acquisition)
    chosen,excluded=select(rows,training,exposed);assert chosen and all(s['label_available_at']<r['cutoff'] for r in chosen)
    selection=dict(protocol_hash=p['hash'],model_hash=digest(artifact),selected_ids=[r['bill_id'] for r in chosen],excluded=excluded);save(directory,'selection.json',selection)
    rate=(sum(r['y'] for r in training)+1)/(len(training)+2)
    pairs=[dict(bill_id=r['bill_id'],title=r['title'],family_id=r['family_id'],cutoff=r['cutoff'],input_features=r['x'],probability=predict(artifact,learning.features(r,'structured')),baseline_probability=rate,outcome=r['y'],law=r['law'],source_url=r['source']['url']) for r in chosen]
    metrics=score([r['probability'] for r in pairs],[r['outcome'] for r in pairs]);baseline=score([rate]*len(pairs),[r['outcome'] for r in pairs])
    class_metrics={}
    for outcome in (0,1):
        subset=[r for r in pairs if r['outcome']==outcome]
        class_metrics[str(outcome)]=dict(n=len(subset),metrics=score([r['probability'] for r in subset],[r['outcome'] for r in subset]) if subset else None)
    detection=dict(threshold=.5,true_positive=sum(r['probability']>=.5 and r['outcome']==1 for r in pairs),false_positive=sum(r['probability']>=.5 and r['outcome']==0 for r in pairs),positive=sum(r['outcome'] for r in pairs))
    result=dict(protocol_hash=p['hash'],model_hash=digest(artifact),selection_hash=digest(selection),predictions=pairs,metrics=metrics,baseline=baseline,brier_difference=metrics['brier']-baseline['brier'],interval=cohort.bootstrap(pairs),class_metrics=class_metrics,detection=detection,counts=dict(screened=len(rows),evaluated=len(pairs),positive=sum(r['outcome'] for r in pairs),training=len(training),training_positive=sum(r['y'] for r in training),excluded=len(excluded)),exclusion_reasons=dict(Counter(r['reason'] for r in excluded)),source_documents=len(acquisition['sources']),source_bytes=sum(r['bytes'] for r in acquisition['sources']),inference=s['inference'],release_eligible=False)
    result['hash']=digest(result);save(directory,'result.json',result);print(json.dumps({k:v for k,v in result.items() if k!='predictions'},indent=2));return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run-dir',default=str(ROOT/'data/research-runs/survivor1000-20261105'));p.add_argument('--offline',action='store_true');a=p.parse_args();run(a.run_dir,a.offline)
