"""Source-local assisted-annotation candidate extractor; never accepted v2 labels.

``extract(view)`` is pure and deterministic. It scans every character of a supplied
boundary-aware reading view, retains whole enclosing sections as review context,
and exposes lexical hits separately. Narrow clause rules produce *suggestions*,
not a learned model, semantic certification, historical features, or absence
claims. No filesystem, network, outcomes, or model access occurs in extract().
"""
from __future__ import annotations

import hashlib
import json
import re

VERSION = "assisted-mechanism-candidates-v1"
MECHANISMS = (
    "create_programme", "authorize", "appropriate", "tax", "prohibit", "require",
    "amend", "repeal", "rename_designate", "reporting", "deadline", "sunset",
)
# Retrieval vocabulary only. Matches can be negated, quoted, deleted or nonoperative.
LEXICON = {
    "create_programme": r"\b(?:establish\w*|program(?:me)?s?|fund|commission|council)\b",
    "authorize": r"\b(?:authoriz\w*|may|permission|authority|discretion)\b",
    "appropriate": r"\b(?:appropriat\w*|rescission|rescind\w*|funds|amounts?\s+made\s+available)\b",
    "tax": r"\b(?:tax\w*|Internal\s+Revenue\s+Code|deduct\w*|excise|exemption)\b",
    "prohibit": r"\b(?:prohibit\w*|shall\s+not|may\s+not|no\s+(?:person|funds?|authority)|not\s+more\s+than|without\s+regard)\b",
    "require": r"\b(?:shall|must|requir\w*|need\s+not)\b",
    "amend": r"\b(?:amend\w*|striking|inserting|redesignating|adding)\b",
    "repeal": r"\b(?:repeal\w*|striking|abrogat\w*)\b",
    "rename_designate": r"\b(?:designat\w*|renam\w*|known\s+as|held\s+in\s+trust)\b",
    "reporting": r"\b(?:report\w*|notif\w*|disclos\w*|certif\w*|submit\w*|notice|publish\w*)\b",
    "deadline": r"\b(?:not\s+later\s+than|within|prior\s+to|before|after|annually|each\s+year|every\s+\d+)\b",
    "sunset": r"\b(?:sunset\w*|terminat\w*|expir\w*|until|duration|extend\w*)\b",
}
_PATTERNS = {m: re.compile(p, re.I) for m, p in LEXICON.items()}
_NONOPERATIVE_HEADER = re.compile(r"\b(?:findings?|sense\s+of|short\s+title|table\s+of\s+contents|definitions?)\b", re.I)
_COMPLEX = re.compile(r"\b(?:except|unless|notwithstanding|subject\s+to|if|provided\s+that|shall\s+not\s+be\s+construed|nothing\s+in)\b", re.I)
_LIST_END = re.compile(r"(?:[:;—–]|\b(?:following|that|if|unless))\s*$", re.I)
_STRUCK = re.compile(r"\b(?:striking|strike|stricken|repeal(?:ed)?)\b", re.I)

# Each rule requires a complete, non-list text block. Patterns deliberately do
# not cover all phrasings. The mechanism names are affected mechanisms, not
# policy sentiment; e.g. imposing an expiry suggests sunset/create.
_RULES = (
    ("establishment", "create_programme", "create", "existence", r"There\s+is\s+established\b.+[.]") ,
    ("future_appropriation_authorization", "authorize", "create", "amount", r"There\s+(?:is|are)\s+authorized\s+to\s+be\s+appropriated\b.+[.]"),
    ("direct_appropriation", "appropriate", "create", "amount", r"There\s+(?:is|are)\s+appropriated\b.+[.]"),
    ("express_tax_imposition", "tax", "create", "amount", r"There\s+is\s+hereby\s+imposed\s+a\s+tax\b.+[.]"),
    ("express_person_bar", "prohibit", "create", "coverage", r"No\s+person\s+(?:may|shall)\b.+[.]"),
    ("secretary_action", "require", "create", "procedure", r"The\s+Secretary\s+shall\s+(?!not\b|be\s+(?:authorized|permitted)\b)(?:submit|provide|conduct|establish|publish|prepare|complete|pay|notify)\b.+[.]"),
    ("statutory_addition", "amend", "create", "text", r"(?:Section|Subsection|Paragraph)\b.+\bis\s+amended\s+by\s+(?:adding|inserting)\b.+[.]"),
    ("express_whole_repeal", "repeal", "remove", "text", r"(?:Section|Subsection|Paragraph)\b.+\bis\s+repealed[.]"),
    ("express_designation", "rename_designate", "create", "coverage", r"The\s+.+\bis\s+designated\s+as\s+.+[.]"),
    ("report_submission", "reporting", "create", "procedure", r"The\s+Secretary\s+shall\s+submit\b.+\breport\b.*[.]"),
    ("action_due_by", "deadline", "create", "duration", r"Not\s+later\s+than\b.+,\s+the\s+Secretary\s+shall\s+(?:submit|provide|conduct|establish|publish|prepare|complete|notify)\b.+[.]"),
    ("authority_expiry", "sunset", "create", "duration", r"The\s+authority\b.+\b(?:shall\s+expire|terminates?)\b.+[.]"),
)


