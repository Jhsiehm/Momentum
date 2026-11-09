"""Offline v2 source coverage and before/after missingness; no labels or fitting."""
import argparse
import collections
import json
import pathlib
from scripts import bicam_inventory_audit_v1 as common


def summarize(directory):
    registration=json.loads((directory/'registration.json').read_text())
    result=json.loads((directory/'result.json').read_text())
    ledger=json.loads((directory/'population-ledger.json').read_text())
    source=pathlib.Path(registration['original_acquisition'])
    for name,sha in registration['inputs'].items():
        path=pathlib.Path(name)
        if not path.is_file() or common.digest(path.read_bytes())!=sha:raise ValueError('Registered input changed/missing: '+name)
    cases={r['bill_id']:r for r in registration['selected']}
    if len(cases)!=12000 or len(ledger)!=12000 or {r['bill_id'] for r in ledger}!=set(cases):raise ValueError('Population binding mismatch')
    if result['labels_read'] is not False or result['model_fits']!=0:raise ValueError('Not source-only result')
    by_congress={str(c):dict(selected=0,dispositions={},anchor_valid=0,before_observed=[0,0,0],after_observed=[0,0,0],after_missing=[0,0,0],complete_context=0,missing_reasons={},feature_errors={})for c in range(113,119)}
    details=[];unchanged=0
    for row in ledger:
        bid=row['bill_id'];case=cases[bid];group=by_congress[str(case['congress'])];group['selected']+=1
        disposition=row['disposition'];group['dispositions'][disposition]=group['dispositions'].get(disposition,0)+1
        path=directory/'features'/(bid+'.json');oldpath=source/'features'/(bid+'.json')
        detail=dict(row)
        if disposition in ('features_saved','feature_ineligible') and not path.exists():raise ValueError('Expected v2 feature missing')
        if path.exists():
            feature=json.loads(path.read_text());prior=json.loads(oldpath.read_text())
            if feature['source_sha256']!=registration['source_hashes'][bid]:raise ValueError('Feature source mismatch')
            for key in ('anchor','stage','cutoff','related'):
                if feature[key]!=prior[key]:raise ValueError('Unchanged component differed: '+key)
            if feature['context'][0]!=prior['context'][0]:raise ValueError('Cosponsor differed')
            unchanged+=1
            detail.update(feature_sha256=common.digest(path.read_bytes()),anchor_valid=feature['anchor'] is not None,before_missing=prior['missing'],after_missing=feature['missing'],missing_reasons=feature.get('missing_reasons'),feature_errors=feature['feature_errors'])
            if feature['anchor'] is not None:
                group['anchor_valid']+=1
                for i in range(3):
                    group['before_observed'][i]+=int(not prior['missing'][i]);group['after_observed'][i]+=int(not feature['missing'][i]);group['after_missing'][i]+=feature['missing'][i]
                group['complete_context']+=int(not any(feature['missing']))
                for reason in feature.get('missing_reasons',[]):
                    if reason:group['missing_reasons'][reason]=group['missing_reasons'].get(reason,0)+1
            for reason in feature['feature_errors']:group['feature_errors'][reason]=group['feature_errors'].get(reason,0)+1
        details.append(detail)
    return dict(version='official-context-v2-source-summary',registration_sha256=common.digest((directory/'registration.json').read_bytes()),result_sha256=common.digest((directory/'result.json').read_bytes()),
        population_ledger_sha256=common.digest((directory/'population-ledger.json').read_bytes()),selected=len(cases),unchanged_anchor_cosponsor_cutoff_family_cases=unchanged,
        by_congress=by_congress,cases=details,labels_read=False,model_fits=0,interpretation='Schema correction coverage only; no predictive improvement measured')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('directory',type=pathlib.Path);args=parser.parse_args()
    summary=summarize(args.directory);sha=common.save(args.directory/'source-summary.json',summary)
    print(json.dumps({'summary_sha256':sha,**{k:v for k,v in summary.items() if k!='cases'}},indent=2))
