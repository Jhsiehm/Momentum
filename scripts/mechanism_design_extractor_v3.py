"""Design-only lexical expansion of frozen v2 assisted-annotation locators.

Rules derive from reviewed vocabulary-gap diagnoses, not quality data or run
metrics. They retrieve review candidates, never prove an effect or an absence.
The v2 structural algorithm is locally reproduced for new hits only because the
frozen module exposes no attachment helper. Dependency hashes below record the
reviewed source versions; the bounded runner authenticates files outside extract.
No monkeypatching, model, network, filesystem access, or global mutation occurs.
"""
from __future__ import annotations

import hashlib
import json
import re

from scripts.mechanism_design_extractor import MECHANISMS, _context, _role
from scripts.mechanism_design_extractor_v2 import extract as extract_v2

VERSION = 'assisted-mechanism-candidates-v3-lexical'
DEPENDENCY_SHA256 = {
    'scripts/mechanism_design_extractor.py': 'b8b58af1f787a703b66ade28e59ebf6a6d8be65649d979bf6f87beeb3deef7a5',
    'scripts/mechanism_design_extractor_v2.py': 'b248aede8fbb5955fee7d4d9938a4817d686bb620dcf0c7afa30969370131825',
}


def _rule(rule_id, mechanism, pattern, rationale):
    return dict(rule_id=rule_id, mechanism=mechanism, pattern=pattern, rationale=rationale)


