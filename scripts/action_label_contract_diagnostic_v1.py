"""Bounded audit of already rejected source assertions; never assigns outcome labels."""
import argparse
import collections
import json
import pathlib
import re
from scripts import bicam_inventory_audit_v1 as common
from scripts import official_context_features_v2 as frozen

VERSION='action-label-contract-diagnostic-v1'
SOURCE=pathlib.Path('data/research-runs/official-context-acquisition-v1-20261109')
FEATURES=pathlib.Path('data/research-runs/action-context-features-v1-20261109')
FAILED=pathlib.Path('data/research-runs/action-context-diagnostic-v1-20261109')
REASON='Enactment action lacks public-law identity'
PATTERN=r'Became Public Law No[.:]?\s*:?\s*(\d+-\d+)\.?'


def inspect(raw,case):
    bill,_=frozen.parsed(raw,case)
    frozen.container(bill,'laws');frozen.container(bill,'actions')
    laws=[dict(type=frozen.scalar(item,'type'),number=frozen.scalar(item,'number')) for item in bill.findall('laws/item')]
    public={r['number'] for r in laws if r['type'].lower() in ('public','public law')}
    terminals=[]
    for ordinal,item in enumerate(bill.findall('actions/item')):
        code=frozen.scalar(item,'actionCode',False)
        if code not in ('36000','E40000'):continue
        source=frozen.scalar(item,'sourceSystem/code',False);text=frozen.scalar(item,'text',False)
        when=frozen.scalar(item,'actionDate');frozen.date(when)
        match=re.fullmatch(PATTERN,text or '',re.I)
        terminals.append(dict(ordinal=ordinal,code=code,source_code=source,date=when,text=text,raw_text=item.findtext('text'),
            supported_pair=(code,source) in (('36000','9'),('E40000','2'),('E40000','9')),
            assertion_kind='public_law_identity_text' if match else 'exact_signing_text' if text=='Signed by President.' else 'other_terminal_text',
            asserted_law_number=match[1] if match else None,law_list_match=bool(match and match[1] in public)))
    concordant=[r for r in terminals if r['supported_pair'] and r['law_list_match']]
    dates={r['date'] for r in concordant};numbers={r['asserted_law_number'] for r in concordant}
    for row in terminals:row['date_matches_any_concordant_assertion']=row['date'] in dates
    problems=[r for r in terminals if r['assertion_kind']!='public_law_identity_text']
    return dict(bill_id=case['bill_id'],congress=case['congress'],laws=laws,terminal_assertions=terminals,
        concordant_assertion_count=len(concordant),concordant_date_count=len(dates),public_law_identity_count=len(public),
        concordant_numbers_equal_law_list=bool(public) and numbers==public,
        all_problem_dates_match_concordant=bool(problems) and all(r['date'] in dates for r in problems),
        diagnostic_only_not_outcome_label=True)


def select_cases(ledger,selected):
    lookup={r['bill_id']:r for r in selected}
    if len(selected)!=12000 or len(lookup)!=12000:raise ValueError('Original sample mismatch')
    ids=sorted(bid for bid,row in ledger.items() if row.get('reason')==REASON)
    if len(ids)!=231:raise ValueError('Fixed rejected-case denominator changed')
    if any(ledger[bid].get('bill_id')!=bid or ledger[bid].get('y') is not None or bid not in lookup for bid in ids):raise ValueError('Rejected case binding mismatch')
    return [lookup[bid] for bid in ids]


def run(output):
    output.mkdir(parents=True,exist_ok=False)
    registration=json.loads((FEATURES/'registration.json').read_text())
    ledger=json.loads((FAILED/'label-ledger.json').read_text())
    selected=select_cases(ledger,registration['selected'])
    for name,sha in registration['inputs'].items():
        if common.digest(pathlib.Path(name).read_bytes())!=sha:raise ValueError('Frozen input changed: '+name)
    paths=[FEATURES/'registration.json',FAILED/'registration.json',FAILED/'failure.json',FAILED/'label-ledger.json',
        pathlib.Path(__file__),pathlib.Path(frozen.__file__),pathlib.Path(frozen.v1.__file__),pathlib.Path(frozen.v1.audit.__file__),
        pathlib.Path('tests/test_action_label_contract_v1.py'),pathlib.Path('tests/test_action_label_contract_independent.py'),pathlib.Path('docs/research/ACTION_LABEL_CONTRACT_DIAGNOSTIC_V1.md')]
    hashes={r['bill_id']:registration['source_hashes'][r['bill_id']] for r in selected}
    common.save(output/'registration.json',dict(version=VERSION,selected=selected,source_hashes=hashes,inputs={str(p):common.digest(p.read_bytes()) for p in paths},
        selection_reason=REASON,exposure='Exactly231already-rejected cases; first hr1071-113 source shape seen before design; adaptive source-contract audit',new_labels=0,model_fits=0,network_requests=0))
    cases=[];errors=[];cross=collections.Counter()
    for case in selected:
        bid=case['bill_id']
        try:
            raw=(SOURCE/'sources'/(bid+'.xml')).read_bytes()
            if common.digest(raw)!=hashes[bid]:raise ValueError('Raw source binding changed')
            row=inspect(raw,case);cases.append(row)
            for item in row['terminal_assertions']:
                cross[(item['code'],item['source_code'],item['assertion_kind'],str(item['date_matches_any_concordant_assertion']))]+=1
        except Exception as error:errors.append(dict(bill_id=bid,error=type(error).__name__+': '+str(error)))
    common.save(output/'cases.json',cases);common.save(output/'errors.json',errors)
    common.save(output/'result.json',dict(version=VERSION,selected=231,inspected=len(cases),errors=len(errors),
        cases_with_concordant_assertions=sum(r['concordant_assertion_count']>0 for r in cases),
        cases_single_concordant_date=sum(r['concordant_date_count']==1 for r in cases),
        cases_all_problem_dates_match=sum(r['all_problem_dates_match_concordant'] for r in cases),
        terminal_assertion_cross_tab=[dict(code=k[0],source_code=k[1],assertion_kind=k[2],date_agreement=k[3],assertions=n) for k,n in sorted(cross.items(),key=lambda x:str(x[0]))],
        new_labels=0,model_fits=0,network_requests=0))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True,type=pathlib.Path);run(parser.parse_args().output)
