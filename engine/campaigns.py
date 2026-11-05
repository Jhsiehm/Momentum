"""Persistent research campaigns: orchestration policy and honest development monitoring.

Campaign controls never silently change the global automatic research settings.
Sample membership is frozen at creation so historical runs cannot be reassigned by edits.
"""
import json
import uuid
from collections import Counter
from .store import now, digest
from . import sampling, sessions, autoresearch, learning

SCHEMA = '''
CREATE TABLE IF NOT EXISTS research_campaigns(id TEXT PRIMARY KEY, body TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS campaign_events(id TEXT PRIMARY KEY, campaign_id TEXT NOT NULL, body TEXT NOT NULL);
CREATE TRIGGER IF NOT EXISTS campaign_events_no_update BEFORE UPDATE ON campaign_events BEGIN SELECT RAISE(ABORT,'Campaign history is immutable'); END;
CREATE TRIGGER IF NOT EXISTS campaign_events_no_delete BEFORE DELETE ON campaign_events BEGIN SELECT RAISE(ABORT,'Campaign history is immutable'); END;
'''
FIELDS={'name','goal','sample_ids','state','daily_run_limit','max_runs_per_cycle','notification_preference'}
STATES={'draft','active','paused','archived'}


def initialize(store):
    store.db.executescript(SCHEMA)


def _row(store, identity):
    initialize(store)
    row=store.db.execute('SELECT body FROM research_campaigns WHERE id=?',(identity,)).fetchone()
    if not row: raise ValueError('Research campaign not found')
    return json.loads(row[0])


def _validate(store,args,creating=False):
    if not isinstance(args,dict) or set(args)-FIELDS: raise ValueError('Unsupported campaign fields')
    for key,minimum,maximum in [('name',3,120),('goal',10,3000)]:
        if key in args and (not isinstance(args[key],str) or not minimum<=len(args[key].strip())<=maximum):
            raise ValueError(f'{key} must contain {minimum}–{maximum} characters')
    if 'state' in args and (not isinstance(args['state'],str) or args['state'] not in STATES): raise ValueError('Unknown campaign state')
    for key,maximum in [('daily_run_limit',100),('max_runs_per_cycle',10)]:
        if key in args and (type(args[key]) is not int or not 1<=args[key]<=maximum): raise ValueError(f'{key} must be 1–{maximum}')
    if 'notification_preference' in args and (not isinstance(args['notification_preference'],str) or args['notification_preference'] not in ('attention','all_results','quiet')):
        raise ValueError('Choose attention, all_results or quiet notifications')
    if 'sample_ids' in args:
        ids=args['sample_ids']
        if not isinstance(ids,list) or not 1<=len(ids)<=20 or any(not isinstance(v,str) for v in ids) or len(set(ids))!=len(ids):
            raise ValueError('Choose 1–20 distinct audited samples')
        for ident in ids: sampling.get_sample(store,ident)
    if creating and not {'name','goal','sample_ids'}<=set(args): raise ValueError('Provide a campaign name, goal and selected samples')


def _save(store,campaign,event):
    with store.db:
        store.db.execute('INSERT INTO research_campaigns VALUES (?,?) ON CONFLICT(id) DO UPDATE SET body=excluded.body',(campaign['id'],json.dumps(campaign)))
        receipt=dict(id=str(uuid.uuid4()),campaign_id=campaign['id'],created_at=now(),**event)
        store.db.execute('INSERT INTO campaign_events VALUES (?,?,?)',(receipt['id'],campaign['id'],json.dumps(receipt)))


def create(store,args):
    initialize(store);_validate(store,args,True)
    campaign=dict(id=str(uuid.uuid4()),name=args['name'].strip(),goal=args['goal'].strip(),sample_ids=list(args['sample_ids']),
                  state=args.get('state','draft'),daily_run_limit=args.get('daily_run_limit',12),max_runs_per_cycle=args.get('max_runs_per_cycle',3),
                  notification_preference=args.get('notification_preference','attention'),created_at=now(),updated_at=now(),version=1)
    _save(store,campaign,dict(kind='created',changes={k:campaign[k] for k in FIELDS}))
    return detail(store,campaign['id'])


