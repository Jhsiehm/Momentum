# Independent synthetic text-pipeline review

Date: 2026-11-08. Reviewer: separate AI agent assigned adversarial review. This is software review, not qualified human source, family, outcome or semantic certification.

## Scope and outcome

Reviewed `scripts/matched_text_preprocessing_v1.py` and `scripts/matched_text_sparse_v1.py` directly, and independently authored `tests/test_matched_text_pipeline_independent.py`. No actual bill documents, legislative outcomes, protected quality cases or predictive scores were read. All twelve independent tests passed in normal and optimized Python. This review precedes the fixed synthetic integration run; that run's frozen hashes and actual results belong in its execution receipt.

The first attempted test run failed on import because the preprocessing manifest contained duplicate `idf` keyword arguments (formula and values). The implementing agent changed the formula key to `idf_formula` before registration. The failure and correction are retained here; no failed registered run was replaced. No further material defect was found in the reviewed implementation.

## Independent cases

| Case | Direct checks | Result |
| --- | --- | --- |
| Substantive language and citations | Negation, substantive “approved,” official-title language, U.S.C. reference and a different bill reference survive; administrative action and focal bill identity are masked | Pass |
| Structural and mask boundaries | Neither adjacent table cells nor the sides of a masked identity create a bigram | Pass |
| Unicode mapping | Decomposed accented source and emoji remain unchanged; NFC tokens normalize the accent; every segment slices the exact original text; no token-offset claim | Pass |
| Vocabulary and IDF isolation | Six core documents; terms in five survive; a term in all six and a singleton do not; exact smoothed IDF; evaluation-exclusive token creates no column; evaluation transformation and repeat fit cannot mutate state | Pass |
| Membership and empty vocabulary | Calibration/evaluation roles rejected; a corpus with no eligible vocabulary rejected | Pass |
| Deterministic columns | Reversing core document order preserves vocabulary, IDF and transformed numeric values | Pass |
| Fraction boundaries | Full fraction context stays in source text; fraction boundaries prevent invented `41` and `NW1` tokens without numeric inference | Pass |
| Objective and intercept | Three finite-difference derivatives within absolute 1e-9; direct scalar NLL agrees with slope penalty; intercept derivative has no L2 term | Pass |
| False optimizer success | Mocked successful optimizer at nonstationary parameters rejected by recomputed gradient | Pass |
| Sparse operation | Fit on four rows and 10,001 columns succeeds with CSR `toarray` patched to raise | Pass |
| Numerical equivalence | Independently coded dense gradient descent reaches max gradient 1e-9; sparse-fit parameters agree within absolute 3e-5 and objective to ten decimal places | Pass |
| Invalid labels and text norm | Single-class, nonbinary, boolean and nonfinite outcomes rejected; unnormalized sparse text rejected | Pass |

The solver uses stable signed-logit NLL and residuals, canonicalizes a copy of the CSR input, and requires both optimizer success and a finite independently recomputed maximum absolute gradient no greater than 1e-6. Text is appended without centering or variance scaling. These are computational guarantees for supplied arrays, not evidence about real data eligibility.

## Limits and remaining checks

The APIs rely on callers to supply core membership and authentic prepared documents. The vocabulary utility accepts minimal versioned token records and caller-supplied roles; those fields alone cannot certify historical availability or prevent a dishonest/mistaken caller from mislabelling evaluation data as core. Real execution requires the independent frozen population and provenance gates.

The tokenizer is a specified Unicode alphanumeric pattern after NFC and lowercasing, not a linguistic parser. Segment-level original coordinates are preserved; normalized token coordinates are deliberately unavailable. Fractions and merged table cells are not assigned mathematical interpretations. Administrative tags found within substantive bill body fail closed rather than silently removing substantive language.

The sparse check prevents the usual CSR `toarray` path and code inspection found no dense matrix conversion; it is not a measured production memory benchmark. The six-row independent numerical fixture does not establish convergence on every future matrix. The tests use shared NumPy/SciPy and XML infrastructure, so independent authorship is not complete implementation diversity. No timing, cost, predictive accuracy, calibration adequacy or historical source eligibility was measured.

