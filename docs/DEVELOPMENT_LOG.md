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

## 2026-11-05 — Fixed original-data survivor, 20 bills

- Tested the exact49-row original-data survivor artifact on20 new eligible118th-Congress bill identities, selected from a preregistered40-candidate screen with known-family exclusions. Model weights unchanged; no performance-based case selection.
- Brier0.00054515 versus smoothed-rate0.00153787; all20 outcomes negative. This tests conservative probabilities, not enacted-case discrimination or general improvement. No promotion.
- Validation: full offline replay; independent20-probability/Brier arithmetic; seeded selection and130 source checksums; two platform reports and one20-bill collection saved and endpoints checked.
- Remaining: adequate natural positive counts and independent temporal evaluation. Same-Congress historical exposure and action/provision provenance limits persist.

## 2026-11-05 — High-volume fixed survivor

- Registered1,000 new118th-Congress candidate IDs; scored all736 eligible known-family-separated cases with the exact49-row survivor weights. Retained264 exclusions and16 qualifying enactments; no source failures, tuning or early stopping.
- Brier0.01995385 versus rate0.02157197 (7.50% lower); conditional paired interval favors survivor. Higher-probability bin underestimates its6/13 enactments. Findings remain historical development evidence, not automatic learning or promotion.
- Validation: six new selection/immutability tests; exact full offline replay; independent arithmetic for736 probabilities/Brier/log loss;3,298 source hashes and lengths; repeated bootstrap. Ten collections and two reports saved, all1,000 source XMLs imported at actual observation time, endpoints verified.
- Remaining: independent temporal validation and separately registered calibration study; rare positives, prior exposure and historical-action/family/human gates remain.

## 2026-11-05 — Controlled survivor/calibration/retraining experiment

- Froze original49-row survivor, monotone calibration on149 separate earlier-Congress bills, and same-feature retraining on198 rows before auditing1,000 new candidates. Added reproducible runner and separate arithmetic/source verifier; previous artifacts remain unchanged.
- Evaluated all696 eligible families,10 enactments: original Brier0.01354544; calibrated0.01365660 (+0.82% worse, interval includes zero); retrained0.01408350 (+3.97% worse, paired interval favors original). Preserve survivor; no challenger promotion or self-improvement claim.
- Validation:36 focused tests; exact offline replay;2,088 probabilities/scores and both bootstraps independently recalculated by separate verifier;3,320 source hashes/lengths checked. Five reports and ten collections saved and API-verified;1,000 current imports retain real observation timestamps.
- Remaining: rare calibration positives, repeated same-Congress exposure, incomplete historical-action/family/human gates; stronger representative training evidence and separately registered time-period validation needed. Receipt: `docs/operations/runs/20261105-three-model.md`.

## 2026-11-05 — Cross-Congress acquisition campaign started

- Completed500-case feasibility and offline replay across113–117:426 eligible checkpoints,411 within-period families,7 positives; discovered75,605 bill identities across113–118. Diagnosed weakened stage separation in the prior retrained model.
- Audited all five final public-law calendars; preserved and explicitly corrected NARA117-354 bill-identity disagreement using calendar and individual law evidence. No prior immutable run changed.
- Registered15,000 development candidates,10,000 count-triggered reserves and5,000 separate confirmation identities. Added resumable acquisition/coordinator, chronological folds, family/label-time gates and one-challenger lock. Large acquisition is running; no completed accuracy or promotion claim.
- Validation:27 focused tests and exact500-case offline replay. Full receipt: `docs/operations/runs/20261105-cross-congress-campaign.md`.

## 2026-11-05 — Legacy source compatibility during scale acquisition

- Large-batch auditing found115-hr3354 uses legacy GovInfo billType/billNumber fields. Added explicit unambiguous identifier normalization with original/parsed hashes; retained original source bytes. Current-time imports now accept the same aliases while retaining the original raw hash. Conflicting aliases are rejected.
- Same-ID retry resolves the parser failure; the bill remains excluded for its missing introduced publication under unchanged evidence rules. An earlier network timeout also recovered without replacement.
- Validation:56 focused temporal/model/import/schema tests passed;500-case feasibility replay rerun after the adapter. Changes amend source compatibility only, before model fitting; frozen statistical rules and previous artifacts remain unchanged.

## 2026-11-05 — Explicit introduction-date conflict disposition

- Official records disagree on116-s4935 introduction (2020-11-30 vs2020-12-01). Both yield day180 after the116th Congress ends. Added explicit source-backed exclusion under every official candidate date; do not choose a date or use the outcome. Retained the disagreement and failed initial attempt.
- A conflict that could change eligibility still blocks.58 focused tests passed, including both-date exclusion and potentially-eligible rejection.

## 2026-11-05 — Additional data triggered and missing-proof quarantine

