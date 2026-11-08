"""Design/synthetic effect evaluation conditional on an adjudicated graph.

This module does not judge legal meaning, create compatibility edges, or open
quality texts. Equal quotations/spans are diagnostics, never semantic matches.
"""
from collections import Counter
import re

from engine.paper_evaluation import require, seal, unseal

SCOPES={'synthetic','design'}
STATUSES={'present','absent','uncertain'}
MECHANISMS={'create_programme','authorize','appropriate','tax','prohibit','require','amend','repeal','rename_designate','reporting','deadline','sunset'}
OPERATIONS={'create','expand','restrict','remove','waive','replace','preserve','rename','clarify','uncertain'}
DIMENSIONS={'coverage','amount','duration','authority_scope','procedure','name','existence','text','other'}


def _text(value):
    return isinstance(value,str) and bool(value.strip())


def _identity(value):
    return _text(value) and value==value.strip()


def _submission(envelope):
    body=unseal(envelope)
    require(body.get('scope') in SCOPES,'Only design/synthetic scope is permitted')
    require(isinstance(body.get('records'),list),'Records must be a list')
    bills={};effects={}
    for row in body['records']:
        bid=row['bill_id']
        require(_identity(bid) and bid not in bills,'Invalid or duplicate bill identity')
        require(isinstance(row.get('mechanisms'),dict) and bool(row['mechanisms']),'Mechanism statuses required')
        require(all(k in MECHANISMS and v in STATUSES for k,v in row['mechanisms'].items()),'Invalid mechanism status')
        require(isinstance(row.get('effects'),list),'Effects must be a list')
        bills[bid]=row
        for effect in row['effects']:
            eid=effect['effect_id']
            require(_identity(eid) and eid not in effects,'Invalid or duplicate effect identity')
            require(effect.get('mechanism') in row['mechanisms'],'Effect mechanism is not in bill status map')
            require(row['mechanisms'][effect['mechanism']]=='present','Effects require a present mechanism status')
            require(effect.get('operation') in OPERATIONS and effect.get('dimension') in DIMENSIONS,'Invalid effect operation/dimension')
            require(_text(effect.get('target')),'Effect target missing')
            require(effect.get('actor') is None or _text(effect['actor']),'Invalid actor')
            require(effect.get('conditions') is None or _text(effect['conditions']),'Invalid conditions')
            evidence=effect.get('evidence')
            require(isinstance(evidence,dict),'Effect source evidence required')
            require(isinstance(evidence.get('source_view_hash'),str) and re.fullmatch(r'[0-9a-f]{64}',evidence['source_view_hash']) is not None,'Invalid source view hash')
            start,end=evidence.get('start'),evidence.get('end')
            require(type(start) is int and type(end) is int and 0<=start<end,'Invalid source offsets')
            require(_text(evidence.get('quote')) and len(evidence['quote'])==end-start,'Invalid quote span length')
            effects[eid]=(bid,effect)
        supported={e['mechanism'] for e in row['effects']}
        require(all(v!='present' or k in supported for k,v in row['mechanisms'].items()),'Present mechanism requires a supported effect')
    return body,bills,effects


def maximum_cardinality(prediction_ids, reference_ids, edges):
    """Kuhn augmenting paths; only cardinality is used for feasibility checks."""
    left=set(prediction_ids);right=set(reference_ids)
    adjacency={p:[] for p in left}
    for p,r in sorted(set(edges)):
        if p in left and r in right:adjacency[p].append(r)
    assigned={}
    def augment(p,seen):
        for r in adjacency[p]:
            if r in seen:continue
            seen.add(r)
            if r not in assigned or augment(assigned[r],seen):
                assigned[r]=p
                return True
        return False
    for p in sorted(left):augment(p,set())
    return len(assigned)


def match_effects(prediction_ids, reference_ids, edges):
    """Lexicographically smallest sorted pair list among maximum-size matchings.

    At each prediction in lexical order, prefer the smallest reference whose
    assignment still permits the remaining maximum cardinality. Skipping a
    prediction is allowed only when no such assignment is feasible.
    """
    preds=sorted(prediction_ids);refs=set(reference_ids);edges=set(edges)
    require(len(preds)==len(set(preds)) and len(refs)==len(reference_ids),'Duplicate matching identity')
    require(all(p in preds and r in refs for p,r in edges),'Unknown matching edge endpoint')
    remaining=maximum_cardinality(preds,refs,edges);result=[]
    for index,p in enumerate(preds):
        if remaining==0:break
        later=preds[index+1:]
        for r in sorted(r for a,r in edges if a==p and r in refs):
            possible=maximum_cardinality(later,refs-{r},edges)
            if possible>=remaining-1:
                result.append((p,r));refs.remove(r);remaining-=1
                break
    require(remaining==0,'Matching cardinality invariant failed')
    return result


def _metrics(tp,fp,fn):
    return dict(tp=tp,fp=fp,fn=fn,precision=tp/(tp+fp) if tp+fp else None,
                recall=tp/(tp+fn) if tp+fn else None,
                f1=2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else None)


def _same_span(left,right):
    return all(left['evidence'][k]==right['evidence'][k] for k in ('source_view_hash','start','end','quote'))


