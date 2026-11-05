"""Frozen survivor, monotone calibration and expanded-training comparison.

Registration fits using earlier-Congress rows only, before acquiring evaluation
sources. The historical follow-up is exploratory and never promotes a model.
"""
import argparse
import hashlib
import json
import math
import random
import re
import time
from collections import Counter
from pathlib import Path
from . import cohort, learning, sample_publication_v2 as pub, sampling
from .model import predict, score, sigmoid
from .store import ROOT, Store, digest, now
from .survivor_batch import save, select

CALIBRATION = dict(iterations=2000, learning_rate=.1, ridge=.01)
DEFAULT = ROOT/'data/research-runs/three-model-20261105'


def logit(p):
    p = min(1-1e-12, max(1e-12, p))
    return math.log(p/(1-p))


def calibrate(artifact, probability):
    return sigmoid(artifact['intercept'] + artifact['slope']*logit(probability))


def fit_calibration(probabilities, outcomes):
    if len(probabilities) != len(outcomes) or set(outcomes) != {0, 1}:
        raise ValueError('Calibration requires paired outcomes of both classes')
    xs = [logit(p) for p in probabilities]
    a, b = 0., 1.
    n = len(xs)
    for _ in range(CALIBRATION['iterations']):
        errors = [sigmoid(a+b*x)-y for x,y in zip(xs,outcomes)]
        da = sum(errors)/n + CALIBRATION['ridge']*a
        db = sum(e*x for e,x in zip(errors,xs))/n + CALIBRATION['ridge']*(b-1)
        a -= CALIBRATION['learning_rate']*da
        b = max(0., b-CALIBRATION['learning_rate']*db)
    return dict(intercept=a, slope=b, parameters=CALIBRATION)


def fit_models(training, original, calibration):
    ids = {r['bill_id'] for r in original}
    assert not ids.intersection(r['bill_id'] for r in calibration)
    assert {r['bill_id'] for r in training} == ids | {r['bill_id'] for r in calibration}
    groups = cohort.family_groups(training)
    assert not {groups[r['bill_id']] for r in original}.intersection(groups[r['bill_id']] for r in calibration)
    def fit(rows):
        transformed = [dict(r,x=learning.features(r,'structured')) for r in rows]
        artifact = learning._fit(transformed,.2)
        artifact.update(policy='structured',training_hash=digest(transformed))
        return artifact
    survivor = fit(original)
    adjusted = fit_calibration([predict(survivor, r['x']) for r in calibration], [r['y'] for r in calibration])
    return dict(original=survivor, calibrated=adjusted, retrained=fit(training))


