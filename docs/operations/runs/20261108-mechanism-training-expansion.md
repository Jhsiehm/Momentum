# Fixed 1,000-bill training-source expansion

November 8, 2026. Completed the authorized larger source corpus before further testing: **1,000 new introduced-bill XML documents**, 250 from each Congress 113–116, totaling **16,052,288 bytes**. All selected cases passed identity and metadata checks; no source failures or replacement cases occurred. The existing 232 validated source identities were retained, bringing the union to **1,232**. This is source coverage, not completed semantic annotation or historical certification.

## Fixed selection and bounded cycles

The new runner, `scripts/mechanism_training_expansion_v2.py`, leaves the earlier hashed acquisition implementation unchanged. It validated all 232 baseline sources and reconstructed the original core/calibration splits before selecting from their union. It excluded all 100 pilot identities and their automated families, plus all 200 identities selected by the previous acquisition and their families. The quality texts were not opened.

Selection used ascending Congress, then canonical digest of bill ID, with a fixed maximum of 250 per Congress and one selected bill per automated family. It did not use outcome values or class counts. No quota or selection adjustment was permitted in response to retrieval success or later class diagnostics. Congress 117 evaluation-only cases were excluded; earlier evaluation identities can enter later training only through the existing dated legacy memberships.

The overall selection and **ten cycle registrations, each capped at 100 bills**, were sealed before HTTP acquisition. Each cycle's records, source bytes, exact identity renderings and frozen-file preservation were replayed before its result was sealed and the next cycle began. This follows the bounded-cycle acquisition rule without redefining the frozen experiment plan. The 1,000-case programme is a separate source-preparation registration, not permission to run 1,000-case model searches.

The runner used a unique shared research lease, renewed it for each case, and released it after successful completion. Its six-hour global deadline bypasses HTTP transport retry handling. Per-case source failures would have been retained without replacement; global integrity, lease or deadline failure would have aborted with a separate receipt. The run completed normally with exit code zero.

## Coverage before and after

Coverage means a current XML rendition whose official package metadata supports availability before the historical bill checkpoint, with matching Congress/chamber/bill identity. It does **not** prove that the current bytes are the original historical rendition. Dated label availability and family-separated legacy membership were checked for every selected training role. Fold counts overlap and must not be summed as independent bills.

| Evaluation fold | Partition | Fixed population | Before | Newly covered | After |
| --- | --- | ---: | ---: | ---: | ---: |
| 115 | Core training | 3,569 | 82 | 361 | 443 |
| 115 | Calibration | 893 | 22 | 92 | 114 |
| 116 | Core training | 5,272 | 130 | 563 | 693 |
| 116 | Calibration | 1,319 | 32 | 144 | 176 |
| 117 | Core training | 7,049 | 184 | 786 | 970 |
| 117 | Calibration | 1,763 | 44 | 192 | 236 |

**Certified historical sources: zero. Mechanism labels created: zero. Models fitted: zero. Outcomes scored: zero.** Real retrieval timestamps remain November 8, 2026. Neither successful current downloads nor official historical package dates certify historical byte identity. Automated family screening does not constitute reviewed genealogy. These convenience-sample coverage counts establish neither adequate class balance nor predictive gain.

## Verification

Eight focused tests passed:

```sh
python3 -m unittest discover -s tests -p test_mechanism_training_expansion_v2.py -v
```

Tests cover the 1,000-case cap, fixed digest ordering, outcome-value invariance, earlier selected-family exclusion, no cross-Congress quota filling, strict timing, malformed membership/exclusion bindings, cycle sizes/complete ordering, completed-source replay, false certification claims, source corruption, blocked-case accounting and the nonretryable global deadline.

The built-in offline replay then verified the sealed outcome-free population and selection ledger, all 1,000 source records/metadata proofs/reading views, all 232 baseline sources, cycle memberships and record hashes, coverage arithmetic, and registered implementation hashes. It confirmed **1,375 frozen files unchanged**. The source-only verifier reads no outcome values and does not render quality texts. Earlier hashed scripts were not modified.

Independent review identified omitted result-field checks. Root completed a separate supplemental verifier outside the registered runner, with adversarial tests and successful normal/optimized replay. The built-in receipt does not substitute for that check. See the [combined readiness receipt](20261108-large-training-corpus.md) for the supplemental seal and subsequent class counts.

## Reproduction and artifact identities

Actual command:

```sh
python3 -m scripts.mechanism_training_expansion_v2 --output data/research-runs/mechanism-training-expansion-20261108-v1
```

Offline replay, with no network acquisition:

```sh
python3 -m scripts.mechanism_training_expansion_v2 --output data/research-runs/mechanism-training-expansion-20261108-v1 --verify-only
```

Runtime sources and artifacts remain under ignored `data/`.

| Artifact | Seal |
| --- | --- |
| Registration | `e7cf38e5576d9dc385dae8a74b8d5a8d214e1e3a398539147775f06ab130fc43` |
| Result | `82448ebb873ad95ca72ef6972ecf8591b61e608feeb46a11084ebb6ebfe28528` |
| Built-in offline verification | `e5f7080e055960ab0cd3c18fa87c392fdf56bab498833183bca5b9efa0b32d72` |

No selection changes were made after registration. Postselection class-readiness analysis, if performed by the coordinating reviewer, is a separate receipt and cannot alter this completed sample.
