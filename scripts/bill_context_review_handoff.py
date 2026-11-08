"""Create a readable design-only review workbook; never record approval."""
import argparse
import json
import re
from pathlib import Path
from engine.paper_evaluation import seal, unseal
from scripts.paper_review_packet import persist_or_compare


def handoff(directory):
    directory=Path(directory)
    registration=json.loads((directory/'registration.json').read_text())
    spec=unseal(registration)
    destination=directory/'review-design'
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
            text=extraction['text']
            fence='`'*(max([len(s) for s in re.findall(r'`+',text)]+[3])+1)
            lines += [f'{fence}text\n{text}\n{fence}\n', '## Section map\n']
            lines += [f"- Section index {s['index']}; XML ID `{s['xml_id']}`; text hash `{s['text_sha256']}`.\n" for s in extraction['sections']]
        else:lines.append('Text extraction unavailable: '+record.get('blocked_reason','unknown')+'\n')
        (destination/filename).write_text('\n'.join(lines))
    (destination/'START_HERE.md').write_text('\n'.join(index))
    value=seal(dict(protocol_hash=registration['hash'], role='first design reviewer volunteered by user',
                    qualifications='not recorded', approvals=0, second_reviewer=None, adjudicator=None,
                    design_ids=ids, quality_content_exported=False))
    persist_or_compare(directory/'review-handoff.json',value)
    return destination/'START_HERE.md'


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory',type=Path)
    print(handoff(p.parse_args().directory))
