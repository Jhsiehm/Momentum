"""Read-only replay of bill-context preparation; does not open quality text."""
import argparse
import hashlib
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from engine.paper_evaluation import seal, unseal, require
from engine.cohort import family_groups
from engine.store import ROOT, digest
from scripts.cross_congress_evaluate import load_rows
from scripts.paper_readiness_audit import audit
from scripts.paper_review_packet import persist_or_compare

def validate_bindings(directory, spec, result, rows, groups, read):
    """Reconstruct authoritative identities and folds, not just internal arithmetic."""
    from scripts.bill_context_execution import MECHANISMS, select_pilot, xml_url, calendar_features, stage_status
    from scripts.cross_congress_evaluate import D, make_split
    from scripts.paper_review_packet import packet
    selected, dispositions = select_pilot(rows, groups)
    require(read('disposition.json') == dispositions, 'Disposition ledger mismatch')
    expected_packet = packet(selected, [D/'sources', ROOT/'data/research-runs/cross-congress-reserve-20261105/sources'], ROOT)
    require(read('source-packet.json') == expected_packet, 'Source packet binding mismatch')
    failures = []
    acquired = parsed = 0
    for row, evidence in zip(selected, expected_packet['records']):
        record = read('records/'+row['bill_id']+'.json')
        for key in ('bill_id', 'congress', 'family_id', 'partition', 'cutoff'):
            require(record[key] == row[key], 'Record identity/cutoff mismatch: '+key)
        require(record['attributes'] == {k:dict(value=None,status='unknown') for k in MECHANISMS}, 'Attribute schema mismatch')
        if 'source' in record:
            acquired += 1
            package, url = xml_url(evidence, ROOT)
            require(record['package'] == package and record['source']['url'] == url, 'Record version/source mismatch')
            require(record['parser_sha256'] == spec['code_sha256'], 'Parser hash mismatch')
            require(record['original_availability'] == 'unverified', 'Uncertified historical availability')
            if row['partition'] == 'quality':
                require(record.get('quality_content') == 'Retained raw only; extraction and annotations unopened until design freeze', 'Quality firewall marker mismatch')
        if 'design_extraction' in record:
            require('source' in record and row['partition'] == 'design', 'Unbound design extraction')
            parsed += 1
            raw=(directory/'sources'/(hashlib.sha256(record['source']['url'].encode()).hexdigest()+'.raw')).read_bytes()
            xml=ET.fromstring(raw)
            for node in xml.iter(): node.tag=node.tag.rsplit('}',1)[-1]
            import re
            form=xml.find('form')
            require(xml.tag=='bill' and form is not None, 'Invalid bill XML')
            match=re.fullmatch(r'\s*(\d+)(?:st|nd|rd|th)?\s+CONGRESS\s*', form.findtext('congress',''), re.IGNORECASE)
            require(match is not None and int(match.group(1))==row['congress'], 'XML Congress mismatch')
            require(re.sub(r'[^a-z0-9]','',form.findtext('legis-num','').lower())==row['bill_id'].split('-',1)[1], 'XML bill identity mismatch')
            extraction=record['design_extraction']
            expected_sections=[dict(index=i,xml_id=node.get('id'),text=''.join(node.itertext()),text_sha256=hashlib.sha256(''.join(node.itertext()).encode()).hexdigest()) for i,node in enumerate(xml.iter('section'))]
            require(extraction['sections']==expected_sections, 'Section coordinates/content mismatch')
            require(extraction['status']=='unreviewed_design_only', 'Extraction status mismatch')
            require(extraction['mechanism_labels']=={k:None for k in MECHANISMS}, 'Mechanism schema mismatch')
            expected_hits={name:[dict(start=m.start(),end=m.end(),quote=m.group()) for m in re.finditer(pattern,extraction['text'],re.IGNORECASE)] for name,pattern in MECHANISMS.items()}
            require(extraction['lexical_candidates']==expected_hits, 'Lexical candidate mismatch')
        if 'blocked_reason' in record:
            failures.append(dict(bill_id=row['bill_id'],error=record['blocked_reason']))
        require('source' in record or 'blocked_reason' in record, 'Unexplained missing source')
    require(result['failures']==failures, 'Failure ledger mismatch')
    require((result['selected'],result['design'],result['quality'])==(100,50,50), 'Selection counts mismatch')
    require(result['acquired_texts']==acquired and result['design_parsed']==parsed, 'Extraction count mismatch')
    require(result['release_eligible'] is False and result['independent_validation'] is False and result['frozen_artifacts_unchanged'] is True, 'Invalid validation/eligibility claims')
    encoding=read('e1-unapproved-inputs.json')
    require(set(encoding)=={'115','116','117'}, 'Missing/extra E1 folds')
    fold_checks={}
    for c in (115,116,117):
        train,test=make_split(rows,c,groups)
        saved=json.loads((D/f'fold-{c}.json').read_text())
        models=json.loads((D/f'fold-{c}-models.json').read_text())
        require(digest(models)==saved['models_hash'], 'Legacy model hash mismatch')
        require([r['bill_id'] for r in train]==saved['training_ids'] and [r['bill_id'] for r in test]==[r['bill_id'] for r in saved['predictions']], 'Legacy fold membership mismatch')
        old=models['calibrated_all_history']; scope=train+test
        expected=dict(core_ids=old['core_ids'],calibration_ids=old['calibration_ids'],evaluation_ids=[r['bill_id'] for r in test],rows=[dict(bill_id=r['bill_id'],cutoff=r['cutoff'],features={arm:calendar_features(r,arm) for arm in ('control','time','interaction')}) for r in scope])
        require(encoding[str(c)]==expected, 'E1 authoritative fold/feature mismatch')
        pending=sum(any(not v.get('introduction_validation',{}).get('human_audit_satisfied',False) for v in r['versions'] if v['package'] in r['eligible_packages']) for r in scope)
        fold_checks[str(c)]=dict(training=len(train),evaluation=len(test),pending_introduction_review_rows=pending,subject_bound_review_rows=sum(bool(r.get('review')) for r in scope),membership_matches=True,temporal_order=max(r['label_available_at'] for r in train)<min(r['cutoff'] for r in test),family_disjoint=not bool({r['family_id'] for r in train}&{r['family_id'] for r in test}),reviewed_positive_family_gate='not established; methods signoff required')
    require(result['stages']==stage_status(fold_checks,acquired), 'Stage disposition mismatch')
    expected_queue=[dict(bill_id=r['bill_id'],partition=r['partition'],annotator_1=None,annotator_2=None,adjudicator=None,status='pending',labels={k:None for k in MECHANISMS}) for r in selected]
    require(read('annotation-queue.json')==expected_queue, 'Annotation queue mismatch')


