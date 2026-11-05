# Granular investigation of period-dependent forecast errors

## Scope and evidence

The user requested an in-depth granular investigation. We audited all 8,568 evaluation rows in the three chronological update tests (115th–117th Congresses; 182 enactments). These are exposed development outcomes. No new candidate was fitted or promoted; original survivor remains unchanged. Period-specific anchors are not the survivor. All conclusions below concern day-180 own-bill public-law enactment by Congress end, not chamber passage, policy incorporation into another bill, or the entire congressional population.

The report preserves nine subgroup partitions: outcome, chamber, publication stage, chamber-by-stage, publication count, publication recency, recent publication activity, time remaining in Congress, and fixed anchor-probability bins. Every partition reconciles to the complete sample and error change. It also records the 20 most helped/harmed cases per period, raw coefficients, training/additional/evaluation distributions, exact feature collisions, and top-case removal sensitivity. Groups with fewer than ten enactments are flagged; no subgroup significance claims or multiple-comparison-adjusted inference are made.

Initial analysis is retained in `data/research-runs/granular-transfer-20261105/`. Additional saved-fit gradient and training-stage checks were added as a disclosed post-hoc extension in `data/research-runs/granular-transfer-v2-20261105/`, preserving the first report. This is a diagnostic investigation, not an untouched trial.

## 1. The failure mechanism differs across periods

Changes below are sums of squared errors, full update minus anchor; negative is better. Divide by each period's sample size for Brier change.

| Test Congress | Change on negatives | Change on enactments | Net change |
| --- | ---: | ---: | ---: |
| 115 | +1.349601 | -2.638441 | -1.288840 |
| 116 | -0.131551 | -0.058468 | -0.190019 |
| 117 | +0.597094 | -0.368090 | +0.229004 |

The 115th-period update accepted more error on unsuccessful bills but gained more on enactments. The 116th-period update improved both groups. The 117th-period update also improved enactments, but that gain was overwhelmed by worse non-enactment predictions. This is different from the previously analyzed 118th comparison, where negative-case gains were canceled by positive-case losses. There is no single observed direction of failure that justifies globally increasing or decreasing all probabilities.

Removing the 1, 5 or 10 cases with largest absolute error changes does not reverse any period's net sign. These are sensitivity calculations only: all cases remain in the main result. The 117th loss becomes larger after removing the ten most influential changes, so the loss is not explained by one unusually harmful bill.

## 2. Stage separation is the clearest repeated mismatch

Stages are publication-document proxies: stage 0 means an introduced-document stage, not a verified absence of legislative activity; stage 2 means a matching originating-chamber passage publication. Expected enactments are sums of model probabilities, not rounded counts of positive classifications.

| Test Congress | Stage | Bills | Actual enactments | Anchor expected | Update expected |
| --- | --- | ---: | ---: | ---: | ---: |
| 115 | Introduced document | 2,518 | 30 | 50.11 | 69.12 |
| 115 | Origin passage document | 129 | 37 | 8.38 | 11.77 |
| 116 | Introduced document | 2,654 | 26 | 48.19 | 43.59 |
| 116 | Origin passage document | 91 | 16 | 5.73 | 5.96 |
| 117 | Introduced document | 2,969 | 29 | 46.60 | 62.61 |
| 117 | Origin passage document | 64 | 28 | 4.80 | 4.85 |

Both models overpredict the introduced-document group and underpredict the passage-document group in all three periods. In the 117th period, the update predicts 2.11% on average for the first group versus 0.98% observed, and 7.58% for the passage group versus 43.75% observed. Those passage outcomes are still sparse and selected; 43.75% must not become a production probability by copying this exposed test rate.

The introduced-document group contributes +0.276675 squared-error change in the 117th period, exceeding the overall +0.229004 loss because other groups partly offset it. Both House and Senate introduced-document groups worsen (+0.169795 and +0.106880). This is not confined to one chamber.

In the same period, cases whose latest eligible publication is more than 90 days old contribute +0.254919; they substantially overlap the introduced-document group. These contributions must not be added across overlapping partitions. Loss occurs in all three remaining-time bands, so it is not isolated to late-Congress cases.

## 3. The training data already contains a large stage distinction

| Model trained for test Congress | Introduced-stage training enactment rate | Passage-stage training enactment rate |
| --- | ---: | ---: |
| 115 | 60 / 4,238 = 1.42% | 45 / 138 = 32.61% |
| 116 | 71 / 6,206 = 1.14% | 71 / 238 = 29.83% |
| 117 | 111 / 8,299 = 1.34% | 93 / 322 = 28.88% |

This suggests investigating how the existing model represents and regularizes stage before assuming we must acquire more data. These aggregate associations do not identify a causal effect of stage, nor prove that a more flexible fit will generalize.

