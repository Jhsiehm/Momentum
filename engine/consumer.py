"""User priorities and a read-only unified activity ledger."""
import json
import re
from .store import now
from . import monitoring, sampling, collections, sessions, autoresearch


def preferences(store,args=None):
    current=store.checkpoint('consumer:priorities') or {'issues':[],'organizations':[]}
    if args is not None:
        if not isinstance(args,dict) or set(args)-{'issues','organizations'}:raise ValueError('Unknown priority fields.')
        for key,values in args.items():
            if not isinstance(values,list) or len(values)>30 or any(not isinstance(v,str) or not 1<=len(v.strip())<=120 for v in values):raise ValueError('Use up to 30 names or search terms, each 1–120 characters.')
            current[key]=list(dict.fromkeys(v.strip() for v in values))
        store.checkpoint('consumer:priorities',current)
    return current


def priorities(store,args=None):
    prefs=preferences(store,args); watches=set(store.watched('official'))
    bills=store.bills('official'); watched=[]; matches=[]
    for b in bills:
        terms=[term for term in prefs['issues'] if term.casefold() in (b['title']+' '+str(b.get('topic',''))).casefold()]
        item={k:b.get(k) for k in ('bill_id','title','topic','congress','source_url','observed_at')}
        item['matched_issues']=terms
        if b['bill_id'] in watches:watched.append(item)
        if terms:matches.append(item)
    monitor=monitoring.summary(store)
    feed=[event for event in monitor['feed'] if event['kind']=='changed' and event.get('bill_id') in watches]
    failures=sum(bool(item.get('last_error')) for item in monitor['watched'])
    health=dict(enabled=monitor['settings']['enabled'],scheduler_running=monitor['scheduler_running'],failed_bills=failures,last_checked=(monitor.get('last_cycle') or {}).get('finished_at'),stale_bills=sum(bool(item.get('stale')) for item in monitor['watched']))
    return dict(preferences=prefs,watched=watched,matches=matches[:100],match_count=len(matches),changes=feed[:10],monitoring=health,
                coverage_note='Issue matches search imported titles and policy topics only. Organization names are saved context, not verified relationships or assessments of impact.')


def activity(store):
    items=[]
    def add(ident,kind,title,status,stamp,detail,view,options):
        items.append(dict(id=ident,type=kind,title=title,status=status,created_at=stamp,detail=detail,view=view,options=options))
    for j in sampling.list_bulk_jobs(store):
        add(j['id'],'import','Bulk bill import',j['status'],j.get('updated_at') or j.get('created_at'),f"{j.get('completed',0)} of {j.get('total',0)} processed; {j.get('failed',0)} failures.",'data',{})
    for j in collections.list_import_jobs(store):
        add(j['id'],'import','Collection import',j['status'],j.get('created_at'),f"{j.get('completed',0)} of {j.get('total',0)} processed.",'collections',{})
    auto=autoresearch.summary(store)
    for j in auto['jobs']:
        add(j['id'],'experiment',f"Background experiment · {j['age_days']} days",j['status'],j.get('finished_at') or j.get('created_at'),j.get('message',''),'session' if j.get('session_id') else 'autoresearch',{'id':j['session_id']} if j.get('session_id') else {})
    for r in sessions.list_sessions(store):
        if r['title'].startswith('Automatic development '):continue
        add(r['id'],'session',r['title'],r['status'],(r.get('result') or {}).get('completed_at') or r['created_at'], 'Development result; repeated runs are not independent evidence.' if r.get('result') else '; '.join(r['preflight']['blockers']), 'session',{'id':r['id']})
    from . import prospective, coverage_pipeline
    for r in prospective.list_receipts(store):
        add(r['id'],'forecast','Forecast snapshot · '+r['bill_id'],r['status'],r['issued_at'],r.get('reason') or 'Forecast and source evidence saved at issuance.','bill',{'bill_id':r['bill_id'],'dataset':r['dataset']})
    for p in coverage_pipeline.list_plans(store):
        add(p['id'],'coverage',p['name'],p['status'],p.get('updated_at') or p['created_at'],f"{p['progress']['imported']} of {p['total']} records imported in resumable batches.",'coverage',{})
    for e in monitoring.summary(store)['feed']:
        add(e['id'],'source',e.get('bill_id') or 'Source monitoring',e['kind'],e['created_at'],e['message'],'bill' if e.get('bill_id') else 'watching',{'bill_id':e['bill_id'],'dataset':'official'} if e.get('bill_id') else {})
    for sample in sampling.list_samples(store):
        audits=sample.get('audits',{})
        for bid,a in audits.items():
            add(a.get('id',sample['id']+bid),'audit','Audit · '+bid,a.get('status','pending'),a.get('created_at'),a.get('notes',''),'sample',{'id':sample['id']})
    items.sort(key=lambda x:x['created_at'] or '',reverse=True)
    return dict(items=items[:200],worker={'enabled':auto['settings']['enabled'],'next_due':auto['next_due']},generated_at=now(),note='Latest 200 activity records; statuses are actual saved receipts, not simulated progress.')


def browse(store,args=None):
    """Bounded discovery of local official records, without running forecasts."""
    args=args or {}
    query=str(args.get('q','')).strip()
    if len(query)>200:raise ValueError('Use a search of 200 characters or fewer.')
    try:
        page=max(1,int(args.get('page',1)))
        limit=max(1,min(50,int(args.get('limit',20))))
        congress=int(args['congress']) if args.get('congress') else None
    except (TypeError,ValueError):raise ValueError('Page, limit and Congress must be numbers.')
    following=str(args.get('following','')).lower() in ('1','true')
    all_bills=store.bills('official'); watched=set(store.watched('official'))
    normalize=lambda value:re.sub(r'[^a-z0-9]+','',str(value).casefold())
    needle=normalize(query)
    tokens=query.casefold().split()
    selected=[]
    for b in all_bills:
        if congress is not None and b.get('congress')!=congress:continue
        if following and b['bill_id'] not in watched:continue
        text=(b.get('title','')+' '+str(b.get('topic') or '')+' '+b['bill_id']).casefold()
        short_id=b['bill_id'].split('-',1)[-1]
        if query and not (all(t in text for t in tokens) or (needle and needle in (normalize(b['bill_id']),normalize(short_id)))):continue
        selected.append(b)
    total=len(selected); pages=max(1,(total+limit-1)//limit);page=min(page,pages)
    rows=[]
    for b in selected[(page-1)*limit:page*limit]:
        row={key:b.get(key) for key in ('bill_id','title','topic','congress','introduced_at','observed_at','source_url')}
        row['following']=b['bill_id'] in watched
        rows.append(row)
    return dict(bills=rows,total=total,page=page,pages=pages,limit=limit,query=query,imported=len(all_bills),congresses=sorted({b['congress'] for b in all_bills},reverse=True),scope='Search covers imported official titles, bill numbers and policy topics. It does not search all of Congress.')
