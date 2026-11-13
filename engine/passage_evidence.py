"""Source-backed passage and day-30 publication evidence; never certifies negatives.
Publication availability is a bounded proxy, not complete historical action evidence.
"""
import argparse,hashlib,json,re,time
from pathlib import Path
from collections import Counter
from datetime import timedelta
from . import cohort
from .publication_identity import validate_introduction
from .store import ROOT,digest,now,timestamp,congress_end
from .model import date
from .sequential import TARGET

D=ROOT/'data/research-runs/passage-evidence-20261105'
PRIOR=ROOT/'data/research-runs/expanded-experiments-20261105'

def passage_actions(bill,kind):
    code='8000' if kind=='hr' else '17000'
    chamber='House' if kind=='hr' else 'Senate'
    rows=[]
    for a in bill.findall('actions/item'):
        text=a.findtext('text','')
        if a.findtext('actionCode')==code and a.findtext('sourceSystem/code')=='9' and text.startswith('Passed/agreed to in '+chamber+':'):
            rows.append(dict(date=timestamp(a.findtext('actionDate')),code=code,text=text))
    return sorted(rows,key=lambda r:r['date'])

class Sources(cohort.Sources):
    def __init__(self,directory,offline=False):
        super().__init__(directory,offline);self.used={}
    def get(self,url):
        key=hashlib.sha256(url.encode()).hexdigest();meta=PRIOR/'sources'/(key+'.json')
        if meta.exists():
            raw,proof=cohort.Sources(PRIOR,True).get(url)
        else:raw,proof=super().get(url)
        self.used[url]=proof;return raw,proof
    def manifest(self):return [self.used[k] for k in sorted(self.used)]

def audit_bill(sources,bid):
    match=re.fullmatch(r'(\d+)-(hr|s)(\d+)',bid);c,kind,n=int(match[1]),match[2],int(match[3])
    raw,source=sources.get(f'https://www.govinfo.gov/bulkdata/BILLSTATUS/{c}/{kind}/BILLSTATUS-{c}{kind}{n}.xml');bill=cohort.xml(raw).find('bill')
    if bill is None or int(bill.findtext('congress'))!=c or bill.findtext('type').lower()!=kind or int(bill.findtext('number'))!=n:
        raise ValueError('Bill identity mismatch')
    intro=timestamp(bill.findtext('introducedDate'));cutoff=timestamp((date(intro)+timedelta(days=30)).isoformat());actions=passage_actions(bill,kind);versions=[]
    packages=set()
    for u in bill.findall('textVersions/item/formats/item/url'):
        m=re.search(r'/pkg/(BILLS-'+str(c)+kind+str(n)+r'([a-z]+)\d*)/',u.text or '')
        if m and m[2] in cohort.VERSION_STAGE:packages.add((m[1],m[2]))
    for package,version in sorted(packages):
        mods,proof=cohort.package_audit(sources,package);proof['version']=version;proof['title']=mods.findtext('m:titleInfo/m:title',namespaces=cohort.M)
        if version==('ih' if kind=='hr' else 'is'):proof['introduction_validation']=validate_introduction(mods,package,intro)
        versions.append(proof)
    introduced=[v for v in versions if v['version']==('ih' if kind=='hr' else 'is')]
    if len(introduced)>1:
        raise ValueError('Ambiguous introduction')
    eligible=[v for v in versions if v['available_at']<=cutoff and v['issued_at']<=cutoff]
    checkpoint_reason=None
    if cutoff>=congress_end(c):checkpoint_reason='checkpoint_after_congress'
    elif not introduced:checkpoint_reason='no_introduced_publication'
    elif introduced[0]['available_at']>cutoff:checkpoint_reason='introduction_not_demonstrably_available_by_day30'
    elif actions and actions[0]['date']<=cutoff:checkpoint_reason='already_passed_by_day30'
    label=None;reason='no_corroborated_passage_no_complete_negative_coverage'
    own='eh' if kind=='hr' else 'es';engrossed=[v for v in versions if v['version']==own]
    if actions:
        first=actions[0];matching=[v for v in engrossed if v['issued_at']==first['date']]
        if first['date']>congress_end(c):reason='passage_outside_horizon'
        elif not matching:reason='passage_action_without_matching_dated_engrossed_version'
        else:
            proof=min(matching,key=lambda v:v['available_at'])
            label=dict(bill_id=bid,target=TARGET,value=1,effective_at=first['date'],available_at=proof['available_at'],source_url=source['url'],source_hash=source['sha256'],audit_note='Automated cross-source corroboration: LOC originating-chamber passage action and same-date official engrossed version. Historical availability bound from MODS/PREMIS plus margin; not human adjudication or historical byte-identity proof.',evidence=proof,action=first,provenance_tier='publication_preservation_bound',human_reviewed=False)
            reason=None
    checkpoint=dict(cutoff=cutoff,status='publication_proxy_available' if checkpoint_reason is None else 'blocked',reason=checkpoint_reason,eligible_packages=[v['package'] for v in eligible],evidence=eligible,complete_action_history=False)
    if checkpoint_reason is None:
        # Only publication-based features, never presented as historical action counts.
        stages=[cohort.VERSION_STAGE[v['version']] if v['version'] not in ('eh','es') or v['version']==own else 0 for v in eligible]
        last=max([intro]+[v['available_at'] for v in eligible]);checkpoint['publication_proxy_features']=[max([0]+stages)/4,30/730,min(len(eligible),30)/30,min((date(cutoff)-date(last)).days,730)/730,int(kind=='s'),min(sum((date(cutoff)-date(v['available_at'])).days<=30 for v in eligible),10)/10]
        checkpoint['title']=introduced[0]['title']
    return dict(bill_id=bid,congress=c,type=kind,source=source,passage_actions=actions,label=label,label_blocker=reason,checkpoint=checkpoint,versions=versions)