The 117th update raises its raw intercept from -3.90884 to -3.65834 while reducing its stage coefficient from 2.95483 to 2.43437. As the feature encodes stage divided by four, these coefficients are not per-stage probability changes. The update raises the broad low-stage group's probabilities while flattening a useful separation. Age is constant at the 180-day checkpoint in every evaluation fold and supplies no within-fold discrimination.

## 4. Regularization is a stronger lead than simply running more iterations

The saved fits use 300 iterations and L2=0.2. We recomputed the gradient of their actual penalized training objective on their exact core training rows. In the 117th update, the standardized stage data gradient is -0.0456500 and the penalty gradient +0.0456258: the net is about -0.00002417. Comparable stage cancellation occurs in the other folds. Largest remaining objective-gradient coordinates are the intercepts, approximately 0.00054–0.00060.

This is consistent with the regularizer suppressing stage separation rather than a large unfinished stage-gradient step. It does not prove global convergence, an optimal penalty, or that reducing L2 will improve unseen forecasts. Feature correlations, the scale floor, and linear stage encoding also matter. The finite-difference gradient test verifies the audit calculation.

## 5. Calibration is not uniformly responsible

We scored four diagnostic combinations: old/new base model crossed with old/new calibration. The symmetric two-factor attribution averages each factor's contribution over both orders; contributions sum exactly to total metric change. These hybrid combinations are counterfactual calculations on saved artifacts, not new fitted or deployable models. Base-model changes include training membership, standardization, and the deterministic core/calibration allocation changes.

| Test Congress | Base-model contribution to Brier change | Calibration contribution | Total |
| --- | ---: | ---: | ---: |
| 115 | -0.00022907 | -0.00024529 | -0.00047436 |
| 116 | -0.00007705 | +0.00000899 | -0.00006806 |
| 117 | +0.00026545 | -0.00019059 | +0.00007486 |

For Brier in the failing 117th period, calibration partly rescues the base-model loss. For log loss, both factors worsen the score. A global calibration change therefore cannot be justified as the sole fix, and metric-specific tradeoffs must remain visible.

## 6. Many different bills are indistinguishable to this feature set

| Test Congress | Bills | Unique exact feature vectors | Enactments sharing a vector with negatives |
| --- | ---: | ---: | ---: |
| 115 | 2,717 | 203 | 42 of 75 |
| 116 | 2,792 | 197 | 28 of 48 |
| 117 | 3,059 | 200 | 32 of 59 |

Any deterministic model using only these six inputs must assign the same probability to bills with identical vectors. Changing weights cannot distinguish those bills. This is not inherently a forecasting error—probabilities appropriately represent uncertain outcomes—but it identifies a limit to bill-specific ranking. It is not a population performance ceiling.

The six inputs are publication stage, fixed age, publication count, time since eligible publication, chamber, and recent publication count. They omit remaining time to the outcome deadline, title/text content, sponsor/cosponsor characteristics, and committee detail. Current snapshots cannot automatically supply historically available values for the omitted fields.

## 7. Prioritized research response

1. Test regularization and stage representation under a small, fixed development design. Compare the existing fit with a weaker-penalty fit while keeping training rows, calibration allocation, features and stopping checks fixed. Separately test categorical stage encoding; do not change both and attribute gains to one. Do not choose a penalty by repeatedly inspecting 118th outcomes.
2. Inspect stage-specific calibration on disjoint earlier training data. Report Brier and log loss together; prohibit using the observed test-group rates above as fitted probabilities.
3. Add remaining days to Congress end as the first new-feature candidate. It can be derived from existing cutoff/calendar information, but usefulness remains untested. Keep chronological/family controls and check interactions with stage.
4. Only then consider historical introduced-title/text signals and sponsor/committee evidence. Reuse the audited introduced publication where possible. Sponsor/cosponsor and committee histories require separate as-of availability checks; current cumulative totals are not valid historical predictors by default.
5. Freeze a single development-selected candidate before independent evaluation. All periods used here are exposed. If no suitable untouched historical sample exists, use prospective shadow forecasts and await outcomes. Keep the survivor until that evaluation supports a replacement.

No experimental model change was made during this investigation. These findings justify a narrower next experiment, not a promise of improved accuracy.

## Verification and delivery

29 tests passed, including score-partition reconciliation, exact mixed-vector counting, and finite-difference gradient verification. Exact offline replay matched. Separate arithmetic checked 34,272 hybrid probabilities, Brier/log-loss scores, all subgroup totals and the symmetric decomposition. The full granular report and verification are saved in the platform campaign chat and API-verified. Reproduce with `python3 -m scripts.granular_transfer_audit`. Runtime evidence is ignored by Git; reproducible code and this receipt are versioned. Machine checks are not independent human certification. Original source availability and family-linkage limitations remain.
