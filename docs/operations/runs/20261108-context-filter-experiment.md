# Context-triage experiment on expanded bill locators

Date: 2026-11-08. Ran a separately versioned, source-based context classifier on all forty design bills. The experiment asks whether narrow context flags can identify misleading occurrences while preserving useful source-location coverage. It does not train a prediction model or certify legal effects.

## Result

| Diagnostic | Result |
| --- | ---: |
| Raw hits, all preserved | 2,727 |
| Flagged for additional context review | 322 |
| Unflagged (`retain`) | 2,405 |
| Raw reference-quotation intersections | 449/501 |
| Intersections using only unflagged hits | 449/501 |
| Lost reference-quotation intersections | 0 |

Flags mark review needs; they do not delete any hit or prove it legally irrelevant. The retained-only counts are a diagnostic view, not replacement annotations. All original 480 mechanism abstentions, five unvalidated proposals, raw candidates and corrected references remain unchanged. No accepted labels are created.

The seven frozen rule families cover structural headings, official titles, locations outside represented legislative bodies, findings/sense contexts, explicitly struck inline quoted text, bounded replacement operands and struck quoted blocks. They use exact local offsets and source hierarchy. A striking instruction elsewhere in a section does not flag unrelated replacement language. Missing structural boundaries, ambiguous deletion operands and descriptive project content remain unflagged.

Observed flag reasons are nonexclusive: heading 206, outside legislative body 88, official title 66, findings/sense context 19 and explicit replacement operand 9. These reason counts must not be summed as distinct hits. Inline-quote and quoted-block rules had synthetic test coverage but no flagged occurrences in this particular design run.

## Previously exposed diagnostic cases

The earlier 24-hit review informed implementation and cannot serve as held-out validation. On those known cases, the classifier:

- Retains all 20 previously supported locators.
- Flags three of four misleading contexts: struck wording, a heading and a purpose statement.
- Retains the descriptive optional-project passage, which the narrow rules do not resolve.

That is a useful engineering check, not a three-of-four semantic recall estimate. Nor does unchanged 449/501 overlap show that all 322 flags are correct: another hit may preserve a quotation intersection, and deleted text may itself identify the target of an operative removal effect.

## Frozen experiment and sampling

The rule manifest, code, synthetic fixtures, input bindings and sampling procedure were sealed before the forty-bill run. No post-result changes were made. The classifier preserves input data and emits a separate decision for every hit, with source-linked reasons. The runner validates complete identity coverage, bill/view/text bindings, selected hit quotes, candidate IDs, exact evidence offsets and explicit false certification flags.

A fresh occurrence sample was fixed as up to twelve flagged and twelve retained **added** hits, ranked by SHA-256 of compact JSON `[bill_id, mechanism, start, end]`, excluding all prior 24 sampled occurrences. Only one new flagged addition was eligible; it was selected and the eleven-item shortfall was retained. Twelve of 48 eligible retained additions were selected. No substitution from old hits or hand-picked cases filled the gap. These thirteen occurrences still belong to previously used design bills and are not a new held-out population.

## Fresh occurrence source review

A separate agent reviewed all thirteen selected occurrences against twelve distinct full candidate contexts and their bound source views. Eleven retained hits were supported as useful locators. Two occurrences were misleading as effect evidence: the single flagged annual-report heading, and one retained `116-s1076` hit at offsets `3850:3901`.

That retained phrase reads “no cost to the Government wherever feasible and may.” The expanded negative-subject rule incorrectly connects “no,” which modifies cost, with “may” from a separate permission clause. An adjacent genuine restriction does not establish that this particular match is meaningful. This residual error is preserved, not repaired after the experiment. It shows that punctuation bounds and the present context flags do not fully resolve clause attachment.

The observed cross-tab is one flagged/misleading, eleven retained/supported and one retained/misleading. The strata are unequal and selected only from remaining added hits; these counts are not generalizable precision or recall and do not validate the other flagged hits. Even supported locators are not accepted legal effects.

Source-review receipt: `6dc9e3715d52e86c1f34475a8ae578947a2be44ea4ef998b1770652d92e6a2bc`. Root independently verified complete sample coverage, view hashes, source offsets and the cross-tab; integrity receipt: `b9246ec3e5bf2a52d5617bdd9818612da9c7e855c047ba326e68e0432215b87f`. No filter or locator rules changed in response.

