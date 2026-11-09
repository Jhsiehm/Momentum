"""Current-rendition retrospective assertions; feature and outcome passes separate."""
import datetime as dt
import math
import re
import xml.etree.ElementTree as ET
import urllib.parse
from scripts import official_billstatus_readiness_v1 as audit

VERSION='official-context-features-v1'
STAGE={'ih':0,'is':0,'rh':1,'rs':1,'eh':2,'es':2,'enr':3}
EDITION_TYPE={'ih':'Introduced in House','is':'Introduced in Senate','rh':'Reported in House','rs':'Reported to Senate','eh':'Engrossed in House','es':'Engrossed in Senate','enr':'Enrolled Bill'}


def scalar(node,path,required=True):
    found=node.findall(path)
    if len(found)>1 or (required and len(found)!=1) or any(len(x) for x in found):
        raise ValueError('Missing/ambiguous scalar '+path)
    return (found[0].text or '').strip() if found else None


def container(node,path):
    found=node.findall(path)
    if len(found)>1:raise ValueError('Duplicate container '+path)
    if found and any(child.tag!='item' for child in found[0]):raise ValueError('Unsupported container layout '+path)
    return found[0] if found else None


def date(value,allow_timestamp=False):
    if not value:raise ValueError('Missing date')
    if allow_timestamp:
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z)?',value):raise ValueError('Unsupported asserted date')
        if 'T' in value:dt.datetime.fromisoformat(value.replace('Z','+00:00'))
        value=value[:10]
    result=dt.date.fromisoformat(value)
    if result.isoformat()!=value:raise ValueError('Noncanonical date')
    return result


def parsed(raw,case):
    inspection=audit.inspect_xml(raw,case)
    if not inspection['identity_valid']:raise ValueError('Invalid XML identity/introduction')
    return ET.fromstring(raw).find('bill'),inspection


def related_ids(bill):
    container(bill,'relatedBills')
    result=[]
    for item in bill.findall('relatedBills/item'):
        c,k,n=scalar(item,'congress'),scalar(item,'type').lower(),scalar(item,'number')
        if not re.fullmatch('[1-9][0-9]*',c) or not re.fullmatch('[1-9][0-9]*',n) or k not in ('hr','s','hres','sres','hjres','sjres','hconres','sconres'):raise ValueError('Invalid related identity')
        result.append(f'{k}{n}-{c}')
    return sorted(set(result))


def baseline(bill,case,intro,cutoff):
    if container(bill,'textVersions') is None:raise ValueError('Missing text-version history')
    editions={}
    prefix=f"BILLS-{case['congress']}{case['bill_type']}{case['bill_number']}"
    for item in bill.findall('textVersions/item'):
        # Only the seven frozen legacy publication codes enter the anchor.
        packages=set()
        for url in item.findall('formats/item/url'):
            parsed_url=urllib.parse.urlparse(url.text or '')
            if parsed_url.scheme!='https' or parsed_url.netloc not in ('www.govinfo.gov','govinfo.gov') or parsed_url.query or parsed_url.fragment:
                raise ValueError('Unsupported edition URL origin')
            match=re.match(r'^/content/pkg/('+re.escape(prefix)+r'([a-z]+)\d*)/(pdf|xml|html)/([^/]+)$',parsed_url.path)
            if match and match[2] in STAGE:
                if match[4]!=match[1]+'.'+('htm' if match[3]=='html' else match[3]):
                    raise ValueError('Edition filename/package identity mismatch')
                packages.add((match[1],match[2]))
        if not packages:continue
        published=date(scalar(item,'date'),True);kind=scalar(item,'type')
        for package,code in packages:
            if kind!=EDITION_TYPE[code]:raise ValueError('Edition code/type conflict')
            entry={'package':package,'code':code,'date':published.isoformat()}
            if package in editions and editions[package]!=entry:raise ValueError('Conflicting edition dates')
            editions[package]=entry
    introductions=[v for v in editions.values() if v['code']==('ih' if case['bill_type']=='hr' else 'is')]
    if len(introductions)!=1 or not intro<=date(introductions[0]['date'])<cutoff:raise ValueError('Missing/ambiguous introduced edition')
    eligible=[v for v in editions.values() if intro<=date(v['date'])<cutoff]
    stage=max([0]+[STAGE[v['code']] if v['code'] not in ('eh','es') or v['code']==('eh' if case['bill_type']=='hr' else 'es') else 0 for v in eligible])
    last=max([intro]+[date(v['date']) for v in eligible])
    x=[stage/4,min((cutoff-intro).days,730)/730,min(len(eligible),30)/30,min((cutoff-last).days,730)/730,int(case['bill_type']=='s'),min(sum((cutoff-date(v['date'])).days<=30 for v in eligible),10)/10]
    return x,stage,sorted(eligible,key=lambda v:(v['date'],v['package']))


