"""Opt-in, process-local watcher. All refreshes preserve retrieval-time evidence."""
import json
import threading
import uuid
from datetime import datetime, timedelta, timezone
from .store import Store, now, digest
from .collections import parse_bill_id
from .ingest import ingest_bill

DEFAULTS={'enabled':False,'interval_minutes':60,'notifications':True}
_LOCKS={}
_SCHEDULERS={}
_GUARD=threading.Lock()
SCHEMA='''
CREATE TABLE IF NOT EXISTS monitoring_settings (singleton INTEGER PRIMARY KEY CHECK(singleton=1), body TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS monitoring_state (bill_id TEXT PRIMARY KEY, body TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS monitoring_feed (id TEXT PRIMARY KEY, created_at TEXT NOT NULL, body TEXT NOT NULL);
'''


def initialize(store):
    store.db.executescript(SCHEMA)
    with store.db:
        store.db.execute('INSERT OR IGNORE INTO monitoring_settings VALUES (1,?)',(json.dumps(DEFAULTS),))


def _settings(store):
    initialize(store)
    return json.loads(store.db.execute('SELECT body FROM monitoring_settings WHERE singleton=1').fetchone()[0])


def configure(store,args):
    initialize(store)
    allowed=set(DEFAULTS)
    if set(args)-allowed:
        raise ValueError('Unknown monitoring setting.')
    for key in ('enabled','notifications'):
        if key in args and type(args[key]) is not bool:
            raise ValueError(key+' must be boolean.')
    if 'interval_minutes' in args and (type(args['interval_minutes']) is not int or not 15<=args['interval_minutes']<=10080):
        raise ValueError('Refresh interval must be 15–10080 minutes.')
    try:
        store.db.execute('BEGIN IMMEDIATE')
        settings=json.loads(store.db.execute('SELECT body FROM monitoring_settings WHERE singleton=1').fetchone()[0])
        settings.update(args)
        store.db.execute('UPDATE monitoring_settings SET body=? WHERE singleton=1',(json.dumps(settings),))
        store.db.commit()
    except Exception:
        store.db.rollback(); raise
    return summary(store)


def _semantic(store,bid):
    bill=store.bill('official',bid)
    if not bill:
        return None
    fields=('title','topic','sponsor','introduced_at','congress','type')
    events=[{k:r.get(k) for k in ('effective_at','text','action_code','stage')} for r in store.records('event','official',bid)]
    resolutions=[{k:r.get(k) for k in ('effective_at','value','complete_coverage','definition')} for r in store.records('resolution','official',bid)]
    return dict(bill={k:bill.get(k) for k in fields},events=sorted(events,key=lambda x:json.dumps(x,sort_keys=True)),resolutions=sorted(resolutions,key=lambda x:json.dumps(x,sort_keys=True)))


def _load_state(store,bid):
    row=store.db.execute('SELECT body FROM monitoring_state WHERE bill_id=?',(bid,)).fetchone()
    return json.loads(row[0]) if row else {'bill_id':bid,'last_attempt':None,'last_success':None,'last_error':None}


def _event(store,bid,kind,message,changes=None,notify=False):
    event=dict(id=str(uuid.uuid4()),bill_id=bid,created_at=now(),kind=kind,message=message,changes=changes or [],notify=notify)
    with store.db:
        store.db.execute('INSERT INTO monitoring_feed VALUES (?,?,?)',(event['id'],event['created_at'],json.dumps(event)))
    return event


def _lock(path):
    with _GUARD:
        return _LOCKS.setdefault(str(path.resolve()),threading.Lock())


