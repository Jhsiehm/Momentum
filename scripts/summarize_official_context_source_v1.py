"""Offline source-only summary; never reads labels or invokes outcome resolution."""
import argparse
import collections
import json
import pathlib
from scripts import bicam_inventory_audit_v1 as common


def summarize(directory):
    registration=json.loads((directory/'registration.json').read_text())
    result=json.loads((directory/'result.json').read_text())
    ledger=json.loads((directory/'population-ledger.json').read_text())
    for name,sha in registration['inputs'].items():
        path=pathlib.Path(name)
        if not path.exists() or common.digest(path.read_bytes())!=sha:raise ValueError('Registered input changed/missing: '+name)
    selected=registration['selected'];expected={r['bill_id']:r for r in selected}
    if len(expected)!=len(selected) or {r['bill_id'] for r in ledger}!=set(expected) or len(ledger)!=len(expected):
        raise ValueError('Population identity mismatch')
    if result['labels_read'] is not False or result['model_fits']!=0:
        raise ValueError('Not source-only')
    by_congress={str(c):dict(selected=0,dispositions={},valid_anchor=0,context_observed=[0,0,0],context_missing=[0,0,0],complete_three_context=0,missing_reasons={},feature_errors={}) for c in range(113,119)}
    cases=[];http=collections.Counter();body_bytes=0;source_files=0
    for row in ledger:
        bid=row['bill_id'];case=expected[bid];stats=by_congress[str(case['congress'])];stats['selected']+=1
        disposition=row['disposition'];stats['dispositions'][disposition]=stats['dispositions'].get(disposition,0)+1
        detail=dict(row)
        receipt_path=directory/'sources'/(bid+'-receipt.json')
        if row.get('receipt_sha256') and not receipt_path.exists():raise ValueError('Expected receipt missing')
        if receipt_path.exists():
            raw_receipt=receipt_path.read_bytes();receipt=json.loads(raw_receipt)
            if row.get('receipt_sha256') and common.digest(raw_receipt)!=row['receipt_sha256']:raise ValueError('Receipt binding mismatch')
            http[str(receipt.get('status','transport_failure'))]+=1
            body_bytes+=receipt.get('bytes',0)
            raw_path=directory/'sources'/(bid+'.xml')
            if receipt.get('sha256') and not raw_path.exists():raise ValueError('Expected source bytes missing')
            if raw_path.exists():
                raw=raw_path.read_bytes()
                if len(raw)!=receipt['bytes'] or common.digest(raw)!=receipt['sha256']:raise ValueError('Raw source binding mismatch')
                source_files+=1
            detail.update(http_status=receipt.get('status'),response_bytes=receipt.get('bytes',0),source_sha256=receipt.get('sha256'))
        feature_path=directory/'features'/(bid+'.json')
        if disposition in ('features_saved','feature_ineligible') and not feature_path.exists():raise ValueError('Expected feature artifact missing')
        if feature_path.exists():
            feature=json.loads(feature_path.read_text())
            if feature['bill_id']!=bid or feature['source_sha256']!=detail.get('source_sha256'):raise ValueError('Feature source binding mismatch')
            detail.update(feature_sha256=common.digest(feature_path.read_bytes()),cutoff=feature['cutoff'],stage=feature['stage'],missing=feature['missing'],missing_reasons=feature.get('missing_reasons'),feature_errors=feature['feature_errors'],related_ids=feature['related'])
            if feature['anchor'] is not None:
                stats['valid_anchor']+=1
                for i,missing in enumerate(feature['missing']):
                    stats['context_missing' if missing else 'context_observed'][i]+=1
                stats['complete_three_context']+=int(not any(feature['missing']))
                for reason in feature.get('missing_reasons',[]):
                    if reason:stats['missing_reasons'][reason]=stats['missing_reasons'].get(reason,0)+1
            for reason in feature['feature_errors']:stats['feature_errors'][reason]=stats['feature_errors'].get(reason,0)+1
        cases.append(detail)
    if body_bytes!=result['response_bytes']:raise ValueError('Response-byte total mismatch')
    return dict(version='official-context-source-summary-v1',registration_sha256=common.digest((directory/'registration.json').read_bytes()),
                acquisition_result_sha256=common.digest((directory/'result.json').read_bytes()),ledger_sha256=common.digest((directory/'population-ledger.json').read_bytes()),
                selected=len(selected),source_files=source_files,response_bytes=body_bytes,http_status_counts=dict(http),by_congress=by_congress,cases=cases,
                labels_read=False,model_fits=0,interpretation='Source-only coverage; no efficacy or certified historical eligibility claim')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('directory',type=pathlib.Path);args=parser.parse_args()
    summary=summarize(args.directory)
    digest=common.save(args.directory/'source-summary.json',summary)
    print(json.dumps({'summary_sha256':digest,**{k:v for k,v in summary.items() if k!='cases'}},indent=2))
