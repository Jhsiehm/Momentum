# Independent agent verification — 2026-11-05

This review independently checks the live agent batch against retained real evidence. It is software and artifact integrity verification, not independent human certification or scientific validation. No new real outcomes were scored, models fitted or frozen research artifacts changed.

## Packet verification

The four focused tests in `tests.test_paper_review_packet` passed. A separate verification script recomputed canonical JSON SHA-256 directly with Python `hashlib` and `json`, independently sorted the original 11,871 training records, and confirmed all 12 selected identities and their order. It compared each exported identity, Congress, family, introduction, checkpoint, feature vector, version identity/stage/date, feature-use flag, availability basis and introduction review against the original row. All original versions and source references were retained.

All **40 unique raw evidence files and 40 sidecar receipts** passed independent URL, raw checksum, byte-count and sidecar checksum checks. Protocol and packet seals, source-code hash and training-file hash matched. Re-running the exporter returned the identical envelope and left every existing JSON file in its output directory byte-identical. The frozen-artifact audit returned identical results before and after replay.

- Packet hash: `5d4f1fe361e9efe466b9850bd671ba836c61cc0f6285a619378abf780d3fc8e1`.
- Protocol hash: `38d34f93dc2e2f03980e2443b37f7e3226ddf7045ea18591bd1392686eb9a69e`.
- Runtime directory: `data/research-runs/live-paper-review-20261105/` (ignored).

The packet omits structured outcomes and predictions and leaves all human reviews pending. Source documents remain original retrospective evidence and can themselves contain later legislative history. The packet is not a blind outcome-custody bundle. No claim of historical byte-identical availability follows from retained-byte replay. `feature_review_ready=true` means the bounded evidence is assembled for review; `human_certified`, `release_eligible` and `independent_validation` all remain false.

## Independent reproduction of agent findings

Executed the reproduction scripts embedded in both the source and methods audit notes successfully. Source replay confirmed 40 files totaling 4,376,740 bytes, 14 publication-version availability bounds, the 12 eligible-package sets, and pending human introduction review. Methods replay confirmed saved training/model membership hashes, chronological boundaries, 12,749 eligible versions with human introduction review still pending, and the reported exposed-period memberships. These checks read already exposed labels and saved predictions where documented; they do not calculate new performance results.

No material defect was found in the bounded exporter. Its intentionally narrow role does not resolve source certification, parser-version association, family completeness, inventory completeness, outcome custody or prospective issuance. Fresh clones require the retained acquisition bundle to reproduce the real-evidence checks.

## Exposure-gate correction and verdict

Inspected the resulting change to `engine/paper_evaluation.py`: registration now requires an exposure registry with unique nonempty string identities, a scope and a review; preparation verifies the review subject and evidence bytes, then rejects any selected bill identity or family overlapping the declared exposed development population before producing predictions. The synthetic fixture explicitly declares its empty exposure population. The gate verifies declared membership and attestations; it cannot establish that the declared population or family graph is complete, or authenticate a named reviewer's qualifications. Those remain external review responsibilities. The unconditional prospective scoring block remains intact.

Independently ran `python3 -m unittest tests.test_paper_review_packet tests.test_paper_evaluation -v`: **20 tests passed**, including missing exposure registry, bill and family intersections, tampered review, exact replay and independent Decimal arithmetic. An earlier command also named a nonexistent `tests.test_paper_evaluation_independent` module and failed test discovery for that name; the corrected command above passed. Independent arithmetic is already part of `tests.test_paper_evaluation`.

Verdict: the bounded real-evidence workflow passes artifact-integrity and focused software verification. No blocking implementation defect was found in the reviewed changes. This verdict does not authorize scientific release or resolve the documented source, family, custody and prospective-ledger gates. The parent workflow owns full-suite validation, development/operation logging and publication of code and suitable summaries.
