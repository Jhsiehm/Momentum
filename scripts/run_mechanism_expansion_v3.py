"""Fixed-design lexical expansion experiment; quote locators are not semantic labels."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from engine.paper_evaluation import require
from engine.store import ROOT
from scripts.run_mechanism_design_extractor import BASE,INPUTS,PILOT,VIEWS,EXPECTED_PILOT,read,persist
from scripts.run_mechanism_context_v2 import check_context,hash_file
from scripts.mechanism_design_extractor import MECHANISMS
from scripts.mechanism_design_extractor_v3 import extract,RULES

BASELINE=BASE/'mechanism-context-v2-20261108'
REFERENCE=BASE/'mechanism-reference-v3-20261108/corrected-dataset.json'
REFERENCE_HASH='8d6da3e94e901c953334548d60617112fe8ea3408219d6e6d4b9d009a2805bd5'
BASELINE_HASH='82c28b7f07e49b7f6ea963951cb8dc0139caf3b7f0e8ea6e26fc99aa93e1ba0e'


def hit_map(output):
    result={}
    for candidate in output['candidates']:
        for hit in candidate['hits']:
            key=(candidate['mechanism'],hit['start'],hit['end'])
            require(key not in result,'Duplicate hit identity')
            result[key]=(candidate,hit)
    return result


def compare(baseline,expanded,reference,text):
    old,new=hit_map(baseline),hit_map(expanded)
    require(set(old)<=set(new),'Expansion lost baseline hits')
    require(expanded['proposals']==baseline['proposals'] and expanded['suppressed_proposals']==baseline['suppressed_proposals'],'Proposal behavior changed')
    require(set(expanded['assessments'])==set(MECHANISMS),'Assessment coverage changed')
    candidates={c['candidate_id']:c for c in expanded['candidates']}
    require(len(candidates)==len(expanded['candidates']),'Duplicate candidate identity')
    for candidate in baseline['candidates']:
        require(candidate['candidate_id'] in candidates,'Baseline candidate lost')
        current=candidates[candidate['candidate_id']]
        require(all(current.get(k)==v for k,v in candidate.items() if k!='hits'),'Baseline candidate context changed')
    for key,(_,hit) in old.items():
        require(all(new[key][1].get(k)==v for k,v in hit.items()),'Baseline hit structure changed')
    for m,assessment in expanded['assessments'].items():
        require(assessment['candidate_count']==sum(c['mechanism']==m for c in expanded['candidates']),'Incorrect candidate count')
    require(all(r['status']=='abstain' for r in expanded['assessments'].values()),'Semantic decision created')
    require(expanded['accepted_v2_labels_created']==0 and expanded['human_certified'] is False and expanded['historical_feature_eligible'] is False and expanded['trained_model'] is False,'Certification overclaim')
    for key,(candidate,hit) in new.items():
        require(type(hit['start']) is int and type(hit['end']) is int and 0<=hit['start']<hit['end']<=len(text),'Invalid hit offsets')
        require(text[hit['start']:hit['end']]==hit['quote'],'Hit quote mismatch')
        require(text[candidate['start']:candidate['end']]==candidate['quote'],'Candidate quote mismatch')
        require(candidate['start']<=hit['start']<hit['end']<=candidate['end'],'Hit outside review context')
    before=[];after=[];counts={m:Counter() for m in MECHANISMS}
    for index,e in enumerate(reference['effects']):
        require(text[e['start']:e['end']]==e['quote'],'Reference quote mismatch')
        m=e['mechanism'];a,b=e['start'],e['end']
        oldhit=any(k[0]==m and k[1]<b and a<k[2] for k in old)
        newhit=any(k[0]==m and k[1]<b and a<k[2] for k in new)
        if oldhit:before.append(index)
        if newhit:after.append(index)
        counts[m].update(reference_effects=1,baseline_overlap=int(oldhit),expanded_overlap=int(newhit),
                         recovered=int(newhit and not oldhit),lost=int(oldhit and not newhit))
    added=[]
    for key in sorted(set(new)-set(old)):
        candidate,hit=new[key]
        overlaps=any(e['mechanism']==key[0] and e['start']<key[2] and key[1]<e['end'] for e in reference['effects'])
        added.append(dict(mechanism=key[0],start=key[1],end=key[2],quote=hit['quote'],rule_ids=hit['rule_ids'],
                          candidate_id=candidate['candidate_id'],intersects_reference_quote=overlaps))
    return dict(by_mechanism={m:dict(c) for m,c in counts.items()},
        recovered_effect_indices=sorted(set(after)-set(before)),lost_effect_indices=sorted(set(before)-set(after)),
        added_hits=added,added_hits_outside_reference_quotes=sum(not h['intersects_reference_quote'] for h in added),
        added_candidates=len(expanded['candidates'])-len(baseline['candidates']))


def sample_key(row):
    return hashlib.sha256(json.dumps([row['bill_id'],row['mechanism'],row['start'],row['end']],separators=(',',':')).encode()).hexdigest()


def run(directory):
    re,reference=read(REFERENCE);be,baseline=read(BASELINE/'result.json');ie,inputs=read(INPUTS);pe,pilot=read(PILOT)
    require(re['hash']==REFERENCE_HASH and be['hash']==BASELINE_HASH and pe['hash']==EXPECTED_PILOT,'Frozen binding mismatch')
    refs={r['bill_id']:r for r in reference['records']};ids=[i['bill_id'] for i in inputs]
    require(len(ids)==len(set(ids))==len(refs)==len(reference['records'])==40 and set(ids)==set(refs)==set(baseline['outputs']),'Population mismatch')
    design={r['bill_id'] for r in pilot['selection'] if r['partition']=='design'};quality={r['bill_id'] for r in pilot['selection'] if r['partition']=='quality'}
    require(set(ids)<=design and set(ids).isdisjoint(quality),'Quality firewall violation')
    paths=[REFERENCE,BASELINE/'result.json',INPUTS,PILOT];views=[];old={}
    for item in inputs:
        bid=item['bill_id'];vp=VIEWS/(bid+'.json');ve,v=read(vp);bp=BASELINE/(bid+'.json');oe,o=read(bp)
        require(ve['hash']==item['view_hash']==refs[bid]['source_view_hash']==o['source_view_hash'],'View binding mismatch')
        require(all(item[k]==v[k] for k in ('bill_id','text','spans','source')),'View content mismatch')
        require(oe['hash']==baseline['outputs'][bid],'Baseline output mismatch')
        paths.extend([vp,bp]);views.append(dict(v,view_hash=ve['hash']));old[bid]=o
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    code=['scripts/run_mechanism_expansion_v3.py','scripts/mechanism_design_extractor_v3.py','scripts/mechanism_design_extractor_v2.py',
          'scripts/mechanism_design_extractor.py','scripts/run_mechanism_context_v2.py','scripts/run_mechanism_design_extractor.py',
          'scripts/mechanism_reference_v3.py','scripts/mechanism_rubric_v2_audit.py','scripts/mechanism_effect_evaluation.py',
          'engine/paper_evaluation.py','engine/store.py','tests/test_mechanism_design_extractor_v3.py','tests/test_mechanism_expansion_contrasts.py',
          'tests/test_mechanism_expansion_runner.py']
    files={str(p.relative_to(ROOT)):hash_file(p) for p in paths};codes={p:hash_file(ROOT/p) for p in code}
    registration=persist(directory/'registration.json',dict(scope='exploratory_design_locator_expansion',bill_ids=ids,
        reference_hash=re['hash'],baseline_hash=be['hash'],input_hash=ie['hash'],input_files=files,code_sha256=codes,
        rules=RULES,review_sampling='First24 added unique mechanism/start/end hits ordered by SHA256 compactJSON[bill_id,mechanism,start,end]',
        tuning_disclosure='Rules and contrast fixtures informed by prior design error reviews; not held-out evaluation',
        semantic_matching=False,quality_text_access=False,model_fitting=False))
    totals=Counter();per_mechanism={m:Counter() for m in MECHANISMS};outputs={};comparisons=[];added=[]
    for v in views:
        bid=v['bill_id'];result=extract(v);require(result==extract(v),'Nondeterministic expansion')
        context=check_context(result,v);comparison=compare(old[bid],result,refs[bid],v['text']);comparison['bill_id']=bid
        comparisons.append(comparison);added.extend(dict(bill_id=bid,source_view_hash=v['view_hash'],**h) for h in comparison['added_hits'])
        for m,counts in comparison['by_mechanism'].items():per_mechanism[m].update(counts)
        totals.update(bills=1,characters=len(v['text']),candidates=len(result['candidates']),hits=len(hit_map(result)),
            added_candidates=comparison['added_candidates'],added_hits=len(comparison['added_hits']),
            added_hits_outside_reference_quotes=comparison['added_hits_outside_reference_quotes'],
            linked_hits=context['linked_hits'],abstentions=len(result['assessments']),unvalidated_suggestions=len(result['proposals']))
        outputs[bid]=persist(directory/(bid+'.json'),result)['hash']
    sample=persist(directory/'review-sample.json',dict(registration_hash=registration['hash'],records=sorted(added,key=sample_key)[:24],
        interpretation='Exploratory added-hit review; not semantic accuracy or reference certification'))
    require(all(hash_file(ROOT/p)==h for p,h in {**files,**codes}.items()),'Frozen source/code changed')
    return persist(directory/'result.json',dict(registration_hash=registration['hash'],outputs=outputs,totals=dict(totals),
        by_mechanism={m:dict(c) for m,c in per_mechanism.items()},comparisons=comparisons,review_sample_hash=sample['hash'],
        semantic_accuracy=None,precision=None,human_certified=False,historical_feature_eligible=False,accepted_labels=0,
        quality_text_access=False,trained_model=False,interpretation='Quote-trigger intersections and review workload only; outside-reference hits are not false positives'))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=run(a.output)
    print(r['hash']);print(r['body']['totals']);print(r['body']['by_mechanism'])
