"""Create a readable design-only review workbook; never record approval."""
import argparse
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from engine.paper_evaluation import seal, unseal
from engine.store import ROOT
from scripts.paper_review_packet import persist_or_compare, resolve
from scripts.bill_context_execution import xml_url
from scripts.bill_context_design_text_v2 import render


def handoff(directory, export_directory=None):
    directory=Path(directory)
    registration=json.loads((directory/'registration.json').read_text())
    spec=unseal(registration)
    source_packet=unseal(json.loads((directory/'source-packet.json').read_text()))
    packet_records={r['bill_id']:r for r in source_packet['records']}
    if len(packet_records)!=len(spec['selection']): raise ValueError('Source packet identities invalid')
    destination=Path(export_directory) if export_directory else directory/'review-design'
    if ROOT/'data' not in destination.resolve().parents: raise ValueError('Export must be under ignored data/')
    destination.mkdir(exist_ok=False)
    index=['# Bill-context design review\n',
           'You volunteered as the first reviewer. No qualifications, annotations or approvals have been recorded. The second independent reviewer and adjudicator remain unassigned.\n',
           'Start with these design cases. Do not open the quality sources or annotate quality cases until the extractor and guide are frozen.\n',
           'For each bill, describe what it actually changes, then assess overlapping mechanisms. Distinguish authorization from appropriation, preserve negation, conditions and exceptions, and cite the supporting section and exact words. Unknown is an acceptable answer.\n',
           'The current XML download does not establish what was public at the historical prediction date. Source timing, family genealogy and outcome reviews are separate; do not approve them without supporting evidence.\n',
           'Reply with the bill ID, your interpretation, mechanism decisions, exact supporting quotations and any uncertainty. We will retain your annotations separately from the immutable source records.\n',
           'The guide is `docs/research/BILL_CONTEXT_ANNOTATION_GUIDE_V1.md`. These pages are review aids, not training labels.\n']
    ids=[]
    for selected in spec['selection']:
        if selected['partition']!='design':continue
        bid=selected['bill_id']; ids.append(bid)
        record=unseal(json.loads((directory/'records'/(bid+'.json')).read_text()))
        original=packet_records[bid]
        if (record['bill_id']!=bid or record['family_id']!=selected['family_id']
                or record['congress']!=original['congress'] or record['cutoff']!=original['cutoff']
                or record['partition']!='design' or record['human_review']!='pending'
                or record['historical_feature_eligible'] is not False):
            raise ValueError('Review record identity/status mismatch')
        # Source-only verification: no outcome population or quality text parsed.
        evidence_sources=[original['discovery_source']]+[s for v in original['versions'] for s in v['sources']]
        for source in evidence_sources:
            caches=[ROOT/m['raw_path'] for m in source['retained_matches']]
            resolve(source,[p.parent for p in caches],ROOT)
            for match in source['retained_matches']:
                if hashlib.sha256((ROOT/match['receipt_path']).read_bytes()).hexdigest()!=match['receipt_sha256']:
                    raise ValueError('Pinned metadata receipt changed')
        package,url=xml_url(original,ROOT)
        if record.get('package')!=package or record.get('source',{}).get('url')!=url:
            raise ValueError('Review rendition source mismatch')
        source=record['source'];key=hashlib.sha256(url.encode()).hexdigest()
        raw=(directory/'sources'/(key+'.raw')).read_bytes()
        receipt=json.loads((directory/'sources'/(key+'.json')).read_text())
        if receipt!=source or hashlib.sha256(raw).hexdigest()!=source['sha256'] or len(raw)!=source['bytes']:
            raise ValueError('Review source bytes changed')
        new_view=render(raw,bid)
        if record.get('design_extraction',{}).get('text')!=''.join(ET.fromstring(raw).itertext()):
            raise ValueError('Original review text differs from retained XML')
        filename=bid+'.md'
        index.append(f'- [{bid}]({filename})\n')
        lines=[f'# {bid}: design review\n',
               f"Prediction checkpoint: {record['cutoff']}. Family: {record['family_id']} (unreviewed).\n",
               '**Review status: pending.** No human certification or mechanism label is implied.\n']
        if 'source' in record:
            source=record['source']
            lines += [f"Official rendition: {source['url']}\n",
                      f"Retrieved: {source['retrieved_at']}; SHA-256: `{source['sha256']}`. Historical availability remains unverified.\n"]
        lines += ['## Your annotation\n',
                  '- What does this bill actually do?\n- Who or what is affected?\n- What conditions, exceptions, dates or amounts matter?\n',
                  '- For each mechanism, state present / absent / unknown / disputed and quote supporting language: create programme; authorize; appropriate; tax; prohibit; require; amend; repeal; rename/designate; reporting; deadline; sunset.\n',
                  '- Is the identity correct? Are any text, interpretation, source-timing or family questions unresolved?\n',
                  '## Preserved text\n']
        extraction=record.get('design_extraction')
        if extraction:
            text=new_view['text']
            fence='`'*(max([len(s) for s in re.findall(r'`+',text)]+[3])+1)
            lines += ['Reading view v2 inserts explicit block boundaries; original XML remains authoritative.\n',f'{fence}text\n{text}\n{fence}\n', '## Section map\n']
            lines += [f"- XML path `{s['path']}`; XML ID `{s['xml_id']}`; view text hash `{s['text_sha256']}`.\n" for s in new_view['spans'] if s['tag']=='section']
        else:lines.append('Text extraction unavailable: '+record.get('blocked_reason','unknown')+'\n')
        (destination/filename).write_text('\n'.join(lines))
    (destination/'START_HERE.md').write_text('\n'.join(index))
    value=seal(dict(protocol_hash=registration['hash'], role='first design reviewer volunteered by user',
                    qualifications='not recorded', approvals=0, second_reviewer=None, adjudicator=None,
                    design_ids=ids, quality_content_exported=False,
                    code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                    renderer_sha256=hashlib.sha256((ROOT/'scripts/bill_context_design_text_v2.py').read_bytes()).hexdigest(),
                    guide_sha256=hashlib.sha256((ROOT/'docs/research/BILL_CONTEXT_ANNOTATION_GUIDE_V1.md').read_bytes()).hexdigest(),
                    page_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(destination.glob('*.md'))}))
    persist_or_compare(destination/'manifest.json',value)
    return destination/'START_HERE.md'


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory',type=Path)
    p.add_argument('--export-directory',type=Path)
    args=p.parse_args();print(handoff(args.directory,args.export_directory))
