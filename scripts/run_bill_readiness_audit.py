"""Fixed forty-design source accounting plus synthetic provenance challenges.

No quality parsing, reference edits, historical certification or predictive fits.
"""
import argparse
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from engine.paper_evaluation import require
from engine.store import ROOT,digest
from scripts.run_mechanism_design_extractor import BASE,INPUTS,PILOT,VIEWS,EXPECTED_PILOT,read,persist
from scripts.bill_render_coverage_audit import audit
from scripts.bill_provenance_preflight import run_manifest

INPUT_HASH='18ad3d6ca86b0656a8c427dad12337218c753f1ddebb29a360d2c15e8d669ca7'
CODE=['scripts/run_bill_readiness_audit.py','scripts/bill_render_coverage_audit.py',
      'scripts/bill_provenance_preflight.py','tests/test_bill_render_coverage_audit.py',
      'tests/test_bill_provenance_preflight.py','tests/test_readiness_independent.py',
      'tests/test_bill_readiness_runner.py','scripts/bill_context_design_text_v2.py',
      'scripts/paper_review_packet.py','scripts/paper_readiness_audit.py',
      'scripts/run_mechanism_design_extractor.py','scripts/mechanism_design_extractor.py',
      'engine/paper_evaluation.py','engine/store.py',
      'tests/fixtures/bill_provenance_preflight_v1.json']
FIXTURES=ROOT/'tests/fixtures/bill_provenance_preflight_v1.json'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def authenticate_source(source,raw):
    require(type(source.get('bytes')) is int and source['bytes']==len(raw),'Source size mismatch')
    require(source.get('sha256')==sha(raw),'Source digest mismatch')


def population(inputs,pilot):
    ids=[x['bill_id'] for x in inputs]
    design={x['bill_id'] for x in pilot['selection'] if x['partition']=='design'}
    quality={x['bill_id'] for x in pilot['selection'] if x['partition']=='quality'}
    require(len(ids)==len(set(ids))==40,'Exactly forty unique fixed design cases required')
    require(set(ids)<=design and set(ids).isdisjoint(quality),'Design/quality firewall violation')
    return ids


def run(directory):
    ie,inputs=read(INPUTS);pe,pilot=read(PILOT)
    require(ie['hash']==INPUT_HASH and pe['hash']==EXPECTED_PILOT,'Frozen population mismatch')
    ids=population(inputs,pilot);paths=[INPUTS,PILOT];loaded={}
    for item in inputs:
        bid=item['bill_id'];vp=VIEWS/(bid+'.json');ve,view=read(vp)
        require(ve['hash']==item['view_hash'],'Source view identity mismatch')
        require(all(view[k]==item[k] for k in ('bill_id','source','text','spans')),'Source view contents mismatch')
        source=view['source'];rawpath=PILOT.parent/'sources'/(sha(source['url'].encode())+'.raw')
        raw=rawpath.read_bytes();authenticate_source(source,raw)
        loaded[bid]=(view,raw);paths.extend([vp,rawpath])
    bound={str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in paths}
    code={p:sha((ROOT/p).read_bytes()) for p in CODE}
    directory=Path(directory);require(ROOT/'data' in directory.resolve().parents,'Output must be ignored runtime data')
    directory.mkdir(parents=True,exist_ok=True)
    reg=persist(directory/'registration.json',dict(scope='design_source_accounting_and_synthetic_provenance',bill_ids=ids,
        input_hash=ie['hash'],pilot_hash=pe['hash'],input_files=bound,code_sha256=code,python_version=sys.version,
        question='Does the frozen reading view preserve parsed text/tails and which structural or nontext information lacks representation? Do supplied identity/time facts pass declared synthetic guards?',
        budget='Exactly forty fixed design cases; authentication failures block before registration; subsequent audit failures retained without replacement; synthetic cases fixed in registered fixture',
        interpretation='Text accounting is not document completeness; conditional temporal validation is not evidence of historical availability',
        quality_access=False,model_fitting=False,human_certified=False,historical_feature_eligible=False))
    outputs={};failures=[];totals=Counter();warning_bills=Counter();unrepresented=Counter()
    for bid in ids:
        view,raw=loaded[bid];before=digest(view)
        try:
            result=audit(raw,bid,view)
            require(result==audit(raw,bid,view) and digest(view)==before,'Audit nondeterminism or mutation')
        except (ValueError,ET.ParseError) as error:
            result=dict(bill_id=bid,status='failed',error=str(error),source_document_completeness_verified=False)
            failures.append(dict(bill_id=bid,error=str(error)))
        totals.update(result.get('counts',{}))
        unrepresented.update(result.get('unrepresented_tags',{}))
        warning_bills.update({w['code'] for w in result.get('warnings',[])})
        outputs[bid]=persist(directory/(bid+'.json'),result)['hash']
    fixtures=run_manifest(json.loads(FIXTURES.read_text()))
    require(fixtures==run_manifest(json.loads(FIXTURES.read_text())),'Synthetic challenge nondeterminism')
    fixture_result=persist(directory/'provenance-fixtures.json',fixtures)
    require(all(sha((ROOT/p).read_bytes())==h for p,h in {**bound,**code}.items()),'Registered bytes changed')
    return persist(directory/'result.json',dict(registration_hash=reg['hash'],outputs=outputs,failures=failures,
        provenance_fixture_hash=fixture_result['hash'],synthetic_cases=len(fixtures['cases']),synthetic_passed=sum(c['passed'] for c in fixtures['cases']),synthetic_all_passed=fixtures['passed'],bills=len(ids),aggregate_counts=dict(totals),warning_bill_counts=dict(warning_bills),unrepresented_tags=dict(unrepresented),quality_access=False,model_fitting=False,
        historical_feature_eligible=False,human_certified=False,semantic_accuracy_verified=False,
        source_document_completeness_verified=False,interpretation='Readiness accounting only; no eligibility or quality promotion'))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    r=run(p.parse_args().output);print(r['hash']);print(r['body'])
