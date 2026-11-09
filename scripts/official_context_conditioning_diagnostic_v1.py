"""Registered post-failure source-feature conditioning audit; no new labels/fits."""
import argparse
import collections
import json
import pathlib
import re
import urllib.parse
import xml.etree.ElementTree as ET
from scripts import bicam_inventory_audit_v1 as common

VERSION='official-context-conditioning-diagnostic-v1'
SOURCE=pathlib.Path('data/research-runs/official-context-acquisition-v1-20261109')
FEATURES=pathlib.Path('data/research-runs/official-context-features-v2-20261109')
FAILED_FIT=pathlib.Path('data/research-runs/official-context-diagnostic-v2-20261109')
CODES={'ih','is','rh','rs','eh','es','enr'}


def inspect(raw,case,feature):
    if b'\x00' in raw or b'<!DOCTYPE' in raw.upper() or b'<!ENTITY' in raw.upper():raise ValueError('Unsafe XML')
    root=ET.fromstring(raw);bills=root.findall('bill')
    if root.tag!='billStatus' or len(bills)!=1:raise ValueError('Invalid source root')
    bill=bills[0]
    if bill.findtext('congress')!=str(case['congress']) or bill.findtext('number')!=str(case['bill_number']) or bill.findtext('type','').lower()!=case['bill_type']:
        raise ValueError('Source identity mismatch')
    law_containers=bill.findall('laws');public=[];law_issues=[]
    if len(law_containers)>1 or any(child.tag!='item' for node in law_containers for child in node):law_issues.append('unsupported_law_container')
    for item in bill.findall('laws/item'):
        types=item.findall('type');numbers=item.findall('number')
        if len(types)!=1 or len(numbers)!=1 or len(types[0]) or len(numbers[0]):law_issues.append('ambiguous_law_item');continue
        kind=(types[0].text or '').strip().lower();number=(numbers[0].text or '').strip()
        if kind in ('public','public law'):
            public.append(number)
            if not re.fullmatch(str(case['congress'])+r'-[1-9][0-9]*',number):law_issues.append('public_law_identity_format')
        elif kind not in ('private','private law'):law_issues.append('unknown_law_type')
    if len(set(public))>1:law_issues.append('multiple_public_law_identities')
    category='public_law_assertion' if public else 'no_public_law_assertion'
    if law_issues:category='ambiguous_law_metadata'
    editions=[]
    prefix=f"BILLS-{case['congress']}{case['bill_type']}{case['bill_number']}"
    for ordinal,item in enumerate(bill.findall('textVersions/item')):
        codes=set()
        for node in item.findall('formats/item/url'):
            parsed=urllib.parse.urlparse(node.text or '')
            match=re.search(r'/pkg/('+re.escape(prefix)+r'([a-z]+)\d*)/',parsed.path)
            if match and match[2]in CODES:codes.add(match[2])
        if not codes:continue
        dates=item.findall('date');values=[(node.text or '').strip()for node in dates]
        status='absent' if not dates else 'multiple' if len(dates)>1 else 'empty' if not values[0] else 'present'
        editions.append(dict(ordinal=ordinal,codes=sorted(codes),date_status=status,date_values=values,
                             version_types=[(node.text or '').strip()for node in item.findall('type')]))
    return dict(bill_id=case['bill_id'],congress=case['congress'],assertion_category=category,public_law_numbers=sorted(set(public)),law_metadata_issues=law_issues,
                anchor_valid=feature['anchor'] is not None,feature_errors=feature['feature_errors'],stage=feature['stage'],recognized_edition_metadata=editions,
                historical_eligibility=False,diagnostic_only_not_new_training_label=True)


def run(output):
    output.mkdir(parents=True,exist_ok=False)
    registration=json.loads((FEATURES/'registration.json').read_text());selected=registration['selected']
    if len(selected)!=12000 or len({r['bill_id']for r in selected})!=12000:raise ValueError('Fixed population changed')
    paths=[SOURCE/'registration.json',FEATURES/'registration.json',FEATURES/'result.json',FEATURES/'population-ledger.json',
           FAILED_FIT/'registration.json',FAILED_FIT/'failure.json',pathlib.Path(__file__),
           pathlib.Path('tests/test_official_context_conditioning_v1.py'),pathlib.Path('docs/research/OFFICIAL_CONTEXT_CONDITIONING_DIAGNOSTIC_V1.md')]
    inputs={str(p):common.digest(p.read_bytes())for p in paths}
    for case in selected:
        path=FEATURES/'features'/(case['bill_id']+'.json');inputs[str(path)]=common.digest(path.read_bytes())
    common.save(output/'registration.json',dict(version=VERSION,inputs=inputs,source_sha256=registration['source_hashes'],selected=selected,
        hypothesis='Current own-public-law assertions may be disproportionately excluded by the frozen publication-anchor reconstruction',
        exposure='Post-failure widened outcome metadata exposure over the original12000; not confirmation or model evaluation',
        model_fits=0,network_requests=0,new_training_labels=0))
    cases=[];cross=collections.Counter();missing=collections.Counter();errors=collections.Counter()
    for case in selected:
        bid=case['bill_id'];raw=(SOURCE/'sources'/(bid+'.xml')).read_bytes()
        if common.digest(raw)!=registration['source_hashes'][bid]:raise ValueError('Source changed')
        feature=json.loads((FEATURES/'features'/(bid+'.json')).read_text())
        if feature['bill_id']!=bid or feature['source_sha256']!=registration['source_hashes'][bid]:raise ValueError('Feature/source mismatch')
        row=inspect(raw,case,feature);cases.append(row)
        cross[(str(row['congress']),row['assertion_category'],'anchor_valid' if row['anchor_valid']else'anchor_ineligible')]+=1
        for error in row['feature_errors']:errors[(row['assertion_category'],error)]+=1
        for edition in row['recognized_edition_metadata']:
            for code in edition['codes']:missing[(row['assertion_category'],code,edition['date_status'])]+=1
    cases_sha=common.save(output/'cases.json',cases)
    common.save(output/'result.json',dict(version=VERSION,n=len(cases),cases_sha256=cases_sha,
        cross_tab=[dict(congress=c,assertion_category=a,eligibility=e,n=n)for(c,a,e),n in sorted(cross.items())],
        feature_errors=[dict(assertion_category=a,error=e,n=n)for(a,e),n in sorted(errors.items())],
        edition_date_counts=[dict(assertion_category=a,edition_code=c,date_status=s,n=n)for(a,c,s),n in sorted(missing.items())],
        network_requests=0,model_fits=0,new_training_labels=0,source_feature_rules_changed=False))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=pathlib.Path,required=True);run(parser.parse_args().output)
