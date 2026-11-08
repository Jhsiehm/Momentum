# Mechanism and direction rubric v2: partial execution

November 8, 2026. The user authorized continuing the semantic design work with independent agents. [Frozen rubric](../../research/BILL_MECHANISM_RUBRIC_V2.md) applies to the remaining 40 design bills, excluding the ten v1 cases. Runtime evidence remains ignored under `data/research-runs/mechanism-rubric-v2-20261108/`.

## Completed and preserved

Frozen the twelve mechanism definitions and separate operation, dimension, actor, target, conditions and exact evidence offsets. Retained full bill language. V2 presence means operative treatment in any direction, so its statuses are not directly comparable with v1. Registered two disjoint 20-case annotation batches and a deterministic ten-case methods subset before annotation. This design uses one primary annotation and a peer challenge per case, not two blinded annotations or an agreement study.

Reviewer A read all 20 assigned complete texts and sealed 240 statuses: **98 present, 137 absent, five uncertain**, with **197 evidence-linked effects**. The primary validator passed, including exact quote offsets and source bindings. These are provisional interpretations, not verified semantic accuracy. Reviewer B reported reading its complete batch and drafting 18 records, but no sealed B submission exists; that progress is not counted as completed annotation.

The methods reviewer inspected all ten audit-subset source texts before annotations and saved source-first notes. Its code audit demonstrated two peer-validation holes: mismatched mechanism/effect-index references and an allowed historical-eligibility claim. Both were repaired and covered by rejection checks. Duplicate input and batch identity checks were also added. The methods reviewer has not yet completed the planned annotation/subset or correction audit.

## Interruption and resume point

Both annotation agents stopped with the tool error: “You hit your spend cap set by the owner of your workspace.” The second primary batch, both reciprocal reviews and the methods annotation audit remain incomplete. No peer consensus or complete 40-case annotation is claimed. Resume the missing B batch first; preserve A unchanged, then cross-review both complete batches and audit the fixed subset plus every requested correction. Keep corrections in separate bound addenda, never overwrite primary evidence. Peer receipts must include `human_certified: false` and `historical_feature_eligible: false`; a nonnull effect index must reference the named mechanism.

## Predictive readiness

Root separately inspected already-exposed outcome counts for readiness only; these counts were not supplied to source annotators. Intersecting the 40 design cases with unchanged legacy splits gives:

| Evaluation Congress | Training core n / positives | Calibration n / positives | Evaluation n / positives |
| --- | ---: | ---: | ---: |
| 115 | 10 / 0 | 2 / 0 | 8 / 1 |
| 116 | 15 / 0 | 3 / 0 | 8 / 0 |
| 117 | 20 / 1 | 4 / 0 | 7 / 0 |

Every calibration subset lacks positive cases; two training cores also lack them. This selected design sample is not a registered modeling population and cannot support the planned calibrated predictive comparison. Broader dated source coverage, sufficient natural outcomes, a frozen reviewed encoding/extractor and a separately registered matched population remain necessary. Do not select evaluation bills by outcome merely to repair these counts. No model fits, new outcome scores, forecasts or 60% improvement claim.

## Validation and provenance

Eleven focused tests passed after final validator repairs (`tests.test_mechanism_rubric_v2`, `tests.test_mechanism_design_audit`, `tests.test_bill_context_design_text_v2`). An initial synthetic repeated-quote fixture used an incorrect offset; it was corrected before passing. No full-suite rerun claimed. Root verified all 40 source views against their preserved full envelopes, the frozen rubric hash, A's schema and quotes, all 359 original pilot file hashes and the unchanged frozen-model audit. Quality cases remain unparsed; no new source acquisition or scheduler change. Shared lease released at close.

- Registration: `0833e20efeaa40bc641662a7433ffee910d1927cd3574438cd99138b2cee32dc`.
- Reviewer A: `2a3e3715ac9024140fff6ce2d9d1eddbcc5beea17e1ff8eaecb13e7f99aaebef`.
- Partial audit: `4bc1088556543ef32d055aaae18af8cc1459d9d8e26b8b4bc72bc91827d21ea9`.
- Readiness counts: `a62c30763fd612d1a89cb20de06ee0b1e2ebaabcf35a7ac0ffb62221c20c8776`.

Integrity checks establish structure and source matching, not interpretation, historical availability or human certification. Original protocols, labels, model artifacts and audit gates remain unchanged.
