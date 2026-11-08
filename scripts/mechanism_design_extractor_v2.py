"""Add structural context to immutable v1 locators, without semantic promotion.

Pure ``extract(view)`` retains v1 candidates, hits, proposals and abstentions.
``structural_spans`` is a deduplicated source-span pool. Each hit's additive
``structural_context`` references that pool with a relation and ancestor_path.
Relations describe XML reading-view hierarchy/order only, never legal governance.
Whole-section v1 review quotes remain available, including following exceptions.
"""
from __future__ import annotations

import hashlib
import re

from scripts.mechanism_design_extractor import VERSION as BASE_VERSION
from scripts.mechanism_design_extractor import extract as extract_v1

VERSION = 'assisted-mechanism-candidates-v2-structural'
CONTEXT_SCHEMA = 'structural-span-references-v1'


def _parent(path: str) -> str:
    return path.rsplit('/', 1)[0]


def extract(view: dict) -> dict:
    """Attach source-local hierarchy references; no I/O or new lexical rules.

    A containing text/header is selected by actual range containment. For each
    strict XML ancestor of the deepest containing source node, attach its direct
    headers and direct text nodes only when they precede the branch containing
    the hit. This excludes sibling paragraphs, following text, and following
    exception clauses from *ancestor lead-in* relations. Such excluded text is
    still present in the unchanged full-section candidate quote. Ancestors may
    cross quoted-block boundaries; those boundaries are exposed, not interpreted
    as proof that the language is inserted rather than deleted.
    """
    # Reject malformed paths before frozen v1's ancestor walk: a relative path
    # without a slash would otherwise never shorten in that implementation.
    if not isinstance(view, dict) or not isinstance(view.get('spans'), list):
        raise ValueError('Boundary-aware view spans required')
    for span in view['spans']:
        path = span.get('path') if isinstance(span, dict) else None
        if not isinstance(path, str) or not re.fullmatch(r'(?:/[^/\s\[\]]+\[[1-9][0-9]*\])+', path):
            raise ValueError('Absolute indexed source hierarchy path required')
    result = extract_v1(view)  # v1 validates hashes and character bounds.
    text = view['text']
    spans = sorted(view['spans'], key=lambda s: (s['start'], -s['end'], s['path']))
    by_path = {s['path']: s for s in spans}
    children = {}
    for span in spans:
        children.setdefault(_parent(span['path']), []).append(span)
    pool = {}
    pool_by_id = {}

    def reference(span, relation, ancestor_path):
        path = span['path']
        identifier = 's_' + hashlib.sha256(path.encode('utf-8')).hexdigest()[:24]
        if path not in pool:
            pool[path] = dict(span_id=identifier, path=path, tag=span['tag'],
                              start=span['start'], end=span['end'],
                              quote=text[span['start']:span['end']])
        pool_by_id[identifier] = pool[path]
        return dict(span_id=identifier, relation=relation, ancestor_path=ancestor_path)

    for candidate in result['candidates']:
        for hit in candidate['hits']:
            containers = [s for s in spans if s['start'] <= hit['start'] and hit['end'] <= s['end']]
            # Path depth resolves nested source nodes; no string matching or
            # first-identical-quote search can move the selected occurrence.
            anchor = max(containers, key=lambda s: (s['path'].count('/'), s['start'], -s['end'], s['path'])) if containers else None
            refs = []
            containing = [s for s in containers if s['tag'] in {'text', 'header'}]
            for span in containing:
                refs.append(reference(span, 'containing_' + span['tag'], None))
            boundaries = []
            if anchor:
                ancestor_path = _parent(anchor['path'])
                while ancestor_path:
                    ancestor = by_path.get(ancestor_path)
                    if ancestor and ancestor['tag'] == 'quoted-block':
                        boundaries.append(reference(ancestor, 'quoted_block_boundary', ancestor_path))
                    # Find the immediate path branch (including renderer-omitted
                    # XML nodes) and its earliest represented character offset.
                    suffix = anchor['path'][len(ancestor_path) + 1:]
                    branch_path = ancestor_path + '/' + suffix.split('/', 1)[0]
                    branch = by_path.get(branch_path)
                    if branch:
                        branch_start = branch['start']
                    else:
                        branch_start = min(s['start'] for s in spans if s['path'] == branch_path or s['path'].startswith(branch_path + '/'))
                    for span in children.get(ancestor_path, []):
                        if span['end'] > branch_start or not text[span['start']:span['end']].strip():
                            continue
                        if span['tag'] == 'header':
                            refs.append(reference(span, 'ancestor_header', ancestor_path))
                        elif span['tag'] == 'text':
                            refs.append(reference(span, 'ancestor_preceding_direct_text', ancestor_path))
                    ancestor_path = _parent(ancestor_path)
            # Stable source order, with one relation per source span in a hit.
            refs = sorted(refs, key=lambda r: (pool_by_id[r['span_id']]['start'], r['relation'], r['span_id']))
            hit['structural_context'] = refs
            hit['structural_boundaries'] = boundaries
            hit['structural_context_status'] = ('containing_text_or_header' if containing else
                                                 'container_only' if anchor else 'no_containing_boundary')
            hit['semantic_governance_verified'] = False
    result['schema'] = 'assisted-annotation-candidates-v2'
    result['base_extractor_version'] = BASE_VERSION
    result['extractor_version'] = VERSION
    result['structural_context_schema'] = CONTEXT_SCHEMA
    result['structural_spans'] = sorted(pool.values(), key=lambda s: (s['start'], s['end'], s['path']))
    result['structural_context_interpretation'] = 'Hierarchy and preceding-source order only; no legal governance, sufficiency, or semantic correctness established'
    return result