def evaluate(predictions,reference,compatibility_graph):
    """Return a sealed, graph-conditional report; no semantic judge is invoked.

    Submissions: {scope, records:[{bill_id, mechanisms:{key:tri_state},
      effects:[{effect_id,mechanism,operation,dimension,actor,target,conditions,
                evidence:{source_view_hash,start,end,quote}}]}]}.
    Graph: {scope,prediction_hash,reference_hash,
      origin:{kind:'synthetic_fixture'|'external_adjudication',adjudicator,method},
      edges:[{bill_id,prediction_id,reference_id}]}.
    All three arguments are seal(body) envelopes. Missing graph edges mean
    incompatibility for this evaluation; graph incompleteness can bias results.
    """
    pred,pb,pe=_submission(predictions);ref,rb,re=_submission(reference)
    graph=unseal(compatibility_graph)
    require(pred['scope']==ref['scope']==graph.get('scope'),'Scope mismatch')
    require(graph.get('prediction_hash')==predictions['hash'] and graph.get('reference_hash')==reference['hash'],'Compatibility graph input binding mismatch')
    require(set(pb)==set(rb),'Prediction/reference bill coverage differs')
    origin=graph.get('origin')
    require(isinstance(origin,dict) and origin.get('kind') in {'synthetic_fixture','external_adjudication'} and
            _text(origin.get('adjudicator')) and _text(origin.get('method')),'Explicit graph origin required')
    require(origin['kind']!='synthetic_fixture' or pred['scope']=='synthetic','Synthetic graph cannot certify design judgments')
    require(isinstance(graph.get('edges'),list),'Compatibility edges must be a list')
    bybill={bid:set() for bid in pb};seen=set()
    for edge in graph['edges']:
        bid,p,r=edge['bill_id'],edge['prediction_id'],edge['reference_id']
        require(p in pe and r in re,'Unknown compatibility endpoint')
        require(bid in pb and pe[p][0]==bid==re[r][0],'Cross-bill compatibility edge')
        require(all(pe[p][1][k]==re[r][1][k] for k in ('mechanism','operation','dimension')),'Incompatible mechanism/operation/dimension edge')
        require((p,r) not in seen,'Duplicate compatibility edge')
        seen.add((p,r));bybill[bid].add((p,r))
    effects=[];statuses=[];total=Counter();confusion=Counter();excluded=[];span_pairs=0;matched_spans=0
    for bid in sorted(pb):
        pr=pb[bid];rr=rb[bid]
        require(set(pr['mechanisms'])==set(rr['mechanisms']),'Mechanism-key coverage differs')
        pids=[e['effect_id'] for e in pr['effects']];rids=[e['effect_id'] for e in rr['effects']]
        pairs=match_effects(pids,rids,bybill[bid]);matchedp={p for p,r in pairs};matchedr={r for p,r in pairs}
        fp=sorted(set(pids)-matchedp);fn=sorted(set(rids)-matchedr)
        total.update(tp=len(pairs),fp=len(fp),fn=len(fn))
        localspan=sum(_same_span(pe[p][1],re[r][1]) for p in pids for r in rids)
        localmatched=sum(_same_span(pe[p][1],re[r][1]) for p,r in pairs)
        span_pairs+=localspan;matched_spans+=localmatched
        effects.append(dict(bill_id=bid,matched_pairs=[dict(prediction_id=p,reference_id=r) for p,r in pairs],
            unmatched_prediction_ids=fp,unmatched_reference_ids=fn,metrics=_metrics(len(pairs),len(fp),len(fn)),
            span_diagnostic=dict(equal_span_pairs=localspan,equal_span_matched_pairs=localmatched)))
        for mechanism in sorted(pr['mechanisms']):
            expected=rr['mechanisms'][mechanism];actual=pr['mechanisms'][mechanism]
            confusion[(expected,actual)]+=1
            if expected=='uncertain':
                excluded.append(dict(bill_id=bid,mechanism=mechanism,prediction=actual,reason='Reference status uncertain'))
                continue
            classification=('tp' if actual=='present' else 'fn') if expected=='present' else ('fp' if actual=='present' else 'tn' if actual=='absent' else 'abstain_negative')
            statuses.append(dict(bill_id=bid,mechanism=mechanism,reference=expected,prediction=actual,classification=classification))
    counts=Counter(s['classification'] for s in statuses)
    result=dict(scope=pred['scope'],prediction_hash=predictions['hash'],reference_hash=reference['hash'],
        compatibility_graph_hash=compatibility_graph['hash'],graph_origin=origin,
        matching_rule='One-to-one maximum cardinality; lexicographically smallest sorted prediction/reference pair list among maxima',
        effect_metrics=_metrics(total['tp'],total['fp'],total['fn']),effect_results=effects,
        span_diagnostic=dict(equal_span_pairs=span_pairs,equal_span_matched_pairs=matched_spans,
            interpretation='Exact shared source coordinates and quote only; never determines compatibility or semantic correctness'),
        status_evaluation=dict(records=statuses,counts={k:counts[k] for k in ('tp','fp','fn','tn','abstain_negative')},
            positive_metrics=_metrics(counts['tp'],counts['fp'],counts['fn']),
            confusion=[dict(reference=a,prediction=b,count=confusion[(a,b)]) for a in sorted(STATUSES) for b in sorted(STATUSES)],
            excluded_reference_uncertain=excluded,excluded_count=len(excluded),
            policy='Reference uncertain excluded from scored statuses. Predicted uncertain on reference present is FN; on reference absent is explicit abstention, not TN.'),
        source_content_verified=False,
        source_integrity_note='Evidence coordinates and lengths are structurally checked; no source view contents are supplied or verified here.',
        human_certified=False,historical_feature_eligible=False,semantic_accuracy_verified=False,independent_validation=False,
        interpretation='Counts are conditional on externally supplied compatibility judgments and reference completeness. They are not independently established semantic accuracy; shared spans do not establish actor, direction, negation or legal effect.')
    return seal(result)
