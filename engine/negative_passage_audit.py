"""Conservative final-calendar cross-check; emits review candidates, not certified labels."""
import argparse,hashlib,json,re
from pathlib import Path
from html.parser import HTMLParser
from collections import Counter
from . import cohort
from .passage_evidence import Sources as PriorSources,D as PRIOR
from .store import ROOT,digest,congress_end
D=ROOT/'data/research-runs/negative-passage-audit-20261105-v2'

class PreText(HTMLParser):
    def __init__(self):super().__init__();self.inside=False;self.parts=[]
    def handle_starttag(self,tag,attrs):
        if tag=='pre':self.inside=True
    def handle_endtag(self,tag):
        if tag=='pre':self.inside=False
    def handle_data(self,text):
        if self.inside:self.parts.append(text)

def entries(raw,kind):
    parser=PreText();parser.feed(raw.decode('utf-8'));text=''.join(parser.parts)
    assert 'HISTORY OF BILLS AND RESOLUTIONS' in text and 'Final' in text,'Not final calendar history text'
    prefix=r'H\.R\.' if kind=='hr' else r'S\.'
    matches=list(re.finditer(r'^'+prefix+r'\s+(\d+)(?=[\s.(])',text,re.M));assert matches,'No numbered entries'
    out={}
    for i,m in enumerate(matches):
        n=int(m[1]);assert n not in out,'Duplicate/continued calendar identity requires review'
        out[n]=text[m.start():matches[i+1].start() if i+1<len(matches) else len(text)].strip()
    return out

def classify(entry,actions,versions,laws,kind):
    if not entry:return 'not_listed_no_inference'
    flat=' '.join(entry.split());origin='House' if kind=='hr' else 'Senate'
    # Broad contradiction screening is deliberate: ambiguity remains review-only.
    risk=r'\b(?:passed|passage|enrolled|enacted|public law|private law|presented to the president|reconsider|veto|received in (?:house|senate))\b'
    if re.search(risk,flat,re.I):return 'calendar_has_passage_or_ambiguous_history'
    if laws or any(v in ('eh','es','enr','eah','eas','eph','cph') for v in versions):return 'status_or_version_contradiction'
    for a in actions:
        if a['code'] in ('8000','17000','28000','36000') or re.search(risk,a['text'],re.I):return 'action_history_requires_review'
    if not re.search(r'(?:Union|House|Private) Calendar\s*\.+\s*(?:Union|House|Private)\s+\d+\s*$',flat):return 'no_explicit_terminal_pending_calendar'
    if not actions:return 'missing_action_history'
    return 'corroborated_pending_negative_candidate'

def run(offline=False):
    protocol=json.loads((D/'protocol.json').read_text());assert digest(protocol['spec'])==protocol['hash'];prior=json.loads((PRIOR/'audit.json').read_text());assert prior['hash']==protocol['spec']['parent_hash']
    sources=cohort.Sources(D,offline);old=PriorSources(PRIOR,True);calendars={};calendar_proofs=[]
    for c in protocol['spec']['congresses']:
        mods,proof=cohort.package_audit(sources,f'CCAL-{c}hcal-S2')
        assert any(e.findtext('m:edition',namespaces=cohort.M)=='FINAL' and e.findtext('m:congress',namespaces=cohort.M)==str(c) for e in mods.findall('m:extension',cohort.M))
        for kind,title in [('hr','HOUSE BILLS'),('s','SENATE BILLS')]:
            items=[i for i in mods.findall('m:relatedItem',cohort.M) if any((n.text or '').upper()=='HISTORY OF BILLS AND RESOLUTIONS - '+title for n in i.findall('.//m:partName',cohort.M))];assert len(items)==1
            urls=[u.text for u in items[0].findall('.//m:url',cohort.M) if (u.text or '').endswith('.htm')];assert len(set(urls))==1
            raw,receipt=sources.get(urls[0]);calendars[c,kind]=(entries(raw,kind),receipt,proof);calendar_proofs.append(dict(congress=c,kind=kind,entries=len(calendars[c,kind][0]),publication=proof,source=receipt))
    results=[]
    for row in prior['rows']:
        bid=row['bill_id'];c=row['congress'];kind=row['type'];number=int(re.search(r'(\d+)$',bid)[1]);mapping,receipt,publication=calendars[c,kind];entry=mapping.get(number)
        raw,bs=old.get(row['source']['url']);bill=cohort.xml(raw).find('bill');assert int(bill.findtext('congress'))==c and bill.findtext('type').lower()==kind and int(bill.findtext('number'))==number
        actions=[dict(date=x.findtext('actionDate'),code=x.findtext('actionCode'),text=x.findtext('text',''),source_system=x.findtext('sourceSystem/code')) for x in bill.findall('actions/item')]
        versions=[]
        for x in bill.findall('textVersions/item/formats/item/url'):
            m=re.search(r'/pkg/BILLS-'+str(c)+kind+str(number)+r'([a-z]+)\d*/',x.text or '')
            if m:versions.append(m[1])
        status=classify(entry,actions,versions,bill.findall('laws/item'),kind)
        assert not (row['label'] and status=='corroborated_pending_negative_candidate'),'Positive control incorrectly classified negative'
        results.append(dict(bill_id=bid,congress=c,kind=kind,positive_control=bool(row['label']),status=status,calendar_entry=entry,calendar_source=receipt,calendar_available_at=publication['available_at'],billstatus_source=bs,actions=actions,versions=sorted(set(versions)),coverage_through=congress_end(c),day30_proxy_available=row['checkpoint']['status']=='publication_proxy_available',complete_coverage_certified=False,human_reviewed=False))
    candidates=[r for r in results if r['status']=='corroborated_pending_negative_candidate'];unresolved=[r for r in results if not r['positive_control']]
    summary=dict(unresolved_audited=len(unresolved),positive_controls=sum(r['positive_control'] for r in results),negative_review_candidates=len(candidates),negative_candidates_with_day30_proxy=sum(r['day30_proxy_available'] for r in candidates),certified_negative_labels=0,status_counts=dict(Counter(r['status'] for r in unresolved)),controls=dict(Counter(r['status'] for r in results if r['positive_control'])),prior_missing_sources=len(prior['failures']),release_eligible=False,scoring_ready=False)
    result=dict(protocol_hash=protocol['hash'],parent_hash=prior['hash'],calendar_proofs=calendar_proofs,rows=results,prior_source_failures=prior['failures'],summary=summary,new_source_manifest=sources.manifest(),code_hash=hashlib.sha256(Path(__file__).read_bytes()).hexdigest());result['hash']=digest(result)
    for name,value in [('audit.json',result),('summary.json',summary),('negative-review-queue.json',candidates)]:
        path=D/name;text=json.dumps(value,indent=2,sort_keys=True)+'\n'
        if path.exists():assert path.read_text()==text,'Frozen result differs: '+name
        else:path.write_text(text)
    print(json.dumps(summary,indent=2));return result
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--offline',action='store_true');args=parser.parse_args();run(args.offline)
