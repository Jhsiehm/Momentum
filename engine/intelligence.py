"""Reusable, source-backed descriptive research; never a causal probability generator."""
import itertools
import json
import math
from datetime import datetime
from .store import now, timestamp, digest, congress_end
from . import prospective

METHOD='legislative-intelligence-v2'
FILTERS={'congresses','topics','query','bill_ids','type'}
COMMON={'dataset','cutoff','filters','limit'}
SCHEMA='''CREATE TABLE IF NOT EXISTS intelligence_reports(id TEXT PRIMARY KEY,created_at TEXT NOT NULL,kind TEXT NOT NULL,body TEXT NOT NULL);
CREATE TRIGGER IF NOT EXISTS intelligence_no_replace BEFORE INSERT ON intelligence_reports WHEN EXISTS (SELECT 1 FROM intelligence_reports WHERE id=NEW.id) BEGIN SELECT RAISE(ABORT,'Research reports are immutable'); END;
CREATE TRIGGER IF NOT EXISTS intelligence_no_update BEFORE UPDATE ON intelligence_reports BEGIN SELECT RAISE(ABORT,'Research reports are immutable'); END;
CREATE TRIGGER IF NOT EXISTS intelligence_no_delete BEFORE DELETE ON intelligence_reports BEGIN SELECT RAISE(ABORT,'Research reports are immutable'); END;'''


def capabilities(store):
    return dict(method=METHOD,supported=['dated bill filtering','descriptive outcome comparisons','overlapping groups','saved prospective estimate comparison','scenario assumption records'],
                unsupported=['validated customer probabilities','causal election scenarios','state legislation','stakeholder influence prediction'],
                filters=sorted(FILTERS),forecast_target='Own-bill enactment by Congress end',
                model_features=['stage','age','action count','inactivity','chamber','recent action count'],
                note='Imported coverage is not the legislative universe. Historical outcome frequencies are descriptive, not calibrated forecasts.')


def _filter(value):
    if not isinstance(value,dict) or set(value)-FILTERS:raise ValueError('Unsupported bill filters')
    result={}
    for key,items in value.items():
        if key in ('congresses','topics','bill_ids'):
            if not isinstance(items,list) or len(items)>100:raise ValueError('Filter lists accept up to 100 values')
            if key=='congresses':
                if any(type(v) is not int or not 1<=v<=200 for v in items):raise ValueError('Invalid Congress')
            elif any(not isinstance(v,str) or not 1<=len(v.strip())<=200 for v in items):raise ValueError('Invalid text filter')
            result[key]=sorted(set(items))
        elif key=='type':
            if items not in ('hr','s'):raise ValueError('Bill type must be hr or s')
            result[key]=items
        else:
            if not isinstance(items,str) or len(items)>200:raise ValueError('Query must contain at most 200 characters')
            result[key]=items.strip()
    return result


def _inputs(args,extra=()):
    if not isinstance(args,dict) or set(args)-COMMON-set(extra):raise ValueError('Unsupported research request fields')
    dataset=args.get('dataset','official')
    if dataset not in ('official','demo'):raise ValueError('Choose official or demo data')
    cutoff=timestamp(args.get('cutoff') or now())
    if cutoff>now():raise ValueError('Future evidence dates are unavailable')
    limit=args.get('limit',50)
    if type(limit) is not int or not 1<=limit<=100:raise ValueError('Limit must be 1–100')
    return dict(dataset=dataset,cutoff=cutoff,filters=_filter(args.get('filters',{})),limit=limit)


def _matches(b,f):
    for key,field in [('congresses','congress'),('topics','topic'),('bill_ids','bill_id')]:
        if f.get(key) and b.get(field) not in f[key]:return False
    if f.get('type') and b.get('type')!=f['type']:return False
    text=' '.join(str(b.get(k) or '') for k in ('bill_id','title','topic')).casefold()
    return all(t in text for t in f.get('query','').casefold().split())


def _population(store,inputs):
    ds,cutoff=inputs['dataset'],inputs['cutoff']
    bills=store.bills(ds,cutoff);events={};outcomes={}
    for e in store.records('event',ds,cutoff=cutoff):events.setdefault(e['bill_id'],[]).append(e)
    for r in store.records('resolution',ds,cutoff=cutoff):outcomes[r['bill_id']]=r
    rows=[]
    for b in bills:
        if not _matches(b,inputs['filters']):continue
        ev=events.get(b['bill_id'],[]);outcome=outcomes.get(b['bill_id'])
        # A missing resolution never implies failure, even after Congress ends.
        row={k:b.get(k) for k in ('bill_id','title','topic','congress','type','family_id','family_status','source_url','observed_at')}
        row.update(stage=max([0]+[e['stage'] for e in ev]),outcome=outcome['value'] if outcome else None,
                   evidence_ids=sorted([b['id']]+[e['id'] for e in ev]+([outcome['id']] if outcome else [])),
                   outcome_source_url=outcome.get('source_url') if outcome else None)
        rows.append(row)
    return rows,len(bills)


