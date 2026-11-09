"""Supplemental XML/render accounting. Character coverage never certifies semantics."""
import hashlib
import re
import xml.etree.ElementTree as ET
from collections import Counter

from engine.paper_evaluation import require
from scripts.bill_context_design_text_v2 import BLOCKS, render

TABLE_TAGS = {'table', 'table-wrapper', 'tgroup', 'thead', 'tbody', 'tfoot', 'tr', 'row', 'td', 'th', 'entry', 'colspec', 'spanspec'}
CELL_TAGS = {'td', 'th', 'entry'}
ROW_TAGS = {'tr', 'row'}
NON_TEXT_TAGS = {'img', 'image', 'graphic', 'figure', 'formula', 'math', 'equation', 'inline-formula', 'disp-formula', 'math-display', 'mml'}


def _local(tag):
    return tag.rsplit('}', 1)[-1]


class _NoDoctype(ET.TreeBuilder):
    def doctype(self, name, pubid, system):
        raise ValueError('DTD declarations forbidden in coverage audit')


def audit(raw, bill_id, supplied_view):
    """Return complete per-node/text-segment accounting against a supplied v2 body.

    Offsets are Python Unicode code points in rendered text, never XML byte offsets.
    XML parser normalization/entity decoding precedes this accounting. Namespace
    identities, attributes and table topology are inventoried, not interpreted.
    """
    require(isinstance(raw, bytes), 'Raw source must be bytes')
    require(isinstance(supplied_view, dict), 'View must be a body mapping')
    require(supplied_view.get('bill_id') == bill_id, 'View bill identity mismatch')
    root = ET.fromstring(raw, parser=ET.XMLParser(target=_NoDoctype()))
    fresh = render(raw, bill_id)
    require(supplied_view.get('text') == fresh['text'], 'Supplied view text differs from fresh renderer')
    require(supplied_view.get('spans') == fresh['spans'], 'Supplied view spans differ from fresh renderer')
    require(supplied_view.get('renderer') == fresh['renderer'], 'Supplied renderer identity mismatch')
    source = supplied_view.get('source')
    if source is not None:
        require(isinstance(source, dict), 'Invalid source binding')
        require(source.get('sha256') == hashlib.sha256(raw).hexdigest(), 'Source byte hash mismatch')
        require(type(source.get('bytes')) is int and source['bytes'] == len(raw), 'Source byte length mismatch')

    # Build events from the XML tree independently of the renderer's pieces/spans.
    events, nodes = [], []
    def inventory(node, path, parent):
        tag = _local(node.tag)
        info = dict(path=path, parent_path=parent, tag=tag, qualified_tag=node.tag,
                    attributes=dict(sorted(node.attrib.items())), represented_span=tag in BLOCKS,
                    table_related=tag in TABLE_TAGS, cell=tag in CELL_TAGS, row=tag in ROW_TAGS,
                    possible_nontext_content=tag in NON_TEXT_TAGS)
        nodes.append(info)
        if tag in BLOCKS:
            events.append(('separator', path, '\n'))
        events.append(('start', path, ''))
        if node.text is not None:
            events.append(('text', path, node.text))
        counts = Counter()
        for child in node:
            child_tag = _local(child.tag)
            counts[child_tag] += 1
            child_path = f'{path}/{child_tag}[{counts[child_tag]}]'
            inventory(child, child_path, path)
            if child.tail is not None:
                events.append(('tail', child_path, child.tail))
        events.append(('end', path, ''))
        if tag in BLOCKS:
            events.append(('separator', path, '\n'))
    inventory(root, '/bill[1]', None)
    segments, separators, bounds, size, chunks = [], [], {}, 0, []
    for kind, path, value in events:
        if kind in ('start', 'end'):
            bounds.setdefault(path, {})[kind] = size
            continue
        end = size + len(value)
        row = dict(path=path, kind=kind, start=size, end=end, text=value,
                   text_sha256=hashlib.sha256(value.encode()).hexdigest())
        (separators if kind == 'separator' else segments).append(row)
        chunks.append(value)
        size = end
    require(''.join(chunks) == fresh['text'], 'Independent segment stream mismatch')
    span_map = {span['path']: span for span in fresh['spans']}
    require(len(span_map) == len(fresh['spans']), 'Duplicate renderer span path')
    for node in nodes:
        node.update(bounds[node['path']])
        if node['represented_span']:
            span = span_map.get(node['path'])
            require(span is not None and span['tag'] == node['tag'] and
                    span['start'] == node['start'] and span['end'] == node['end'], 'Independent span boundary mismatch')
    require(len(span_map) == sum(n['represented_span'] for n in nodes), 'Unexpected renderer span')
    for segment in segments:
        require(fresh['text'][segment['start']:segment['end']] == segment['text'], 'Segment offset mismatch')

    warnings = []
    def warn(code, paths, detail):
        if paths:
            warnings.append(dict(code=code, paths=paths, detail=detail))
    warn('unrepresented_table_structure', [n['path'] for n in nodes if n['table_related'] and not n['represented_span']],
         'Table, row, cell and column relationships are not represented as renderer spans; text coverage cannot establish table meaning.')
    warn('attributes_not_rendered', [n['path'] for n in nodes if n['attributes']],
         'Attributes are inventoried but are not rendered text; references, units, spans and amendment semantics may depend on them.')
    warn('nontext_content_requires_review', [n['path'] for n in nodes if n['possible_nontext_content']],
         'Figures, images and mathematical structures may convey information beyond text nodes.')
    warn('namespace_identity_collapsed', [n['path'] for n in nodes if n['qualified_tag'] != n['tag']],
         'Renderer paths discard namespace identity. The inventory preserves qualified tags.')
    boundaries = []
    by_parent = {}
    for node in nodes:
        if node['cell']:
            by_parent.setdefault(node['parent_path'], []).append(node)
    for cells in by_parent.values():
        for left, right in zip(cells, cells[1:]):
            gap = fresh['text'][left['end']:right['start']]
            left_text = fresh['text'][left['start']:left['end']]
            right_text = fresh['text'][right['start']:right['end']]
            boundaries.append(dict(left=left['path'], right=right['path'], left_end=left['end'], right_start=right['start'],
                                   gap=gap, no_whitespace_boundary=bool(left_text and right_text and
                                   not re.search(r'\s', left_text[-1:] + gap + right_text[:1]))))
    warn('adjacent_cells_without_whitespace', [b['left'] + ' -> ' + b['right'] for b in boundaries if b['no_whitespace_boundary']],
         'Adjacent cell text is concatenated without a whitespace boundary; a locator can cross cells.')
    unrepresented = Counter(n['tag'] for n in nodes if not n['represented_span'])
    return dict(bill_id=bill_id, raw_sha256=hashlib.sha256(raw).hexdigest(), raw_bytes=len(raw),
                rendered_text_sha256=hashlib.sha256(fresh['text'].encode()).hexdigest(),
                renderer=fresh['renderer'], offset_unit='unicode_code_points',
                counts=dict(nodes=len(nodes), represented_nodes=len(span_map), unrepresented_nodes=sum(unrepresented.values()),
                            text_segments=len(segments), source_text_characters=sum(len(s['text']) for s in segments),
                            inserted_separator_characters=len(separators), rendered_characters=len(fresh['text']),
                            table_nodes=sum(n['table_related'] for n in nodes), rows=sum(n['row'] for n in nodes),
                            cells=sum(n['cell'] for n in nodes), attribute_nodes=sum(bool(n['attributes']) for n in nodes),
                            possible_nontext_nodes=sum(n['possible_nontext_content'] for n in nodes)),
                unrepresented_tags=dict(sorted(unrepresented.items())), nodes=nodes, segments=segments,
                inserted_separators=separators, cell_boundaries=boundaries, warnings=warnings,
                supplied_view_matches_fresh_render=True, independent_segment_accounting_matches=True,
                parser_text_segments_accounted=True, source_document_completeness=False,
                semantic_structure_complete=False, historical_feature_eligible=False, human_certified=False,
                limitations=['Accounts for parser-visible element text and tails after XML normalization and character-reference decoding; not a byte-to-character source map.',
                             'Comments, processing instructions, attribute semantics, external resources and visual layout are not rendered semantic content.',
                             'Coverage cannot authenticate publication time, legal identity, source completeness or semantic correctness.'])
