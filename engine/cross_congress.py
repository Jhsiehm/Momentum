"""Cross-period acquisition campaign. Evidence collection never promotes a model."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import random
import re
import shutil
from . import cohort,sample_publication_v2 as pub
from .store import ROOT,digest,now
from .survivor_batch import save
from .billstatus_compat import AuditedSources
from .cross_congress_adjudication import late_introduction_conflict

DIRECTORY=ROOT/'data/research-runs/cross-congress-20261105'


def excluded_ids():
    ids=set()
    for pattern in ('data/cohorts/*/cohort.json','data/research-runs/*/acquisition.json'):
        for path in ROOT.glob(pattern):
            value=json.loads(path.read_text())
            ids.update(r['bill_id'] for r in value.get('rows',[]))
    for path in ROOT.glob('data/research-runs/*/protocol.json'):
        spec=json.loads(path.read_text()).get('spec',{})
        for key in ('candidate_ids','bill_ids','development_ids','confirmation_ids','ids'):
            ids.update(x for x in spec.get(key,[]) if isinstance(x,str))
    return ids


def register(directory=DIRECTORY):
    directory=Path(directory)
    if (directory/'protocol.json').exists():raise ValueError('Already registered')
    inventory=json.loads((directory/'inventory.json').read_text())
    excluded=excluded_ids();rng=random.Random(20261105500)
    populations={str(c):sorted(b for b in inventory['bill_ids'] if b.startswith(str(c)+'-') and b not in excluded) for c in range(113,118)}
    ids=[b for c in populations for b in rng.sample(populations[c],100)]
    save(directory,'populations.json',populations)
    spec=dict(registered_at=now(),candidate_ids=ids,seed=20261105500,populations_hash=digest(populations),
        congresses=list(range(113,118)),target='Own-bill enactment before Congress end',age_days=180,
        purpose='Feasibility only. All500 cases exposed development data; no accuracy-based expansion or model selection.',
        expansion='After feasibility, freeze up to15000 further candidates from usable periods; extend to25000 if fewer than200 usable training positives or50 development positives. Expansion uses evidence/count gates only, never comparative scores. Stop at cap and report insufficiency.',
        eligibility='Publication-v2 evidence rules unchanged. One representative per known family; future scoring removes training/evaluation family overlap.',
        label_gate='Full law census crosscheck plus historically dated complete census and positive-law identity/date proof before a row can train a historical forecast.',
        failures='Retain and retry sameIDs. Unresolved source failures block scoring; never replace failed cases.',
        promotion=False,limitations='Historical publication proxies, incomplete family linkage, no independent human certification; existing118 data exposed.')
    dependencies={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'engine').glob('*.py'))}
    save(directory,'dependencies.json',dependencies);spec['dependencies_hash']=digest(dependencies)
    spec['law_hashes']={str(c):digest(json.loads((directory/f'laws-{c}.json').read_text())) for c in spec['congresses']}
    snapshot=directory/'dependency-snapshot';snapshot.mkdir(exist_ok=True)
    for name in dependencies:shutil.copyfile(ROOT/'engine'/name,snapshot/name)
    save(directory,'protocol.json',dict(spec=spec,hash=digest(spec)))
    print('Registered',len(ids),'candidates',digest(spec),flush=True)


def audit(directory=DIRECTORY,offline=False):
    directory=Path(directory);protocol=json.loads((directory/'protocol.json').read_text());spec=protocol['spec']
    assert digest(spec)==protocol['hash']
    sources=AuditedSources(directory,offline)
    labels={}
    for c in spec['congresses']:
        value=json.loads((directory/f'laws-{c}.json').read_text())
        assert digest(value)==spec['law_hashes'][str(c)]
        labels.update({r['bill_id']:r for r in value['laws']})
    rows=[];failures=[]
    records=directory/'records';records.mkdir(exist_ok=True)
    adjudications=json.loads((directory/'adjudications.json').read_text()) if (directory/'adjudications.json').exists() else {}
    def collect(bid):
        path=records/(bid+'.json')
        if path.exists() and not offline:return json.loads(path.read_text()),None
        try:
            m=re.fullmatch(r'(\d+)-(hr|s)(\d+)',bid);assert m
            if adjudications.get(bid)=='late-under-all-official-dates-v1':row=late_introduction_conflict(sources,bid)
            else:row=pub.sample_bill(sources,int(m[1]),m[2],int(m[3]),spec,labels)
            save(records,bid+'.json',row)
            return row,None
        except Exception as e:return None,dict(bill_id=bid,error=str(e))
    with ThreadPoolExecutor(max_workers=4) as pool:
        for i,(row,failure) in enumerate(pool.map(collect,spec['candidate_ids']),1):
            if row:rows.append(row)
            if failure:failures.append(failure)
            if not offline:
                (directory/'progress.json').write_text(json.dumps(dict(completed=i,total=len(spec['candidate_ids']),failures=failures,updated_at=now())))
                if i%50==0:print('Audited',i,'/',len(spec['candidate_ids']),'failures',len(failures),flush=True)
    report=dict(protocol_hash=protocol['hash'],rows=rows,failures=failures,sources=sources.manifest())
    save(directory,'acquisition.json' if not failures else 'acquisition-blocked.json',report)
    groups=cohort.family_groups(rows);counts={}
    for c in spec['congresses']:
        selected=[r for r in rows if r['congress']==c];eligible=[r for r in selected if not r['exclusion']]
        unique={}
        for r in eligible:unique.setdefault(groups[r['bill_id']],r)
        counts[str(c)]=dict(screened=len(selected),eligible=len(eligible),unique_families=len(unique),positives=sum(r['y'] for r in unique.values()),
            failures=sum(f['bill_id'].startswith(str(c)+'-') for f in failures),exclusions=dict(Counter(r['exclusion'] for r in selected if r['exclusion'])))
    summary=dict(protocol_hash=protocol['hash'],counts=counts,source_documents=len(report['sources']),source_bytes=sum(r['bytes'] for r in report['sources']),failures=failures,scored=False,release_eligible=False)
    save(directory,'summary.json' if not failures else 'summary-blocked.json',summary)
    print(json.dumps(summary,indent=2));return summary


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--register',action='store_true');p.add_argument('--offline',action='store_true');p.add_argument('--run-dir',default=str(DIRECTORY));a=p.parse_args()
    if a.register:register(a.run_dir)
    else:audit(a.run_dir,a.offline)
