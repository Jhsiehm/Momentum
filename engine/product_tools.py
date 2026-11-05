"""Allowlisted product workflow tools shared by chat and the local API."""
from . import collections, sessions, monitoring, sampling, sample_research, autoresearch, campaigns, coverage_pipeline, consumer


def tool(name, description, properties, required):
    return {'type':'function','function':{'name':name,'description':description,'parameters':{'type':'object','properties':properties,'required':required,'additionalProperties':False}}}

S={'type':'string'}
D={'type':'string','enum':['demo','official']}
TOOLS=[
    tool('inspect_priorities','Read saved issue interests, watched bills and source changes. Organization names are context, not verified relationships.',{},[]),
    tool('save_priorities','Save issue search terms and organization context when requested.',{'issues':{'type':'array','items':S},'organizations':{'type':'array','items':S}},[]),
    tool('inspect_activity','Read actual import, audit, monitoring and research receipts.',{},[]),
    tool('inspect_data_coverage','Read imported, audited and historical metadata coverage. Unknown training eligibility is not zero.',{},[]),
    tool('plan_coverage_import','Create a resumable complete-Congress import plan from a saved inventory when requested. Starts local background batches; does not establish historical eligibility.',{'inventory_id':S,'congresses':{'type':'array','items':{'type':'integer'}}},['inventory_id','congresses']),
    tool('list_research_campaigns','List research campaigns, goals and progress.',{},[]),
    tool('inspect_research_campaign','Inspect a campaign, blockers and comparable result groups.',{'id':S},['id']),
    tool('create_research_campaign','Create a draft campaign over exact saved sample membership. Does not enable the global worker.',{'name':S,'goal':S,'sample_ids':{'type':'array','items':S}},['name','goal','sample_ids']),
    tool('configure_research_campaign','Activate or pause a campaign and adjust its budgets when requested. Global worker limits remain in force.',{'id':S,'state':{'type':'string','enum':['active','paused','draft']},'daily_run_limit':{'type':'integer'},'max_runs_per_cycle':{'type':'integer'}},['id']),
    tool('inspect_background_research','Inspect the bounded local research schedule, real jobs and evidence blockers. Repeated evidence is not new learning.',{},[]),
    tool('configure_background_research','Configure or pause unattended local development experiments when requested. No paid model calls; only selected audited samples. The local server must remain running. Evidence gates cannot be bypassed.',{'enabled':{'type':'boolean'},'interval_minutes':{'type':'integer'},'max_runs_per_cycle':{'type':'integer'},'daily_run_limit':{'type':'integer'},'sample_ids':{'type':'array','items':S}},[]),
    tool('list_audited_samples','List frozen random samples and their evidence readiness. Human audit pending is not a passed audit.',{},[]),
    tool('discover_bill_inventory','Fetch complete official GovInfo bill directory listings for selected completed Congresses. This discovers IDs, not historically eligible evidence.',{'congresses':{'type':'array','items':{'type':'integer'}}},['congresses']),
    tool('create_audited_sample','Freeze a seeded stratified sample from a discovered inventory, with a separate audit subset. Does not import, approve evidence or run an experiment.',{'inventory_id':S,'name':S,'size':{'type':'integer'},'seed':S,'audit_size':{'type':'integer'}},['inventory_id','name','size','seed']),
    tool('inspect_audited_sample','Inspect the saved sample, exact split and evidence readiness.',{'id':S},['id']),
    tool('import_audited_sample','Start a resumable official record import for a frozen sample when requested. Inspect the job before claiming completion.',{'sample_id':S},['sample_id']),
    tool('inspect_bulk_import','Read real progress and failures of a bulk import.',{'id':S},['id']),
    tool('propose_sample_comparison','Freeze a comparison using only sampled evidence: earlier sampled Congresses for training and latest for evaluation. Historical eligibility can block execution. Does not perform a human audit.',{'sample_id':S,'title':S,'hypothesis':S},['sample_id']),
    tool('explore_collection','Inspect dated evidence and changes for a saved collection. Use cutoff and collection_version from chat context. No forecast-change or causal inference is implied.',{'collection_id':S,'collection_version':{'type':'integer'},'cutoff':S,'window_days':{'type':'integer'},'bill_id':S,'filter':{'type':'object','properties':{'query':S,'topic':S,'watched_only':{'type':'boolean'}},'additionalProperties':False}},['collection_id']),
    tool('find_sources','Find imported bill identifiers by dataset, Congress and text. Paginated; do not mistake a page for a complete cohort.',{'dataset':D,'congress':{'type':'integer'},'query':S,'offset':{'type':'integer'},'limit':{'type':'integer'}},['dataset']),
    tool('list_collections','List saved bill collections and imported/missing coverage.',{},[]),
    tool('save_collection','Create a named collection of 1–100 explicitly selected bill IDs. Saving is not importing. Update needs id and expected_version; old versions remain.',{'name':S,'dataset':D,'bill_ids':{'type':'array','items':S},'id':S,'expected_version':{'type':'integer'}},['name','dataset','bill_ids']),
    tool('import_collection','Start a bounded official import job for a saved collection. Returns a job, not completed imports; inspect job before claiming completion.',{'collection_id':S,'refresh':{'type':'boolean'}},['collection_id']),
    tool('inspect_import_job','Read per-bill import progress and failures.',{'id':S},['id']),
    tool('propose_research_session','Freeze a reviewable research proposal for an exact saved collection, with evidence snapshot and preflight. This does not run it. Supported method: action-history structured B, own-bill enactment. Never substitute it for an unsupported requested method.',{'collection_id':S,'title':S,'hypothesis':S,'age_days':{'type':'integer'},'target':S,'candidate':S,'track':S},['collection_id','title','hypothesis']),
    tool('list_research_sessions','Find saved proposals and results for follow-up or rerun.',{},[]),
    tool('inspect_research_session','Read a frozen proposal, preflight and computed result.',{'id':S},['id']),
    tool('run_research_session','Execute a saved proposal when the user asks to run it. Frozen evidence and exact cohort; cannot bypass preflight. Do not run merely because user asked for a proposal.',{'id':S},['id']),
    tool('revise_research_session','Create a child proposal changing exactly one of age_days, collection_id or hypothesis. Original stays immutable. Use replicate_research_session for an unchanged rerun.',{'id':S,'changes':{'type':'object','properties':{'age_days':{'type':'integer'},'collection_id':S,'hypothesis':S},'additionalProperties':False}},['id','changes']),
    tool('replicate_research_session','Create a distinct child proposal with identical frozen inputs for an unchanged rerun. Execute its new ID to obtain a separate result.',{'id':S},['id']),
    tool('verify_research_session','Recompute the saved bundle offline and compare reproducibility hashes. Does not fetch new evidence.',{'id':S},['id']),
    tool('compare_research_sessions','Compute a descriptive comparison. Different checkpoints/populations are not paired validation or independent evidence of improvement.',{'left_id':S,'right_id':S},['left_id','right_id']),
    tool('export_research_session','Prepare a downloadable frozen research bundle. No credentials or chat history included.',{'id':S},['id']),
    tool('inspect_watching','Inspect local monitoring settings, watched bills, freshness and change feed.',{},[]),
    tool('watch_bill','Save or remove an imported bill in the local watchlist. Does not itself enable scheduled refresh.',{'dataset':D,'bill_id':S,'enabled':{'type':'boolean'}},['dataset','bill_id','enabled']),
    tool('configure_monitoring','Change local refresh schedule only when user requests it. Runs while server is open. In-app notification preferences only; no external messages.',{'enabled':{'type':'boolean'},'interval_minutes':{'type':'integer'},'notifications':{'type':'boolean'}},[]),
    tool('refresh_watched','Refresh watched official bills now when requested, preserving evidence and logging meaningful changes and failures.',{},[]),
]
from . import intelligence_tools
TOOLS += intelligence_tools.TOOLS
NAMES={t['function']['name'] for t in TOOLS}


