# Introduced-text training and calibration coverage expansion

November 8, 2026. Executed a bounded source acquisition before any further model testing. **200 new official introduced-bill XML documents were acquired and validated**, 50 each from Congresses 113–116, totaling 3,260,056 bytes. All 200 selected cases passed the metadata and identity checks; no replacement cases or per-bill acquisition failures occurred. No mechanism labels, model fits, outcome scores or forecasts were generated.

## Selection and timing

The run first replayed the existing E1 core/calibration memberships against the legacy forward splits and calibrated-model membership lists for evaluation Congresses 115, 116 and 117. Training labels had to be available strictly before each applicable fold's first evaluation checkpoint, and within-fold family separation was verified.

The acquisition population was the union of those existing training/calibration identities. Selection used Congress order, then canonical digest of bill ID, with at most 50 per Congress and one selected bill per automated family. All 100 original pilot identities and their families were excluded, including the held-back quality cases. Congress 117 evaluation-only cases were not selected. Bills evaluated in an earlier fold may legitimately enter a later fold's training set only through its existing dated membership; this expansion does not redefine any split.

A sealed registration, an outcome-free population snapshot and a selection-disposition ledger were written before the first HTTP request. Selection did not use outcome values or class counts. No selection changes were allowed after retrieval failures. Publication checks use existing retained MODS/PREMIS metadata: the introduced package must have a unique XML link, matching package identity, matching issuance/access bounds, and a metadata availability bound no later than the bill checkpoint. The downloaded XML must render as the exact Congress, chamber and bill number.

The runner held the shared research lease under a unique owner for the entire operation, renewed it for every case and released it on completion. No paid services or new metadata acquisition were used.

## Coverage result

“Covered” here means a retained, identity-checked **current XML rendition with dated official package metadata**, not a historically certified rendition or a completed mechanism annotation. Baseline coverage counts only eligible original **design** texts; quality text is excluded. There were 32 distinct baseline design identities across the union of training/calibration memberships, increasing to 232 with the new documents. Fold counts overlap and must not be summed as independent cases.

| Evaluation fold | Partition | Fixed population | Covered before | Newly covered | Covered after |
| --- | --- | ---: | ---: | ---: | ---: |
| 115 | Core training | 3,569 | 10 | 72 | 82 |
| 115 | Calibration | 893 | 3 | 19 | 22 |
| 116 | Core training | 5,272 | 17 | 113 | 130 |
| 116 | Calibration | 1,319 | 4 | 28 | 32 |
| 117 | Core training | 7,049 | 23 | 161 | 184 |
| 117 | Calibration | 1,763 | 6 | 38 | 44 |

**Certified historical coverage remains zero in every partition.** The sources were actually retrieved on November 8, 2026; no receipt was backdated. Official historical package dates do not prove that the newly downloaded XML bytes are identical to those available before each historical checkpoint. Automated family exclusions are not a completed human genealogy review. Source expansion alone supplies neither mechanism annotations nor adequate class coverage for fitting.

## Validation and preserved failure

Seven focused tests passed using:

```sh
python3 -m unittest discover -s tests -p test_mechanism_training_coverage.py -v
```

They cover fixed caps/order, outcome-value invariance, exclusion of pilot families, strict label timing, malformed quotas, duplicate identities, historical-certification flags, retained metadata corruption, package identity and publication cutoffs. The test added after the initial runtime failure also covers excluded discovery rows without checkpoints.

The first attempt, `mechanism-training-coverage-20261108-v1`, stopped **before registration or network acquisition** because excluded legacy discovery rows can lack `cutoff`. Its sealed failure was retained. The population projection was corrected to preserve missing excluded-row checkpoints as null; selected-case timing requirements remain strict. A fresh v2 run then executed the unchanged deterministic selection rule successfully.

Offline verification replayed the exact selection from the sealed outcome-free population, checked the disposition ledger, all 200 source receipts and retained metadata proofs, reconstructed all 200 reading views and offsets, and recomputed the coverage tables. It confirmed **370 frozen files unchanged**, including the original pilot and legacy model/fold artifacts. Quality-source preservation used byte hashing only; no quality text was rendered or inspected. Code hashes matched the registered implementation. No outcomes were needed by this offline replay.

## Artifacts

Implementation: `scripts/mechanism_training_coverage.py`; focused tests: `tests/test_mechanism_training_coverage.py`. The actual run command was:

```sh
python3 -m scripts.mechanism_training_coverage --output data/research-runs/mechanism-training-coverage-20261108-v2
```

Runtime material stays in ignored `data/research-runs/mechanism-training-coverage-20261108-v2/`, including the outcome-free selection snapshot, source packets, raw XML receipts, source-coordinate reading views and per-case dispositions.

| Artifact | Seal |
| --- | --- |
| Registration | `801dd51ca5cb3aad862e7b308fa3e91cf7192f2f9a605e29699b8a695bfd9af1` |
| Result | `703adb6c43eee67169a38acf6dbc397dbd3b79cff72a0711836ec3e0d25d892f` |
| Offline verification | `07b83360b9d7afed8d1805aa30ebd4cdbd1507ba0829748d8dd0fd53c488db8b` |

This batch expands the available source material for a separately specified annotation/extraction stage. It does not satisfy historical-source certification, authorize alteration of frozen protocols or establish predictive improvement.
