# Bill-context methods clarification v1

November 8, 2026. Status: pre-execution clarification and unresolved-methods register. This document accompanies [the original experiment plan](BILL_CONTEXT_EXPERIMENT_PLAN_V1.md) and [the independent agent methods audit](reviews/20261108-context-methods-audit.md). It does not modify that plan, its hash-bound execution registration, the paper protocol, source evidence or frozen model artifacts. No predictions, fits or new performance comparisons are authorized by this document.

## Comparable populations before E6 selection

The original plan permits feature-specific matched subsets for E2–E5, but its capped E6 block selection ranks their relative gains. Different subsets can have different baseline difficulty and different effect modifiers. Within-block matching does not make cross-block gains comparable.

For any later E6 registration, qualification and cross-block ranking must use an identical, predeclared population within each evaluation fold, with identical eligible core/calibration populations where the compared procedures require them. Freeze the common population before viewing the comparisons used for that selection. Retain all exclusions, missingness and blocked-fold decisions. The shared population must independently pass source, family, temporal, class and positive-family gates. A common population selected after feature-specific scores have been inspected is itself an exposed development choice and cannot be characterized as independent confirmation.

The existing feature-specific results, if later produced, may retain their own conditional interpretation. They must not be ranked as interchangeable inputs to capped E6 selection. Recomputing only the final combination and anchor on a common population does not repair earlier incomparable screening.

Until a separate sealed registration specifies the common-population comparisons, block identities, computational allocation and decision rule, E6 selection is blocked. Such registration must respect the original 75-fit ceiling unless a separately documented prospective amendment explicitly changes the budget before the affected scores are viewed. Unused fits are not automatic permission for new comparisons. No calculations have been added to the current execution or performed under this clarification.

## Positive-family scope remains unresolved

The existing requirement is at least 200 reviewed positive training families and at least 100 reviewed positive development families for a new selection study, at its applicable registered population level. Neither the preparation run nor this agent audit establishes reviewed counts or signs off a different scope.

The reproduced raw counts are:

| Fold | Training positives, core plus calibration | Evaluation positives |
| --- | ---: | ---: |
| 115 | 116 | 75 |
| 116 | 158 | 48 |
| 117 | 227 | 59 |

These are unreviewed recorded outcomes under a provisional family graph. If the floors apply per fold, training folds 115 and 116 and all three development evaluation folds fail before review. Fold 117's raw training count does not establish 200 accepted reviewed positive families. If a study-level interpretation is appropriate, a methods reviewer must first name the exact training and development populations and count distinct accepted global families, without summing repeated fold appearances. A population definition chosen because it passes a desired threshold is not an adequate preregistered gate. The modeling stages remain blocked pending that resolution and actual evidence review.

## Agent review and future work

Independent agent reviews can identify implementation errors, reproduce deterministic results and retain disagreements. They do not constitute the two qualified human annotations, separate adjudication, historical-source certification or protected-outcome custody required by the unchanged protocols. Agent agreement is neither outcome truth nor a new independent temporal sample.

Permitted immediate work remains evidence preparation, machine-only design annotations, cross-audits, software fixtures, robust verifiers and prospective registration drafts. Human approval records remain pending, quality content remains unopened for extraction until design freeze, and E1–E9 are not released by this clarification. Any later change to those scientific requirements must be explicit, versioned and accurately described rather than retroactively relabeling machine work as human certification.