def artifact(view,label,**fields):
    return dict(type='view',view=view,label=label,**fields)


def execute(store,name,args):
    if not isinstance(args,dict):raise ValueError('Tool arguments must be an object')
    if name in intelligence_tools.NAMES:return intelligence_tools.execute(store,name,args)
    if name=='inspect_priorities':return consumer.priorities(store),artifact('priorities','Open my priorities')
    if name=='save_priorities':return consumer.priorities(store,args),artifact('priorities','Open my priorities')
    if name=='inspect_activity':return consumer.activity(store),artifact('activity','Open activity')
    if name=='inspect_data_coverage':
        r=coverage_pipeline.summary(store);r['plans']=[{k:v for k,v in p.items() if k not in ('bill_ids','batches','provenance')} for p in r['plans']]
        return r,artifact('coverage','Open data coverage')
    if name=='plan_coverage_import':
        p=coverage_pipeline.plan_import(store,args)
        return {k:v for k,v in p.items() if k not in ('bill_ids','batches','provenance')},artifact('coverage','Open import plan')
    if name=='list_research_campaigns':return campaigns.list_campaigns(store),artifact('campaigns','Open research lab')
    if name=='inspect_research_campaign':return campaigns.detail(store,args['id']),artifact('campaigns','Open campaign',id=args['id'])
    if name=='create_research_campaign':
        r=campaigns.create(store,args);return r,artifact('campaigns','Open campaign',id=r['id'])
    if name=='configure_research_campaign':return campaigns.update(store,args['id'],{k:v for k,v in args.items() if k!='id'}),artifact('campaigns','Open campaign',id=args['id'])
    if name=='inspect_background_research':return autoresearch.summary(store),artifact('autoresearch','Open background research')
    if name=='configure_background_research':return autoresearch.configure(store,args),artifact('autoresearch','Open background research')
    if name=='list_audited_samples':return {'samples':[sample_brief(r) for r in sampling.list_samples(store)]},artifact('data','Open data and imports')
    if name=='discover_bill_inventory':return inventory_brief(sampling.discover_inventory(store,args)),artifact('sample','Create a sample')
    if name=='create_audited_sample':
        r=sampling.create_sample(store,args);return sample_brief(r),artifact('sample','Review sample: '+r.get('name','Saved sample'),id=r['id'])
    if name=='inspect_audited_sample':return sample_brief(sampling.get_sample(store,args['id'])),artifact('sample','Open audited sample',id=args['id'])
    if name=='import_audited_sample':return bulk_brief(sampling.start_bulk_job(store,args)),artifact('data','Open import progress')
    if name=='inspect_bulk_import':return bulk_brief(sampling.get_bulk_job(store,args['id'])),artifact('data','Open import progress')
    if name=='propose_sample_comparison':
        r=sample_research.propose(store,args);return session_brief(r),artifact('session','Open sample comparison',id=r['id'])
    if name=='explore_collection':
        from .explore import collection_view
        result=collection_view(store,args['collection_id'],args.get('cutoff'),args.get('window_days',90),args.get('collection_version'))
        from .chat_context import validate
        context=validate(store,dict(collection_id=result['collection']['id'],collection_version=result['collection']['version'],dataset=result['collection']['dataset'],cutoff=result['as_of'],window_days=result['window_days'],filter=args.get('filter'),bill_id=args.get('bill_id')),result['collection']['dataset'])
        result['collection_summary']=result['summary']
        result['rows']=[r for r in result['rows'] if r['bill_id'] in context['visible_bill_ids']]
        rows=result['rows']
        result['summary']=dict(total=len(rows),available=sum(r['available'] for r in rows),unavailable=sum(not r['available'] for r in rows),changed=sum(bool(r['new_event_count'] or r['stage_change'] or r['newly_available']) for r in rows),new_events=sum(r['new_event_count'] for r in rows),newly_available=sum(r['newly_available'] for r in rows))
        result['research_context']=context
        return result,artifact('explore','Open evidence landscape',collection_id=result['collection']['id'],collection_version=result['collection']['version'],cutoff=result['as_of'],window_days=result['window_days'],filter=context['filter'],bill_id=context['bill_id'])
    if name=='find_sources':
        if args.get('dataset') not in ('demo','official'):raise ValueError('Choose official or demo')
        limit=args.get('limit',40);offset=args.get('offset',0)
        if not isinstance(limit,int) or not 1<=limit<=100 or not isinstance(offset,int) or offset<0:raise ValueError('Use limit 1–100 and nonnegative offset')
        rows=[b for b in store.bills(args['dataset']) if (not args.get('congress') or b['congress']==args['congress']) and args.get('query','').lower() in (b['bill_id']+' '+b['title']).lower()]
        page=[{k:b.get(k) for k in ('bill_id','title','congress','observed_at')} for b in rows[offset:offset+limit]]
        return {'bills':page,'total':len(rows),'next_offset':offset+limit if offset+limit<len(rows) else None},artifact('collections','Open collections')
    if name=='list_collections':return {'collections':collections.list_collections(store)},artifact('collections','Open collections')
    if name=='save_collection':
        r=collections.save_collection(store,args);return r,artifact('collections','Open collection: '+r['name'],id=r['id'])
    if name=='import_collection':
        r=collections.start_import_job(store,args);return r,artifact('collections','View import progress',job_id=r['id'])
    if name=='inspect_import_job':return collections.get_import_job(store,args['id']),artifact('collections','View import progress',job_id=args['id'])
    if name=='list_research_sessions':return {'sessions':[session_brief(r) for r in sessions.list_sessions(store)]},artifact('experiments','Open research sessions')
    if name in ('propose_research_session','inspect_research_session','run_research_session','revise_research_session','replicate_research_session'):
        if name=='propose_research_session':r=sessions.propose(store,args)
        elif name=='inspect_research_session':r=sessions.get_session(store,args['id'])
        elif name=='run_research_session':sessions.execute(store,args['id']);r=sessions.get_session(store,args['id'])
        elif name=='replicate_research_session':r=sessions.replicate(store,args['id'])
        else:r=sessions.revise(store,args['id'],args['changes'])
        return session_brief(r),artifact('session','Open research session: '+r.get('title',r['id']),id=r['id'])
    if name=='compare_research_sessions':
        return sessions.compare(store,args['left_id'],args['right_id']),artifact('session','Open session comparison',id=args['right_id'],compare_id=args['left_id'])
    if name=='verify_research_session':
        return sessions.reproduce_bundle(sessions.export_bundle(store,args['id'])),artifact('session','Open reproduced session',id=args['id'])
    if name=='export_research_session':
        bundle=sessions.export_bundle(store,args['id'])
        return {'id':args['id'],'status':'ready','note':'Download the research bundle from this session. It contains frozen inputs; no credentials or chat messages.'},artifact('session','Download research bundle',id=args['id'])
    if name=='inspect_watching':return monitoring.summary(store),artifact('watching','Open watching')
    if name=='watch_bill':
        if args.get('dataset') not in ('official','demo') or not isinstance(args.get('enabled'),bool):raise ValueError('Invalid watch settings')
        if not store.bill(args['dataset'],args['bill_id']):raise ValueError('Import this bill first')
        store.watch(args['dataset'],args['bill_id'],args['enabled'])
        return {'bill_id':args['bill_id'],'watched':args['enabled']},artifact('watching','Open watching')
    if name=='configure_monitoring':return monitoring.configure(store,args),artifact('watching','Open monitoring settings')
    if name=='refresh_watched':return monitoring.refresh_watched(store),artifact('watching','Open refresh results')
    raise ValueError('Unknown product tool')


