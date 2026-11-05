# Controlled regularization and stage-representation experiments

## Design

User authorized the two experiments recommended by the granular audit. Before fitting, registered three configurations: unchanged linear-stage control at L2=0.2, weaker regularization at L2=0.05 with unchanged inputs, and categorical stage at L2=0.2. Categorical representation uses indicators for stages 1/2/3, omits introduced stage as reference, and retains the other five inputs. Its dimensionality, scaling and penalty geometry necessarily change with representation. No combined categorical/weaker-penalty experiment was run and no further penalties were searched.

Reused the exact audited 115th–117th Congress training, calibration and evaluation memberships. Core/calibration split, 300 iterations, learning rate 0.12, scaling rule and calibration fitting procedure stay fixed. Each candidate's calibrator is refitted on the same calibration cases; both raw and calibrated scores are retained to distinguish effects. All training labels precede test checkpoints; training/test families are disjoint. Control base artifacts and calibrators reproduce the earlier experiment exactly.

These periods are exposed development evidence. The models are compared with the existing period-specific calibrated full-history control, **not the original survivor**. No fresh 118th-Congress test was performed. No model promotion, new acquisition, paid call or schedule change. The fixed development-lead gate requires lower Brier and no worse log loss in every fold, then ranks qualifying candidates by equal-period mean relative Brier gain.

## Results

8,568 evaluation rows across three periods, with 182 enactments. Families may recur between periods; this is not a set of independent trials.

| Test Congress | Control Brier | L2=0.05 Brier | Relative improvement | Categorical Brier |
| --- | ---: | ---: | ---: | ---: |
| 115 | 0.02515112 | 0.02272965 | 9.63% | 0.02508979 |
| 116 | 0.01621106 | 0.01528609 | 5.71% | 0.01641010 |
| 117 | 0.01799019 | 0.01629932 | 9.40% | 0.01803286 |

Weaker L2 clears the development-lead gate in all three periods. Equal-period mean relative Brier improvement is **8.2441%**. Categorical encoding clears the gate only in 115 and averages **0.4071% worse** Brier. These figures are not claims about improvement over the survivor or unseen data.

| Test Congress | Control log loss | L2=0.05 log loss | Categorical log loss |
| --- | ---: | ---: | ---: |
| 115 | 0.10966112 | 0.09833200 | 0.10953644 |
| 116 | 0.07763809 | 0.07264974 | 0.07937066 |
| 117 | 0.08386591 | 0.07435692 | 0.08446685 |

The weaker-penalty base model also improves uncalibrated Brier in every period: 0.02543031→0.02294130, 0.01624899→0.01541864, and 0.01805305→0.01646377. The improvement is therefore not solely produced by refitting calibration. Supplementary 2,000-family bootstrap intervals are retained in runtime `uncertainty.json`; they are conditional, selected-lead analyses and not independent or selection-adjusted inference.

## Stage behavior

| Test Congress | Stage | Actual enactments | Control expected | Weaker-L2 expected |
| --- | --- | ---: | ---: | ---: |
| 115 | Introduced document | 30 | 69.12 | 55.02 |
| 115 | Origin passage document | 37 | 11.77 | 29.84 |
| 116 | Introduced document | 26 | 43.59 | 31.27 |
| 116 | Origin passage document | 16 | 5.96 | 16.45 |
| 117 | Introduced document | 29 | 62.60 | 48.83 |
| 117 | Origin passage document | 28 | 4.85 | 12.51 |

Expected counts are sums of probabilities. The weaker penalty improves stage separation in the direction identified by the audit, and stage-group Brier improves in every observed stage group across these folds. Important errors remain: in 117, introduced-stage expectations still exceed outcomes, and passage-stage expectations remain well below outcomes. Sparse higher-stage cases must not be treated as calibrated group probabilities.

Categorical stage alone does not solve the mismatch under this penalty/scaling configuration. This does not establish that every categorical model is inferior, only that the fixed tested configuration did not transfer consistently.

## Optimization limitation and decision

The same 300-iteration budget isolates the configured procedure, not fully optimized solutions. Maximum absolute penalized-objective gradients for weaker L2 are approximately 0.00278, 0.00304 and 0.00284, versus 0.00054–0.00060 for control. Thus weaker-L2 fits are not demonstrated converged; different optimization rates may contribute to the measured difference. Do not silently increase their iteration budget and describe it as the same experiment.

**Retain the original survivor; record L2=0.05 with existing linear features as the development lead.** Before freezing a new independently evaluated candidate, run a separately registered convergence sensitivity check with the same rows and parameters, changing only the stopping budget/rule for both control and weaker L2. Do not combine categorical encoding or new features at that stage. Then fix one training/calibration procedure and evaluate it on genuinely unexposed evidence or prospective shadow outcomes. No final combined-training artifact was fitted or deployed in this development experiment.

## Verification and delivery

32 focused tests passed. Exact refitting replay reproduced all three controls and both candidate configurations in every fold. A separate verifier recalculated 51,408 raw/calibrated probabilities, Brier and log-loss metrics, stage expected counts, split membership, source hashes and the selection statistics. Original survivor digest remains `ffb089cff396415431c2e2b04cb99ebf7d75fe040a777da661bb58d6af9d255c`. Result digest: `36a5fa642fc09351b167778fd633f54a79301046675b5099ee7142c1ab0412e0`.

The complete report is saved to the platform campaign chat and retrieved through its API. Runtime protocol/artifacts/predictions/verification are under ignored `data/research-runs/stage-regularization-20261105/`. Machine reproducibility is not independent human certification; historical publication and family-linkage limitations persist.

Commands: `python3 -m scripts.stage_regularization_experiment`, then `python3 -m scripts.verify_stage_regularization`. Existing divergent protocol/results are rejected rather than overwritten. Tests: `python3 -m unittest tests.test_stage_regularization_experiment tests.test_granular_transfer_audit tests.test_chronological_weight_updates tests.test_transfer_diagnosis tests.test_engine`.