def register(directory):
    directory = Path(directory)
    if (directory/'protocol.json').exists():
        raise ValueError('Already registered; use run/replay without overwriting')
    directory.mkdir(parents=True,exist_ok=True)
    frozen = json.loads((ROOT/'data/research-runs/expanded-experiments-20261105/frozen-inputs.json').read_text())
    training, original = frozen['training'], frozen['original_training']
    original_ids = {r['bill_id'] for r in original}
    calibration = [r for r in training if r['bill_id'] not in original_ids]
    assert all(r['congress'] in (114,116) for r in training)
    assert all(r['congress'] == 116 for r in calibration)
    models = fit_models(training,original,calibration)
    assert models['original'] == json.loads((ROOT/'data/research-runs/survivor1000-20261105/artifact.json').read_text())
    store = Store()
    try:
        inventory = sampling.list_inventories(store)[0]
        excluded = {b['bill_id'] for b in store.bills('official')}
    finally:
        store.close()
    exposed = {}
    for path in list((ROOT/'data/cohorts').glob('*/cohort.json')) + list((ROOT/'data/research-runs').glob('*/acquisition.json')):
        for row in json.loads(path.read_text()).get('rows',[]):
            excluded.add(row['bill_id'])
            if row.get('congress') == 118 and 'related' in row:
                exposed[row['bill_id']] = row
    for path in (ROOT/'data/research-runs').glob('*/protocol.json'):
        spec = json.loads(path.read_text()).get('spec',{})
        for key in ('candidate_ids','bill_ids','development_ids','confirmation_ids','ids'):
            excluded.update(x for x in spec.get(key,[]) if isinstance(x,str))
    population = sorted(b for b in inventory['bill_ids'] if b.startswith('118-') and b not in excluded)
    seed = 202611053000
    candidates = random.Random(seed).sample(population,1000)
    artifacts = dict(training=training,original_training=original,calibration_training=calibration,
                     models=models,exposed=list(exposed.values()),population=population)
    spec = dict(id=directory.name,registered_at=now(),candidate_ids=candidates,seed=seed,
        population_count=len(population),hashes={k:digest(v) for k,v in artifacts.items()},
        age_days=180,label_available_at='2021-05-08T23:59:59Z',
        target='Own-bill public-law enactment before Congress end',
        calibration=CALIBRATION,calibration_method='Monotone affine-logit; initialize(0,1), identity-anchored ridge; no tuning',
        training_counts={k:dict(n=len(v),positives=sum(r['y'] for r in v)) for k,v in artifacts.items() if k in ('training','original_training','calibration_training')},
        selection='All eligible among fixed1000; no replacements/early stopping. Exclude prior/training family overlaps and duplicate families in random order.',
        primary='Paired Brier: calibrated minus original; retrained minus original; conditional family bootstrap2000 seed20261024. Two exploratory comparisons, no multiplicity-adjusted confirmatory claim.',
        secondary='Log loss; reliability; outcome-specific Brier; original Beta(1,1) rate reference',
        source_failures='Any required failure blocks all scoring; same-ID cached retries only',
        inference='Historical same118Congress development follow-up, not untouched final or prospective validation. Prior broad calendar exposure and repeated comparisons; only5 calibration positives. No automatic promotion.',
        budget='Manual1000 candidate comparison; official sources only; no paid calls or scheduled-budget changes',
        release_eligible=False)
    for key,value in artifacts.items(): save(directory,key+'.json',value)
    # Freeze executable dependencies before any evaluation acquisition.
    dependencies = {}
    for path in sorted((ROOT/'engine').glob('*.py')):
        dependencies[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
        snapshot=directory/'dependency-snapshot';snapshot.mkdir(exist_ok=True)
        (snapshot/path.name).write_bytes(path.read_bytes())
    spec['dependencies_hash']=digest(dependencies)
    save(directory,'dependencies.json',dependencies)
    save(directory,'protocol.json',dict(spec=spec,hash=digest(spec)))
    print(json.dumps(dict(protocol_hash=digest(spec),counts=spec['training_counts'],calibration=models['calibrated'],population=len(population)),indent=2))


def run(directory, offline=False):
    directory = Path(directory)
    protocol = json.loads((directory/'protocol.json').read_text());s=protocol['spec']
    assert digest(s)==protocol['hash']
    artifacts={k:json.loads((directory/(k+'.json')).read_text()) for k in s['hashes']}
    assert all(digest(v)==s['hashes'][k] for k,v in artifacts.items())
    deps=json.loads((directory/'dependencies.json').read_text())
    assert digest(deps)==s['dependencies_hash']
    assert all(hashlib.sha256((ROOT/'engine'/k).read_bytes()).hexdigest()==v for k,v in deps.items())
    training,original,calibration,models,exposed=[artifacts[k] for k in ('training','original_training','calibration_training','models','exposed')]
    assert models==fit_models(training,original,calibration)
    assert random.Random(s['seed']).sample(artifacts['population'],len(s['candidate_ids']))==s['candidate_ids']
    laws,lawproofs=pub.law_census(cohort.Sources(pub.DIRECTORY,True),118,274)
    labels={r['bill_id']:r for r in laws};sources=pub.Sources(directory,offline);rows=[];failures=[]
    for i,bid in enumerate(s['candidate_ids'],1):
        try:
            match=re.fullmatch(r'118-(hr|s)(\d+)',bid);assert match
            rows.append(pub.sample_bill(sources,118,match[1],int(match[2]),{'age_days':s['age_days']},labels))
        except Exception as error:
            failures.append(dict(bill_id=bid,error=str(error)))
        if not offline:
            (directory/'progress.json').write_text(json.dumps(dict(completed=i,total=len(s['candidate_ids']),failures=failures,updated_at=now())))
            if i%25==0:print('Audited',i,'/',len(s['candidate_ids']),'failures',len(failures),flush=True)
            time.sleep(.05)
    acquisition=dict(rows=rows,failures=failures,sources=sources.manifest(),law_sources=lawproofs)
    if failures:
        (directory/'acquisition-failed.json').write_text(json.dumps(acquisition,indent=2,sort_keys=True))
        raise ValueError('Source failures block all scoring')
    save(directory,'acquisition.json',acquisition)
    groups=cohort.family_groups(training+exposed+rows)
    assert not {groups[r['bill_id']] for r in original}.intersection(groups[r['bill_id']] for r in calibration),'New link invalidates calibration independence'
    chosen,excluded=select(rows,training,exposed)
    assert chosen and all(s['label_available_at']<r['cutoff'] for r in chosen)
    save(directory,'selection.json',dict(selected_ids=[r['bill_id'] for r in chosen],excluded=excluded))
    pairs=[]
    for row in chosen:
        p=predict(models['original'],row['x'])
        pairs.append(dict(bill_id=row['bill_id'],family_id=row['family_id'],cutoff=row['cutoff'],input_features=row['x'],outcome=row['y'],law=row['law'],source_url=row['source']['url'],
            original=p,calibrated=calibrate(models['calibrated'],p),retrained=predict(models['retrained'],row['x'])))
    outcomes=[r['outcome'] for r in pairs]
    metrics={key:score([r[key] for r in pairs],outcomes) for key in models}
    comparisons={}
    for key in ('calibrated','retrained'):
        bootstrap_pairs=[dict(r,probability=r[key],baseline_probability=r['original']) for r in pairs]
        comparisons[key]=dict(brier_difference=metrics[key]['brier']-metrics['original']['brier'],interval=cohort.bootstrap(bootstrap_pairs))
    rate=(sum(r['y'] for r in original)+1)/(len(original)+2)
    class_metrics={str(y):{key:score([r[key] for r in pairs if r['outcome']==y],[y]*outcomes.count(y)) for key in models} for y in (0,1) if y in outcomes}
    result=dict(protocol_hash=protocol['hash'],models_hash=digest(models),predictions=pairs,metrics=metrics,comparisons=comparisons,class_metrics=class_metrics,
        baseline=score([rate]*len(pairs),outcomes),counts=dict(screened=len(rows),evaluated=len(pairs),positives=sum(outcomes),excluded=len(excluded)),
        exclusion_reasons=dict(Counter(r['reason'] for r in excluded)),source_documents=len(acquisition['sources']),source_bytes=sum(r['bytes'] for r in acquisition['sources']),
        inference=s['inference'],release_eligible=False)
    result['hash']=digest(result);save(directory,'result.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('predictions','class_metrics')},indent=2))
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--run-dir',default=str(DEFAULT));parser.add_argument('--register',action='store_true');parser.add_argument('--offline',action='store_true')
    args=parser.parse_args()
    if args.register:register(args.run_dir)
    else:run(args.run_dir,args.offline)
