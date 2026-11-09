"""Registered structural-boundary diagnostic; never fits or promotes a model."""
import argparse
import sys
from collections import Counter
from pathlib import Path
from engine.paper_evaluation import require
from engine.store import ROOT,digest
from scripts.run_mechanism_design_extractor import BASE,INPUTS,PILOT,VIEWS,EXPECTED_PILOT,read,persist
from scripts.run_bill_readiness_audit_v2 import population,authenticate_source,sha,INPUT_HASH
from scripts.run_bill_structural_input_v1 import CODE as STRUCTURAL_CODE
from scripts.run_mechanism_validity_v5 import CODE as BASE_CODE
from scripts.run_mechanism_expansion_v3 import REFERENCE,REFERENCE_HASH,hit_map
from scripts.run_mechanism_context_filter import audit_decisions
from scripts.mechanism_validity_guard import validate_reference,validate_output
from scripts.mechanism_design_extractor import MECHANISMS
from scripts.bill_structural_input_v1 import validate
from scripts.mechanism_structural_extractor_v1 import extract

SIDE=BASE/'structural-input-v1-20261108'
OLD=BASE/'mechanism-validity-v5-20261108'
SIDE_HASH='f3505ea7c8618d686c0401790130ad619c0c73a0812fca21e05a0559706c3bb0'
OLD_HASH='e75c04b8b4b29e4e9665c3b91cfee3699ee4d5789edd99154daf7fbbbe3cfb79'
CODE=sorted(set(STRUCTURAL_CODE+BASE_CODE+['scripts/run_mechanism_structural_v1.py',
    'scripts/mechanism_structural_extractor_v1.py','tests/test_mechanism_structural_extractor_v1.py',
    'tests/test_mechanism_structural_independent.py']))


def metrics(reference, baseline, prior, decisions):
    hits=hit_map(baseline)
    by={m:Counter(dict(raw_hits=0,boundary_usable=0,boundary_flagged=0,prior_retained=0,combined_retained=0,
        reference_effects=0,raw_overlap=0,boundary_overlap=0,prior_retained_overlap=0,combined_overlap=0)) for m in MECHANISMS}
    usable={(d['identity']['mechanism'],d['identity']['start'],d['identity']['end']) for d in decisions if d['decision']=='retain'}
    require(len(decisions)==len(hits) and {(d['identity']['mechanism'],d['identity']['start'],d['identity']['end']) for d in decisions}==set(hits),'Decision identity coverage')
    for k in hits:
        c=by[k[0]]; c['raw_hits']+=1;c['boundary_usable']+=int(k in usable);c['boundary_flagged']+=int(k not in usable)
        c['prior_retained']+=int(prior[k]['status']=='retain');c['combined_retained']+=int(k in usable and prior[k]['status']=='retain')
    effects=[]
    for i,e in enumerate(reference['effects']):
        matched={k for k in hits if k[0]==e['mechanism'] and k[1]<e['end'] and e['start']<k[2]}
        retained={k for k in matched if prior[k]['status']=='retain'}
        row=dict(effect_index=i,mechanism=e['mechanism'],raw_overlap=bool(matched),boundary_overlap=bool(matched&usable),
                 prior_retained_overlap=bool(retained),combined_overlap=bool(retained&usable))
        by[e['mechanism']]['reference_effects']+=1
        for k in ('raw_overlap','boundary_overlap','prior_retained_overlap','combined_overlap'):by[e['mechanism']][k]+=int(row[k])
        effects.append(row)
    return {m:dict(c) for m,c in by.items()},effects


