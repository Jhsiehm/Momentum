"""Frozen official directory samples, human audit records, and resumable bulk imports.

Directory completeness means a fully received directory listing, not historical
availability, eligible outcomes, or a protected evaluation set.
"""
import csv
import io
import json
import random
import re
import threading
import uuid
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
from .store import Store, now, digest, congress_end
from . import collections
from .ingest import fetch, ingest_bill, retain

MAX_BULK = 10000
SCHEMA = '''
CREATE TABLE IF NOT EXISTS sample_inventories(id TEXT PRIMARY KEY, body TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS research_samples(id TEXT PRIMARY KEY, body TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS sample_audits(id TEXT PRIMARY KEY, sample_id TEXT, bill_id TEXT, body TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS bulk_import_jobs(id TEXT PRIMARY KEY,status TEXT NOT NULL,body TEXT NOT NULL);
CREATE TRIGGER IF NOT EXISTS inventories_frozen BEFORE UPDATE ON sample_inventories BEGIN SELECT RAISE(ABORT,'Inventory immutable'); END;
CREATE TRIGGER IF NOT EXISTS samples_frozen BEFORE UPDATE ON research_samples BEGIN SELECT RAISE(ABORT,'Sample immutable'); END;
CREATE TRIGGER IF NOT EXISTS audits_frozen BEFORE UPDATE ON sample_audits BEGIN SELECT RAISE(ABORT,'Audit append-only'); END;
CREATE TRIGGER IF NOT EXISTS inventories_no_delete BEFORE DELETE ON sample_inventories BEGIN SELECT RAISE(ABORT,'Inventory immutable'); END;
CREATE TRIGGER IF NOT EXISTS samples_no_delete BEFORE DELETE ON research_samples BEGIN SELECT RAISE(ABORT,'Sample immutable'); END;
CREATE TRIGGER IF NOT EXISTS audits_no_delete BEFORE DELETE ON sample_audits BEGIN SELECT RAISE(ABORT,'Audit append-only'); END;
'''

def initialize(store):
    store.db.executescript(SCHEMA)

def _load(store, table, ident):
    initialize(store)
    row = store.db.execute('SELECT body FROM '+table+' WHERE id=?',(ident,)).fetchone()
    if not row: raise ValueError('Record not found.')
    return json.loads(row[0])

def _list(store, table):
    initialize(store)
    return [json.loads(r[0]) for r in store.db.execute('SELECT body FROM '+table+' ORDER BY rowid DESC LIMIT 100')]

class DirectoryParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.names=[]
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag=='a' and attrs.get('href'): self.links.append(attrs['href'])
        if tag=='tr' and attrs.get('data-name'): self.names.append(attrs['data-name'])

def parse_directory(raw, congress, kind):
    html=raw.decode('utf-8')
    if '</html>' not in html.lower() or '</table>' not in html.lower():
        raise ValueError('Directory response is incomplete; no sampling allowed.')
    parser=DirectoryParser(); parser.feed(html)
    base=f'https://www.govinfo.gov/bulkdata/BILLSTATUS/{congress}/{kind}/'
    pattern=re.compile(r'BILLSTATUS-'+str(congress)+kind+r'([1-9]\d*)\.xml')
    ids=set()
    for href in parser.links:
        target=urlparse(urljoin(base,href))
        if target.scheme!='https' or target.netloc!='www.govinfo.gov': continue
        match=pattern.fullmatch(target.path.rsplit('/',1)[-1])
        if match and target.path==f'/bulkdata/BILLSTATUS/{congress}/{kind}/'+match[0]:
            ids.add(f'{congress}-{kind}{match[1]}')
        if target.path.rstrip('/')==urlparse(base).path.rstrip('/') and target.query:
            raise ValueError('Paginated directory is unsupported; inventory cannot be certified complete.')
    names={n for n in parser.names if pattern.fullmatch(n)}
    if not ids or len(names)!=len(ids):
        raise ValueError('Directory file rows and links do not match; inventory cannot be certified complete.')
    return sorted(ids,key=lambda b: int(b.split('-')[1][len(kind):]))

