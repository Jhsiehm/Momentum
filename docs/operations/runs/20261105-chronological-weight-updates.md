# Chronological constrained-weight update tests

User authorized testing restrained updates across earlier development periods. Original survivor remains unchanged. This tests an update rule using period-specific anchors, not the saved survivor or an independently validated successor.

## Fixed design

Registered 25% and 50% interpolation fractions before this run. For each test Congress (115, 116, 117), reconstruct the existing audited temporal/family split. Fit a calibrated anchor excluding the latest eligible training Congress; compare with the existing calibrated full-history update, and two raw-coefficient interpolations. The anchor and update use the same deterministic core/calibration split rule, L2 and fitting settings. Intercept and all six coefficients are interpolated in common raw feature units. A full update can change core/calibration allocation as data grows, so this measures the combined updating procedure, not the isolated causal effect of adding rows.

All training labels must precede the earliest test checkpoint. Training and test families must be disjoint. The first historical fold is omitted because it lacks older training history for an anchor. Anchor training requires at least 200 cases and five positives, with both classes in core and calibration. Existing full-update probabilities must reproduce exactly within numerical tolerance. Evaluation periods were already exposed; this is exploratory development, not confirmation. No new acquisition, outcome-driven replacement, schedule change or promotion.

The fixed consistency criterion requires a restrained update to improve Brier and not worsen log loss in all three periods. Report each period, equal-weight average relative Brier gains, and comparisons with full updates and historical rates. Do not count recurring families across folds as independent trials.

## Results

| Test Congress | Eligible bills | Enactments | Anchor Brier | 25% update | 50% update | Full update |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 115 | 2,717 | 75 | 0.02562548 | 0.02550423 | 0.02538332 | 0.02515112 |
| 116 | 2,792 | 48 | 0.01627911 | 0.01626151 | 0.01624432 | 0.01621106 |
| 117 | 3,059 | 59 | 0.01791533 | 0.01792677 | 0.01794249 | 0.01799019 |

8,568 evaluation rows across three periods, with 182 enactments; not necessarily independent bill families across periods. All updates improve Brier and log loss versus anchor in two periods, and fail that joint criterion in the third. Equal-weight mean relative Brier improvement: 25% update 0.1725%; 50% update 0.3357%; full update 0.6171%. A positive average does not meet the registered all-period consistency criterion or establish statistical significance. Full updating performs best in the first two periods; retaining the anchor performs best in the third. Restraint softens both gains and losses.

**No consistent restrained-update lead. Preserve survivor.** This does not establish that the survivor is optimal; it establishes that these weight-update experiments have not justified replacing it. The previously saved 50% artifact remains a research candidate only. No independent confirmation is claimed and no pooled confidence interval is reported.

## Verification and delivery

26 focused tests passed. Exact refitting/replay reproduced the full result. Separate arithmetic verification recalculated 34,272 probabilities plus Brier and log-loss metrics. Temporal/family checks passed; existing full-update predictions match within 1e-12. Original survivor digest remains `ffb089cff396415431c2e2b04cb99ebf7d75fe040a777da661bb58d6af9d255c`.

Runtime protocol, models, predictions and verification are under ignored `data/research-runs/chronological-weight-updates-20261105/`. Full report is saved to the platform campaign chat and API-verified. Source preservation and historical publication/family-linkage limitations remain; these are machine checks, not independent human certification.

Reproduce using `python3 -m scripts.chronological_weight_updates`. Existing protocol and result must match; no overwrite on divergent replay. Tests: `python3 -m unittest tests.test_chronological_weight_updates tests.test_transfer_diagnosis tests.test_engine`.

## Next research decision

Do not tune more blending fractions on these same outcomes. Investigate period-specific feature/outcome shifts and whether the six historical publication features omit useful signals. Any proposed new feature must have verifiable historical availability before its checkpoint. Use exposed folds for development, then freeze one model and a new evaluation design before collecting or scoring genuinely unexposed outcomes. Evidence from these folds alone cannot establish a reliable adaptive update policy.
