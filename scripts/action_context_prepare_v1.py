"""Separately registered offline re-extraction of fixed v1 source bytes; no labels/fits."""
import argparse
import collections
import json
import pathlib
from scripts import bicam_inventory_audit_v1 as common
from scripts import action_context_features_v1 as features

SOURCE=pathlib.Path('data/research-runs/official-context-acquisition-v1-20261109')
VERSION='action-context-prepare-v1'


def run(output):
    output.mkdir(parents=True,exist_ok=False);(output/'features').mkdir()
    registration=json.loads((SOURCE/'registration.json').read_text());ledger=json.loads((SOURCE/'population-ledger.json').read_text())
    # Validate every original frozen dependency before using source artifacts.
    for name,sha in registration['inputs'].items():
        if common.digest(pathlib.Path(name).read_bytes())!=sha:raise ValueError('Original registered input changed: '+name)
    paths=[SOURCE/'registration.json',SOURCE/'result.json',SOURCE/'population-ledger.json',
           pathlib.Path('scripts/action_context_features_v1.py'),pathlib.Path('scripts/official_context_features_v2.py'),pathlib.Path(__file__),
           pathlib.Path('tests/test_action_context_features_v1.py'),pathlib.Path('tests/test_action_context_independent.py'),
           pathlib.Path('docs/research/ACTION_CONTEXT_PREPARATION_V1.md'),
           pathlib.Path('docs/research/20261109-action-context-successor-proposal.md'),
           pathlib.Path('data/research-runs/official-context-primary-docs-20261109/gpo-guide.txt')]
    selected=registration['selected']
    ids=[r['bill_id'] for r in selected]
    ledger_ids=[r['bill_id'] for r in ledger]
    if len(ids)!=12000 or len(set(ids))!=12000 or len(ledger_ids)!=12000 or len(set(ledger_ids))!=12000 or set(ids)!=set(ledger_ids):
        raise ValueError('Original exact 12000 identity/ledger binding mismatch')
    if collections.Counter(r['congress'] for r in selected)!={c:2000 for c in range(113,119)}:
        raise ValueError('Original selected stratum count mismatch')
    oldledger={r['bill_id']:r for r in ledger}
    source_hashes={}
    for case in selected:
        bid=case['bill_id'];raw_path=SOURCE/'sources'/(bid+'.xml');receipt_path=SOURCE/'sources'/(bid+'-receipt.json')
        oldfeature=SOURCE/'features'/(bid+'.json')
        if not all(p.is_file() for p in (raw_path,receipt_path,oldfeature)):
            raise ValueError('Mandatory original artifact missing: '+bid)
        paths.extend([receipt_path,oldfeature])
        receipt_raw=receipt_path.read_bytes();receipt=json.loads(receipt_raw);raw=raw_path.read_bytes()
        if receipt['status']!=200 or receipt.get('parsed') is not True or receipt.get('identity_valid') is not True:
            raise ValueError('Original successful-source disposition changed')
        if common.digest(receipt_raw)!=oldledger[bid]['receipt_sha256']:
            raise ValueError('Original receipt/ledger binding mismatch')
        sha=common.digest(raw)
        if sha!=receipt['sha256'] or len(raw)!=receipt['bytes']:
            raise ValueError('Original source hash/size mismatch')
        prior=json.loads(oldfeature.read_text())
        if prior['bill_id']!=bid or prior['source_sha256']!=sha:
            raise ValueError('Original feature/source binding mismatch')
        source_hashes[bid]=sha
    common.save(output/'registration.json',dict(version=VERSION,inputs={str(p):common.digest(p.read_bytes()) for p in paths},source_hashes=source_hashes,
        original_acquisition=str(SOURCE),selected=registration['selected'],network_requests=0,labels_read=False,model_fits=0,
        change='Substantive adaptive action/chamber baseline replacing publication eligibility uniformly on all 12000 exposed identities; unchanged v2 contexts and outcome resolver. Whole-history structural selection remains.'))
    oldledger={r['bill_id']:r for r in ledger};newledger=[];changes=[]
    for case in registration['selected']:
        bid=case['bill_id'];row=dict(oldledger[bid]);raw_path=SOURCE/'sources'/(bid+'.xml')
        receipt_path=SOURCE/'sources'/(bid+'-receipt.json')
        receipt=json.loads(receipt_path.read_text()) if receipt_path.exists() else {}
        if receipt.get('parsed') and receipt.get('identity_valid'):
            try:
                raw=raw_path.read_bytes()
                if common.digest(raw)!=source_hashes[bid]:raise ValueError('Source changed during extraction')
                result=features.extract_features(raw,case);result['source_sha256']=source_hashes[bid]
                row.update(disposition='features_saved' if result['anchor'] is not None else 'feature_ineligible',reason=result['feature_errors'],feature_missing=result['missing'])
                prior_path=SOURCE/'features'/(bid+'.json')
                if prior_path.is_file():
                    prior=json.loads(prior_path.read_text())
                    for key in ('cutoff','related'):
                        if prior[key]!=result[key]:raise ValueError('Unchanged feature component changed: '+key)
                    changes.append(dict(bill_id=bid,before_anchor=prior['anchor'],after_anchor=result['anchor'],before_errors=prior['feature_errors'],after_errors=result['feature_errors'],before_stage=prior['stage'],after_stage=result['stage']))
                common.save(output/'features'/(bid+'.json'),result)
            except Exception as error:row.update(disposition='feature_failure',reason=type(error).__name__+': '+str(error))
        newledger.append(row)
    common.save(output/'population-ledger.json',newledger)
    common.save(output/'changes.json',changes)
    common.save(output/'result.json',dict(version=VERSION,selected=len(registration['selected']),source_files=len(source_hashes),dispositions=dict(collections.Counter(r['disposition'] for r in newledger)),changed_cases=len(changes),network_requests=0,labels_read=False,model_fits=0))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=pathlib.Path,required=True);run(parser.parse_args().output)