def refresh_watched(store, scheduled=False):
    """Explicit manual refresh or opted-in scheduler cycle; caller owns Store thread."""
    initialize(store)
    lock=_lock(store.path)
    if not lock.acquire(blocking=False):
        return {'status':'already_running','results':[]}
    try:
        settings=_settings(store)
        all_ids=sorted(store.watched('official'))
        cycle=dict(id=str(uuid.uuid4()),status='running',started_at=now(),results=[])
        store.checkpoint('monitoring:last_cycle',cycle)
        if len(all_ids)>100:
            cycle.update(status='failed',finished_at=now(),error='Monitoring supports at most 100 official watched bills; reduce your watchlist before refreshing.')
            store.checkpoint('monitoring:last_cycle',cycle)
            _event(store,None,'scheduler_error',cycle['error'],notify=settings['notifications'])
            return cycle
        for bid in all_ids:
            if scheduled and not _settings(store)['enabled']:
                cycle['stopped_early']=True
                break
            if bid not in store.watched('official'):
                continue
            settings=_settings(store)
            state=_load_state(store,bid)
            state['last_attempt']=now()
            try:
                parts=parse_bill_id(bid)
                before=_semantic(store,bid)
                baseline=state.get('semantic_components')
                if baseline is None and before is not None:
                    baseline={k:digest(v) for k,v in before.items()}
                ingest_bill(store,*parts,refresh=True)
                after=_semantic(store,bid)
                if after is None:
                    raise ValueError('Source did not provide expected bill.')
                changes=[]
                components={k:digest(v) for k,v in after.items()}
                if baseline is None:
                    changes=['initial_import']
                else:
                    changes=[k for k in ('bill','events','resolutions') if baseline[k]!=components[k]]
                state.update(last_success=now(),last_error=None,semantic_hash=digest(after),semantic_components=components)
                status='changed' if changes else 'unchanged'
                if changes:
                    _event(store,bid,'changed','Official evidence changed since the previous refresh.' if baseline else 'Initial official record imported.',changes,settings['notifications'])
                elif state.get('previous_failure'):
                    _event(store,bid,'recovered','Official source refresh recovered.')
                state['previous_failure']=False
                from . import prospective
                try:
                    capture=prospective.capture(store,'official',bid)
                    state['prospective_receipt_id']=capture['id']
                except Exception:
                    _event(store,bid,'capture_failed','Source refresh succeeded, but prospective capture failed. Retry from the bill workspace.')
                cycle['results'].append({'bill_id':bid,'status':status,'changes':changes})
            except Exception:
                state.update(last_error='Official source refresh failed. Existing evidence is preserved.',previous_failure=True)
                _event(store,bid,'failed',state['last_error'],notify=settings['notifications'])
                cycle['results'].append({'bill_id':bid,'status':'failed','error':state['last_error']})
            with store.db:
                store.db.execute('INSERT OR REPLACE INTO monitoring_state VALUES (?,?)',(bid,json.dumps(state)))
            store.checkpoint('monitoring:last_cycle',cycle)
        cycle.update(status='completed_with_errors' if any(r['status']=='failed' for r in cycle['results']) else 'completed',finished_at=now())
        store.checkpoint('monitoring:last_cycle',cycle)
        return cycle
    finally:
        lock.release()


def summary(store):
    settings=_settings(store)
    cycle=store.checkpoint('monitoring:last_cycle')
    current=datetime.now(timezone.utc)
    watched=[]
    for bid in sorted(store.watched('official')):
        state=_load_state(store,bid)
        last=state.get('last_success')
        state['stale']=not last or (current-datetime.fromisoformat(last.replace('Z','+00:00'))).total_seconds()>settings['interval_minutes']*60
        watched.append(state)
    next_due=None
    if settings['enabled']:
        started=(cycle or {}).get('started_at')
        next_due=(datetime.fromisoformat(started.replace('Z','+00:00'))+timedelta(minutes=settings['interval_minutes'])).isoformat().replace('+00:00','Z') if started else now()
    feed=[json.loads(r[0]) for r in store.db.execute('SELECT body FROM monitoring_feed ORDER BY rowid DESC LIMIT 100')]
    return dict(settings=settings,watched=watched,feed=feed,last_cycle=cycle,next_due=next_due,
                runtime_note='Scheduled refresh runs only while this local server is running. Notifications are in-app only. Demo bills are not refreshed.',
                scheduler_running=str(store.path.resolve()) in _SCHEDULERS)


def _is_due(settings, cycle):
    last=cycle.get('started_at')
    elapsed=(datetime.now(timezone.utc)-datetime.fromisoformat(last.replace('Z','+00:00'))).total_seconds() if last else float('inf')
    return settings['enabled'] and elapsed>=settings['interval_minutes']*60


def recover_monitoring(store):
    """Call once at startup before workers; never during live request handling."""
    initialize(store)
    cycle=store.checkpoint('monitoring:last_cycle')
    if cycle and cycle.get('status')=='running':
        cycle.update(status='interrupted',finished_at=now(),error='Local server stopped during this refresh. Completed bill refreshes were preserved; retry manually or wait for the next scheduled cycle.')
        store.checkpoint('monitoring:last_cycle',cycle)
        _event(store,None,'interrupted',cycle['error'])
    return cycle


def start_scheduler(db_path=None):
    """Start once at server startup; returns stop Event. No network unless enabled."""
    probe=Store(db_path)
    initialize(probe)
    path=probe.path.resolve()
    probe.close()
    key=str(path)
    with _GUARD:
        if key in _SCHEDULERS:
            return _SCHEDULERS[key]
        stop=threading.Event()
        _SCHEDULERS[key]=stop
    def work():
        store=Store(path)
        try:
            while not stop.is_set():
                try:
                    settings=_settings(store)
                    cycle=store.checkpoint('monitoring:last_cycle') or {}
                    if _is_due(settings,cycle):
                        refresh_watched(store,scheduled=True)
                except Exception:
                    message='Scheduled refresh could not finish. Check the watchlist and retry manually.'
                    store.checkpoint('monitoring:last_cycle',{'id':str(uuid.uuid4()),'status':'failed','started_at':now(),'finished_at':now(),'results':[],'error':message})
                    _event(store,None,'scheduler_error',message)
                stop.wait(30)
        finally:
            store.close()
            with _GUARD:
                _SCHEDULERS.pop(key,None)
    threading.Thread(target=work,daemon=True,name='bill-watch-scheduler').start()
    return stop