def run(directory):
    ie,inputs=read(INPUTS);pe,pilot=read(PILOT);re,reference=read(REFERENCE)
    se,sr=read(SIDE/'result.json');oe,old=read(OLD/'result.json')
    require((ie['hash'],pe['hash'],re['hash'],se['hash'],oe['hash'])==(INPUT_HASH,EXPECTED_PILOT,REFERENCE_HASH,SIDE_HASH,OLD_HASH),'Frozen bindings changed')
    ids=population(inputs,pilot);refs={r['bill_id']:r for r in reference['records']}
    require(set(ids)==set(refs)==set(sr['outputs'])==set(old['outputs'])==set(old['filters']),'Population mismatch')
    paths=[INPUTS,PILOT,REFERENCE,SIDE/'result.json',OLD/'result.json'];loaded={};views={}
    for item in inputs:
        bid=item['bill_id'];vp=VIEWS/(bid+'.json');sp=SIDE/(bid+'.json');op=OLD/(bid+'.json');fp=OLD/(bid+'-filter.json')
        ve,v=read(vp);sce,side=read(sp);be,baseline=read(op);fe,prior=read(fp)
        require(ve['hash']==item['view_hash']==refs[bid]['source_view_hash']==baseline['source_view_hash'],'View binding')
        require(sce['hash']==sr['outputs'][bid] and be['hash']==old['outputs'][bid] and fe['hash']==old['filters'][bid],'Output binding')
        require(all(v[k]==item[k] for k in ('bill_id','text','spans','source')),'View altered')
        rp=PILOT.parent/'sources'/(sha(v['source']['url'].encode())+'.raw');raw=rp.read_bytes();authenticate_source(v['source'],raw)
        validate(side,raw,bid,v,ve['hash']);view=dict(v,view_hash=ve['hash']);validate_output(view,baseline)
        decisions=audit_decisions(prior,baseline,view)
        views[bid]=view;loaded[bid]=(view,side,baseline,decisions);paths.extend([vp,sp,op,fp,rp])
    validate_reference(reference,views)
    files={str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in paths};code={p:sha((ROOT/p).read_bytes()) for p in CODE}
    directory=Path(directory).resolve();require(ROOT/'data' in directory.parents,'Runtime output required');directory.mkdir(parents=True,exist_ok=True)
    reg=persist(directory/'registration.json',dict(version='structural-boundary-diagnostic-v1',bill_ids=ids,input_files=files,code_sha256=code,
        python_version=sys.version,reference_hash=re['hash'],baseline_hash=oe['hash'],structural_input_hash=se['hash'],
        hypothesis='Cell boundary guards prevent concatenation-derived locators while full text and fraction context remain available; all losses and null results reported',
        configuration='Frozen v5 lexical rules; every raw hit retained; strictly interior cell edges flag usability; no numeric normalization or semantic labels',
        metrics='Same-mechanism half-open quotation overlap, boundary usability, and conjunction with frozen filter-v3 retain status; not semantic accuracy',
        review='All40 source/decision mappings, all boundary-flagged cases and every table/fraction-associated hit; no outcome-guided sampling',
        budget='One fixed40 exposed-design run, deterministic replays only; no substitutions or post-result tuning',
        quality_access=False,model_fitting=False,historical_feature_eligible=False))
    outputs={};per_bill=[];totals=Counter();categories={m:Counter() for m in MECHANISMS};review_cases=[]
    for bid in ids:
        view,side,baseline,prior=loaded[bid];before=(digest(view),digest(side));result=extract(view,side)
        require(result==extract(view,side) and before==(digest(view),digest(side)),'Mutation/nondeterminism')
        require(result['raw_output']==baseline,'Raw baseline changed')
        cats,effects=metrics(refs[bid],baseline,prior,result['boundary_decisions'])
        counts=Counter()
        for m,c in cats.items():categories[m].update(c);counts.update(c)
        totals.update(counts)
        per_bill.append(dict(bill_id=bid,counts=dict(counts),by_mechanism=cats,effects=effects))
        outputs[bid]=persist(directory/(bid+'.json'),result)['hash']
        for d in result['boundary_decisions']:
            if d['decision']!='retain' or d['containing_cell_paths'] or d['intersecting_cell_paths'] or d['fraction_context']:
                review_cases.append(dict(bill_id=bid,decision=d))
    require(all(sha((ROOT/p).read_bytes())==h for p,h in {**files,**code}.items()),'Frozen bytes changed')
    return persist(directory/'result.json',dict(registration_hash=reg['hash'],outputs=outputs,per_bill=per_bill,totals=dict(totals),
        by_mechanism={m:dict(c) for m,c in categories.items()},review_cases=review_cases,accepted_labels=0,model_fitting=False,
        quality_access=False,historical_feature_eligible=False,semantic_accuracy=None,predictive_accuracy=None))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    r=run(p.parse_args().output);print(r['hash']);print(r['body']['totals'])
