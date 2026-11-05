"""Freeze expansion and future evaluation identities before acquisition/scoring."""
import copy,json,random,shutil,hashlib
from pathlib import Path
from engine.store import ROOT,digest,now
from engine.cross_congress import DIRECTORY,excluded_ids
from engine.survivor_batch import save
D=ROOT/'data/research-runs/cross-congress-scale-20261105'
D.mkdir(exist_ok=True)
assert not (D/'protocol.json').exists(),'Already registered'
base=json.loads((DIRECTORY/'protocol.json').read_text())
summary=json.loads((DIRECTORY/'summary.json').read_text())
evidence=json.loads((ROOT/'data/research-runs/cross-congress-labels-20261105/calendar-evidence-v2.json').read_text())
assert not evidence['failures'] and not summary['failures']
assert all(v['eligible']>=50 for v in summary['counts'].values()),'Evidence coverage insufficient'
inv=json.loads((DIRECTORY/'inventory.json').read_text());excluded=excluded_ids()
populations={str(c):sorted(b for b in inv['bill_ids'] if b.startswith(str(c)+'-') and b not in excluded) for c in range(113,119)}
rng=random.Random(2026110515000)
# Fixed prefixes make all acquisition increases nested and outcome-independent.
orders={c:rng.sample(ids,len(ids)) for c,ids in populations.items()}
initial=[bid for c in range(113,118) for bid in orders[str(c)][:3000]]
reserve=[bid for c in range(113,118) for bid in orders[str(c)][3000:5000]]
holdout=orders['118'][:5000]
spec=copy.deepcopy(base['spec']);spec.update(registered_at=now(),purpose='Representative expanded historical development corpus; protected new118 identities reserved separately',candidate_ids=initial,
 seed=2026110515000,populations_hash=digest(populations),reserve_ids=reserve,confirmation_ids=holdout,
 initial_count=15000,maximum_development_count=25000,confirmation_count=5000,
 expansion_gate='After all15000 audited and family/temporal proof checks: if fewer than200 usable113–116 training positives OR50 usable117 development positives, acquire all10000 frozen reserves. No outcome/model-performance stopping. Cap25000, report insufficiency.',
 nested_training_sizes=[250,1000,'all'],models=['nested250','nested1000','all_history','recent_congress','calibrated_all_history'],
 model_settings=dict(l2=.2,calibration='Existing monotone affine-logit, iterations2000 lr0.1 ridge0.01, disjoint20% family split of earlier data; no tuning'),
 forward_folds=[114,115,116,117],selection='Equal-weight mean fold Brier skill versus fold training-rate baseline; require all4 folds, tie-break fixed model order. Select one challenger before confirmation acquisition.',
 minimum_fold=dict(training=200,training_positives=5,evaluation=200,evaluation_positives=10),
 confirmation='5000 reserved118 identities; original survivor versus one locked challenger only. Exclude all known prior/development/training families. Same-Congress retrospective exposure remains; not untouched temporal/prospective validation.',
 success='Exploratory challenger signal requires >=2% lower confirmation Brier, paired95% interval below0, no worse log loss, >=50 positive confirmation outcomes, all provenance/replay checks. Still no production promotion or human-gate bypass.',
 insufficiency='If development evidence insufficient after reserve, do not score or open confirmation. Record required further acquisition. Confirmation insufficiency yields inconclusive, never outcome-driven extensions.',
 feature_addition='Deferred: no newly audited historical feature available. No contemporary metadata substituted.',
 simulation='Before confirmation, compute resampling-based sensitivity on exposed development paired errors; descriptive design sensitivity, not guaranteed power.',
 census_corrections='117 Public Law354: NARA s4296 corrected to s4926 using finalcalendar and individual law metadata; old runs unchanged',
 label_evidence_hash=evidence['hash'])
for c in range(113,118):
 value=json.loads((DIRECTORY/f'laws-{c}.json').read_text())
 corrections=evidence['proofs'][str(c)]['corrections']
 for fix in corrections:
  value['laws']=[fix['corrected'] if r['law']==fix['original']['law'] else r for r in value['laws']]
 value['adjudications']=corrections
 save(D,f'laws-{c}.json',value)
spec['law_hashes']={str(c):digest(json.loads((D/f'laws-{c}.json').read_text())) for c in range(113,118)}
deps={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'engine').glob('*.py'))+sorted((ROOT/'scripts').glob('*cross_congress*.py'))}
spec['dependencies_hash']=digest(deps)
for name,value in [('populations',populations),('orders',orders),('dependencies',deps),('label-evidence',evidence)]:save(D,name+'.json',value)
save(D,'protocol.json',dict(spec=spec,hash=digest(spec)))
print(json.dumps(dict(protocol_hash=digest(spec),initial=len(initial),reserves=len(reserve),confirmation=len(holdout)),indent=2))
