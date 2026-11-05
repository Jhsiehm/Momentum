"""Frozen original-data survivor, twenty-case historical development diagnostic."""
import argparse,copy,json,re,hashlib
from collections import Counter
from . import cohort,sample_publication_v2 as pub,learning
from .model import predict,score
from .store import ROOT,digest
D=ROOT/'data/research-runs/survivor20-20261105'

def save(name,value):
    path=D/name;body=json.dumps(value,indent=2,sort_keys=True)+'\n'
    if path.exists():assert json.loads(path.read_text())==value,'Frozen artifact mismatch: '+name
    else:path.write_text(body)

def run(offline=False):
    p=json.loads((D/'protocol.json').read_text());s=p['spec'];assert digest(s)==p['hash']
    population=json.loads((D/'population.json').read_text());assert digest(population)==s['population_hash']
    artifact=json.loads((D/'artifact.json').read_text());train=json.loads((D/'training.json').read_text());exposed=json.loads((D/'exposed.json').read_text())
    assert digest(artifact)==s['model_hash'] and digest(train)==s['training_hash'] and digest(exposed)==s['exposed_rows_hash']
    # Refit only to verify identity; predictions below exclusively use the locked artifact.
    transformed=[dict(r,x=learning.features(r,'structured')) for r in train];check=learning._fit(transformed,.2);check.update(policy='structured',training_hash=digest(transformed));assert check==artifact
    dependencies={str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted((ROOT/'engine').glob('*.py'))};save('dependencies.json',dependencies)
    old=cohort.Sources(pub.DIRECTORY,True);laws,lawproofs=pub.law_census(old,118,274);labels={x['bill_id']:x for x in laws};sources=cohort.Sources(D,offline);rows=[];failures=[]
    for i,bid in enumerate(s['candidate_ids'],1):
        try:
            m=re.fullmatch(r'(118)-(hr|s)(\d+)',bid);rows.append(pub.sample_bill(sources,118,m[2],int(m[3]),{'age_days':180},labels))
        except Exception as e:failures.append(dict(bill_id=bid,error=str(e)))
        if not offline and i%10==0:print('Audited',i,'/40',flush=True)
    acquired=dict(rows=rows,failures=failures,sources=sources.manifest(),law_sources=lawproofs);save('acquisition.json',acquired)
    assert not failures,'Source failures block scoring'
    groups=cohort.family_groups(train+exposed+rows);forbidden={groups[r['bill_id']] for r in train+exposed};chosen=[];excluded=[];used=set();surplus=[]
    for row in rows:
        r=copy.deepcopy(row);r['family_id']=groups[r['bill_id']];reason=r['exclusion']
        if not reason and r['family_id'] in forbidden:reason='Known prior/training family overlap'
        if not reason and r['family_id'] in used:reason='Duplicate selected family'
        if reason:excluded.append(dict(bill_id=r['bill_id'],reason=reason));continue
        if len(chosen)==20:surplus.append(r['bill_id']);continue
        chosen.append(r);used.add(r['family_id'])
    assert len(chosen)==20,'Fewer than20 eligible; no unregistered replacement'
    assert all('2021-05-08T23:59:59Z'<r['cutoff'] for r in chosen)
    frozen=dict(protocol_hash=p['hash'],model_hash=digest(artifact),selected_ids=[r['bill_id'] for r in chosen],excluded=excluded,eligible_surplus_ids=surplus);save('selection.json',frozen)
    rate=(sum(r['y'] for r in train)+1)/(len(train)+2)
    pairs=[dict(bill_id=r['bill_id'],title=r['title'],family_id=r['family_id'],cutoff=r['cutoff'],input_features=r['x'],probability=predict(artifact,learning.features(r,'structured')),baseline_probability=rate,outcome=r['y'],law=r['law'],source_url=r['source']['url']) for r in chosen]
    metrics=score([r['probability'] for r in pairs],[r['outcome'] for r in pairs]);baseline=score([rate]*20,[r['outcome'] for r in pairs])
    result=dict(protocol_hash=p['hash'],model_hash=digest(artifact),selection_hash=digest(frozen),predictions=pairs,metrics=metrics,baseline=baseline,brier_difference=metrics['brier']-baseline['brier'],interval=cohort.bootstrap(pairs),counts=dict(screened=40,evaluated=20,positive=sum(r['outcome'] for r in pairs),training=len(train),training_positive=sum(r['y'] for r in train),excluded=len(excluded),surplus=len(surplus)),exclusion_reasons=dict(Counter(r['reason'] for r in excluded)),source_documents=len(acquired['sources']),inference=s['inference'],release_eligible=False)
    result['hash']=digest(result);save('result.json',result);print(json.dumps({k:v for k,v in result.items() if k!='predictions'},indent=2));return result
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--offline',action='store_true');args=parser.parse_args();run(args.offline)
