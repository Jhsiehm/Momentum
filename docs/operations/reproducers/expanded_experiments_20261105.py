"""Registered expanded historical experiment; offline replay verifies frozen outputs."""
import argparse,copy,hashlib,importlib.util,json,re,time,sys
from pathlib import Path
from engine import cohort,learning,sample_publication_v2 as pub
from engine.label_investigation import law_identity
from engine.model import predict,score
from engine.store import digest,now
D=Path(__file__).resolve().parent

def write_once(path,value):
    if path.exists(): assert json.loads(path.read_text())==value,'Frozen artifact differs: '+str(path)
    else: path.write_text(json.dumps(value,indent=2))

def run(offline=False):
    p=json.loads((D/'protocol.json').read_text());s=p['spec'];assert digest(s)==p['hash']
    dependencies={str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(Path('engine').glob('*.py'))}
    dependencies[str(Path(__file__))]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    write_once(D/'dependency-manifest.json',dict(files=dependencies,python=sys.version))
    ms=importlib.util.spec_from_file_location('prior',D.parent/'full-cycle-20261105/run_official.py');m=importlib.util.module_from_spec(ms);ms.loader.exec_module(m);previous=m.run(True)
    sources=cohort.Sources(D,offline);oldsrc=cohort.Sources(pub.DIRECTORY,True)
    labels={};census=[]
    for c,n in [(116,344),(118,274)]:
        laws,proofs=pub.law_census(oldsrc,c,n);labels.update({r['bill_id']:r for r in laws});census.extend(proofs)
    rows=[];failures=[];positive_proofs={}
    ids=s['new_training_ids']+s['development_ids']+s['confirmation_ids']
    for i,bid in enumerate(ids,1):
        try:
            match=re.fullmatch(r'(116|118)-(hr|s)(\d+)',bid)
            row=pub.sample_bill(sources,int(match[1]),match[2],int(match[3]),{'age_days':s['age_days']},labels)
            if row['congress']==116 and row.get('y'):
                mods,proof=cohort.package_audit(sources,f"PLAW-116publ{row['law']['law']}")
                assert law_identity(mods,116,row['law']['law'])==row['law']
                positive_proofs[bid]=proof
            rows.append(row)
        except Exception as e: failures.append(dict(bill_id=bid,error=str(e)))
        if not offline:
            (D/'acquisition-progress.json').write_text(json.dumps(dict(completed=i,total=len(ids),failures=failures,updated_at=now()),indent=2))
            if i%10==0: print('Audited',i,'/',len(ids),'failures',len(failures),flush=True)
            time.sleep(.15)
    acquired=dict(protocol_hash=p['hash'],rows=rows,failures=failures,positive_proofs=positive_proofs,source_manifest=sources.manifest(),census_sources=census)
    acquired['hash']=digest(acquired)
    if failures:
        (D/'acquisition-failed.json').write_text(json.dumps(acquired,indent=2));raise ValueError('Required source failures block scoring')
    write_once(D/'acquisition.json',acquired)
    old=json.loads((pub.DIRECTORY/'cohort.json').read_text())
    original=copy.deepcopy([r for r in old['rows'] if r['congress']<118 and not r['exclusion']])
    exposed=json.loads((D/'exposed-rows.json').read_text());assert digest(exposed)==s['exposed_rows_hash']
    groups=cohort.family_groups(original+rows+exposed)
    targets=[r for r in rows if r['congress']==118];newtrain=[r for r in rows if r['congress']==116]
    oldfamilies={groups[r['bill_id']] for r in exposed};devfamilies={groups[b] for b in s['development_ids']};targetfamilies={groups[r['bill_id']] for r in targets}
    exclusions=[];dev=[];confirm=[]
    for r in targets:
        r=copy.deepcopy(r);r['family_id']=groups[r['bill_id']];isdev=r['bill_id'] in s['development_ids'];reason=r['exclusion']
        if not reason and r['family_id'] in oldfamilies: reason='Previously exposed evaluation family'
        if not reason and not isdev and r['family_id'] in devfamilies: reason='Development family overlap'
        if reason: exclusions.append(dict(bill_id=r['bill_id'],reason=reason));continue
        (dev if isdev else confirm).append(r)
    assert dev and confirm
    boundary=min(r['cutoff'] for r in dev+confirm)
    availability=max([previous['calendar']['available_at']]+[x['available_at'] for x in previous['dated_positive_proofs']]+[x['available_at'] for x in old['training_label_provenance'] if x['congress']==116]);assert availability<boundary
    training=[];used=set();trainex=[]
    for r in sorted(original+newtrain,key=lambda r:r['bill_id']):
        r=copy.deepcopy(r);r['family_id']=groups[r['bill_id']];reason=r['exclusion']
        if not reason and r['bill_id'] in positive_proofs and positive_proofs[r['bill_id']]['available_at']>=boundary: reason='Positive label proof too late'
        if not reason and r['family_id'] in targetfamilies: reason='Evaluation family overlap'
        if not reason and r['family_id'] in used: reason='Duplicate training family'
        if reason: trainex.append(dict(bill_id=r['bill_id'],reason=reason,y=r.get('y')));continue
        used.add(r['family_id']);training.append(r)
    assert len(training)>=20 and len({r['y'] for r in training})==2
    originalids={r['bill_id'] for r in original};originalonly=[r for r in training if r['bill_id'] in originalids];assert len({r['y'] for r in originalonly})==2
    frozen=dict(protocol_hash=p['hash'],acquisition_hash=acquired['hash'],training=training,original_training=originalonly,development=dev,confirmation=confirm,excluded_training=trainex,excluded_targets=exclusions,training_counts_before={'n':len(original+newtrain),'positive':sum(r.get('y',0) for r in original+newtrain)},label_available_at=availability)
    frozen['hash']=digest(frozen);write_once(D/'frozen-inputs.json',frozen)
    def transform(r,policy):
        return learning.features(r,policy) if policy in ('structured','structured_context') else [r['x'][i] for i in s['ablation_policies'][policy]]
    def fit(design,train):
        transformed=[dict(r,x=transform(r,design['policy'])) for r in train];a=learning._fit(transformed,design['l2']);a.update(policy=design['policy'],training_hash=digest(transformed));return a
    rate=(sum(r['y'] for r in training)+1)/(len(training)+2)
    def evaluate(a,test,baseline=None):
        pairs=[dict(bill_id=r['bill_id'],family_id=r['family_id'],outcome=r['y'],probability=predict(a,transform(r,a['policy'])),baseline_probability=rate if baseline is None else baseline[i]) for i,r in enumerate(test)]
        return dict(metrics=score([r['probability'] for r in pairs],[r['outcome'] for r in pairs]),predictions=pairs,interval=cohort.bootstrap(pairs))
    results=[];artifacts={}
    for design in s['experiments']:
        a=fit(design,training);artifacts[design['id']]=a
        result=dict(design=design,artifact=a,artifact_hash=digest(a),input_hash=frozen['hash'],**evaluate(a,dev));result['hash']=digest(result);write_once(D/(design['id']+'-development.json'),result);results.append(result)
    chosen=results[0]
    for r in results[1:]:
        if r['metrics']['brier']<chosen['metrics']['brier']-1e-12: chosen=r
    selection=dict(id=chosen['design']['id'],artifact_hash=chosen['artifact_hash'],development_results_hash=digest(results),protocol_hash=p['hash'])
    write_once(D/'selection.json',selection) # MUST precede confirmation scoring/count summaries
    survivor=evaluate(artifacts['X1'],confirm);selected=evaluate(chosen['artifact'],confirm)
    comparison=evaluate(chosen['artifact'],confirm,[r['probability'] for r in survivor['predictions']])
    originalartifact=fit(s['experiments'][0],originalonly);originalresult=evaluate(originalartifact,confirm)
    addition=evaluate(artifacts['X1'],confirm,[r['probability'] for r in originalresult['predictions']])
    confirmation=dict(selection=selection,selected=selected,survivor=survivor,selected_minus_survivor=comparison['interval'],original_only_artifact=originalartifact,original_only=originalresult,expanded_minus_original=addition['interval'],baseline=score([rate]*len(confirm),[r['y'] for r in confirm]))
    confirmation['hash']=digest(confirmation);write_once(D/'confirmation.json',confirmation)
    summary=dict(protocol_hash=p['hash'],input_hash=frozen['hash'],selection=selection,development=[dict(id=r['design']['id'],metrics=r['metrics']) for r in results],confirmation={k:v for k,v in confirmation.items() if k not in ('selected','survivor','original_only','original_only_artifact')},confirmation_metrics={k:confirmation[k]['metrics'] for k in ('selected','survivor','original_only')},counts={k:dict(n=len(v),positive=sum(r['y'] for r in v)) for k,v in [('training',training),('original_training',originalonly),('development',dev),('confirmation',confirm)]},source_documents=len(acquired['source_manifest']),release_eligible=False,limitations=s['limitations'])
    summary['hash']=digest(summary);write_once(D/'summary.json',summary);print(json.dumps(summary,indent=2));return summary
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--offline',action='store_true');args=parser.parse_args();run(args.offline)
