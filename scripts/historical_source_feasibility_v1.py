"""Fixed eight-case public-route feasibility study, never historical certification."""
import argparse
import hashlib
import io
import json
import time
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime,timezone
from pathlib import Path
from engine.store import ROOT
from engine.paper_evaluation import require
from scripts.run_mechanism_design_extractor import BASE,read,persist

AUDIT=BASE/'historical-text-eligibility-20261108-v1/audit.json'
AUDIT_HASH='4f8db6a2506056554f9220a641e9ffc2264d01565335d3bf4022fb4dd4d0a178'
MAX_BYTES=20_000_000
MAX_UNCOMPRESSED=50_000_000
CODE=['scripts/historical_source_feasibility_v1.py','tests/test_historical_source_feasibility_v1.py',
      'tests/test_historical_source_feasibility_independent.py','scripts/run_mechanism_design_extractor.py',
      'scripts/paper_review_packet.py','scripts/mechanism_design_extractor.py','engine/paper_evaluation.py','engine/store.py']

def sha(raw):return hashlib.sha256(raw).hexdigest()
def now():return datetime.now(timezone.utc).isoformat()
def local(tag):return tag.rsplit('}',1)[-1]

def xml_root(raw):
    require(b'\x00' not in raw and not raw.startswith((b'\xff\xfe',b'\xfe\xff')), 'Only UTF-8 compatible metadata accepted')
    require(b'<!DOCTYPE' not in raw.upper() and b'<!ENTITY' not in raw.upper(),'DTD/entity metadata forbidden')
    try:return ET.fromstring(raw)
    except ET.ParseError as e:raise ValueError('Invalid metadata XML') from e

def objects(raw):
    root=xml_root(raw)
    require(local(root.tag)=='premis','Not PREMIS metadata')
    output=[]
    for obj in root:
        if local(obj.tag)!='object':continue
        def values(tag):return [(n.text or '').strip() for n in obj.iter() if local(n.tag)==tag]
        identifiers=values('objectIdentifierValue')
        require(len(identifiers)==1 and bool(identifiers[0]),'Ambiguous or empty object identity')
        digests=[]
        for fixity in obj.iter():
            if local(fixity.tag)=='fixity':
                keys=[local(n.tag) for n in fixity]
                require(len(keys)==len(set(keys)), 'Ambiguous fixity fields')
                fs={local(n.tag):(n.text or '').strip() for n in fixity}
                digests.append(dict(algorithm=fs.get('messageDigestAlgorithm'),digest=fs.get('messageDigest')))
        output.append(dict(id=identifiers[0],formats=values('formatName'),digests=digests,
            sizes=values('size'),locations=values('contentLocationValue'),names=values('originalName')))
    require(len({o['id'] for o in output})==len(output),'Duplicate object ID')
    return output


def inspect_zip(raw,package):
    try:z=zipfile.ZipFile(io.BytesIO(raw))
    except zipfile.BadZipFile as e:raise ValueError('Not a valid ZIP') from e
    with z:
        infos=z.infolist()
        require(len(infos)<=256,'Too many ZIP members')
        require(len({i.filename for i in infos})==len(infos),'Duplicate ZIP names')
        require(sum(i.file_size for i in infos)<=MAX_UNCOMPRESSED,'ZIP decompression budget exceeded')
        members=[];premis=[];manifests=[]
        for info in infos:
            require(not info.filename.startswith('/') and '..' not in Path(info.filename).parts,'Unsafe ZIP member')
            require(not (info.flag_bits&1),'Encrypted ZIP unsupported')
            if info.is_dir():continue
            with z.open(info) as f:body=f.read(MAX_UNCOMPRESSED+1)
            require(len(body)==info.file_size and len(body)<=MAX_UNCOMPRESSED,'ZIP member size mismatch')
            members.append(dict(name=info.filename,bytes=len(body),sha256=sha(body),md5=hashlib.md5(body).hexdigest(),sha1=hashlib.sha1(body).hexdigest()))
            if Path(info.filename).name.lower()=='premis.xml':
                premis.extend(objects(body))
            if Path(info.filename).name.lower() in ('dip.xml','mets.xml','aip.xml','acp.xml'):
                root=xml_root(body)
                manifests.append(dict(name=info.filename,root=local(root.tag),attributes=dict(root.attrib),
                    file_entries=[dict(n.attrib) for n in root.iter() if local(n.tag)=='file']))
        require(any(any(part == package or Path(part).stem == package for part in Path(m['name']).parts) for m in members),'ZIP package identity absent')
    return dict(members=members,premis_objects=premis,manifests=manifests)


