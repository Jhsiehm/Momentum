"""Exploratory context-triage experiment on immutable design locators.

Flagging is review prioritization, not proof of legal inoperativeness. All raw
locators are retained. Only diagnostic views exclude flagged hit identities.
"""
import argparse
from collections import Counter
import hashlib
from pathlib import Path
from engine.paper_evaluation import require
from engine.store import ROOT,digest
from scripts.run_mechanism_design_extractor import BASE,INPUTS,PILOT,VIEWS,EXPECTED_PILOT,read,persist
from scripts.run_mechanism_context_v2 import hash_file
from scripts.run_mechanism_expansion_v3 import hit_map,sample_key,REFERENCE,REFERENCE_HASH
from scripts.mechanism_design_extractor import MECHANISMS
from scripts.mechanism_context_filter import classify,RULES

EXPANDED=BASE/'mechanism-expansion-v3-20261108'
EXPANDED_HASH='e04abe0d2804f4e022a9885f5af76df4b4598ebdcd4897431b772cf41d8d0713'
PRIOR_REVIEW_HASH='e2189bd7ca958abf044fedc1777152d222ca300aa973e4cec55254a2d6ff21e2'


def key(row):
    return row['mechanism'],row['start'],row['end']


def audit_decisions(result,expanded,view):
    require(all(result.get(k) is False for k in ('human_certified','historical_feature_eligible','semantic_accuracy_verified')),'Certification overclaim')
    require(result['bill_id']==view['bill_id'] and result['source_view_hash']==view['view_hash']==expanded['source_view_hash'],'Decision source binding mismatch')
    require(result['input_text_sha256']==hashlib.sha256(view['text'].encode()).hexdigest(),'Decision text binding mismatch')
    hits=hit_map(expanded);rows=result['decisions'];decisions={key(r):r for r in rows}
    require(len(rows)==len(decisions) and set(hits)==set(decisions),'Decision coverage mismatch')
    for k,r in decisions.items():
        require(type(r['start']) is int and type(r['end']) is int,'Invalid decision offsets')
        require(r['status'] in {'flagged','retain'},'Unknown triage status')
        require(isinstance(r['reasons'],list) and all(isinstance(s,str) and s.strip() for s in r['reasons']),'Invalid reasons')
        if r['status']=='flagged':
            require(bool(r['reasons']) and all(reason in {rule['id'] for rule in RULES} for reason in r['reasons']),'Unknown flag reason')
        else:require(r['reasons']==['no_narrow_context_flag'],'Invalid retained reason')
        candidate,hit=hits[k]
        require(r['candidate_id']==candidate['candidate_id'] and r['quote']==hit['quote'],'Decision occurrence binding mismatch')
        require(isinstance(r['evidence'],list),'Evidence must be a list')
        require(r['status']!='flagged' or bool(r['evidence']),'Flag without evidence')
        for e in r['evidence']:
            a,b=e['start'],e['end'];require(type(a) is int and type(b) is int and 0<=a<b<=len(view['text']),'Invalid evidence range')
            require(view['text'][a:b]==e['quote'],'Evidence quote mismatch')
    return decisions


def overlap(reference,hits,decisions):
    counts={m:Counter() for m in MECHANISMS};lost=[]
    for i,e in enumerate(reference['effects']):
        matched=[k for k in hits if k[0]==e['mechanism'] and k[1]<e['end'] and e['start']<k[2]]
        raw=bool(matched);retained=any(decisions[k]['status']=='retain' for k in matched)
        counts[e['mechanism']].update(reference_effects=1,raw_overlap=int(raw),retained_overlap=int(retained),lost=int(raw and not retained))
        if raw and not retained:lost.append(i)
    return {m:dict(c) for m,c in counts.items()},lost


def review_sample(added,decisions,excluded):
    rows=[];counts={}
    for status in ('flagged','retain'):
        eligible=[]
        for row in added:
            identity=(row['bill_id'],*key(row))
            if identity in excluded:continue
            d=decisions[identity]
            if d['status']==status:eligible.append(dict(row,status=status,reasons=d['reasons']))
        chosen=sorted(eligible,key=sample_key)[:12]
        counts[status]=dict(eligible=len(eligible),selected=len(chosen),requested=12,shortfall=max(0,12-len(chosen)))
        rows.extend(chosen)
    return rows,counts


