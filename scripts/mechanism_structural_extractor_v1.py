"""Structural boundary screen over frozen v5 locators, retaining full context.

No lexical rules, text, semantic labels or reference offsets are changed. The
caller must independently authenticate raw XML and canonically validate the
sidecar with bill_structural_input_v1.validate before research use. This API
checks bindings and internal topology, not the truth of a coherently forged XML
representation. All baseline hits survive in raw_output, including flagged hits.
"""
import hashlib

from engine.paper_evaluation import require, seal
from scripts.bill_structural_input_v1 import VERSION as INPUT_VERSION, FRACTION_TAGS, CONTEXT_CHARACTERS
from scripts.mechanism_design_extractor_v5 import extract as extract_baseline, VERSION as BASELINE_VERSION

VERSION = 'mechanism-structural-extractor-v1'


def _sha(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def _validate(view, sidecar):
    require(isinstance(view, dict) and isinstance(sidecar, dict), 'View and sidecar mappings required')
    body = {k: v for k, v in view.items() if k != 'view_hash'}
    require(view.get('view_hash') == seal(body)['hash'], 'Full view envelope binding mismatch')
    require(sidecar.get('version') == INPUT_VERSION, 'Unsupported structural input version')
    require(sidecar.get('bill_id') == view.get('bill_id'), 'Structural bill identity mismatch')
    require(sidecar.get('text') == view.get('text') and isinstance(view.get('text'), str), 'Structural text mismatch')
    text = view['text']
    source = sidecar.get('source', {})
    require(source.get('view_hash') == view['view_hash'] and source.get('rendered_text_sha256') == _sha(text),
            'Structural source binding mismatch')
    require(source.get('renderer') == view.get('renderer'), 'Renderer binding mismatch')
    if 'source' in view:
        require(source.get('raw_sha256') == view['source'].get('sha256') and
                source.get('raw_bytes') == view['source'].get('bytes'), 'Raw source binding mismatch')
    require(sidecar.get('offset_unit') == 'unicode_code_points' and
            sidecar.get('interval_convention') == 'half_open' and
            sidecar.get('offset_reference') == 'unchanged_v2_rendered_view', 'Unsupported offset coordinates')
    nodes = sidecar.get('nodes')
    require(isinstance(nodes, list) and bool(nodes), 'Structural nodes required')
    by_path = {}
    for node in nodes:
        require(isinstance(node, dict), 'Invalid node')
        path = node.get('path')
        require(isinstance(path, str) and path.startswith('/') and path not in by_path, 'Invalid or duplicate node path')
        a, b = node.get('start'), node.get('end')
        require(type(a) is int and type(b) is int and 0 <= a <= b <= len(text), 'Invalid node offsets')
        require(isinstance(node.get('qualified_tag'), str) and
                node.get('tag') == node['qualified_tag'].split('}')[-1], 'Node tag mismatch')
        require(isinstance(node.get('attributes'), dict) and all(isinstance(k, str) and isinstance(v, str)
                for k, v in node['attributes'].items()), 'Invalid attributes')
        require(type(node.get('cell')) is bool and node['cell'] == (node['tag'] in {'td', 'th', 'entry'}), 'Cell classification mismatch')
        require(type(node.get('row')) is bool and node['row'] == (node['tag'] in {'tr', 'row'}), 'Row classification mismatch')
        parent = node.get('parent_path')
        if parent is None:
            require(not by_path, 'Multiple roots')
        else:
            require(parent in by_path and path.rsplit('/', 1)[0] == parent, 'Invalid node parent/order')
            require(by_path[parent]['start'] <= a <= b <= by_path[parent]['end'], 'Child outside parent')
        by_path[path] = node
    children = {p: [] for p in by_path}
    for node in nodes:
        if node['parent_path'] is not None:
            children[node['parent_path']].append(node['path'])
    for node in nodes:
        require(node.get('children_paths') == children[node['path']], 'Child links mismatch')
        siblings = [by_path[p] for p in children[node['path']]]
        require(all(x['end'] <= y['start'] for x, y in zip(siblings, siblings[1:])), 'Sibling offsets overlap/out of order')
    for span in view.get('spans', []):
        node = by_path.get(span['path'])
        require(node is not None and node['start'] == span['start'] and node['end'] == span['end']
                and node['tag'] == span['tag'], 'Frozen span mapping mismatch')
    parts = sidecar.get('segments', []) + sidecar.get('inserted_separators', [])
    cursor = 0
    for part in sorted(parts, key=lambda p: (p['start'], p['end'])):
        a, b = part.get('start'), part.get('end')
        require(type(a) is int and type(b) is int and a == cursor and a < b <= len(text), 'Segment partition mismatch')
        require(part.get('path') in by_path and part.get('text') == text[a:b]
                and part.get('text_sha256') == _sha(text[a:b]), 'Segment content mismatch')
        cursor = b
    require(cursor == len(text), 'Incomplete segment partition')

    def ancestor(node, predicate):
        parent = node['parent_path']
        while parent is not None:
            if predicate(by_path[parent]):
                return parent
            parent = by_path[parent]['parent_path']
        return None

    owner = {n['path']: ancestor(n, lambda x: x['tag'] == 'table') for n in nodes}
    row_owner = {}
    for n in nodes:
        if n['cell']:
            p = ancestor(n, lambda x: x['row'] or x['tag'] == 'table')
            row_owner[n['path']] = p if p and by_path[p]['row'] else None
    expected_tables = []
    for table in (n for n in nodes if n['tag'] == 'table'):
        path = table['path']
        rows = [n for n in nodes if n['row'] and owner[n['path']] == path]
        cells = [n for n in nodes if n['cell'] and owner[n['path']] == path]
        counts = {}
        table_cells = []
        for cell in cells:
            row_path = row_owner[cell['path']]
            counts[row_path] = counts.get(row_path, 0) + 1
            table_cells.append(dict(path=cell['path'], row_path=row_path, source_cell_ordinal=counts[row_path],
                                    start=cell['start'], end=cell['end'], text=text[cell['start']:cell['end']],
                                    attributes=cell['attributes']))
        expected_tables.append(dict(table_path=path, parent_table_path=owner[path],
            rows=[dict(path=r['path'], source_row_ordinal=i, cell_paths=[c['path'] for c in cells
                   if row_owner[c['path']] == r['path']]) for i, r in enumerate(rows, 1)],
            cells=table_cells, orphan_cell_paths=[c['path'] for c in cells if row_owner[c['path']] is None],
            grid_coordinates_inferred=False, span_attributes_interpreted=False))
    require(sidecar.get('tables') == expected_tables, 'Table topology mismatch')
    expected_fractions = []
    for n in nodes:
        if n['tag'] in FRACTION_TAGS:
            a, b = n['start'], n['end']
            ca, cb = max(0, a - CONTEXT_CHARACTERS), min(len(text), b + CONTEXT_CHARACTERS)
            expected_fractions.append(dict(path=n['path'], qualified_tag=n['qualified_tag'], attributes=n['attributes'],
                children_paths=n['children_paths'], start=a, end=b, text=text[a:b], context_start=ca,
                context_end=cb, context_text=text[ca:cb], numeric_value_inferred=False))
    require(sidecar.get('fractions') == expected_fractions, 'Fraction mapping mismatch')
    require(sidecar.get('orphan_row_paths') == [n['path'] for n in nodes if n['row'] and owner[n['path']] is None],
            'Orphan row mismatch')
    require(sidecar.get('orphan_cell_paths') == [n['path'] for n in nodes if n['cell'] and owner[n['path']] is None],
            'Orphan cell mismatch')
    return nodes, owner


def extract(view, sidecar):
    """Retain v5 output and screen each hit at every explicit cell boundary.

    A boundary strictly inside a half-open hit is flagged, including an empty
    cell or nested-cell boundary. Touching a hit endpoint is not a crossing.
    Flagging means structural-review required, not a proven false positive.
    """
    nodes, table_owner = _validate(view, sidecar)
    raw = extract_baseline(view)
    cells = [n for n in nodes if n['cell']]
    decisions = []
    usable = []
    for candidate in raw['candidates']:
        for hit in candidate['hits']:
            a, b = hit['start'], hit['end']
            identity = dict(candidate_id=candidate['candidate_id'], mechanism=candidate['mechanism'], start=a, end=b)
            boundaries = [dict(cell_path=c['path'], table_path=table_owner[c['path']], kind=kind, offset=c[kind])
                          for c in cells for kind in ('start', 'end') if a < c[kind] < b]
            containing = [c['path'] for c in cells if c['start'] <= a < b <= c['end']]
            intersecting = [c['path'] for c in cells if max(a, c['start']) < min(b, c['end'])]
            fraction_context = [f for f in sidecar['fractions'] if
                                max(a, f['context_start']) < min(b, f['context_end'])]
            decisions.append(dict(identity=identity, quote=view['text'][a:b],
                decision='flag_cell_boundary' if boundaries else 'retain',
                reason='strictly_interior_cell_boundary' if boundaries else 'no_cell_boundary_inside_hit',
                boundary_evidence=boundaries, containing_cell_paths=containing,
                intersecting_cell_paths=intersecting,
                enclosing_node_paths=[n['path'] for n in nodes if n['start'] <= a < b <= n['end']],
                fraction_context=[dict(path=f['path'], start=f['start'], end=f['end'], text=f['text'],
                    context_start=f['context_start'], context_end=f['context_end'], context_text=f['context_text'],
                    overlaps_hit=max(a, f['start']) < min(b, f['end']), numeric_value_inferred=False)
                    for f in fraction_context]))
            if not boundaries:
                usable.append(identity)
    return dict(version=VERSION, baseline_version=BASELINE_VERSION, structural_input_version=INPUT_VERSION,
        bill_id=view['bill_id'], view_hash=view['view_hash'], sidecar_hash=seal(sidecar)['hash'],
        source=dict(sidecar['source']), full_context_text=view['text'], raw_output=raw,
        boundary_decisions=decisions, usable_hits=usable,
        counts=dict(raw_hits=len(decisions), retained_hits=len(usable), flagged_hits=len(decisions) - len(usable)),
        offset_unit='unicode_code_points', interval_convention='half_open',
        semantic_labels_accepted=False, historical_feature_eligible=False, human_certified=False,
        limitations=['Structural screening is not semantic classification or predictive evaluation.',
                    'All raw hits and full bill context remain available; flagged hits require review.',
                    'Cell nesting and empty cells are screened conservatively; table grid and fraction values are not inferred.',
                    'Internal binding checks require separate canonical sidecar validation against authenticated raw XML.'])
