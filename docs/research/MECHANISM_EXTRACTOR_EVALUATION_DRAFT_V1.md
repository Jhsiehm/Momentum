# Mechanism extractor evaluation contract — draft v1

Date: November 8, 2026. **Design draft only: no extractor registered, trained, implemented or validated by this document. No quality text opened.** This specifies the minimum next implementation and evaluation package; it does not release E2, change an existing registration, or certify historical predictors.

The corrected 40 bills support rule development, regression examples and an annotation interface. They do **not** support a claim of a learned, generalizable legal-effect extractor. Build and test the source-preserving pipeline on design material first. Freeze it and the reference-review protocol before anyone opens the existing quality text for this study.

## Evidence bound to this draft

- Frozen semantics: [Bill mechanism and direction rubric v2](BILL_MECHANISM_RUBRIC_V2.md), SHA-256 `64de90cfa547866ff120964758e93ba26a1e84500ad0024022e3bc1a4e38085b`.
- Corrected design envelope: `data/research-runs/mechanism-corrections-20261108-v1/corrected-dataset.json`, seal `041ad00ca21d623b68771d5e81e9dab8d3965f5585232fe688c8804ecb2a5a57`. Original primary reviews, peer challenges, methods decisions, corrections and intermediate versions remain separate.
- Original mechanism registration: `0833e20efeaa40bc641662a7433ffee910d1927cd3574438cd99138b2cee32dc`. Corrected records retain `human_certified: false` and `historical_feature_eligible: false`.
- Existing pilot selection: `data/research-runs/bill-context-20261108-v1/registration.json`, seal `318eca5e2797e8d09c14f5d8efe66bbe69e556b05e3861c3ea3f9f3f52fd0c5a`. The evaluation population is exactly its ordered `selection` entries whose `partition == "quality"`: 50 bills, ten per Congress 113–117. Canonical repository `digest()` of that ordered list of selection objects is `3d295c88cae0a85ba93ebb3a49c2bcbcf6575b9ea4e2283cdcb59a37b7d504e3`. No replacement or convenient subsampling is permitted.
- The 40 corrected cases have zero bill-ID overlap with that quality partition. This is an identity check, not certification of the automated family graph. The ten earlier design bills used rubric v1 and cannot silently be pooled with v2 labels.

The [annotation guide](BILL_CONTEXT_ANNOTATION_GUIDE_V1.md), [experiment plan, E0](BILL_CONTEXT_EXPERIMENT_PLAN_V1.md), and [methods clarification](BILL_CONTEXT_METHODS_CLARIFICATION_V1.md) remain controlling for human review, quality exposure and historical eligibility. This draft retains their engineering thresholds rather than selecting thresholds from new results.

Exposure disclosure: inspecting the pilot registration's metadata also displayed its embedded `frozen_audit` block containing earlier aggregate historical outcome counts and a model-gain summary. A documentation search also returned historical aggregate status lines. Those aggregates did not determine this contract, thresholds, category definitions or coverage assessment. No individual outcome labels, quality bill text, model execution or new score was accessed. Do not describe this inspection as wholly outcome-blind. Quality-content custody remains intact within this task; project-wide custody must still be checked before execution.

## What the corrected labels cover

Counts below were recomputed from the sealed corrected dataset, not inferred from summaries. There are 480 bill/mechanism statuses: 205 present, 259 absent and 16 uncertain. There are 501 effect records; overlapping mechanism records can refer to the same operative clause and are not 501 independent examples. Fifteen additional unresolved-effect notes occur in eight bills. A supported effect can coexist with an unresolved additional effect.

