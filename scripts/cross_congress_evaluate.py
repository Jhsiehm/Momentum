"""Forward-only development folds and locked confirmation for the scale campaign.

No outcomes from reserved confirmation identities are read by development fitting.
"""
import argparse,copy,json,random,math
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from engine import cohort,learning,sample_publication_v2 as pub
from engine.label_investigation import law_identity
from engine.model import predict,score
from engine.store import ROOT,digest,now
from engine.survivor_batch import save
from engine.three_model_experiment import fit_calibration,calibrate
D=ROOT/'data/research-runs/cross-congress-scale-20261105'
MODEL_ORDER=['nested250','nested1000','all_history','recent_congress','calibrated_all_history']


def unique(rows,groups,forbidden=()):
 used=set(forbidden);result=[]
 for row in rows:
  family=groups[row['bill_id']]
  if row['exclusion'] or family in used:continue
  used.add(family);result.append(dict(row,family_id=family))
 return result


def fit(rows):
 return learning._fit([dict(r,x=learning.features(r,'structured')) for r in rows],.2)


def train_models(rows):
 ordered=sorted(rows,key=lambda r:digest(r['bill_id']))
 latest=max(r['congress'] for r in rows)
 calibration=[r for i,r in enumerate(ordered) if i%5==0]
 core=[r for i,r in enumerate(ordered) if i%5!=0]
 if len({r['y'] for r in calibration})!=2 or len({r['y'] for r in core})!=2:
  raise ValueError('Disjoint calibration/core lack both outcome classes')
 base=fit(core)
 return dict(nested250=fit(ordered[:250]),nested1000=fit(ordered[:1000]),all_history=fit(ordered),recent_congress=fit([r for r in ordered if r['congress']==latest]),
  calibrated_all_history=dict(base=base,calibration=fit_calibration([predict(base,r['x']) for r in calibration],[r['y'] for r in calibration]),core_ids=[r['bill_id'] for r in core],calibration_ids=[r['bill_id'] for r in calibration]))


def probability(key,artifact,x):
 return calibrate(artifact['calibration'],predict(artifact['base'],x)) if key=='calibrated_all_history' else predict(artifact,x)


def acquire_label_dates(directory=D):
 directory=Path(directory);a=json.loads((directory/'acquisition.json').read_text());sources=pub.Sources(directory/'label-dates')
 candidates=[r for r in a['rows'] if r.get('law') and not r['exclusion']]
 def collect(row):
  try:
   c=row['congress'];law=row['law'];mods,proof=cohort.package_audit(sources,f"PLAW-{c}publ{law['law']}")
   assert law_identity(mods,c,law['law'])==law,'Individual law identity/date mismatch'
   return row['bill_id'],dict(available_at=proof['available_at'],proof=proof),None
  except Exception as e:return row['bill_id'],None,str(e)
 proofs={};failures=[]
 with ThreadPoolExecutor(max_workers=4) as pool:
  for bid,proof,error in pool.map(collect,candidates):
   if error:failures.append(dict(bill_id=bid,error=error))
   else:proofs[bid]=proof
 result=dict(proofs=proofs,failures=failures,sources=sources.manifest());save(directory,'positive-date-evidence.json' if not failures else 'positive-date-blocked.json',result)
 return result


def load_rows(initial_only=False):
 dirs=[D]
 if not initial_only and (D/'expansion-decision.json').exists() and json.loads((D/'expansion-decision.json').read_text())['expand']:dirs.append(ROOT/'data/research-runs/cross-congress-reserve-20261105')
 rows=[];proofs={};failures=[]
 for directory in dirs:
  acquisition=json.loads((directory/'acquisition.json').read_text());assert not acquisition['failures']
  rows+=acquisition['rows'];e=json.loads((directory/'positive-date-evidence.json').read_text());proofs.update(e['proofs']);failures+=e['failures']
 assert not failures
 calendars=json.loads((D/'label-evidence.json').read_text())['proofs']
 for row in rows:
  if row.get('law') and not row['exclusion']:assert row['bill_id'] in proofs,'Missing required dated positive law proof'
  row['label_available_at']=max(calendars[str(row['congress'])]['available_at'],proofs.get(row['bill_id'],{}).get('available_at',''))
 return rows


def make_split(rows,test_congress,groups):
 evaluation=unique([r for r in rows if r['congress']==test_congress],groups)
 if not evaluation:return [],[]
 cutoff=min(r['cutoff'] for r in evaluation)
 train=unique([r for r in rows if r['congress']<test_congress and r['label_available_at']<cutoff],groups,{r['family_id'] for r in evaluation})
 return train,evaluation


