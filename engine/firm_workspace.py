"""Local organization work records; never model labels, influence claims or network calls."""
import json
import re
import uuid
from datetime import date, datetime, timedelta, timezone
from urllib.parse import urlsplit
from .store import now, digest
from . import monitoring

SCHEMA = '''
CREATE TABLE IF NOT EXISTS firm_profiles(id TEXT PRIMARY KEY, body TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS firm_work(profile_id TEXT, bill_id TEXT, body TEXT NOT NULL, PRIMARY KEY(profile_id,bill_id));
CREATE TABLE IF NOT EXISTS firm_positions(id TEXT PRIMARY KEY, profile_id TEXT, body TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS firm_briefs(id TEXT PRIMARY KEY, profile_id TEXT, body TEXT NOT NULL);
CREATE TRIGGER IF NOT EXISTS firm_briefs_no_replace BEFORE INSERT ON firm_briefs WHEN EXISTS(SELECT 1 FROM firm_briefs WHERE id=NEW.id) BEGIN SELECT RAISE(ABORT,'Briefs are immutable'); END;
CREATE TRIGGER IF NOT EXISTS firm_briefs_no_update BEFORE UPDATE ON firm_briefs BEGIN SELECT RAISE(ABORT,'Briefs are immutable'); END;
CREATE TRIGGER IF NOT EXISTS firm_briefs_no_delete BEFORE DELETE ON firm_briefs BEGIN SELECT RAISE(ABORT,'Briefs are immutable'); END;
'''
SCOPE = ('Federal bills imported on this computer only. Matching searches titles and policy topics; '
         'it does not assess impact or passage probability. Owner names are local labels, not accounts. '
         'Positions are user-recorded citations, not verified influence. Monitoring runs only while this local server runs.')


def initialize(store):
    store.db.executescript(SCHEMA)


def _text(value, label, maximum=3000, required=False):
    if not isinstance(value,str) or len(value.strip())>maximum or (required and not value.strip()):
        raise ValueError(f'{label} must be {"nonempty " if required else ""}text of at most {maximum} characters.')
    return value.strip()


def _fields(args, allowed):
    if not isinstance(args,dict) or set(args)-set(allowed.split()):
        raise ValueError('Unknown fields or invalid object.')


def _terms(value,label):
    if not isinstance(value,list) or len(value)>30:raise ValueError(label+' must be a list of at most 30 terms.')
    return list(dict.fromkeys(_text(x,label,120,True) for x in value))


def _profile(store,identity):
    initialize(store)
    identity=_text(identity,'Profile ID',100,True)
    row=store.db.execute('SELECT body FROM firm_profiles WHERE id=?',(identity,)).fetchone()
    if not row:raise ValueError('Organization profile not found.')
    return json.loads(row[0])


def profiles(store):
    initialize(store)
    return [json.loads(r[0]) for r in store.db.execute('SELECT body FROM firm_profiles ORDER BY id')]


def save_profile(store,args):
    _fields(args,'id name issues excluded_terms congresses description expected_version')
    initialize(store)
    identity=_text(args.get('id') or str(uuid.uuid4()),'Profile ID',100,True)
    name=_text(args.get('name',''),'Name',120,True)
    issues=_terms(args.get('issues',[]),'Issues')
    excluded=_terms(args.get('excluded_terms',[]),'Excluded terms')
    congresses=args.get('congresses',[])
    if not isinstance(congresses,list) or len(congresses)>30 or any(type(c)is not int or not 93<=c<=200 for c in congresses):
        raise ValueError('Congresses must be a list of up to 30 integers from 93 to 200.')
    description=_text(args.get('description',''),'Client context')
    try:
        store.db.execute('BEGIN IMMEDIATE')
        row=store.db.execute('SELECT body FROM firm_profiles WHERE id=?',(identity,)).fetchone()
        old=json.loads(row[0]) if row else None
        if args.get('id') and not old:raise ValueError('Organization profile not found.')
        if old and (type(args.get('expected_version')) is not int or args['expected_version']!=old['version']):raise ValueError('Profile changed. Reload and retry with its current expected_version.')
        result=dict(id=identity,name=name,issues=issues,excluded_terms=excluded,congresses=sorted(set(congresses)),description=description,version=old['version']+1 if old else 1,created_at=old['created_at'] if old else now(),updated_at=now())
        store.db.execute('INSERT OR REPLACE INTO firm_profiles VALUES (?,?)',(identity,json.dumps(result)))
        store.db.commit()
    except Exception:
        store.db.rollback();raise
    return result


def _bill(store,identity):
    identity=_text(identity,'Bill ID',100,True)
    bill=store.bill('official',identity)
    if not bill:raise ValueError('Import the official bill before adding organization work or positions.')
    return bill


def _choice(value,choices,label):
    if value not in choices:raise ValueError('Invalid '+label+'.')
    return value


