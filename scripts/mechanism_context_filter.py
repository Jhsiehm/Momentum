"""Conservative review-triage flags, separate from immutable candidate extraction.

The prior 24-item design review motivated this experiment. Its cases are not a
held-out evaluation and no identifiers or individual outcomes drive the rules.
Retain means no narrow context flag, never semantic approval. Even flagged hits
remain in the result; deletion language may itself operate on a v2 mechanism.
"""
from __future__ import annotations

import hashlib
import re

from scripts.mechanism_design_extractor import MECHANISMS, _check_view

VERSION = 'mechanism-context-triage-v1'
DESIGN_MOTIVATION_REVIEW_HASH = 'e2189bd7ca958abf044fedc1777152d222ca300aa973e4cec55254a2d6ff21e2'
RULES = (
    {'id': 'heading_only', 'description': 'Hit entirely contained in a structural header.'},
    {'id': 'outside_legis_body', 'description': 'Hit entirely outside all supplied legis-body boundaries; no flag when those boundaries are unavailable.'},
    {'id': 'official_title', 'description': 'Hit inside an official-title purpose statement.'},
    {'id': 'findings_or_sense_context', 'description': 'Hit in a structurally governed findings/sense context marked by a preceding direct header; a triage flag, not legal nonoperation proof.'},
    {'id': 'struck_inline_quote', 'description': 'Hit entirely inside balanced quoted text immediately following a striking directive in the same text node.'},
    {'id': 'struck_replacement_operand', 'description': 'Hit entirely inside a bounded unquoted old-text operand between by striking and and inserting in the same direct text node.'},
    {'id': 'struck_quoted_block', 'description': 'Hit inside a quoted-block whose nearest preceding direct sibling text ends in an unambiguous striking-the-following directive.'},
)
_HEADER = re.compile(r'^\s*(?:findings|sense\s+of\s+(?:Congress|the\s+Congress|the\s+Senate|the\s+House\s+of\s+Representatives|the\s+House))\s*[.]?\s*$', re.I)
# Limit both distance and nesting; ambiguous punctuation or embedded directives
# abstain. New replacement wording is never included in a struck operand.
_INLINE = (
    re.compile(r'\bby\s+striking\s+(?:the\s+words?\s+)?“(?P<old>[^“”]{1,1500})”', re.I),
    re.compile(r'\bby\s+striking\s+(?:the\s+words?\s+)?"(?P<old>[^"\n]{1,1500})"', re.I),
)
_REPLACE = re.compile(r'\bby\s+striking\s+(?P<old>[^.;:!?“”"\n]{1,1500}?)\s+and\s+inserting\b', re.I)
# Whitespace/newlines inside old words are common in the boundary-aware view.
# A separate bounded word-sequence pattern allows layout whitespace but never a
# punctuation delimiter or quote. It still requires an explicit replacement.
_REPLACE_LAYOUT = re.compile(r'\bby\s+striking\s+(?P<old>(?:[^.;:!?“”"\s]+\s+){0,150}[^.;:!?“”"\s]+)\s+and\s+inserting\b', re.I)
_BLOCK_DIRECTIVE = re.compile(r'\bby\s+striking\s+the\s+following(?:\s+(?:text|provision|paragraph|subsection|section))?\s*:\s*$', re.I)
_AMBIGUOUS = re.compile(r'\b(?:by\s+(?:striking|inserting|adding)|and\s+inserting)\b', re.I)


def _evidence(text, start, end):
    return {'start': start, 'end': end, 'quote': text[start:end]}


