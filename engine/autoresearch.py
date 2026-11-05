"""Bounded, opt-in development experiments over frozen audited samples.

No imports, network requests, human audit decisions, or production promotions.
The persistent identity prevents repeatedly optimizing against unchanged evidence.
"""
import json
import threading
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from .store import Store, now, digest
from . import sampling, sample_research, sessions

AGES=(90,180,365)
DEFAULTS=dict(enabled=False,interval_minutes=60,max_runs_per_cycle=3,daily_run_limit=12,sample_ids=[])
SCHEMA='''
CREATE TABLE IF NOT EXISTS autoresearch_settings (singleton INTEGER PRIMARY KEY CHECK(singleton=1),body TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS autoresearch_jobs (id TEXT PRIMARY KEY,identity TEXT UNIQUE NOT NULL,status TEXT NOT NULL,body TEXT NOT NULL);
'''
_GUARD=threading.Lock()
_LOCKS={}
_SCHEDULERS={}


def initialize(store):
    store.db.executescript(SCHEMA)
    with store.db:
        store.db.execute('INSERT OR IGNORE INTO autoresearch_settings VALUES (1,?)',(json.dumps(DEFAULTS),))


def _settings(store):
    initialize(store)
    return json.loads(store.db.execute('SELECT body FROM autoresearch_settings WHERE singleton=1').fetchone()[0])


def configure(store,args):
    from . import campaigns
    initialize(store)
    active_campaign_samples=campaigns.active_sample_ids(store)
    if not isinstance(args,dict) or set(args)-set(DEFAULTS):raise ValueError('Unknown automatic research setting.')
    if 'enabled' in args and type(args['enabled']) is not bool:raise ValueError('enabled must be boolean.')
    for key,low,high in [('interval_minutes',15,10080),('max_runs_per_cycle',1,10),('daily_run_limit',1,100)]:
        if key in args and (type(args[key]) is not int or not low<=args[key]<=high):raise ValueError(f'{key} must be {low}–{high}.')
    if 'sample_ids' in args:
        ids=args['sample_ids']
        if not isinstance(ids,list) or len(ids)>20 or any(not isinstance(v,str) for v in ids) or len(set(ids))!=len(ids):raise ValueError('Select at most 20 distinct audited sample IDs.')
        sampling.initialize(store)
        for ident in ids:sampling.get_sample(store,ident)
    try:
        store.db.execute('BEGIN IMMEDIATE')
        settings=json.loads(store.db.execute('SELECT body FROM autoresearch_settings WHERE singleton=1').fetchone()[0]);settings.update(args)
        if settings['enabled'] and not settings['sample_ids'] and not active_campaign_samples:raise ValueError('Select an audited sample or activate a campaign before enabling automatic research.')
        store.db.execute('UPDATE autoresearch_settings SET body=? WHERE singleton=1',(json.dumps(settings),));store.db.commit()
    except Exception:
        store.db.rollback();raise
    return summary(store)


def _jobs(store):
    return [json.loads(r[0]) for r in store.db.execute('SELECT body FROM autoresearch_jobs ORDER BY rowid')]


def _save(store,job):
    with store.db:
        store.db.execute('INSERT INTO autoresearch_jobs VALUES (?,?,?,?) ON CONFLICT(id) DO UPDATE SET status=excluded.status,body=excluded.body',(job['id'],job['identity'],job['status'],json.dumps(job)))


def _used(store):
    day=now()[:10]
    return sum(j.get('budget_day',(j.get('started_at') or '')[:10])==day for j in _jobs(store))


def _fingerprint(store,sample):
    selected=set(sample['bill_ids'])
    evidence=[dict(r) for r in store.db.execute("SELECT * FROM records WHERE dataset='official' ORDER BY id") if r['bill_id'] in selected]
    code=dict(sessions._code())
    for name in ('sampling.py','sample_research.py','autoresearch.py'):
        code[name]=digest(Path(__file__).with_name(name).read_text())
    return dict(sample_hash=sample['hash'],evidence_hash=digest(evidence),audit_hash=digest(sample.get('audits',{})),implementation_hashes=code)


