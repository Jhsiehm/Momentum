"""Separate boundary-aware design text views; original pilot remains immutable."""
import argparse
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from engine.paper_evaluation import seal, unseal
from engine.store import ROOT
from scripts.paper_review_packet import persist_or_compare

BLOCKS = set('form congress session legis-num current-chamber legis-type official-title legis-body preamble section subsection paragraph subparagraph clause subclause header enum text quoted-block appropriations-major appropriations-intermediate appropriations-small'.split())


def render(raw, bill_id):
    if b'<!ENTITY' in raw.upper(): raise ValueError('XML entities forbidden')
    identity=re.fullmatch(r'(\d+)-(hr|s)([1-9]\d*)',bill_id)
    if not identity: raise ValueError('Invalid bill identity')
    congress, kind, number=identity.groups()
    tree=ET.fromstring(raw)
    for node in tree.iter(): node.tag=node.tag.rsplit('}',1)[-1]
    if tree.tag!='bill': raise ValueError('Not bill XML')
    form=tree.find('form')
    if form is None: raise ValueError('Missing bill form')
    found=re.fullmatch(r'\s*(\d+)(?:st|nd|rd|th)?\s+CONGRESS\s*',form.findtext('congress',''),re.I)
    if not found or int(found[1])!=int(congress): raise ValueError('Congress identity mismatch')
    if re.sub(r'[^a-z0-9]','',form.findtext('legis-num','').lower())!=kind+number:
        raise ValueError('Bill number identity mismatch')
    pieces=[]; spans=[]; size=0
    def append(value):
        nonlocal size
        if value:
            pieces.append(value);size+=len(value)
    def walk(node,path):
        if node.tag in BLOCKS: append('\n')
        start=size
        append(node.text)
        counts={}
        for child in node:
            counts[child.tag]=counts.get(child.tag,0)+1
            walk(child,f'{path}/{child.tag}[{counts[child.tag]}]')
            append(child.tail)
        end=size
        if node.tag in BLOCKS:
            spans.append(dict(path=path,xml_id=node.get('id'),tag=node.tag,start=start,end=end))
            append('\n')
    walk(tree,'/bill[1]')
    text=''.join(pieces)
    for span in spans:
        span['text_sha256']=hashlib.sha256(text[span['start']:span['end']].encode()).hexdigest()
    return dict(bill_id=bill_id,text=text,spans=spans,
                renderer='block-boundaries-v2',status='unreviewed_design_view',
                note='Offsets refer to this view, not original XML bytes or v1 extraction. Inline text and tails preserved; inserted block newlines are explicit.')


def build(directory, output):
    directory=Path(directory);output=Path(output)
    if ROOT/'data' not in output.resolve().parents: raise ValueError('Output must be under ignored data/')
    registration=json.loads((directory/'registration.json').read_text());spec=unseal(registration)
    output.mkdir(parents=True,exist_ok=False)
    code_hash=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    views=[]
    for selected in spec['selection']:
        if selected['partition']!='design': continue
        bid=selected['bill_id']
        envelope=json.loads((directory/'records'/(bid+'.json')).read_text());record=unseal(envelope)
        if record['bill_id']!=bid or record['partition']!='design': raise ValueError('Record identity/partition mismatch')
        source=record['source'];key=hashlib.sha256(source['url'].encode()).hexdigest()
        raw=(directory/'sources'/(key+'.raw')).read_bytes()
        if hashlib.sha256(raw).hexdigest()!=source['sha256'] or len(raw)!=source['bytes']:
            raise ValueError('Source bytes changed')
        view=seal(dict(**render(raw,bid),source=source,original_record_hash=envelope['hash'],parser_sha256=code_hash))
        persist_or_compare(output/(bid+'.json'),view)
        views.append(dict(bill_id=bid,hash=view['hash']))
    result=seal(dict(original_protocol_hash=registration['hash'],renderer_sha256=code_hash,views=views,
                     quality_parsed=False,labels_created=0,historical_feature_eligible=False))
    persist_or_compare(output/'manifest.json',result)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory',type=Path);p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();r=build(args.directory,args.output)
    print(json.dumps(dict(hash=r['hash'],design_views=len(r['body']['views']),quality_parsed=False)))
