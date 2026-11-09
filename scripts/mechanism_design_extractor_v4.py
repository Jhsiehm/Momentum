"""Adversarially constrained expansion; legacy locators remain explicitly risky.

Only expanded v3 rules are searched within complete leaf text nodes. Inline XML
formatting stays contiguous, but separate legislative blocks cannot form a new
expanded hit. Frozen v2 legacy hits are retained (including its whole-view risks).
All legacy suggestions are quarantined, not selectively treated as validated.
"""
import copy
import hashlib
import json
import re

from scripts.mechanism_design_extractor import MECHANISMS, _context, _role
from scripts.mechanism_design_extractor_v2 import extract as extract_v2
from scripts.mechanism_design_extractor_v3 import RULES as V3_RULES, _attach_new_context

VERSION = 'assisted-mechanism-candidates-v4-leaf-scope'
# A bounded subject grammar, not a general prohibition parser. Deliberately
# abstains on coordinated subjects, unknown noun heads and punctuation-heavy
# relative clauses. No cost ... and may is not a negative grammatical subject.
_NEGATIVE = (r'\bno\s+(?:(?:federal|state|local|governmental|public|private|new)\s+){0,3}'
             r'(?:person|individual|applicant|agency|entity|officer|director|secretary|board|commission|court|'
             r'broadcaster|carrier|provider|employer|employee|member|government|company|institution|'
             r'order|cause\s+of\s+action|road|roads|information|evidence)\b'
             r'(?:\s+(?:whose|that|which)\s+(?:(?!(?:and|or|may|shall|not)\b)[\w’\-]+\s+){0,10}'
             r'(?!(?:and|or|may|shall|not)\b)[\w’\-]+)?\s+(?:may|shall)\b')
RULES = tuple(dict(rule, pattern=_NEGATIVE,
                   rationale='Narrow negative grammatical subject only; excludes cost phrases and conjunction bridges.')
              if rule['rule_id'] == 'negative_subject_modal' else dict(rule) for rule in V3_RULES)
_COMPILED = tuple((r, re.compile(r['pattern'], re.I)) for r in RULES)


def _sha(value):
    return hashlib.sha256(value.encode()).hexdigest()


def _leaf_texts(spans):
    """Only text nodes without represented child blocks; no concatenation."""
    return [s for s in spans if s['tag'] == 'text' and not any(
        other['path'].startswith(s['path'] + '/') for other in spans)]


def extract(view):
    result = extract_v2(view)
    text = view['text']
    spans = sorted(view['spans'], key=lambda s: (s['start'], -s['end'], s['path']))
    leaves = _leaf_texts(spans)
    # Hash-valid spans can still make false hierarchy claims. Reject overlapping
    # unrelated paths instead of selecting a misleading nearest source node.
    active = []
    for span in spans:
        active = [s for s in active if s['end'] > span['start']]
        for other in active:
            if span['start'] < span['end'] and not (span['path'].startswith(other['path'] + '/') or other['path'].startswith(span['path'] + '/')):
                raise ValueError('Overlapping unrelated source spans')
        active.append(span)
    groups = {(c['context_path'], c['mechanism']): c for c in result['candidates']}
    existing = {(c['mechanism'], h['start'], h['end']): h for c in result['candidates'] for h in c['hits']}
    legacy_keys = set(existing)
    new_hits = []
    matched = set()
    for rule, pattern in _COMPILED:
        mechanism = rule['mechanism']
        for leaf in leaves:
            for match in pattern.finditer(text, leaf['start'], leaf['end']):
                a, b = match.span()
                matched.add((rule['rule_id'], a, b))
                identity = (mechanism, a, b)
                if identity in existing:
                    hit = existing[identity]
                    hit.setdefault('rule_ids', []).append(rule['rule_id'])
                    continue
                context = _context(text, spans, a, b)
                key = (context['path'], mechanism)
                if key not in groups:
                    role, warnings = _role(text, spans, context)
                    groups[key] = dict(candidate_id='c_' + _sha(json.dumps([view['bill_id'], _sha(text), *key], ensure_ascii=False))[:20],
                                       mechanism=mechanism, start=context['start'], end=context['end'],
                                       quote=text[context['start']:context['end']], hits=[], context_path=context['path'],
                                       context_tag=context['tag'], context_role=role, warnings=warnings,
                                       interpretation_status='unreviewed_locator')
                hit = dict(start=a, end=b, quote=text[a:b], rule_ids=[rule['rule_id']],
                           expansion_scope='complete_leaf_text', leaf_text_path=leaf['path'])
                groups[key]['hits'].append(hit)
                existing[identity] = hit
                new_hits.append(hit)
    excluded = []
    for rule in V3_RULES:
        for match in re.finditer(rule['pattern'], text, re.I):
            a, b = match.span()
            if (rule['rule_id'], a, b) in matched:
                continue
            contained = any(s['start'] <= a and b <= s['end'] for s in leaves)
            excluded.append(dict(rule_id=rule['rule_id'], mechanism=rule['mechanism'], start=a, end=b,
                                 quote=text[a:b], reason='negative_subject_pattern_rejected' if contained else 'not_within_complete_leaf_text',
                                 remains_as_legacy_hit=(rule['mechanism'], a, b) in legacy_keys))
    result['candidates'] = sorted(groups.values(), key=lambda c: (c['start'], c['end'], MECHANISMS.index(c['mechanism']), c['context_path']))
    for candidate in result['candidates']:
        candidate['hits'].sort(key=lambda h: (h['start'], h['end']))
    _attach_new_context(view, result, new_hits)
    for mechanism, assessment in result['assessments'].items():
        assessment['candidate_count'] = sum(c['mechanism'] == mechanism for c in result['candidates'])
        if assessment['candidate_count']:
            assessment['reason'] = 'Candidate language requires legal interpretation; no accepted mechanism status emitted'
    result['legacy_proposals'] = [dict(proposal=copy.deepcopy(p), quarantine_reason='All legacy surface-rule suggestions withheld pending semantic validation') for p in result['proposals']]
    result['proposals'] = []
    result['schema'] = 'assisted-annotation-candidates-v4'
    result['previous_extractor_version'] = result['extractor_version']
    result['extractor_version'] = VERSION
    result['excluded_v3_rule_matches'] = excluded
    result['lexical_rule_manifest_sha256'] = _sha(json.dumps(RULES, sort_keys=True, separators=(',', ':')))
    result['legacy_locator_scope_warning'] = 'Frozen v2 hits are retained unchanged; legacy whole-view boundary and semantic false positives are not fixed by v4 expansion scoping'
    result['expansion_scope'] = 'Only complete leaf text nodes; no headings, metadata or cross-block expanded matches'
    result['proposal_policy'] = 'All legacy suggestions quarantined intentionally; this is withholding, not measured accuracy improvement'
    return result
