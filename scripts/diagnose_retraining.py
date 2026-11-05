"""Descriptive diagnosis using already exposed experiment data only."""
import json
from collections import Counter
from pathlib import Path
from engine.store import ROOT,digest
from engine.survivor_batch import save
from engine.model import predict,score
D=ROOT/'data/research-runs/cross-congress-20261105'
F=json.loads((ROOT/'data/research-runs/expanded-experiments-20261105/frozen-inputs.json').read_text())
R=json.loads((ROOT/'data/research-runs/three-model-20261105/result.json').read_text())
M=json.loads((ROOT/'data/research-runs/three-model-20261105/models.json').read_text())
NAMES=['publication_stage','age','publication_count','time_since_publication','senate','recent_publications']

def profile(rows):
 return dict(n=len(rows),positives=sum(r['y'] for r in rows),congress=dict(Counter(str(r['congress']) for r in rows)),chamber=dict(Counter(r['type'] for r in rows)),stage=dict(Counter(str(r['x'][0]*4) for r in rows)),mean_features={name:sum(r['x'][i] for r in rows)/len(rows) for i,name in enumerate(NAMES)})

def outcome_metrics(rows,key):
 return {str(y):dict(n=len(v),mean_probability=sum(r[key] for r in v)/len(v),brier=sum((r[key]-y)**2 for r in v)/len(v)) for y in (0,1) for v in [[r for r in rows if r['outcome']==y]] if v}

original_ids={r['bill_id'] for r in F['original_training']}
profiles={key:profile(rows) for key,rows in [('original',F['original_training']),('added',[r for r in F['training'] if r['bill_id'] not in original_ids]),('expanded',F['training'])]}
rows=R['predictions'];strata={}
for dimension,fn in [('chamber',lambda r:'s' if r['input_features'][4] else 'hr'),('stage',lambda r:str(r['input_features'][0]*4)),('original_probability',lambda r:'>=0.1' if r['original']>=.1 else '<0.1')]:
 strata[dimension]={}
 for value in sorted(set(map(fn,rows))):
  sub=[r for r in rows if fn(r)==value]
  strata[dimension][value]=dict(n=len(sub),positives=sum(r['outcome'] for r in sub),metrics={key:score([r[key] for r in sub],[r['outcome'] for r in sub]) for key in M})
coefficients={key:dict(raw_feature_weights={name:artifact['weights'][i+1]/artifact['scales'][i] for i,name in enumerate(NAMES)},raw_intercept=artifact['weights'][0]-sum(w*m/s for w,m,s in zip(artifact['weights'][1:],artifact['means'],artifact['scales']))) for key,artifact in M.items() if key!='calibrated'}
report=dict(title='Why expanded training hurt: exposed-data diagnosis',profiles=profiles,coefficients=coefficients,strata=strata,outcome_metrics={key:outcome_metrics(rows,key) for key in M},
 source_result_hash=R['hash'],interpretation='Descriptive attribution, not causal identification. Compare class-specific probability shifts and stage separation; original one-positive training makes coefficient estimates unstable.',release_eligible=False)
report['hash']=digest(report);save(D,'diagnosis.json',report)
print(json.dumps({k:report[k] for k in ('profiles','coefficients','outcome_metrics')},indent=2))