def _sha(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _check_view(view: dict) -> tuple[str, list[dict]]:
    if not isinstance(view, dict) or not isinstance(view.get("text"), str):
        raise ValueError("A text reading view is required")
    if not isinstance(view.get("bill_id"), str) or not view["bill_id"]:
        raise ValueError("A bill_id is required")
    text = view["text"]
    spans = view.get("spans")
    if not isinstance(spans, list) or not spans:
        raise ValueError("Boundary-aware spans are required; no fallback sentence parser")
    seen = set()
    for s in spans:
        if not isinstance(s, dict):
            raise ValueError("Invalid span")
        a, b = s.get("start"), s.get("end")
        if type(a) is not int or type(b) is not int or not 0 <= a <= b <= len(text):
            raise ValueError("Invalid character offsets")
        if not isinstance(s.get("path"), str) or not isinstance(s.get("tag"), str):
            raise ValueError("Span path and tag required")
        if s["path"] in seen:
            raise ValueError("Duplicate span path")
        seen.add(s["path"])
        if s.get("text_sha256") != _sha(text[a:b]):
            raise ValueError("Span content hash mismatch")
    by_path = {s["path"]: s for s in spans}
    for s in spans:
        parent_path = s["path"].rsplit("/", 1)[0]
        while parent_path:
            parent = by_path.get(parent_path)
            if parent and not parent["start"] <= s["start"] <= s["end"] <= parent["end"]:
                raise ValueError("Inconsistent ancestor span bounds")
            parent_path = parent_path.rsplit("/", 1)[0]
    h = view.get("view_hash")
    if h is not None and (not isinstance(h, str) or not re.fullmatch(r"[0-9a-f]{64}", h)):
        raise ValueError("Invalid supplied view_hash")
    return text, sorted(spans, key=lambda s: (s["start"], -s["end"], s["path"]))


def _context(text: str, spans: list[dict], a: int, b: int) -> dict:
    # Outermost section retains prefatory negation, parent instructions and lists;
    # selecting a nested paragraph could detach the operative governing clause.
    containers = [s for s in spans if s["start"] <= a and b <= s["end"]]
    sections = [s for s in containers if s["tag"] == "section"]
    if sections:
        return min(sections, key=lambda s: (s["path"].count("/"), s["start"], s["path"]))
    # Outside a section, preserve the complete view rather than invent boundaries.
    return {"start": 0, "end": len(text), "path": "__document__", "tag": "document"}


def _role(text: str, spans: list[dict], context: dict) -> tuple[str, list[str]]:
    headers = [s for s in spans if s["tag"] == "header" and
               s["path"].rsplit("/", 1)[0] == context["path"]]
    if context["tag"] != "section":
        return "outside_section", ["No operative section boundary for this hit"]
    if any(_NONOPERATIVE_HEADER.search(text[s["start"]:s["end"]]) for s in headers):
        return "nonoperative_or_definition_context", ["Header marks findings, sense, title, contents, or definition context; no operative suggestion"]
    value = text[context["start"]:context["end"]]
    warnings = []
    if _STRUCK.search(value):
        warnings.append("Section contains deletion/repeal instructions; language may be struck rather than enacted")
    if _COMPLEX.search(value):
        warnings.append("Conditional, exception, or nonconstruction scope requires full-context review")
    if any(s["tag"] == "quoted-block" and s["path"].startswith(context["path"] + "/") for s in spans):
        warnings.append("Quoted statutory blocks require insertion/deletion-context interpretation")
    return "operative_status_unreviewed", warnings


def extract(view: dict) -> dict:
    """Return locator candidates, narrow suggestions and twelve abstentions.

    Input is an unsealed boundary-aware renderer body with optional ``view_hash``
    binding its original sealed envelope. This function validates span hashes but
    cannot authenticate that envelope or establish source/historical completeness.
    Candidate quote spans are *review context*. ``hits`` contain exact lexical
    trigger locations for locator diagnostics; neither overlap is semantic recall.
    """
    text, spans = _check_view(view)
    groups = {}
    for mechanism in MECHANISMS:
        for match in _PATTERNS[mechanism].finditer(text):
            context = _context(text, spans, *match.span())
            key = (context["path"], mechanism)
            if key not in groups:
                role, warnings = _role(text, spans, context)
                groups[key] = {
                    "candidate_id": "c_" + _sha(json.dumps([view["bill_id"], _sha(text), *key], ensure_ascii=False))[:20],
                    "mechanism": mechanism, "start": context["start"], "end": context["end"],
                    "quote": text[context["start"]:context["end"]], "hits": [],
                    "context_path": context["path"], "context_tag": context["tag"],
                    "context_role": role, "warnings": warnings,
                    "interpretation_status": "unreviewed_locator",
                }
            groups[key]["hits"].append({"start": match.start(), "end": match.end(), "quote": match.group()})
    candidates = sorted(groups.values(), key=lambda c: (c["start"], c["end"], MECHANISMS.index(c["mechanism"]), c["context_path"]))
    proposals = []
    suppressed = []
    # Only direct text nodes are eligible. No isolated list member, quoted block,
    # nested paragraph, or inline heading is promoted by the narrow rules.
    for node in spans:
        if node["tag"] != "text":
            continue
        value = text[node["start"]:node["end"]].strip()
        if not value:
            continue
        a = node["start"] + len(text[node["start"]:node["end"]]) - len(text[node["start"]:node["end"]].lstrip())
        b = a + len(value)
        context = _context(text, spans, a, b)
        role, warnings = _role(text, spans, context)
        local_parent = node["path"].rsplit("/", 1)[0]
        reasons = []
        if role != "operative_status_unreviewed":
            reasons.append("nonoperative_or_unclassified_context")
        if "/quoted-block[" in node["path"]:
            reasons.append("quoted_statutory_text_requires_review")
        if local_parent != context["path"]:
            reasons.append("nested_clause_may_depend_on_parent")
        if _LIST_END.search(value):
            reasons.append("incomplete_list_or_clause")
        if _COMPLEX.search(text[context["start"]:context["end"]]):
            reasons.append("conditional_or_negated_scope_requires_review")
        # More than one direct text block or subordinate legislative block can
        # change the meaning of an apparently simple sentence.
        descendants = [s for s in spans if s["path"].startswith(context["path"] + "/")]
        if any(s["tag"] in {"subsection", "paragraph", "subparagraph", "clause", "quoted-block"} for s in descendants):
            reasons.append("section_has_dependent_blocks")
        if sum(s["tag"] == "text" for s in descendants) != 1:
            reasons.append("section_has_multiple_text_blocks")
        for rule_id, mechanism, operation, dimension, pattern in _RULES:
            if not re.fullmatch(pattern, value, re.I | re.S):
                continue
            rule_reasons = list(reasons)
            if _STRUCK.search(text[context["start"]:context["end"]]) and mechanism != "repeal":
                rule_reasons.append("struck_text_context")
            if re.search(r"\b(?:finds?|sense\s+of|should|example|quot(?:e|ed|ation))\b", value, re.I):
                rule_reasons.append("nonoperative_language")
            if re.search(r"[.!?]\s+[A-Z]", value):
                rule_reasons.append("multiple_sentence_or_abbreviation_review")
            key = (context["path"], mechanism)
            if key not in groups:
                continue
            if rule_reasons:
                suppressed.append({"rule_id": rule_id, "candidate_id": groups[key]["candidate_id"],
                                   "start": a, "end": b, "reasons": sorted(set(rule_reasons))})
                continue
            proposals.append({
                "proposal_id": "p_" + _sha(f"{groups[key]['candidate_id']}:{rule_id}:{a}:{b}")[:20],
                "candidate_id": groups[key]["candidate_id"], "rule_id": rule_id,
                "mechanism": mechanism, "suggested_operation": operation, "suggested_dimension": dimension,
                "start": a, "end": b, "quote": text[a:b],
                "interpretation_status": "unvalidated_rule_supported_suggestion",
                "requires_full_context_review": True,
                "rationale": "Complete direct text block matches the named narrow surface rule; source context is retained in the candidate. This is not an accepted v2 effect.",
            })
    counts = {m: sum(c["mechanism"] == m for c in candidates) for m in MECHANISMS}
    assessments = {
        m: {"status": "abstain", "candidate_count": counts[m],
            "reason": ("Candidate language requires legal interpretation; no accepted mechanism status emitted"
                       if counts[m] else "No locator match; lexical silence is not evidence of absence")}
        for m in MECHANISMS
    }
    return {
        "schema": "assisted-annotation-candidates-v1", "extractor_version": VERSION,
        "bill_id": view["bill_id"], "source_view_hash": view.get("view_hash"),
        "input_text_sha256": _sha(text), "candidates": candidates, "proposals": proposals,
        "suppressed_proposals": suppressed, "assessments": assessments,
        "coverage": {"characters_supplied": len(text), "characters_scanned": len(text),
                     "scan_ranges": [[0, len(text)]], "input_view_scanned_completely": True,
                     "span_count": len(spans), "truncated": False,
                     "source_document_completeness_verified": False,
                     "semantic_coverage": "not_established",
                     "provenance_warning": None if view.get("view_hash") else "Original sealed view hash not supplied"},
        "human_certified": False, "historical_feature_eligible": False,
        "accepted_v2_labels_created": 0, "trained_model": False,
    }