| Mechanism | Present bills | Absent bills | Uncertain bills | Effect records |
| --- | ---: | ---: | ---: | ---: |
| create_programme | 21 | 17 | 2 | 28 |
| authorize | 26 | 14 | 0 | 97 |
| appropriate | 2 | 36 | 2 | 5 |
| tax | 4 | 35 | 1 | 7 |
| prohibit | 28 | 10 | 2 | 56 |
| require | 32 | 7 | 1 | 127 |
| amend | 25 | 15 | 0 | 34 |
| repeal | 4 | 36 | 0 | 6 |
| rename_designate | 8 | 31 | 1 | 18 |
| reporting | 24 | 15 | 1 | 54 |
| deadline | 22 | 15 | 3 | 60 |
| sunset | 9 | 28 | 3 | 9 |

Only seven mechanisms have at least 20 present **design** bills. This does not satisfy the separate minimum of 20 positive **quality** annotations. Appropriation has only two positive bills; tax and repeal four each. Directional support is thinner: `rename` occurs in one bill, `clarify` four, `preserve` six and `waive` seven. No claim about an unobserved mechanism/direction combination follows from observing that operation elsewhere.

The five largest effect sets contain 206 of 501 records: Nevada lands (64), electronic privacy (47), Maryland heritage area (36), Peace Corps (34), and Choose Respect (25). Only one bill has no effects at all, the nonbinding sense-of-Senate bill. The corpus is therefore useful for difficult examples but weak for estimating false-positive behavior across ordinary negative documents. A random effect-level train/test split would leak clauses, bill context and reviewer conventions.

Corrections expanded the original 463 effects to 501 and changed 21 bills. The separate correction layer records 50 finding references, including overlapping recommendations and two explicit self-audit discoveries. Those counts document revision, not error rates. Peer agreement and resolving quotations cannot certify semantic accuracy. Remaining boundaries include individual-project funding termination versus sunset, database naming, missing grant-criterion context, and unavailable appropriation or amendment text. A trainable system needs more independently reviewed, family-separated positive and negative examples, especially rare directions, before a credible learning assessment. No number of additional XML downloads alone supplies those labels.

## Frozen input and output contract

**Unit.** One complete introduced bill reading view, identified by bill ID, source version and content hash. A bill has twelve statuses and zero or more distinct operative effects. Bill IDs route records and are excluded from predictive inputs. Headings, findings, struck text, inserted text and operative prose remain distinguishable; titles do not themselves prove an effect.

**Input manifest.** Before quality execution, seal the ordered 50 identities and family IDs from the existing selection, source URL/package/version, raw-byte SHA-256, renderer version/hash, exact reading-view hash, XML-path-to-character-span map, source effective/publication date and its evidence, retrieval timestamp, intended day-180 cutoff, and unresolved provenance fields. Retrieval time is not historical public availability. Missing or mismatched identity, truncated views, source loss, and failed renders produce explicit failed-case records rather than substituted bills. Any new source acquisition follows a separately bounded source procedure; it does not occur under this draft.

**Output.** Retain the v2 record schema: `bill_id`, `source_view_hash`, `summary`, all twelve `mechanisms`, `uncertainties`, `unresolved_effects`, and `effects`. Each effect contains exactly `mechanism`, `operation`, `dimension`, `actor`, `target`, `conditions`, `quote`, `start`, `end`, `rationale`; enums remain those in the frozen registration. `start`/`end` are zero-based Python string character offsets into the exact view, inclusive/exclusive, not UTF-8 byte offsets. No whitespace-normalized text may replace the retained quote. Repeated occurrences require the selected contextual occurrence. Null actor/condition means not supplied, never inferred from historical knowledge.

A separate run sidecar records extractor code/config/lexicon hashes, dependencies, seeds if applicable, run times, per-case full-view coverage, parser failures, abstention reason codes, and any human interventions. It must identify automated output separately from later human corrections. The summary is source-only and excluded from mechanism/effect metrics; fabricated summary claims are still logged for safety review. Do not claim validated summaries from extraction scores.