## Validation and receipts

Eighty-nine focused tests passed, including independently authored cases placing identical wording in headings versus body text and in struck versus replacement clauses. Tests also cover source hierarchy, ambiguous deletion boundaries, exact Unicode spans, missing boundaries, full raw-hit preservation, no mutation, deterministic concurrent execution, sample exclusion/shortfalls and refusal of mismatched evidence or certification claims. No full-suite result is claimed.

Normal and optimized execution reproduced result `9079f2fba97f912c0950cd8070e728539d283a8f94c86d0d0a2328f39243810b`. A separate methods agent recomputed every decision mapping, all raw/unflagged overlaps, prior-case diagnostics, exact sample selection and binding checks; then replayed the actual runner successfully. Methods receipt: `bff8db78d6d65f602421988a4b4a953e0a6b46751f583ad7dea040567ab1d083`.

Registration: `16dabe678d177a176fb779934839642f95f301c8e98a473015bffce22a632335`. Fresh sample: `648423e48350f3864ee9efc49800780ab96bb2d0b6d173f81813ea2bfffd4123`. Expanded baseline and corrected v3 reference hashes remain those in the [previous experiment](20261108-expanded-candidate-rules.md). Runtime directory: `data/research-runs/mechanism-context-filter-20261108/`.

```sh
python3 -m scripts.run_mechanism_context_filter --output data/research-runs/mechanism-context-filter-20261108
python3 -O -m scripts.run_mechanism_context_filter --output data/research-runs/mechanism-context-filter-20261108
python3 -m unittest tests.test_mechanism_context_filter tests.test_mechanism_context_filter_contrasts tests.test_mechanism_filter_runner
```

Preservation replay verified all 143 inventoried prior files and an identical frozen-model audit. Receipt: `1ec3c8c962706ade955551453b7483f39057566ece423cc7ea0ebb04fee0b064`. No protected quality text was parsed; no sources acquired, outcomes scored, prediction models fitted, schedules changed or releases promoted. The shared research lease was released.

## Interpretation

This supports a separate context-warning layer for design review, with unchanged locator coverage. It does not justify automatically discarding flagged text, accepting retained hits as legal effects, or claiming a predictive improvement. Descriptive roles, governing conditions and prior-law relationships remain unresolved by these rules. The next semantic experiment must evaluate explicit effect interpretations against separately reviewed compatibility judgments, while keeping historical source and quality-reference gates intact.

## Detailed audit appendix

This appendix was added from the existing sealed records after the user requested complete experiment details. It does not change the experiment, rules or results. Code and results were published in commit `60d67a5`. Exact runtime duration and cost were not captured as experiment metrics and are not estimated here.

### Every bill

Offsets in review records use zero-based Python character indices in the bound source reading view; end offsets are exclusive. Bills have distinct Congress/chamber/number identities.

