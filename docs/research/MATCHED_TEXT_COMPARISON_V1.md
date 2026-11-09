# Matched introduced-text comparison: specification v1

November 8, 2026. This freezes the next candidate question and identity-only starting population. It is **blocked preparation, not an execution registration or permission to fit**. No new outcomes, predictions or model scores are read. No qualified review is invented. The calendar study's scoped exceptions are not inherited.

## Readiness decision before scores

Select the original programme's E3 introduced-text comparison: six-feature anchor versus that same anchor plus introduced text. E2 is not the next candidate because no semantic descriptor fields have passed their designated quality gate. The conditional E3 descriptors-plus-text arm is excluded for the same reason. This is a readiness choice, not evidence that text is better. Retain full bill language and structural sidecars; the sidecars do not add predictive columns or create arithmetic interpretations. Current XML bytes are not presumed historically eligible.

The controlling rules are [the original plan](BILL_CONTEXT_EXPERIMENT_PLAN_V1.md), especially §§3, 5–9 and 11–12, [methods clarification](BILL_CONTEXT_METHODS_CLARIFICATION_V1.md) and [paper protocol](PAPER_PROTOCOL_V1.md). This specification neither amends them nor bypasses source, family, outcome, qualified-review, numerical or custody requirements. The source feasibility study is a bounded dependency test on eight cases, not certification of a model corpus.

## Identity-only population freeze

Read only the existing sealed calendar registration, hash `b61d21f14255b73ee55573f78865114c0646ef748bc1f9dc0c22af440e108200`, and copy its `memberships` identities in original order. No row feature or outcome file is loaded. This establishes planned candidate populations, not eligible populations. Their existing development exposure persists.

| Evaluation Congress | Planned core IDs | Planned calibration IDs | Planned evaluation IDs |
| --- | ---: | ---: | ---: |
| 115 | 3,569 | 893 | 2,717 |
| 116 | 5,272 | 1,319 | 2,792 |
| 117 | 7,049 | 1,763 | 3,059 |

These repeated fold appearances are not independent cases and must not be summed to satisfy positive-family floors. `eligible_memberships` and `eligible_counts` remain null: unknown eligibility is not a negative outcome or an accepted zero feature. Source-unavailable rows will require an explicit exclusion ledger; both arms must then use one identical frozen eligible core/calibration/evaluation membership in each fold. That subsequent execution freeze must occur before scoring. Identity-only temporal Congress checks do not certify exact label dates, global-family disjointness or negative evidence coverage.

## Fixed conditional comparison

Two arms × three required folds = **at most six model/period fits**, with the original six-hour block cap and overall 75-fit programme ceiling. No unused slots authorize searches. No fit is executed by this freezer. Calibration fits and matched rate/stage calculations remain separately defined by the original programme; the six model-fit ceiling does not conceal them. A missing or failed fold blocks the all-fold decision.

The structured control has the original six columns, fitted through the same sparse solver as the text arm, with core-only means/scales and scale floor 0.1. The objective is mean negative log likelihood plus `(0.05/2) × sum(slope²)`, leaving the intercept unpenalized. Sparse deterministic L-BFGS has a 20,000-iteration cap and maximum absolute objective gradient ≤1e-6; the low-dimensional gradient-descent minimum-step rule does not apply. Independent numerical equivalence and a pinned research-only dependency implementation are required before fitting; no silent dense conversion or penalty substitution.

Text uses introduced language, Unicode normalization and lowercasing, word unigrams/bigrams, minimum five core documents, maximum document frequency 0.95, maximum 10,000 features and core-only TF-IDF vocabulary/IDF. Text vectors are L2-normalized and concatenated with standardized structured columns; do not center or variance-standardize sparse text. Retain negation; no stemming or generic stopword removal, embeddings, latest/final-text arm or vocabulary search. Focal identity and status boilerplate must be masked while substantive statutory references remain. The original programme does **not** specify an exact Unicode normalization form, tokenizer or masking implementation. Those details are explicitly unresolved and block execution until tested and hash-frozen; this document does not silently supply new defaults.

Calibrate each arm using the existing 2,000-step monotone affine-logit procedure on the identical earlier calibration families. Both classes must exist in core and calibration; that computational check is not proof of adequate sparse-event calibration. Historical-rate baseline is Beta(1,1) over eligible core plus calibration; stage baseline is `(stage positives + 5 × global rate)/(stage n + 5)` for stages 0–3. Both are fitted before evaluation and scored on identical cases.

Report raw/calibrated Brier and log loss, Brier skill against rate and stage, fixed-decile reliability/counts, expected events, class-specific Brier, event/family counts and all coverage/exclusions. Primary aggregation is equal-period mean losses; skill is the ratio of those mean losses. Bill-weighted pooled loss is secondary. A development lead strictly improves calibrated Brier and does not worsen log loss in every required fold. Global-family paired bootstrap uses 10,000 draws and original seed 20261105; report empty-period invalid draws and block interval-based success below 9,000 valid draws. These are descriptive conditional intervals on exposed development periods, not independent validation. No promotion or 60% claim follows; a later confirmatory 60% contrast requires its own prespecified multiplicity/custody handling.

## Executable fail-closed preflight

`scripts/freeze_matched_text_comparison_v1.py` seals the specification, candidate memberships, code/protocol hashes and prior registration bytes. It can additionally hash-bind the sealed source feasibility result; it does not promote a favorable eight-case result into corpus eligibility. Output must be a new directory under ignored `data/`. Existing results cannot be overwritten. Input/code hashes are rechecked before the result is sealed.

All ten prerequisites are explicitly unknown/false: historical introduced text; required qualified source/family/outcome reviews; methods definition and reviewed 200/100 positive-family counts; exact temporal/family eligibility; eligible matched populations; core/calibration classes; exact preprocessing; sparse numerical verification; storage/runtime preflight; complete execution registration. No booleans or user-supplied evidence can unlock fitting through this tool, and it contains no model-fitting function. Resolving gates requires evidence-bound later execution tooling, not changing a saved verdict.

Reproduction after tests and before any predictive work:

```sh
python3 -m unittest tests.test_matched_text_comparison_v1
python3 -O -m unittest tests.test_matched_text_comparison_v1
python3 -m scripts.freeze_matched_text_comparison_v1 data/research-runs/matched-text-comparison-v1-20261108
```

The freezer can take `--feasibility-result PATH` to include a sealed local feasibility result. Exact run hashes and the executed command belong in the operation receipt. Software tests validate specification integrity and fail-closed behavior; they do not measure model efficacy or certify data. The shortest next empirical step is to resolve the historical-source route, exact preprocessing/numerics and designated reviews for this one comparison, then freeze the eligible population once and execute within its unchanged budget.