def discover_inventory(store,args):
    initialize(store)
    congresses=args.get('congresses',[114,116,118])
    if not isinstance(congresses,list) or not 1<=len(congresses)<=6 or any(type(c)!=int or c<113 or congress_end(c)>=now() for c in congresses):
        raise ValueError('Choose 1–6 completed Congresses from 113 onward.')
    congresses=sorted(set(congresses)); strata=[]; all_ids=[]
    for congress in congresses:
        for kind in ('hr','s'):
            url=f'https://www.govinfo.gov/bulkdata/BILLSTATUS/{congress}/{kind}'
            # Reuse retained, validated inventories unless an explicit fresh discovery is requested.
            cached=next((s for inv in _list(store,'sample_inventories') for s in inv['strata'] if s['congress']==congress and s['type']==kind),None)
            if cached and not args.get('refresh',False):
                stratum=cached
            else:
                raw=fetch(url); ids=parse_directory(raw,congress,kind)
                stratum=dict(congress=congress,type=kind,count=len(ids),bill_ids=ids,source_url=url,raw_hash=retain(raw),retrieved_at=now())
            strata.append(stratum); all_ids.extend(stratum['bill_ids'])
    body=dict(congresses=congresses,strata=strata,bill_ids=all_ids,total=len(all_ids),discovered_at=now(),status='directory_complete',note='Complete received GovInfo directory listings only. Historical evidence availability and outcome eligibility require a separate audit.')
    body['hash']=digest(body); body['id']=str(uuid.uuid4())
    with store.db: store.db.execute('INSERT INTO sample_inventories VALUES (?,?)',(body['id'],json.dumps(body)))
    return body

def list_inventories(store): return _list(store,'sample_inventories')

