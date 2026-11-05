"""Versioned evidence-rule amendment to the fixed-sample publication study; never unlocks human/action audits."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
import time
from . import cohort
from .publication_identity import validate_introduction
from .cohort import timestamp, date, timedelta, xml, excluded_slot, package_audit, VERSION_STAGE, M, congress_end
from .model import fit, predict, score
from .store import ROOT, digest, now

DIRECTORY = ROOT/'data/cohorts/seeded-publication-v2'
SPEC = ROOT/'docs/cohorts/seeded-publication-v2.json'
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
    directory.mkdir(parents=True, exist_ok=True)
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

def sample_bill(sources, congress, kind, number, spec, labels, directories=None):
    identity = f'{congress}-{kind}{number}'
    if directories and number not in directories[(congress,kind)][0]:
        return excluded_slot(identity,congress,kind,'No BILLSTATUS entry in complete official chamber directory; no historical introduction audited',directories[(congress,kind)][1])
    raw, source = sources.get(f'https://www.govinfo.gov/bulkdata/BILLSTATUS/{congress}/{kind}/BILLSTATUS-{congress}{kind}{number}.xml')
    bill = xml(raw).find('bill')
    if bill is None or int(bill.findtext('congress')) != congress or bill.findtext('type').lower() != kind or int(bill.findtext('number')) != number:
        raise ValueError('BILLSTATUS identifier mismatch: ' + identity)
    intro = timestamp(bill.findtext('introducedDate'))
    cutoff = (date(intro) + timedelta(days=spec['age_days'])).isoformat().replace('+00:00', 'Z')
    law = labels.get(identity)
    reported = {int(x.findtext('number').split('-')[-1]) for x in bill.findall('laws/item') if x.findtext('type', '').lower() in ('public','public law')}
    expected = {law['law']} if law else set()
    if reported != expected:
        raise ValueError('BILLSTATUS / National Archives outcome mismatch: ' + identity)
    packages = set()
    for url in bill.findall('textVersions/item/formats/item/url'):
        match = re.search(r'/pkg/(BILLS-' + str(congress) + kind + str(number) + r'([a-z]+)\d*)/', url.text or '')
        if match and match.group(2) in VERSION_STAGE:
            packages.add((match.group(1), match.group(2)))
    versions = []
    for package, version in sorted(packages):
        mods, proof = package_audit(sources, package)
        proof['version'] = version
        proof['stage'] = VERSION_STAGE[version] if (version not in ('eh', 'es') or version == ('eh' if kind == 'hr' else 'es')) else 0
        proof['title'] = mods.findtext('m:titleInfo/m:title', namespaces=M)
        if version == ('ih' if kind == 'hr' else 'is'):
            proof['introduction_validation'] = validate_introduction(mods, package, intro)
        versions.append(proof)
    introductions = [v for v in versions if v['version'] == ('ih' if kind == 'hr' else 'is')]
    if not introductions:
        return excluded_slot(identity,congress,kind,'No introduced publication in official text-version list',source,bill.findtext('title','No title'))
    if len(introductions) != 1:
        raise ValueError('Conflicting introduced publication: ' + identity)
    title = introductions[0]['title']
    related = []
    for item in bill.findall('relatedBills/item'):
        rc, rt, rn = item.findtext('congress'), item.findtext('type', '').lower(), item.findtext('number')
        if rc and rt and rn:
            related.append(f'{rc}-{rt}{rn}')
    exclusion = None
    if cutoff >= congress_end(congress): exclusion = 'Checkpoint at/after Congress end'
    elif law and law['enacted'] == congress_end(congress)[:10]: exclusion = 'Enactment on session-end date has insufficient time precision'
    elif law and law['enacted'] <= cutoff[:10]: exclusion = 'Already enacted by checkpoint'
    elif introductions[0]['available_at'] > cutoff: exclusion = 'Introduction publication not available by checkpoint'
    eligible = [v for v in versions if v['available_at'] <= cutoff and v['issued_at'] <= cutoff]
    stage = max([0] + [v['stage'] for v in eligible])
    last = max([intro] + [v['available_at'] for v in eligible])
    x = [stage / 4, min(spec['age_days'], 730) / 730, min(len(eligible), 30) / 30,
         min((date(cutoff)-date(last)).days, 730) / 730, int(kind == 's'),
         min(sum((date(cutoff)-date(v['available_at'])).days <= 30 for v in eligible), 10) / 10]
    return {'bill_id': identity, 'congress': congress, 'type': kind, 'title': title, 'introduced_at': intro,
            'cutoff': cutoff, 'x': x, 'y': int(bool(law and law['enacted'] < congress_end(congress)[:10])),
            'law': law, 'related': related, 'versions': versions, 'eligible_packages': [v['package'] for v in eligible],
            'source': source, 'exclusion': exclusion}



def prepare(directory=DIRECTORY, offline=False, rebuild=False):
    frozen=frozen_spec(directory); spec=frozen['spec']; sources=Sources(directory,offline)
    if (directory/'cohort.json').exists() and not rebuild: return json.loads((directory/'cohort.json').read_text())
    labels={}; label_proofs=[]; law_sources=[]
    for c,expected in ((114,329),(116,344),(118,274)):
        laws,proofs=law_census(sources,c,expected); law_sources+=proofs; labels.update({r['bill_id']:r for r in laws})
        if c == 114: label_proofs.append(training_census(sources,c,laws,(129,130)))
        elif c == 116:
            from .earlier_labels import historical_census, dated_law
            proof = historical_census(sources, laws)
            # A complete mapping supports absence; sampled positives also need dated law evidence.
            proof['dated_laws'] = [dated_law(sources, law) for law in laws if law['bill_id'] in spec['bill_ids']]
            proof['available_at'] = max([proof['available_at']] + [law['available_at'] for law in proof['dated_laws']])
            label_proofs.append(proof)
    jobs=[]
    for identity in spec['bill_ids']:
        m=re.fullmatch(r'(114|116|118)-(hr|s)(\d+)',identity)
        if not m: raise ValueError('Invalid frozen identity')
        jobs.append((int(m[1]),m[2],int(m[3])))
    def collect(args):
        try: return sample_bill(sources,*args,spec,labels),None
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
    if any(not p.get('complete',True) for p in audit['training_label_provenance']): blockers.append('Historical training-law census completeness not established')
    if test and max(p['available_at'] for p in audit['training_label_provenance'])>min(r['cutoff'] for r in test): blockers.append('Complete training labels not archived before earliest evaluation checkpoint')
    result={'title':'Seeded sample · revised publication evidence study','kind':'sample_publication_study_v2','candidate':'document-stage-l2-v1',
        'status':'blocked' if blockers else 'completed','blockers':blockers,'config':{'dataset':'official','congress':118,'age_days':180},
        'design_status':frozen['spec']['design_status'],'protocol_hash':frozen['spec_hash'],'source_hash':audit['source_hash'],'cohort_hash':audit['cohort_hash'],
        'selected':len(audit['rows']),'attempted':sum(r['congress']==118 for r in audit['rows']),'available':0,'publication_eligible_count':len(test),
        'training_count':len(train),'training_positives':sum(r['y'] for r in train),'evaluation_positives':sum(r['y'] for r in test),
        'training_ids':[r['bill_id'] for r in train],'exclusions':[{'bill_id':r['bill_id'],'reason':r['exclusion']} for r in audit['rows'] if r['exclusion']],
        'failures':audit['failures'],'sample_id':frozen['spec']['sample_id'],'limitations':LIMITATIONS,'release_eligible':False,'results':[],
        'preflight':{'status':'blocked' if blockers else 'passed bounded publication source audit; human action-history audit remains pending'},
        'protocol':'Evidence-amended v2; 114th + 116th training → 118th evaluation; exact seeded100 sample, 180-day publication features.',
        'amends_protocol':'seeded-publication-v1',
        'amendment_note':frozen['spec'].get('interpretation'),
        'evaluation_discrimination_assessable':len({r['y'] for r in test}) == 2,
        'training_label_provenance':audit['training_label_provenance']}
    if not blockers:
        model=fit([{'x':r['x'],'y':r['y']} for r in train]); rate=(sum(r['y'] for r in train)+1)/(len(train)+2)
        pairs=[{'bill_id':r['bill_id'],'title':r['title'],'family_id':r['family_id'],'cutoff':r['cutoff'],'status':'available',
            'probability':predict(model,r['x']),'baseline_probability':rate,'outcome':r['y'],'feature_hash':digest({'x':r['x'],'packages':r['eligible_packages']})} for r in test]
        metrics=score([r['probability'] for r in pairs],[r['outcome'] for r in pairs]); baseline=score([rate]*len(pairs),[r['outcome'] for r in pairs]); diff=metrics['brier']-baseline['brier']
        interval=cohort.bootstrap(pairs)
        conclusion=('No added value: candidate Brier loss is at least baseline loss.' if diff>=0 else 'Lower candidate Brier loss in this development sample; not evidence of validated generalization.')
        if len({r['y'] for r in test})<2: conclusion+=' Evaluation contains only one outcome class; discrimination cannot be assessed.'
        result.update(available=len(pairs),results=pairs,model_artifact=model,metrics=metrics,baseline=baseline,brier_difference=diff,brier_difference_interval=interval,conclusion=conclusion)
    else: result['conclusion']='Scoring blocked: '+'; '.join(blockers)
    result['note']=result['conclusion']+' Separate publication-version study; does not unlock the human/action-history audit.'
    result['code_files']={name:hashlib.sha256((ROOT/'engine'/name).read_bytes()).hexdigest() for name in ('sample_publication_v2.py','publication_identity.py','earlier_labels.py','label_investigation.py','cohort.py','model.py','store.py','ingest.py')}
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
