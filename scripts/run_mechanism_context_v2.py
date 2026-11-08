"""Design-only structural-context run; isolate reference edits from extractor behavior."""
import argparse
from collections import Counter
import hashlib
from pathlib import Path
from engine.paper_evaluation import require
from engine.store import ROOT
from scripts.run_mechanism_design_extractor import (BASE, INPUTS, REFERENCE, PILOT, VIEWS,
    EXPECTED_REFERENCE, EXPECTED_PILOT, read, persist, locator_diagnostic)
from scripts.mechanism_reference_v3 import run as validate_reference
from scripts.mechanism_design_extractor_v2 import extract


def hash_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def invariant_signature(output):
    return dict(candidates=[{k:v for k,v in c.items() if k!='hits'} | {'hits':[
        {k:h[k] for k in ('start','end','quote')} for h in c['hits']]} for c in output['candidates']],
        proposals=output['proposals'],assessments=output['assessments'],suppressed_proposals=output['suppressed_proposals'])


def check_context(output,view):
    text=view['text'];source={s['path']:s for s in view['spans']}
    pool=output['structural_spans'];byid={s['span_id']:s for s in pool}
    require(len(pool)==len(byid),'Duplicate structural span identity')
    for s in pool:
        require(s['path'] in source,'Unknown source path')
        original=source[s['path']]
        require(all(s[k]==original[k] for k in ('tag','start','end')),'Source structure mismatch')
        require(type(s['start']) is int and type(s['end']) is int and 0<=s['start']<s['end']<=len(text),'Bad context offsets')
        require(text[s['start']:s['end']]==s['quote'],'Context quote mismatch')
    relations=Counter();linked=0
    for c in output['candidates']:
        for hit in c['hits']:
            require(hit['semantic_governance_verified'] is False,'Semantic governance overclaim')
            containers=[s for s in view['spans'] if s['start']<=hit['start']<hit['end']<=s['end']]
            anchor=max(containers,key=lambda s:(s['path'].count('/'),s['start'],-s['end'],s['path'])) if containers else None
            linked+=bool(hit['structural_context'])
            for link in hit['structural_context']+hit['structural_boundaries']:
                require(link['span_id'] in byid,'Unbound context link')
                span=byid[link['span_id']];relation=link['relation'];ancestor=link['ancestor_path']
                if relation in {'containing_text','containing_header'}:
                    require(ancestor is None and span['tag']==relation.removeprefix('containing_'),'Wrong containing relation')
                    require(span['start']<=hit['start']<hit['end']<=span['end'],'Noncontaining context')
                elif relation=='quoted_block_boundary':
                    require(span['tag']=='quoted-block' and span['path']==ancestor,'Wrong quoted boundary')
                    require(anchor is not None and anchor['path'].startswith(ancestor+'/'),'Nonancestor boundary')
                    require(span['start']<=hit['start']<hit['end']<=span['end'],'Noncontaining boundary')
                else:
                    require(relation in {'ancestor_header','ancestor_preceding_direct_text'},'Unknown structural relation')
                    require(isinstance(ancestor,str) and anchor is not None and anchor['path'].startswith(ancestor+'/'),'Nonancestor context')
                    require(span['path'].rsplit('/',1)[0]==ancestor,'Not direct ancestor child')
                    require(span['tag']==('header' if relation=='ancestor_header' else 'text'),'Wrong ancestor tag')
                    branch=ancestor+'/'+anchor['path'][len(ancestor)+1:].split('/',1)[0]
                    branch_spans=[s for s in view['spans'] if s['path']==branch or s['path'].startswith(branch+'/')]
                    require(bool(branch_spans) and span['end']<=min(s['start'] for s in branch_spans),'Nonpreceding ancestor context')
                relations[relation]+=1
    return dict(pool_spans=len(pool),linked_hits=linked,relations=dict(relations))


