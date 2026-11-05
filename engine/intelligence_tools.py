"""Shared chat contracts for deterministic intelligence and local organization work."""
from . import intelligence, firm_workspace
S={'type':'string'}
STRINGS={'type':'array','items':S}
FILTER={'type':'object','properties':{'congresses':{'type':'array','items':{'type':'integer'}},'topics':STRINGS,'query':S,'bill_ids':STRINGS,'type':S},'additionalProperties':False}
def tool(name,description,properties,required=()):
    return {'type':'function','function':{'name':name,'description':description,'parameters':{'type':'object','properties':properties,'required':list(required),'additionalProperties':False}}}
COMMON={'dataset':{'type':'string','enum':['official','demo']},'cutoff':S,'filters':FILTER,'limit':{'type':'integer'}}
TOOLS=[
 tool('inspect_intelligence_capabilities','Inspect supported evidence analysis and missing forecasting capabilities before answering novel hypotheses.',{}),
 tool('analyze_bill_groups','Calculate and save descriptive historical bill groups and disjoint overlaps. Raw resolved-case rates are NOT forecast probabilities or causal effects. Unknown outcomes stay unknown.',dict(COMMON,groups={'type':'array','items':{'type':'object','properties':{'name':S,'filters':FILTER},'required':['name','filters'],'additionalProperties':False}})),
 tool('rank_saved_forecasts','Compare only compatible, recent, unresolved saved prospective estimates within the specified local population. Does not generate or validate forecasts. Report missing coverage; never call this all of Congress.',dict(COMMON,max_age_days={'type':'integer'})),
 tool('record_legislative_scenario','Save a requested hypothesis with explicit assumptions and evidence gaps. Election/stakeholder interventions are unsupported for numeric forecasts; this does not simulate or train a model.',dict(COMMON,question=S,assumptions=STRINGS),['question','assumptions']),
 tool('inspect_intelligence_report','Read an immutable saved analysis, ranking or scenario evidence packet.',{'id':S},['id']),
 tool('list_organization_profiles','List local organization profiles; these are not authenticated client accounts.',{}),
 tool('save_organization_profile','Create or update local matching interests when requested. Updates require expected_version. Matching covers imported federal titles/topics only; does not automatically follow bills.',{'id':S,'name':S,'issues':STRINGS,'excluded_terms':STRINGS,'congresses':{'type':'array','items':{'type':'integer'}},'description':S,'expected_version':{'type':'integer'}},['name']),
 tool('inspect_organization_workspace','Read organization matches, assignments, meaningful monitored changes, stakeholder citations and saved briefs.',{'profile_id':S},['profile_id']),
 tool('save_bill_assignment','Save local owner label, task and user-assessed impact when requested. Owner is not an authenticated user; impact is separate from passage probability. Updates require expected_version.',{'profile_id':S,'bill_id':S,'owner':S,'status':S,'priority':S,'impact':S,'impact_reason':S,'next_action':S,'due_date':S,'notes':S,'expected_version':{'type':'integer'}},['profile_id','bill_id']),
 tool('record_stakeholder_position','Record a user-provided sourced position. Citation remains unverified; never infer influence or a probability change. Do not invent source URLs, quotations or dates.',{'profile_id':S,'bill_id':S,'organization':S,'position':S,'statement':S,'source_url':S,'published_at':S},['profile_id','bill_id','organization','position','statement','source_url','published_at']),
 tool('create_organization_brief','Save a deterministic, sourced local briefing snapshot when requested. No external sending. Includes scope and monitoring limits.',{'profile_id':S,'window_days':{'type':'integer'}},['profile_id']),
]
NAMES={t['function']['name'] for t in TOOLS}
def execute(store,name,args):
    if not isinstance(args,dict):raise ValueError('Tool arguments must be an object')
    view='intelligence';options={}
    if name=='inspect_intelligence_capabilities':result=intelligence.capabilities(store)
    elif name=='analyze_bill_groups':result=intelligence.analyze(store,args);options={'id':result['id']}
    elif name=='rank_saved_forecasts':result=intelligence.rank(store,args);options={'id':result['id']}
    elif name=='record_legislative_scenario':result=intelligence.scenario(store,args);options={'id':result['id']}
    elif name=='inspect_intelligence_report':result=intelligence.report(store,args['id']);options={'id':result['id']}
    else:
        view='firm'
        if name=='list_organization_profiles':result={'profiles':firm_workspace.profiles(store)}
        elif name=='save_organization_profile':result=firm_workspace.save_profile(store,args);options={'profile_id':result['id']}
        elif name=='inspect_organization_workspace':result=firm_workspace.dashboard(store,args['profile_id']);options={'profile_id':args['profile_id']}
        elif name=='save_bill_assignment':result=firm_workspace.save_work_item(store,args);options={'profile_id':args['profile_id'],'bill_id':args['bill_id']}
        elif name=='record_stakeholder_position':result=firm_workspace.add_position(store,args);options={'profile_id':args['profile_id'],'bill_id':args['bill_id']}
        elif name=='create_organization_brief':result=firm_workspace.create_brief(store,args);options={'profile_id':args['profile_id'],'brief_id':result['id']}
        else:raise ValueError('Unknown intelligence tool')
    # Frozen raw evidence is available in the report, not duplicated into model context.
    if view=='intelligence':result={k:v for k,v in result.items() if k not in ('frozen_rows','evidence')}
    return result,dict(type='view',view=view,label='Open evidence analysis' if view=='intelligence' else 'Open organization workspace',**options)
