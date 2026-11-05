# Development log

Record each meaningful work batch with its date, changes, validation, and remaining work. Detailed research receipts remain in `docs/operations/`.

## 2026-11-05 — GitHub baseline and public documentation

### Changes

- Connected this previously uncommitted workspace to `https://github.com/Jhsiehm/Momentum.git`; the remote had no refs at setup.
- Included the existing application, tests, research documentation, and operational receipts in the initial baseline.
- Rewrote the README for public readers and preserved the earlier detailed documentation in `WORKSPACE_GUIDE.md`.
- Added `AGENTS.md` with the user's standing instruction to commit and push future changes, keep progress logs, and preserve research gates.
- Added `CHANGELOG.md`; excluded OS metadata and runtime log files alongside existing credential, cache, and local-data exclusions.

### Validation

- Python regression suite: 204 tests passed in 73.275 seconds (`python3 -m unittest discover -s tests -q`).
- JavaScript syntax: all 17 `web/*.js` files passed `node --check`.
- Staged-file check: `.env` and `data/` excluded; no matches for the checked credential/private-key patterns. This is a targeted scan, not a comprehensive security audit.
- Diff whitespace check found six pre-existing trailing-whitespace lines in legacy documentation, a font license, and `engine/workspace.py`. Preserved baseline source and license content; no new application behavior was introduced.

### Remaining work

- Research limitations and follow-up studies remain documented in `docs/operations/status.md` and the roadmaps. This repository setup does not validate forecasting accuracy.
- Local runtime datasets and research bundles referenced by historical receipts are not included in Git.

## 2026-11-05 — Capture concurrent research progress

- Included updates produced by ongoing workspace activity to the operations status, lessons, and five-experiment receipt after the initial baseline was staged.
- Reviewed these documentation diffs; they record the completed verifier and preserve negative-transfer and development-only conclusions. Their numerical findings are attributed to the research receipts, not independently rerun by this repository-publication task.
- Validation: documentation diff whitespace check passed. Application code unchanged from the tested baseline.

## 2026-11-05 — Historical data audit and expansion design

- Audited a read-only official-data snapshot, saved publication studies, temporal/model/evaluator gates and the concurrent research lease. Added an aggregate audit receipt with exact inventory/import/positive counts, saved baseline performance, provenance gaps and blockers; no fitting or new scoring.
- Documented a proposed full 113–117 census, fixed day180 target, global adjudicated family purges, historical source/label availability gates, positive-family minima, and future 120/121 protected temporal evaluation before scoring. Existing 118 studies remain exposed; 119 is not asserted untouched.
- Extended only the read-only import-quality audit (schema v2) with per-Congress horizon/availability diagnostics, conflicting identities/labels/dates and orphan-resolution counts. No labels, model behavior, forecasts, frozen studies, human reviews or UI changed.
- Validation: focused suite 7/7; full suite 209 tests passed in 117.890 seconds. Checked 70,858 record IDs, 10,398 raw hashes and 10,392 import receipts without integrity failures. Verified 5,321 frozen files unchanged and 2,625 source receipt hashes. Historical proof is still not certified by byte integrity.
- Remaining: source acquisition/availability, complete negatives, family adjudication, enough eligible positive families, protected access and stricter future scoring preflight. No improvement or promotion claim. Full receipt: `docs/operations/runs/20261105-historical-data-audit.md`; detailed local artifacts remain ignored in `data/audits/historical-expansion-20261105/`.

## 2026-11-05 — Expanded survivor experiments

- Acquired 700 new official historical bills, fitted 10 prespecified variants, and locked development selection before confirmation scoring. Added 149 eligible training rows after temporal/family gates.
- Saved 12 local research reports and 7 collections; all 700 source imports retain actual observation times. Added reproducible runner archive and detailed operations receipt. Runtime sources, private chat and databases remain ignored.
- Validation: independent design/implementation/numerical audits passed; full isolated offline replay matched all frozen artifacts; all 2,334 source hashes and 12 report endpoints verified. Initial replay needed the docs symlink added; no research outputs changed.
- Results are mixed: selected X2 improves descriptively over expanded survivor, but intervals cross zero; adding training worsened the survivor's Brier 6.00%. No production promotion or scheduled-budget changes. Later independent-Congress validation remains outstanding.