def _date(value,label,required=False):
    value=_text(value,label,10,required)
    if value:
        try:
            if not re.fullmatch(r'\d{4}-\d{2}-\d{2}',value):raise ValueError()
            date.fromisoformat(value)
        except ValueError:raise ValueError(label+' must be a real date in YYYY-MM-DD format.')
    return value


def save_work_item(store,args):
    _fields(args,'profile_id bill_id owner status priority impact impact_reason next_action due_date notes expected_version')
    profile=_profile(store,args.get('profile_id',''));bill=_bill(store,args.get('bill_id',''))
    values=dict(owner=_text(args.get('owner',''),'Owner',120),status=_choice(args.get('status','tracked'),('tracked','reviewing','closed'),'work status'),priority=_choice(args.get('priority','normal'),('low','normal','high','urgent'),'priority'),impact=_choice(args.get('impact','unknown'),('unknown','low','medium','high'),'impact'),impact_reason=_text(args.get('impact_reason',''),'Impact reason'),next_action=_text(args.get('next_action',''),'Next action',1000),due_date=_date(args.get('due_date',''),'Due date'),notes=_text(args.get('notes',''),'Notes',10000))
    try:
        store.db.execute('BEGIN IMMEDIATE')
        row=store.db.execute('SELECT body FROM firm_work WHERE profile_id=? AND bill_id=?',(profile['id'],bill['bill_id'])).fetchone()
        old=json.loads(row[0]) if row else None
        if old and (type(args.get('expected_version'))is not int or args['expected_version']!=old['version']):raise ValueError('Work item changed. Reload and retry with its current expected_version.')
        result=dict(profile_id=profile['id'],bill_id=bill['bill_id'],**values,version=old['version']+1 if old else 1,created_at=old['created_at'] if old else now(),updated_at=now(),assessment='User-assessed priority and impact; not a passage estimate.')
        store.db.execute('INSERT OR REPLACE INTO firm_work VALUES (?,?,?)',(profile['id'],bill['bill_id'],json.dumps(result)))
        store.db.commit()
    except Exception:
        store.db.rollback();raise
    return result


def _url(value):
    value=_text(value,'Source URL',2000,True)
    try:
        u=urlsplit(value)
        if u.scheme not in ('http','https') or not u.hostname or u.username or u.password or any(ord(c)<=32 for c in value):raise ValueError()
        u.port
    except ValueError:raise ValueError('Use a valid HTTP(S) source URL without credentials.')
    return value


def add_position(store,args):
    _fields(args,'profile_id bill_id organization position statement source_url published_at')
    profile=_profile(store,args.get('profile_id',''));bill=_bill(store,args.get('bill_id',''))
    result=dict(id=str(uuid.uuid4()),profile_id=profile['id'],bill_id=bill['bill_id'],organization=_text(args.get('organization',''),'Stakeholder organization',160,True),position=_choice(args.get('position'),('support','oppose','mixed','unclear'),'position'),statement=_text(args.get('statement',''),'Quoted statement',5000,True),source_url=_url(args.get('source_url','')),published_at=_date(args.get('published_at',''),'Source publication date',True),recorded_at=now(),verification_status='user_recorded_unverified',note='User-recorded quotation and citation; not independently verified and not evidence of causal influence.')
    if result['published_at']>datetime.now(timezone.utc).date().isoformat():raise ValueError('Source publication date cannot be in the future.')
    with store.db:store.db.execute('INSERT INTO firm_positions VALUES (?,?,?)',(result['id'],profile['id'],json.dumps(result)))
    return result


def dashboard(store,profile_id):
    profile=_profile(store,profile_id);profile_id=profile['id'];watched=set(store.watched('official'));matches=[]
    for b in store.bills('official'):
        if profile['congresses'] and b['congress'] not in profile['congresses']:continue
        fields={k:str(b.get(k)or'') for k in ('title','topic')}
        if any(t.casefold() in ' '.join(fields.values()).casefold() for t in profile['excluded_terms']):continue
        reasons=[dict(field=k,term=t) for t in profile['issues'] for k,v in fields.items() if t.casefold() in v.casefold()]
        if reasons:matches.append(dict({k:b.get(k) for k in ('bill_id','title','topic','congress','source_url','observed_at')},matching_reasons=reasons,following=b['bill_id'] in watched))
    matches.sort(key=lambda b:b['bill_id'])
    work=[json.loads(r[0]) for r in store.db.execute('SELECT body FROM firm_work WHERE profile_id=? ORDER BY bill_id',(profile_id,))]
    positions=[json.loads(r[0]) for r in store.db.execute('SELECT body FROM firm_positions WHERE profile_id=? ORDER BY rowid DESC',(profile_id,))]
    relevant={b['bill_id'] for b in matches}|{b['bill_id'] for b in work}
    monitor=monitoring.summary(store)
    changes=[e for e in monitor['feed'] if e['kind']=='changed' and e.get('bill_id') in relevant and e.get('bill_id') in watched and e.get('changes')!=['initial_import']]
    briefs=[json.loads(r[0]) for r in store.db.execute('SELECT body FROM firm_briefs WHERE profile_id=? ORDER BY rowid DESC LIMIT 20',(profile_id,))]
    return dict(profile=profile,matches=matches[:100],work_items=work[:100],positions=positions[:100],changes=changes,briefs=[{k:b[k] for k in ('id','profile_id','created_at','hash')} for b in briefs],counts=dict(matches=len(matches),work_items=len(work),positions=len(positions)),truncated=dict(matches=len(matches)>100,work_items=len(work)>100,positions=len(positions)>100),monitoring=dict(settings=monitor['settings'],last_cycle=monitor['last_cycle'],scheduler_running=monitor['scheduler_running'],watched=monitor['watched']),generated_at=now(),scope=SCOPE+' Lists show at most 100 matches, work items and positions, 20 briefs and relevant events from the latest 100 global monitoring receipts.')