def verify(directory):
    directory = Path(directory)

    def read(name):
        return unseal(json.loads((directory / name).read_text()))
    registration = json.loads((directory / 'registration.json').read_text())
    spec = unseal(registration)
    result = read('result.json')
    require(result['protocol_hash'] == registration['hash'], "Bill-context verification failed: result['protocol_hash'] == registration['hash']")
    require(hashlib.sha256((ROOT / 'scripts/bill_context_execution.py').read_bytes()).hexdigest() == spec['code_sha256'], "Bill-context verification failed: hashlib.sha256((ROOT / 'scripts/bill_context_execution.py').read_bytes()).hexdigest() == spec['code_sha256']")
    require(hashlib.sha256((ROOT / 'docs/research/BILL_CONTEXT_EXPERIMENT_PLAN_V1.md').read_bytes()).hexdigest() == spec['plan_sha256'], "Bill-context verification failed: hashlib.sha256((ROOT / 'docs/research/BILL_CONTEXT_EXPERIMENT_PLAN_V1.md').read_bytes()).hexdigest() == spec['plan_sha256']")
    for (path, hashed) in spec['dependencies'].items():
        require(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == hashed, 'Bill-context verification failed: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == hashed')
    require(audit() == spec['frozen_audit'], "Bill-context verification failed: audit() == spec['frozen_audit']")
    rows = load_rows()
    require(digest(rows) == spec['population_sha256'], "Bill-context verification failed: digest(rows) == spec['population_sha256']")
    groups = family_groups(rows)
    require(digest(groups) == spec['family_graph_sha256'], "Bill-context verification failed: digest(groups) == spec['family_graph_sha256']")
    dispositions = read('disposition.json')
    eligible = {r['bill_id']: r for r in dispositions}
    used = set()
    expected = []
    for c in range(113, 118):
        n = 0
        for row in sorted((r for r in rows if r['congress'] == c), key=lambda r: (digest(r['bill_id']), r['bill_id'])):
            family = eligible[row['bill_id']]['family_id']
            require(family == groups[row['bill_id']], "Bill-context verification failed: family == groups[row['bill_id']]")
            if row['exclusion'] or family in used or n >= 20:
                continue
            used.add(family)
            expected.append(dict(bill_id=row['bill_id'], family_id=family, partition='design' if n < 10 else 'quality'))
            n += 1
        require(n == 20, 'Bill-context verification failed: n == 20')
    require(expected == spec['selection'], "Bill-context verification failed: expected == spec['selection']")
    packet = read('source-packet.json')
    references = 0
    for row in packet['records']:
        sources = [row['discovery_source']] + [s for v in row['versions'] for s in v['sources']]
        for source in sources:
            references += 1
            for match in source['retained_matches']:
                raw = (ROOT / match['raw_path']).read_bytes()
                receipt = (ROOT / match['receipt_path']).read_bytes()
                require(hashlib.sha256(raw).hexdigest() == source['sha256'] and len(raw) == source['bytes'], "Bill-context verification failed: hashlib.sha256(raw).hexdigest() == source['sha256'] and len(raw) == source['bytes']")
                require(hashlib.sha256(receipt).hexdigest() == match['receipt_sha256'], "Bill-context verification failed: hashlib.sha256(receipt).hexdigest() == match['receipt_sha256']")
    require(references == result['source_references'], "Bill-context verification failed: references == result['source_references']")
    acquired = design = byte_count = sections = 0
    for row in expected:
        record = read('records/' + row['bill_id'] + '.json')
        require(record['partition'] == row['partition'] and record['human_review'] == 'pending', "Bill-context verification failed: record['partition'] == row['partition'] and record['human_review'] == 'pending'")
        require(record['historical_feature_eligible'] is False, "Bill-context verification failed: record['historical_feature_eligible'] is False")
        require(all((a == dict(value=None, status='unknown') for a in record['attributes'].values())), "Bill-context verification failed: all((a == dict(value=None, status='unknown') for a in record['attributes'].values()))")
        if 'source' in record:
            source = record['source']
            key = hashlib.sha256(source['url'].encode()).hexdigest()
            raw = (directory / 'sources' / (key + '.raw')).read_bytes()
            receipt = json.loads((directory / 'sources' / (key + '.json')).read_text())
            require(receipt == source and hashlib.sha256(raw).hexdigest() == source['sha256'] and (len(raw) == source['bytes']), "Bill-context verification failed: receipt == source and hashlib.sha256(raw).hexdigest() == source['sha256'] and (len(raw) == source['bytes'])")
            acquired += 1
            byte_count += len(raw)
        if row['partition'] == 'quality':
            require('design_extraction' not in record, "Bill-context verification failed: 'design_extraction' not in record")
        elif 'design_extraction' in record:
            design += 1
            extraction = record['design_extraction']
            sections += len(extraction['sections'])
            xml = ET.fromstring(raw)
            require(''.join(xml.itertext()) == extraction['text'], "Bill-context verification failed: ''.join(xml.itertext()) == extraction['text']")
            original_sections = [''.join(e.itertext()) for e in xml.iter() if e.tag.rsplit('}', 1)[-1] == 'section']
            require(original_sections == [s['text'] for s in extraction['sections']], "Bill-context verification failed: original_sections == [s['text'] for s in extraction['sections']]")
            for section in extraction['sections']:
                require(hashlib.sha256(section['text'].encode()).hexdigest() == section['text_sha256'], "Bill-context verification failed: hashlib.sha256(section['text'].encode()).hexdigest() == section['text_sha256']")
            for hits in extraction['lexical_candidates'].values():
                for hit in hits:
                    require(extraction['text'][hit['start']:hit['end']] == hit['quote'], "Bill-context verification failed: extraction['text'][hit['start']:hit['end']] == hit['quote']")
            require(all((v is None for v in extraction['mechanism_labels'].values())), "Bill-context verification failed: all((v is None for v in extraction['mechanism_labels'].values()))")
    require(acquired == result['acquired_texts'] and design == result['design_parsed'], "Bill-context verification failed: acquired == result['acquired_texts'] and design == result['design_parsed']")
    count = 0
    for (c, fold) in read('e1-unapproved-inputs.json').items():
        require(set(fold['core_ids']).isdisjoint(fold['calibration_ids']), "Bill-context verification failed: set(fold['core_ids']).isdisjoint(fold['calibration_ids'])")
        require(set(fold['evaluation_ids']).isdisjoint(fold['core_ids'] + fold['calibration_ids']), "Bill-context verification failed: set(fold['evaluation_ids']).isdisjoint(fold['core_ids'] + fold['calibration_ids'])")
        require(set((r['bill_id'] for r in fold['rows'])) == set(fold['core_ids'] + fold['calibration_ids'] + fold['evaluation_ids']), "Bill-context verification failed: set((r['bill_id'] for r in fold['rows'])) == set(fold['core_ids'] + fold['calibration_ids'] + fold['evaluation_ids'])")
        for row in fold['rows']:
            end = datetime.fromisoformat(f'{1789 + 2 * int(c):04d}-01-03T17:00:00+00:00')
            congress = int(row['bill_id'].split('-')[0])
            end = end.replace(year=1789 + 2 * congress)
            cutoff = datetime.fromisoformat(row['cutoff'].replace('Z', '+00:00'))
            remaining = (end - cutoff).total_seconds() / 63072000
            x = row['features']['control']
            require(row['features']['time'] == x + [remaining], "Bill-context verification failed: row['features']['time'] == x + [remaining]")
            require(row['features']['interaction'] == x + [remaining, x[0] * remaining], "Bill-context verification failed: row['features']['interaction'] == x + [remaining, x[0] * remaining]")
            count += 1
    queue = read('annotation-queue.json')
    require([r['bill_id'] for r in queue] == [r['bill_id'] for r in expected], "Bill-context verification failed: [r['bill_id'] for r in queue] == [r['bill_id'] for r in expected]")
    require(all((r['annotator_1'] is None and r['annotator_2'] is None and (r['adjudicator'] is None) for r in queue)), "Bill-context verification failed: all((r['annotator_1'] is None and r['annotator_2'] is None and (r['adjudicator'] is None) for r in queue))")
    require(result['models_fitted'] == result['outcomes_scored'] == result['forecasts_issued'] == 0, "Bill-context verification failed: result['models_fitted'] == result['outcomes_scored'] == result['forecasts_issued'] == 0")
    validate_bindings(directory, spec, result, rows, groups, read)
    return dict(status='passed software/artifact checks only', source_references=references, text_files=acquired, text_bytes=byte_count, design_cases=design, design_sections=sections, calendar_rows_checked=count, quality_text_parsed=False, frozen_artifacts_unchanged=True, scientific_validation=False)
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    result = verify(args.directory)
    persist_or_compare(args.directory / 'verification.json', seal(result))
    print(json.dumps(result, indent=2))
