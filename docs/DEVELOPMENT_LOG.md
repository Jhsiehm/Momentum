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

## 2026-11-05 — Expanded survivor experiments

- Acquired 700 new official historical bills, fitted 10 prespecified variants, and locked development selection before confirmation scoring. Added 149 eligible training rows after temporal/family gates.
- Saved 12 local research reports and 7 collections; all 700 source imports retain actual observation times. Added reproducible runner archive and detailed operations receipt. Runtime sources, private chat and databases remain ignored.
- Validation: independent design/implementation/numerical audits passed; full isolated offline replay matched all frozen artifacts; all 2,334 source hashes and 12 report endpoints verified. Initial replay needed the docs symlink added; no research outputs changed.
- Results are mixed: selected X2 improves descriptively over expanded survivor, but intervals cross zero; adding training worsened the survivor's Brier 6.00%. No production promotion or scheduled-budget changes. Later independent-Congress validation remains outstanding.