## 2026-11-05 — Sequential originating-chamber passage benchmark

- Added `engine.sequential`, a separate fixed-day30 passage-label workflow with forward Congress training, initial frozen model, expanding structured retraining, existing bounded adaptive selection, and historical-rate comparison on identical cases. Preserved enactment code and worker configuration.
- Added strict target/provenance fields, complete-coverage requirements for negatives, checkpoint/availability/family gates, explicit missing-label exclusions and blocked sparse/unfinished folds. Reports retain code/label identities, manifests, model artifacts, selection traces, reliability and event detection metrics; exclusive content-addressed files avoid overwriting prior runs.
- Documented the active sequential-learning milestone and maintenance-only product scope in the public README and benchmark protocol. Added an operations receipt alongside existing research receipts.
- Validation: final focused suite 8/8; final full suite 217 tests passed in 105.937 seconds; CLI smoke replay twice reused one immutable report; CLI help, compilation and whitespace checks passed. The initial full run (215 tests) had one reproducibility failure because source hashes changed during an in-flight edit; the unchanged-source rerun passed.
- Outstanding: no official passage study scored; audited passage labels and multi-Congress feature coverage, clustered uncertainty, protected final evaluation and a minimal dashboard remain. Synthetic tests demonstrate software correctness only; improvement is not established and release eligibility stays false.

## 2026-11-05 — Execute updated sequential practices

- Ran the new day-30 passage benchmark against a consistent official-data snapshot: 11,092 bills, no adjudicated passage-label manifest, no historical evaluation checkpoint metadata; all six folds blocked with no scores. Nineteen available checkpoints belong to out-of-scope Congress119.
- Ran a separate fixed-seed 1,080-bill synthetic workflow across six forward Congress folds and four methods; exact replay matched. Results remain mixed and establish software behavior only.
- Validation: 8/8 sequential tests, independent report-hash and all24 Brier arithmetic checks, temporal/equal-case assertions, and all3 saved platform report endpoints passed. Archived reproducible runner and execution receipt; no core model changes or promotion.
- Outstanding: audited passage labels, historically available day-30 features, early-Congress coverage and remaining research gates are required for real-data scoring.

## 2026-11-05 — Acquire passage and day-30 source evidence

- Added a bounded source-audit pipeline and six focused tests. Audited802 of820 fixed candidates, acquiring early110–112 official sources and reusing verified700-bill caches. Retained18 HTTP404 failures without replacement.
- Produced64 machine-corroborated passage-positive labels and584 day30 publication-proxy rows (32 overlap), with raw-source receipts and explicit provenance/human-review flags. No missing action was labelled negative; no official observations backdated.
- Validation:14 focused tests passed; all802 successful rows reconstructed offline;2,664 source hashes/lengths verified; three platform reports saved and API-checked.
- Remaining: no certified negatives or complete historical action histories; early-Congress feature coverage and human/family gates remain. Sequential scoring stays blocked. No model, schedule or production change.

## 2026-11-05 — Negative passage audit

- Cross-checked738 unresolved outcomes and64 positive controls against five final calendars and retained official action histories. Source-reviewed12 explicitly pending House bills into current-time negative labels;10 have day30 publication proxies. Remaining726 unresolved outcomes and18 prior missing sources preserved.
- Added conservative screening, separate source adjudication and nine tests. Coverage assertion is outcome-specific, not historical feature or independent human certification; label availability is current audit time. No scoring or promotion.
- Validation:23 focused tests; exact offline screen/adjudication replay; report/source hashes; three saved platform endpoints. Initial key-order serialization failure fixed in a new canonical revision while preserving initial artifacts and unchanged evidence.
- Remaining: historical training availability, representative negatives, early-Congress evidence and action/family/human gates. Full receipt: `docs/operations/runs/20261105-negative-passage-audit.md`.
