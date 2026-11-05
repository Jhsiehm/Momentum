"""Source-backed relationships, text links and observed metadata revisions.

No network reads, family adjudication, or full-text comparison is performed here.
"""
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.parse import urlsplit
from .store import ROOT, now, timestamp

_HOSTS = {'www.govinfo.gov', 'govinfo.gov', 'www.congress.gov', 'congress.gov'}
_TYPES = {'hr':'house-bill','s':'senate-bill','hres':'house-resolution','sres':'senate-resolution',
          'hjres':'house-joint-resolution','sjres':'senate-joint-resolution',
          'hconres':'house-concurrent-resolution','sconres':'senate-concurrent-resolution'}


def _safe_url(value):
    try:
        url = urlsplit(value or '')
        return value if (url.scheme=='https' and url.hostname in _HOSTS and not url.username and
                         not url.password and url.port in (None,443) and not any(ord(c)<33 for c in value)) else None
    except (ValueError,TypeError):
        return None


class _Plain(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts=[]; self.hidden=0
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style'): self.hidden+=1
        if tag in ('p','div','li','br'): self.parts.append(' ')
    def handle_endtag(self,tag):
        if tag in ('script','style'): self.hidden=max(0,self.hidden-1)
        if tag in ('p','div','li'): self.parts.append(' ')
    def handle_data(self,data):
        if not self.hidden: self.parts.append(data)


def _raw_bill(store,bill,cutoff):
    sha=bill.get('raw_hash','')
    if bill.get('dataset')!='official' or not re.fullmatch('[0-9a-f]{64}',sha): return None
    try:
        if timestamp(bill['observed_at'])>cutoff: return None
        receipt=store.checkpoint('raw:'+bill['bill_id']+':'+sha)
        # Audit imports can carry raw hashes but cannot make current XML historical.
        if not receipt or timestamp(receipt['retrieved_at'])>cutoff: return None
        path=ROOT/'data'/'raw'/sha
        if path.stat().st_size>20*1024*1024: return None
        raw=path.read_bytes()
        if hashlib.sha256(raw).hexdigest()!=sha or b'<!DOCTYPE' in raw.upper() or b'<!ENTITY' in raw.upper(): return None
        root=ET.fromstring(raw)
        for node in root.iter(): node.tag=node.tag.rsplit('}',1)[-1]
        item=root if root.tag=='bill' else root.find('bill')
        if item is None: return None
        ident=f"{int(item.findtext('congress'))}-{item.findtext('type','').lower()}{int(item.findtext('number'))}"
        return item if ident==bill['bill_id'] else None
    except (OSError,ET.ParseError,ValueError,TypeError,KeyError):
        return None


def _summary(raw,cutoff):
    if raw is None: return None
    summaries=[]
    for item in list(raw.findall('summaries/summary'))+list(raw.findall('summaries/item')):
        text=item.findtext('text') or item.findtext('cdata/text')
        dates=[item.findtext(k) for k in ('actionDate','updateDate') if item.findtext(k)]
        try:
            if not text or any(timestamp(d)>cutoff for d in dates): continue
        except (ValueError,TypeError): continue
        summaries.append((max(dates,default=''),text))
    if not summaries: return None
    parser=_Plain(); parser.feed(max(summaries,key=lambda x:x[0])[1])
    return ' '.join(''.join(parser.parts).split())


def context(store,dataset,bill_id,cutoff=None):
    if dataset not in ('official','demo'): raise ValueError('Unknown collection')
    cutoff=timestamp(cutoff or now())
    result=dict(related_bills=[],text_versions=[],changes=[],notes=[
        'Relationships are official source labels; they do not establish shared bill families or causal influence.',
        'Text versions link to official documents. Changes below compare observed metadata and summaries, not full legislative text.'])
    rows=store.db.execute("SELECT body FROM records WHERE kind='bill' AND dataset=? AND bill_id=? AND available_at<=? AND effective_at<=? ORDER BY available_at,effective_at,id",(dataset,bill_id,cutoff,cutoff)).fetchall()
    history=[json.loads(r[0]) for r in rows]
    if not history:
        result['notes'].append('No metadata available at this evidence date.')
        return result
    latest=history[-1]; raw=_raw_bill(store,latest,cutoff)
    if raw is None:
        result['notes'].append('No eligible retained bill-status XML at this evidence date; relationships and text links are unavailable.')
    else:
        seen=set()
        for item in raw.findall('relatedBills/item'):
            kind=item.findtext('type','').lower(); number=item.findtext('number',''); congress=item.findtext('congress','')
            if kind not in _TYPES or not number.isdigit() or not congress.isdigit(): continue
            bid=f'{int(congress)}-{kind}{int(number)}'
            relationships=[i.findtext('type','').strip() for i in item.findall('relationshipDetails/item')]
            relationships=[r for r in relationships if r] or ['Related bill (source-listed)']
            for relationship in relationships:
                if (bid,relationship) in seen: continue
                seen.add((bid,relationship))
                result['related_bills'].append(dict(bill_id=bid,title=item.findtext('title'),relationship=relationship,
                    source_url=f'https://www.congress.gov/bill/{int(congress)}th-congress/{_TYPES[kind]}/{int(number)}',
                    imported=store.bill(dataset,bid,cutoff) is not None))
        seen=set()
        for item in raw.findall('textVersions/item'):
            date=item.findtext('date')
            try:
                if date and timestamp(date)>cutoff: continue
            except (ValueError,TypeError): continue
            for fmt in item.findall('formats/item'):
                url=_safe_url(fmt.findtext('url'))
                if url and (date,url) not in seen:
                    seen.add((date,url))
                    result['text_versions'].append(dict(date=date,type=item.findtext('type') or 'Official text',url=url))
    previous=None
    for bill in history:
        # A later human assertion of old availability is not an earlier observed revision.
        if timestamp(bill['observed_at'])>cutoff: continue
        values={k:bill.get(k) for k in ('title','topic','sponsor')}
        summary=_summary(_raw_bill(store,bill,cutoff),cutoff)
        if summary is not None: values['summary']=summary
        if previous is not None:
            for field in ('title','topic','sponsor','summary'):
                if field in previous and field in values and previous[field]!=values[field]:
                    result['changes'].append(dict(field=field,before=previous[field],after=values[field],observed_at=bill['observed_at']))
        previous=values
    result['changes'].reverse()
    return result
