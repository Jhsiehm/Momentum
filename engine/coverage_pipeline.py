"""Durable, exact-population coverage imports; coverage is not model eligibility."""
import json
import threading
import uuid
from datetime import datetime, timedelta, timezone
from . import sampling
from .store import now, digest, timestamp


def initialize(store):
    sampling.initialize(store)
    store.db.execute('CREATE TABLE IF NOT EXISTS coverage_plans(id TEXT PRIMARY KEY, body TEXT NOT NULL)')
    store.db.commit()


def _save(store, plan):
    store.db.execute('INSERT OR REPLACE INTO coverage_plans VALUES (?,?)', (plan['id'], json.dumps(plan)))


def _raw(store, ident):
    row = store.db.execute('SELECT body FROM coverage_plans WHERE id=?', (ident,)).fetchone()
    if not row:
        raise ValueError('Coverage plan not found.')
    return json.loads(row[0])


def get_plan(store, ident):
    initialize(store)
    plan = _raw(store, ident)
    jobs = [sampling.get_bulk_job(store, b['job_id']) for b in plan['batches'] if b.get('job_id')]
    plan['progress'] = dict(total=plan['total'], completed=sum(j['completed'] for j in jobs),
                            imported=sum(j['parsed'] for j in jobs), failed=sum(j['failed'] for j in jobs),
                            batches=len(plan['batches']), batches_completed=sum(j['status']=='completed' for j in jobs))
    plan['jobs'] = [{k:j[k] for k in ('id','status','total','completed','parsed','failed')} for j in jobs]
    return plan


def list_plans(store):
    initialize(store)
    ids = [r[0] for r in store.db.execute('SELECT id FROM coverage_plans ORDER BY rowid DESC')]
    return [get_plan(store, ident) for ident in ids]


def plan_import(store, args):
    initialize(store)
    inv = sampling._load(store, 'sample_inventories', args.get('inventory_id'))
    congresses = args.get('congresses', [min(inv['congresses'])])
    if not isinstance(congresses,list) or not congresses or any(type(c)!=int or c not in inv['congresses'] for c in congresses):
        raise ValueError('Choose Congresses present in the saved inventory.')
    congresses = sorted(set(congresses))
    ids = list(dict.fromkeys(b for b in inv['bill_ids'] if int(b.split('-')[0]) in congresses))
    if not ids:
        raise ValueError('Selected population is empty.')
    batch_size = args.get('batch_size', 250)
    if type(batch_size)!=int or not 1<=batch_size<=sampling.MAX_BULK:
        raise ValueError('Batch size must be 1–10000.')
    population = dict(inventory_id=inv['id'], inventory_hash=inv['hash'], congresses=congresses, bill_ids=ids)
    population_hash = digest(population)
    # A repeated create is idempotent, including completed populations.
    for existing in list_plans(store):
        if existing['population_hash']==population_hash:
            return existing
    plan = dict(id=str(uuid.uuid4()), name='Official coverage · '+', '.join(map(str,congresses)),
                created_at=now(), status='active', population_hash=population_hash, **population,
                total=len(ids), batch_size=batch_size, batches=[dict(bill_ids=ids[i:i+batch_size], job_id=None)
                                       for i in range(0,len(ids),batch_size)],
                provenance=[{k:s[k] for k in ('congress','type','source_url','raw_hash','retrieved_at')}
                            for s in inv['strata'] if s['congress'] in congresses],
                note='Exact saved directory population. Pause takes effect between batches. Imported records do not establish historical eligibility.')
    with store.db:
        _save(store, plan)
    return get_plan(store, plan['id'])


def update_plan(store, ident, args):
    initialize(store)
    action = args.get('action')
    if action not in ('pause','resume'):
        raise ValueError('Choose pause or resume.')
    with store.db:
        store.db.execute('BEGIN IMMEDIATE')
        plan = _raw(store, ident)
        if plan['status']=='completed':
            raise ValueError('Coverage plan already completed.')
        plan.update(status='paused' if action=='pause' else 'active', updated_at=now())
        if action=='resume':
            plan['retry_requested'] = True
        _save(store, plan)
    return get_plan(store, ident)


