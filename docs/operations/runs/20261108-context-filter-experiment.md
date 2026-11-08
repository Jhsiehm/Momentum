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
