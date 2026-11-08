# Exploratory calendar experiment: nine real fits, mixed result

November 8, 2026. User explicitly authorized a separate exploratory study using agent review after being informed that the original protocol's human-review and sample requirements remained unmet. The [separate protocol](../../research/EXPLORATORY_CALENDAR_PROTOCOL_V1.md) relaxes those computation gates only for this diagnostic study. It does not modify the frozen paper protocol, certify historical source/family/outcome evidence, or authorize model promotion.

## Registration and execution

Executed `python3 -m scripts.exploratory_calendar --output data/research-runs/exploratory-calendar-20261108-v1`.

- Machine registration sealed before fitting: `b61d21f14255b73ee55573f78865114c0646ef748bc1f9dc0c22af440e108200`.
- Result digest: `cd420dc3cce731a599381b89ae690ea894b97c080246506c1a48751367d8a811`.
- Exact ordered legacy core/calibration/evaluation memberships; folds 115, 116, 117. Their evaluation rows total 8,568 appearances, 182 positive appearances and 7,596 distinct provisional global families. Repeated families across evaluation periods are handled together in the descriptive bootstrap; these are not independent period replications.
- Three fixed arms per fold: original six-feature control, plus remaining time, plus remaining time and stage interaction. Nine actual model fits, fixed L2=.05, no parameter search, no 118 ranking, no final deployment fit.
- All nine converged at the registered gradient threshold; 3,612–3,979 iterations. Scalar gradients agree; training-logit clipping inactive. Each control exactly reproduces its earlier base artifact, including weights, means, scales and iteration count.
- Rate and stage baselines fitted only on earlier core+calibration populations. Calibration remains the existing fixed 2,000-step procedure, not a claim of calibrator convergence.
- Saved per-arm artifacts, diagnostics, raw/calibrated predictions, Brier/logloss, positive/negative errors, expected events and fixed-decile reliability. Runtime artifacts remain ignored.

## Results

Calibrated Brier loss, lower is better:

| Congress | Six-feature control | + remaining time | + time + stage interaction | Historical rate | Stage baseline |
| --- | ---: | ---: | ---: | ---: | ---: |
| 115 | 0.02269734 | 0.02270439 | 0.02280179 | 0.02684394 | 0.02289601 |
| 116 | 0.01528056 | 0.01521718 | 0.01512030 | 0.01694436 | 0.01571366 |
| 117 | 0.01625855 | 0.01620484 | 0.01598870 | 0.01895865 | 0.01564042 |
| Equal-period mean | 0.01807882 | 0.01804214 | 0.01797026 | 0.02091565 | 0.01808336 |

| Arm | Mean Brier reduction vs control | Skill vs historical rate | Skill vs stage baseline |
| --- | ---: | ---: | ---: |
| Control | — | 13.5632% | 0.0251% |
| + time | 0.2029% | 13.7386% | 0.2280% |
| + time + interaction | 0.6004% | 14.0822% | 0.6254% |

**Decision: mixed exploratory result; no qualifying lead.** Both additions improve Brier and logloss in 116/117. Time alone slightly worsens Brier in 115 despite lower logloss; interaction worsens both there. Therefore neither satisfies the predeclared all-three-fold rule. Do not promote the lowest average score or claim the 60% ambition was reached. The unchanged control remains the exploratory reference.

The interaction-minus-control equal-period Brier difference has descriptive paired-family 95% interval **[-0.00028854, +0.00006309]**. Time-minus-control interval is **[-0.00007613, +0.00000149]**. Both include zero. All 10,000 global-family draws were valid; seed 20261108 was explicitly registered for this separate study. Intervals are conditional on exposed periods and the provisional family graph, unadjusted for selection/multiplicity. Their role is descriptive uncertainty, not independent significance or generalization evidence.

## Interpretation and limits

This tests whether a simple remaining-time coordinate adds to an already strong stage-based control. It does not test the value of full bill meaning, text, substantive categories or actual announcement-vintage schedules. A small mixed calendar effect does not disprove those ideas, but it does not justify escalating model claims or automatically adding arms after scores.

Underlying human source/label/family certifications remain pending and raw positive counts remain below several original per-fold floors. The separate exploratory authorization permits computation with these disclosed limitations; it does not turn them into passed evidence gates. The existing frozen paper, survivor, challenger and original bill-context pilot remain unchanged. No prospective forecasts, new source downloads, paid calls, deployment or schedule changes occurred.

## Verification

An independent agent reviewed the amended scope and code before scoring; flagged dependency-hash coverage and control-equivalence gaps, both corrected before registration. Post-run scalar/baseline/split replay is documented in the [independent audit](../../research/reviews/20261108-exploratory-calendar-audit.md). The agent's judgment is machine review, not human certification.

Root validation: **321 tests passed in 78.390 seconds** with `python3 -m unittest discover -s tests -q`. Six focused experiment/convergence tests passed before execution; the three new tests also passed after adding an explicit skip for environments lacking optional NumPy. Independent agent replay passed numerical, membership and all 10,000 bootstrap checks. Before/after audit confirms the frozen artifacts and all 359 original pilot files unchanged. Shared lease released; diff whitespace checked. Preservation receipt digest: `43177802d7f3fe83929f6c8f6a910b061d99234aaeab10e624efa18f1daaf496`.