Reproduction:

```sh
python3 -m unittest tests.test_matched_text_pipeline_independent
python3 -O -m unittest tests.test_matched_text_pipeline_independent
```

No predictive model comparison occurred. Small synthetic optimization fixtures are numerical software verification only. Historical-source, review, matched-population and predictive-registration gates remain closed.

## Integration harness pre-run review

Direct inspection of `scripts/run_matched_text_synthetic_v1.py` found three pre-registration improvements: enforce the positional role order as well as role counts; check cross-cell bigrams in every prepared segment before vocabulary filtering (ubiquitous terms can otherwise be removed by max-DF, concealing a boundary defect); and report the actual gradient-descent update count at the iteration cap. These were sent to the harness author before execution and their corrections were confirmed by direct inspection before registration. The revised guard checks prepared streams directly and verifies the holdout challenge and substantive negation were not erased. The reviewed harness declares exactly three synthetic L-BFGS optimizations and one capped scalar GD reference, freezes inputs/code before preparation, and does not score real forecasts. Post-run verification is recorded below when available.

## Registered failure and successor

The v1 integration run completed its three synthetic optimizations and scalar GD reference, then failed to serialize a NumPy boolean into the sealed final result. Its registration, prepared documents, vocabulary, fits and explicit failure record remain intact. The separately registered v2 changes only serialization of the scalar objective error and boolean checks, plus version/registration/failure bindings. Two independent regression tests in `tests/test_matched_text_synthetic_runner_v2.py` passed normally and under optimized Python before v2 registration: native/NumPy booleans preserve truth values through sealing, while nonboolean values cannot be coerced into verdicts. The combined registered execution count is six synthetic L-BFGS optimizations and two scalar GD references; unit-test optimizations are separate software checks.

## Post-run independent recomputation

The successor result passed all ten declared checks. The independent verifier loaded only sealed synthetic outputs and synthetic fixture/configuration inputs, imported no production preprocessing or solver functions, and ran no further optimization. It checked all 21 registered code/input bindings, all 28 prepared document segment offsets and cell boundaries, and recomputed the exact 22-term vocabulary/IDF from core document counts. Independently rebuilt text rows match reported sparse shapes/nonzero counts, and scalar core means/scales match the saved scaler. Prepared documents, vocabulary and fitted artifacts are exactly identical across v1 and v2. The original failure seal also validates.

| Saved synthetic fit | Independently recomputed objective | Maximum absolute gradient | Objective difference | Gradient-norm difference |
| --- | ---: | ---: | ---: | ---: |
| Two-column numerical fixture | 0.36673261497839726 | 4.104748541969294e-7 | 0 | 6.245004513516506e-17 |
| Six-column synthetic anchor | 0.21667308570894522 | 1.4484417708640618e-7 | 0 | 1.387784074737366e-18 |
| Anchor plus synthetic text | 0.17675555209637234 | 2.928378050643006e-7 | 2.7755575615628914e-17 | 2.6020852139652106e-18 |

Normal and optimized Python produced identical independent-verifier results. These are training-objective numerical checks on invented examples, not forecast losses or evidence that text improves real predictions. No real-bill model comparison was performed.

Ignored runtime evidence is under `data/research-runs/matched-text-synthetic-v2-20261108/`:

- `independent-review.json`: seal `b1c072111ecc49418ed8ecfb4435d737f07d947b95a89430b7a3e6299d8ee732`.
- `independent-replay.json`: seal `5054811252f8519059f072cdbabb5340057030ca90ca485b5b9f5d12e282f504`.
- `independent_verify.py`: byte SHA-256 `dfeea395695e740140931ee076289673cb4f9c0141307c149a6389aaf2708f05`.

Read-only reproduction (does not fit models):

```sh
python3 data/research-runs/matched-text-synthetic-v2-20261108/independent_verify.py
python3 -O data/research-runs/matched-text-synthetic-v2-20261108/independent_verify.py
```
