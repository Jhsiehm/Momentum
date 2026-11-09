# Supplemental XML renderer coverage audit implementation review

Date: 2026-11-08. Reviewer: implementation agent; this is an AI engineering review, not human source certification.

## Scope and interface

New module `scripts/bill_render_coverage_audit.py` exposes `audit(raw, bill_id, supplied_view)`. It does not alter the frozen v2 renderer or any prior view. The caller authenticates selected source records and restricts execution to registered design cases before calling it. If a supplied view contains a source binding, byte count and SHA-256 must match the supplied raw bytes. Text, spans, renderer identity and bill identity must match a fresh rendering.

The supplemental traversal inventories each parsed XML element with its qualified tag, local tag, indexed path, parent, attributes and rendered start/end. A separate event stream maps every parser-visible element-text and child-tail segment to exact Unicode offsets, alongside explicit inserted newline segments. Stream reconstruction and represented span boundaries must equal the frozen renderer. The audit shares the renderer's explicit `BLOCKS` configuration: it independently checks segment traversal/accounting but does not independently validate that the block list is semantically adequate.

The result includes raw byte SHA-256, byte length, rendered-text SHA-256, counts, complete node and segment inventories, unrepresented tag counts, and warnings. All validation uses explicit `require` rather than optimization-removable assertions. DTD declarations are rejected using the XML parser callback, including UTF-16 declarations; external declarations are not treated as safe because their content was not fetched.

## Structural limitations made visible

- Table/row/cell topology remains in the XML inventory but not in the frozen renderer's spans. Adjacent cells can concatenate into a single lexical phrase. Cell boundaries with no whitespace are explicitly listed; even whitespace does not establish semantic separation.
- Attributes are inventoried without semantic interpretation. IDs, references, table column spans, units, image links or amendment instructions may carry information absent from rendered text.
- Figure/image/formula/math elements trigger review warnings. Their text nodes alone do not establish visual or mathematical meaning, nor resolve external resources.
- Namespace identities remain in the inventory. Frozen renderer paths collapse namespace identity, although local-name sibling counting keeps paths distinct.
- Unrepresented generic wrapper tags remain in the inventory. Preservation of their text does not prove preservation of scope or semantic relationships.
- The counters apply after XML parser normalization and character-reference decoding. They are not XML byte offsets. Comments and processing instructions are not rendered semantic content. Byte hashes authenticate exact provided input bytes, not source publication date or legal authenticity.

`source_document_completeness`, `semantic_structure_complete`, `historical_feature_eligible` and `human_certified` are always false. Passing accounting cannot open quality, historical or prediction gates.

## Synthetic checks performed

Nine test methods cover adjacent cells across two rows, nested unrepresented wrappers, inline tails, Unicode and numeric/predefined character references, default namespaces, distinct namespaces sharing local names, empty cells/text, attributes and nontext elements, DTD/entity declarations in UTF-8 and UTF-16, forged text/spans/renderer/bill identity, exact source-byte bindings including boolean-length rejection, and whitespace cell boundaries.

`python3 -m unittest tests.test_bill_render_coverage_audit` passed all nine methods. No actual forty-bill audit was run by this implementation agent before root registration. Subsequent independent challenges and registered execution are recorded separately by their reviewers and the execution receipt.
