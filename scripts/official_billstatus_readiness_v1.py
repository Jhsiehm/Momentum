"""Bounded outcome-blind official BILLSTATUS source-readiness audit."""
import argparse
import collections
import datetime
import hashlib
import html.parser
import json
import pathlib
import re
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from scripts import bicam_inventory_audit_v1 as common

VERSION='official-billstatus-readiness-v1'
DIRECTORY=pathlib.Path('data/research-runs/bicam-official-inventory-offline-v2-20261109')
HTML_DIRECTORY=pathlib.Path('data/research-runs/bicam-official-inventory-v1-20261109')
CAP=2_000_000

class Links(html.parser.HTMLParser):
    def __init__(self):
        super().__init__();self.hrefs=[]
    def handle_starttag(self,tag,attrs):
        if tag.lower()=='a':
            self.hrefs += [v for k,v in attrs if k.lower()=='href' and v is not None]


def population_and_sample(index, pages):
    if index.get('all_indexes_accepted') is not True or len(index['results'])!=12:
        raise ValueError('Official indexes not accepted')
    population={}; strata=set()
    for item in index['results']:
        congress,kind=item['congress'],item['bill_type'];key=f'{congress}-{kind}'
        if congress not in range(113,119) or kind not in ('hr','s') or key in strata:
            raise ValueError('Invalid/duplicate stratum')
        strata.add(key)
        links=Links();links.feed(pages[key]); observed=set(links.hrefs)
        if len(item['ids'])!=item['unique_count'] or not item['accepted_index']:
            raise ValueError('Index count mismatch')
        for bid in item['ids']:
            match=re.fullmatch(r'(hr|s)([1-9][0-9]*)-([1-9][0-9]*)',bid)
            if not match or match[1]!=kind or int(match[3])!=congress or bid in population:
                raise ValueError('Invalid/duplicate identity')
            href=f'/bulkdata/BILLSTATUS/{congress}/{kind}/BILLSTATUS-{congress}{kind}{match[2]}.xml'
            if href not in observed:
                raise ValueError('Expected XML URL absent from observed hrefs')
            population[bid]=dict(bill_id=bid,congress=congress,bill_type=kind,bill_number=int(match[2]),url='https://www.govinfo.gov'+href)
    if len(population)!=index['unique_ids'] or len(population)<100:
        raise ValueError('Population count mismatch')
    sample=sorted(population.values(),key=lambda row:common.digest((VERSION+'\n'+row['bill_id']).encode()))[:100]
    return population,sample


def date_check(value):
    try:
        date=datetime.date.fromisoformat(value)
        return date.isoformat()==value
    except (ValueError,TypeError):
        return False


def inspect_xml(raw,case):
    if len(raw)>CAP or b'\x00' in raw or b'<!DOCTYPE' in raw.upper() or b'<!ENTITY' in raw.upper():
        raise ValueError('Oversized or unsafe/unsupported XML encoding/declaration')
    root=ET.fromstring(raw)
    paths=collections.Counter()
    stack=[(root,root.tag)]
    while stack:
        node,path=stack.pop();paths[path]+=1
        if len(paths)>10000:
            raise ValueError('Schema path cap exceeded')
        stack.extend((child,path+'/'+child.tag) for child in node)
    result=dict(bill_id=case['bill_id'],schema_paths=dict(sorted(paths.items())),
                schema_fingerprint=common.digest(json.dumps(sorted(paths),separators=(',',':')).encode()),
                schema_version=root.attrib.get('version'),identity_valid=False,errors=[],
                exposure='Current retrospective metadata; not historically certified or untouched confirmatory evaluation')
    if root.tag!='billStatus' or len(root.findall('bill'))!=1:
        result['errors'].append('unsupported_root_or_bill_cardinality');return result
    bill=root.find('bill')
    def one(path):
        nodes=bill.findall(path)
        if len(nodes)!=1 or len(nodes[0]):
            raise ValueError('Missing/ambiguous scalar field: '+path)
        return (nodes[0].text or '').strip()
    try:
        legacy=bool(bill.findall('billNumber') or bill.findall('billType'))
        modern=bool(bill.findall('number') or bill.findall('type'))
        if legacy==modern:
            raise ValueError('Ambiguous/unknown identity schema')
        number=one('billNumber' if legacy else 'number')
        kind=one('billType' if legacy else 'type').lower()
        # Official old documentation uses H for House bills, current schema uses HR.
        if kind=='h':kind='hr'
        congress=one('congress');introduced=one('introducedDate')
        if (number,kind,congress)!=(str(case['bill_number']),case['bill_type'],str(case['congress'])):
            raise ValueError('XML/requested identity mismatch')
        if not date_check(introduced):
            raise ValueError('Invalid introduction date')
        result.update(identity_valid=True,introduced_at=introduced,identity_schema='legacy' if legacy else 'modern')
        start=datetime.date(1789+2*(case['congress']-1),1,3);end=datetime.date(start.year+2,1,3)
        intro=datetime.date.fromisoformat(introduced);cut=intro+datetime.timedelta(days=180)
        result.update(introduction_in_calendar_congress=start<=intro<end,day180_date=cut.isoformat(),day180_before_congress_end=cut<end)
    except ValueError as error:
        result['errors'].append(str(error))
    # Values are only read from explicitly allowed dates and text-version metadata.
    for name,path in [('actions','actions/item'),('sponsors','sponsors/item'),('cosponsors','cosponsors/item'),('text_versions','textVersions/item')]:
        nodes=bill.findall(path)
        container=bill.find(path.rsplit('/',1)[0])
        result[name]={'container_present':container is not None,'item_count':len(nodes)}
    action_dates=[(node.text or '').strip() for node in bill.findall('actions/item/actionDate')]
    result['actions'].update(date_count=len(action_dates),valid_date_count=sum(date_check(d) for d in action_dates))
    result['sponsors']['bioguide_identifier_count']=len(bill.findall('sponsors/item/bioguideId'))+len(bill.findall('sponsors/item/identifiers/bioguideId'))
    joins=[(node.text or '').strip() for node in bill.findall('cosponsors/item/sponsorshipDate')]
    withdrawn=[(node.text or '').strip() for node in bill.findall('cosponsors/item/sponsorshipWithdrawnDate')]
    result['cosponsors'].update(join_date_count=len(joins),valid_join_date_count=sum(date_check(d) for d in joins),withdrawal_date_count=len(withdrawn),valid_withdrawal_date_count=sum(date_check(d) for d in withdrawn))
    versions=[]
    for node in bill.findall('textVersions/item'):
        record={}
        for name in ('date','type'):
            values=node.findall(name)
            record[name]=[(v.text or '').strip() for v in values]
        record['source_urls']=[(v.text or '').strip() for v in node.findall('formats/item/url')]
        record['url_count']=len(record['source_urls'])
        record['all_urls_http']=all(urllib.parse.urlparse(u).scheme in ('http','https') for u in record['source_urls'])
        versions.append(record)
    result['text_versions']['records']=versions
    return result