def _allocation(strata,size):
    total=sum(s['count'] for s in strata)
    counts=[size*s['count']//total for s in strata]
    order=sorted(range(len(strata)),key=lambda i: (-(size*strata[i]['count']%total),i))
    for i in order[:size-sum(counts)]: counts[i]+=1
    return counts

def create_sample(store,args):
    inv=_load(store,'sample_inventories',args.get('inventory_id'))
    size=args.get('size',100); audit_size=args.get('audit_size',25); seed=args.get('seed','legislative-sample-v1')
    name=args.get('name','Audited development sample')
    if type(size)!=int or not 1<=size<=min(MAX_BULK,inv['total']): raise ValueError('Sample size must be 1–10000 and no larger than the inventory.')
    if type(audit_size)!=int or not 1<=audit_size<=min(size,500): raise ValueError('Audit size must be 1–500 and no larger than the sample.')
    if not isinstance(seed,str) or not 1<=len(seed)<=200: raise ValueError('Supply a reproducible seed of 1–200 characters.')
    if not isinstance(name,str) or not 1<=len(name.strip())<=80: raise ValueError('Name must contain 1–80 characters.')
    rng=random.Random(seed); ids=[]; strata=[]
    for stratum,n in zip(inv['strata'],_allocation(inv['strata'],size)):
        chosen=sorted(rng.sample(stratum['bill_ids'],n)); ids.extend(chosen)
        strata.append(dict(congress=stratum['congress'],type=stratum['type'],population=stratum['count'],selected=n))
    audit=random.Random(seed+':human-audit-v1').sample(ids,audit_size)
    latest=max(inv['congresses']); train=[b for b in ids if int(b.split('-')[0])<latest]; test=[b for b in ids if int(b.split('-')[0])==latest]
    # Collections are immutable versions; sample saves their exact references.
    def batches(bills,label):
        return [collections.save_collection(store,dict(name=f'{name.strip()} · {label} {i//100+1}',bill_ids=bills[i:i+100]))['id'] for i in range(0,len(bills),100)]
    all_collections=batches(ids,'sample'); training=batches(train,'training'); evaluation=batches(test,'evaluation')
    body=dict(id=str(uuid.uuid4()),name=name.strip(),created_at=now(),inventory_id=inv['id'],inventory_hash=inv['hash'],seed=seed,algorithm='proportional-largest-remainder + Python Random.sample v1',size=size,audit_size=audit_size,bill_ids=ids,audit_bill_ids=audit,strata=strata,collection_ids=all_collections,collection_id=all_collections[0],training_collection_ids=training,evaluation_collection_ids=evaluation,evaluation_collection_id=evaluation[0] if len(evaluation)==1 else None,collection_version=1,protocol=dict(train_congresses=[c for c in inv['congresses'] if c<latest],test_congress=latest,checkpoint_days=180,target='Own-bill enactment by Congress end',candidate='Existing action-history model',baseline='Prior training enactment rate',split='Chronological Congress split',notes='Development sample, not a protected holdout. Use the sample comparison route to restrict training to this frozen sampled universe. Generic collection experiments may use additional prior eligible imported records. Historical availability, family linkage, and negative outcomes require adjudication.'),exclusions=[])
    body['hash']=digest(body)
    with store.db: store.db.execute('INSERT INTO research_samples VALUES (?,?)',(body['id'],json.dumps(body)))
    return get_sample(store,body['id'])

def get_sample(store,ident):
    sample=_load(store,'research_samples',ident)
    audits={}
    for row in store.db.execute('SELECT body FROM sample_audits WHERE sample_id=? ORDER BY rowid',(ident,)):
        entry=json.loads(row[0]); audits[entry['bill_id']]=entry
    imported=sum(store.bill('official',b) is not None for b in sample['bill_ids'])
    passed=sum(a['status']=='passed' for a in audits.values())
    sample['audits']=audits
    sample['readiness']=dict(imported=imported,total=sample['size'],audit_total=sample['audit_size'],audited=len(audits),audit_passed=passed,status='needs_evidence_review',historical_eligible=None,blockers=['Current downloads do not prove historical availability.','Family linkage and negative outcomes require adjudication.']+(['Human audit remains incomplete.'] if passed<sample['audit_size'] else []),note='Human review records do not change evidence availability or automatically unlock historical experiments.')
    return sample

def list_samples(store): return [get_sample(store,s['id']) for s in _list(store,'research_samples')]

def save_audit(store,args):
    sample=get_sample(store,args.get('sample_id')); bid=args.get('bill_id'); status=args.get('status'); notes=args.get('notes','')
    if bid not in sample['audit_bill_ids']: raise ValueError('Bill is not in the frozen audit subset.')
    if status not in ('passed','needs_correction'): raise ValueError('Audit status must be passed or needs_correction.')
    checks=args.get('checks',{})
    fields=('identity','source','availability','family','outcome')
    if not isinstance(checks,dict) or any(type(checks.get(k)) is not bool for k in fields): raise ValueError('Record all five audit checks as booleans.')
    if status=='passed' and not all(checks[k] for k in fields): raise ValueError('Passing requires all five checks.')
    if not isinstance(notes,str) or not 1<=len(notes.strip())<=4000: raise ValueError('Record review evidence or correction notes (1–4000 characters).')
    entry=dict(id=str(uuid.uuid4()),sample_id=sample['id'],bill_id=bid,status=status,checks={k:checks[k] for k in fields},notes=notes.strip(),reviewed_at=now())
    with store.db: store.db.execute('INSERT INTO sample_audits VALUES (?,?,?,?)',(entry['id'],sample['id'],bid,json.dumps(entry)))
    return get_sample(store,sample['id'])

def export_audit_csv(store,ident):
    sample=get_sample(store,ident); output=io.StringIO(newline=''); writer=csv.writer(output)
    writer.writerow(['sample_id','sample_hash','bill_id','source_url','title','review_status','identity','source','availability','family','outcome','review_notes'])
    def safe(value):
        value=str(value)
        return "'"+value if value.lstrip().startswith(('=','+','-','@','\t','\r')) else value
    for bid in sample['audit_bill_ids']:
        congress,kind,number=collections.parse_bill_id(bid); bill=store.bill('official',bid) or {}; audit=sample['audits'].get(bid,{})
        writer.writerow([safe(v) for v in [sample['id'],sample['hash'],bid,f'https://www.govinfo.gov/bulkdata/BILLSTATUS/{congress}/{kind}/BILLSTATUS-{congress}{kind}{number}.xml',bill.get('title','Not imported'),audit.get('status','pending'),*[audit.get('checks',{}).get(k,'') for k in ('identity','source','availability','family','outcome')],audit.get('notes','')]])
    return output.getvalue()

def get_bulk_job(store,ident): return _load(store,'bulk_import_jobs',ident)
def list_bulk_jobs(store): return _list(store,'bulk_import_jobs')

def _save_job(store,job):
    job['completed']=len(job['results']); job['parsed']=sum(r['status']=='success' for r in job['results']); job['failed']=sum(r['status']=='failed' for r in job['results'])
    with store.db: store.db.execute('UPDATE bulk_import_jobs SET status=?,body=? WHERE id=?',(job['status'],json.dumps(job),job['id']))

def start_bulk_job(store,args,launch=True):
    initialize(store)
    sample=get_sample(store,args['sample_id']) if args.get('sample_id') else None
    ids=sample['bill_ids'] if sample else args.get('bill_ids')
    if not isinstance(ids,list) or not 1<=len(ids)<=MAX_BULK: raise ValueError('Supply 1–10000 official bill identifiers.')
    ids=list(dict.fromkeys(f'{c}-{k}{n}' for c,k,n in (collections.parse_bill_id(b) for b in ids)))
    if type(args.get('refresh',False)) is not bool: raise ValueError('refresh must be boolean.')
    job=dict(id=str(uuid.uuid4()),status='queued',sample_id=sample['id'] if sample else None,bill_ids=ids,total=len(ids),completed=0,parsed=0,failed=0,downloaded=None,audited=0,results=[],refresh=args.get('refresh',False),created_at=now(),note='Parsed includes unchanged cached records. Download count is unavailable separately from parsing. Imports never constitute human audit or historical eligibility.')
    try:
        store.db.execute('BEGIN IMMEDIATE')
        if store.db.execute("SELECT COUNT(*) FROM bulk_import_jobs WHERE status IN ('queued','running')").fetchone()[0]>=1: raise ValueError('A bulk import is already active.')
        store.db.execute('INSERT INTO bulk_import_jobs VALUES (?,?,?)',(job['id'],job['status'],json.dumps(job))); store.db.commit()
    except Exception:
        store.db.rollback(); raise
    if launch: threading.Thread(target=run_bulk_job,args=(store.path,job['id']),daemon=True,name='bulk-import').start()
    return job

def run_bulk_job(db_path,ident):
    store=Store(db_path)
    try:
        job=get_bulk_job(store,ident)
        if job['status']!='queued': return job
        job.update(status='running',started_at=now())
        with store.db:
            claimed=store.db.execute("UPDATE bulk_import_jobs SET status='running',body=? WHERE id=? AND status='queued'",(json.dumps(job),ident)).rowcount
        if not claimed: return get_bulk_job(store,ident)
        done={r['bill_id'] for r in job['results']}
        for bid in job['bill_ids']:
            if bid in done: continue
            try:
                result=ingest_bill(store,*collections.parse_bill_id(bid),refresh=job['refresh'])
                job['results'].append(dict(bill_id=bid,status='success',result=result))
            except Exception:
                job['results'].append(dict(bill_id=bid,status='failed',error='Official source import failed. Retry this record.'))
            _save_job(store,job)
        job.update(status='completed_with_errors' if job['failed'] else 'completed',finished_at=now()); _save_job(store,job)
        return job
    finally: store.close()

def retry_bulk_job(store,ident,launch=True):
    initialize(store)
    try:
        store.db.execute('BEGIN IMMEDIATE')
        row=store.db.execute('SELECT body FROM bulk_import_jobs WHERE id=?',(ident,)).fetchone()
        if not row: raise ValueError('Import job not found.')
        job=json.loads(row[0])
        if job['status'] not in ('interrupted','completed_with_errors'): raise ValueError('Only interrupted or failed imports can be resumed.')
        if store.db.execute("SELECT COUNT(*) FROM bulk_import_jobs WHERE status IN ('queued','running')").fetchone()[0]: raise ValueError('A bulk import is already active.')
        job.setdefault('previous_attempts',[]).append(dict(results=job['results'],finished_at=job.get('finished_at'),status=job['status']))
        job['results']=[r for r in job['results'] if r['status']=='success']; job.update(status='queued',resumed_at=now()); job.pop('error',None)
        job['completed']=len(job['results']); job['parsed']=job['completed']; job['failed']=0
        store.db.execute('UPDATE bulk_import_jobs SET status=?,body=? WHERE id=?',(job['status'],json.dumps(job),ident))
        store.db.commit()
    except Exception:
        store.db.rollback(); raise
    if launch: threading.Thread(target=run_bulk_job,args=(store.path,job['id']),daemon=True,name='bulk-import').start()
    return job

def recover_bulk_jobs(store):
    initialize(store)
    for job in list_bulk_jobs(store):
        if job['status'] in ('queued','running'):
            job.update(status='interrupted',error='Server stopped. Resume to retry unfinished records; completed records are preserved.')
            _save_job(store,job)
