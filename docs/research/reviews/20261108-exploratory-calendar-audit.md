# Independent exploratory calendar audit

November 8, 2026. Independent agent review; not human certification. Scope: the separately authorized [exploratory calendar protocol](../EXPLORATORY_CALENDAR_PROTOCOL_V1.md), its implementation and the completed nine-fit run. No model fitting, source acquisition or original-protocol changes were performed by this auditor.

Run: `data/research-runs/exploratory-calendar-20261108-v1`. Result digest: `cd420dc3cce731a599381b89ae690ea894b97c080246506c1a48751367d8a811`.

## Before-score review

The scoped waiver of human certifications and reviewed-positive-family floors is explicit and does not assert those requirements passed. The original paper remains frozen. Calendar-only E1 does not require rich-text extraction quality. All three periods are exposed development evidence, not independent validation.

Reviewed the fixed nine-fit budget, exact encodings, original memberships, core-only preprocessing, objective/stopping rules, fixed calibration, earlier-only baselines and all-period lead criterion before scoring. Requested stronger whole-artifact control reproduction and executable dependency hashes. The implementer added these before registration, together with a training-logit clipping-inactivity gate and a valid-bootstrap-draw threshold. The new seed 20261108 is explicitly registered for this separate exploratory study.

## Independent numerical replay

The read-only [reproducer](../../operations/reproducers/verify_exploratory_calendar_20261108.py) retains these checks. From the repository root, with NumPy available, run `python3 docs/operations/reproducers/verify_exploratory_calendar_20261108.py`. It reads the original ignored run and validates its registered code hashes; it neither fits models nor writes artifacts. Later changes to registered source files intentionally cause a hash failure, so replay against the corresponding execution checkout.

Passed read-only Python replays using independently written scalar arithmetic rather than the experiment's prediction, metric, summary or interval functions:

- Verified registration, fold and result seals; registered code, protocol, population and global-family hashes.
- Reconstructed legacy splits, checked training identity unions, evaluation ordering, disjoint core/calibration/evaluation families, and training-label availability before evaluation checkpoints.
- Independently reconstructed remaining time from Congress number and the January 3 17:00 UTC boundary; checked the interaction uses the already normalized stage input.
- Recomputed core-only feature means and scales for all nine fits, exactly matching stored values.
- Recomputed unclipped logistic gradients: every maximum absolute gradient is at most 1e-6, iterations stay within 300–20000, and training logits remain inside the clipping boundary.
- Replayed all raw predictions and affine-logit calibration predictions within 1e-12. Calibration parameter optimization itself was not independently refitted.
- Reconstructed rate and stage baselines using only core plus calibration outcomes; replayed raw/calibrated Brier and log loss exactly.
- Recomputed equal-period averages and the all-period lead decision.
- Independently rebuilt paired global-family bootstrap sufficient statistics and replayed all 10000 draws: 7596 global evaluation families, zero invalid draws, all stored interval bounds reproduced within 1e-14. Shared family multiplicities across periods were retained.

## Findings

| Exposed evaluation Congress | Bills | Positive outcomes | Control Brier | Time Brier | Interaction Brier |
| --- | ---: | ---: | ---: | ---: | ---: |
| 115 | 2717 | 75 | 0.0226973393 | 0.0227043926 | 0.0228017882 |
| 116 | 2792 | 48 | 0.0152805599 | 0.0152171796 | 0.0151203010 |
| 117 | 3059 | 59 | 0.0162585536 | 0.0162048421 | 0.0159887049 |

Neither addition qualifies as a development lead: both worsen calibrated Brier in Congress 115. The interaction's equal-period mean Brier is 0.01797026468 versus control 0.01807881760, a descriptive 0.60044% reduction. Its skill is 14.08221% versus the rate baseline and 0.62543% versus the stage baseline. These different denominators must not be conflated. The time-only reduction versus control is 0.20289%.

The interaction-minus-control descriptive 95% Brier-difference interval is [-0.000288540, 0.0000630864], spanning zero. No interval is selection-adjusted or evidence of independent success. The 60% ambition was not reached. Preserve the control as the plan's anchor; retain the mixed findings without tuning against these results.

Conclusion: no execution or numerical blocker found in this registered run. This finding does not certify historical rendition availability, negative-label completeness, family genealogy, reviewer qualifications or independent generalization. Those limitations remain explicit, and this audit does not release the frozen paper study or later experiment stages.
