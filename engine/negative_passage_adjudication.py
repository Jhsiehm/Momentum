"""Current-time AI/source adjudication of explicitly pending final-calendar bills.
Does not assert historical checkpoint completeness, historical label availability,
or independent human review. Never promotes a model.
"""
import json,re
from .store import now,digest,timestamp,congress_end
from .sequential import TARGET
from .negative_passage_audit import D,classify

def adjudicate(row,review_time):
    if row['positive_control'] or row['status']!='corroborated_pending_negative_candidate':raise ValueError('Not a pending negative candidate')
    if classify(row['calendar_entry'],row['actions'],row['versions'],[],row['kind'])!='corroborated_pending_negative_candidate':raise ValueError('Contradictory evidence')
    flat=' '.join(row['calendar_entry'].split());m=re.search(r'(Union|House|Private) Calendar\s*\.+\s*\1\s+(\d+)\s*$',flat)
    if not m:raise ValueError('Missing terminal calendar identity')
    matching=[a for a in row['actions'] if a['text']==f'Placed on the {m[1]} Calendar, Calendar No. {m[2]}.' and a['source_system']=='2']
    if len(matching)!=1:raise ValueError('Calendar number/action mismatch')
    end=congress_end(row['congress']);dates=[timestamp(a['date']) for a in row['actions']]
    if max(dates)>timestamp(matching[0]['date']) or max(dates)>end:raise ValueError('Later actions require adjudication')
    intro=[a for a in row['actions'] if a['code'] in ('1000','Intro-H') and a['text']=='Introduced in House']
    if not intro or min(dates)<min(timestamp(a['date']) for a in intro):raise ValueError('Incomplete or inconsistent introduction history')
    if row['kind']!='hr':raise ValueError('This reviewed rule covers House bills only')
    if row['calendar_available_at']<=end or review_time<row['calendar_available_at']:raise ValueError('Final-calendar availability inconsistent with closed Congress')
    return dict(bill_id=row['bill_id'],target=TARGET,value=0,effective_at=end,available_at=review_time,complete_coverage=True,coverage_through=end,source_url=row['calendar_source']['url'],source_hash=row['calendar_source']['sha256'],audit_note='AI/source-reviewed outcome: final second-session numbered history explicitly leaves this exact bill pending on the House/Union calendar; full retained official BILLSTATUS action list ends at the same calendar placement and contains no passage or contradictory later action. Coverage assertion is for this outcome through Congress end, not historical day30 features. Available only at current adjudication time; no earlier availability claimed.',evidence=dict(calendar_entry=row['calendar_entry'],calendar_source=row['calendar_source'],billstatus_source=row['billstatus_source'],actions_hash=digest(row['actions']),matched_calendar_action=matching[0],final_calendar_historical_bound=row['calendar_available_at']),reviewer_kind='AI_assistant_and_deterministic_source_checks',human_reviewed=False,historical_training_eligible=False,release_eligible=False)

def run():
    audit=json.loads((D/'audit.json').read_text());rows=json.loads((D/'negative-review-queue.json').read_text());path=D/'adjudication.json'
    review_time=json.loads(path.read_text())['reviewed_at'] if path.exists() else now()
    labels=[adjudicate(r,review_time) for r in rows]
    result=dict(parent_audit_hash=audit['hash'],reviewed_at=review_time,labels=labels,source_reviewed_negative_labels=len(labels),human_certified_labels=0,historical_training_labels=0,with_day30_publication_proxy=sum(r['day30_proxy_available'] for r in rows),note='Case-by-case current-time outcome adjudication, appended after candidate screening; original audit preserved. Selection-biased subset; not representative training data.',release_eligible=False);result['hash']=digest(result)
    body=json.dumps(result,indent=2)+'\n'
    if path.exists():assert path.read_text()==body
    else:path.write_text(body)
    target=D/'audited-negative-labels.jsonl';body=''.join(json.dumps(x,sort_keys=True)+'\n' for x in labels)
    if target.exists():assert target.read_text()==body
    else:target.write_text(body)
    print(json.dumps({k:v for k,v in result.items() if k!='labels'},indent=2));return result
if __name__=='__main__':run()
