"""Bounded additional negative-subject locators on frozen v4, not semantics.

Rules derive from exposed design failures. No bill identifiers or reference spans
are encoded. The full v4 result, including risky legacy hits, stays available.
"""
import json
import re
from scripts.mechanism_design_extractor import MECHANISMS, _context, _role
from scripts.mechanism_design_extractor_v3 import _attach_new_context
from scripts.mechanism_design_extractor_v4 import extract as extract_v4, _leaf_texts, _sha

VERSION = 'assisted-mechanism-candidates-v5-bounded-subjects'
# Exclude conjunctions, another negative subject, modal verbs and punctuation.
# Deliberately not an unrestricted wildcard or a general noun-phrase parser.
_WORD = r'(?!(?:and|or|but|no|not|may|shall|can|could|would|will|must)\b)[\w’\-]+'
_MODAL = r'\s+(?:may|shall)\b(?!\s+not\b)'
RULES = (
    dict(rule_id='negative_franchise_authority', mechanism='prohibit',
         pattern=r'\bno\s+(?:(?:state|local)\s+)?franchise\s+authorit(?:y|ies)' + _MODAL,
         rationale='Named authority head followed directly by modal; locator only.'),
    dict(rule_id='negative_information_qualified', mechanism='prohibit',
         pattern=r'\bno\s+information\s+(?:concerning|obtained|acquired)(?:\s+' + _WORD + r'){1,24}' + _MODAL,
         rationale='Information with a bounded uninterrupted modifier; no conjunction or sentence bridge.'),
    dict(rule_id='negative_evidence_derived', mechanism='prohibit',
         pattern=r'\bno\s+evidence\s+derived\s+(?:therefrom|from(?:\s+' + _WORD + r'){1,24})' + _MODAL,
         rationale='Derived evidence head with therefrom or bounded from qualifier.'),
    dict(rule_id='negative_pay_rate_fixed', mechanism='prohibit',
         pattern=r'\bno\s+rate\s+of\s+pay\s+fixed\s+(?:under|pursuant\s+to)(?:\s+' + _WORD + r'){1,12}' + _MODAL,
         rationale='Pay-rate head with bounded fixing authority qualifier.'),
    dict(rule_id='negative_coordinated_roads', mechanism='prohibit',
         pattern=r'\bno\s+(?:new\s+)?(?:(?:permanent|temporary)(?:\s+(?:or|and)\s+(?:permanent|temporary))?\s+)?roads?'
                 r'(?:\s+(?:or|and)\s+(?:other\s+)?(?:motorized\s+)?(?:vehicle\s+)?routes?)?' + _MODAL,
         rationale='Explicit road adjectives and road/route coordination only; no arbitrary clause coordination.'),
)
_COMPILED = tuple((r, re.compile(r['pattern'], re.I)) for r in RULES)


def extract(view):
    result = extract_v4(view)
    text = view['text']
    spans = sorted(view['spans'], key=lambda s: (s['start'], -s['end'], s['path']))
    groups = {(c['context_path'], c['mechanism']): c for c in result['candidates']}
    existing = {(c['mechanism'], h['start'], h['end']): h for c in result['candidates'] for h in c['hits']}
    new_hits = []
    for rule, pattern in _COMPILED:
        for leaf in _leaf_texts(spans):
            for match in pattern.finditer(text, leaf['start'], leaf['end']):
                a, b = match.span()
                identity = (rule['mechanism'], a, b)
                if identity in existing:
                    existing[identity].setdefault('rule_ids', []).append(rule['rule_id'])
                    continue
                context = _context(text, spans, a, b)
                key = (context['path'], rule['mechanism'])
                if key not in groups:
                    role, warnings = _role(text, spans, context)
                    groups[key] = dict(candidate_id='c_' + _sha(json.dumps([view['bill_id'], _sha(text), *key], ensure_ascii=False))[:20],
                                       mechanism=rule['mechanism'], start=context['start'], end=context['end'],
                                       quote=text[context['start']:context['end']], hits=[], context_path=context['path'],
                                       context_tag=context['tag'], context_role=role, warnings=warnings,
                                       interpretation_status='unreviewed_locator')
                hit = dict(start=a, end=b, quote=text[a:b], rule_ids=[rule['rule_id']],
                           expansion_scope='complete_leaf_text', leaf_text_path=leaf['path'])
                groups[key]['hits'].append(hit)
                existing[identity] = hit
                new_hits.append(hit)
    result['candidates'] = sorted(groups.values(), key=lambda c: (c['start'], c['end'], MECHANISMS.index(c['mechanism']), c['context_path']))
    for candidate in result['candidates']:
        candidate['hits'].sort(key=lambda h: (h['start'], h['end']))
    _attach_new_context(view, result, new_hits)
    for mechanism, assessment in result['assessments'].items():
        assessment['candidate_count'] = sum(c['mechanism'] == mechanism for c in result['candidates'])
        if assessment['candidate_count']:
            assessment['reason'] = 'Candidate language requires legal interpretation; no accepted mechanism status emitted'
    result['schema'] = 'assisted-annotation-candidates-v5'
    result['previous_extractor_version'] = result['extractor_version']
    result['extractor_version'] = VERSION
    result['previous_lexical_rule_manifest_sha256'] = result['lexical_rule_manifest_sha256']
    result['lexical_rule_manifest_sha256'] = _sha(json.dumps(RULES, sort_keys=True, separators=(',', ':')))
    result['v5_rule_interpretation'] = 'Five exposed-design-derived bounded locator families; no semantic labels or independent quality claims'
    result['excluded_v3_rule_matches_interpretation'] = 'Frozen v4 exclusion provenance; a v5 rule may separately recover the same location'
    return result
