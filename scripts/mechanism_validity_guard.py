"""Strict composition boundary for provisional design artifacts.

Checks source identity, structure and internal consistency, never legal meaning.
Existing sealed modules are deliberately unchanged; call these before consuming
an extractor/reference in new experiments or semantic evaluation.
"""
import hashlib
import re
from collections import Counter
from engine.paper_evaluation import require,unseal,seal
from scripts.mechanism_design_extractor import MECHANISMS
from scripts.mechanism_effect_evaluation import OPERATIONS,DIMENSIONS,_submission
from scripts.run_mechanism_context_v2 import check_context

EFFECT_FIELDS={'mechanism','operation','dimension','actor','target','conditions','quote','start','end','rationale'}
RECORD_FIELDS={'bill_id','source_view_hash','summary','mechanisms','uncertainties','unresolved_effects','effects'}


def nonempty(value):
    return isinstance(value,str) and bool(value.strip())


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def quote(item,text):
    a,b=item.get('start'),item.get('end')
    require(type(a) is int and type(b) is int and 0<=a<b<=len(text),'Invalid exact quote offsets')
    require(nonempty(item.get('quote')) and text[a:b]==item['quote'],'Exact source quote mismatch')


def validate_view(view):
    require(isinstance(view,dict) and nonempty(view.get('bill_id')) and isinstance(view.get('text'),str),'Invalid source view')
    require(isinstance(view.get('view_hash'),str) and re.fullmatch('[0-9a-f]{64}',view['view_hash']) is not None,'Bound view hash required')
    spans=view.get('spans');require(isinstance(spans,list) and bool(spans),'Source spans required')
    seen={};text=view['text']
    for s in spans:
        require(isinstance(s,dict),'Invalid source span')
        path=s.get('path');require(isinstance(path,str) and re.fullmatch(r'(?:/[^/\s\[\]]+\[[1-9][0-9]*\])+',path) is not None,'Invalid absolute indexed source path')
        require(path not in seen,'Duplicate source path');seen[path]=s
        require(path.rsplit('/',1)[1].rsplit('[',1)[0]==s.get('tag'),'Path/tag mismatch')
        a,b=s.get('start'),s.get('end')
        require(type(a) is int and type(b) is int and 0<=a<=b<=len(text),'Invalid source span bounds')
        require(s.get('text_sha256')==sha(text[a:b]),'Source span hash mismatch')
    for path,s in seen.items():
        for ancestor,p in seen.items():
            if path.startswith(ancestor+'/'):
                require(p['start']<=s['start']<=s['end']<=p['end'],'Ancestor bounds mismatch')
    for i,s in enumerate(spans):
        for p in spans[i+1:]:
            if max(s['start'],p['start'])<min(s['end'],p['end']):
                require(s['path'].startswith(p['path']+'/') or p['path'].startswith(s['path']+'/'),'Overlapping unrelated source nodes')
    # Hash authenticity is supplied by the caller's unseal+registered-hash check;
    # a well-formed hash string alone is never proof of provenance.