- The15,000-candidate batch completed with clean recovered acquisition,51,138 source documents and5.795GB retained evidence. Temporal/family checks yielded156 usable training positives and46 development positives, triggering the registered10,000-candidate reserve before any model fitting.
- Reserve113-hr2793 lacks mandatory explicit introduction-date evidence in its official introduced package; retained an explicit provenance quarantine with no features/outcome assigned and no replacement. The pre-fitting disposition amendment does not relax requirements for included rows; unavailable network sources and identity conflicts still block.60 focused tests passed.

## 2026-11-05 — Explicit legislative-day reconciliation

- Reserve114-s895 official introduced header says March27 (legislative day, March26),2015. BILLSTATUS uses March26 and MODS action uses March27. Added a narrowly scoped validator requiring exact package/bill identity and explicit corroboration of both dates in the official introduced header; original BILLSTATUS checkpoint convention stays unchanged.
- Default publication validation remains unchanged; only named adjudicated records use the supplementary validator. Original raw sources and initial failed attempt retained.68 focused tests passed, including missing/wrong-header rejection and publication regressions.

## 2026-11-05 — Cross-Congress campaign completed; no demonstrated gain

- Completed30,500 candidate audits:500 feasibility,15,000 initial development,10,000 automatically triggered reserve and5,000 reserved comparison. Latest forward fold clears training/development evidence gates with227/59 enactments; five fixed methods evaluated across four chronological folds.
- Locked calibrated-all-history challenger on11,871 families/281 enactments. Final comparison:2,315 eligible cases/29 enactments; Brier0.0121439707 vs original0.0121441147, effectively tied; paired95% interval includes zero. Secondary log loss1.98% lower. Primary2% and50-positive gates unmet; preserve survivor, no promotion.
- Explicitly quarantined final118-s4197 unresolved date conflict before scoring, with unchanged model/candidate identities and no replacement. Reported historical exposure and source-disposition amendments.
- Validation:70 focused tests, exact source/fitting/scoring replays, separate61,410-probability arithmetic and102,417 main source-file checks. Full receipt: `docs/operations/runs/20261105-cross-congress-campaign.md`.
- Platform delivery: 25,400 new bill identities, 5,100 unchanged records, four final reports verified through the API, and six 100-candidate collections. Completed campaign releases its research lease; recurring schedules remain unchanged.

## 2026-11-05 — Transfer diagnosis and constrained weight tests

- Preserved the survivor and diagnosed the canceled gains: improved negative-case error was offset by worse positive-case error; calibration partly rescued retraining.
- Tested fixed 25%/50% weight changes on explicitly exposed development evidence. Best blend improves Brier only 0.1195%, conditional interval includes zero; no independent validation or promotion.
- 22 tests, exact replay and 11,575 independently recalculated probabilities passed. Full report saved to the platform campaign chat. Receipt: `docs/operations/runs/20261105-transfer-diagnosis.md`.

## 2026-11-05 — Chronological weight-update consistency tests

- Tested 25%/50% constrained updates against period-specific anchors and full updates in three exposed chronological folds (8,568 evaluation rows, 182 enactments).
- Each update improved two periods and worsened one; no restrained rule passed the all-period criterion. Survivor unchanged; no independent validation or promotion.
- 26 tests, exact refitting replay and 34,272 probability/metric checks passed. Report saved to campaign chat; receipt: `docs/operations/runs/20261105-chronological-weight-updates.md`.

## 2026-11-05 — Granular transfer and feature audit

- Audited nine subgroup partitions, class errors, influential cases, exact feature collisions, calibration/base-model swaps and saved-fit gradients across 8,568 exposed evaluation rows.
- Repeated stage mismatch: introduced-document groups overpredicted, passage-document groups underpredicted. In 117, broad negative-case losses outweigh enactment gains; calibration partly rescues Brier. L2 gradient cancellation makes regularization a specific hypothesis, not a proven fix.
- No new fitted candidate or promotion. 29 tests, exact replay and 34,272 hybrid probability checks passed. Report saved to platform; receipt: `docs/operations/runs/20261105-granular-transfer-audit.md`.

## 2026-11-05 — Controlled regularization and stage experiments

- Fixed L2=0.05 with unchanged inputs improves Brier/log loss in all three exposed development periods; mean relative Brier gain 8.24% versus period-specific L2=0.2 controls. Categorical stage alone worsens two periods. This is not a survivor or independent-evidence win.
- Stage separation improves but residual calibration errors and larger saved-fit gradients remain. Convergence sensitivity is required before freezing a candidate. Survivor unchanged; no combined final fit or promotion.
- 32 tests, exact refitting replay, 51,408 independently recalculated probabilities and platform API delivery passed. Receipt: `docs/operations/runs/20261105-stage-regularization.md`.

## 2026-11-05 — Converged weaker-penalty candidate frozen for research

- Training-only gradient stopping confirms L2=0.05 improves all three exposed development folds, averaging 8.39% lower Brier against converged L2=0.2 controls. Both penalties reach tolerance; calibration procedure unchanged.
- Frozen separate candidate on 11,871 historical families/281 enactments, 9,496 core and 2,375 calibration rows. No fresh survivor comparison, independent validation or promotion.
- Retained initial numerical-warning artifacts; accepted explicit finite-checked einsum rerun agrees within 6.94e-16. 35 tests, exact replay and 34,272 scalar probability checks passed. Platform report saved. Receipt: `docs/operations/runs/20261105-convergence.md`.

