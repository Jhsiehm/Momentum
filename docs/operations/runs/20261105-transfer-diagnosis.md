# Transfer diagnosis and constrained weight experiments

User authorized diagnosis followed by targeted weight experiments. Original survivor artifact is preserved and its digest verified as `ffb089cff396415431c2e2b04cb99ebf7d75fe040a777da661bb58d6af9d255c`. No promotion, recurring schedule change, paid call or new acquisition.

## Design and exposure

The completed campaign's 2,315 eligible 118th-Congress bills, including 29 enactments, are now explicitly development evidence. This analysis does not create a fresh holdout. Before computing the new variants, the runtime protocol fixed two fractions: 25% and 50% of the weight change from survivor to calibrated challenger. Coefficients are first converted into common raw feature units; interpolation includes the intercept and incorporates the challenger's affine-logit calibration. This changes weights, not a simple average of probabilities. No model is trained on these outcomes, but the blending fraction is selected using them, so performance is selection-biased.

The uncalibrated model is included as a diagnostic ablation, not an additional candidate search. The fixed candidate rule selects the lowest-Brier blend only if it improves Brier and does not worsen log loss versus survivor. Selection identifies a development lead only. Existing evidence/temporal eligibility is reused without alteration.

## Findings

| Model | Brier | Log loss |
| --- | ---: | ---: |
| Survivor | 0.0121441147 | 0.0667170447 |
| Retrained, before calibration | 0.0121892830 | 0.0663909410 |
| Calibrated challenger | 0.0121439707 | 0.0653982644 |
| 25% weight change | 0.0121321153 | 0.0662807277 |
| 50% weight change | 0.0121296012 | 0.0659190805 |

For the calibrated challenger, the sum of squared-error changes on 2,286 negatives is -0.7773715, almost exactly canceled by +0.7770382 on 29 positives. These sums reconcile to the overall Brier difference after division by 2,315. Calibration partially rescued the retrained model; it was not the sole cause of the lost transfer performance.

The effective publication-stage coefficient fell from 3.13937 in the survivor to 2.46843 in the calibrated challenger; publication-count coefficient fell from 0.49468 to 0.27106. The raw intercept also became more negative. These are algebraic/descriptive changes, not causal explanations. The report includes chamber, publication-stage and fixed survivor-probability strata, class-specific metrics, and mean logit-change contributions. The age feature is effectively constant at this checkpoint and its coefficient is near zero.

The 50% blend is the exploratory lead: Brier is 0.1195% lower than survivor. The 25% blend improves 0.0988%. Both are far below the earlier campaign's 2% practical threshold. Conditional 2,000-family bootstrap intervals for Brier difference include zero: 50% [-0.0001136503, +0.0001021636]; 25% [-0.0000646210, +0.0000493875]. These intervals do not correct for development selection or establish independent validation.

## Decision and next gate

Retain survivor; keep the 50% artifact only as a reproducible development lead. Do not launch a larger confirmation campaign on the claim that this small exposed-data improvement is a win. First test whether the constrained-update rule is stable across chronological development folds with period-appropriate anchors; the original survivor must not be backtested into periods preceding its training-label availability. A later independent study must freeze its candidate, eligible population, sample size, minimum meaningful effect, uncertainty method and outcome-resolution rules before scoring. Plan sample size from paired-error variance and expected enactments, rather than treating 50 enactments as sufficient statistical power. If no genuinely unexposed historical cohort remains, use prospective shadow forecasts and wait for outcomes. Never extend a scored cohort until it wins.

## Verification and delivery

22 tests passed, including raw-coefficient equivalence, blend endpoints/logit interpolation, invalid-fraction rejection, error-contribution reconciliation and existing engine tests. Exact deterministic replay passed. A separate arithmetic check recalculated 11,575 probabilities and each model's Brier score. All original and calibrated predictions reproduce the earlier campaign within 1e-12. Original survivor remains unchanged.

Runtime protocol, complete predictions/models, diagnosis, verification and platform receipt are in ignored `data/research-runs/weight-diagnosis-20261105/`. Result digest: `dc8b77c66f77a1eea4acc504e99b1c678ba47f6502dc88a95ad92c1e2b8b7f74`. Full report was saved, attached to the campaign chat and retrieved through the platform API. Machine checks are not independent human certification. Historical publication/family-linkage limitations persist.

Reproduce with `python3 -m scripts.diagnose_transfer`; existing result must match exactly. Test with `python3 -m unittest tests.test_transfer_diagnosis tests.test_engine`.
