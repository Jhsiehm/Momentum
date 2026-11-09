"""Versioned syntax triage for qualified, structurally inherited striking.

Adds no legal-effect decisions. Restores only frozen deletion flags supported
by a bounded chain of amendment-scope lead-ins; retains v2 provenance unchanged.
"""
import copy
import re

from scripts.mechanism_context_filter_v2 import (
    classify as classify_v2, RULES as V2_RULES, _AFFIRM, _VETO, _DELETION,
)

VERSION = 'mechanism-context-triage-v3-qualified-structural-provenance'
RULES = tuple(dict(r, description=r['description'] + (
    ' Allows bounded qualified structural scope chains with affirmative ancestor declaration.'
    if r['id'] in _DELETION else '')) for r in V2_RULES)
# Only legislative subdivision references, never free-form descriptions. Each
# qualification must consume the entire prefix/lead-in; no search-and-skip.
_UNIT = r'(?:section|subsection|paragraph|subparagraph|clause|subclause)'
_REF = r'(?:\([A-Za-z0-9]{1,12}\)){1,4}|\d[\w().–-]{0,30}'
_SCOPE = rf'in\s+(?:{_UNIT}\s+(?:{_REF})|the\s+matter\s+preceding\s+{_UNIT}\s+(?:{_REF}))(?:\s*,\s*as\s+redesignated)?'
_SCOPE_CHAIN = re.compile(rf'{_SCOPE}(?:\s*,\s*{_SCOPE}){{0,3}}', re.I)


def _scope(value):
    return len(value) <= 512 and bool(_SCOPE_CHAIN.fullmatch(value.strip().rstrip(',—–-').strip()))


def _qualified_proof(text, node, directive_start, spans):
    prefix = text[node['start']:directive_start]
    if not _scope(prefix):
        return None
    evidence = [{'start': node['start'], 'end': directive_start, 'quote': prefix}]
    by_path = {s['path']: s for s in spans}
    ancestor = node['path'].rsplit('/', 1)[0]
    # Fixed depth cap limits inference through extremely deep structures.
    for _ in range(12):
        if not ancestor:
            break
        parent = by_path.get(ancestor)
        if parent and parent['tag'] == 'quoted-block':
            return None
        branch = ancestor + '/' + node['path'][len(ancestor) + 1:].split('/', 1)[0]
        branch_nodes = [s for s in spans if s['path'] == branch or s['path'].startswith(branch + '/')]
        if not branch_nodes:
            return None
        branch_start = min(s['start'] for s in branch_nodes)
        preceding = [s for s in spans if s['tag'] == 'text'
                     and s['path'].rsplit('/', 1)[0] == ancestor and s['end'] <= branch_start]
        if preceding:
            lead = max(preceding, key=lambda s: (s['end'], s['start'], s['path']))
            value = text[lead['start']:lead['end']]
            item = {'start': lead['start'], 'end': lead['end'], 'quote': value}
            if len(value) > 512 or _VETO.search(value):
                return None
            if _AFFIRM.fullmatch(value.strip().rstrip('—–-:').strip()):
                return evidence + [item]
            if not _scope(value):
                return None
            evidence.append(item)
        ancestor = ancestor.rsplit('/', 1)[0]
    return None


def classify(view, expanded_output):
    result = classify_v2(view, expanded_output)
    text, spans = view['text'], view['spans']
    texts = [s for s in spans if s['tag'] == 'text']
    for decision in result['decisions']:
        decision['previous_status'] = decision['status']
        decision['previous_reasons'] = list(decision['reasons'])
        decision['previous_evidence'] = copy.deepcopy(decision['evidence'])
        if decision.get('deletion_provenance') != 'not_established':
            continue
        missing = _DELETION.intersection(decision['legacy_reasons'])
        if not missing:
            continue
        proof = None
        for item in decision['legacy_evidence']:
            if not re.match(r'by\s+striking\b', item['quote'], re.I):
                continue
            containers = [s for s in texts if s['start'] <= item['start'] and item['end'] <= s['end']]
            if containers:
                node = max(containers, key=lambda s: s['path'].count('/'))
                proof = _qualified_proof(text, node, item['start'], spans)
                if proof:
                    break
        if proof:
            decision['reasons'] = list(decision['legacy_reasons'])
            decision['status'] = 'flagged'
            decision['evidence'] = copy.deepcopy(decision['legacy_evidence'])
            for item in proof:
                if item not in decision['evidence']:
                    decision['evidence'].append(item)
            decision['deletion_provenance'] = 'qualified_structural_affirmative_amendment_source'
    result['previous_classifier_version'] = result['classifier_version']
    result['classifier_version'] = VERSION
    result['schema'] = 'mechanism-context-triage-v3'
    result['limitations'].append('Qualified scope inheritance is bounded syntax triage, not a determination of legal operation; unsupported qualifiers remain unflagged')
    return result