def cosponsors(bill,intro,cutoff):
    if container(bill,'cosponsors') is None:return None,'absent_cosponsor_container'
    if any(child.tag!='item' for child in bill.find('cosponsors')):raise ValueError('Unsupported cosponsor layout')
    histories={}
    for item in bill.findall('cosponsors/item'):
        identity=scalar(item,'bioguideId',False) or scalar(item,'identifiers/bioguideId',False)
        if not identity or not re.fullmatch('[A-Z][0-9]{6}',identity):raise ValueError('Missing/invalid cosponsor identity')
        joined=date(scalar(item,'sponsorshipDate'));withdrawn=scalar(item,'sponsorshipWithdrawnDate',False)
        withdrawn=date(withdrawn) if withdrawn else None
        if joined<intro or withdrawn and withdrawn<joined:raise ValueError('Invalid cosponsor interval')
        interval=(joined,withdrawn)
        if identity in histories and histories[identity]!=interval:raise ValueError('Conflicting duplicate cosponsor history')
        histories[identity]=interval
    if any(joined==cutoff or withdrawn==cutoff for joined,withdrawn in histories.values()):
        return None,'same_day_cosponsor_event_ambiguous'
    active=sum(joined<cutoff and (withdrawn is None or withdrawn>=cutoff) for joined,withdrawn in histories.values())
    return math.log1p(active),None


def procedural(bill,intro,cutoff):
    action_container=container(bill,'actions')
    if action_container is None:return (None,'absent_action_container'),(None,'absent_action_container')
    actions=[];committees=set()
    for item in bill.findall('actions/item'):
        when=date(scalar(item,'actionDate'));code=scalar(item,'actionCode',False)
        if when<intro:raise ValueError('Action predates introduction')
        if when>=cutoff:continue
        system=scalar(item,'sourceSystem/code',False)
        if system not in ('0','1','2','9'):raise ValueError('Unsupported action source system')
        if code and not re.fullmatch(r'[A-Za-z0-9]+',code):raise ValueError('Invalid action code')
        actions.append((when,system,code))
    # Committee activity records corroborate exact referral activity without action-text inference.
    committee_container=container(bill,'committees')
    referral_missing=False
    if committee_container is not None:
        if any(child.tag!='item' for child in committee_container):raise ValueError('Unsupported committee layout')
        for item in bill.findall('committees/item'):
            code=scalar(item,'systemCode')
            if not re.fullmatch('[a-z]{2}[a-z0-9]{2}[0-9]{2}',code):raise ValueError('Invalid committee code')
            activities=container(item,'activities')
            if activities is None:referral_missing=True
            elif any(child.tag!='item' for child in activities):raise ValueError('Unsupported committee activity layout')
            for activity in item.findall('activities/item'):
                when=date(scalar(activity,'date'),True);name=scalar(activity,'name')
                if when<intro:raise ValueError('Committee activity predates introduction')
                if when<cutoff and name=='Referred to':committees.add(code)
    breadth=(math.log1p(len(committees)),None) if committee_container is not None and not referral_missing else (None,'missing_referral_identity_or_committee_history')
    recency=(min(180,(cutoff-max(d for d,system,code in set(actions))).days)/180,None) if actions else (None,'no_qualifying_precutoff_action')
    return breadth,recency


def extract_features(raw,case):
    bill,inspection=parsed(raw,case)
    if not inspection['introduction_in_calendar_congress']:raise ValueError('Introduction outside calendar Congress')
    intro=date(inspection['introduced_at']);cutoff=intro+dt.timedelta(days=180)
    end=dt.date(1789+2*(case['congress']-1)+2,1,3)
    result=dict(version=VERSION,bill_id=case['bill_id'],congress=case['congress'],cutoff=cutoff.isoformat(),congress_end=end.isoformat(),related=related_ids(bill),feature_errors=[],context=[None]*3,missing=[1]*3,anchor=None,stage=None,source_semantics='retrospective_publication_date_assertions_not_availability')
    if cutoff>=end:result['feature_errors'].append('cutoff_at_or_after_congress_end');return result
    try:result['anchor'],result['stage'],result['eligible_editions']=baseline(bill,case,intro,cutoff)
    except ValueError as error:result['feature_errors'].append(str(error));return result
    reasons=[]
    try:co=cosponsors(bill,intro,cutoff)
    except ValueError as error:co=(None,str(error))
    try:breadth,recency=procedural(bill,intro,cutoff)
    except ValueError as error:breadth,recency=(None,str(error)),(None,str(error))
    for index,(value,reason) in enumerate((co,breadth,recency)):
        result['context'][index]=value;result['missing'][index]=int(value is None);reasons.append(reason)
    result['missing_reasons']=reasons
    return result


