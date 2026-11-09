"""Versioned structural sidecar bound to an unchanged, authenticated v2 view.

This is parsed XML topology, not legal interpretation or a visual table grid.
No raw XML byte offsets, historical eligibility or semantic certification are
inferred. Expanded namespace names survive; original prefix spellings do not.
"""
import re

from engine.paper_evaluation import require, seal
from scripts.bill_render_coverage_audit_v2 import audit

VERSION = 'structural-input-v1'
CONTEXT_CHARACTERS = 32
FRACTION_TAGS = {'fraction', 'mfrac'}


def build(raw, bill_id, view, view_hash):
    """Build deterministic topology with half-open Unicode reading-view offsets."""
    require(isinstance(bill_id, str) and re.fullmatch(r'[1-9]\d*-(hr|s)[1-9]\d*', bill_id),
            'Invalid bill identity')
    require(isinstance(view, dict), 'View must be a body mapping')
    require(isinstance(view_hash, str) and re.fullmatch(r'[0-9a-f]{64}', view_hash), 'Invalid view hash')
    require(seal(view)['hash'] == view_hash, 'View envelope hash mismatch')
    coverage = audit(raw, bill_id, view)
    nodes = coverage['nodes']
    by_path = {node['path']: node for node in nodes}
    for node in nodes:
        node['children_paths'] = []
    for node in nodes:
        if node['parent_path'] is not None:
            by_path[node['parent_path']]['children_paths'].append(node['path'])

    def ancestor(node, predicate):
        parent = node['parent_path']
        while parent is not None:
            candidate = by_path[parent]
            if predicate(candidate):
                return candidate['path']
            parent = candidate['parent_path']
        return None

    table_owner = {n['path']: ancestor(n, lambda x: x['tag'] == 'table') for n in nodes}
    row_owner = {}
    for node in nodes:
        if node['cell']:
            row = ancestor(node, lambda x: x['row'] or x['tag'] == 'table')
            row_owner[node['path']] = row if row is not None and by_path[row]['row'] else None
    text = view['text']
    tables = []
    for table in (n for n in nodes if n['tag'] == 'table'):
        path = table['path']
        rows = [n for n in nodes if n['row'] and table_owner[n['path']] == path]
        cells = [n for n in nodes if n['cell'] and table_owner[n['path']] == path]
        table_rows = []
        for ordinal, row in enumerate(rows, 1):
            table_rows.append(dict(path=row['path'], source_row_ordinal=ordinal,
                                   cell_paths=[n['path'] for n in cells if row_owner[n['path']] == row['path']]))
        ordinal_by_row = {}
        table_cells = []
        for cell in cells:
            row_path = row_owner[cell['path']]
            ordinal_by_row[row_path] = ordinal_by_row.get(row_path, 0) + 1
            table_cells.append(dict(path=cell['path'], row_path=row_path,
                source_cell_ordinal=ordinal_by_row[row_path], start=cell['start'], end=cell['end'],
                text=text[cell['start']:cell['end']], attributes=dict(cell['attributes'])))
        tables.append(dict(table_path=path, parent_table_path=table_owner[path], rows=table_rows,
                           cells=table_cells, orphan_cell_paths=[n['path'] for n in cells if row_owner[n['path']] is None],
                           grid_coordinates_inferred=False, span_attributes_interpreted=False))
    fractions = []
    for node in nodes:
        if node['tag'] in FRACTION_TAGS:
            start, end = node['start'], node['end']
            context_start, context_end = max(0, start - CONTEXT_CHARACTERS), min(len(text), end + CONTEXT_CHARACTERS)
            fractions.append(dict(path=node['path'], qualified_tag=node['qualified_tag'],
                attributes=dict(node['attributes']), children_paths=list(node['children_paths']),
                start=start, end=end, text=text[start:end], context_start=context_start,
                context_end=context_end, context_text=text[context_start:context_end],
                numeric_value_inferred=False))
    return dict(version=VERSION, bill_id=bill_id,
        source=dict(raw_sha256=coverage['raw_sha256'], raw_bytes=coverage['raw_bytes'],
                    view_hash=view_hash, rendered_text_sha256=coverage['rendered_text_sha256'], renderer=coverage['renderer']),
        offset_unit='unicode_code_points', offset_reference='unchanged_v2_rendered_view',
        interval_convention='half_open', raw_byte_offsets_available=False,
        text=text, nodes=nodes, segments=coverage['segments'], inserted_separators=coverage['inserted_separators'],
        tables=tables, fractions=fractions,
        orphan_row_paths=[n['path'] for n in nodes if n['row'] and table_owner[n['path']] is None],
        orphan_cell_paths=[n['path'] for n in nodes if n['cell'] and table_owner[n['path']] is None],
        doctype_declarations=coverage['doctype_declarations'], external_resources_resolved=False,
        counts=dict(coverage['counts'], tables=len(tables), fractions=len(fractions),
                    attributes=sum(len(n['attributes']) for n in nodes)),
        source_document_completeness=False, semantic_structure_complete=False,
        historical_feature_eligible=False, human_certified=False,
        limitations=coverage['limitations'] + [
            'Expanded namespace names and parsed attribute values are preserved, not prefix spellings, declaration placement, attribute lexical order or raw XML byte positions.',
            'Row and cell ordinals are source order only. CALS/HTML span attributes remain uninterpreted; nested table ownership is explicit and no rectangular visual grid is inferred.',
            'Cell text includes descendant content, including nested tables. Ownership lists isolate nested rows and cells; offsets remain anchored to the unchanged view.',
            'Fraction and mfrac nodes retain exact rendered substrings and surrounding context; no mixed-number, arithmetic or land-description interpretation is inferred.',
            'This sidecar does not amend frozen reference offsets or certify semantic labels, historical publication time or prediction readiness.'])


def validate(sidecar, raw, bill_id, view, view_hash):
    """Reject any altered, missing or extra field against authenticated recomputation."""
    expected = build(raw, bill_id, view, view_hash)
    require(isinstance(sidecar, dict) and seal(sidecar)['hash'] == seal(expected)['hash'],
            'Structural sidecar differs from canonical recomputation')
    return True
