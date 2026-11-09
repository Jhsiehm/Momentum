# Adversarial code audit: experiment validity and source boundaries

2026-11-08. Design-only code audit; provisional agent review, not human certification, legal validation, held-out accuracy, or historical feature eligibility. No quality texts, individual outcomes, network or model fitting were accessed. The earlier 24-item added-hit review was already exposed during filter development; it remains design motivation, not independent validation. Frozen v1/v2/v3 extractor, renderer and original context filter files were not edited.

## Reproduced defects and versioned dispositions

| ID | Layer | Synthetic reproduction | Observed frozen behavior | New disposition |
| --- | --- | --- | --- | --- |
| B01 | v3 expanded negative-subject regex | `Services are provided at no cost to the public and may be used freely.` | Retrieves `no cost to the public and may` as a prohibition locator. The negative phrase is not the subject of `may`. | v4 replaces this rule with a deliberately narrow noun-head and optional relative-clause pattern. Conjunction bridges and cost phrases are excluded. Unknown/coordinated subjects may be missed. |
| B02 | v3 whole-view expansion | Separate text or paragraph nodes containing `No applicant` and `may receive aid.` | The regex crosses inserted block newlines and returns one negative-modal hit. | v4 expansion runs within each complete leaf text node independently. No concatenation of separate blocks. |
| B03 | v3 whole-view expansion | A text node ending `provide`, followed by a paragraph containing `records` | Retrieves a reporting phrase spanning distinct structural nodes. | Same leaf-node boundary correction. Inline emphasis inside one text node remains contiguous. |
| B04 | original context filter | `Section 2 is not amended by striking “annual report” and inserting “monthly report”.` | Flags the quoted annual-report hit as struck despite the negated amendment instruction. | New filter v2 requires affirmative amendment provenance and rejects the negated context. The original decision is preserved as legacy data. |
| B05 | original context filter | `The manual describes amendments by striking “annual report” and inserting “monthly report”.` | A narrative example is flagged as struck operative language. | New filter v2 accepts a narrow affirmative local declaration or a standalone instruction with an affirmative structural ancestor lead-in. Narrative/ambiguous provenance retains the hit without approval. |
| B06 | frozen v1 proposal rules, inherited by v2/v3 | `No person may not submit a report.` | Suggests `prohibit/create` despite double negation. | v4 quarantines **all** inherited suggestions, including apparently sound ones; active proposals are empty. This is an intentional withholding policy, not a selectively measured accuracy gain. |
| B07 | frozen v1 proposal rules, inherited by v2/v3 | `There are appropriated no funds for the program.` | Suggests `appropriate/create` from the affirmative-looking surface prefix. | Same universal suggestion quarantine. Exact original suggestions remain available for review. |
| B08 | source schema | Duplicate character ranges assigned to unrelated indexed sibling text paths, each with a valid text hash | Frozen validation verifies hashes and ancestor containment but permits overlapping siblings. | v4 rejects overlapping unrelated source spans before returning output. Hash-valid text is not sufficient evidence of a valid hierarchy. |
| B09 | frozen v1 malformed-path traversal | Relative span path without `/`, such as `section[1]` | Ancestor traversal cannot shorten the string. | Previously fixed at the immutable v2 wrapper boundary by rejecting malformed paths; v4 inherits that guard. Frozen v1 remains unsafe as a direct arbitrary-input API. |

Reproductions use invented source strings and the existing boundary-aware renderer. The first three failures were demonstrated before writing v4. No 40-bill v4/filter-v2 run was used to select these changes.

## Exact scope of the new implementation

`scripts/mechanism_design_extractor_v4.py` starts from frozen v2 output, preserving its candidates and hit identities. It reconstructs expanded rules from the reviewed v3 manifest, changes only the negative-subject pattern, and searches those expansion rules in complete leaf `text` spans. A text node with represented child blocks is not a leaf. XML inline formatting omitted from block spans remains part of its containing text. Expansion-only header/metadata matches and cross-block matches no longer enter the active expansion layer. `excluded_v3_rule_matches` records the old rule, exact source range, reason, and whether the same identity remains as a legacy hit. A narrower match can have a different range from its old whole-view counterpart.

