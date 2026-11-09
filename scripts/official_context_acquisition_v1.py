"""Registered 12k current-source acquisition and feature-only preparation; no labels/fits."""
import argparse
import concurrent.futures as cf
import hashlib
import json
import pathlib
import re
import time
import urllib.request
from scripts import bicam_inventory_audit_v1 as common
from scripts import official_billstatus_readiness_v1 as audit
from scripts import official_context_features_v1 as features

VERSION='official-context-diagnostic-v1'
BASE=pathlib.Path('data/research-runs')
TOTAL_BYTES=500_000_000
WALL_SECONDS=1800
WORKERS=4


def body(path):
    value=json.loads(path.read_text());return value.get('body',value)


def canonical(bid):
    match=re.fullmatch(r'(\d+)-(hr|s|hres|sres|hjres|sjres|hconres|sconres)(\d+)',bid)
    if match:return f'{match[2]}{match[3]}-{match[1]}'
    if re.fullmatch(r'(hr|s|hres|sres|hjres|sjres|hconres|sconres)\d+-\d+',bid):return bid
    raise ValueError('Invalid known-family identity')


def protected_manifest():
    pilot_path=BASE/'bill-context-20261108-v1/registration.json'
    pilot=body(pilot_path);paths=[pilot_path]
    direct={canonical(r['bill_id']) for r in pilot['selection']}
    families={r['family_id'] for r in pilot['selection']}
    previous=BASE/'retrospective-text-diagnostic-v1-20261108'
    exposed=set()
    for congress in (115,116):
        path=previous/f'{congress}-predictions.json';paths.append(path)
        for row in body(path)['predictions']:
            exposed.add(canonical(row['bill_id']));families.add(row['family_id'])
    if len(direct)!=100 or len(exposed)!=595:raise ValueError('Protected/exposed cohort counts changed')
    direct|=exposed
    known={}
    for name in ('mechanism-training-coverage-20261108-v2','mechanism-training-expansion-20261108-v1'):
        for path in sorted((BASE/name/'records').glob('*.json')):
            row=body(path);paths.append(path)
            if 'bill_id' in row and 'family_id' in row:
                bid=canonical(row['bill_id']);family=row['family_id']
                if bid in known and known[bid]!=family:raise ValueError('Conflicting frozen family assignment')
                known[bid]=family
    excluded=set(direct)|{bid for bid,family in known.items() if family in families}
    return dict(excluded_ids=sorted(excluded),direct_pilot_and_scored_ids=sorted(direct),banned_family_ids=sorted(families),known_family_assignments=known,
                family_coverage='Frozen protected/exposed/source records only; no full provision genealogy',input_sha256={str(p):common.digest(p.read_bytes()) for p in paths})


def select(population,excluded,per_congress=2000):
    groups={c:[] for c in range(113,119)};ledger=[]
    for bid,row in population.items():
        if bid in excluded:ledger.append(dict(bill_id=bid,reason='protected_or_previously_scored_known_family'));continue
        groups[row['congress']].append(row)
    selected={}
    for congress,rows in groups.items():
        selected[congress]=sorted(rows,key=lambda r:common.digest((VERSION+'\n'+r['bill_id']).encode()))[:per_congress]
        if len(selected[congress])!=per_congress:raise ValueError('Insufficient source-only stratum')
    schedule=[selected[c][i] for i in range(per_congress) for c in range(113,119)]
    return schedule,ledger