def _summary(rows):
    successes=sum(r['outcome']==1 for r in rows);failures=sum(r['outcome']==0 for r in rows);resolved=successes+failures
    return dict(total=len(rows),resolved=resolved,enacted=successes,not_enacted=failures,unknown=len(rows)-resolved,
                observed_rate=successes/resolved if resolved else None,unique_families=len({r['family_id'] for r in rows}),
                interpretation='Observed rate among explicitly resolved bills only; missing outcomes and related bills can bias comparisons. Not a forecast.')


def _save(store,kind,inputs,content):
    store.db.executescript(SCHEMA)
    payload=dict(kind=kind,method=METHOD,inputs=inputs,**content)
    payload['content_hash']=digest(payload);payload['id']=payload['content_hash'];payload['created_at']=now()
    # Serialize the existence check with insertion. A BEFORE INSERT guard also
    # rejects REPLACE, whose implicit deletion otherwise bypasses delete triggers.
    with store.db:
        store.db.execute('BEGIN IMMEDIATE')
        existing=store.db.execute('SELECT body FROM intelligence_reports WHERE id=?',(payload['id'],)).fetchone()
        if existing:return json.loads(existing[0])
        store.db.execute('INSERT INTO intelligence_reports VALUES (?,?,?,?)',(payload['id'],payload['created_at'],kind,json.dumps(payload,sort_keys=True)))
    return report(store,payload['id'])


def report(store,identity):
    store.db.executescript(SCHEMA)
    row=store.db.execute('SELECT body FROM intelligence_reports WHERE id=?',(identity,)).fetchone()
    if not row:raise ValueError('Research report not found')
    return json.loads(row[0])


def reports(store):
    store.db.executescript(SCHEMA)
    return [dict(id=r['id'],kind=r['kind'],created_at=r['created_at']) for r in store.db.execute('SELECT id,kind,created_at FROM intelligence_reports ORDER BY created_at DESC,rowid DESC LIMIT 100')]


def analyze(store,args):
    inputs=_inputs(args,{'groups'});groups=args.get('groups',[])
    if not isinstance(groups,list) or len(groups)>3:raise ValueError('Use up to three comparison groups')
    parsed=[]
    for g in groups:
        if not isinstance(g,dict) or set(g)-{'name','filters'} or not isinstance(g.get('name'),str) or not 1<=len(g['name'].strip())<=80:raise ValueError('Each group needs a name and filters')
        parsed.append(dict(name=g['name'].strip(),filters=_filter(g.get('filters',{}))))
    if len({g['name'] for g in parsed})!=len(parsed):raise ValueError('Group names must be unique')
    inputs['groups']=parsed;rows,imported=_population(store,inputs)
    comparisons=[dict(name=g['name'],filters=g['filters'],**_summary([r for r in rows if _matches(r,g['filters'])])) for g in parsed]
    overlaps=[]
    # Exact membership regions partition the population, including outside all groups.
    for n in range(0,len(parsed)+1):
        for combo in itertools.combinations(parsed,n):
            names={g['name'] for g in combo}
            members=[r for r in rows if all(_matches(r,g['filters']) == (g['name'] in names) for g in parsed)]
            overlaps.append(dict(groups=[g['name'] for g in combo],**_summary(members)))
    return _save(store,'analysis',inputs,dict(summary=_summary(rows),groups=comparisons,overlaps=overlaps,rows=rows[:inputs['limit']],
                 coverage=dict(imported_at_cutoff=imported,matched=len(rows),shown=min(len(rows),inputs['limit']),truncated=len(rows)>inputs['limit'],scope='Imported subset, not all legislation'),
                 evidence=dict(bill_ids=[r['bill_id'] for r in rows],record_ids=sorted({e for r in rows for e in r['evidence_ids']})),
                 frozen_rows=rows,note='Overlaps are disjoint exact-membership regions; an empty groups list means outside every named group. Current outcome comparisons do not test a causal hypothesis or validate predictive skill.'))