def classify(view, expanded_output):
    """Pure, deterministic hit-preserving decisions with exact source evidence.

    Consumes an unsealed renderer body (optional view_hash) and unsealed v3
    output. Original candidates, proposals and abstentions are never modified.
    Full supplied hierarchy is used, not nearest-keyword section heuristics.
    Unknown/descriptive contexts and ambiguous deletion boundaries are retained.
    """
    if not isinstance(view, dict) or not isinstance(view.get('spans'), list):
        raise ValueError('Boundary-aware view required')
    for span in view['spans']:
        path = span.get('path') if isinstance(span, dict) else None
        if not isinstance(path, str) or not re.fullmatch(r'(?:/[^/\s\[\]]+\[[1-9][0-9]*\])+', path):
            raise ValueError('Absolute indexed hierarchy path required')
    text, spans = _check_view(view)
    if not isinstance(expanded_output, dict) or expanded_output.get('bill_id') != view['bill_id']:
        raise ValueError('Candidate bill binding mismatch')
    text_hash = hashlib.sha256(text.encode()).hexdigest()
    if expanded_output.get('input_text_sha256') != text_hash:
        raise ValueError('Candidate text binding mismatch')
    if view.get('view_hash') is not None and expanded_output.get('source_view_hash') != view['view_hash']:
        raise ValueError('Candidate view binding mismatch')
    bodies = [s for s in spans if s['tag'] == 'legis-body']
    headers = [s for s in spans if s['tag'] == 'header']
    titles = [s for s in spans if s['tag'] == 'official-title']
    text_nodes = [s for s in spans if s['tag'] == 'text']
    paths = {s['path']: s for s in spans}
    marked_contexts = []
    for header in headers:
        parent = paths.get(header['path'].rsplit('/', 1)[0])
        if parent and _HEADER.fullmatch(text[header['start']:header['end']]):
            marked_contexts.append((parent, header))

    struck = []
    for node in text_nodes:
        value = text[node['start']:node['end']]
        for pattern in _INLINE:
            for match in pattern.finditer(value):
                if _AMBIGUOUS.search(match.group('old')):
                    continue
                a, b = match.span('old')
                struck.append((node['start'] + a, node['start'] + b, 'struck_inline_quote',
                               _evidence(text, node['start'] + match.start(), node['start'] + match.end())))
        for pattern in (_REPLACE, _REPLACE_LAYOUT):
            for match in pattern.finditer(value):
                if len(match.group('old')) > 1500 or _AMBIGUOUS.search(match.group('old')):
                    continue
                a, b = match.span('old')
                struck.append((node['start'] + a, node['start'] + b, 'struck_replacement_operand',
                               _evidence(text, node['start'] + match.start(), node['start'] + match.end())))
    for block in (s for s in spans if s['tag'] == 'quoted-block'):
        parent = block['path'].rsplit('/', 1)[0]
        # Nearest preceding represented direct sibling must itself be text.
        # Intervening paragraph/quoted-block cannot borrow an older directive.
        earlier = [s for s in spans if s['path'].rsplit('/', 1)[0] == parent and s['end'] <= block['start']]
        if not earlier:
            continue
        preceding = max(earlier, key=lambda s: (s['end'], s['start'], s['path']))
        if preceding['tag'] != 'text':
            continue
        directive = text[preceding['start']:preceding['end']]
        match = _BLOCK_DIRECTIVE.search(directive)
        if match and not re.search(r'\binserting\b|\badding\b', directive, re.I):
            struck.append((block['start'], block['end'], 'struck_quoted_block',
                           _evidence(text, preceding['start'] + match.start(), preceding['end'])))

    decisions = []
    seen = set()
    for candidate in expanded_output['candidates']:
        mechanism = candidate['mechanism']
        if mechanism not in MECHANISMS:
            raise ValueError('Unknown candidate mechanism')
        for hit in candidate['hits']:
            a, b = hit['start'], hit['end']
            if type(a) is not int or type(b) is not int or not 0 <= a < b <= len(text) or text[a:b] != hit['quote']:
                raise ValueError('Invalid source hit')
            identity = (mechanism, a, b)
            if identity in seen:
                raise ValueError('Duplicate source hit')
            seen.add(identity)
            reasons = []
            evidence = []

            def flag(reason, item):
                if reason not in reasons:
                    reasons.append(reason)
                if item not in evidence:
                    evidence.append(item)

            for header in headers:
                if header['start'] <= a and b <= header['end']:
                    flag('heading_only', _evidence(text, header['start'], header['end']))
            if bodies and all(b <= s['start'] or s['end'] <= a for s in bodies):
                flag('outside_legis_body', _evidence(text, a, b))
            for title in titles:
                if title['start'] <= a and b <= title['end']:
                    flag('official_title', _evidence(text, title['start'], title['end']))
            for parent, header in marked_contexts:
                if parent['start'] <= a and b <= parent['end'] and header['end'] <= a:
                    flag('findings_or_sense_context', _evidence(text, header['start'], header['end']))
            for start, end, reason, item in struck:
                if start <= a and b <= end:
                    flag(reason, item)
            # Always preserve the selected occurrence as evidence, including
            # retained hits; header/directive evidence supplies context separately.
            occurrence = _evidence(text, a, b)
            if occurrence not in evidence:
                evidence.append(occurrence)
            decisions.append(dict(mechanism=mechanism, start=a, end=b, quote=hit['quote'],
                                  candidate_id=candidate['candidate_id'], status='flagged' if reasons else 'retain',
                                  reasons=reasons if reasons else ['no_narrow_context_flag'], evidence=evidence))
    return dict(schema='mechanism-context-triage-v1', classifier_version=VERSION,
                bill_id=view['bill_id'], source_view_hash=expanded_output.get('source_view_hash'),
                input_text_sha256=text_hash, decisions=decisions, all_hits_preserved=True,
                design_motivation_review_hash=DESIGN_MOTIVATION_REVIEW_HASH,
                design_review_exposure=True, quality_text_access=False,
                human_certified=False, historical_feature_eligible=False, semantic_accuracy_verified=False,
                accepted_labels=0, trained_model=False,
                interpretation='Flags are review triage, not legal truth. Retain means not flagged, not approved. Deletion may itself affect a mechanism; no hit is removed.',
                limitations=['No general legal parser or descriptive-project detector',
                             'Ambiguous, long, nested or unbounded striking operands are retained',
                             'Missing legis-body boundaries do not establish nonoperative location',
                             'Known 24 design items motivated rules and are not held-out validation'])
