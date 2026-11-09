"""Offline amendment: classify exact directory ZIP links separately from XML."""
import argparse
import json
from pathlib import Path
import urllib.parse
from scripts import bicam_official_inventory_v1 as v1

VERSION = 'bicam-official-inventory-offline-v2'


def parse(raw, congress, bill_type, url):
    result = v1.parse(raw, congress, bill_type, url)
    zip_url = f'https://www.govinfo.gov/bulkdata/BILLSTATUS/{congress}/{bill_type}/BILLSTATUS-{congress}-{bill_type}.zip'
    resource, rejected = [], []
    for href in result['rejected_bill_links']:
        (resource if urllib.parse.urljoin(url+'/', href) == zip_url else rejected).append(href)
    result['directory_zip_resources'] = resource
    result['rejected_bill_links'] = rejected
    result['accepted_index'] = bool(result['ids']) and result['closed_html'] and not result['pagination_links'] and not rejected
    return result


def run(source, out):
    original = json.loads((source/'result.json').read_text())
    if original['requests'] != 12:
        raise ValueError('Expected complete twelve-request acquisition receipt')
    paths = [source/'result.json', source/'registration.json']
    for c,t,_ in v1.URLS:
        paths.extend([source/f'{c}-{t}.html', source/f'{c}-{t}-receipt.json'])
    pinned = [Path(__file__), Path(v1.__file__), Path('tests/test_bicam_official_inventory_offline_v2.py'), Path('docs/research/BICAM_OFFICIAL_INVENTORY_OFFLINE_V2.md')]
    out.mkdir(parents=True, exist_ok=False)
    reg = {'version': VERSION, 'input_hashes': {str(p):v1.digest(p.read_bytes()) for p in paths},
           'code_protocol_hashes':{str(p):v1.digest(p.read_bytes()) for p in pinned}, 'network_requests':0,
           'change':'Exact same-directory official ZIP links are preserved separately; XML rules unchanged.'}
    reg_hash = v1.save(out/'registration.json',reg)
    results = []
    for congress,bill_type,url in v1.URLS:
        receipt = json.loads((source/f'{congress}-{bill_type}-receipt.json').read_text())
        raw = (source/f'{congress}-{bill_type}.html').read_bytes()
        if receipt.get('status') != 200 or receipt.get('truncated') or v1.digest(raw)!=receipt.get('raw_sha256'):
            raise ValueError('Unusable acquisition response')
        results.append(parse(raw,congress,bill_type,url))
    result = {'version':VERSION,'registration_sha256':reg_hash,'network_requests':0,
              'all_indexes_accepted':all(r['accepted_index'] for r in results),
              'unique_ids':sum(r['unique_count'] for r in results),'results':results,
              'official_completeness_certified':False,'historical_availability_certified':False,'model_fits':0}
    v1.save(out/'result.json',result)
    print(json.dumps({k:v for k,v in result.items() if k!='results'},indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();run(args.source,args.output)