def validate_output(view,output):
    validate_view(view);text=view['text'];spans={s['path']:s for s in view['spans']}
    require(output.get('bill_id')==view['bill_id'] and output.get('source_view_hash')==view['view_hash'],'Output source/bill binding mismatch')
    require(output.get('input_text_sha256')==sha(text),'Output text binding mismatch')
    require(all(output.get(k) is False for k in ('human_certified','historical_feature_eligible','trained_model')),'Extractor certification overclaim')
    require(type(output.get('accepted_v2_labels_created')) is int and output['accepted_v2_labels_created']==0,'Accepted label overclaim')
    coverage=output.get('coverage',{})
    require(type(coverage.get('characters_supplied')) is int and coverage['characters_supplied']==len(text),'Supplied length claim mismatch')
    require(type(coverage.get('characters_scanned')) is int and coverage['characters_scanned']==len(text),'Scan length claim mismatch')
    require(coverage.get('scan_ranges')==[[0,len(text)]] and coverage.get('input_view_scanned_completely') is True and coverage.get('truncated') is False,'Scan coverage claim mismatch')
    require(coverage.get('source_document_completeness_verified') is False,'Source completeness unverified')
    require(type(coverage.get('span_count')) is int and coverage['span_count']==len(view['spans']),'Span count claim mismatch')
    candidates=output.get('candidates');require(isinstance(candidates,list),'Candidates required')
    ids=set();hits=set();groups=set();counts=Counter()
    for c in candidates:
        require(nonempty(c.get('candidate_id')) and c['candidate_id'] not in ids,'Duplicate/invalid candidate ID');ids.add(c['candidate_id'])
        m=c.get('mechanism');require(m in MECHANISMS,'Unknown mechanism');counts[m]+=1
        require(c.get('interpretation_status')=='unreviewed_locator','Candidate semantic promotion')
        quote(c,text);path=c.get('context_path');group=(path,m)
        require(group not in groups,'Duplicate context/mechanism candidate');groups.add(group)
        if path=='__document__':
            require(c['start']==0 and c['end']==len(text) and c['context_tag']=='document','Invalid document context')
        else:
            require(path in spans and all(c[k]==spans[path][k] for k in ('start','end')) and c['context_tag']==spans[path]['tag'],'Candidate structural context mismatch')
        require(isinstance(c.get('hits'),list) and bool(c['hits']),'Empty candidate')
        for h in c['hits']:
            quote(h,text);key=(m,h['start'],h['end']);require(key not in hits,'Duplicate hit');hits.add(key)
            require(c['start']<=h['start']<h['end']<=c['end'],'Hit outside candidate context')
    assessments=output.get('assessments');require(isinstance(assessments,dict) and set(assessments)==set(MECHANISMS),'Incomplete assessment coverage')
    for m,a in assessments.items():
        require(a.get('status')=='abstain' and nonempty(a.get('reason')),'Assessment semantic promotion')
        require(type(a.get('candidate_count')) is int and a['candidate_count']==counts[m],'Candidate count mismatch')
    byid={c['candidate_id']:c for c in candidates};proposal_ids=set()
    require(isinstance(output.get('proposals'),list),'Proposal collection required')
    quarantined=output.get('legacy_proposals',[])
    require(isinstance(quarantined,list),'Invalid quarantine collection')
    for item in quarantined:
        require(set(item)=={'proposal','quarantine_reason'} and nonempty(item['quarantine_reason']),'Invalid quarantine record')
    if quarantined:
        require(output['proposals']==[],'Quarantined output cannot activate suggestions')
    for p in output['proposals']+[item['proposal'] for item in quarantined]:
        require(nonempty(p.get('proposal_id')) and p['proposal_id'] not in proposal_ids,'Duplicate proposal');proposal_ids.add(p['proposal_id'])
        require(p.get('candidate_id') in byid,'Unbound proposal');c=byid[p['candidate_id']]
        require(p.get('suggested_operation') in OPERATIONS and p.get('suggested_dimension') in DIMENSIONS,'Invalid proposal dimensions')
        require(p.get('mechanism')==c['mechanism'],'Proposal mechanism mismatch');quote(p,text)
        require(c['start']<=p['start']<p['end']<=c['end'],'Proposal outside candidate')
        require(p.get('interpretation_status')=='unvalidated_rule_supported_suggestion' and p.get('requires_full_context_review') is True,'Proposal semantic promotion')
    check_context(output,view)
    return dict(candidates=len(candidates),hits=len(hits),proposals=len(output['proposals']),quarantined_proposals=len(quarantined),assessments=len(assessments))