This does **not** repair the frozen v2 legacy hit vocabulary or its whole-view search. Legacy hits may still cross blocks, match negated or nonoperative text, or identify the wrong mechanism. The output explicitly states that limitation. All twelve assessments remain abstentions. Counts reflect current candidates, not legal status. Original surface suggestions are moved verbatim into `legacy_proposals[].proposal` with a quarantine reason, while `proposals` is empty.

`scripts/mechanism_context_filter_v2.py` is separate triage. It preserves original filter status, reasons and evidence per hit. Deletion reasons survive only when a source text node supplies a narrow affirmative amendment declaration, or a standalone `by striking` instruction inherits such a declaration through actual ancestor/direct-child ordering. Negation, narrative/proposal cues, insertion directives and quoted-block ancestry prevent unsafe inheritance. Failure to establish that provenance removes only the deletion reasons; heading/location/findings flags may independently remain. `retain` still means unflagged, never approved.

## Renderer and structural semantics

The renderer faithfully keeps text and inline tails and inserts explicit newlines around its enumerated block tags. These are reading-view character offsets, not raw XML byte offsets. The enum does not represent every XML construct, including table cells. Consequently a table can lose column distinctions or concatenate cell text in the reading view. A locator can also span distinct blocks if it is run on the entire flattened view. Complete-view scanning therefore establishes processing coverage, not legal-context sufficiency.

v4 deliberately does not revise the renderer or create a new reading-view identity. Table/other text outside complete leaf text nodes remains available in the full source and legacy locators, but is not covered by the new expansion layer. This is a recall tradeoff, not evidence that those regions contain no legal effects. Structural ancestry identifies where text appears; it does not establish which clause legally governs another, whether quoted language is enacted, or whether an external statutory cross-reference supplies missing conditions.

## Validation and evidence

Owner tests: `tests/test_mechanism_design_extractor_v4.py` and `tests/test_mechanism_context_filter_v2.py`. The initial combined execution ran 13 tests successfully, covering the reproduced defects, inline-vs-block boundaries, positive subject variants, exact source evidence, unchanged input objects, repeat determinism, original hit preservation, universal proposal quarantine, overlapping-sibling rejection, positive/negated/narrative amendment provenance, and old-vs-replacement operands. Independent agent A separately exercised seven v4 synthetic probes before the first design run. These checks establish the asserted code behavior on fixtures, not legal precision/recall.

A later bounded runner must bind source views, code hashes, rule manifests and reference versions; report legacy and expanded hit changes separately; inspect all removals and reference-overlap losses; and leave semantic accuracy unset. Changes in overlap can arise from source-boundary or quote-boundary changes and must not be described as accuracy improvement. The known design review is not an independent control group.

## Residual risk matrix

| Risk | Status after these versions | Consequence and required interpretation |
| --- | --- | --- |
| Cross-block expanded regex matches | Corrected for new expansion hits | Leaf boundaries are enforced; no claim about retained legacy hits. |
| `no cost ... and may` negative-subject failure | Corrected for the reproduced family | The narrow subject vocabulary sacrifices recall and is not a legal grammar. |
| Negated/narrative striking false flags | Corrected for reproduced forms | Complex amendment syntax can still be missed; absence of a flag is not approval. |
| Legacy proposal semantic overclaims | Quarantined universally | Zero active proposals is policy withholding, not measured semantic perfection. |
| Legacy whole-view locators and semantic false positives | Retained, explicitly unresolved | May remain in active candidate review inventory; must not be counted as accepted effects. |
| Headings/findings/location flags | Triage only | Even those contexts can contain material relevant to interpretation; no automatic deletion or legal truth label. |
| Descriptive project content, conditions, nonconstruction, permissions and duties | Unresolved beyond narrow checks | No automatic legal interpretation or promotion. |
| Table cell boundaries and unrepresented XML nodes | Renderer unchanged | New expansion may omit them; full-view access remains necessary. |
| Structurally valid but falsely supplied source hierarchy | Not authenticated by pure functions | Sealed source/view binding and provenance audit remain runner responsibilities. |
| Referenced prior law and unknown net direction | Unresolved | Never infer unseen rates, powers, deadlines or outcomes. |
| Design reuse and pretrained knowledge | Not eliminated | Agent fixtures and reviews are not independent validation or historically eligible features. |
| Quality population/generalization | Untested | No quality exposure or readiness/accuracy claim follows from design fixtures. |

No commits or external publication were performed by this subagent. Root owns the repository integration and final immutable-run authorization.