| Bill | Raw hits | Flagged | Retained | Reference effects | Raw intersections | Retained intersections |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 113-hr1257 | 16 | 6 | 10 | 2 | 1 | 1 |
| 113-hr128 | 57 | 2 | 55 | 12 | 10 | 10 |
| 113-hr1979 | 28 | 7 | 21 | 8 | 5 | 5 |
| 113-hr4429 | 24 | 9 | 15 | 6 | 5 | 5 |
| 113-s2088 | 39 | 4 | 35 | 12 | 11 | 11 |
| 113-s439 | 61 | 13 | 48 | 14 | 14 | 14 |
| 113-s5 | 1 | 1 | 0 | 0 | 0 | 0 |
| 113-s848 | 8 | 1 | 7 | 5 | 3 | 3 |
| 114-hr2575 | 7 | 3 | 4 | 1 | 1 | 1 |
| 114-hr3803 | 113 | 13 | 100 | 8 | 6 | 6 |
| 114-hr5053 | 36 | 7 | 29 | 6 | 4 | 4 |
| 114-s1259 | 67 | 13 | 54 | 20 | 20 | 20 |
| 114-s2388 | 42 | 3 | 39 | 15 | 13 | 13 |
| 114-s2769 | 16 | 4 | 12 | 7 | 7 | 7 |
| 114-s2940 | 24 | 8 | 16 | 3 | 3 | 3 |
| 114-s375 | 31 | 7 | 24 | 4 | 2 | 2 |
| 115-hr1714 | 5 | 1 | 4 | 1 | 1 | 1 |
| 115-hr2259 | 193 | 12 | 181 | 34 | 32 | 32 |
| 115-hr5527 | 43 | 18 | 25 | 11 | 10 | 10 |
| 115-hr5589 | 24 | 3 | 21 | 9 | 9 | 9 |
| 115-s1372 | 22 | 3 | 19 | 9 | 9 | 9 |
| 115-s1657 | 452 | 28 | 424 | 47 | 43 | 43 |
| 115-s1809 | 93 | 16 | 77 | 21 | 19 | 19 |
| 115-s284 | 50 | 3 | 47 | 10 | 8 | 8 |
| 116-hr2943 | 2 | 1 | 1 | 1 | 1 | 1 |
| 116-hr3024 | 17 | 1 | 16 | 3 | 2 | 2 |
| 116-hr3777 | 184 | 23 | 161 | 16 | 15 | 15 |
| 116-hr7433 | 21 | 2 | 19 | 6 | 4 | 4 |
| 116-hr846 | 73 | 11 | 62 | 15 | 14 | 14 |
| 116-s1076 | 89 | 16 | 73 | 25 | 23 | 23 |
| 116-s2089 | 13 | 2 | 11 | 6 | 5 | 5 |
| 116-s856 | 39 | 3 | 36 | 8 | 8 | 8 |
| 117-hr1597 | 437 | 20 | 417 | 64 | 57 | 57 |
| 117-hr1662 | 46 | 11 | 35 | 12 | 12 | 12 |
| 117-hr2448 | 21 | 5 | 16 | 3 | 3 | 3 |
| 117-hr5229 | 146 | 21 | 125 | 24 | 24 | 24 |
| 117-hr6835 | 12 | 1 | 11 | 4 | 3 | 3 |
| 117-s1230 | 44 | 1 | 43 | 9 | 8 | 8 |
| 117-s4377 | 13 | 5 | 8 | 4 | 4 | 4 |
| 117-s825 | 118 | 14 | 104 | 36 | 30 | 30 |
| **Total** | **2727** | **322** | **2405** | **501** | **449** | **449** |

### Every mechanism

| Mechanism | Reference effects | Raw intersections | Unflagged intersections | Lost |
| --- | ---: | ---: | ---: | ---: |
| amend | 34 | 33 | 33 | 0 |
| appropriate | 5 | 4 | 4 | 0 |
| authorize | 97 | 89 | 89 | 0 |
| create_programme | 28 | 15 | 15 | 0 |
| deadline | 60 | 58 | 58 | 0 |
| prohibit | 56 | 49 | 49 | 0 |
| rename_designate | 18 | 13 | 13 | 0 |
| repeal | 6 | 6 | 6 | 0 |
| reporting | 54 | 50 | 50 | 0 |
| require | 127 | 123 | 123 | 0 |
| sunset | 9 | 6 | 6 | 0 |
| tax | 7 | 3 | 3 | 0 |

### Every freshly reviewed occurrence

These are provisional source-review judgments, not certified semantic labels. Full source quotations and offsets are preserved in `source-review.json`.