**Abstention.** `uncertain` is not zero. Require a reason, with sidecar codes such as `missing_referenced_text`, `ambiguous_scope`, `rubric_boundary`, or `parse_or_coverage_failure`. If one effect is supported, keep mechanism present and place additional unknown effects in `unresolved_effects`. `operation: uncertain` is distinct from uncertain mechanism presence: the mechanism may be known while direction is unresolved. An absent status requires complete supplied-view coverage; failure to find a lexicon term is not proof of absence.

## Minimum implementation before quality access

The first candidate is a deterministic, research-only parser and fixed candidate-rule system with an explicit abstention path, consistent with the original E0 plan. Preserve the original XML and reading views. Candidate rules can locate language; they must not declare semantics from keywords alone. If human interpretation is required, call the product an assisted annotation workflow and report the unassisted machine output separately. Do not score human-corrected output as autonomous extraction.

Before freeze, implement a fail-closed runner and evaluator with the following acceptance fixtures on synthetic or exposed design text:

1. Full-document coverage and deterministic output, including long documents, section boundaries, Unicode offsets and repeated identical quotes.
2. Explicit contrasts: prohibition creation versus authority restriction; permission preserved by nonconstruction; authorization versus actual appropriation; complete repeal versus replacement; deadline waiver versus imposed deadline; effective date versus action deadline; new expiry versus removed expiry.
3. Conditional approvals, exceptions, list-wide scope, cross-reference failures and missing displaced-law context. A quote ending before the operative list must not justify an all-items target.
4. Distinct effects within one mechanism, including multiple reporting recipients or deadlines, and opposite operations within one bill. A single present flag cannot conceal omissions.
5. Deliberate validator counterexamples: exact quotes paired with wrong direction, wrong actor, omitted negation, findings-only language or a wrong repeated occurrence must pass source matching where appropriate but fail the independent semantic test.

These are implementation requirements, not tests executed by this draft. Freeze the complete code, renderer, lexicon, rules, abstention policy, matching instructions, exclusions, run budget and fixtures before opening any quality text or annotation. A machine-readable registration must bind their hashes and this exact population. An unbuilt implementation cannot be retrospectively declared frozen.

## Independent reference and scoring rules

Two qualified human reviewers independently read each full quality view under the frozen rubric without seeing candidate output, each other's annotations or outcome labels; a third adjudicates. Preserve both submissions, complete effect inventories, rationales and unresolved disputes. Agents can prepare packets but do not fill these human roles. Build and seal the reference before revealing candidate output to adjudicators. Source/family/historical-availability certification remains a separate gate. Unresolved rubric boundaries remain uncertain; do not rewrite the rubric after seeing quality cases.

Use a frozen normalization rule for reference and predicted effect units: one mechanism/operation/dimension/actor/target/condition relationship; split materially different targets, directions or conditions, but do not count duplicate paraphrases as new effects. Design examples must settle treatment of compound clauses before quality exposure. Do not redefine effect granularity to improve a quality score.

Run two separate checks:

- **Source integrity:** schema, identity/order, seals, enum validity, complete twelve-status coverage, and exact `text[start:end] == quote`. Report valid-reference rate over every emitted reference, including invalid outputs; no silent dropping. This check cannot establish correct legal meaning or completeness.
- **Semantic assessment:** assess each proposed effect against the sealed reference and complete source. A match requires the same mechanism, direction, dimension, substantive actor/target, conditions/exceptions and a supporting operative span. Textual overlap alone is insufficient. Different exact boundaries may still support the same effect if context is sufficient. A human matching decision must record the paired effect IDs and rationale; no LLM-as-judge substitutes for this reference assessment.

Make one-to-one effect assignments within each bill. The adjudicated compatibility graph supplies allowed matches; use maximum-cardinality bipartite matching with a deterministic lexical effect-ID tie break. Unmatched supported reference effects are false negatives; unmatched predicted effects and duplicate predictions are false positives. Do not match one broad prediction to several reference effects. Preserve compatibility decisions and assignments for replay. Report strict boundary equality separately as a locator diagnostic, never as semantic accuracy.