def run(directory,reference_directory):
    reference_directory=Path(reference_directory).resolve()
    new_envelope=validate_reference(reference_directory);new=new_envelope['body']
    ie,inputs=read(INPUTS);oe,old=read(REFERENCE);pe,pilot=read(PILOT)
    require(oe['hash']==EXPECTED_REFERENCE and pe['hash']==EXPECTED_PILOT,'Frozen identity changed')
    ids=[r['bill_id'] for r in inputs]
    oldrows={r['bill_id']:r for r in old['records']};newrows={r['bill_id']:r for r in new['records']}
    require(len(ids)==len(set(ids))==len(oldrows)==len(newrows)==40 and set(ids)==set(oldrows)==set(newrows),'Design population mismatch')
    design={r['bill_id'] for r in pilot['selection'] if r['partition']=='design'}
    quality={r['bill_id'] for r in pilot['selection'] if r['partition']=='quality'}
    require(set(ids)<=design and set(ids).isdisjoint(quality),'Quality firewall violation')
    baseline=BASE/'mechanism-extractor-design-20261108-v1'
    be,br=read(baseline/'result.json')
    require(be['hash']=='0d350fd1bace59d990908268e71560a3dec87ba2f4df74a8e29eada728508bd8','Wrong baseline')
    paths=[INPUTS,REFERENCE,PILOT,baseline/'result.json',Path(reference_directory)/'corrected-dataset.json',
           Path(reference_directory)/'adjudication.json',Path(reference_directory)/'peer-review.json']
    views=[];baselines={}
    for item in inputs:
        bid=item['bill_id'];path=VIEWS/(bid+'.json');ve,v=read(path)
        require(ve['hash']==item['view_hash']==oldrows[bid]['source_view_hash']==newrows[bid]['source_view_hash'],'View binding mismatch')
        require(all(v[k]==item[k] for k in ('text','spans','source','bill_id')),'Input contents differ')
        bp=baseline/(bid+'.json');ce,cb=read(bp);require(ce['hash']==br['outputs'][bid],'Baseline output binding mismatch')
        paths.extend([path,bp]);views.append(dict(v,view_hash=ve['hash']));baselines[bid]=cb
    code=['scripts/run_mechanism_context_v2.py','scripts/mechanism_design_extractor_v2.py','scripts/mechanism_design_extractor.py',
          'scripts/run_mechanism_design_extractor.py','scripts/mechanism_reference_v3.py','scripts/mechanism_rubric_v2_audit.py',
          'scripts/mechanism_effect_evaluation.py','engine/paper_evaluation.py','engine/store.py']
    files={str(p.relative_to(ROOT)):hash_file(p) for p in paths};codehash={p:hash_file(ROOT/p) for p in code}
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    registration=persist(directory/'registration.json',dict(scope='design_only_structural_context',bill_ids=ids,
        old_reference_hash=oe['hash'],new_reference_hash=new_envelope['hash'],baseline_hash=be['hash'],input_hash=ie['hash'],
        input_files=files,code_sha256=codehash,lexical_changes=False,semantic_matching=False,quality_text_access=False,
        interpretation='Compare exact same triggers under old and revised reference quotes; structural context is not legal entailment'))
    totals=Counter();relations=Counter();outputs={};diagnostics={'old_reference':Counter(),'new_reference':Counter()}
    for v in views:
        bid=v['bill_id'];result=extract(v)
        require(result==extract(v),'Nondeterministic context extraction')
        require(invariant_signature(result)==invariant_signature(baselines[bid]),'Baseline candidates/proposals/statuses changed')
        checked=check_context(result,v);relations.update(checked['relations'])
        totals.update(bills=1,characters=len(v['text']),pool_spans=checked['pool_spans'],linked_hits=checked['linked_hits'],
            candidates=len(result['candidates']),lexical_hits=sum(len(c['hits']) for c in result['candidates']),abstentions=len(result['assessments']))
        for label,refs in [('old_reference',oldrows),('new_reference',newrows)]:
            diag=locator_diagnostic(result,refs[bid],v['text'])
            for counts in diag.values():diagnostics[label].update(counts)
        outputs[bid]=persist(directory/(bid+'.json'),result)['hash']
    require(all(hash_file(ROOT/p)==h for p,h in {**files,**codehash}.items()),'Bound source/code changed')
    return persist(directory/'result.json',dict(registration_hash=registration['hash'],outputs=outputs,totals=dict(totals),
        relations=dict(relations),locator_diagnostics={k:dict(v) for k,v in diagnostics.items()},
        baseline_behavior_unchanged=True,semantic_accuracy=None,human_certified=False,historical_feature_eligible=False,
        accepted_labels=0,quality_text_access=False,trained_model=False))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--reference-directory',type=Path,required=True);a=p.parse_args()
    e=run(a.output,a.reference_directory);print(e['hash']);print(e['body']['totals']);print(e['body']['locator_diagnostics'])