## 2026-11-05 — Consolidated research handoff and log audit

User requested that all new findings be committed and logged. Verified the preceding implementation commits and existing development log, changelog, operational status and detailed receipts.

| Work | Implementation commit | Receipt |
| --- | --- | --- |
| Transfer diagnosis and small weight changes | `c060511` | [Transfer diagnosis](operations/runs/20261105-transfer-diagnosis.md) |
| Chronological update consistency | `5b2d9f0` | [Chronological tests](operations/runs/20261105-chronological-weight-updates.md) |
| Granular errors and feature audit | `5a63cf9` | [Granular audit](operations/runs/20261105-granular-transfer-audit.md) |
| Regularization and categorical stage | `711615f` | [Controlled experiments](operations/runs/20261105-stage-regularization.md) |
| Convergence and candidate freeze | `3310549` | [Convergence receipt](operations/runs/20261105-convergence.md) |

Current conclusion: smaller blending changes did not generalize consistently; categorical stage alone worsened two development periods. Weaker L2 improved all three exposed periods, averaging 8.39% lower Brier against converged period-specific controls. This is not an independent win against the survivor.

Frozen candidate: 11,871 historical family representatives, 281 enactments; 9,496 core and 2,375 calibration rows; final base gradient target reached after 3,917 iterations. Candidate digest `149b5f618cd74bcc1974cd502581490e8e8cb3c390baf25b9279e213bb35c0c5`. Survivor digest `ffb089cff396415431c2e2b04cb99ebf7d75fe040a777da661bb58d6af9d255c` remains unchanged.

Validation carried forward: 35 tests, exact replay, and 34,272 scalar probability checks. This documentation-only audit rechecked result/candidate/survivor hashes against verification receipts; no model retraining or new test-performance claim. Full numerical-warning reconciliation, limitations and runtime locations are in the convergence receipt. Runtime data and private platform chat history remain outside Git.

Next gate: newly registered unexposed evaluation against survivor and rate baseline, or prospective shadow forecasting if an appropriate historical cohort cannot be established. No production promotion or recurring schedule change.

## 2026-11-05 — Formal paper preparation and validation-readiness audit

- Audited research lineage from the original-only 49-row survivor through the 30,500-candidate campaign, chronological updates, stage/regularization diagnostics and accepted convergence candidate. Preserved every prior protocol/model/result; no fitting, new final scoring, search, promotion, imports or schedule changes.
- Created `docs/research/PAPER_PROTOCOL_V1.md`, `VALIDATION_READINESS.md`, `PAPER_DRAFT_V1.md`, `INFRASTRUCTURE.md` and `READINESS_AUDIT_V1.json`. No audited historical period establishes independent forward validation; proposed prospective 120–121 comparison preserves event/readiness and human gates and explicitly limits Congress-level inference.
- Added isolated `engine.paper_evaluation` preparation with immutable manifests, code/model/training/source hashes, identical cases, earlier-only historical-rate/stage baselines, strict labels/times/families and synthetic metrics. Real scoring deliberately blocks pending certified prospective issuance. Added a read-only artifact auditor and 15 focused tests with independent Decimal prediction/loss arithmetic.
- Validation: final full suite **297 tests passed in 62.580 seconds**; focused 15 passed; exact aggregate artifact audit replay, Python compilation, four-document local-link check and staged whitespace check passed. Earlier full iteration passed 294 tests in 95.944 seconds. No broad source recertification or independent human review claimed.
- README/changelog/status now link paper preparation and explain exposed historical evidence. Full receipt: `docs/operations/runs/20261105-paper-preparation.md`.
- Outstanding: independent custodian and source/family reviewers, external preregistration/timestamps, reviewed legacy adapters, rolling census/paired day-180 ledger, clustered inference implementation and publication reproduction bundle. No prospective forecast issued; existing live capture is a different workflow. Scientific experiment specified but not yet certified for execution.


## 2026-11-05 — Execute research-preparation workflow

- Ran the requested paper-preparation workflow under a unique shared lease; preserved an exclusive timestamped runtime execution envelope and exact test output.
- Validation: 15 focused tests passed in 0.263 seconds; before/after audits exactly match the versioned reference; frozen artifact and implementation/protocol hashes unchanged; saved envelope hash verified. Initial preflight also passed 15 tests. No full-suite rerun or new empirical result claimed.
- Outcome: preparation software checks pass; independent scientific evaluation remains blocked on the existing evidence, custody, prospective issuance and inference requirements. Zero models fitted, new real outcomes scored or forecasts issued; no schedule changes.
- Receipt: `docs/operations/runs/20261105-paper-preparation-workflow.md`. Runtime data stays ignored. This execution-only batch introduces no user-facing functionality or model milestone.
