"""Separate arithmetic/provenance verification for the completed scale campaign."""
import hashlib,json,math
from pathlib import Path
from engine.store import ROOT,digest
from engine import cohort
from engine.survivor_batch import save
from scripts.cross_congress_evaluate import D,load_rows


def direct(artifact,x):
 z=artifact['weights'][0]
 for w,v,m,s in zip(artifact['weights'][1:],x,artifact['means'],artifact['scales']):z+=w*(v-m)/s
 return 1/(1+math.exp(-max(-35,min(35,z))))


def probability(key,artifact,x):
 if key!='calibrated_all_history':return direct(artifact,x)
 p=direct(artifact['base'],x);p=min(1-1e-12,max(1e-12,p));c=artifact['calibration'];z=c['intercept']+c['slope']*math.log(p/(1-p))
 return 1/(1+math.exp(-max(-35,min(35,z))))


def verify_scores(pairs,key,metrics):
 probabilities=[r[key] for r in pairs];outcomes=[r['outcome'] for r in pairs]
 brier=sum((p-y)**2 for p,y in zip(probabilities,outcomes))/len(pairs)
 loss=-sum(y*math.log(max(1e-12,min(1-1e-12,p)))+(1-y)*math.log(1-max(1e-12,min(1-1e-12,p))) for p,y in zip(probabilities,outcomes))/len(pairs)
 assert abs(brier-metrics['brier'])<1e-12 and abs(loss-metrics['log_loss'])<1e-12


def verify():
 root=ROOT/'data/research-runs';directories=[D,root/'cross-congress-confirmation-20261105']
 if json.loads((D/'expansion-decision.json').read_text())['expand']:directories.append(root/'cross-congress-reserve-20261105')
 verified_sources=0;source_bytes=0
 for directory in directories:
  protocol=json.loads((directory/'protocol.json').read_text());assert digest(protocol['spec'])==protocol['hash']
  acquisition=json.loads((directory/'acquisition.json').read_text());assert not acquisition['failures']
  assert [r['bill_id'] for r in acquisition['rows']]==protocol['spec']['candidate_ids']
  for bundle,base in [(acquisition,directory)]+([(json.loads((directory/'positive-date-evidence.json').read_text()),directory/'label-dates')] if (directory/'positive-date-evidence.json').exists() else []):
   for source in bundle['sources']:
    raw=(base/'sources'/(hashlib.sha256(source['url'].encode()).hexdigest()+'.raw')).read_bytes()
    assert len(raw)==source['bytes'] and hashlib.sha256(raw).hexdigest()==source['sha256']
    verified_sources+=1;source_bytes+=len(raw)
 rows=load_rows();by_id={r['bill_id']:r for r in rows};groups=cohort.family_groups(rows);predictions=0
 for c in range(114,118):
  fold=json.loads((D/f'fold-{c}.json').read_text());models=json.loads((D/f'fold-{c}-models.json').read_text())
  assert digest(models)==fold['models_hash']
  training=[by_id[bid] for bid in fold['training_ids']]
  assert all(r['congress']<c and r['label_available_at']<fold['first_test_checkpoint'] for r in training)
  assert not {groups[r['bill_id']] for r in training}&{r['family_id'] for r in fold['predictions']}
  for r in fold['predictions']:
   for key,artifact in models.items():
    assert abs(probability(key,artifact,r['input_features'])-r[key])<1e-12;predictions+=1
  for key in models:verify_scores(fold['predictions'],key,fold['metrics'][key])
 confirmation=directories[1];r=json.loads((confirmation/'result.json').read_text());lock=json.loads((D/'challenger-lock.json').read_text())
 assert digest({k:v for k,v in lock.items() if k!='hash'})==lock['hash']==r['lock_hash']
 assert digest({k:v for k,v in r.items() if k!='hash'})==r['hash']
 original=json.loads((root/'survivor1000-20261105/artifact.json').read_text())
 cp=json.loads((confirmation/'protocol.json').read_text());assert lock['locked_at']<=cp['spec']['registered_at']
 for pair in r['predictions']:
  assert lock['latest_training_label']<pair['cutoff']
  assert abs(probability(lock['selected'],lock['artifact'],pair['input_features'])-pair['probability'])<1e-12
  assert abs(direct(original,pair['input_features'])-pair['baseline_probability'])<1e-12;predictions+=2
 verify_scores(r['predictions'],'probability',r['metrics']['challenger']);verify_scores(r['predictions'],'baseline_probability',r['metrics']['original'])
 assert cohort.bootstrap(r['predictions'])==r['interval']
 report=dict(status='passed',verified_sources=verified_sources,source_bytes=source_bytes,verified_probabilities=predictions,result_hash=r['hash'],checks=['Source SHA256 and byte length','Frozen protocol hashes and candidate identities','Forward label-time and family separation','Separate probability/Brier/log-loss arithmetic','Challenger locked before confirmation registration','Repeated conditional bootstrap'],human_certified=False,release_eligible=False)
 save(D,'verification.json',report);print(json.dumps(report,indent=2));return report

if __name__=='__main__':verify()