def assess(record,premis_objects,archive):
    old_ids={o['id'] for o in record['xml_objects'] if o['digest'] is None}
    require(len(old_ids)==2,'Expected two unresolved historical XML objects')
    combined=premis_objects+archive.get('premis_objects',[])
    candidates=[];matches=[]
    for obj in combined:
        if obj['id'] not in old_ids:continue
        for d in obj['digests']:
            algorithm=(d.get('algorithm') or '').lower().replace('-','')
            value=(d.get('digest') or '').lower()
            valid=algorithm in ('sha256','sha1','md5') and len(value)=={'sha256':64,'sha1':40,'md5':32}[algorithm] and all(c in '0123456789abcdef' for c in value)
            candidates.append(dict(object_id=obj['id'],algorithm=d.get('algorithm'),digest=d.get('digest'),supported_valid_digest=valid))
            if valid:
                for m in archive.get('members',[]):
                    if m[algorithm]==value:matches.append(dict(object_id=obj['id'],member=m['name'],algorithm=algorithm,digest=value))
    unique={json.dumps(d,sort_keys=True):d for d in candidates}
    current=[m['name'] for m in archive.get('members',[]) if m['sha256']==record['current_source']['sha256']]
    return dict(bill_id=record['bill_id'],package=record['package'],cutoff=record['cutoff'],old_object_ids=sorted(old_ids),
        recovered_digest_records=list(unique.values()),old_digest_member_matches=matches,current_xml_matching_members=current,
        historical_public_access_proven=False,historical_feature_eligible=False,
        disposition='unresolved_public_access_chain' if matches else 'unresolved_historical_object_digest_or_bytes',
        reason='A current public ZIP or PREMIS response does not by itself bind recovered bytes to public access before the historical cutoff; preserve candidates for independent evidence review.')


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):return None


def fetch(url):
    require(url.startswith('https://www.govinfo.gov/'),'Official HTTPS route required')
    started=now();start=time.monotonic();body=b'';status=None;headers={};error=None;chunks=[];size=0
    opener=urllib.request.build_opener(NoRedirect())
    try:
        request=urllib.request.Request(url,headers={'User-Agent':'Momentum-research-source-feasibility/1.0','Accept-Encoding':'identity'})
        try:response=opener.open(request,timeout=15)
        except urllib.error.HTTPError as e:response=e
        with response:
            status=response.code
            headers={k:v for k,v in response.headers.items() if k.lower() in ('content-type','content-length','last-modified','etag','retry-after','location','date')}
            while True:
                require(time.monotonic()-start<=30,'Response time budget exceeded')
                require(size<MAX_BYTES,'Response byte budget reached')
                chunk=response.read(min(65536,MAX_BYTES-size))
                if not chunk:break
                chunks.append(chunk);size+=len(chunk)
                require(size<=MAX_BYTES,'Response byte budget exceeded')
            body=b''.join(chunks)
    except Exception as e:
        error=type(e).__name__+': '+str(e)
    body=b''.join(chunks)
    return body,dict(url=url,started_at=started,completed_at=now(),status=status,headers=headers,
        bytes=len(body),sha256=sha(body),error=error,redirects_followed=0,attempts=1)