def run(output):
    output.mkdir(parents=True,exist_ok=False)
    sources=output/'sources';sources.mkdir()
    feature_dir=output/'features';feature_dir.mkdir()
    index_path=audit.DIRECTORY/'result.json';index=json.loads(index_path.read_text());pages={}
    paths=[index_path]
    for c in range(113,119):
        for kind in ('hr','s'):
            path=audit.HTML_DIRECTORY/f'{c}-{kind}.html';paths.append(path);pages[f'{c}-{kind}']=path.read_text()
    population,_=audit.population_and_sample(index,pages)
    protected=protected_manifest();selected,exclusions=select(population,set(protected['excluded_ids']))
    for name in ('scripts/official_context_acquisition_v1.py','scripts/official_context_features_v1.py','scripts/official_billstatus_readiness_v1.py','scripts/bicam_inventory_audit_v1.py','tests/test_official_context_v1.py','tests/test_official_context_independent.py','docs/research/OFFICIAL_CONTEXT_DIAGNOSTIC_V1.md'):
        paths.append(pathlib.Path(name))
    paths.extend(sorted((BASE/'official-context-primary-docs-20261109').glob('*.txt')))
    hashes={str(p):common.digest(p.read_bytes()) for p in paths};hashes.update(protected['input_sha256'])
    common.save(output/'registration.json',dict(version=VERSION,inputs=hashes,selected=selected,exclusions=exclusions,protected=protected,
        maximum_requests=len(selected),total_byte_cap=TOTAL_BYTES,per_response_cap=audit.CAP+1,workers=WORKERS,scheduling_wall_seconds=WALL_SECONDS,
        retries=0,replacements=0,labels_read=False,model_fits=0,exposure='Retrospective current-rendition diagnostic; no historically certified forecasts'))
    started=time.monotonic();receipts={};pending={};iterator=iter(selected);used_bytes=0;scheduled=0;stop_reason=None
    def task(case):return audit.fetch_case(case,sources,urllib.request.build_opener(common.NoRedirect))
    with cf.ThreadPoolExecutor(max_workers=WORKERS) as pool:
        exhausted=False
        while pending or not exhausted:
            while len(pending)<WORKERS and not exhausted:
                if time.monotonic()-started>=WALL_SECONDS:stop_reason='scheduling_wall_cap';exhausted=True;break
                if used_bytes+(len(pending)+1)*(audit.CAP+1)>TOTAL_BYTES:stop_reason='aggregate_byte_cap_reservation';exhausted=True;break
                try:case=next(iterator)
                except StopIteration:exhausted=True;break
                future=pool.submit(task,case);pending[future]=case;scheduled+=1
            if not pending:break
            done,_=cf.wait(pending,return_when=cf.FIRST_COMPLETED)
            for future in done:
                case=pending.pop(future)
                try:receipt=future.result()
                except Exception as error:receipt=dict(bill_id=case['bill_id'],parsed=False,error=type(error).__name__+': '+str(error))
                receipts[case['bill_id']]=receipt;used_bytes+=receipt.get('bytes',0)
                if used_bytes>TOTAL_BYTES:raise ValueError('Aggregate body cap violated')
            if len(receipts)%100==0:print(json.dumps(dict(completed=len(receipts),scheduled=scheduled,bytes=used_bytes)),flush=True)
    ledger=[];feature_counts={}
    for case in selected:
        bid=case['bill_id'];receipt=receipts.get(bid)
        row=dict(bill_id=bid,congress=case['congress'],disposition='not_attempted',reason=stop_reason)
        if receipt is not None:
            row.update(disposition='source_failure',receipt_sha256=common.digest((sources/(bid+'-receipt.json')).read_bytes()) if (sources/(bid+'-receipt.json')).exists() else None,reason=receipt.get('error'))
            if receipt.get('parsed') and receipt.get('identity_valid'):
                try:
                    raw=(sources/(bid+'.xml')).read_bytes()
                    if common.digest(raw)!=receipt['sha256']:raise ValueError('Saved source hash mismatch')
                    feature=features.extract_features(raw,case)
                    feature['source_sha256']=receipt['sha256'];common.save(feature_dir/(bid+'.json'),feature)
                    row.update(disposition='features_saved' if feature['anchor'] is not None else 'feature_ineligible',reason=feature['feature_errors'],feature_missing=feature['missing'])
                except Exception as error:row.update(disposition='feature_failure',reason=type(error).__name__+': '+str(error))
        ledger.append(row);feature_counts[row['disposition']]=feature_counts.get(row['disposition'],0)+1
    common.save(output/'population-ledger.json',ledger)
    common.save(output/'result.json',dict(version=VERSION,selected=len(selected),requests_scheduled=scheduled,completed=len(receipts),response_bytes=used_bytes,
        stop_reason=stop_reason,dispositions=feature_counts,labels_read=False,model_fits=0,
        historical_eligibility=False,note='Features/source population only; family split and label protocol require independent review before labels/fits'))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=pathlib.Path,required=True);run(parser.parse_args().output)