def validate_reference(reference_body,views_by_bill):
    require(reference_body.get('human_certified') is False and reference_body.get('historical_feature_eligible') is False,'Reference certification overclaim')
    require(reference_body.get('semantic_accuracy_verified',False) is False,'Reference semantic certification overclaim')
    rows=reference_body.get('records');require(isinstance(rows,list),'Reference records required')
    ids=[r['bill_id'] for r in rows];require(len(ids)==len(set(ids)) and set(ids)==set(views_by_bill),'Reference bill coverage mismatch')
    counts=Counter()
    for row in rows:
        require(set(row)==RECORD_FIELDS,'Reference record schema mismatch')
        v=views_by_bill[row['bill_id']];validate_view(v)
        require(v['bill_id']==row['bill_id'] and row['source_view_hash']==v['view_hash'],'Reference source binding mismatch')
        require(nonempty(row['summary']),'Missing bill summary')
        statuses=row['mechanisms'];require(set(statuses)==set(MECHANISMS) and all(s in {'present','absent','uncertain'} for s in statuses.values()),'Reference status coverage mismatch')
        require(set(row['uncertainties'])=={m for m,s in statuses.items() if s=='uncertain'} and all(nonempty(s) for s in row['uncertainties'].values()),'Uncertainty explanation mismatch')
        require(isinstance(row['unresolved_effects'],list),'Unresolved list required')
        for item in row['unresolved_effects']:
            require(item['mechanism'] in MECHANISMS and statuses[item['mechanism']]!='absent' and nonempty(item['reason']),'Unresolved effect conflict')
        observed=set();seen=set()
        for e in row['effects']:
            require(set(e)==EFFECT_FIELDS,'Effect schema mismatch')
            require(e['mechanism'] in MECHANISMS and statuses[e['mechanism']]=='present','Effect/status conflict')
            require(e['operation'] in OPERATIONS and e['dimension'] in DIMENSIONS,'Invalid effect dimensions')
            require(nonempty(e['target']) and nonempty(e['rationale']) and all(e[k] is None or nonempty(e[k]) for k in ('actor','conditions')),'Incomplete effect')
            quote(e,v['text']);observed.add(e['mechanism']);counts['effects']+=1
            signature=tuple((k,str(e[k])) for k in sorted(e));require(signature not in seen,'Duplicate exact effect');seen.add(signature)
        require(observed=={m for m,s in statuses.items() if s=='present'},'Present status without effect')
        counts['bills']+=1;counts['statuses']+=len(statuses)
    return dict(counts)


def validate_semantic_sources(prediction_envelope,reference_envelope,views_by_hash):
    """Validate exact semantic-evaluator evidence before graph-conditional scoring.

    External compatibility judgments are still required. No actor/target/meaning
    equivalence is inferred from matching quotations or source identity.
    """
    for envelope in (prediction_envelope,reference_envelope):
        body,_,_=_submission(envelope)
        require(body.get('scope') in {'design','synthetic'},'Only design/synthetic source validation')
        require(all(body.get(k,False) is False for k in ('human_certified','historical_feature_eligible','semantic_accuracy_verified')),'Semantic certification overclaim')
        require(all(h==v.get('view_hash') for h,v in views_by_hash.items()),'Source manifest key mismatch')
        bybill={v['bill_id']:v for v in views_by_hash.values()}
        require(len(bybill)==len(views_by_hash),'Ambiguous source manifest')
        require({r['bill_id'] for r in body['records']}==set(bybill),'Semantic population differs from source manifest')
        for row in body['records']:
            validate_view(bybill[row['bill_id']])
            require(set(row['mechanisms'])==set(MECHANISMS),'Incomplete semantic mechanism coverage')
            for effect in row['effects']:
                require({'effect_id','mechanism','operation','dimension','actor','target','conditions','evidence'}<=set(effect),'Missing semantic effect fields')
                evidence=effect['evidence'];h=evidence['source_view_hash'];require(h in views_by_hash,'Unknown semantic evidence source')
                view=views_by_hash[h];validate_view(view)
                require(view['view_hash']==h and view['bill_id']==row['bill_id'],'Cross-bill semantic evidence')
                quote(evidence,view['text'])


def evaluate_guarded(predictions,reference,compatibility_graph,views_by_hash):
    """Source-bound design/synthetic scoring, still conditional on external graph."""
    from scripts.mechanism_effect_evaluation import evaluate
    validate_semantic_sources(predictions,reference,views_by_hash)
    result=unseal(evaluate(predictions,reference,compatibility_graph))
    result['source_content_verified']=True
    result['source_integrity_note']='Exact evidence checked against supplied source manifest; caller must authenticate registered source envelopes. Historical identity and semantic compatibility are not established.'
    result['source_manifest_hashes']=sorted(views_by_hash)
    return seal(result)
