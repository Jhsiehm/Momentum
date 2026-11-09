"""Registered synthetic software validation; never opens bill outcomes or fits forecasts."""
import argparse
import hashlib
import json
import math
import platform
import sys
from pathlib import Path
import numpy as np
import scipy
from scipy import sparse
from scipy.special import expit
from engine.store import ROOT,digest
from engine.paper_evaluation import require,seal
from scripts.run_mechanism_design_extractor import BASE,read,persist
from scripts.bill_context_design_text_v2 import render
from scripts.bill_structural_input_v1 import build
from scripts.matched_text_preprocessing_v1 import prepare_document,CoreTfidf
from scripts.matched_text_sparse_v1 import objective_gradient,fit,fit_structured_scaler,transform_structured,combine_features,SOLVER_OPTIONS

FIXTURE=ROOT/'tests/fixtures/matched_text_synthetic_v1.json'
SPEC=BASE/'matched-text-comparison-v1-20261108/registration.json'
SPEC_HASH='6fcf636b2fa7801d6c6098ac54a82f5ee611ef56a5d4a447c690b8b9461e385a'
CODE=['scripts/run_matched_text_synthetic_v2.py','tests/test_matched_text_synthetic_runner_v2.py','scripts/run_matched_text_synthetic_v1.py','scripts/matched_text_preprocessing_v1.py','scripts/matched_text_sparse_v1.py',
      'tests/test_matched_text_preprocessing_v1.py','tests/test_matched_text_sparse_v1.py','tests/test_matched_text_pipeline_independent.py',
      'docs/research/MATCHED_TEXT_PREPROCESSING_V1.md','requirements-research-text-v1.txt',
      'scripts/bill_context_design_text_v2.py','scripts/bill_structural_input_v1.py','scripts/bill_render_coverage_audit_v2.py',
      'scripts/run_mechanism_design_extractor.py','scripts/paper_review_packet.py','scripts/mechanism_design_extractor.py',
      'engine/paper_evaluation.py','engine/store.py']


def sha(raw):return hashlib.sha256(raw).hexdigest()

def scalar(theta,X,y):
    gradient=[0.0]*len(theta);total=0.
    for row,label in zip(X,y):
        z=theta[0]+sum(a*b for a,b in zip(theta[1:],row))
        total+=max(z,0)-label*z+math.log1p(math.exp(-abs(z)))
        p=1/(1+math.exp(-z)) if z>=0 else math.exp(z)/(1+math.exp(z))
        residual=p-label;gradient[0]+=residual
        for j,x in enumerate(row,1):gradient[j]+=residual*x
    return total/len(y)+.025*sum(w*w for w in theta[1:]),np.array([g/len(y)+(.05*theta[j] if j else 0) for j,g in enumerate(gradient)])


def serializable_checks(checks):
    require(all(isinstance(value,(bool,np.bool_)) for value in checks.values()),'Boolean checks required')
    return {key:bool(value) for key,value in checks.items()}


