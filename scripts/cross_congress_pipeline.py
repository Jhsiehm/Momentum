"""Resumable campaign coordinator; count-based acquisition, then locked testing.
Never schedules itself, promotes a model, or changes the retained survivor.
"""
import copy,hashlib,json,subprocess,sys,time,threading
from pathlib import Path
from engine.store import ROOT,Store,digest,now
from engine.research_lease import lease
from engine.survivor_batch import save,select
from engine import cohort
from engine.model import predict,score
from scripts.cross_congress_evaluate import D,unique,load_rows,evaluate,acquire_label_dates,probability,make_split
OWNER='cross-congress-20261105'


def renewal(stop):
 store=Store()
 try:
  while not stop.is_set():
   result=lease(store,'acquire',OWNER)
   if not result['granted']:raise RuntimeError('Research lease held by another owner')
   stop.wait(120)
 finally:store.close()


def command(args,log):
 with open(log,'a') as out:
  result=subprocess.run([sys.executable,'-m',*args],cwd=ROOT,stdout=out,stderr=subprocess.STDOUT)
 if result.returncode:raise RuntimeError('Command failed: '+' '.join(args)+'; see '+str(log))


def stage(status,**kwargs):
 store=Store()
 try:granted=lease(store,'acquire',OWNER)['granted']
 finally:store.close()
 if not granted:raise RuntimeError('Another research owner holds the lease')
 body=dict(status=status,updated_at=now(),**kwargs)
 (D/'pipeline-progress.json').write_text(json.dumps(body,indent=2));print(json.dumps(body),flush=True)


def ensure_acquisition(directory):
 if not (directory/'acquisition.json').exists():
  command(['engine.cross_congress','--run-dir',str(directory)],directory/'resume.log')
 value=json.loads((directory/'acquisition.json').read_text());assert not value['failures']
 return value


def derive_directory(name,ids,congresses,base):
 target=ROOT/'data/research-runs'/name;target.mkdir(exist_ok=True)
 if (target/'protocol.json').exists():return target
 spec=copy.deepcopy(base['spec']);spec.update(candidate_ids=ids,congresses=congresses,registered_at=now(),parent_protocol_hash=base['hash'],purpose=name)
 for c in congresses:
  source=D/f'laws-{c}.json'
  if not source.exists():source=ROOT/'data/research-runs/cross-congress-20261105'/f'laws-{c}.json'
  if not source.exists():
   from engine import sample_publication_v2 as pub
   laws,proofs=pub.law_census(pub.Sources(target),c,274);value=dict(laws=laws,proofs=proofs)
  else:value=json.loads(source.read_text())
  save(target,f'laws-{c}.json',value)
 spec['law_hashes']={str(c):digest(json.loads((target/f'laws-{c}.json').read_text())) for c in congresses}
 save(target,'protocol.json',dict(spec=spec,hash=digest(spec)))
 return target


