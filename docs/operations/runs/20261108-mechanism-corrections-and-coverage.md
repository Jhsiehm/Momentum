# Corrected bill representation and dated source coverage

November 8, 2026. User authorized applying the completed audit's corrections in a separate version and expanding dated training/calibration coverage before predictive testing. This batch does not fit models or change frozen research gates.

## Separate corrected representation

Two agents applied the accepted source-based changes to their original batches, then reviewed each other's correction deltas. The resulting combined design dataset contains **40 bills, 480 mechanism classifications and 501 evidence-linked effects** (previously 463). **21 bills changed**; statuses are now **205 present, 259 absent and 16 uncertain**. Retaining more uncertainty reflects source/rubric boundaries, not an accuracy result.

All 13 subset findings, 34 peer findings, the methods auditor's additional Commission sunset finding and two new consistency findings have explicit dispositions: 50 references in total, including overlapping recommendations. The additional fixes concern newly imposed sunsets in 117-s825 and 117-hr5229. These are identified as new findings, not attributed to earlier reviews. Unknown referenced law and the database/programme/appropriation boundaries remain explicit.

Each primary annotation, methods decision and source view is hash-bound. The validator checks exact quote offsets, complete population/schema, every finding reference exactly once, and that every changed bill is documented. Both peer agents checked all 20 opposite-batch records and the actual changed effects against source text; neither reported a further correction. This is reciprocal machine review, not independent human ground truth or exhaustive accuracy measurement.

The original primary files and all earlier reviews remain unchanged. A first corrected-A receipt was sealed before the added consistency-finding schema arrived; it was preserved, and the final explicit version is `corrected-agent-a-v2.json`. B's selected receipt is `corrected-agent-b.json`. No sealed output was overwritten.

Runtime: `data/research-runs/mechanism-corrections-20261108-v1/` (ignored).

- Combined corrected dataset: `041ad00ca21d623b68771d5e81e9dab8d3965f5585232fe688c8804ecb2a5a57`.
- Correction integrity audit: `c094256d1ab337b40ae363928a5f18dc48c704adef0e9abb3a025201082b87a5`.
- Corrected A v2: `6bfd96c005311bcaa6203abe5609d3d30961395668718d63440d9601889ab931`.
- Corrected B: `009dc5ddec9838d0d36b2c53008e2e999e34f0ab6a2c0fc233748e82b39d67ad`.

Reproduce the integrity audit and combined dataset with:

```sh
python3 -m scripts.mechanism_corrections_audit data/research-runs/mechanism-rubric-v2-20261108 data/research-runs/mechanism-corrections-20261108-v1 --a-file corrected-agent-a-v2.json
```

## Coverage design and limits

The expansion is fixed before downloading: up to 50 bills per Congress 113–116, ordered by canonical bill-ID digest within Congress, selected only from the union of unchanged legacy core/calibration memberships. Exclude all 100 original pilot identities and their known families, including the protected quality partition; enforce global selected-family uniqueness. Selection does not use outcome values and failures do not trigger replacement. Existing automated family assignments remain provisional.

The evidence workflow resolves retained official MODS/PREMIS metadata, checks publication bounds against each feature cutoff, verifies label-availability ordering for existing training roles, follows the introduced XML link and checks exact bill identity. Current downloaded bytes retain their actual retrieval times. Dated metadata does not establish archived historical byte identity, so certified historical coverage remains zero. Earlier-fold evaluation identities may appear as later-fold training in the unchanged rolling design; this is exposed development evidence, not a new independent evaluation set.

The first run stopped before registration or network activity because some excluded population rows lack a checkpoint. That failure is preserved in `mechanism-training-coverage-20261108-v1/failure.json`. The snapshot projection was corrected to retain missing excluded-row dates as null, while selected-row timing remains mandatory. A fresh v2 directory preserves the failed run and registers the unchanged selection before acquisition.

## Actual expansion and readiness result

Acquired and validated **200/200 new introduced XMLs**, 50 each from Congresses 113–116, with **zero failures and 3,260,056 source bytes**. Runtime: `data/research-runs/mechanism-training-coverage-20261108-v2/`. Registration `801dd51ca5cb3aad862e7b308fa3e91cf7192f2f9a605e29699b8a695bfd9af1`; result `703adb6c43eee67169a38acf6dbc397dbd3b79cff72a0711836ec3e0d25d892f`.

Baseline counts below use all previously acquired design texts intersecting the training union (32 unique bills), including v1 design cases. This differs from the prior readiness table restricted to the 40 v2 design cases. Counts are fold-specific memberships; do not sum them as distinct bills.

| Fold | Core XML coverage before → after | Calibration XML coverage before → after | Recorded positives after: core / calibration |
| --- | ---: | ---: | ---: |
| 115 | 10 → 82 | 3 → 22 | 1 / 0 |
| 116 | 17 → 130 | 4 → 32 | 1 / 0 |
| 117 | 23 → 184 | 6 → 44 | 2 / 0 |

Root computed class counts only after acquisition and selection were sealed, using already-exposed labels. No resampling or selection changes followed. Class-readiness receipt: `eab6921cbf36faaca469633ecd6d4a9da0818bd6da9785610100a4feece8fdb1`.

**Every calibration subset still lacks positive outcomes.** More raw text has improved source coverage but has not resolved calibration readiness. New texts have no mechanism annotations yet, and no frozen extractor has been validated. Historical source/label/family certification also remains incomplete. Therefore no predictive comparison was attempted, no model learned new weights, and no improvement or 60% claim is supported. Further expansion should use a prespecified broader natural population with dated evidence, not outcome-selected evaluation cases. Preserve unknowns in corrected features and separately validate the extractor before fitting.

## Final validation

Twenty-one focused tests passed across correction integrity, coverage selection/metadata, v2 annotations, v1 audit and text rendering. Independent code review found no substantive issue within the selection, timing, cap and quality-family exclusion checks. Root verified both correction peer receipts and all 384 original pilot/semantic-study files plus the unchanged frozen model audit. No full regression-suite rerun is claimed.

Offline coverage replay reconstructed all 200 views and source receipts, selection/ledger and coverage tables, confirming370 coverage-run frozen files unchanged (overlaps the384-file preservation check). Registered acquisition implementation hashes remain unchanged. Root added a reusable offline verifier with explicit checks, including result/registration and source-packet identity bindings, and replayed successfully in normal and optimized Python. Verification seal: `07b83360b9d7afed8d1805aa30ebd4cdbd1507ba0829748d8dd0fd53c488db8b`.

```sh
python3 -m scripts.verify_mechanism_training_coverage data/research-runs/mechanism-training-coverage-20261108-v2
```

[Detailed acquisition receipt](20261108-mechanism-training-coverage.md). Runtime sources, annotations, receipts and intermediate failures stay ignored under data/. Shared lease released; original protocols and scheduler settings preserved.