def update(store,identity,args):
    _validate(store,args)
    campaign=_row(store,identity)
    if 'sample_ids' in args and args['sample_ids']!=campaign['sample_ids']: raise ValueError('Campaign membership is frozen; create a new campaign to change selected samples')
    changes={k:dict(before=campaign[k],after=v.strip() if k in ('name','goal') else v) for k,v in args.items() if campaign[k]!=v}
    if changes:
        campaign.update({k:v['after'] for k,v in changes.items()});campaign.update(updated_at=now(),version=campaign['version']+1)
        _save(store,campaign,dict(kind='updated',changes=changes))
    return detail(store,identity)


def _all(store):
    initialize(store)
    return [json.loads(r[0]) for r in store.db.execute('SELECT body FROM research_campaigns ORDER BY rowid DESC')]


def active_sample_ids(store):
    return sorted({s for c in _all(store) if c['state']=='active' for s in c['sample_ids']})


def scheduling_policy(store,sample_id):
    """Conservative caps across active memberships; no membership means legacy policy.

    Caller must recheck before each run. Jobs count against every matching campaign,
    including manual/global runs of the same sample, to prevent overlapping budget bypass.
    """
    linked=[c for c in _all(store) if sample_id in c['sample_ids']]
    active=[c for c in linked if c['state']=='active']
    autoresearch.initialize(store);jobs=autoresearch._jobs(store)
    policies=[]
    for c in active:
        used=sum(j['sample_id'] in c['sample_ids'] and j.get('budget_day',(j.get('started_at') or '')[:10])==now()[:10] for j in jobs)
        policies.append(dict(campaign_id=c['id'],sample_ids=c['sample_ids'],daily_remaining=max(0,c['daily_run_limit']-used),max_runs_per_cycle=c['max_runs_per_cycle']))
    return dict(managed=bool(linked),allowed=not linked or bool(active) and all(p['daily_remaining']>0 for p in policies),campaigns=policies)


def _session_brief(proposal,result,adaptive=None):
    config=proposal['config']; result=result or {}; adaptive=adaptive or {}
    # Evidence, membership and checkpoint must match before displaying a comparison.
    basis=dict(dataset=config['dataset'],age_days=config['age_days'],target=config.get('target'),
               bill_ids=sorted(proposal['collection']['bill_ids']),evidence_hash=proposal['evidence_hash'],feature_version=proposal.get('feature_version'),
               scored_bill_ids=sorted(r['bill_id'] for r in result.get('results',[]) if r.get('status')=='available' and r.get('outcome') is not None))
    return dict(id=proposal['id'],title=proposal['title'],created_at=proposal['created_at'],status=result.get('status',proposal['status']),
                sample_id=proposal['sample_context']['sample_id'],config=config,parent_id=proposal.get('parent_id'),change=proposal.get('change'),
                comparison_group=digest(basis),comparison_basis=basis,metrics=result.get('metrics'),baseline=result.get('baseline'),
                brier_difference=result.get('brier_difference'),scored=result.get('scored',0),families=result.get('families',0),
                preflight={k:proposal['preflight'].get(k) for k in ('target_count','eligible_count','scoreable_count','blockers','next_step')},
                adaptive_metrics=adaptive.get('metrics'),fixed_paired_metrics=adaptive.get('fixed_metrics'),learning_status=adaptive.get('status'),
                feature_policy_counts=dict(Counter(c.get('selected_feature_policy','structured') for c in adaptive.get('cases',[]) if c.get('probability') is not None)),
                learning_version=adaptive.get('version'),learning_feature_version=adaptive.get('selection_policy',{}).get('feature_version'),
                implementation_hashes=proposal.get('implementation_hashes'),release_eligible=False)


