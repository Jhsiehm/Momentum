"""Adaptive retrospective action baseline; no publication eligibility gate."""
import datetime as dt
from scripts import official_context_features_v2 as v2
from scripts.official_context_features_v2 import resolve_outcome

VERSION='action-context-features-v1'
MILESTONES={'hr':{'5000':1,'8000':2,'28000':3},'s':{'14000':1,'17000':2,'28000':3}}


def baseline(bill,case,intro,cutoff):
    actions=v2.container(bill,'actions')
    if actions is None or not list(actions):raise ValueError('Missing action coverage')
    evidence=set();precutoff=0
    for item in actions:
        when=v2.date(v2.scalar(item,'actionDate'))
        if when<intro:raise ValueError('Action predates introduction')
        source=v2.action_source(item) # Whole history, including later source structure.
        code=v2.scalar(item,'actionCode',False)
        # Other code values are opaque activity assertions, not new milestone semantics.
        if when>=cutoff:continue
        precutoff+=1
        index=MILESTONES[case['bill_type']].get(code) if source=='code:9' else None
        if index:evidence.add((when.isoformat(),code,index))
    if not precutoff:raise ValueError('No qualifying precutoff action')
    stage=max((r[2] for r in evidence),default=0)
    return [stage/3,float(case['bill_type']=='s')],stage,[dict(date=d,source_code='9',action_code=c,index=i) for d,c,i in sorted(evidence)]


def extract_features(raw,case):
    bill,inspection=v2.parsed(raw,case)
    if not inspection['introduction_in_calendar_congress']:raise ValueError('Introduction outside calendar Congress')
    intro=v2.date(inspection['introduced_at']);cutoff=intro+dt.timedelta(days=180)
    end=dt.date(1789+2*(case['congress']-1)+2,1,3)
    result=dict(version=VERSION,bill_id=case['bill_id'],congress=case['congress'],cutoff=cutoff.isoformat(),congress_end=end.isoformat(),related=v2.v1.related_ids(bill),feature_errors=[],context=[None]*3,missing=[1]*3,missing_reasons=['baseline_ineligible']*3,anchor=None,stage=None,milestone_evidence=[],source_semantics='retrospective_action_date_assertions_not_historical_availability; whole_history_structural_eligibility')
    if cutoff>=end:result['feature_errors'].append('cutoff_at_or_after_congress_end');return result
    try:result['anchor'],result['stage'],result['milestone_evidence']=baseline(bill,case,intro,cutoff)
    except ValueError as error:result['feature_errors'].append(str(error));return result
    for index,extractor in enumerate((v2.v1.cosponsors,v2.referral_breadth,v2.action_recency)):
        try:value,reason=extractor(bill,intro,cutoff)
        except ValueError as error:value,reason=None,str(error)
        result['context'][index]=value;result['missing'][index]=int(value is None);result['missing_reasons'][index]=reason
    return result
