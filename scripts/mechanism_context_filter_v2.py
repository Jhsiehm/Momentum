"""Triage-only correction: require affirmative amendment provenance for deletion.

Frozen filter decisions are preserved per hit as legacy_status/legacy_reasons.
No original candidate is removed. Failure to prove a narrow deletion context
means retain (unless another triage rule flags it), never legal approval.
"""
import copy
import re
from scripts.mechanism_context_filter import classify as classify_v1, RULES as V1_RULES

VERSION = 'mechanism-context-triage-v2-affirmative-provenance'
_DELETION = {'struck_inline_quote', 'struck_replacement_operand', 'struck_quoted_block'}
RULES = tuple(dict(r, description=r['description'] + (' Requires affirmative local or structural-ancestor amendment provenance.' if r['id'] in _DELETION else '')) for r in V1_RULES)
_AFFIRM = re.compile(r'^\s*(?:Section|Subsection|Paragraph|Subparagraph|Clause)\s+(?:\d[\w().–-]*|\([A-Za-z0-9]+\))(?:\s+of\s+[^;!?]{1,180}?)?\s+(?:is|are)\s+amended\b', re.I)
_VETO = re.compile(r'\b(?:not|never|unless|except|if|should|would|could|describes?|discusses?|example|propos(?:al|ed)|inserting|adding)\b', re.I)


def _proof(text, node, directive_start, spans):
    prefix = text[node['start']:directive_start]
    value = text[node['start']:node['end']]
    if _AFFIRM.match(prefix) and not _VETO.search(prefix):
        return {'start': node['start'], 'end': directive_start, 'quote': prefix}
    # A standalone amendment-list instruction may inherit a declaration. A
    # narrative prefix or a quoted-block boundary cannot borrow that authority.
    if prefix.strip() or not re.match(r'\s*by\s+striking\b', value, re.I):
        return None
    ancestor = node['path'].rsplit('/', 1)[0]
    by_path = {s['path']: s for s in spans}
    while ancestor:
        parent = by_path.get(ancestor)
        if parent and parent['tag'] == 'quoted-block':
            return None
        branch = ancestor + '/' + node['path'][len(ancestor) + 1:].split('/', 1)[0]
        branch_start = min(s['start'] for s in spans if s['path'] == branch or s['path'].startswith(branch + '/'))
        preceding = [s for s in spans if s['tag'] == 'text' and s['path'].rsplit('/', 1)[0] == ancestor and s['end'] <= branch_start]
        if preceding:
            lead = max(preceding, key=lambda s: (s['end'], s['start'], s['path']))
            content = text[lead['start']:lead['end']]
            if _VETO.search(content):
                return None
            if _AFFIRM.match(content):
                return {'start': lead['start'], 'end': lead['end'], 'quote': content}
        ancestor = ancestor.rsplit('/', 1)[0]
    return None


def classify(view, expanded_output):
    result = classify_v1(view, expanded_output)
    text, spans = view['text'], view['spans']
    texts = [s for s in spans if s['tag'] == 'text']
    for decision in result['decisions']:
        decision['legacy_status'] = decision['status']
        decision['legacy_reasons'] = list(decision['reasons'])
        decision['legacy_evidence'] = copy.deepcopy(decision['evidence'])
        deletion_reasons = _DELETION.intersection(decision['reasons'])
        if not deletion_reasons:
            continue
        proof = None
        for evidence in decision['evidence']:
            # The frozen filter's directive evidence starts at 'by striking'.
            # Ignore the standalone occurrence/header evidence and use the full
            # containing text node to establish its affirmative provenance.
            if not re.match(r'by\s+striking\b', evidence['quote'], re.I):
                continue
            containers = [s for s in texts if s['start'] <= evidence['start'] and evidence['end'] <= s['end']]
            if not containers:
                continue
            node = max(containers, key=lambda s: s['path'].count('/'))
            proof = _proof(text, node, evidence['start'], spans)
            if proof:
                break
        if proof:
            if proof not in decision['evidence']:
                decision['evidence'].append(proof)
            decision['deletion_provenance'] = 'affirmative_amendment_source'
        else:
            decision['reasons'] = [r for r in decision['reasons'] if r not in _DELETION]
            decision['status'] = 'flagged' if decision['reasons'] else 'retain'
            if not decision['reasons']:
                decision['reasons'] = ['no_narrow_context_flag']
            decision['deletion_provenance'] = 'not_established'
            # Prior evidence is kept explicitly as legacy evidence. Active
            # evidence retains source occurrence; it does not claim deletion.
            if decision['status'] == 'retain':
                decision['evidence'] = [{'start': decision['start'], 'end': decision['end'], 'quote': decision['quote']}]
    result['previous_classifier_version'] = result['classifier_version']
    result['classifier_version'] = VERSION
    result['schema'] = 'mechanism-context-triage-v2'
    result['limitations'] += ['Deletion provenance grammar intentionally incomplete; narrative, negated and ambiguous directives retained',
                              'Affirmative amendment provenance supports only a triage flag, not semantic effect correctness']
    return result