def detail(store,identity):
    campaign=_row(store,identity);selected=set(campaign['sample_ids'])
    samples=[sampling.get_sample(store,s) for s in campaign['sample_ids']]
    autoresearch.initialize(store);sessions.initialize(store);store.db.executescript(learning.SCHEMA)
    jobs=[j for j in autoresearch._jobs(store) if j['sample_id'] in selected]
    job_sessions={j.get('session_id') for j in jobs}
    automatic_titles={'Automatic development '+j['id'] for j in jobs}
    runs=[]
    for row in store.db.execute('SELECT s.body,r.body,l.body FROM research_sessions s LEFT JOIN session_results r ON r.session_id=s.id LEFT JOIN learning_records l ON l.session_id=s.id ORDER BY s.created_at DESC,s.rowid DESC'):
        p=json.loads(row[0])
        if p.get('sample_context',{}).get('sample_id') not in selected:continue
        if p['title'] in automatic_titles and not row[1] and p['id'] not in job_sessions:continue
        runs.append(_session_brief(p,json.loads(row[1]) if row[1] else None,json.loads(row[2]) if row[2] else None))
    groups={}
    for run in runs:
        if run['status']!='completed' or run['scored']<=0 or not run['metrics']:continue
        group=groups.setdefault(run['comparison_group'],dict(id=run['comparison_group'],basis=run['comparison_basis'],runs=[]))
        group['runs'].append({k:run[k] for k in ('id','created_at','status','metrics','baseline','brier_difference','scored','families','adaptive_metrics','fixed_paired_metrics','learning_status','feature_policy_counts','learning_version','learning_feature_version')})
    latest={}
    for run in runs:latest.setdefault(run['sample_id'],run)
    blockers=list(dict.fromkeys(b for sample in samples for b in (latest[sample['id']]['preflight']['blockers'] or [] if sample['id'] in latest else sample['readiness']['blockers'])))
    sample_briefs=[dict({k:s.get(k) for k in ('id','name','size','audit_size','readiness','hash')},imported_count=s['readiness']['imported'],audit_passed=s['readiness']['audit_passed']) for s in samples]
    settings=autoresearch._settings(store)
    effective=set(settings['sample_ids'])|set(active_sample_ids(store))
    uncovered=sorted(selected-effective)
    if campaign['state']!='active':next_action='Activate this campaign to permit its samples to run in background research.'
    elif not settings['enabled']:next_action='Enable background research; campaign activation does not change the global runner.'
    elif uncovered:next_action='Add the campaign samples to the background research selection.'
    elif blockers:next_action='Resolve the evidence and audit blockers shown for the frozen proposals, then run a fresh cycle.'
    else:next_action='The campaign is ready for the next background research cycle; unchanged evidence is skipped.'
    events=[json.loads(r[0]) for r in store.db.execute('SELECT body FROM campaign_events WHERE campaign_id=? ORDER BY rowid DESC',(identity,))]
    notification_states={'blocked','failed'} if campaign['notification_preference']=='attention' else {'blocked','failed','completed'} if campaign['notification_preference']=='all_results' else set()
    notifications=[dict(id=j['id'],campaign_id=identity,job_id=j['id'],sample_id=j['sample_id'],session_id=j.get('session_id'),status=j['status'],message=j.get('message',''),created_at=j.get('finished_at') or j.get('started_at') or j['created_at'],age_days=j['age_days']) for j in reversed(jobs) if j['status'] in notification_states]
    return dict(campaign,notifications=notifications,samples=sample_briefs,jobs=list(reversed(jobs)),runs=runs,comparison_groups=list(groups.values()),events=events,
                progress=dict(job_counts=dict(Counter(j['status'] for j in jobs)),session_counts=dict(Counter(r['status'] for r in runs)),
                              completed_runs=sum(r['status']=='completed' for r in runs),distinct_evaluation_contexts=len(groups)),
                blockers=blockers,next_action=next_action,runner=dict(enabled=settings['enabled'],unselected_sample_ids=uncovered),
                runtime_note='Campaigns share the local runner and global budgets. Notifications are shown inside the app; no external delivery is configured.',
                interpretation='Overlapping bills and repeated experiments are not independent validation. Comparison groups align frozen evidence, checkpoints and scored membership. No automatic production promotion.',release_eligible=False)


def list_campaigns(store):
    return [detail(store,c['id']) for c in _all(store)]