At bill/mechanism level, report the complete three-way table. On determinate reference statuses, compute positive precision `TP/(TP+FP)` and recall `TP/(TP+FN)`; predicted abstention on a positive is a false negative for end-to-end recall. Predicted abstention on a negative is not a false positive but remains in coverage and exact-status counts. Undefined denominators are reported as undefined. Reference-uncertain cells are excluded from binary denominators, counted explicitly and separately reviewed for unsupported certainty. Do not count reference uncertainty as either a correct negative or an extraction success.

For effects, report joint semantic precision/recall, each mechanism, each observed mechanism-operation pair, condition/exception errors, direction confusion, abstention rate and bill-level exact effect-set recovery. Break out partial-presence bills with unresolved additional effects. Report micro totals and equal-bill macro summaries so long bills cannot dominate the only headline. Stratify descriptively by Congress and bill length using cutpoints frozen on design data; retain small-cell counts. Include all 50 registered cases in availability/failure accounting, even if no semantic score is possible for some cases. No effect-row independence assumption or inflated effective sample size is permitted.

## Decision and release gates

Retain E0's engineering requirements: 100% retained references resolve, zero unresolved identity/future-availability errors, and at least 20 positive quality bills for a mechanism before assessing its precision of at least 95% and recall of at least 90%. Report counts and uncertainty intervals as descriptive uncertainty, not proof of population performance. A field with fewer than 20 positives remains uncertified even if its observed score is perfect. Do not enlarge the frozen sample after inspecting labels to rescue a sparse category.

For the detailed v2 representation, additionally propose applying the same 95%/90% thresholds to joint semantic effect precision/recall **within each sufficiently supported mechanism**, with at least 20 positive quality bills and 20 determinate reference effects. This additional proposal must be accepted in the execution registration before exposure; it is not an existing completed gate. Directional cells without adequate independent-bill support remain explicitly uncertified. Passing bill-presence metrics alone never certifies a multi-effect extractor. No zero-denominator category passes by default.

Any identity, source or historical-provenance blocker prevents feature eligibility irrespective of extraction scores. A semantic failure preserves the failed frozen run. Changes after quality feedback require a new extractor version and separately registered fresh quality sample; the original quality data become development material. Do not use retries, prompt changes, changed rule order or selectively rescored cases as independent evaluation. No modeling or forecasting follows automatically from a positive extraction result.

## Pretrained knowledge and historical use

The first candidate uses deterministic source-local processing with no pretrained generative model, embeddings, network lookup, outcome store, later bill version or external-law retrieval. Runtime access should be allowlisted to manifest-bound inputs and pinned code. Record attempted unauthorized reads and fail closed. Legislative citations remain text; absent prior-law content remains unknown.

This restriction reduces one contamination route; it does not make modern design decisions historically contemporaneous. The corrected design annotations are modern machine judgments and remain historically ineligible. A future neural/LLM extractor needs a separate registration specifying training provenance, model/corpus cutoff, exposure accounting and an untouched prospective extraction evaluation. Prompts saying “ignore future knowledge,” disabling browsing, or exact source quotes cannot demonstrate that a pretrained model lacks later knowledge. Likewise, successful present-day extraction does not establish that the source rendition was available at the historical checkpoint.

## Next concrete deliverables

1. Implement the design-only parser, candidate/abstention outputs and evaluator fixtures, preserving full text and the original provisional labels.
2. Complete the point-in-time source/family manifest and exposure ledger without using acquisition counts as labeled-training counts.
3. Resolve or explicitly retain open category boundaries on exposed design material; reannotate the earlier ten design cases under a separately documented v2 procedure before any pooling.
4. Secure the required reference reviewers and seal the execution contract, code and exact quality partition before access. Until then, quality execution and extractor certification remain blocked.

This draft creates no learned model, no quality evaluation, no historical feature certification and no forecast-improvement claim.