def evaluate():
 rows=load_rows();groups=cohort.family_groups(rows);folds=[]
 protocol=json.loads((D/'protocol.json').read_text());spec=protocol['spec'];gate=spec['minimum_fold']
 for c in spec['forward_folds']:
  training,test=make_split(rows,c,groups)
  counts=dict(training=len(training),training_positives=sum(r['y'] for r in training),evaluation=len(test),evaluation_positives=sum(r['y'] for r in test))
  if any(counts[k]<v for k,v in gate.items()):
   save(D,f'fold-{c}-blocked.json',dict(counts=counts,required=gate));raise ValueError(f'Fold{c} insufficient: {counts}')
  models=train_models(training);rate=(sum(r['y'] for r in training)+1)/(len(training)+2)
  save(D,f'fold-{c}-models.json',models)
  pairs=[dict(bill_id=r['bill_id'],family_id=r['family_id'],cutoff=r['cutoff'],outcome=r['y'],input_features=r['x'],baseline_probability=rate,**{k:probability(k,m,r['x']) for k,m in models.items()}) for r in test]
  metrics={k:score([r[k] for r in pairs],[r['outcome'] for r in pairs]) for k in models};baseline=score([rate]*len(test),[r['y'] for r in test])
  fold=dict(congress=c,counts=counts,training_ids=[r['bill_id'] for r in training],latest_training_label=max(r['label_available_at'] for r in training),first_test_checkpoint=min(r['cutoff'] for r in test),models_hash=digest(models),predictions=pairs,metrics=metrics,baseline=baseline)
  save(D,f'fold-{c}.json',fold);folds.append(fold)
 skills={k:sum(1-f['metrics'][k]['brier']/f['baseline']['brier'] for f in folds)/len(folds) for k in MODEL_ORDER}
 selected=max(MODEL_ORDER,key=lambda k:skills[k])
 # Fit final challenger from113–117. Latest label availability gates confirmation rows later.
 train=unique(rows,groups);models=train_models(train)
 locked_at=json.loads((D/'challenger-lock.json').read_text())['locked_at'] if (D/'challenger-lock.json').exists() else now()
 lock=dict(selected=selected,mean_fold_skill=skills,artifact=models[selected],training_ids=[r['bill_id'] for r in train],training_families=[r['family_id'] for r in train],training_rows_hash=digest(train),latest_training_label=max(r['label_available_at'] for r in train),locked_at=locked_at,protocol_hash=protocol['hash'],release_eligible=False)
 lock['hash']=digest(lock);save(D,'challenger-lock.json',lock);save(D,'final-training.json',train)
 # Sensitivity before confirmation: resample paired development errors, not future outcomes.
 deltas=[(r[selected]-r['outcome'])**2-(r['baseline_probability']-r['outcome'])**2 for f in folds for r in f['predictions']]
 mean=sum(deltas)/len(deltas);sd=math.sqrt(sum((d-mean)**2 for d in deltas)/(len(deltas)-1))
 original=json.loads((ROOT/'data/research-runs/survivor1000-20261105/artifact.json').read_text())
 reference=folds[-1]['predictions']
 original_errors=[(predict(original,r['input_features'])-r['outcome'])**2 for r in reference]
 diffs=[(r[selected]-r['outcome'])**2-e for r,e in zip(reference,original_errors)]
 observed_mean=sum(diffs)/len(diffs);target=.02*sum(original_errors)/len(original_errors)
 centered=[d-observed_mean-target for d in diffs];rng=random.Random(202611055000);detected=0
 for _ in range(500):
  draw=[rng.choice(centered) for _ in range(3500)];avg=sum(draw)/len(draw)
  se=math.sqrt(sum((d-avg)**2 for d in draw)/(len(draw)-1)/len(draw))
  detected+=avg+1.96*se<0
 sensitivity=dict(n=len(deltas),mean_challenger_minus_rate=mean,sd=sd,approximate_95_half_width_at_3500_eligible=1.96*sd/math.sqrt(3500),
  simulation=dict(replicates=500,seed=202611055000,assumed_eligible=3500,assumed_relative_brier_gain=.02,reference='Exposed117 paired errors against fixed original survivor',normal_interval_detection_fraction=detected/500),
  note='Resampling sensitivity conditional on exposed117 error distribution and assumed2% effect; not a guaranteed prospective power calculation. Congress shifts and model-selection uncertainty remain.')
 result=dict(protocol_hash=protocol['hash'],folds=[{k:v for k,v in f.items() if k!='predictions'} for f in folds],skills=skills,selected=selected,lock_hash=lock['hash'],sensitivity=sensitivity,release_eligible=False)
 result['hash']=digest(result);save(D,'development-result.json',result);print(json.dumps(dict(selected=selected,skills=skills,sensitivity=sensitivity),indent=2))
 return result


if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--labels',action='store_true');p.add_argument('--run-dir',default=str(D));args=p.parse_args()
 if args.labels:print(json.dumps({k:v for k,v in acquire_label_dates(args.run_dir).items() if k not in ('proofs','sources')},indent=2))
 else:evaluate()