def resolve_outcome(raw,case,cutoff):
    """Called only after independently frozen feature/family population, never in acquisition."""
    bill,inspection=parsed(raw,case);cutoff=date(cutoff)
    end=dt.date(1789+2*(case['congress']-1)+2,1,3)
    answer=dict(bill_id=case['bill_id'],y=None,reason=None,certified_negative=False)
    public=set();events=[];other_enactment_assertion=False
    try:
        law_container=container(bill,'laws')
        if law_container is not None and any(child.tag!='item' for child in law_container):raise ValueError('Unsupported law container layout')
        for item in bill.findall('laws/item'):
            kind=scalar(item,'type').lower();number=scalar(item,'number')
            if kind in ('public','public law'):
                if not re.fullmatch(str(case['congress'])+r'-[1-9][0-9]*',number):raise ValueError('Public-law identity mismatch')
                public.add(number)
            else:raise ValueError('Private or unsupported law type')
        if container(bill,'actions') is None or not bill.findall('actions/item'):raise ValueError('Missing action coverage')
        for action in bill.findall('actions/item'):
            when=date(scalar(action,'actionDate'));code=scalar(action,'actionCode',False)
            system=scalar(action,'sourceSystem/code',False)
            if system not in ('0','1','2','9'):raise ValueError('Unsupported action source system')
            action_text=scalar(action,'text',False) or ''
            if code in ('37000','E30000') or re.match(r'(?:Signed by President|Became (?:Public|Private) Law|Enacted)',action_text,re.I):
                other_enactment_assertion=True
            if re.search(r'became\s+public\s+law',action_text,re.I) and code not in ('36000','E40000'):
                raise ValueError('Public-law assertion with unsupported action code')
            if code in ('36000','E40000'):
                system=scalar(action,'sourceSystem/code')
                if (code,system) not in (('36000','9'),('E40000','2'),('E40000','9')):raise ValueError('Unsupported enactment code/source pairing')
                text=scalar(action,'text');match=re.fullmatch(r'Became Public Law No[.:]?\s*:?\s*(\d+-\d+)\.?',text,re.I)
                if not match:raise ValueError('Enactment action lacks public-law identity')
                events.append((match[1],when))
        for path in ('latestAction','lastAction'):
            latest=bill.find(path)
            if latest is not None:
                text=scalar(latest,'text',False) or ''
                if re.match(r'(?:Signed by President|Became (?:Public|Private) Law|Enacted)',text,re.I) and not events:
                    raise ValueError('Uncorroborated latest-action public-law assertion')
        if other_enactment_assertion and not events:
            raise ValueError('Uncorroborated signing/enactment assertion')
        container(bill,'textVersions')
        for version in bill.findall('textVersions/item'):
            if (scalar(version,'type',False) or '').lower()=='public law' and not events:
                raise ValueError('Uncorroborated public-law edition assertion')
        if public or events:
            if not public or not events or {law for law,when in events}!=public:raise ValueError('Law/action disagreement')
            dates={when for law,when in events}
            if len(public)!=1 or len(dates)!=1:raise ValueError('Ambiguous law/date multiplicity')
            enacted=next(iter(dates));answer['enacted_at']=enacted.isoformat()
            if enacted<=cutoff:answer['reason']='already_enacted_or_cutoff_date_ambiguous'
            elif enacted>=end:answer['reason']='outside_horizon_or_end_date_ambiguous'
            else:answer.update(y=1,reason='concordant_own_bill_public_law_action',label_matured_at=enacted.isoformat())
        else:
            updated=date(scalar(bill,'updateDate'),True)
            if updated<=end:raise ValueError('No postCongress update assertion')
            answer.update(y=0,reason='uncertified_current_official_record_negative_proxy',assertion_updated_at=updated.isoformat(),label_matured_at=end.isoformat())
    except (ValueError,TypeError) as error:answer['reason']=str(error)
    return answer
