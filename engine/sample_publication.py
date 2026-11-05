"""Separate fixed-sample publication-version study; never unlocks human/action audits."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
import time
from . import cohort
from .model import fit, predict, score
from .store import ROOT, digest, now

DIRECTORY = ROOT/'data/cohorts/seeded-publication-v1'
SPEC = ROOT/'docs/cohorts/seeded-publication-v1.json'
LIMITATIONS = [
    'Fixed stratified random sample from the 114th, 116th and 118th official inventories; one evaluation Congress and small event counts cannot establish generalization.',
    *cohort.LIMITATIONS[1:],
    'Separate publication-version development study; does not make current BILLSTATUS actions historically eligible or satisfy the pending human audit.',
]

class Sources(cohort.Sources):
    def get(self, url):
        for attempt in range(3):
            try: return super().get(url)
            except Exception:
                if self.offline or attempt == 2: raise
                time.sleep(attempt + 1)

def frozen_spec(directory=DIRECTORY):
    value=json.loads(SPEC.read_text()); path=directory/'protocol.json'
    if path.exists():
        frozen=json.loads(path.read_text())
        if frozen['spec_hash']!=digest(value): raise ValueError('Protocol changed; create a new study')
        return frozen
    frozen={'registered_at':now(),'spec':value,'spec_hash':digest(value)}
    cohort.write_json(path,frozen); return frozen

def law_census(sources, congress, expected):
    if congress != 116: return cohort.law_census(sources, congress, expected)
    rows=[]; proofs=[]
    for session in ('first','second'):
        raw, proof=sources.get(f'https://www.archives.gov/files/federal-register/laws/116-{session}-session.txt')
        rows += cohort.parse_law_list(raw,116); proofs.append(proof)
    if len(rows)!=expected or {r['law'] for r in rows}!=set(range(1,expected+1)) or len({r['bill_id'] for r in rows})!=expected:
        raise ValueError('Incomplete/duplicate116 law census')
    return rows,proofs

def training_census(sources, congress, laws, volumes):
    entries={}; proofs=[]
    for volume in volumes:
        mods,proof=cohort.package_audit(sources,f'STATUTE-{volume}'); proofs.append(proof)
        for item in mods.findall('m:relatedItem',cohort.M):
            ext=item.find('m:extension',cohort.M)
            if ext is None or ext.findtext('m:granuleClass',namespaces=cohort.M)!='PUBLICLAW': continue
            number=int(ext.findtext('m:number',namespaces=cohort.M))
            bills=[b for b in ext.findall('.//m:bill',cohort.M) if b.get('priority')=='primary']
            if len(bills)!=1 or bills[0].get('congress')!=str(congress): raise ValueError('Ambiguous Statutes linkage')
            if number in entries: raise ValueError('Duplicate Statutes law')
            b=bills[0]; entries[number]={'law':number,'bill_id':f"{congress}-{b.get('type').lower()}{b.get('number')}",'enacted':ext.findtext('m:granuleDate',namespaces=cohort.M)}
    if sorted(entries.values(),key=lambda r:r['law'])!=sorted(laws,key=lambda r:r['law']): raise ValueError('Statutes / NARA census disagreement')
    return {'congress':congress,'complete_laws':len(entries),'available_at':max(p['available_at'] for p in proofs),'volumes':proofs}

def assign_families(rows, test_congress=118):
    groups=cohort.family_groups(rows)
    for row in rows: row['family_id']=groups[row['bill_id']]
    test_families={r['family_id'] for r in rows if r['congress']==test_congress}; used=set()
    for row in sorted(rows,key=lambda r:r['bill_id']):
        if row['congress']!=test_congress and not row['exclusion']:
            if row['family_id'] in test_families: row['exclusion']='Identified family overlaps evaluation cohort'
            elif row['family_id'] in used: row['exclusion']='Duplicate training family'
            else: used.add(row['family_id'])
    return rows

def prepare(directory=DIRECTORY, offline=False, rebuild=False):
    frozen=frozen_spec(directory); spec=frozen['spec']; sources=Sources(directory,offline)
    if (directory/'cohort.json').exists() and not rebuild: return json.loads((directory/'cohort.json').read_text())
    labels={}; label_proofs=[]; law_sources=[]
    for c,expected in ((114,329),(116,344),(118,274)):
        laws,proofs=law_census(sources,c,expected); law_sources+=proofs; labels.update({r['bill_id']:r for r in laws})
        if c!=118: label_proofs.append(training_census(sources,c,laws,{114:(129,130),116:(133,134)}[c]))
    jobs=[]
    for identity in spec['bill_ids']:
        m=re.fullmatch(r'(114|116|118)-(hr|s)(\d+)',identity)
        if not m: raise ValueError('Invalid frozen identity')
        jobs.append((int(m[1]),m[2],int(m[3])))
    def collect(args):
        try: return cohort.sample_bill(sources,*args,spec,labels),None
        except Exception as e: return None,{'bill_id':f'{args[0]}-{args[1]}{args[2]}','error':str(e)}
    rows=[]; failures=[]
    with ThreadPoolExecutor(max_workers=4) as pool:
        for index,(row,failure) in enumerate(pool.map(collect,jobs),1):
            if failure:
                failures.append(failure)
                c,k,n=jobs[index-1]
                url=f'https://www.govinfo.gov/bulkdata/BILLSTATUS/{c}/{k}/BILLSTATUS-{c}{k}{n}.xml'
                _,source=sources.get(url)
                rows.append(cohort.excluded_slot(failure['bill_id'],c,k,'Source audit failed: '+failure['error'],source))
            else: rows.append(row)
            if not offline and index%10==0: print(f'Audited {index}/{len(jobs)}; failures {len(failures)}',flush=True)
    assign_families(rows)
    audit={'protocol_hash':frozen['spec_hash'],'selected':len(jobs),'rows':rows,'failures':failures,
           'training_label_provenance':label_proofs,'law_census_sources':law_sources,'limitations':LIMITATIONS}
    audit['source_hash']=digest(sources.manifest()); audit['cohort_hash']=digest(rows)
    if not rebuild:
        cohort.write_json(directory/'cohort.json',audit)
        if failures: cohort.write_json(directory/'audit-blocked.json',audit)
        cohort.write_json(directory/'source-manifest.json',sources.manifest())
    return audit

def compute(directory=DIRECTORY):
    frozen=frozen_spec(directory); audit=json.loads((directory/'cohort.json').read_text())
    rebuilt=prepare(directory,offline=True,rebuild=True)
    if any(rebuilt[k]!=audit[k] for k in ('source_hash','cohort_hash','protocol_hash')): raise ValueError('Offline reconstruction mismatch')
    if sorted(r['bill_id'] for r in audit['rows'])!=sorted(frozen['spec']['bill_ids']): raise ValueError('Frozen sample denominator mismatch')
    train=[r for r in audit['rows'] if r['congress']!=118 and not r['exclusion']]
    test=[r for r in audit['rows'] if r['congress']==118 and not r['exclusion']]
    blockers=[f"{len(audit['failures'])} source audits failed; all scoring blocked"] if audit['failures'] else []
    if len(train)<20 or {r['y'] for r in train}!={0,1}: blockers.append('Insufficient eligible training families/classes (need >=20 and both labels)')
    if not test: blockers.append('No eligible evaluation rows')
    if {r['family_id'] for r in train}&{r['family_id'] for r in test}: blockers.append('Training/evaluation family overlap')
    if test and max(p['available_at'] for p in audit['training_label_provenance'])>min(r['cutoff'] for r in test): blockers.append('Complete training labels not archived before earliest evaluation checkpoint')
    result={'title':'Seeded sample · publication-version development study','kind':'audited_cohort','candidate':'document-stage-l2-v1',
        'status':'blocked' if blockers else 'completed','blockers':blockers,'config':{'dataset':'official','congress':118,'age_days':180},
        'design_status':frozen['spec']['design_status'],'protocol_hash':frozen['spec_hash'],'source_hash':audit['source_hash'],'cohort_hash':audit['cohort_hash'],
        'selected':len(audit['rows']),'attempted':sum(r['congress']==118 for r in audit['rows']),'available':len(test),
        'training_count':len(train),'training_positives':sum(r['y'] for r in train),'evaluation_positives':sum(r['y'] for r in test),
        'training_ids':[r['bill_id'] for r in train],'exclusions':[{'bill_id':r['bill_id'],'reason':r['exclusion']} for r in audit['rows'] if r['exclusion']],
        'failures':audit['failures'],'sample_id':frozen['spec']['sample_id'],'limitations':LIMITATIONS,'release_eligible':False,'results':[],
        'preflight':{'status':'blocked' if blockers else 'passed bounded publication source audit; human action-history audit remains pending'},
        'protocol':'114th + 116th training → 118th evaluation; exact seeded100 sample,180-day publication features.',
        'training_label_provenance':audit['training_label_provenance']}
    if not blockers:
        model=fit([{'x':r['x'],'y':r['y']} for r in train]); rate=(sum(r['y'] for r in train)+1)/(len(train)+2)
        pairs=[{'bill_id':r['bill_id'],'title':r['title'],'family_id':r['family_id'],'cutoff':r['cutoff'],'status':'available',
            'probability':predict(model,r['x']),'baseline_probability':rate,'outcome':r['y'],'feature_hash':digest({'x':r['x'],'packages':r['eligible_packages']})} for r in test]
        metrics=score([r['probability'] for r in pairs],[r['outcome'] for r in pairs]); baseline=score([rate]*len(pairs),[r['outcome'] for r in pairs]); diff=metrics['brier']-baseline['brier']
        interval=cohort.bootstrap(pairs)
        conclusion=('No added value: candidate Brier loss is at least baseline loss.' if diff>=0 else 'Lower candidate Brier loss in this development sample; not evidence of validated generalization.')
        if len({r['y'] for r in test})<2: conclusion+=' Evaluation contains only one outcome class; discrimination cannot be assessed.'
        result.update(results=pairs,model_artifact=model,metrics=metrics,baseline=baseline,brier_difference=diff,brier_difference_interval=interval,conclusion=conclusion)
    else: result['conclusion']='Scoring blocked: '+'; '.join(blockers)
    result['note']=result['conclusion']+' Separate publication-version study; does not unlock the human/action-history audit.'
    result['code_files']={name:hashlib.sha256((ROOT/'engine'/name).read_bytes()).hexdigest() for name in ('sample_publication.py','cohort.py','model.py','store.py','ingest.py')}
    result['code_hash']=digest(result['code_files']); result['reproducibility_hash']=digest(result)
    return result

def run(directory=DIRECTORY):
    result=compute(directory); path=directory/'result.json'
    if path.exists() and json.loads(path.read_text())['reproducibility_hash']!=result['reproducibility_hash']: raise ValueError('Locked result differs; original preserved')
    if not path.exists():
        cohort.write_json(path,result)
        for name in result['code_files']:
            target=directory/'code'/name; target.parent.mkdir(exist_ok=True);target.write_bytes((ROOT/'engine'/name).read_bytes())
        (directory/'predictions.jsonl').write_text(''.join(json.dumps(p,sort_keys=True)+'\n' for p in result['results']))
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('action',choices=['prepare','run','reproduce']); args=parser.parse_args()
    r=prepare() if args.action=='prepare' else run()
    print(json.dumps({k:v for k,v in r.items() if k in ('selected','training_count','training_positives','evaluation_positives','available','metrics','baseline','brier_difference','brier_difference_interval','conclusion','reproducibility_hash','failures')},indent=2))
if __name__=='__main__': main()