def run(directory):
    se,_=read(SPEC);require(se['hash']==SPEC_HASH,'Specification binding changed')
    require(np.__version__=='2.0.2' and scipy.__version__=='1.13.1','Pinned research dependencies required')
    fixture=json.loads(FIXTURE.read_text());rows=fixture['documents'];ids=[r['id'] for r in rows]
    require(len(ids)==len(set(ids))==28,'Fixed28 synthetic rows required')
    require([r['role'] for r in rows]==['core']*20+['calibration']*4+['evaluation']*4,'Fixed ordered synthetic split')
    failure_path=BASE/'matched-text-synthetic-v1-20261108/failure.json'
    failure,_=read(failure_path);require(failure['hash']=='a8151e163ddd9cac86a87405e14238ccb1e1c0f76639ce25f647cb1b6f7a017a','Prior failure changed')
    files={str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in [FIXTURE,SPEC,failure_path]};code={p:sha((ROOT/p).read_bytes()) for p in CODE}
    directory=Path(directory).resolve();require(ROOT/'data' in directory.parents,'Runtime output required');directory.mkdir(parents=True,exist_ok=True)
    reg=persist(directory/'registration.json',dict(version='matched-text-synthetic-validation-v2-json-booleans',prior_failure_hash=failure['hash'],input_files=files,code_sha256=code,
        environment=dict(python=sys.version,numpy=np.__version__,scipy=scipy.__version__,platform=platform.platform()),
        fixture_origin=fixture['origin'],specification_hash=se['hash'],ids=ids,thresholds=fixture['thresholds'],solver_options=SOLVER_OPTIONS,
        budget='Three fixed synthetic L-BFGS optimizations plus one scalar GD reference capped20000 iterations; no real-data fits, tuning or retries',
        checks=['source-preserving preparation','core-only vocab and IDF','structural bigram barriers','sparse assembly','scalar/finite-difference objective','GD agreement','final gradient'],
        interpretation='Synthetic engineering verification only; no original evidence gates automatically released',real_bill_access=False,outcome_access=False))
    prepared=[]
    for row in rows:
        number=row['bill_id'].split('hr')[1]
        raw=('<bill><form><congress>113th CONGRESS</congress><legis-num>H. R. '+number+'</legis-num><official-title>Invented fixture for software verification</official-title></form><legis-body>'+row['body']+'</legis-body></bill>').encode()
        view=render(raw,row['bill_id']);vh=seal(view)['hash'];side=build(raw,row['bill_id'],view,vh)
        doc=prepare_document(raw,row['bill_id'],view,vh,side)
        require(doc['text']==view['text'],'Source context changed');prepared.append(doc)
    require(all(('red','blue') not in list(zip(segment['tokens'],segment['tokens'][1:])) for doc in prepared for segment in doc['token_segments']),'Cross-cell bigram in prepared stream')
    require(any('quarantinetoken' in segment['tokens'] for doc in prepared[20:] for segment in doc['token_segments']),'Holdout challenge was erased')
    require(any('not' in segment['tokens'] for doc in prepared[:20] for segment in doc['token_segments']),'Negation was erased')
    core=prepared[:20];vectorizer=CoreTfidf().fit(core,ids[:20],['core']*20);manifest=vectorizer.manifest();manifest_before=digest(manifest)
    matrices={role:vectorizer.transform([d for d,r in zip(prepared,rows) if r['role']==role]) for role in ('core','calibration','evaluation')}
    require(digest(vectorizer.manifest())==manifest_before,'Heldout transform mutated vocabulary')
    terms={tuple(t) for t in manifest['terms']}
    require(not any('quarantinetoken' in t or 'unseenholdout' in t for t in terms),'Holdout vocabulary leaked')
    require(('red','blue') not in terms,'Cross-cell bigram leaked')
    raw_structured=np.array([r['structured'] for r in rows],dtype=float);scaler=fit_structured_scaler(raw_structured[:20]);scaler_before=digest(scaler)
    anchor=transform_structured(raw_structured[:20],scaler);combined=combine_features(raw_structured[:20],scaler,matrices['core'])
    evaluation_combined=combine_features(raw_structured[24:],scaler,matrices['evaluation'])
    require(digest(scaler)==scaler_before,'Heldout structured scaling mutated core')
    case=fixture['numerical'];X=sparse.csr_matrix(case['X']);y=np.array(case['y']);theta=np.array(case['theta']);loss,gradient=objective_gradient(theta,X,y)
    sloss,sgrad=scalar(theta,case['X'],case['y']);finite_diff=[]
    for j in range(len(theta)):
        delta=np.zeros(len(theta));delta[j]=1e-6
        finite_diff.append((objective_gradient(theta+delta,X,y)[0]-objective_gradient(theta-delta,X,y)[0])/2e-6)
    check=dict(scalar_objective_error=float(abs(loss-sloss)),scalar_gradient_error=float(np.max(np.abs(gradient-sgrad))),finite_difference_error=float(np.max(np.abs(gradient-finite_diff))))
    first=fit(X,y)
    gd=np.zeros(len(theta));gd_steps=0
    for step in range(20000):
        _,g=scalar(gd,case['X'],case['y'])
        if step>=300 and np.max(np.abs(g))<=1e-6:break
        gd-=.12*g;gd_steps+=1
    _,g=scalar(gd,case['X'],case['y'])
    check['gd_gradient']=float(np.max(np.abs(g)));check['gd_iterations']=gd_steps
    check['gd_prediction_difference']=None if first['parameters'] is None else float(np.max(np.abs(expit(X@np.array(first['parameters'])[1:]+first['parameters'][0])-expit(X@gd[1:]+gd[0]))))
    synthetic_y=np.array([r['synthetic_label'] for r in rows[:20]])
    fits={'low_dimension':first,'synthetic_anchor':fit(anchor,synthetic_y),'synthetic_anchor_plus_text':fit(combined,synthetic_y)}
    thresholds=fixture['thresholds']
    checks=dict(core_only_vocabulary=True,heldout_transform_state_unchanged=True,source_context_preserved=True,cross_cell_bigram_absent=True,
        scalar_objective=check['scalar_objective_error']<=thresholds['scalar_objective_max_error'],
        scalar_gradient=check['scalar_gradient_error']<=thresholds['scalar_gradient_max_error'],
        finite_difference=check['finite_difference_error']<=thresholds['finite_difference_max_error'],
        gd_converged=check['gd_gradient']<=1e-6,
        gd_predictions=check['gd_prediction_difference'] is not None and check['gd_prediction_difference']<=thresholds['gd_prediction_max_difference'],
        all_synthetic_optimizations_accepted=all(f['accepted'] for f in fits.values()))
    checks=serializable_checks(checks)
    prep=persist(directory/'prepared-synthetic-documents.json',prepared)
    vf=persist(directory/'vocabulary.json',manifest);ff=persist(directory/'synthetic-fits.json',fits)
    require(all(sha((ROOT/p).read_bytes())==h for p,h in {**files,**code}.items()),'Registered code/input changed')
    return persist(directory/'result.json',dict(registration_hash=reg['hash'],checks=checks,all_passed=all(checks.values()),numerical=check,
        vocabulary_size=len(terms),prepared_document_hash=prep['hash'],vocabulary_hash=vf['hash'],synthetic_fits_hash=ff['hash'],
        matrices={k:dict(shape=list(v.shape),nnz=v.nnz) for k,v in matrices.items()},combined_core_shape=list(combined.shape),combined_evaluation_shape=list(evaluation_combined.shape),
        structured_scaler=scaler,synthetic_optimizations=3,scalar_gd_references=1,real_data_fits=0,real_outcomes_accessed=False,
        remaining_gates='Historical source, qualified reviews, positive-family scope, temporal/family eligibility, eligible membership, actual classes/runtime, real-source masking validation and execution freeze remain unresolved',
        historical_feature_eligible=False,predictive_execution_permitted=False))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    r=run(p.parse_args().output);print(r['hash']);print(r['body'])