- **114-s1259 · deadline · [6773, 6786)** — filter `flagged`; review `misleading_context`. This selected annual-report occurrence is the section heading. The following operative subsection separately requires annual submission, but that does not convert the heading occurrence into an action deadline. It is misleading if promoted to an additional effect; the full context remains useful for review.
- **114-s2769 · reporting · [1848, 1870)** — filter `retain`; review `supported_locator`. The Administrator shall prescribe regulations requiring each air carrier to display passenger-space information on its website. The parent regulatory mandate governs the list item. This supports a reporting locator for public disclosure, without certifying the detailed effect or timing.
- **117-hr1597 · prohibit · [23174, 23197)** — filter `retain`; review `supported_locator`. The clause limits motorized vehicle use in special management areas to designated roads and routes, except for emergency response or administrative purposes. The full management-plan and savings context qualifies the restriction. This is a supported scoped prohibition locator, not an absolute vehicle ban.
- **113-s2088 · reporting · [2629, 2659)** — filter `retain`; review `supported_locator`. The newly added paragraph directs the Energy Secretary to issue a detailed environmental-impact statement about export orders. Its insertion context and affirmative shall distinguish it from language struck elsewhere in the same section. This supports a communication locator; no unseen NEPA requirements are inferred.
- **117-hr6835 · prohibit · [1707, 1730)** — filter `retain`; review `supported_locator`. The operative clause permits subsequent extension of normal trade relations only under the specified historical statutory regime. It is a supported limitation locator even though the exact external requirements and their net effects are unavailable; no reconstruction of those requirements is attempted.
- **115-hr2259 · authorize · [11022, 11043)** — filter `retain`; review `supported_locator`. The replacement subsection gives an applicant the option to decline an invitation without retaliation and with priority for another country, after receipt of the specified risk information. Shall have the option allocates discretion rather than imposing a duty to decline. The unrelated textual deletion elsewhere does not negate this clause.
- **117-s825 · deadline · [4732, 4745)** — filter `retain`; review `supported_locator`. The governing Local Coordinating Entity shall and the for-any-year-funds-received condition apply to the annual-report list item. This is a supported recurring-action deadline locator. No fixed calendar day is supplied, and reporting content and funding conditions remain attached.
- **116-s1076 · prohibit · [3850, 3901)** — filter `retain`; review `misleading_context`. The selected no cost to the Government wherever feasible and may fragment is not a no-subject-may prohibition: no modifies cost in the donated-services duty, while may begins the separate may-only procurement clause. Although that adjacent clause supplies a real restriction, it does not validate this accidental negative-subject match as a separate operative locator. The narrow context filter retains this misleading lexical match.
- **116-s1076 · deadline · [9357, 9382)** — filter `retain`; review `supported_locator`. The Director shall submit a report to Congress on an annual basis, governing the subsequent content list. This supports an annual submission-timing locator, not a certification of the full effect annotation or a specific calendar due date.
- **114-s1259 · prohibit · [3295, 3320)** — filter `retain`; review `supported_locator`. The maximum grant amount is expressly limited to $5,000,000 per fiscal year for the specified recipient programme. This ceiling constrains awards and supports a prohibition locator; it does not itself appropriate funds.
- **117-hr1597 · prohibit · [60042, 60065)** — filter `retain`; review `supported_locator`. The off-highway-area clause permits motorized use only on designated roads and trails, except for administration or emergency response. The separate interim-management and road-closing provisions and utility savings clauses remain relevant. This is a supported scoped limitation locator, not an unconditional ban.
- **117-hr1662 · reporting · [1340, 1428)** — filter `retain`; review `supported_locator`. The newly added operative subsection directs the Postmaster General to provide address records to each chief State election official on the stated recurring schedule. This occurrence is in the body duty, unlike the prior reviewed purpose statement. It supports an information-transfer locator.
- **116-hr7433 · authorize · [2048, 2087)** — filter `retain`; review `supported_locator`. The inserted deferment provision allows eligibility to be established with listed documentation or other documentation the Secretary determines appropriate. This expressly allocates scoped discretion over acceptable evidence, not unrestricted authority over the entire loan programme.

### Full records and reproduction

The following files remain local, ignored runtime artifacts rather than committed research data. Paths are relative to the repository root. Each per-bill file contains every hit decision, exact quote, reasons and supporting source evidence; `result.json` binds their hashes.

- `data/research-runs/mechanism-context-filter-20261108/registration.json`: complete frozen rule manifest, all input/code hashes, population and sampling procedure.
- `data/research-runs/mechanism-context-filter-20261108/result.json`: all aggregate/per-mechanism results, output hashes, sample quotas and prior-review diagnostic.
- `data/research-runs/mechanism-context-filter-20261108/<bill-id>.json`: all 2,727 per-hit decisions across the forty bill files, including all 322 flags.
- `data/research-runs/mechanism-context-filter-20261108/review-sample.json`: exact thirteen selected fresh occurrences and quota shortages.
- `data/research-runs/mechanism-context-filter-20261108/source-review.json`: all thirteen rationales and full source evidence.
- `data/research-runs/mechanism-context-filter-20261108/source-review-integrity.json`: exact source and coverage verification.
- `data/research-runs/mechanism-context-filter-20261108/methods-replay.json`: independent arithmetic/provenance/sample replay receipt.
- `scripts/mechanism_context_filter.py`: exact seven flag families and boundary handling.
- `scripts/run_mechanism_context_filter.py`: registration, checks, measurement and deterministic sampling.

The reproduction commands above replay the existing sealed result; they do not fit or evaluate a predictive model.