def run(offline=False):
    D.mkdir(parents=True,exist_ok=True);prior=json.loads((PRIOR/'acquisition.json').read_text());oldids=[r['bill_id'] for r in prior['rows']]
    ids=oldids+[f'{c}-{k}{n}' for c in (110,111,112) for k in ('hr','s') for n in range(1,21)]
    spec=dict(target=TARGET,ids=ids,checkpoint_days=30,negative_rule='Unknown until independent complete action coverage is audited; never infer from missing action or missing version',positive_rule='Matching first coded LOC origin passage and same-date EH/ES; preservation bound, not human certification',sampling='Existing exposed700 plus deterministic first20 HR/S in each110–112; early-bill sample is not representative',scoring=False)
    def save(name,value):
        path=D/name;text=json.dumps(value,indent=2)+'\n'
        if path.exists():
            if path.read_text()!=text:raise ValueError('Frozen artifact changed: '+name)
        else:path.write_text(text)
    save('protocol.json',dict(spec=spec,hash=digest(spec)))
    sources=Sources(D,offline);rows=[];failures=[]
    for i,bid in enumerate(ids,1):
        try:rows.append(audit_bill(sources,bid))
        except Exception as e:failures.append(dict(bill_id=bid,error=str(e)))
        if not offline and i%20==0:
            (D/'progress.json').write_text(json.dumps(dict(completed=i,total=len(ids),failures=failures)));print('Audited',i,'/',len(ids),'failures',len(failures),flush=True)
        if not offline and i>700:time.sleep(.15)
    labels=[r['label'] for r in rows if r['label']];available=[r for r in rows if r['checkpoint']['status']=='publication_proxy_available']
    summary=dict(selected=len(ids),audited=len(rows),source_failures=len(failures),corroborated_positive_labels=len(labels),certified_negative_labels=0,day30_publication_proxy_rows=len(available),positive_and_day30=sum(bool(r['label']) for r in available),complete_action_history_rows=0,human_reviewed_rows=0,by_congress={str(c):dict(audited=sum(r['congress']==c for r in rows),positive=sum(r['congress']==c and bool(r['label']) for r in rows),day30=sum(r['congress']==c for r in available)) for c in sorted({r['congress'] for r in rows})},label_blockers=dict(Counter(r['label_blocker'] for r in rows if r['label_blocker'])),checkpoint_blockers=dict(Counter(r['checkpoint']['reason'] for r in rows if r['checkpoint']['reason'])),source_documents=len(sources.manifest()),release_eligible=False,sequential_ready=False)
    result=dict(protocol_hash=digest(spec),rows=rows,failures=failures,sources=sources.manifest(),summary=summary,code_hashes={n:hashlib.sha256(Path(__file__).with_name(n).read_bytes()).hexdigest() for n in ('passage_evidence.py','publication_identity.py','cohort.py','store.py')});result['hash']=digest(result);save('audit.json',result)
    save('summary.json',summary)
    text=''.join(json.dumps(x,sort_keys=True)+'\n' for x in labels);path=D/'corroborated-positive-labels.jsonl'
    if path.exists():
        if path.read_text()!=text:raise ValueError('Frozen passage labels changed')
    else:path.write_text(text)
    print(json.dumps(summary,indent=2));return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--offline',action='store_true');run(p.parse_args().offline)
