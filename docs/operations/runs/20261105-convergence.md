# Convergence check and frozen weaker-penalty research candidate

## Fixed procedure

User authorized further machine-learning work after the regularization experiment. We registered a bounded training-convergence check, not an open-ended hyperparameter search. Compare only linear-stage L2=0.2 and L2=0.05, using identical prior core/calibration/test memberships in the 115th–117th Congress folds. No additional features, penalties or test cohorts searched.

Both base models use the existing mean/scaling rules, smoothed-rate initialization and gradient-descent learning rate 0.12. Continue for at least 300 iterations until maximum absolute penalized-training-objective gradient is at most 1e-6, capped at 20,000 iterations. Stopping uses training data only. Check the 300-step predictions against the original scalar implementation within 1e-12. Preserve the same 2,000-iteration calibration procedure and disjoint calibration rows; convergence statements apply to the base fit, not the calibrator or real-world accuracy.

A development lead must improve calibrated Brier without worsening log loss in every fold, and both fits must reach the gradient tolerance. If that gate passes, fit and freeze the weaker-penalty procedure on the previous final historical training population, provided its base also reaches tolerance. No deployment or independent-validation claim is permitted.

This research-only runner uses optional NumPy 2.0.2 for float64 arithmetic. The core application remains independent of NumPy; research tests skip when the optional dependency is absent. No package installation was needed.

## Results

| Test Congress | Converged control Brier | Converged L2=0.05 Brier | Relative improvement | Control iterations | L2=0.05 iterations |
| --- | ---: | ---: | ---: | ---: | ---: |
| 115 | 0.02515716 | 0.02269734 | 9.78% | 2,553 | 3,758 |
| 116 | 0.01621364 | 0.01528056 | 5.75% | 2,554 | 3,831 |
| 117 | 0.01799317 | 0.01625855 | 9.64% | 2,439 | 3,612 |

Equal-period mean relative Brier improvement is **8.3911%**. Log loss improves in every period: 0.10969544→0.09819255, 0.07765314→0.07261837, and 0.08388455→0.07417823. Both models reach the training-gradient target in all folds. The weaker-penalty advantage survives the longer training procedure; it was not eliminated by letting the controls train longer.

These are 8,568 exposed development evaluation rows, including 182 enactments. The comparator is the period-specific stronger-penalty model, not the saved survivor. Periods and families are not independent trials. The 8.39% figure is neither a percentage-point accuracy gain nor proof of improvement on new bills.

## Frozen candidate

The selected procedure was fitted on 11,871 historical family representatives from Congresses 113–117, including 281 enactments. The exact pre-existing split supplies 9,496 core and 2,375 calibration cases. Core/calibration families are disjoint. Latest training-label availability is 2023-04-13T23:59:59Z. The final base reaches tolerance after 3,917 iterations, with maximum absolute gradient 9.9856e-7.

Frozen research candidate digest: `149b5f618cd74bcc1974cd502581490e8e8cb3c390baf25b9279e213bb35c0c5`.

Development result digest: `57b0c73eb88550c1b53232af4a39c31df55b84870da0c50b9a05020b79ced062`.

The candidate includes weights, scaling parameters, calibration, membership IDs, training hash, latest label date, protocol hash and freeze timestamp. It is saved separately from the original survivor and marked `release_eligible=false`, `independent_validation=false`. No 118th outcomes enter final fitting, but prior 118th results influenced the research direction, so independence must not be inferred from that exclusion. The original survivor digest remains `ffb089cff396415431c2e2b04cb99ebf7d75fe040a777da661bb58d6af9d255c`.

## Arithmetic incident and checks

The first NumPy matrix-multiplication execution emitted divide/overflow/invalid warnings despite successful scalar checks. Its artifacts are retained in `data/research-runs/convergence-20261105/`. Before accepting a candidate, reran the entire registered statistical procedure using explicit `einsum(optimize=False)` reductions and finite-weight/gradient assertions on every iteration. The accepted run is `data/research-runs/convergence-einsum-20261105/`, with the arithmetic path disclosed in its protocol. Maximum probability difference between paths is 6.94e-16; no result was selected based on which arithmetic path scored better.

35 tests passed, including scalar/vector equivalence, training-only stopping and cap handling. The complete accepted experiment and final fit replay exactly. A separate scalar verifier recalculated 34,272 evaluation probabilities, Brier/log-loss metrics, training gradients, final training membership/family separation and artifact hashes. Original 300-step probabilities reproduce within 1e-12. Optional-dependency test handling was additionally checked with the three convergence tests.

Full results and the research-only candidate receipt are saved to the platform campaign chat and API-verified. No paid calls, recurring schedule changes or production promotion. Historical publication availability, proxy-stage and family-linkage limitations remain; machine checks do not provide independent human certification.

## Next gate

Keep both artifacts frozen. Before scoring another cohort, register its candidate identities, prior-exposure/family exclusions, outcome target, sample size, minimum useful effect and uncertainty analysis. Compare candidate directly against survivor and rate baseline. Do not reuse the previously scored 118th sample as an independent test, extend a test until it wins, or retune this candidate against confirmation outcomes. If sufficiently unexposed historical evidence is unavailable, use prospective shadow forecasts and await outcomes. Better development scores alone do not authorize promotion or establish a globally optimal model.

Reproduce: `python3 -m scripts.convergence_experiment`, then `python3 -m scripts.verify_convergence` (NumPy required for the research runner). Runtime data stays ignored; reproducible code and this receipt are versioned.
