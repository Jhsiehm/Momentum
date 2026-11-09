"""Offline identity set comparison; presence does not certify metadata or outcomes."""
import argparse
import json
from pathlib import Path
import re
from scripts.bicam_official_inventory_v1 import digest, save


def compare(official, candidates, errors):
    if not official.get('all_indexes_accepted') or len(official['results']) != 12:
        raise ValueError('Require twelve accepted current indexes')
    if {(r['congress'],r['bill_type']) for r in official['results']} != {(c,t) for c in range(113,119) for t in ('hr','s')}:
        raise ValueError('Incorrect official group membership')
    official_ids = {bid for group in official['results'] for bid in group['ids']}
    candidate_ids = {r['bill_id'] for r in candidates}
    if any(not re.fullmatch(r'(hr|s)[1-9]\d*-11[3-8]', bid) for bid in official_ids | candidate_ids):
        raise ValueError('Out-of-scope comparison identity')
    if len(candidate_ids) != len(candidates):
        raise ValueError('Duplicate candidate IDs')
    ledger = []
    for error in errors:
        bid = error.get('original', {}).get('bill_id', '')
        match = re.fullmatch(r'(hr|s)([1-9]\d*)-(11[3-8])', bid)
        ledger.append({'error':error,'identity_string_in_target_scope':bool(match),
                       'official_directory_present':bid in official_ids if match else None,
                       'candidate_census_present':bid in candidate_ids if match else None})
    by_group = []
    for group in official['results']:
        prefix, suffix = group['bill_type'], '-'+str(group['congress'])
        c = {bid for bid in candidate_ids if re.fullmatch(prefix+r'[1-9]\d*'+suffix,bid)}
        o = set(group['ids'])
        by_group.append({'congress':group['congress'],'bill_type':prefix,'official_count':len(o),
                         'candidate_count':len(c),'intersection':len(o&c),
                         'official_not_candidate':sorted(o-c),'candidate_not_official':sorted(c-o)})
    return {'official_count':len(official_ids),'candidate_count':len(candidate_ids),
            'intersection':len(official_ids&candidate_ids),
            'official_not_candidate':sorted(official_ids-candidate_ids),
            'candidate_not_official':sorted(candidate_ids-official_ids),
            'by_group':by_group,'all_corpus_errors':ledger,'candidate_census_complete':False,
            'historical_availability_certified':False,'model_fits':0}


def run(official_path, census_path, errors_path, out):
    paths=[official_path,census_path,errors_path]
    out.mkdir(parents=True,exist_ok=False)
    reg={'input_hashes':{str(p):digest(p.read_bytes()) for p in paths},
         'code_protocol_hashes':{str(p):digest(p.read_bytes()) for p in [Path(__file__),Path('tests/test_bicam_inventory_compare_v1.py'),Path('docs/research/BICAM_INVENTORY_COMPARE_V1.md')]},
         'network_requests':0,'model_fits':0}
    reg_hash=save(out/'registration.json',reg)
    result=compare(*(json.loads(p.read_text()) for p in paths))
    result['registration_sha256']=reg_hash
    save(out/'result.json',result)
    print(json.dumps({k:result[k] for k in ['official_count','candidate_count','intersection']}))

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name in ['official','census','errors','output']:
        p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();run(a.official,a.census,a.errors,a.output)