# Bounded, generic phrasing only. Negation/findings/struck text can match: these
# are locators and retain full review context, not inferred operative semantics.
RULES = (
    _rule('issue_statement', 'reporting', r'\bissue\s+(?:a\s+)?(?:detailed\s+)?statement\b', 'A statement can be a communication output; inspect its object and legal force.'),
    _rule('furnish_information', 'reporting', r'\bfurnish\s+(?:such\s+)?(?:information|records|estimates|statistics)\b', 'Furnishing identified information may communicate it to a recipient.'),
    _rule('display_website', 'reporting', r'\bdisplay\s+on\s+(?:the|a|an)\s+website\b', 'Website display can be public disclosure, subject to governing clause.'),
    _rule('advise_in_writing', 'reporting', r'\badvise\b[^.;:!?]{0,100}\bin\s+writing\b', 'Written advice may be an information duty; retrieve the bounded phrase.'),
    _rule('provide_records', 'reporting', r'\bprovide\b[^.;:!?]{0,160}\b(?:records|information|data)\b', 'Identified information provision is a locator, not a generic provide keyword.'),
    _rule('file_document', 'reporting', r'\bfile\s+(?:a|an|the)\s+(?:map|report|statement|notice|legal\s+description|application)\b', 'Document filing differs from file cabinet or filesystem vocabulary.'),
    _rule('demonstrate_match', 'reporting', r'\bdemonstrate\b[^.;:!?]{0,160}\b(?:matched|matching|match)\b', 'Grant-match demonstration may be an eligibility information requirement.'),
    _rule('information_available', 'reporting', r'\binformation\b[^.;:!?]{0,80}\bshall\s+be\s+available\s+to\b', 'Availability to recipients can be disclosure rather than collection alone.'),
    _rule('annual_report', 'deadline', r'\bannual\s+reports?\b', 'Recurring report timing; annual salary is intentionally excluded.'),
    _rule('annual_basis', 'deadline', r'\b(?:submit|provide|transfer|pay)\b[^.;:!?]{0,60}\bon\s+an\s+annual\s+basis\b', 'Annual-basis action wording, subject to mandatory context.'),
    _rule('semiannual_action', 'deadline', r'\b(?:conduct|hold)\b[^.;:!?]{0,120}\bsemiannually\b', 'Meeting-action recurrence, not a free-standing frequency adjective.'),
    _rule('frequency_action', 'deadline', r'\b(?:payments?|transfers?|meetings?|reports?)\b[^.;:!?]{0,100}\bnot\s+less\s+frequently\s+than\s+(?:\d+|two|three|four)\s+times\s+a\s+year\b', 'Minimum action recurrence does not imply evenly spaced intervals.'),
    _rule('event_date_action', 'deadline', r'\bprovides?\b[^.;:!?]{0,120}\bon\s+the\s+date\s+on\s+which\b', 'Provision tied to an event date needs its complete object and conditions.'),
    _rule('evaluation_year_window', 'deadline', r'\bduring\b[^.;:!?]{0,90}\byears?\s+of\s+operations?\s*,[^.;:!?]{0,90}\bevaluation\b', 'Evaluation during operating years is distinct from funding-year coverage.'),
    _rule('election_relative', 'deadline', r'\b(?:broadcast|allotted)\b[^.;:!?]{0,120}\b(?:months?|weeks?)\s+immediately\s+preceding\s+election\s+day\b', 'Election-relative broadcast action windows need parent mandatory scope.'),
    _rule('negative_subject_modal', 'prohibit', r'\bno\s+(?:[\w’\-]+\s+){1,12}(?:may|shall)\b', 'Bounded no-subject-modal variants; punctuation prevents sentence bridging.'),
    _rule('maximum_award', 'prohibit', r'\bmaximum\s+amount\s+of\s+(?:a|an|the)\s+(?:grant|voucher|award)\b', 'Award ceilings can limit conduct but do not appropriate money.'),
    _rule('not_greater_than', 'prohibit', r'\bshall\s+be\s+not\s+greater\s+than\b', 'Explicit upper-bound phrasing omitted by not-more-than locators.'),
    _rule('only_permission', 'prohibit', r'\b(?:may\s+only|only\s+pursuant\s+to|only\s+in\s+accordance\s+with|shall\s+allow\s+only|shall\s+be\s+permitted\s+only|may\s+be\s+issued\b[^.;:!?]{0,65}\bonly)\b', 'Only-based permission limits require full exception and object review.'),
    _rule('supplement_not_supplant', 'prohibit', r'\bsupplement\s*,?\s+and\s+not\s+supplant\b', 'Supplement-not-supplant language can constrain resource use.'),
    _rule('ineligible_funding', 'prohibit', r'\bshall\s+be\s+ineligible\s+to\s+receive\s+(?:additional\s+)?funding\b', 'Funding ineligibility may be a conditional conduct bar.'),
    _rule('none_amounts', 'prohibit', r'\bnone\s+of\s+the\s+amounts\b[^.;:!?]{0,100}\bmay\s+be\s+(?:obligated|expended)\b', 'Negative spending-use formulation, not direct money provision.'),
    _rule('land_withdrawal', 'prohibit', r'\b(?:land|lands)\b[^.;:!?]{0,300}\b(?:is|are)\s+withdrawn\s+from\b', 'Land withdrawal requires the governed use list and retained-rights scope.'),
    _rule('right_or_option', 'authorize', r'\bshall\s+have\s+the\s+(?:right|option)\b', 'A stated right or option can be discretion despite shall wording.'),
    _rule('retain_right', 'authorize', r'\bshall\s+retain\s+(?:any|the)\s+(?:right|claim)\b', 'Express retention is preservation, not an automatic new power.'),
    _rule('jurisdiction_savings', 'authorize', r'\bnothing\b[^.;:!?]{0,100}\baffects\s+the\s+jurisdiction\b', 'Noninterference with jurisdiction can preserve legal authority.'),
    _rule('appropriate_discretion', 'authorize', r'\b(?:as|to\s+the\s+extent)\s+(?:[\w’\-]+\s+){0,8}(?:determines?|deems?)\s+appropriate\b', 'A scoped appropriateness decision may allocate discretion; not every decision does.'),
    _rule('authorities', 'authorize', r'\bauthorities\b', 'Plural authority wording retains withdrawal/preservation review context.'),
    _rule('not_unauthorized', 'authorize', r'\bshall\s+not\s+constitute\s+(?:the\s+)?unauthorized\s+use\b', 'Double-negative permissible-use phrasing needs the complete governed list.'),
    _rule('deemed_approval', 'rename_designate', r'\bis\s+deemed\s+to\s+be\s+subject\s+to\s+an?\s+(?:application|premarket\s+notification)\b', 'Potential substantive approval status, not all deemed language.'),
    _rule('calendar_designation', 'rename_designate', r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}\s+is\s+(?:[\w’\-]+\s+){0,6}Day\b', 'Calendar designation phrasing; headings and statutory context remain necessary.'),
    _rule('boundary_exclusion', 'rename_designate', r'\bboundary\b[^.;:!?]{0,160}\b(?:modified|adjusted)\s+to\s+exclude\b', 'Boundary exclusion may change a legal designation, not necessarily a programme.'),
    _rule('reimplement_initiative', 'create_programme', r'\breimplement\b[^.;:!?]{0,100}\binitiative\b', 'Reimplementation of an initiative needs named-framework context.'),
)
_COMPILED = tuple((r, re.compile(r['pattern'], re.I)) for r in RULES)


