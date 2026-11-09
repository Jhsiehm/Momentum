# Matched-text preprocessing and sparse numerical preflight — 2026-11-08

## Outcome and scope

The separately versioned synthetic successor passed all ten engineering checks. A first registered run completed its three numerical optimizations but failed final JSON serialization; that registration, fitted outputs and failure remain preserved. The successor changes result serialization only. No real bill text, bill outcomes, forecasting fits, calibration fits or predictive evaluation occurred.

Question: can the specified E3 text representation be fitted on core only, retain source context, respect structural boundaries and feed the exact sparse logistic objective with independently verified gradients? This is synthetic software validation, not a new model-effectiveness study. Labels and predictors are deliberately constructed (including a direct synthetic class signal); their losses cannot estimate legislative prediction performance.

## Versioned definitions and frozen inputs

- New preprocessing `matched-text-preprocessing-v1`: NFC then lowercasing; Unicode alphanumeric tokens without underscores; unigrams/bigrams within source segments only. Block, table-cell, fraction/mfrac and mask boundaries prevent joined bigrams. Full source text stays unchanged; segment bounds map to original Unicode coordinates, with no claim of normalized token offsets.
- Mask explicit administrative subtrees outside legis-body and exact focal bill identifiers. Preserve official title, substantive status words, negation, other bills and statutory references. Ambiguous administrative nodes inside substantive body reject. Fractions keep their literal text and separate token boundaries; no arithmetic value is inferred.
- TF-IDF: raw counts; IDF `log((1+n_core)/(1+df))+1`; minimum 5 core documents, maximum 95% core frequency, maximum 10,000 terms; rank by descending core term count with lexicographic ties and lexicographic columns. L2 normalization; no stemming, generic stopwords, embeddings or text-column standardization.
- Sparse solver `matched-text-sparse-v1`: mean logistic NLL plus `.025*sum(slopes²)`, unpenalized intercept; zero-initialized unbounded L-BFGS-B, maxiter=20,000, gtol=1e-6, ftol=0, maxfun=1,000,000, maxls=50, maxcor=10. Both optimizer success and a separately recomputed finite gradient≤1e-6 are required; no retry or fallback. The [SciPy 1.13.1 documentation](https://docs.scipy.org/doc/scipy-1.13.1/reference/optimize.minimize-lbfgsb.html) distinguishes its stopping options; optimizer success alone is not the acceptance check.
- Six structured columns use core-only population standard deviations, floor 0.1; sparse TF-IDF remains uncentered/unstandardized. Installed NumPy 2.0.2 and SciPy 1.13.1 were used, pinned in `requirements-research-text-v1.txt`; no dependency installation or production dependency change.

[Exact preprocessing specification](../../research/MATCHED_TEXT_PREPROCESSING_V1.md). These definitions supplement rather than rewrite the frozen matched-comparison specification. Caller-provided roles and prepared documents still require an authenticated execution population; a role string is not source eligibility evidence.

The fixed committed [fixture manifest](../../../tests/fixtures/matched_text_synthetic_v1.json) contains 28 invented documents: 20 core, 4 calibration, 4 evaluation; all canonical-looking bill IDs are synthetic fixture identifiers. There is also one fixed 6-row/2-column numerical case. Calibration/evaluation documents are transformed only, with deliberate holdout-only tokens. Every row, label, structured value and source fragment is in the manifest. No sampled bills, substituted cases or outcome-guided selection.

## Registered failure and successor

| Artifact | Seal |
|---|---|
| First registration | `e36a2bf5f99deda1b637f1ef76adbfbc43dc2070ed3a022e5849f2c008384c46` |
| First failure | `a8151e163ddd9cac86a87405e14238ccb1e1c0f76639ce25f647cb1b6f7a017a` |
| Successor registration | `decabe73d83b03a540bc5d35563d6463cf6b504f7a45513badff17a3f7d3f5c8` |
| Successor result | `74bbad2dc851db8d8be0f7bcd89e15190aef92fb8a6449b8cec2043eb3a62476` |
| Vocabulary | `ed006b9019c87f4724f158b57e8b0093ada50b8f1e229883220dbe45a6a1f151` |
| Synthetic fits | `ec4cbca945b7f1e03d562556d322462215c0614a11208c3fc1ab9e9dc89ed428` |

The first run failed at final result serialization: a NumPy Boolean was not JSON-serializable. `run_matched_text_synthetic_v2.py` converts check values to native Booleans and the scalar objective error to native float, binds the previous failure and otherwise retains all fixtures, algorithms, tolerances and solver settings. Regression tests verify serialization preserves truth and rejects nonboolean values. Prepared-document, vocabulary and fitted-output seals are identical between runs. No numerical tuning occurred after results.

Each registered run executed three L-BFGS optimizations and one scalar gradient-descent reference. Across both registered runs: **six synthetic L-BFGS optimizations and two scalar GD references**. Unit tests additionally exercise synthetic optimizations; these are software checks, not the six proposed real-data E3 fits. All real-data fit counts remain zero.

[Failed run](../../../data/research-runs/matched-text-synthetic-v1-20261108/failure.json), [successor registration](../../../data/research-runs/matched-text-synthetic-v2-20261108/registration.json), [result](../../../data/research-runs/matched-text-synthetic-v2-20261108/result.json). Runtime prepared inputs, vocabulary, fitted coefficients and validation evidence remain ignored locally.

## Numerical results

| Check | Observed | Frozen tolerance |
|---|---:|---:|
| Scalar vs sparse objective error | 0 | ≤1e-12 |
| Scalar vs sparse gradient error | 0 | ≤1e-12 |
| Central finite-difference gradient error | 2.5991743479725216e-11 | ≤1e-7 |
| Scalar GD final max gradient | 9.983625539981371e-7 | ≤1e-6 |
| Sparse vs scalar-GD prediction max difference | 1.7706698609148974e-6 | ≤1e-4 |

The scalar GD reference used 1,267 updates (minimum 300, cap 20,000); finite differences used step 1e-6 at the fixed manifest parameters. Reference predictions concern six invented numerical rows only.

| Synthetic optimization | Rows | Columns | Nonzeros | Iterations | Objective calls | Penalized training objective | Final max gradient |
|---|---:|---:|---:|---:|---:|---:|---:|
| low_dimension | 6 | 2 | 10 | 9 | 10 | 0.36673261497839726 | 4.1047485425937946e-07 |
| synthetic_anchor | 20 | 6 | 76 | 8 | 9 | 0.21667308570894522 | 1.4484417708779396e-07 |
| synthetic_anchor_plus_text | 20 | 28 | 296 | 10 | 11 | 0.17675555209637231 | 2.9283780506690268e-07 |

These three accepted numerical fits are not model-comparison efficacy results. The engineered class signal makes training loss differences uninterpretable for real-world performance. No evaluation-set loss or calibrated score was computed.

## Representation and every synthetic document

The core vocabulary has 22 terms. Sparse text matrices: core 20×22 with 220 nonzeros; calibration 4×22 with 40 nonzeros; evaluation 4×22 with 40 nonzeros. Combined structured+text matrices have 28 columns. Heldout-only tokens remain outside the vocabulary, transforming heldout documents does not alter IDF/scaling, and cross-cell `red blue` is absent from the prepared segment stream before vocabulary filtering. Negation survives.

| Fixture ID | Role | Synthetic label | Masks | Token segments | Tokens |
|---|---|---:|---:|---:|---:|
| synthetic-core-00 | core | 0 | 4 | 8 | 26 |
| synthetic-core-01 | core | 1 | 4 | 8 | 26 |
| synthetic-core-02 | core | 0 | 4 | 8 | 26 |
| synthetic-core-03 | core | 1 | 4 | 8 | 26 |
| synthetic-core-04 | core | 0 | 4 | 8 | 26 |
| synthetic-core-05 | core | 1 | 4 | 8 | 26 |
| synthetic-core-06 | core | 0 | 4 | 8 | 26 |
| synthetic-core-07 | core | 1 | 4 | 8 | 26 |
| synthetic-core-08 | core | 0 | 4 | 8 | 26 |
| synthetic-core-09 | core | 1 | 4 | 8 | 26 |
| synthetic-core-10 | core | 0 | 4 | 8 | 26 |
| synthetic-core-11 | core | 1 | 4 | 8 | 26 |
| synthetic-core-12 | core | 0 | 4 | 8 | 26 |
| synthetic-core-13 | core | 1 | 4 | 8 | 26 |
| synthetic-core-14 | core | 0 | 4 | 8 | 26 |
| synthetic-core-15 | core | 1 | 4 | 8 | 26 |
| synthetic-core-16 | core | 0 | 4 | 8 | 26 |
| synthetic-core-17 | core | 1 | 4 | 8 | 26 |
| synthetic-core-18 | core | 0 | 4 | 8 | 26 |
| synthetic-core-19 | core | 1 | 4 | 8 | 26 |
| synthetic-calibration-00 | calibration | 0 | 4 | 8 | 28 |
| synthetic-calibration-01 | calibration | 1 | 4 | 8 | 28 |
| synthetic-calibration-02 | calibration | 0 | 4 | 8 | 28 |
| synthetic-calibration-03 | calibration | 1 | 4 | 8 | 28 |
| synthetic-evaluation-00 | evaluation | 0 | 4 | 8 | 28 |
| synthetic-evaluation-01 | evaluation | 1 | 4 | 8 | 28 |
| synthetic-evaluation-02 | evaluation | 0 | 4 | 8 | 28 |
| synthetic-evaluation-03 | evaluation | 1 | 4 | 8 | 28 |

## Validation, review and preservation

All 34 focused tests passed normally and under optimized Python. The full suite passed **626 tests in 80.218 seconds**. Before registration, review caught a duplicate `idf` keyword import failure, positional role-order checking, a potentially vacuous bigram check after vocabulary filtering, and a GD iteration-cap counter issue; all were corrected before the first registration. The post-registration serialization failure is recorded separately above.

The [independent agent review](../../research/reviews/20261108-text-pipeline-review.md) covers twelve adversarial cases and two serialization regressions. Its post-run verifier used standard-library scalar recomputation without importing the preprocessing/solver implementations or running further optimization: all 21 successor bindings, 28 documents, 22 vocabulary terms, IDF/scaling, matrix counts and three fitted objectives/gradients matched (maximum numerical discrepancy 6.245004513516506e-17). Normal and optimized replays agree. This is AI software review, not human source certification; shared XML/numerical infrastructure and synthetic-case coverage remain limitations.

Root separately verified 39 registration bindings across both runs and all **696** previously inventoried files; none changed. The frozen-model audit is unchanged and the research lease was released.

| Final evidence | Seal |
|---|---|
| Independent review | `b1c072111ecc49418ed8ecfb4435d737f07d947b95a89430b7a3e6299d8ee732` |
| Independent replay | `5054811252f8519059f072cdbabb5340057030ca90ca485b5b9f5d12e282f504` |
| Preservation after | `82cdf8d57381fde02369ae113046966863431c0dc8601a2cb550f1d6ea4a3ab7` |
| Validation | `44463d049d225e4ac883dd57535774d8e7da2562981dfd999072498943a8e646` |

[Validation evidence](../../../data/research-runs/matched-text-synthetic-v2-20261108/validation.json), [preservation](../../../data/research-runs/matched-text-synthetic-v2-20261108/preservation-after.json), [independent review evidence](../../../data/research-runs/matched-text-synthetic-v2-20261108/independent-review.json). Runtime evidence links require the local ignored artifacts; committed code, fixtures and summaries remain public. No experiment-wide elapsed time or monetary cost was measured.

## Reproduction

```sh
python3 -m unittest tests.test_matched_text_preprocessing_v1 tests.test_matched_text_sparse_v1 tests.test_matched_text_pipeline_independent tests.test_matched_text_synthetic_runner_v2
python3 -O -m unittest tests.test_matched_text_preprocessing_v1 tests.test_matched_text_sparse_v1 tests.test_matched_text_pipeline_independent tests.test_matched_text_synthetic_runner_v2
python3 -m scripts.run_matched_text_synthetic_v2 --output data/research-runs/matched-text-synthetic-v2-20261108
```

The runner command reproduces three synthetic optimizations and one GD reference and compares immutable outputs. It does not fit bill outcomes. The failed v1 remains reproducibly failed; do not edit it or overwrite its registration.

## Remaining limits

These fixtures validate the declared behavior only. Full real-source masking quality, source availability, qualified reviews, positive-family scope, temporal/family separation, eligible matched rows, actual class coverage/runtime and complete execution registration remain unresolved. The frozen previous gate report is unchanged; synthetic success does not certify its gates. No historical eligibility, legal semantic accuracy, predictive gain, self-learning deployment or 60% claim follows. The historical evidence-request packet remains local and unsent.