def fetch_case(case,output,opener):
    bid=case['bill_id'];intent=dict(bill_id=bid,url=case['url'],max_response_bytes=CAP,timeout_seconds=20,
                                  requested_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
    common.save(output/(bid+'-intent.json'),intent)
    receipt=dict(intent);raw=b''
    try:
        request=urllib.request.Request(case['url'],headers={'User-Agent':'Momentum-source-readiness/1','Accept-Encoding':'identity'})
        try:
            response=opener.open(request,timeout=20)
        except urllib.error.HTTPError as error:
            response=error
        with response:
            receipt.update(status=response.status,headers=dict(response.headers))
            raw=response.read(CAP+1)
        with (output/(bid+'.xml')).open('xb') as stream:stream.write(raw)
        receipt.update(bytes=len(raw),sha256=common.digest(raw),truncated=len(raw)>CAP)
        if receipt['status']!=200:
            raise ValueError('Non-200 response')
        if len(raw)>CAP:
            raise ValueError('Response exceeded byte cap; sentinel retained')
        parsed=inspect_xml(raw,case)
        common.save(output/(bid+'-inspection.json'),parsed)
        receipt.update(parsed=True,identity_valid=parsed['identity_valid'],inspection_errors=parsed['errors'])
    except Exception as error:
        receipt.update(error_type=type(error).__name__,error=str(error),parsed=False)
    common.save(output/(bid+'-receipt.json'),receipt)
    return receipt


def run(output):
    output.mkdir(parents=True,exist_ok=False)
    index_path=DIRECTORY/'result.json';index=json.loads(index_path.read_text())
    pages={};bindings={str(index_path):common.digest(index_path.read_bytes())}
    for congress in range(113,119):
        for kind in ('hr','s'):
            path=HTML_DIRECTORY/f'{congress}-{kind}.html';pages[f'{congress}-{kind}']=path.read_text();bindings[str(path)]=common.digest(path.read_bytes())
    population,sample=population_and_sample(index,pages)
    for path in [pathlib.Path(__file__),pathlib.Path(common.__file__),pathlib.Path('tests/test_official_billstatus_readiness_v1.py'),pathlib.Path('tests/test_official_readiness_independent.py'),pathlib.Path('docs/research/OFFICIAL_BILLSTATUS_READINESS_V1.md')]:
        bindings[str(path)]=common.digest(path.read_bytes())
    common.save(output/'registration.json',dict(version=VERSION,input_and_code_sha256=bindings,population_count=len(population),sample=sample,
        request_limit=100,body_cap_per_response=CAP,sentinel_bytes=1,retries=0,redirects=0,timeout_seconds=20,
        sample_rule='first100 SHA256(official-billstatus-readiness-v1 + newline + canonicalbillid)',
        source_change='Adaptive official-directory sample independent of failed BICAM metadata gates; not a BICAM pass',
        purpose='Source-readiness only, not confirmatory prediction evaluation',model_fits=0))
    opener=urllib.request.build_opener(common.NoRedirect)
    receipts=[fetch_case(case,output,opener) for case in sample]
    counts=collections.Counter(str(r.get('status','transport_error')) for r in receipts)
    common.save(output/'result.json',dict(version=VERSION,population_count=len(population),sample_count=len(sample),request_count=len(receipts),
        http_status_counts=dict(counts),response_bytes=sum(r.get('bytes',0) for r in receipts),parsed=sum(r.get('parsed',False) for r in receipts),
        identity_valid=sum(r.get('identity_valid',False) for r in receipts),errors=[{'bill_id':r['bill_id'],'error':r.get('error'),'inspection_errors':r.get('inspection_errors',[])} for r in receipts if r.get('error') or r.get('inspection_errors')],
        model_fits=0,labels_extracted=0,historical_availability_certified=False,official_population_completeness_certified=False))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=pathlib.Path,required=True);run(parser.parse_args().output)
