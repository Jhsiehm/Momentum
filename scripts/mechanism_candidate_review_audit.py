"""Reproduce design miss packets and validate source-bound agent review coverage.

Integrity checks only: reviews remain provisional and no semantic score is made.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from engine.paper_evaluation import require, unseal
from engine.store import ROOT
from scripts.run_mechanism_design_extractor import persist, read, BASE, VIEWS

RUN = BASE/'mechanism-extractor-design-20261108-v1'
REF = BASE/'mechanism-corrections-20261108-v1/corrected-dataset.json'
RESULT_HASH = '0d350fd1bace59d990908268e71560a3dec87ba2f4df74a8e29eada728508bd8'
REFERENCE_HASH = '041ad00ca21d623b68771d5e81e9dab8d3965f5585232fe688c8804ecb2a5a57'
MISS = {'vocabulary_gap','implicit_legal_effect','reference_question','scope_or_offset_issue','uncertain'}
PROPOSAL = {'supported_as_suggestion','overclaim','uncertain'}
PEER = {'agree','challenge','uncertain'}


def packet_records():
    re, reference = read(REF)
    result_envelope, result = read(RUN/'result.json')
    require(re['hash']==REFERENCE_HASH and result_envelope['hash']==RESULT_HASH, 'Frozen inputs changed')
    registration_envelope, registration = read(RUN/'registration.json')
    require(registration_envelope['hash']==result['registration_hash'], 'Registration binding mismatch')
    require(set(result['outputs'])==set(registration['bill_ids']), 'Run population differs')
    rows=[]; views={}; source_hashes={}
    for row in reference['records']:
        bid=row['bill_id']
        require(bid in registration['bill_ids'],'Non-design reference identity')
        ce,candidates=read(RUN/(bid+'.json'))
        ve,view=read(VIEWS/(bid+'.json'))
        require(ce['hash']==result['outputs'][bid], 'Candidate output mismatch')
        require(ve['hash']==row['source_view_hash']==candidates['source_view_hash'], 'Source view binding mismatch')
        views[bid]=view
        source_hashes[bid]=ve['hash']
        misses=[]
        for index,e in enumerate(row['effects']):
            if not any(h['start']<e['end'] and e['start']<h['end'] for c in candidates['candidates'] if c['mechanism']==e['mechanism'] for h in c['hits']):
                misses.append(dict(effect_index=index,**e))
        if misses or candidates['proposals']:
            rows.append(dict(bill_id=bid,source_view_hash=ve['hash'],misses=misses,proposals=candidates['proposals'],
                             view_path=str((VIEWS/(bid+'.json')).relative_to(ROOT))))
    require(len(views)==40 and len(rows)==34 and sum(len(r['misses']) for r in rows)==102, 'Unexpected design coverage')
    return rows,views,source_hashes


def validate_review(packet, review, views, peer=False):
    require(review.get('human_certified') is False and review.get('historical_feature_eligible') is False,'Certification overclaim')
    records=review['records']; rows={r['bill_id']:r for r in records}
    expected={r['bill_id']:r for r in packet['records']}
    require(len(rows)==len(records) and set(rows)==set(expected),'Review bill coverage mismatch')
    counts=Counter()
    for bid,source in expected.items():
        if 'source_view_hash' in rows[bid]:
            require(rows[bid]['source_view_hash']==source['source_view_hash'],'Contradictory source view hash')
        for field,items,key,allowed in (
            ('miss_reviews',source['misses'],'effect_index',PEER if peer else MISS),
            ('proposal_reviews',source['proposals'],'proposal_id',PEER if peer else PROPOSAL)):
            reviews=rows[bid][field]
            require(all(type(item[key]) is int if key=='effect_index' else isinstance(item[key],str) and bool(item[key].strip()) for item in reviews),'Invalid review item identity type')
            wanted={item[key]:item for item in items}
            got={item[key]:item for item in reviews}
            require(len(got)==len(reviews) and set(got)==set(wanted),'Review item coverage mismatch')
            for identity,item in got.items():
                require(item['disposition'] in allowed,'Unknown review disposition')
                require(isinstance(item.get('rationale'),str) and item['rationale'].strip(),'Missing rationale')
                if not peer and field=='miss_reviews':
                    require(item.get('mechanism')==wanted[identity]['mechanism'],'Mechanism mismatch')
                evidence=item['evidence']; a,b=evidence['start'],evidence['end'];text=views[bid]['text']
                require(type(a) is int and type(b) is int and 0<=a<b<=len(text),'Invalid evidence offset')
                require(text[a:b]==evidence['quote'],'Evidence quote mismatch')
                counts[field+':'+item['disposition']]+=1
    return dict(counts)


def run(directory, prepare=False):
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    rows,views,hashes=packet_records()
    packets={}
    for name,selected in [('packet',rows),('agent-a',rows[::2]),('agent-b',rows[1::2])]:
        packets[name]=persist(directory/(name+'.json'),dict(scope='design_only',records=selected,human_certified=False,historical_feature_eligible=False))
    if prepare:return packets['packet']
    counts={}; bindings={}
    for name,other in [('agent-a','agent-b'),('agent-b','agent-a')]:
        envelope,body=read(directory/(name+'-review.json'))
        require(body['packet_hash']==packets[name]['hash'],'Review packet binding mismatch')
        counts[name]=validate_review(unseal(packets[name]),body,views)
        pe,pb=read(directory/(other+'-peer.json'))
        require(pb['review_hash']==envelope['hash'],'Peer binding mismatch')
        counts[other+'-peer']=validate_review(unseal(packets[name]),pb,views,peer=True)
        bindings[name+'-review']=envelope['hash'];bindings[other+'-peer']=pe['hash']
    return persist(directory/'integrity.json',dict(packet_hash=packets['packet']['hash'],source_view_hashes=hashes,
        review_hashes=bindings,counts=counts,validator_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        human_certified=False,historical_feature_eligible=False,semantic_accuracy_verified=False,
        interpretation='Complete source-bound agent review coverage, not agreement as accuracy or accepted labels'))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--directory',type=Path,required=True);p.add_argument('--prepare',action='store_true');a=p.parse_args()
    result=run(a.directory,a.prepare);print(json.dumps({'hash':result['hash'],'counts':result['body'].get('counts')}))