def rank(store,args):
    inputs=_inputs(args,{'max_age_days'});age=args.get('max_age_days',7)
    if type(age) is not int or not 1<=age<=30:raise ValueError('Forecast freshness must be 1–30 days')
    inputs['max_age_days']=age;rows,imported=_population(store,inputs);by_id={r['bill_id']:r for r in rows}
    prospective.initialize(store);latest={}
    # No 500-receipt page cap: account for every matching bill before reporting coverage.
    for item in store.db.execute('SELECT body FROM prospective_receipts WHERE dataset=? AND issued_at<=? ORDER BY issued_at DESC,rowid DESC',(inputs['dataset'],inputs['cutoff'])):
        r=json.loads(item[0]);latest.setdefault(r['bill_id'],r)
    excluded={};eligible=[]
    def exclude(reason):excluded[reason]=excluded.get(reason,0)+1
    cutoff_dt=datetime.fromisoformat(inputs['cutoff'].replace('Z','+00:00'))
    for bid,b in by_id.items():
        r=latest.get(bid)
        if b['outcome'] is not None or b['stage']==4 or inputs['cutoff']>=congress_end(b['congress']):exclude('resolved_or_congress_ended');continue
        if not r:exclude('no_saved_receipt');continue
        f=r.get('forecast') or {};p=f.get('probability')
        if r.get('status')!='captured' or not r.get('prospective_eligible') or r.get('synthetic') or f.get('status')!='available':exclude('not_eligible_prospective');continue
        if type(p) not in (int,float) or not math.isfinite(p) or not 0<=p<=1:exclude('invalid_probability');continue
        issued=datetime.fromisoformat(timestamp(r['issued_at']).replace('Z','+00:00'))
        if (cutoff_dt-issued).total_seconds()>age*86400:exclude('stale_receipt');continue
        if not f.get('target') or not f.get('deadline') or not f.get('model_version') or not f.get('feature_version'):exclude('missing_comparability_metadata');continue
        if f['deadline']!=congress_end(b['congress']) or f.get('cutoff',r['cutoff'])>inputs['cutoff']:exclude('incompatible_target_time');continue
        # New source records invalidate the claim that an old receipt represents current evidence.
        source_ids={s['id'] for s in r.get('source_records',[]) if s.get('bill_id')==bid}
        if not set(b['evidence_ids']).issubset(source_ids):exclude('changed_evidence');continue
        key=(f['target'],f['deadline'],f['model_version'],f['feature_version'],f.get('calibration_version'),r.get('cutoff'))
        eligible.append(dict(bill_id=bid,title=b['title'],probability=p,receipt_id=r['id'],issued_at=r['issued_at'],source_url=b['source_url'],comparison_key=list(key),release_eligible=False))
    buckets={}
    for r in eligible:buckets.setdefault(tuple(r['comparison_key']),[]).append(r)
    groups=[]
    for key,items in sorted(buckets.items(),key=lambda kv:str(kv[0])):
        items.sort(key=lambda r:(-r['probability'],r['bill_id']))
        groups.append(dict(comparison_key=list(key),total=len(items),rows=items[:inputs['limit']]))
    return _save(store,'ranking',inputs,dict(status='experimental_only' if eligible else 'unavailable',groups=groups,eligible=len(eligible),excluded=excluded,
                 coverage=dict(imported_at_cutoff=imported,matched=len(rows)),release_eligible=False,
                 evidence=dict(record_ids=sorted({e for r in rows for e in r['evidence_ids']}),receipt_ids=sorted(r['receipt_id'] for r in eligible)),
                 note='Only existing eligible, fresh receipts with identical target, deadline, model and evidence cutoff are compared within each group. Singleton comparison groups cannot provide a useful ranking. Estimates are unvalidated; no customer-ready probability ranking is established.'))


def scenario(store,args):
    inputs=_inputs(args,{'question','assumptions'})
    question=args.get('question');assumptions=args.get('assumptions',[])
    if not isinstance(question,str) or not 1<=len(question.strip())<=2000:raise ValueError('Provide a scenario question of at most 2000 characters')
    if not isinstance(assumptions,list) or not 1<=len(assumptions)<=20 or any(not isinstance(a,str) or not 1<=len(a.strip())<=500 for a in assumptions):raise ValueError('Provide 1–20 explicit assumptions, each at most 500 characters')
    inputs.update(question=question.strip(),assumptions=[a.strip() for a in assumptions]);rows,imported=_population(store,inputs)
    return _save(store,'scenario',inputs,dict(status='unsupported_for_numeric_forecast',probability=None,probability_shift=None,summary=_summary(rows),rows=rows[:inputs['limit']],
                 gaps=['No validated intervention or causal model','Political control and stakeholder influence are not model features','Assumptions are user-supplied, not verified events'],
                 coverage=dict(imported_at_cutoff=imported,matched=len(rows),shown=min(len(rows),inputs['limit'])),
                 evidence=dict(bill_ids=[r['bill_id'] for r in rows],record_ids=sorted({e for r in rows for e in r['evidence_ids']})),
                 note='Saved scenario notebook grounded in selected bill evidence. No causal effect or numerical forecast was computed; assumptions never become observed training outcomes.'))