def session_brief(session):
    result=session.get('result')
    brief={k:v for k,v in session.items() if k!='result'}
    if session.get('learning'):
        learning=session['learning']
        brief['learning']={k:v for k,v in learning.items() if k!='cases'}
        brief['learning']['cases']=[{k:v for k,v in row.items() if k not in ('artifact','inner_validation')} for row in learning.get('cases',[])][:20]
        brief['learning']['case_count']=len(learning.get('cases',[]))
    if result:
        brief['result']={k:v for k,v in result.items() if k!='results'}
        brief['result']['results']=[{k:v for k,v in row.items() if k not in ('model_artifact','input_snapshot','training_manifest')} for row in result.get('results',[])]
    return brief


def session_summary(session):
    result=session.get('result') or {}
    if result.get('status')!='completed':
        return 'Research session '+session.get('status','saved')+'. Open the proposal for its evidence checks.'
    label='Synthetic demonstration' if session['config']['dataset']=='demo' else 'Official-source development'
    text=f"{label} session completed: {result['available']} of {result['attempted']} selected bills had eligible forecasts; {result['scored']} resolved cases were scored."
    if result.get('metrics'):
        text+=f"\n\nModel Brier: {result['metrics']['brier']:.4f}. Historical-rate baseline: {result['baseline']['brier']:.4f}. Lower is better."
    if session.get('learning'):
        learning=session['learning']
        text+=f"\n\nAutomatic learning: {learning['status'].replace('_',' ')}. {learning.get('adjusted_count',0)} case settings adjusted using earlier training evidence. The adaptive result is a separate development comparison, not validated forecasting skill."
    text+='\n\nThis is a retrospective development result, not validated forecasting skill. The report preserves the frozen collection, evidence, exclusions and model inputs. Open it to compare, revise one assumption, reproduce or export.'
    return text


def contextual_arguments(name,args,context):
    """Carry omitted Explore scope into tools; explicit arguments can change it."""
    if name!='explore_collection' or not isinstance(args,dict) or not context or args.get('collection_id')!=context['collection_id']:
        return args
    scoped=dict(args)
    for key in ('collection_version','cutoff','window_days','filter','bill_id'):
        if context.get(key) is not None:scoped.setdefault(key,context[key])
    return scoped


def inventory_brief(r):
    return {k:([{key:s[key] for key in ('congress','type','count')} for s in r[k]] if k=='strata' else r[k]) for k in ('id','hash','total','congresses','strata','status','note')}


def sample_brief(r):
    return {k:r.get(k) for k in ('id','name','size','seed','inventory_hash','hash','strata','protocol','readiness','collection_id','evaluation_collection_id')}


def bulk_brief(r):
    result={k:r.get(k) for k in ('id','sample_id','status','total','completed','parsed','failed','downloaded','audited','note')}
    result['failures']=[v for v in r.get('results',[]) if v['status']=='failed'][:20]
    result['failure_list_note']='At most 20 failures shown; open Data & imports for all records.'
    return result