def _md(value):
    # Render user data as inert Markdown text, not HTML, images, headings or links.
    text=str(value).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    return re.sub(r'([\\`*_{}\[\]()#+.!|~-])',r'\\\1',text).replace('\n',' ').replace('\r',' ')


def _markdown(brief):
    s=brief['snapshot'];lines=['# '+_md(s['profile']['name'])+' — legislative briefing','', 'Generated: '+brief['created_at'],'',s['scope'],'', 'Window starts: '+s['window_start'],'','## Matching bills','']
    for b in s['matches']:lines += ['- '+_md(b['bill_id']+' — '+b['title']), '  Source: '+_md(b.get('source_url')or'Unavailable'), '  Reasons: '+_md('; '.join(r['term']+' in '+r['field'] for r in b['matching_reasons']))]
    lines+=['','## Recorded changes','']
    for e in s['changes']:lines+=['- '+_md(e['bill_id']+' — '+e['message']+' ('+e['created_at']+')')]
    if not s['changes']:lines+=['No relevant change receipts in this window. This does not establish that official records are current.']
    lines+=['','## Organization work','']
    for w in s['work_items']:lines+=['- '+_md(f"{w['bill_id']} · {w['status']} · owner: {w['owner'] or 'unassigned'} · priority: {w['priority']} · user-assessed impact: {w['impact']}"),'  Next action: '+_md(w['next_action'] or 'None recorded')+'; due: '+_md(w['due_date'] or 'None recorded'),'  Notes: '+_md(w['notes'])]
    lines+=['','## Stakeholder citations (user-recorded, unverified)','']
    for p in s['positions']:lines+=['- '+_md(p['bill_id']+' — '+p['organization']+' — '+p['position']), '  Statement: '+_md(p['statement']), '  Source: '+_md(p['source_url'])+'; published: '+p['published_at']]
    lines+=['','## Official source references','']
    for source in s['sources']:lines+=['- '+_md(source['bill_id'])+': '+_md(source.get('source_url')or'Unavailable')+'; observed: '+_md(source.get('observed_at')or'Unknown')]
    lines+=['','No probability or causal influence is inferred by this briefing.','', 'Snapshot hash: '+brief['hash']]
    return '\n'.join(lines)+'\n'


def create_brief(store,args):
    _fields(args,'profile_id window_days')
    days=args.get('window_days',7)
    if type(days)is not int or not 1<=days<=365:raise ValueError('Brief window must be 1–365 days.')
    snapshot=dashboard(store,args.get('profile_id',''));snapshot.pop('briefs')
    start=(datetime.now(timezone.utc)-timedelta(days=days)).isoformat().replace('+00:00','Z')
    snapshot['window_start']=start;snapshot['window_days']=days
    snapshot['changes']=[e for e in snapshot['changes'] if e['created_at']>=start]
    ids=sorted({b['bill_id'] for b in snapshot['matches']+snapshot['work_items']+snapshot['positions']+snapshot['changes']})
    snapshot['sources']=[{k:b.get(k) for k in ('bill_id','title','source_url','observed_at','raw_hash')} for bid in ids if (b:=store.bill('official',bid))]
    snapshot['source_note']='Official source references identify retained records; cited stakeholder pages are user-recorded and have not been fetched.'
    result=dict(id=str(uuid.uuid4()),profile_id=snapshot['profile']['id'],created_at=now(),snapshot=snapshot,hash=digest(snapshot))
    result['markdown']=_markdown(result)
    with store.db:store.db.execute('INSERT INTO firm_briefs VALUES (?,?,?)',(result['id'],result['profile_id'],json.dumps(result)))
    return result


def get_brief(store,identity):
    initialize(store);identity=_text(identity,'Brief ID',100,True)
    row=store.db.execute('SELECT body FROM firm_briefs WHERE id=?',(identity,)).fetchone()
    if not row:raise ValueError('Briefing not found.')
    return json.loads(row[0])


def export_brief(store,identity):
    return get_brief(store,identity)['markdown']
