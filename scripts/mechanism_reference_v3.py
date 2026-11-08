"""Apply eight source-reviewed design amendments in a separate provisional version."""
import argparse
import copy
import hashlib
from pathlib import Path
from engine.paper_evaluation import require
from scripts.run_mechanism_design_extractor import read, persist, BASE, REFERENCE, EXPECTED_REFERENCE, VIEWS
from scripts.mechanism_rubric_v2_audit import check_quote, nonempty
from scripts.mechanism_effect_evaluation import OPERATIONS, DIMENSIONS

QUESTIONS={('114-s1259',15),('115-s284',4),('117-s825',6),('117-hr5229',16),
           ('116-s1076',9),('116-s1076',13),('116-s1076',22),('117-hr1597',37)}


def indexed(items):
    result={}
    for row in items:
        require(isinstance(row['bill_id'],str) and type(row['effect_index']) is int,'Invalid question identity')
        key=(row['bill_id'],row['effect_index'])
        require(key not in result,'Duplicate question')
        result[key]=row
    require(set(result)==QUESTIONS,'Incomplete or out-of-scope question set')
    return result


def apply_decisions(parent, adjudication, peer, views):
    for body in (adjudication,peer):
        require(body.get('human_certified') is False and body.get('historical_feature_eligible') is False,'Certification overclaim')
    decisions=indexed(adjudication['decisions']);reviews=indexed(peer['decisions'])
    output=copy.deepcopy(parent)
    rows={r['bill_id']:r for r in output['records']}
    require(len(rows)==len(output['records']),'Duplicate parent bill')
    changes=[]
    for key,d in decisions.items():
        bid,index=key; original=rows[bid]['effects'][index]; after=d['after']; text=views[bid]['text']
        require(d['before']==original,'Before effect does not match parent')
        require(set(after)==set(original),'Effect schema changed')
        require(after['mechanism']==original['mechanism'],'Mechanism change outside question scope')
        require(after['operation'] in OPERATIONS and after['dimension'] in DIMENSIONS,'Invalid effect enums')
        require(nonempty(after['target']) and nonempty(after['rationale']),'Missing effect explanation')
        require(all(after[k] is None or nonempty(after[k]) for k in ('actor','conditions')),'Invalid actor/conditions')
        check_quote(after,text)
        require(d['disposition'] in {'correct','retain','uncertain'} and nonempty(d['rationale']),'Invalid adjudication')
        require(bool(d['evidence']),'Missing adjudication evidence')
        for span in d['evidence']:check_quote(span,text)
        r=reviews[key]
        require(r['disposition'] in {'agree','challenge','uncertain'} and nonempty(r['rationale']),'Invalid peer disposition')
        check_quote(r['evidence'],text)
        # No disputed change can silently become an accepted reference amendment.
        require(r['disposition']=='agree','Peer disagreement requires a separately resolved adjudication')
        require(d['disposition']!='uncertain','Unresolved question cannot be applied')
        require((after==original)==(d['disposition']=='retain'),'Change/disposition mismatch')
        rows[bid]['effects'][index]=copy.deepcopy(after)
        if after!=original:changes.append({'bill_id':bid,'effect_index':index,'changed_fields':sorted(k for k in original if original[k]!=after[k])})
    return output,changes


def run(directory):
    directory=Path(directory)
    pe,parent=read(REFERENCE);ae,a=read(directory/'adjudication.json');re,r=read(directory/'peer-review.json')
    require(pe['hash']==EXPECTED_REFERENCE==a['parent_reference_hash'],'Parent binding mismatch')
    require(r['adjudication_hash']==ae['hash'],'Peer adjudication binding mismatch')
    views={}
    for row in parent['records']:
        ve,v=read(VIEWS/(row['bill_id']+'.json'))
        require(ve['hash']==row['source_view_hash'],'Source view binding mismatch');views[row['bill_id']]=v
    output,changes=apply_decisions(parent,a,r,views)
    # Do not retain upstream metadata implying this new layer was certified by old reviews.
    body=dict(purpose='Agent-adjudicated design reference v3; provisional, not predictive-ready ground truth',
        parent_reference_hash=pe['hash'],adjudication_hash=ae['hash'],peer_review_hash=re['hash'],
        records=output['records'],changes=changes,human_certified=False,historical_feature_eligible=False,
        semantic_accuracy_verified=False,exporter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    return persist(directory/'corrected-dataset.json',body)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--directory',type=Path,required=True);a=p.parse_args()
    result=run(a.directory);print(result['hash'])
