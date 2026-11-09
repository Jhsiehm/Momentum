# Independent readiness review: XML coverage and provenance preflight

Status: independent implementation and bounded-result review complete; no certified semantic or historical results.

Scope is the fixed, already exposed forty design bills and synthetic fixtures only. This reviewer has not opened protected quality text or individual outcomes. Agent review is an internal independent implementation check, not qualified human source or reference certification.

## Boundaries identified before implementation review

The frozen `block-boundaries-v2` renderer preserves element text and child tails and inserts newlines at its declared block tags. It strips element namespace qualifiers and omits attributes, comments and processing instructions from its rendered text. Its block vocabulary does not explicitly separate table rows/cells, formulas or footnotes. Thus complete traversal of the rendered string does not establish complete source interpretation or safe phrase continuity across every legal structure.

Raw-byte hashes, parsed logical text, rendered text and structural spans are distinct identities. Character references and XML line-ending normalization can change the relationship between byte offsets and rendered character offsets; neither should be silently substituted for the other. Namespace collisions and empty nodes with meaningful attributes need explicit accounting. A reconciled character inventory can demonstrate no unexpected character omissions in that inventory, but not complete legal meaning, interpretation of tables or accessibility of linked figures.

Bill identity includes Congress, chamber/type, number and rendition. An exact current package name and raw hash do not establish that the bytes were available by a historical cutoff. Schedules require announcement vintage and effective-event distinction; a future scheduled event announced earlier may be usable, whereas later cancellations, revisions and actual occurrence cannot be backdated. Missing schedules remain unknown. Self-asserted timestamps do not independently authenticate historical custody.

## Executed review

The executed review and the preserved negative v1 result are documented below.

### Pre-run implementation review and challenges

Read the new `bill_render_coverage_audit`, `bill_provenance_preflight` and root runner. Twelve independently authored test methods pass in normal and optimized Python. They test each identity component, raw versus rendered byte hashes, microsecond cutoff exclusion, equivalent timezones, ambiguous same-time schedule revisions, future cancellations, exact elapsed 180 days, actual cross-cell concatenation in the frozen renderer, inline/tail preservation, Unicode character offsets, exact partition of rendered text, colliding namespace-local tags, attribute-only graphics and UTF-16 DTD rejection.

No failing implementation counterexample was found in these fixtures. The reviewer requested explicit propagation of false historical-certification flags to schedule selections and direct manifest-byte binding by the runner; neither is evidence of actual historical validity. The comparator trusts an expected version token supplied by the caller and is not an official version-code vocabulary validator. `view_sha256` in synthetic byte checks hashes rendered bytes, not the sealed view envelope; consumers must not confuse these identities.

The XML audit independently reconstructs traversal events and offsets but deliberately shares the frozen renderer's `BLOCKS` vocabulary. It is an independent accounting check, not independent validation of legal structural semantics. Comments, processing instructions, attribute semantics and externally referenced resources remain outside rendered semantic content. Table warnings remain present even where a whitespace separator prevents literal character concatenation: whitespace is not a verified legal boundary.

The runner authenticates population and source hashes before registration and parsing. Missing or corrupt authenticated inputs abort that preflight, while per-bill parse/accounting failures after registration are retained without replacement. This is not an acquisition failure ledger or proof that the source pool is complete.

### Frozen v1 result and separately versioned correction

Independent recount authenticated all forty sealed per-bill outputs against result `b28fd1e13ec0cc21d690402953a188722d952c7b3685707069e470b6ba9505ec`: all forty failed with `DTD declarations forbidden in coverage audit`; the recorded failure list also contains forty. All twenty-five synthetic provenance cases passed. This is a real parser-compatibility failure, not evidence of absent source content. The original synthetic coverage fixtures omitted the external declaration present in these sources.

A separate v2 permits declaration identifiers while never loading external DTDs and continues to reject internal subsets, entity definitions and unresolved entity references. The reviewer added seven independent methods, including a frozen/new runner wiring identity check. Their first execution exposed one actual defect: malformed XML raised ExpatError outside the runner's retained-failure boundary. This failure was reported before v2 registration for normalization to ValueError. The other six methods passed. No v1 code or results were modified.

### Frozen v2 independent results

After normalizing malformed-XML exceptions, all seven v2 independent methods passed in normal and optimized Python. Frozen result `9c82fc612cef6d480d6afcaa7c18e41431c9fbc806f885acd1aadff0b178b9c6` contains forty successful bills and no failures. The reviewer independently authenticated registered code/input bytes and all output seals; counted all 8,331 nodes directly from XML; reconciled raw parser text lengths and every segment/separator as an exact, gap-free rendered-text partition; and recomputed all aggregate counts, warning bill counts and unrepresented-tag counts. All twenty-five synthetic provenance outcomes pass. Normal and optimized independent recomputations produce the same review seal: `20faa12f802b458d963481f65219b58f4401b0ddc9a555a36ac05c18d9ec803e`.

Exact totals: 8,331 XML nodes; 6,667 represented spans; 1,664 unrepresented nodes; 9,299 text/tail segments; 324,489 parser-visible characters plus 13,334 inserted newlines equals 337,823 rendered characters. All forty bills warn about unresolved external DTD identifiers, attributes not rendered and namespace identity collapse. One bill has 35 table-related nodes, ten rows, twenty cells and ten within-row zero-whitespace cell joins: **114-HR3803**. The reviewer compared all ten paired cells directly against raw XML and view offsets, with no sampling shortfall. This table describes a proposed statutory budget timetable, not observed actual legislative-calendar events.

| Row | Left cell | Right cell | Join offset |
| --- | --- | --- | ---: |
| 1 | On or before: | Action to be completed: | 1779 |
| 2 | First Monday in February | President submits budget recommendations. | 1835 |
| 3 | February 15 | Congressional Budget Office submits report to Budget Committees. | 1896 |
| 4 | Not later than 6 weeks after budget submission | Committees submit views and estimates to Budget Committees. | 2015 |
| 5 | April 1 | Budget Committees report joint resolution on the budget. | 2090 |
| 6 | April 15 | Congress completes action on joint resolution on the budget. | 2163 |
| 7 | May 15 | Appropriation bills may be considered in the House of Representatives. | 2238 |
| 8 | June 10 | House Appropriations Committee reports last appropriation bill. | 2324 |
| 9 | June 30 | House completes action on appropriation bills. | 2403 |
| 10 | October 1 | Fiscal year begins. | 2467 |

A supplemental inspection of all nine between-row boundaries found a newline and eight tabs at each boundary: no additional literal cross-row concatenation, although row topology remains unrepresented. Supplemental seal: `2a0ad049eceb7ade8b95da67bda8b99d0025661972db7ed5148973a818d754dd`.

Zero recognized nontext-tag matches must not be stated as absence of mathematical structure. The unrepresented-node inventory contains three `fraction` nodes outside the narrow nontext-risk vocabulary: two in **113-HR128**, rendered as `41/2 hours` with an adjacent whole number, and one in **117-HR1597**, rendered as `NW1/4`. These retain their characters but expose formatting/interpretation risk. No semantic error rate was measured. Supplemental seal: `b36cce4788f2a3daaa982045e85f3aa5d31e50e97793f064714b4ecc9ecaeb29`.

The independent recomputation script and all three sealed supplemental reviews are preserved under ignored `data/research-runs/readiness-coverage-v2-20261108/`. No protected quality text or individual outcomes were accessed, no model was fit, and no source, reference or historical certification follows from these checks. Table-aware rendering and fraction-aware representation require separately registered changes; the frozen view remains untouched.