def summary(store):
    settings=_settings(store);jobs=_jobs(store);cycle=store.checkpoint('autoresearch:last_cycle');used=_used(store)
    due=None
    if settings['enabled']:
        stamp=(cycle or {}).get('started_at')
        due=(datetime.fromisoformat(stamp.replace('Z','+00:00'))+timedelta(minutes=settings['interval_minutes'])).isoformat().replace('+00:00','Z') if stamp else now()
    return dict(settings=settings,jobs=list(reversed(jobs[-100:])),last_cycle=cycle,next_due=due,daily_used=used,daily_remaining=max(0,settings['daily_run_limit']-used),checkpoint_ages=list(AGES),scheduler_running=str(store.path.resolve()) in _SCHEDULERS,
                runtime_note='Runs only while this local server is running. Local structured development only; no paid model calls or automatic imports. Unchanged evidence is skipped. Repeated development scores are not independent validation or permission to release a model.')


def _existing_session(store,job):
    sessions.initialize(store)
    title='Automatic development '+job['id']
    found=[]
    for row in store.db.execute('SELECT body FROM research_sessions ORDER BY rowid DESC'):
        proposal=json.loads(row[0])
        if proposal['title']==title:found.append(proposal)
    matching=next((p for p in found if p['config']['age_days']==job['age_days']),None)
    return sessions.get_session(store,matching['id']) if matching else (sessions.get_session(store,found[0]['id']) if found else None)


def _run(store,job):
    job.update(status='running',started_at=job.get('started_at') or now(),budget_day=now()[:10],message='Checking frozen sample eligibility.');_save(store,job)
    try:
        proposal=_existing_session(store,job)
        if proposal is None:
            sample=sampling.get_sample(store,job['sample_id'])
            if _fingerprint(store,sample)!=job['fingerprint']:
                job.update(status='blocked',message='Evidence changed while queued. A fresh identity will be considered next cycle.');return
            proposal=sample_research.propose(store,{'sample_id':job['sample_id'],'title':'Automatic development '+job['id']})
        if proposal['config']['age_days']!=job['age_days']:
            proposal=sessions.revise(store,proposal['id'],{'age_days':job['age_days']})
        job['session_id']=proposal['id'];_save(store,job)
        if proposal['preflight']['blockers']:
            job.update(status='blocked',message='; '.join(proposal['preflight']['blockers']));return
        result=sessions.execute(store,proposal['id'])
        job.update(status='completed',message='Development experiment completed. No production promotion.',result_status=result['status'])
    except Exception as exc:
        job.update(status='failed',message=str(exc)[:2000])
    finally:
        job['finished_at']=now();_save(store,job)