def run(directory):
    ee,expanded=read(EXPANDED/'result.json');re,reference=read(REFERENCE);ie,inputs=read(INPUTS);pe,pilot=read(PILOT)
    pre,prior=read(EXPANDED/'added-hit-review.json');se,sample=read(EXPANDED/'review-sample.json')
    require(ee['hash']==EXPANDED_HASH and re['hash']==REFERENCE_HASH and pe['hash']==EXPECTED_PILOT,'Frozen experiment binding mismatch')
    require(pre['hash']==PRIOR_REVIEW_HASH and prior['sample_hash']==se['hash']==expanded['review_sample_hash'],'Prior review binding mismatch')
    ids=[r['bill_id'] for r in inputs];refs={r['bill_id']:r for r in reference['records']}
    require(len(ids)==len(set(ids))==len(refs)==40 and set(ids)==set(refs)==set(expanded['outputs']),'Design population mismatch')
    design={r['bill_id'] for r in pilot['selection'] if r['partition']=='design'};quality={r['bill_id'] for r in pilot['selection'] if r['partition']=='quality'}
    require(set(ids)<=design and set(ids).isdisjoint(quality),'Quality firewall violation')
    paths=[EXPANDED/'result.json',REFERENCE,INPUTS,PILOT,EXPANDED/'added-hit-review.json',EXPANDED/'review-sample.json']
    views=[];outputs={}
    for item in inputs:
        bid=item['bill_id'];vp=VIEWS/(bid+'.json');ve,v=read(vp);op=EXPANDED/(bid+'.json');oe,o=read(op)
        require(oe['hash']==expanded['outputs'][bid] and ve['hash']==item['view_hash']==refs[bid]['source_view_hash']==o['source_view_hash'],'View/output binding mismatch')
        require(all(item[k]==v[k] for k in ('bill_id','text','spans','source')),'Input changed')
        paths.extend([vp,op]);views.append(dict(v,view_hash=ve['hash']));outputs[bid]=o
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    code=['scripts/run_mechanism_context_filter.py','scripts/mechanism_context_filter.py','scripts/run_mechanism_expansion_v3.py',
          'scripts/mechanism_design_extractor_v3.py','scripts/mechanism_design_extractor_v2.py','scripts/mechanism_design_extractor.py',
          'scripts/run_mechanism_context_v2.py','scripts/run_mechanism_design_extractor.py','scripts/mechanism_reference_v3.py',
          'scripts/mechanism_rubric_v2_audit.py','scripts/mechanism_effect_evaluation.py','engine/paper_evaluation.py','engine/store.py',
          'tests/test_mechanism_context_filter.py','tests/test_mechanism_context_filter_contrasts.py','tests/test_mechanism_filter_runner.py']
    files={str(p.relative_to(ROOT)):hash_file(p) for p in paths};codes={p:hash_file(ROOT/p) for p in code}
    registration=persist(directory/'registration.json',dict(scope='exploratory_design_context_filter',bill_ids=ids,
        expanded_hash=ee['hash'],reference_hash=re['hash'],prior_review_hash=pre['hash'],rules=RULES,input_files=files,code_sha256=codes,
        hypothesis='Generic context flags identify nonoperative occurrences while limiting loss of useful locators; assess tradeoff without automatic promotion',
        tuning_disclosure='Prior24 review and design source patterns informed implementation; not held-out semantic validation',
        review_sampling='Per status flagged/retain: first12 added unique hits by SHA256 compactJSON[bill_id,mechanism,start,end], excluding prior24; no quota replacement',
        quality_text_access=False,model_fitting=False,raw_hit_deletion=False))
    totals=Counter();reasons=Counter();bymechanism={m:Counter() for m in MECHANISMS};all_decisions={};hashes={};losses=[]
    for view in views:
        bid=view['bill_id'];o=outputs[bid];before=(digest(view),digest(o))
        result=classify(view,o);require(result==classify(view,o),'Nondeterministic filter')
        require(before==(digest(view),digest(o)),'Filter mutated raw inputs')
        decisions=audit_decisions(result,o,view);counts,lost=overlap(refs[bid],hit_map(o),decisions)
        for m,c in counts.items():bymechanism[m].update(c)
        totals.update(bills=1,raw_hits=len(decisions),flagged=sum(d['status']=='flagged' for d in decisions.values()),retained=sum(d['status']=='retain' for d in decisions.values()))
        for k,d in decisions.items():all_decisions[(bid,*k)]=d;reasons.update(d['reasons'])
        if lost:losses.append(dict(bill_id=bid,effect_indices=lost))
        hashes[bid]=persist(directory/(bid+'.json'),result)['hash']
    prior_counts=Counter()
    for row in prior['records']:prior_counts[row['disposition']+':'+all_decisions[(row['bill_id'],*key(row))]['status']]+=1
    added=[dict(bill_id=c['bill_id'],source_view_hash=refs[c['bill_id']]['source_view_hash'],**h) for c in expanded['comparisons'] for h in c['added_hits']]
    excluded={(r['bill_id'],*key(r)) for r in sample['records']}
    selected,quotas=review_sample(added,all_decisions,excluded)
    review=persist(directory/'review-sample.json',dict(registration_hash=registration['hash'],records=selected,quotas=quotas,
        interpretation='Fresh occurrence review on previously used design bills; stratified sample, not blinded or generalizable accuracy'))
    require(all(hash_file(ROOT/p)==h for p,h in {**files,**codes}.items()),'Bound code/source changed')
    return persist(directory/'result.json',dict(registration_hash=registration['hash'],outputs=hashes,totals=dict(totals),reason_counts=dict(reasons),
        by_mechanism={m:dict(c) for m,c in bymechanism.items()},lost_reference_intersections=losses,prior24_diagnostic=dict(prior_counts),
        review_sample_hash=review['hash'],quotas=quotas,semantic_accuracy=None,accepted_labels=0,raw_hits_preserved=True,
        human_certified=False,historical_feature_eligible=False,quality_text_access=False,trained_model=False))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=run(a.output)
    print(r['hash']);print(r['body']['totals']);print(r['body']['prior24_diagnostic']);print(r['body']['quotas'])
