"""Consumer bill view with explicit evidence-time and forecast boundaries."""
from html.parser import HTMLParser
import re
import xml.etree.ElementTree as ET
from .store import ROOT, now, timestamp, congress_end
from .model import snapshot, forecast, resolution

class PlainText(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts=[]; self.hidden=0
    def handle_starttag(self, tag, attrs):
        if tag in ('script','style'): self.hidden+=1
    def handle_endtag(self, tag):
        if tag in ('script','style'): self.hidden=max(0,self.hidden-1)
        if tag in ('p','li','div'): self.parts.append('\n')
    def handle_data(self, data):
        if not self.hidden:self.parts.append(data)


def overview(bill, cutoff):
    fallback={'text':bill['title'],'label':'Official title / purpose' if bill['dataset']=='official' else 'Synthetic example purpose',
              'note':'This is the source title, not a full summary of the bill’s provisions.', 'source_url':bill['source_url']}
    raw_hash=bill.get('raw_hash','')
    if not re.fullmatch('[a-f0-9]{64}',raw_hash) or bill['observed_at']>cutoff:return fallback
    path=ROOT/'data'/'raw'/raw_hash
    if not path.exists():return fallback
    try:
        raw=path.read_bytes()
        if b'<!ENTITY' in raw.upper():return fallback
        root=ET.fromstring(raw)
        summaries=root.findall('bill/summaries/summary')+root.findall('bill/summaries/item')
        candidates=[s for s in summaries if (s.findtext('text') or s.findtext('cdata/text'))]
        if not candidates:return fallback
        item=max(candidates,key=lambda s:(s.findtext('actionDate',''), s.findtext('updateDate','')))
        parser=PlainText();parser.feed(item.findtext('text') or item.findtext('cdata/text'))
        text='\n\n'.join(' '.join(p.split()) for p in ''.join(parser.parts).split('\n') if p.strip())
        return {'text':text,'label':'Congressional Research Service summary', 'source_url':bill['source_url'],
                'note':'Official summary retained in the retrieved bill-status record; not an AI-generated interpretation.',
                'action_date':item.findtext('actionDate'),'version':item.findtext('actionDesc')}
    except (ET.ParseError,ValueError):return fallback


def detail(store,dataset,bill_id,cutoff=None):
    from . import bill_context, prospective
    if dataset not in ('official','demo'):raise ValueError('Unknown collection')
    cutoff=timestamp(cutoff or now())
    if cutoff>now():raise ValueError('Future evidence dates are not available')
    if not store.bill(dataset,bill_id):raise ValueError('Bill not imported. Import its official record first.')
    snap=snapshot(store,dataset,bill_id,cutoff)
    watched=bill_id in store.watched(dataset)
    if not snap:
        return {'bill_id':bill_id,'dataset':dataset,'as_of':cutoff,'watched':watched,'available':False,
                'reason':'No bill metadata demonstrably available at this evidence date. Open the latest imported record or inspect historical replay.'}
    bill=snap['bill'];outcome=resolution(store,dataset,bill_id,cutoff)
    ended=cutoff>=congress_end(bill['congress'])
    if outcome and outcome['value']==1: status='Enacted'
    elif outcome and outcome['value']==0:status='Did not become law by the recorded deadline'
    elif ended:status='Congress ended · final outcome not audited'
    else:status=snap['stage_name']
    estimate=forecast(store,dataset,bill_id,cutoff,persist=False)
    events=sorted(snap['events'],key=lambda e:(e['effective_at'],e['id']),reverse=True)
    return {'available':True,'bill_id':bill_id,'dataset':dataset,'as_of':cutoff,'watched':watched,
            'context':bill_context.context(store,dataset,bill_id,cutoff),
            'prospective':prospective.list_receipts(store,dataset,bill_id,20),
            'bill':bill,'overview':overview(bill,cutoff),'status':status,'events':events,'outcome':outcome,
            'forecast':{k:estimate.get(k) for k in ('status','reason','probability','issued_at','model_version','track','training_count','snapshot_hash','calibration_version','baseline_probability')},
            'forecast_note':'Experimental, unvalidated estimate. It is not a recommendation or a calibrated probability.',
            'research':{'evidence_count':len(snap['evidence_ids']),'snapshot_hash':snap['snapshot_hash'],
                        'effective_at':bill['effective_at'],'observed_at':bill['observed_at'],
                        'historical_availability':bill.get('archive_proof') or 'Historical availability has not been independently established; retrieval time is used.',
                        'family_status':bill.get('family_status','Not adjudicated'),
                        'coverage':'Imported subset; a missing enactment record is not proof of non-enactment.',
                        'model_validation':'The separate publication-version pilot did not establish Brier improvement over its baseline. This action-history model is also unvalidated.',
                        'forecast_target':'Own-bill public-law enactment by Congress end; provisions passed through another bill are not counted.',
                        'source_hash':bill.get('raw_hash'),'record_id':bill['id']}}
