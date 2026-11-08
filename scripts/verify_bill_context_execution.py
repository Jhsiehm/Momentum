"""Read-only replay of bill-context preparation; does not open quality text."""
import argparse
import hashlib
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

from engine.paper_evaluation import seal, unseal
from engine.cohort import family_groups
from engine.store import ROOT, digest
from scripts.cross_congress_evaluate import load_rows
from scripts.paper_readiness_audit import audit
from scripts.paper_review_packet import persist_or_compare


def verify(directory):
    directory = Path(directory)
    def read(name):
        return unseal(json.loads((directory/name).read_text()))
    registration = json.loads((directory/'registration.json').read_text())
    spec = unseal(registration); result = read('result.json')
    assert result['protocol_hash'] == registration['hash']
    assert hashlib.sha256((ROOT/'scripts/bill_context_execution.py').read_bytes()).hexdigest() == spec['code_sha256']
    assert hashlib.sha256((ROOT/'docs/research/BILL_CONTEXT_EXPERIMENT_PLAN_V1.md').read_bytes()).hexdigest() == spec['plan_sha256']
    for path, hashed in spec['dependencies'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == hashed
    assert audit() == spec['frozen_audit']
    rows = load_rows(); assert digest(rows) == spec['population_sha256']
    groups = family_groups(rows)
    assert digest(groups) == spec['family_graph_sha256']
    # Reconstruct the recorded selection from the complete disposition ledger.
    dispositions = read('disposition.json')
    eligible = {r['bill_id']:r for r in dispositions}
    used = set(); expected = []
    for c in range(113,118):
        n = 0
        for row in sorted((r for r in rows if r['congress']==c), key=lambda r:(digest(r['bill_id']),r['bill_id'])):
            family = eligible[row['bill_id']]['family_id']
            assert family == groups[row['bill_id']]
            if row['exclusion'] or family in used or n >= 20: continue
            used.add(family)
            expected.append(dict(bill_id=row['bill_id'],family_id=family,partition='design' if n<10 else 'quality'))
            n += 1
        assert n == 20
    assert expected == spec['selection']
    packet = read('source-packet.json'); references = 0
    for row in packet['records']:
        sources = [row['discovery_source']]+[s for v in row['versions'] for s in v['sources']]
        for source in sources:
            references += 1
            for match in source['retained_matches']:
                raw = (ROOT/match['raw_path']).read_bytes()
                receipt = (ROOT/match['receipt_path']).read_bytes()
                assert hashlib.sha256(raw).hexdigest() == source['sha256'] and len(raw)==source['bytes']
                assert hashlib.sha256(receipt).hexdigest() == match['receipt_sha256']
    assert references == result['source_references']
    acquired = design = byte_count = sections = 0
    for row in expected:
        record = read('records/'+row['bill_id']+'.json')
        assert record['partition']==row['partition'] and record['human_review']=='pending'
        assert record['historical_feature_eligible'] is False
        assert all(a==dict(value=None,status='unknown') for a in record['attributes'].values())
        if 'source' in record:
            source = record['source']; key=hashlib.sha256(source['url'].encode()).hexdigest()
            raw=(directory/'sources'/(key+'.raw')).read_bytes()
            receipt=json.loads((directory/'sources'/(key+'.json')).read_text())
            assert receipt==source and hashlib.sha256(raw).hexdigest()==source['sha256'] and len(raw)==source['bytes']
            acquired+=1; byte_count+=len(raw)
        if row['partition']=='quality':
            assert 'design_extraction' not in record
        elif 'design_extraction' in record:
            design+=1; extraction=record['design_extraction']; sections+=len(extraction['sections'])
            xml=ET.fromstring(raw)
            assert ''.join(xml.itertext()) == extraction['text']
            original_sections=[''.join(e.itertext()) for e in xml.iter() if e.tag.rsplit('}',1)[-1]=='section']
            assert original_sections == [s['text'] for s in extraction['sections']]
            for section in extraction['sections']:
                assert hashlib.sha256(section['text'].encode()).hexdigest()==section['text_sha256']
            for hits in extraction['lexical_candidates'].values():
                for hit in hits: assert extraction['text'][hit['start']:hit['end']]==hit['quote']
            assert all(v is None for v in extraction['mechanism_labels'].values())
    assert acquired==result['acquired_texts'] and design==result['design_parsed']
    count=0
    for c, fold in read('e1-unapproved-inputs.json').items():
        assert set(fold['core_ids']).isdisjoint(fold['calibration_ids'])
        assert set(fold['evaluation_ids']).isdisjoint(fold['core_ids']+fold['calibration_ids'])
        assert set(r['bill_id'] for r in fold['rows'])==set(fold['core_ids']+fold['calibration_ids']+fold['evaluation_ids'])
        for row in fold['rows']:
            end=datetime.fromisoformat(f'{1789+2*int(c):04d}-01-03T17:00:00+00:00')
            # Training rows belong to earlier Congresses; derive their own boundary.
            congress=int(row['bill_id'].split('-')[0])
            end=end.replace(year=1789+2*congress)
            cutoff=datetime.fromisoformat(row['cutoff'].replace('Z','+00:00'))
            remaining=(end-cutoff).total_seconds()/63072000
            x=row['features']['control']
            assert row['features']['time']==x+[remaining]
            assert row['features']['interaction']==x+[remaining,x[0]*remaining]
            count+=1
    queue=read('annotation-queue.json')
    assert [r['bill_id'] for r in queue]==[r['bill_id'] for r in expected]
    assert all(r['annotator_1'] is None and r['annotator_2'] is None and r['adjudicator'] is None for r in queue)
    assert result['models_fitted']==result['outcomes_scored']==result['forecasts_issued']==0
    return dict(status='passed software/artifact checks only',source_references=references,
                text_files=acquired,text_bytes=byte_count,design_cases=design,design_sections=sections,
                calendar_rows_checked=count,quality_text_parsed=False,
                frozen_artifacts_unchanged=True,scientific_validation=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory',type=Path)
    args=parser.parse_args(); result=verify(args.directory)
    persist_or_compare(args.directory/'verification.json',seal(result))
    print(json.dumps(result,indent=2))
