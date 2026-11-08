"""Source-offset and review-integrity checks for provisional v2 design records."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from engine.paper_evaluation import require, seal, unseal
from engine.store import ROOT, digest
from scripts.paper_review_packet import persist_or_compare


def nonempty(value):
    return isinstance(value,str) and bool(value.strip())


def check_quote(item,text):
    require(nonempty(item['quote']),'Missing evidence quote')
    start,end=item['start'],item['end']
    require(type(start) is int and type(end) is int and 0<=start<end<=len(text),'Invalid quote offsets')
    require(text[start:end]==item['quote'],'Quote/offset mismatch')


def validate_primary(review,spec,inputs,registration_hash,reviewer):
    require(review['reviewer']==reviewer and review['registration_hash']==registration_hash,'Reviewer/registration mismatch')
    require(review['rubric_sha256']==spec['rubric_sha256'],'Wrong rubric version')
    require(review['human_certified'] is False and review['historical_feature_eligible'] is False,'Invalid certification claim')
    require([r['bill_id'] for r in review['records']]==spec['batches'][reviewer],'Batch identity/order mismatch')
    byid={r['bill_id']:r for r in inputs};count=0
    # These checks establish structure and source matching, never entailment.
    for row in review['records']:
        require(set(row)==set(spec['record_fields']),'Record schema mismatch')
        source=byid[row['bill_id']]
        require(row['source_view_hash']==source['view_hash'],'Source view binding mismatch')
        require(nonempty(row['summary']),'Missing summary')
        require(set(row['mechanisms'])==set(spec['mechanisms']),'Incomplete mechanisms')
        require(all(s in spec['statuses'] for s in row['mechanisms'].values()),'Invalid mechanism status')
        uncertain={m for m,s in row['mechanisms'].items() if s=='uncertain'}
        require(set(row['uncertainties'])==uncertain and all(nonempty(s) for s in row['uncertainties'].values()),'Uncertainty explanations mismatch')
        require(isinstance(row['unresolved_effects'],list),'Invalid unresolved effects')
        for unknown in row['unresolved_effects']:
            require(unknown['mechanism'] in spec['mechanisms'] and nonempty(unknown['reason']),'Invalid unresolved effect')
            require(row['mechanisms'][unknown['mechanism']]!='absent','Unresolved effect contradicts absent status')
        require(isinstance(row['effects'],list),'Invalid effects')
        observed=set()
        for effect in row['effects']:
            require(set(effect)==set(spec['effect_fields']),'Effect schema mismatch')
            mechanism=effect['mechanism']
            require(mechanism in spec['mechanisms'] and row['mechanisms'][mechanism]=='present','Effect attached to nonpresent mechanism')
            require(effect['operation'] in spec['operations'] and effect['dimension'] in spec['dimensions'],'Invalid direction/dimension')
            require(nonempty(effect['target']) and nonempty(effect['rationale']),'Missing target/rationale')
            require(effect['actor'] is None or nonempty(effect['actor']),'Invalid actor')
            require(effect['conditions'] is None or nonempty(effect['conditions']),'Invalid conditions')
            check_quote(effect,source['text']);observed.add(mechanism);count+=1
        require(observed=={m for m,s in row['mechanisms'].items() if s=='present'},'Present mechanism lacks effect')
    return count


def validate_peer(peer,primary_envelope,spec,inputs,registration_hash,reviewer):
    primary=unseal(primary_envelope);byid={r['bill_id']:r for r in inputs}
    require(peer['reviewer']==reviewer and reviewer!=primary['reviewer'],'Peer role mismatch')
    require(peer['registration_hash']==registration_hash and peer['primary_review_hash']==primary_envelope['hash'],'Peer provenance mismatch')
    require(peer['human_certified'] is False and peer['historical_feature_eligible'] is False,'Peer certification forbidden')
    require([r['bill_id'] for r in peer['records']]==[r['bill_id'] for r in primary['records']],'Peer case coverage mismatch')
    allowed={'supported','corrections_requested','uncertain'}
    primary_rows={r['bill_id']:r for r in primary['records']};issues=0
    for row in peer['records']:
        require(row['decision'] in allowed and isinstance(row['findings'],list),'Invalid peer decision')
        require(bool(row['findings'])==(row['decision']!='supported'),'Peer findings/decision mismatch')
        for finding in row['findings']:
            require(finding['mechanism'] in spec['mechanisms'] and nonempty(finding['issue']) and nonempty(finding['proposed_change']),'Incomplete peer finding')
            index=finding['effect_index']
            require(index is None or type(index) is int and 0<=index<len(primary_rows[row['bill_id']]['effects']),'Invalid effect index')
            if index is not None:
                require(primary_rows[row['bill_id']]['effects'][index]['mechanism']==finding['mechanism'],'Peer mechanism/index mismatch')
            if finding['quote'] is not None:check_quote(finding,byid[row['bill_id']]['text'])
            else:require(finding['start'] is None and finding['end'] is None,'Offsets without quote')
            issues+=1
    return issues


def run(directory,peers=False):
    directory=Path(directory)
    def read(name):return json.loads((directory/name).read_text())
    registration=read('registration.json');spec=unseal(registration);inputs=unseal(read('inputs.json'))
    require(digest(inputs)==spec['inputs_hash'],'Inputs hash mismatch')
    input_ids=[row['bill_id'] for row in inputs]
    batch_ids=spec['batches']['agent_a']+spec['batches']['agent_b']
    require(len(set(input_ids))==len(input_ids) and len(set(batch_ids))==len(batch_ids) and set(input_ids)==set(batch_ids),'Duplicate or incomplete input/batch identities')
    require(hashlib.sha256((ROOT/spec['rubric_path']).read_bytes()).hexdigest()==spec['rubric_sha256'],'Frozen rubric changed')
    primary={};counts=Counter();mechanisms={m:Counter() for m in spec['mechanisms']};operations=Counter();effects=0
    for name in ('agent_a','agent_b'):
        primary[name]=read(name+'.json');body=unseal(primary[name])
        effects+=validate_primary(body,spec,inputs,registration['hash'],name)
        for row in body['records']:
            for m,status in row['mechanisms'].items():counts[status]+=1;mechanisms[m][status]+=1
            operations.update(e['operation'] for e in row['effects'])
    require(set(spec['batches']['agent_a']).isdisjoint(spec['batches']['agent_b']),'Primary batches overlap')
    result=dict(registration_hash=registration['hash'],primary_hashes={k:v['hash'] for k,v in primary.items()},
                cases=sum(len(unseal(v)['records']) for v in primary.values()),status_counts=dict(counts),
                by_mechanism={k:dict(v) for k,v in mechanisms.items()},effect_count=effects,operations=dict(operations),
                human_certified=False,historical_feature_eligible=False,semantic_accuracy_verified=False)
    if peers:
        peer_results={}
        for reviewer,target in (('agent_a','agent_b'),('agent_b','agent_a')):
            envelope=read(reviewer+'-peer.json');body=unseal(envelope)
            issues=validate_peer(body,primary[target],spec,inputs,registration['hash'],reviewer)
            peer_results[reviewer]=dict(hash=envelope['hash'],issues=issues,decisions=dict(Counter(r['decision'] for r in body['records'])))
        result['peer_reviews']=peer_results
    envelope=seal(result);persist_or_compare(directory/('peer-audit.json' if peers else 'primary-audit.json'),envelope)
    return envelope


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory',type=Path);p.add_argument('--peers',action='store_true')
    a=p.parse_args();r=run(a.directory,a.peers);print(json.dumps(r,indent=2))