def advance(store, launch=True):
    """Advance at most one batch. Call after sampling recovery and on worker ticks."""
    initialize(store)
    job = None
    retry = None
    with store.db:
        store.db.execute('BEGIN IMMEDIATE')
        if store.db.execute("SELECT 1 FROM bulk_import_jobs WHERE status IN ('queued','running') LIMIT 1").fetchone():
            return None
        for row in store.db.execute('SELECT body FROM coverage_plans ORDER BY rowid').fetchall():
            plan = json.loads(row[0])
            if plan['status']!='active':
                continue
            for batch in plan['batches']:
                if batch['job_id']:
                    prior = json.loads(store.db.execute('SELECT body FROM bulk_import_jobs WHERE id=?',(batch['job_id'],)).fetchone()[0])
                    if prior['status']=='completed':
                        continue
                    if prior['status']=='interrupted' or (prior['status']=='completed_with_errors' and plan.get('retry_requested')):
                        retry = prior['id']
                        plan.pop('retry_requested',None)
                    else:
                        plan.update(status='blocked', blocker='A batch has failed records. Resume to retry failed records before the next batch.')
                    _save(store, plan)
                    break
                job = dict(id=str(uuid.uuid4()), status='queued', sample_id=None, coverage_plan_id=plan['id'],
                           bill_ids=batch['bill_ids'], total=len(batch['bill_ids']), completed=0, parsed=0, failed=0,
                           downloaded=None, audited=0, results=[], refresh=False, created_at=now(),
                           note='Coverage batch; parsed includes cached records. No historical eligibility inferred.')
                batch['job_id'] = job['id']
                plan.pop('retry_requested',None)
                store.db.execute('INSERT INTO bulk_import_jobs VALUES (?,?,?)',(job['id'],job['status'],json.dumps(job)))
                _save(store, plan)
                break
            else:
                plan.update(status='completed', finished_at=now())
                _save(store,plan)
                continue
            break
    if retry:
        return sampling.retry_bulk_job(store,retry,launch=launch)
    if job and launch:
        threading.Thread(target=sampling.run_bulk_job,args=(store.path,job['id']),daemon=True,name='coverage-import').start()
    return job


def summary(store):
    initialize(store)
    inventories = sampling.list_inventories(store)
    population = set(b for inv in inventories for b in inv['bill_ids'])
    bills = {b['bill_id']:b for b in store.bills('official')}
    events = {r[0] for r in store.db.execute("SELECT DISTINCT bill_id FROM records WHERE kind='event' AND dataset='official'")}
    outcomes = {r[0] for r in store.db.execute("SELECT DISTINCT bill_id FROM records WHERE kind='resolution' AND dataset='official'")}
    audits = {}
    for r in store.db.execute('SELECT body FROM sample_audits ORDER BY rowid'):
        audit = json.loads(r[0]); audits[audit['bill_id']] = audit
    historical = set()
    # Metadata availability is a narrow measurable condition, not scoreability.
    for r in store.db.execute("SELECT bill_id,available_at,effective_at,body FROM records WHERE kind='bill' AND dataset='official' ORDER BY available_at,effective_at,id"):
        b = json.loads(r['body'])
        try:
            checkpoint = datetime.fromisoformat(timestamp(b['introduced_at']).replace('Z','+00:00'))+timedelta(days=180)
            if (datetime.fromisoformat(r['available_at'].replace('Z','+00:00'))<=checkpoint and
                datetime.fromisoformat(r['effective_at'].replace('Z','+00:00'))<=checkpoint and
                checkpoint<=datetime.now(timezone.utc)):
                historical.add(r['bill_id'])
        except (ValueError,KeyError,TypeError):
            pass
    def counts(ids):
        imported = ids & bills.keys()
        return dict(population=len(ids), imported=len(imported), downloaded=None,
                    audited=len(ids & audits.keys()), audit_passed=sum(audits[b]['status']=='passed' for b in ids & audits.keys()),
                    historical_metadata_eligible=len(ids & historical), historical_eligible=None, training_eligible=None,
                    evaluation_ready=None, outcomes_known=len(ids & outcomes), outcomes_unknown=len(imported-outcomes))
    all_ids = population | bills.keys()
    result = counts(all_ids)
    result['inventory_total'] = len(population)
    result['field_coverage'] = dict(title=sum(bool(b.get('title')) for b in bills.values()),
        topic=sum(bool(b.get('topic')) and b.get('topic')!='Unclassified' for b in bills.values()),
        actions=len(events & bills.keys()), outcomes=len(outcomes & bills.keys()),
        adjudicated_family=sum(bool(b.get('family_status')) and 'unadjudicated' not in b.get('family_status','').lower() for b in bills.values()),
        full_text=None, sponsor_network=None)
    result['congresses'] = [dict(congress=c,**counts({b for b in all_ids if b.startswith(str(c)+'-')}))
                           for c in sorted({int(b.split('-')[0]) for b in all_ids})]
    result['inventories'] = [{k:i[k] for k in ('id','hash','congresses','total','discovered_at','status')} for i in inventories]
    result['plans'] = list_plans(store)
    result['note'] = 'Metadata eligible means metadata available by introduction + 180 days only. Training and evaluation eligibility require experiment-specific evidence, family, outcome and audit checks. Unknown is not zero; downloads cannot be counted separately from cached imports.'
    return result
