# XML coverage v2: offline external DOCTYPE compatibility

Date: 2026-11-08. Reviewer: implementation agent, not human source certification.

## Observed failure and separate correction

The root's first registered 40-bill audit rejected all sources at the v1 DOCTYPE policy. This is an input compatibility failure, not evidence that those sources have missing text. The original module, tests and failed results remain immutable. The separate `scripts/bill_render_coverage_audit_v2.py` keeps the earlier coverage accounting and introduces a narrower declaration policy. No actual 40-bill rerun was performed by this implementation agent before the new registration.

## Policy

An Expat declaration preflight records external DOCTYPE name/public/system identifiers without retrieving any resource. Parameter-entity parsing is disabled. `StartDoctypeDeclHandler` rejects every internal subset, including an empty subset; `EntityDeclHandler` rejects entity declarations; `ExternalEntityRefHandler` rejects attempted external resolution. This operates on parsed XML declarations, including UTF-16, rather than trusting ASCII byte searches. Undefined entities fail parsing rather than disappearing from coverage.

A separate ElementTree builder records the same declaration identifiers and must agree. It does not fetch or resolve the DTD. The frozen renderer is then used unchanged, with its existing restrictions and identity checks. Existing source-byte, supplied-render, span, segment, table, namespace and nontext checks remain intact. A DOCTYPE that points to an unavailable resource is permissible precisely because the audit does not use that resource.

Additional result fields are `audit_version`, `doctype_declarations` and `external_resources_resolved=False`. External declarations add `external_doctype_not_resolved` warnings. DTD defaults, entities, schemas and external semantics are explicitly unevaluated. Character-accounting success still cannot establish document completeness, structure semantics, historical eligibility or human certification.

## Validation

Twelve test methods pass under normal and optimized Python. The v1 structural/source/mixed-content cases are retained, with declaration cases updated for this new policy. Tests cover external PUBLIC and SYSTEM declarations, bare DOCTYPE, nonexistent local and network resources, UTF-8 and UTF-16, predefined character references, empty/internal subsets, internal general/parameter entity declarations and undeclared external entities. Network socket creation is patched to fail during positive external-declaration tests. No acquisition or source modification is performed.

A pre-freeze independent review identified Expat exception normalization as necessary for per-case failure recording. Expat and ElementTree parsing failures now become ValueError with their original causes preserved. A temporary stricter test expected ExpatError for an undefined entity; the actual parser raised ElementTree ParseError, and the final test verifies the normalized ValueError. The independent reviewer tests this API separately; the root's new registered receipt records their outcome and actual-source execution. Replacing a blanket DTD ban does not relax the original experiment's source authenticity, timestamp, quality or predictive gates.
