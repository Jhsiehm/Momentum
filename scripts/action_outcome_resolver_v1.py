"""Separately versioned exact signing-annotation compatibility; no invented law events."""
import datetime as dt
import re
from scripts.official_context_features_v2 import parsed,date,scalar,container,action_source

VERSION='action-outcome-resolver-v1'


def resolve_outcome(raw,case,cutoff):
    """Called only after independently frozen feature/family population, never in acquisition."""
    bill,inspection=parsed(raw,case);cutoff=date(cutoff)
    end=dt.date(1789+2*(case['congress']-1)+2,1,3)
    answer=dict(bill_id=case['bill_id'],y=None,reason=None,certified_negative=False)
    public=set();events=[];signing_annotations=[];other_enactment_assertion=False
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
            action_source(action)  # Named Senate ordinary history is accepted without inventing a code.
            action_text=scalar(action,'text',False) or ''
            if code in ('37000','E30000') or re.match(r'(?:Signed by President|Became (?:Public|Private) Law|Enacted)',action_text,re.I):
                other_enactment_assertion=True
            if re.search(r'became\s+public\s+law',action_text,re.I) and code not in ('36000','E40000'):
                raise ValueError('Public-law assertion with unsupported action code')
            if (code,system,action_text)==('36000','9','Signed by President.'):
                signing_annotations.append(when)
                continue  # This assertion never supplies a law identity or enactment event.
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
            enacted=next(iter(dates))
            if any(when!=enacted for when in signing_annotations):raise ValueError('Signing annotation/enactment date disagreement')
            answer['enacted_at']=enacted.isoformat()
            if enacted<=cutoff:answer['reason']='already_enacted_or_cutoff_date_ambiguous'
            elif enacted>=end:answer['reason']='outside_horizon_or_end_date_ambiguous'
            else:answer.update(y=1,reason='concordant_own_bill_public_law_action',label_matured_at=enacted.isoformat())
        else:
            updated=date(scalar(bill,'updateDate'),True)
            if updated<=end:raise ValueError('No postCongress update assertion')
            answer.update(y=0,reason='uncertified_current_official_record_negative_proxy',assertion_updated_at=updated.isoformat(),label_matured_at=end.isoformat())
    except (ValueError,TypeError) as error:answer['reason']=str(error)
    return answer
