# Independent review: retrospective text diagnostic

November 8, 2026. Independent agent software and numerical review; no qualified human source/outcome certification. Original forecasting gates remain unresolved. No optimization or additional model fitting was performed by this review.

## Pre-fit review

The reviewer inspected the separate protocol and runner before registration. The review identified and the implementation addressed four issues before any real fit: membership chronology was checked only after label loading; bootstrap inputs lacked explicit empty-partition/draw-count checks; a duplicate historical identity could silently overwrite an outcome row; the new synthetic test file needed inclusion in registered bindings. The runner now checks source identity/Congress during membership selection, rejects invalid bootstrap inputs, rejects duplicate historical rows and invalid selected labels, and binds the test file as an input. The root also discovered that legacy rows lack a separate stage field and derived stage from the existing first feature using its original scale; the reviewer checked that scale against `engine/cohort.py`.

Fifteen independently authored synthetic tests passed normally and under optimized Python, each observed at 0.012 seconds. Tests cover ordered core/calibration merging, source intersection, pilot family exclusion, duplicate identities/families, cross-role family overlap, chronology, scalar metrics, class/bin boundaries, invalid values, shared-family bootstrap weights, reproducibility and invalid-draw suppression. An intermediate test fixture omitted the newly required Congress field, causing eight fixture errors; the fixture was corrected before registration. These tests did not read real outcomes or fit models.

Code inspection confirmed registration precedes document preparation, final paired memberships precede label loading, vocabulary/scaling use only the merged training partition, and both arms/references use the same ordered evaluation identities. The source-conditioned population and deliberate absence of calibration are explicit, separate from E3. This is inspection of execution logic, not proof that underlying source timestamps or family labels are correct.

## Independent post-fit replay

The ignored verifier independently reconstructed term counts, document frequencies, ranked vocabularies, IDF values, normalized sparse matrices, structured means/scales, objectives, gradients and predictions from saved inputs and coefficients. It did not call the fitting function. It separately recomputed training-rate/stage references, losses, expected events, class-specific losses, reliability bins, equal-fold aggregates, skill ratios and all 10,000 paired global-family bootstrap draws.

The review verified registered code/input hashes and parent seals, all 1,186 prepared-document identities/hashes, the nine preparation exclusions, and the exact candidate-to-final population mapping. There are 1,195 unique candidate identities across fold memberships, drawn from 1,200 nonpilot source documents. These counts must not be conflated. Evaluation has 595 distinct rows, each with two model probabilities (1,190 total), plus two reference probabilities. Both fold text vocabularies have 10,000 terms.

| Fold | Arm | Training rows | Columns | Recomputed penalized objective | Maximum absolute gradient | Maximum probability discrepancy |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 115 | Anchor | 540 | 6 | 0.08526247336785929 | 8.920214521201952e-8 | 0 |
| 115 | Text | 540 | 10,006 | 0.08461560337607209 | 3.5334635034258615e-7 | 2.0816681711721685e-17 |
| 116 | Anchor | 843 | 6 | 0.08317113722528571 | 5.931765137429795e-7 | 0 |
| 116 | Text | 843 | 10,006 | 0.08260902285050005 | 8.547038135922613e-8 | 5.551115123125783e-17 |

All checked values matched at absolute tolerance `1e-12`; all recomputed gradients meet `1e-6`. The bootstrap replay matched all three intervals and the reported 10,000 valid/zero invalid draws. This verifies computation, not significance or independent generalization.

The first verifier invocation used an incorrect `runpy` command and failed before running the verifier. The corrected command below succeeded. No result artifact was silently replaced and no model refit occurred.

## Evidence and reproduction

Runtime directory: `data/research-runs/retrospective-text-diagnostic-v1-20261108/`.

- Registered result: `result.json`, seal `71dadbbacbc20523bdf8a6c0e5ade90daec5fa1716edcab6af559ac9ca63b369`.
- Independent review: `independent-review.json`, seal `e8d10cc275193e82cc2042633b5be30c46485cf15ab3bac72ce3bc1426d304ae`.
- Independent verifier: `independent_verify.py`, SHA-256 `6bfa2a6f3593b815538436ddd7c7a6c721314e0d209b0c6fdf86fa819a368bad`.
- Synthetic tests: [test_retrospective_text_diagnostic_v1.py](../../../tests/test_retrospective_text_diagnostic_v1.py).
- Frozen protocol: [retrospective diagnostic](../RETROSPECTIVE_TEXT_DIAGNOSTIC_V1.md).

Executed from repository root:

```sh
python3 -m unittest tests.test_retrospective_text_diagnostic_v1
python3 -O -m unittest tests.test_retrospective_text_diagnostic_v1
PYTHONPATH=. python3 data/research-runs/retrospective-text-diagnostic-v1-20261108/independent_verify.py
```

The verifier writes its result once; preserve that receipt rather than rerun over an existing output. A later replay should use a separately versioned receipt destination.

## Remaining limits

Review covered every saved model prediction and numerical result, not a sample. It did not independently re-adjudicate bill outcomes, correct the provisional family graph, certify historical source availability, inspect protected quality text, or establish source representativeness. Prepared-document seals establish consistency with saved artifacts, not semantic correctness of every mask or a new source-custody certification. The earlier synthetic preprocessing review remains software evidence only. Sparse event counts, source selection, exposed development periods and no calibration limit interpretation. No model promotion, deployment, confirmatory gain or achievement of the 60% target follows from this audit.