def tick(store):
    from . import campaigns
    initialize(store)
    key=str(store.path.resolve())
    with _GUARD:lock=_LOCKS.setdefault(key,threading.Lock())
    if not lock.acquire(blocking=False):
        result=summary(store);result['tick_status']='already_running';return result
    try:
        settings=_settings(store)
        if not settings['enabled']:
            result=summary(store);result['tick_status']='paused';return result
        cycle=dict(id=str(uuid.uuid4()),started_at=now(),status='running',results=[])
        store.checkpoint('autoresearch:last_cycle',cycle)
        # At most one cycle's work is persisted; interrupted work is handled first.
        selected=list(dict.fromkeys(settings['sample_ids']+campaigns.active_sample_ids(store)))
        selected=[sid for sid in selected if (lambda p:p['allowed'] or bool(p['campaigns']))(campaigns.scheduling_policy(store,sid))]
        pending=[j for j in _jobs(store) if j['status'] in ('queued','recovered') and j['sample_id'] in selected]
        capacity=min(settings['max_runs_per_cycle'],max(0,settings['daily_run_limit']-_used(store)))
        known={j['identity'] for j in _jobs(store)}
        if capacity>0 and len(pending)<capacity:
            for sample_id in selected:
                if not campaigns.scheduling_policy(store,sample_id)['allowed']:continue
                sample=sampling.get_sample(store,sample_id);fingerprint=_fingerprint(store,sample)
                for age in AGES:
                    identity=digest(dict(fingerprint=fingerprint,age_days=age))
                    if identity in known:continue
                    job=dict(id=str(uuid.uuid4()),identity=identity,sample_id=sample_id,age_days=age,fingerprint=fingerprint,status='queued',session_id=None,created_at=now(),message='Waiting for the local development runner.')
                    _save(store,job);known.add(identity);pending.append(job)
                    if len(pending)>=capacity:break
                if len(pending)>=capacity:break
        campaign_counts={}
        for job in pending[:settings['max_runs_per_cycle']]:
            current=_settings(store)
            if not current['enabled']:break
            if job['sample_id'] not in current['sample_ids']+campaigns.active_sample_ids(store):continue
            policy=campaigns.scheduling_policy(store,job['sample_id'])
            charged_today=job.get('budget_day',(job.get('started_at') or '')[:10])==now()[:10]
            if not policy['allowed'] and not (charged_today and policy['campaigns']):continue
            if any((p['daily_remaining']<=0 and not charged_today) or campaign_counts.get(p['campaign_id'],0)>=p['max_runs_per_cycle'] for p in policy['campaigns']):continue
            if job.get('budget_day',(job.get('started_at') or '')[:10])!=now()[:10] and _used(store)>=current['daily_run_limit']:break
            _run(store,job);cycle['results'].append(dict(id=job['id'],status=job['status'],session_id=job.get('session_id')))
            for p in policy['campaigns']:campaign_counts[p['campaign_id']]=campaign_counts.get(p['campaign_id'],0)+1
            store.checkpoint('autoresearch:last_cycle',cycle)
        cycle.update(status='completed' if _settings(store)['enabled'] else 'paused',finished_at=now())
        store.checkpoint('autoresearch:last_cycle',cycle)
        return summary(store)
    finally:lock.release()


def recover(store):
    """Startup only, before scheduler starts. Reuse any already persisted session."""
    initialize(store)
    for job in _jobs(store):
        if job['status']=='running':
            job.update(status='recovered',message='Interrupted run recovered; existing frozen session and result will be reused.');_save(store,job)
    cycle=store.checkpoint('autoresearch:last_cycle')
    if cycle and cycle['status']=='running':
        cycle.update(status='recovered',finished_at=now());store.checkpoint('autoresearch:last_cycle',cycle)
    return summary(store)


def start_scheduler(db_path=None):
    probe=Store(db_path);initialize(probe);path=probe.path.resolve();probe.close();key=str(path)
    with _GUARD:
        if key in _SCHEDULERS:return _SCHEDULERS[key]
        stop=threading.Event();_SCHEDULERS[key]=stop
    def work():
        store=Store(path)
        try:
            while not stop.is_set():
                try:
                    from . import coverage_pipeline
                    coverage_pipeline.advance(store)
                except Exception:
                    store.checkpoint('coverage:worker_error',{'at':now(),'message':'Coverage worker could not advance. Review the import plan and retry.'})
                try:
                    settings=_settings(store);cycle=store.checkpoint('autoresearch:last_cycle') or {};stamp=cycle.get('started_at')
                    elapsed=(datetime.now(timezone.utc)-datetime.fromisoformat(stamp.replace('Z','+00:00'))).total_seconds() if stamp else float('inf')
                    if settings['enabled'] and elapsed>=settings['interval_minutes']*60:tick(store)
                except Exception:
                    store.checkpoint('autoresearch:last_cycle',dict(status='failed',started_at=now(),finished_at=now(),message='Automatic development failed. Inspect saved jobs before retrying.',results=[]))
                stop.wait(30)
        finally:
            store.close()
            with _GUARD:_SCHEDULERS.pop(key,None)
    threading.Thread(target=work,name='automatic-development',daemon=True).start()
    return stop