def confirm(directory):
 base=json.loads((D/'protocol.json').read_text());lock=json.loads((D/'challenger-lock.json').read_text())
 assert digest({k:v for k,v in lock.items() if k!='hash'})==lock['hash']
 acquisition=json.loads((directory/'acquisition.json').read_text());assert not acquisition['failures']
 train=json.loads((D/'final-training.json').read_text());assert digest(train)==lock['training_rows_hash']
 original=json.loads((ROOT/'data/research-runs/survivor1000-20261105/artifact.json').read_text())
 prior={}
 for pattern in ('data/cohorts/*/cohort.json','data/research-runs/*/acquisition.json'):
  for path in ROOT.glob(pattern):
   if path.parent==directory:continue
   for row in json.loads(path.read_text()).get('rows',[]):
    if 'related' in row:prior[row['bill_id']]=row
 original_train=json.loads((ROOT/'data/research-runs/survivor1000-20261105/training.json').read_text())
 selected,excluded=select(acquisition['rows'],train+original_train,list(prior.values()))
 timely=[]
 for row in selected:
  if row['cutoff']<=lock['latest_training_label']:excluded.append(dict(bill_id=row['bill_id'],reason='Challenger training labels unavailable by cutoff'))
  else:timely.append(row)
 selected=timely;assert selected
 save(directory,'selection.json',dict(selected_ids=[r['bill_id'] for r in selected],excluded=excluded))
 pairs=[dict(bill_id=r['bill_id'],family_id=r['family_id'],cutoff=r['cutoff'],outcome=r['y'],input_features=r['x'],probability=probability(lock['selected'],lock['artifact'],r['x']),baseline_probability=predict(original,r['x'])) for r in selected]
 challenger=score([r['probability'] for r in pairs],[r['outcome'] for r in pairs]);survivor=score([r['baseline_probability'] for r in pairs],[r['outcome'] for r in pairs]);interval=cohort.bootstrap(pairs)
 positive=sum(r['outcome'] for r in pairs);relative=1-challenger['brier']/survivor['brier']
 signal=relative>=.02 and interval['upper_95']<0 and challenger['log_loss']<=survivor['log_loss'] and positive>=50
 result=dict(challenger=lock['selected'],lock_hash=lock['hash'],predictions=pairs,metrics=dict(challenger=challenger,original=survivor),interval=interval,relative_brier_improvement=relative,
 counts=dict(screened=len(acquisition['rows']),evaluated=len(pairs),positive=positive,excluded=len(excluded)),exploratory_success=signal,release_eligible=False,human_certified=False,
 conclusion='Historical exploratory signal only; same118Congress exposure remains, no production promotion.' if signal else 'Preserve survivor; challenger improvement not established under registered criteria.')
 result['hash']=digest(result);save(directory,'result.json',result);return result


def run(wait_initial=False):
 stop=threading.Event();worker=threading.Thread(target=renewal,args=(stop,),daemon=True);worker.start()
 try:
  base=json.loads((D/'protocol.json').read_text());assert digest(base['spec'])==base['hash']
  if wait_initial:
   stage('waiting_initial_acquisition')
   while not any((D/name).exists() for name in ('acquisition.json','acquisition-blocked.json')):time.sleep(15)
  stage('audit_initial');ensure_acquisition(D)
  stage('historical_positive_law_dates')
  if not (D/'positive-date-evidence.json').exists():
   proof=acquire_label_dates(D);assert not proof['failures'],'Positive law proof failure'
  rows=load_rows(initial_only=True);groups=cohort.family_groups(rows)
  training,development=make_split(rows,117,groups)
  decision=dict(training_positives=sum(r['y'] for r in training),development_positives=sum(r['y'] for r in development))
  decision['expand']=decision['training_positives']<200 or decision['development_positives']<50
  if (D/'expansion-decision.json').exists():decision=json.loads((D/'expansion-decision.json').read_text())
  else:save(D,'expansion-decision.json',decision)
  if decision['expand']:
   stage('acquire_registered_reserve',**decision)
   reserve=derive_directory('cross-congress-reserve-20261105',base['spec']['reserve_ids'],list(range(113,118)),base)
   ensure_acquisition(reserve)
   if not (reserve/'positive-date-evidence.json').exists():
    proof=acquire_label_dates(reserve);assert not proof['failures']
  rows=load_rows();groups=cohort.family_groups(rows)
  train,dev=make_split(rows,117,groups)
  counts=dict(training_positives=sum(r['y'] for r in train),development_positives=sum(r['y'] for r in dev))
  if counts['training_positives']<200 or counts['development_positives']<50:
   stage('blocked_insufficient_after_cap',**counts);return
  stage('forward_development');evaluate()
  stage('locked_challenger_confirmation')
  confirmation=derive_directory('cross-congress-confirmation-20261105',base['spec']['confirmation_ids'],[118],base)
  ensure_acquisition(confirmation);result=confirm(confirmation)
  stage('completed_needs_verification',result_hash=result['hash'],counts=result['counts'])
 except Exception as error:
  stage('blocked',error=str(error));raise
 finally:
  stop.set();worker.join(timeout=5)

if __name__=='__main__':run('--wait-initial' in sys.argv)