def _sha(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def _attach_new_context(view, result, hits):
    """Frozen-v2 hierarchy/order algorithm, applied only to newly located hits."""
    text = view['text']
    spans = sorted(view['spans'], key=lambda s: (s['start'], -s['end'], s['path']))
    by_path = {s['path']: s for s in spans}
    children = {}
    for s in spans:
        children.setdefault(s['path'].rsplit('/', 1)[0], []).append(s)
    pool = {s['path']: s for s in result['structural_spans']}
    by_id = {s['span_id']: s for s in pool.values()}

    def reference(span, relation, ancestor):
        path = span['path']
        identifier = 's_' + _sha(path)[:24]
        if path not in pool:
            pool[path] = dict(span_id=identifier, path=path, tag=span['tag'], start=span['start'],
                              end=span['end'], quote=text[span['start']:span['end']])
        by_id[identifier] = pool[path]
        return dict(span_id=identifier, relation=relation, ancestor_path=ancestor)

    for hit in hits:
        containers = [s for s in spans if s['start'] <= hit['start'] and hit['end'] <= s['end']]
        anchor = max(containers, key=lambda s: (s['path'].count('/'), s['start'], -s['end'], s['path'])) if containers else None
        containing = [s for s in containers if s['tag'] in {'text', 'header'}]
        refs = [reference(s, 'containing_' + s['tag'], None) for s in containing]
        boundaries = []
        if anchor:
            ancestor = anchor['path'].rsplit('/', 1)[0]
            while ancestor:
                parent = by_path.get(ancestor)
                if parent and parent['tag'] == 'quoted-block':
                    boundaries.append(reference(parent, 'quoted_block_boundary', ancestor))
                branch_path = ancestor + '/' + anchor['path'][len(ancestor) + 1:].split('/', 1)[0]
                branch = by_path.get(branch_path)
                branch_start = branch['start'] if branch else min(s['start'] for s in spans if s['path'] == branch_path or s['path'].startswith(branch_path + '/'))
                for s in children.get(ancestor, []):
                    if s['end'] > branch_start or not text[s['start']:s['end']].strip():
                        continue
                    if s['tag'] == 'header':
                        refs.append(reference(s, 'ancestor_header', ancestor))
                    elif s['tag'] == 'text':
                        refs.append(reference(s, 'ancestor_preceding_direct_text', ancestor))
                ancestor = ancestor.rsplit('/', 1)[0]
        hit['structural_context'] = sorted(refs, key=lambda r: (by_id[r['span_id']]['start'], r['relation'], r['span_id']))
        hit['structural_boundaries'] = boundaries
        hit['structural_context_status'] = ('containing_text_or_header' if containing else 'container_only' if anchor else 'no_containing_boundary')
        hit['semantic_governance_verified'] = False
    result['structural_spans'] = sorted(pool.values(), key=lambda s: (s['start'], s['end'], s['path']))


def extract(view):
    """Pure additive locators; proposals remain the frozen v2 proposals only."""
    result = extract_v2(view)
    text = view['text']
    spans = sorted(view['spans'], key=lambda s: (s['start'], -s['end'], s['path']))
    groups = {(c['context_path'], c['mechanism']): c for c in result['candidates']}
    existing = {(c['mechanism'], h['start'], h['end']): h for c in result['candidates'] for h in c['hits']}
    new_hits = []
    for rule, pattern in _COMPILED:
        mechanism = rule['mechanism']
        for match in pattern.finditer(text):
            identity = (mechanism, match.start(), match.end())
            if identity in existing:
                hit = existing[identity]
                hit.setdefault('rule_ids', []).append(rule['rule_id'])
                continue
            context = _context(text, spans, *match.span())
            key = (context['path'], mechanism)
            if key not in groups:
                role, warnings = _role(text, spans, context)
                groups[key] = dict(candidate_id='c_' + _sha(json.dumps([view['bill_id'], _sha(text), *key], ensure_ascii=False))[:20],
                                   mechanism=mechanism, start=context['start'], end=context['end'],
                                   quote=text[context['start']:context['end']], hits=[], context_path=context['path'],
                                   context_tag=context['tag'], context_role=role, warnings=warnings,
                                   interpretation_status='unreviewed_locator')
            hit = dict(start=match.start(), end=match.end(), quote=match.group(), rule_ids=[rule['rule_id']])
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
    result['schema'] = 'assisted-annotation-candidates-v3'
    result['previous_extractor_version'] = result['extractor_version']
    result['extractor_version'] = VERSION
    result['lexical_rule_manifest_sha256'] = _sha(json.dumps(RULES, sort_keys=True, separators=(',', ':')))
    result['structural_dependency_sha256'] = dict(DEPENDENCY_SHA256)
    result['lexical_expansion_interpretation'] = 'Reviewed design vocabulary locators only; no new effect proposals, semantic decisions, or absence claims'
    return result