def run(directory):
    ae,a=read(AUDIT);require(ae['hash']==AUDIT_HASH,'Audit changed');records=a['records']
    require(len(records)==8 and len({r['bill_id'] for r in records})==8,'Exactly eight cases required')
    routes=[]
    for r in records:
        routes.extend([dict(bill_id=r['bill_id'],kind='premis',url=r['metadata']['premis.xml']['url']),
                       dict(bill_id=r['bill_id'],kind='zip',url='https://www.govinfo.gov/content/pkg/'+r['package']+'.zip')])
    inputs={str(AUDIT.relative_to(ROOT)):sha(AUDIT.read_bytes())}
    for r in records:
        for m in r['metadata'].values():
            p=ROOT/m['path'];require(sha(p.read_bytes())==m['sha256'] and p.stat().st_size==m['bytes'],'Prior metadata changed');inputs[m['path']]=m['sha256']
    code={p:sha((ROOT/p).read_bytes()) for p in CODE}
    directory=Path(directory).resolve();require(ROOT/'data' in directory.parents,'Runtime output required');directory.mkdir(parents=True,exist_ok=True)
    reg=persist(directory/'registration.json',dict(version='historical-source-feasibility-v1',audit_hash=ae['hash'],
        cases=[dict(bill_id=r['bill_id'],package=r['package'],cutoff=r['cutoff'],old_object_ids=[o['id'] for o in r['xml_objects'] if o['digest'] is None]) for r in records],
        routes=routes,input_files=inputs,code_sha256=code,budget=dict(requests=16,retries=0,redirects=0,response_bytes=MAX_BYTES,zip_uncompressed_bytes=MAX_UNCOMPRESSED,zip_members=256,study_seconds=900,socket_timeout_seconds=15,response_check_seconds=30),
        question='Do refreshed public PREMIS and package ZIP expose the missing historical XML object digests/bytes and an auditable pre-cutoff access chain?',
        routing_source='https://github.com/usgpo/api/wiki/Transition-Guide',
        rule='No replacement cases, extra routes, automatic retries or history certification from package dates/current byte equality. Failed and unresolved cases retained.',
        quality_access=False,outcome_access=False,model_fitting=False))
    clock_path=directory/'acquisition-clock.json'
    if clock_path.exists():_,clock=read(clock_path)
    else:clock=dict(started_epoch=time.time(),study_seconds=900);persist(clock_path,clock)
    receipts=[];parsed={r['bill_id']:{} for r in records}
    for index,route in enumerate(routes):
        path=directory/f'request-{index:02d}.json';rawpath=directory/f'request-{index:02d}.raw'
        if path.exists():
            _,receipt=read(path);require(receipt['url']==route['url'],'Receipt route mismatch');body=rawpath.read_bytes();require(sha(body)==receipt['sha256'],'Receipt bytes mismatch')
        else:
            intent=directory/f'request-{index:02d}-intent.json'
            if intent.exists() or rawpath.exists():
                body=rawpath.read_bytes() if rawpath.exists() else b''
                receipt=dict(url=route['url'],status=None,bytes=len(body),sha256=sha(body),error='Interrupted request; no retry permitted',attempts=1)
            elif time.time()-clock['started_epoch']>900:
                body=b'';receipt=dict(url=route['url'],status=None,bytes=0,sha256=sha(b''),error='Study budget exhausted',attempts=0)
            else:
                persist(intent,dict(url=route['url'],attempt=1,started_at=now()))
                body,receipt=fetch(route['url'])
            if not rawpath.exists():rawpath.write_bytes(body)
            persist(path,receipt)
        row=dict(route,receipt_hash=read(path)[0]['hash'],status=receipt['status'],error=receipt['error'])
        if receipt['status']==200 and not receipt['error']:
            try:
                rec=next(r for r in records if r['bill_id']==route['bill_id'])
                parsed[route['bill_id']][route['kind']]=objects(body) if route['kind']=='premis' else inspect_zip(body,rec['package'])
                row['parsed']=True
            except (ValueError,zipfile.BadZipFile,RuntimeError,NotImplementedError,EOFError,OSError) as e:row.update(parsed=False,parse_error=str(e))
        else:row['parsed']=False
        receipts.append(row);print(route['bill_id'],route['kind'],row['status'],row['parsed'],flush=True)
    dispositions=[assess(r,parsed[r['bill_id']].get('premis',[]),parsed[r['bill_id']].get('zip',{})) for r in records]
    for r in records:persist(directory/(r['bill_id']+'-inventory.json'),parsed[r['bill_id']])
    require(all(sha((ROOT/p).read_bytes())==h for p,h in {**inputs,**code}.items()),'Frozen inputs/code changed')
    return persist(directory/'result.json',dict(registration_hash=reg['hash'],routes=receipts,cases=dispositions,
        counts=dict(cases=8,routes=16,http_200=sum(x['status']==200 for x in receipts),parsed=sum(x['parsed'] for x in receipts),
          cases_with_old_digest=sum(bool(x['recovered_digest_records']) for x in dispositions),cases_with_old_member_match=sum(bool(x['old_digest_member_matches']) for x in dispositions),historically_eligible=0),
        historical_feature_eligible=False,quality_access=False,outcome_access=False,model_fitting=False))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    r=run(p.parse_args().output);print(r['hash']);print(r['body']['counts'])
