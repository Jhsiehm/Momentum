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

## 2026-11-05 — Real-source workflow with three live agents

- Executed evidence/methods audits and independent verification with `/root/source_audit`, `/root/methods_audit` and `/root/independent_verifier`. Audited actual retained official sources and frozen memberships; no new scoring, fitting, acquisition or promotion.
- Added deterministic immutable review-packet exporter and four tests. Actual packet includes 12 selected training cases, 14 publication versions and 40 verified source files (4,376,740 bytes), with all human decisions pending. Independent byte-identical replay passed.
- Fixed agent-discovered exposed-development exclusion gap: paper preparation now requires a reviewed exposure registry and blocks matching bill/family identities. Completeness and reviewer qualifications remain external gates. Prior models, results and registrations preserved.
- Validation: root full suite **302 tests passed in 188.321 seconds**; root/verifier 20 focused tests passed; methods agent separately passed 16 paper tests. All three reports include concrete findings/reproduction and retain source/family/custody limitations. Initial verifier test-discovery mistake was corrected and disclosed, not counted as success.
- Read-only local research APIs returned HTTP 200; scheduler settings unchanged. Unique research lease acquired/renewed/released. Receipt: `docs/operations/runs/20261105-live-agent-paper-review.md`; agent reports under `docs/research/reviews/`; raw runtime packet remains ignored.
- Outstanding: human source/family review, historical rendition identity, parser lineage, complete exposure registry, source-supported survivor label times, protected custody and certified prospective issuance. No independent forecasting gain claimed.

## 2026-11-08 — Complete bill-context experimental programme

- Created `docs/research/BILL_CONTEXT_EXPERIMENT_PLAN_V1.md`: versioned whole-bill evidence representation, E0 extraction-quality pilot, E1–E8 bounded development experiments and E9 independently registered successor validation. Incorporates multi-label meaning, full language, political/procedural context, relationships and announced calendar information.
- Fixed chronological/matched-case comparison rules, development decisions, baseline and calibration rules, missingness handling, trial/compute caps, controlled update cadence and the meaning of a 60% Brier reduction. Maximum historical modeling budget is 75 model/period fits; no power or performance guarantee. Preserves all existing paper/model gates and requires a distinct successor registration for richer models.
- Grounding: inspected repository protocols/runners and primary GovInfo, Senate and research-paper sources. Validation: manual design-consistency review, local document links, E0–E9/14-section coverage, fit-budget arithmetic and whitespace check passed. No tests or empirical experiments executed for this documentation-only batch.
- Added a planning receipt and documentation links. Next: reviewed schema/pilot registration and bounded E1 calendar experiment preparation; actual evidence/human/custody gates remain. Receipt: `docs/operations/runs/20261108-bill-context-experiment-plan.md`.

## 2026-11-08 — Bill-context execution and human-review handoff

- Executed the bounded 100-bill introduced-text acquisition with immutable selection and provenance. All 100 downloads succeeded; parsed only the 50 design cases, preserving 213 sections. Quality text remains unparsed pending design freeze.
- Added preparation runner, artifact verifier, readable design-review exporter and versioned annotation/dictionary guidance. Calendar encodings prepared on exact legacy splits; no new model fits or outcome scores.
- Assessed E0–E9 dependencies: E0 partial, E1–E9 blocked by required evidence/review/upstream/prospective prerequisites. User volunteered as first reviewer; no approval inferred.
- Validation: 25 focused tests and full 307-test suite passed (57.302 seconds); real artifact replay passed; 50 design / zero quality review pages checked. Frozen artifacts preserved. Diff whitespace checked before commit.
- Receipt: [execution and blockers](operations/runs/20261108-bill-context-execution.md). Runtime XML, reviews and manifests remain ignored. Remaining work: qualified human annotations, second reviewer/adjudicator, historical-source/family/label certification and approved model registrations.

## 2026-11-08 — Independent agents, reciprocal audit and verified repairs

- Dispatched three independent source, methods and software auditors at the user's explicit request, then had each cross-review a peer. Retained reports distinguish independent findings, implementation ownership and repeated checks.
- Fixed verifier optimized-mode and resealed-data gaps with explicit checks and authoritative source/split/vector/section/annotation bindings. Added eight local-corpus mutation/replay tests (explicit skip when runtime evidence is absent).
- Added separately versioned text rendering with exact Congress identity and block boundaries, preserving inline words and all original evidence. Bound readable review exports to source bytes, metadata receipts, guide/code and page hashes. Source agent identified and rechecked receipt-chain repair; methods agent identified and rechecked section-coordinate repair.
- Documented unresolved positive-family scope and E6 population-comparison ambiguity in a separate methods clarification. Did not change the hashed original plan, registered runner, human gates or frozen models.
- Validation: full **318-test suite passed in 77.310 seconds**; independent real-source replay, temporal/split checks, mutation probes and final export checks passed. All 359 original pilot files and frozen audit hashes preserved; no quality extraction, new fitting, scoring, acquisition or promotion. Diff whitespace checked.
- Receipt: [reciprocal agent audit](operations/runs/20261108-context-peer-audit.md). Remaining work includes certified source/family/annotation evidence, applicable population signoff, common-population registration and prospective custody. Machine review is not human certification.

## 2026-11-08 — Authorized exploratory calendar study executed

- Created a separately named exploratory protocol following explicit user authorization to relax human certification and reviewed positive-family floors for computation. Preserved original paper protocols, pending reviews and frozen studies; retained temporal/family/class/same-case checks and provenance limitations.
- Registered code/input hashes before nine fixed L2=.05 logistic fits across Congresses 115–117; all converged, inactive logit clipping, exact prior control reproduction. Added training-only rate/stage baselines, raw/calibrated metrics and 10,000 paired global-family bootstrap draws.
- Mixed result: time improves equal-period mean Brier by 0.2029%, interaction by 0.6004% versus control; both worsen Congress 115 and fail the all-period lead rule. Best average skill versus historical rate 14.0822%, not 60%. No promotion or final candidate fit.
- Validation: full 321-test suite passed in 78.390 seconds; six focused solver/experiment tests and final three new tests passed. Independent agent replayed gradients, predictions, baselines, metrics, splits and bootstrap; original frozen audit and all 359 pilot files preserved. Diff whitespace checked.
- [Execution receipt](operations/runs/20261108-exploratory-calendar.md) and [independent audit](research/reviews/20261108-exploratory-calendar-audit.md). Runtime results remain ignored. Remaining limitations: exposed periods, provisional source/label/family evidence, unadjusted uncertainty, no independently validated gain.

## 2026-11-08 — Bill-mechanism representation design

- Registered ten original design cases (two per Congress 113–117) before independent agent annotation. Each of two reviewers read full supplied text, produced summaries and 120 mechanism labels; third source-first agent challenged all 120 pairs and preserved disagreement history.
- Initial 111/120 agreement is descriptive consistency, not accuracy. Final provisional labels: 32 present / 74 absent / 14 uncertain; all nine disagreements and four prior shared uncertainties retained, plus one agreed label challenged. Reviewer B counter-audited the adjudicator without changing sealed submissions.
- Added deterministic paired-annotation and adjudication integrity tooling; exact quotes, identities, status schemas, original review bindings, comparison replay and challenge coverage verified. Seven focused tests passed, including changed-original rejection; no full regression rerun claimed.
- All 359 original pilot files and frozen model audit preserved. No quality-text parsing, downloads, training, scores or promotion. Runtime annotations remain ignored; public methodological summaries committed. Diff whitespace checked.
- [Receipt](operations/runs/20261108-mechanism-design.md). Remaining work: define operative category boundaries and action direction, separated extraction measurement and source eligibility before E2 predictive comparison. Machine agreement does not certify labels or historical validity.


## 2026-11-08 — Mechanism/direction rubric v2, partial agent batch

- Froze a clearer mechanism/direction/evidence rubric and registered the remaining 40 design cases. Reviewer A sealed 20 cases, 240 statuses and 197 effects; B has no sealed submission. Reciprocal reviews and methods annotation audit remain incomplete after both annotators hit the workspace spending cap.
- Added source-offset/schema/provenance validators and rejection tests; repaired two independently demonstrated peer-validation gaps. Methods agent read its ten-case subset before labels; source-first notes preserved.
- Validation: eleven focused tests passed; all 40 input views matched preserved source envelopes; A validated; all 359 original pilot files and frozen model audit unchanged. No full regression claim. Runtime data remains ignored.
- Readiness counts show zero positive cases in every design-subset calibration split. No fitting, scoring, quality parsing, promotion or performance gain. Resume missing B annotations and reciprocal/methods review before broader source-coverage preparation.
- [Partial execution receipt](operations/runs/20261108-mechanism-rubric-v2.md). Frozen rubric and sealed A submission must remain unchanged on resume.


## 2026-11-08 — Resumed mechanism v2 annotation and reciprocal review

- Resumed agents successfully after prior spending-cap interruption; preserved the partial receipt and A's sealed primary. Both batches now contain 40 bills, 480 statuses and 463 evidence-linked effects, with original counts 205 present / 261 absent / 14 uncertain.
- Completed source-based reciprocal review of every case: 23 supported without peer findings, 16 corrections requested and one uncertain; 34 findings in separately sealed receipts. These are review dispositions, not accuracy. Original annotations remain immutable.
- Eleven focused tests passed. Primary/peer integrity replay passed; all 40 source views, all 359 original pilot files and frozen audit preserved. No full-suite claim, quality parsing, acquisition, fitting, scoring, promotion or scheduler change.
- [Resumed execution receipt](operations/runs/20261108-mechanism-rubric-v2-resume.md). Predictive readiness remains blocked by missing calibration positives and source/encoding eligibility; corrections remain a separate representation version, not silently applied original labels.
- Independent methods audit completed the fixed ten-case subset (120 statuses/86 effects;13 findings) and every peer finding (33 accepted with qualifications,one uncertain), plus one additional sunset-direction correction. Root verified coverage, bindings and evidence quotes. Preserved an explicit later revision to one subset interpretation; no forced consensus or overwritten primary.


## 2026-11-08 — Applied mechanism corrections and expanded dated XML coverage

- Created a separate corrected 40-bill design dataset: 501 evidence-linked effects, 205 present /259 absent /16 uncertain statuses,21 changed bills. All50 finding dispositions recorded, including overlapping prior recommendations and two explicit new consistency findings. Reciprocal corrected-layer checks found no additional issues; originals and intermediate sealed corrections preserved.
- Added correction integrity/export utility and tests for finding bindings, coverage and undocumented edits. Expanded dated training/calibration XML coverage by200 fixed, outcome-blind selections (50each113–116), excluding all100pilot IDs/families;200 successful downloads,zero failures,3,260,056bytes. Added selection/timing/metadata tests and independent read-only code review.
- Initial acquisition run failed before registration/network on missing checkpoint metadata for excluded rows; preserved failure and fixed the outcome-free snapshot projection. Fresh v2run registered before network. Current retrieval timestamps retained; zero certified historical feature rows.
- Validation:21 focused tests passed; correction source/schema/finding and peer receipts verified;384 original research files and frozen audit preserved. No full-suite rerun. New source bytes/annotations remain ignored under data/.
- Postselection exposed-label readiness shows zero positives in all expanded calibration subsets (n = 22/32/44). No predictive fits, scoring, new mechanism annotations on acquired texts, promotion or scheduler change. Broader natural coverage and validated source-eligible extraction remain prerequisites.
- [Execution receipt](operations/runs/20261108-mechanism-corrections-and-coverage.md).
- Added public offline coverage verifier using explicit checks; exact 200-source replay passed normally and under Python optimization. Registered acquisition code unchanged; independent coverage replay confirms 370 frozen files unchanged (overlapping root's 384). Shared lease released.


## 2026-11-08 — Larger corpus, archival evidence audit and extractor contract

- Registered and acquired 1,000 additional introduced XMLs in ten presealed cycles of at most 100 cases, 250 per Congress 113–116, excluding all pilot/prior-selected identities and families. Zero failures; 16,052,288 bytes. Metadata-dated current-source coverage increased 232→1,232 distinct training/calibration identities. Fixed splits and acquisition code preserved; no adaptive replacements or outcome-based selection.
- Postselection exposed-label counts now show calibration positives 5/1/5 across folds 115–117, removing the zero-positive issue but leaving inadequate evidence for reliable calibration and required certification. No fits, predictions, scores, new mechanism labels or promotion.
- Independent eight-case PREMIS audit verified current XML checksums but found all matching rendition creation events in 2023 after cutoffs; earlier XML digest values absent. Historical identity remains unresolved; no claim that legislative meaning changed. Root verified 16 metadata files/spans and recounted 2,007 events.
- Added a draft extractor evaluation contract, with corrected-label coverage and explicit abstention, semantic one-to-one effect matching and protected quality-access gates. No extractor implemented/trained; quality texts untouched. Aggregate historical exposure during draft preparation disclosed.
- Independent code review found omitted result/cycle claim checks. Added separate supplemental verifier without changing registered acquisition code; resealed-claim mutation tests and normal/optimized actual replay passed. 36 focused tests passed. All 1,401 prior research files and frozen audit preserved; no full-suite rerun claimed.
- [Combined execution/readiness receipt](operations/runs/20261108-large-training-corpus.md). Shared lease released; schedules unchanged. Next: archival byte/public-availability binding and design-only extractor implementation before quality validation or predictive testing.

## 2026-11-08 — Executed design-only mechanism extraction

- Added pure deterministic extractor retaining section context, exact trigger locations and explicit abstention; ran all forty corrected design bills (337,823 characters):706 candidates,2,654 hits,five unvalidated suggestions,480 abstentions,zero accepted labels. Locator intersections399/501 are not semantic recall or prediction accuracy.
- Added hash-bound graph-conditional one-to-one effect evaluator. Independent review found and fixed unsupported present statuses, incompatible graph edges and suggestion direction/dimension issues. Added structural rejection and exhaustive matching tests. Root runner checks original design membership, reference/view hashes, immutable outputs and end-of-run source/code preservation.
- Validation:36 focused tests passed; normal and optimized replay agree; independent agent replay and full candidate/hit/suggestion offset checks passed. No full-suite claim. Historical official-doc investigation used eight requests; zero of eight historical identities resolved.
- No quality-text parsing, fits, outcome scoring, accepted annotations, promotion or schedule changes. Source provenance and semantic review gates remain. [Execution receipt](operations/runs/20261108-design-extractor.md); runtime receipts remain ignored in data/.
- Preservation replay verified 265,400 prior files unchanged and identical frozen-model audit; shared lease released. Independent replay reproduced the exact sealed result.

## 2026-11-08 — Reviewed all candidate misses and suggestions

- Reproduced a separate sealed packet of all 102 missed effect quotations and five unvalidated suggestions across 34 design bills. Two agents completed full assigned-view primary review (326,914 characters), followed by source-based reciprocal review of every item. Peer agreement is not blinded agreement or semantic accuracy.
- Primary diagnoses:49 vocabulary gaps,41 implicit effects,11 scope/quotation issues,one reference-direction question. All five suggestions supported only as suggestions. Preserved seven deadline-dimension questions (including three later self-audit findings) and one direction question separately; no original reference or extractor overwritten.
- Added reproducible packet/integrity audit with exact source evidence, full item coverage, review bindings and false-certification checks. Independent review found Boolean identity acceptance; fixed with explicit types and regression. Contradictory supplied view hashes also reject.
- Validation:40 focused tests passed; normal/optimized review replay identical. All120 inventoried prior files and frozen-model audit unchanged. No full-suite claim, protected quality parsing, fits, outcome scoring, accepted labels, promotion or schedule change.
- Followed six official HTTP routes including architecture PDFs, public API summary and current package ZIP. Preserved raw responses/headers and independently verified eleven file hashes; zero of eight historical identities resolved. No external contact/private credentials. [Batch receipt](operations/runs/20261108-candidate-error-review.md).

## 2026-11-08 — Reference v3 and structural-context extractor v2

- Adjudicated all eight recorded questions using six complete bound views and frozen rubric; independent methods review agreed on all eight. Exported separate provisional v3:seven deadline dimensions corrected, one duty operation/dimension corrected, four quotations expanded; forty bills,501 effects and480 statuses retained. Parent and original reviews unchanged.
- Added pure structural-context wrapper around immutable v1, with deduplicated source spans and explicit hierarchy/order links, retaining all lexical hits/proposals/abstentions. Independent review found malformed-path hang and insufficient runner structure checks; added fail-fast preflight and source/ancestor/boundary validation with regression tests.
- Executed all forty design bills:337,823 characters,706 candidates,2,654 unchanged hits,2,567 context-linked hits,1,932 pooled spans,480 abstentions. Quote intersections399→401 arise only from expanded references, not model accuracy or lexical gain.
- Validation:54 focused tests passed; normal/optimized replay identical;133 prior files and frozen-model audit unchanged. No full-suite claim, protected quality parsing, acquisition, outcomes, fits, accepted labels, promotion or schedule change. [Execution receipt](operations/runs/20261108-reference-v3-context-v2.md).
- Independent full design replay reproduced the exact result and verified source links plus all four baseline code hashes. Shared lease released.

## 2026-11-08 — Tested expanded candidate rules against corrected references

- Froze33 generic lexical rule families and independent design contrast fixtures before the forty-bill run, preserving corrected reference v3. Locator intersections401→449/501:48 recovered,zero lost,52 still unlocated. Added73 hits and19 candidate groups;21 additions outside reference quotations are not false-positive labels.
- Preserved every original candidate/hit structure and proposals; expanded counts reflect actual groups,480 abstentions and five unvalidated suggestions remain. Exact structural/source links verified. Rules and tests are informed by prior design errors; no held-out, semantic or predictive accuracy claim.
- Fixed hash-ranked24-hit review found20 supported locators and4 misleading contexts (struck wording, descriptive project feature, heading,purpose). All evidence/coverage checks passed. Recorded map-title boundary issue; no post-result tuning or label changes.
- Validation:70 focused tests passed after an initial missing owner-test-file import during concurrent authoring; normal/optimized results identical. Independent methods replay recomputed all deltas/sample selections and source/code bindings.151 prior files and frozen-model audit unchanged. No full-suite claim, protected quality parsing, acquisition, outcomes, fitting, promotion or schedule changes. Shared lease released.
- [Experiment receipt](operations/runs/20261108-expanded-candidate-rules.md). Next semantic work must distinguish operative context and effect meaning before interpreting locator gains as model improvements.

## 2026-11-08 — Executed context-triage experiment

- Froze seven generic source-context warning rules before running forty design bills. Separate decisions preserve all2,727 raw hits:322 flagged,2,405 unflagged. Retained-only reference quotation coverage remains449/501 with zero losses; no legal-effect or prediction accuracy implied.
- Prior exposed24 diagnostic retains20 supported locators and flags3of4 misleading cases; descriptive optional-project passage remains unflagged. Fresh added-hit sampling excludes all24:only1flagged eligible (11shortfall),12of48retained selected. No replacement sampling.
- Fresh source review of all13 found11 supported locators and2 misleading occurrences:flaggedheading and retained cross-clause “no cost ... and may” match. Root verified all evidence, bindings and cross-tab. Preserved residual failure; no post-result tuning, rejected raw hits or accepted labels.
- Validation:89 focused tests passed; normal/optimized results and independent full arithmetic/source/sample replay agree.143 prior files and frozen-model audit unchanged. No full-suite claim, protected quality parsing, acquisition, outcome scoring, model fitting, promotion or schedule change. Shared lease released.
- [Experiment receipt](operations/runs/20261108-context-filter-experiment.md). Context flags remain review aids; clause attachment and explicit semantic interpretation remain next research questions.

## 2026-11-08 — Detailed experiment reporting preference

- Recorded standing user preference in AGENTS.md: every experiment must receive detailed user-facing results and a complete saved receipt, including setup, definitions, denominators, per-category/per-case measurements, failures, exclusions, validation, uncertainty and exact artifact/reproduction links.
- Expanded the existing context-triage receipt with all forty bill rows, all twelve mechanism results, every fresh source-review rationale, offset conventions and a full artifact index. No new experiment or research result was produced.
- Validation: authenticated forty output envelopes and verified their recomputed totals match2,727 raw/322flagged/2,405retained hits,501effects and449raw/retained intersections; all13review records mapped to the sample. Documentation diff check passed. No code or tests changed; no suite rerun needed.

## 2026-11-08 — Experiment validity audit, isolated repairs and negative rerun

- Three agent collaborators audited code, source integrity and research methods, then cross-reviewed new versions. Added a strict source/reference/evaluator guard, leaf-scoped v4 expansion, affirmative-provenance filter v2, universal legacy-proposal quarantine and adversarial/runner tests. Frozen implementations and evidence remain unchanged.
- Registered one forty-bill design rerun before execution: 2,727→2,717 raw hits; 449→447 of 501 reference quotation intersections; eleven removed identities and one added; 322→317 flags; five suggestions quarantined. All 480 statuses remain abstentions. These are locator diagnostics, not semantic/predictive accuracy.
- Reviewed all sixteen changed-case records: five useful locators lost, five misleading/nonoperative matches removed, one malformed boundary match replaced; both overlap losses are useful coverage losses and two relaxed flags concern genuinely struck wording. Preserved the first source-review receipt and a separate revision correcting two rationale overstatements. No post-result tuning or promotion.
- Documented thirteen methods findings, the earlier 200-source single-cycle protocol deviation, and staged recovery/quality/prediction gates. Historical identity, provisional reference completeness, independent human review, family/class coverage and prospective custody remain unresolved. No protected quality texts or new outcomes accessed; no model fitting.
- Validation: final full suite 465 tests passed in 79.610 seconds; final focused 32 tests passed normally and under optimized Python. Earlier suite 456 passed before final tests were added. Initial adversarial failures were fixed before registration. Independent normal/optimized arithmetic and runner replay match result `950af33a265164374f41651dbd3bfdaf6f72bb8759626e602ccb4b3e82867178`. Root verified all sixteen review source spans and case coverage. All 230 prior inventoried files and the frozen-model audit remain unchanged. Shared research lease released.
- Full setup, all forty bills/twelve categories, every changed-case rationale, exact hashes, reproduction commands and limitations: [execution receipt](operations/runs/20261108-experiment-validity-audit.md). Next work follows the [recovery plan](research/EXPERIMENT_VALIDITY_RECOVERY_PLAN.md); this version is not qualified for predictive use.

## 2026-11-08 — Bounded v5 regression recovery

- Added separate extractor v5 with five bounded prohibition-subject families and filter v3 with qualified structural amendment-prefix chains. Preserved frozen v4/filter v2, every prior locator and exact quarantine; no semantic labels or promotion.
- Registered one identical forty-bill design comparison before extraction, pinning 124 input files and 31 code/test files. Recovered all five useful locators lost in v4: 2,717→2,722 hits, no removals. Raw/retained quote intersections 447→449/501, two recovered and none lost. Restored two struck-text flags, 317→319; all five suggestions remain quarantined, all 480 statuses abstain.
- Independent collaborator recomputed every count and reviewed all seven changed occurrences plus two secondary reference intersections. Five previous misleading identities and the malformed cross-block identity stay absent. This is exposed-design regression recovery, not independent semantic or predictive accuracy. No protected quality texts, new outcomes, fitting or source acquisition.
- Validation: 486 full-suite tests passed in 77.294 seconds; 34 focused tests passed normally and optimized. Independent arithmetic and full runner replays agree across both modes. Root checked all nine review records, exact evidence and complete change coverage. All 341 preserved files and frozen-model audit unchanged; research lease released.
- [Complete receipt](operations/runs/20261108-v5-regression-recovery.md) records all forty bills/twelve mechanisms, all changed-case rationales, exact seals/code/input identities and reproduction commands. Next: parser/table/mixed-content coverage and provenance/time-edge fixtures, followed by genuine source/reference readiness. Historical, human-review and prospective gates remain unresolved; no 60% improvement claim.

## 2026-11-08 — Source-render coverage and provenance-edge readiness

- Added XML node, attribute, text/tail and structural accounting plus conditional identity/time preflight helpers and a fixed 25-case synthetic manifest. Kept renderer, reference offsets, prior experiments and production features unchanged.
- First registered forty-source run failed all forty cases because the audit rejected official external DTD declarations; preserved all failures and passing provenance result. Separate audit v2 accepts declaration identifiers offline without external resolution, rejecting internal subsets/entities. An independent malformed-XML test caught an exception escape; normalized before the second registration.
- Second registered run reconciled all forty views: 8,331 nodes, 6,667 represented spans, 1,664 unrepresented nodes, 9,299 text/tail segments; 324,489 source characters + 13,334 inserted newlines = 337,823 rendered characters. No post-registration failures; 25/25 synthetic cases match expected behavior. Parser-visible coverage is not document completeness or historical certification.
- Actual findings: 114-HR3803 has ten table rows/twenty cells and ten concatenated within-row boundaries; nine between-row gaps retain whitespace. Three fraction nodes remain unrepresented: two 41/2 hours contexts and one NW1/4. All forty bills warn about attributes, namespace identity and unresolved external DTD semantics. Zero narrow nontext-tag matches does not exclude mathematics.
- Validation: 535 full-suite tests passed in 79.337 seconds; 49 focused tests passed normally and optimized. Independent source/partition/count/table review and replays agree. Root verified aggregates, nine row gaps and three fraction offsets. All 433 preserved files and frozen-model audit unchanged; lease released. No quality/outcomes, model fits or predictive testing.
- [Complete receipt](operations/runs/20261108-source-render-provenance-audit.md) includes both registrations, all forty cases, tag categories, all 25 synthetic dispositions, table rows and exact artifact/code hashes. Next: structural input retaining tables/fractions/attributes and offsets; evidence-backed availability and at-risk gate composition before quality/training. Historical and independent-human gates remain unresolved.

## 2026-11-08 — Separate structural bill input v1

- Added an authenticated structural sidecar with complete parsed element hierarchy, qualified attributes, table row/cell ownership, fraction context and exact Unicode mappings into the unchanged frozen reading view. Preserved span attributes without interpreting a visual grid or normalizing fractions.
- Registered 83 input files and 23 code/test/fixture files before the fixed forty-design run. All forty succeeded: 8,331 nodes, 2,903 attribute-bearing nodes/3,726 attributes, 9,299 text/tail segments, 337,823 unchanged characters, one table/ten rows/twenty cells and three fractions. No reference migration, quality parsing, acquisition, model fitting or prediction test.
- Independent agent reconstructed all forty raw XML trees and checked every mapping, relationship and attribute plus every actual table/fraction case; all matched. Shared parser implementation and exposed-design limitations explicitly retained. No post-result tuning or observed failure.
- Validation: 552 full-suite tests passed in 78.230 seconds; 17 focused tests passed normally and optimized. Optimized runner and independent verifier results identical. All 536 inventoried prior files and frozen-model audit unchanged; lease released.
- [Complete receipt](operations/runs/20261108-structural-input-v1.md) includes all forty output identities, every table row/fraction, test cases, immutable hashes, exact reproduction and remaining gates. Next: separately registered structural consumer evaluation; historical availability, human/source/family/time and protected quality gates remain unresolved.

## 2026-11-08 — Structural extractor null experiment and model critical path

- Added separate structural-boundary extractor v1 preserving frozen v5 raw candidates, full bill context and literal fraction annotations. Screens every explicit cell endpoint, including nested/empty/orphan cells, without changing lexical rules or accepting labels.
- Registered 205 input and 52 code/test/fixture files before the fixed forty-design comparison. Null result: zero cell crossings among 2,722 hits; combined context retention remains 2,403; raw/retained quotation overlap remains 449/501. All 480 statuses abstain and five proposals remain quarantined. No protected quality, acquisition, model fitting, new outcomes or forecasts.
- Independent review verified every decision, all 501 effect rows and twelve category totals, plus all seventeen table/fraction-associated occurrences. Documented unchanged month-name “May,” committee-name “Appropriations,” timetable and header ambiguities; no post-result tuning. Full source text and reference anchors preserved.
- Validation: 566 full-suite tests passed in 81.463 seconds; fourteen focused tests passed normally and optimized. Optimized runner and independent verifier match. All 586 inventoried prior files and frozen-model audit unchanged; lease released.
- Added a repository-grounded critical-path plan: stop open-ended locator tuning, resolve the same eight historical rendition cases in a bounded evidence study, complete applicable review and exact matched populations, then run one eligible predictive block. Prior nine-fit calendar study remains mixed; no 60% claim or gate waiver.
- [Complete experiment receipt](operations/runs/20261108-structural-extractor-v1.md) and [model-experiment critical path](research/20261108-model-experiment-critical-path.md) include exact results, hashes, all cases, reproduction, current coverage constraints and stopping decisions.

## 2026-11-08 — Eight-case historical feasibility and matched-text specification

- Registered the same eight unresolved cases before sixteen public GovInfo PREMIS/ZIP requests, with fixed size/time/attempt limits and no retries/substitutions. All sixteen responses HTTP 200 and parsed; 4,674,296 bytes and 48 archive members retained. Zero old XML digests or historical-byte bridges recovered; all eight XMLs match current renditions, eligibility remains 0/8.
- Pre-registration review corrected UTF-16 entity guard bypass (initial independent 10/11), discarded partial bodies, crash retry risk, reset resume clock and ambiguous identity handling. Final independent review verified all responses, member hashes, old object IDs, manifests and dispositions. Normal/optimized offline replay identical, with fetch disabled during root replay.
- Froze E3 two-arm specification and exact identity-only planned folds 115–117: six conditional fits, zero executed; same sparse solver/control, core-only TF-IDF, fixed existing budgets and ten explicit unresolved gates. Eligible populations remain null. No outcomes or protected quality loaded.
- Separate post-result PDF/HTML metadata exploration found all sixteen current rendition/checksum events also 2023; no new requests or text extraction. Prepared exact eight-package/sixteen-object evidence request locally, not sent. Root confirmed all alternative member/object digest bindings after correcting an ad hoc verification base-directory error.
- Validation: 592 full-suite tests passed in 82.628 seconds; 26 focused tests passed normally and optimized. All 637 inventoried prior files and frozen-model audit unchanged; lease released. No model fits, predictions, source certification or gate waiver.
- [Complete receipt](operations/runs/20261108-historical-source-feasibility.md), [conditional specification](research/MATCHED_TEXT_COMPARISON_V1.md) and [evidence request](research/HISTORICAL_OBJECT_EVIDENCE_REQUEST_V1.md) provide every case/request/hash, fixed settings, observed failures and remaining external dependency.

## 2026-11-08 — Synthetic matched-text preprocessing and sparse solver

- Implemented separately versioned structural text preparation, core-only TF-IDF and sparse penalized logistic optimization, with research-only NumPy/SciPy pins. Preserve full source context, negation, citations and source segment mappings; mask administrative/focal identity text and enforce structural bigram boundaries.
- Registered 28 invented documents (20 core/4 calibration/4 evaluation) and a six-row numerical fixture. First run completed numerical fits but failed NumPy-Boolean result serialization; preserved it and registered a serialization-only v2. All ten successor checks pass, with identical prepared/vocabulary/fits across versions. Six registered synthetic optimizations and two GD references total; zero real forecasting/calibration fits or predictive scores.
- Scalar objective/gradient errors zero; finite-difference error 2.5991743479725216e-11; GD prediction difference 1.7706698609148974e-6. Independent agent recomputed all 28 documents, 22 terms and three fit objectives/gradients without additional optimization; maximum discrepancy 6.245004513516506e-17.
- Validation: 626 full-suite tests passed in 80.218 seconds; 34 focused tests passed normally and optimized. Initial duplicate-keyword import failure and three harness weaknesses corrected before registration, documented alongside registered serialization failure. All 696 prior files and frozen-model audit unchanged; 39 registered bindings verified; lease released.
- [Complete receipt](operations/runs/20261108-matched-text-synthetic-preflight.md) includes exact settings, every synthetic row, fit metrics, both registrations/failure, independent review, artifact hashes and reproduction. Synthetic success does not release real-data gates or establish predictive gain. Historical evidence packet remains local and unsent; source availability, qualified review, matched populations, class coverage and execution registration remain unresolved.

## 2026-11-08 — Delegated archive follow-up and prospective feasibility

- Three agents investigated historical sources, assessed a prospective fallback and cross-audited validity. Two separately sealed current/legacy archive-index phases made sixteen bounded metadata requests on the same eight cases; all HTTP 200 and empty, 48 response bytes, zero capture leads and unchanged 0/8 eligibility. Legacy mapping was an explicit inference and separately planned after the first result, not universal archive coverage.
- Independent review checked 36 seals, sixteen case/cutoff bindings, code/input/response hashes and timing; root replay agreed. All 85 inventoried prior files and frozen-model audit unchanged; lease released. No production-code edits or test-suite rerun; no bill-body acquisition, outcomes, fits, forecasts, external messages or gate release.
- Prospective draft identifies source-only immutable capture/verifier gap and distinguishes it from the live recorder and research issuance contract. New source collection cannot supply matured historical training immediately. Methods review retains unresolved positive-family scope; per-fold interpretation fails two training/all development floors before source filtering.
- [Complete receipt](operations/runs/20261108-historical-next-feasibility.md) links every case, bounded acquisition settings, failure/absence limitations, source findings, independent cross-review and prospective implementation specification. Custodian request remains ready but unsent; no evidence of predictive improvement.

## 2026-11-08 — Scholar-informed real-data retrospective text diagnostic

- Reviewed four primary legislative-prediction studies and author/official datasets. A separate bounded BICAM schema investigation retained 148,573 bytes from ten direct requests, verifying 26 ZIP members and three headers; no bill rows imported. Independent review verified all 18 manifest hashes, request ordering and archive/header evidence. Full coverage, text-body semantics and archive-wide license remain unresolved.
- Registered a separate four-fit current-rendition retrospective association study, preserving original E3/paper gates. User authorized autonomous methodological decisions and historical learning; human certification/positive-family floors are explicitly not computation prerequisites for this limited study, not declared passed. Two arms, two exposed folds; merged training core/calibration, no calibration/tuning or promotion.
- 1,200 nonpilot source records yielded 1,195 unique candidate identities and 1,186 prepared documents. Nine substantive committee-name-tag ambiguities were excluded before labels; all cases and offsets retained. Accepted train/evaluation: 115 = 540/298 (11/10 positives), 116 = 843/297 (17/8 positives). Four fits converged; 595 evaluated families, 18 events.
- Text mean Brier 0.026963601507469 vs anchor 0.027028531593121: 0.2402279437% relative improvement, with both folds slightly improved. Text skill vs rate 8.2925872232%, but 1.9701400334% worse than stage reference. Text-minus-anchor descriptive interval [-0.00017522276398180823, 0.0000025946416800441225] includes zero; 10,000 valid draws. No robust forecasting gain, independent validation or 60% claim.
- Validation: 641 full-suite tests passed in 85.477 seconds; 15 new tests normal/optimized and 49 combined focused tests optimized. Independent replay verified all prepared seals, two vocabularies/scalers, four objectives/gradients, 1,190 model probabilities, all references/metrics/bins and bootstrap draws without refits; maximum probability discrepancy 5.55e-17. Pre-run guard/fixture corrections and verifier invocation failures documented. All 2,532 registration bindings, 6,427 preserved prior files and frozen-model audit unchanged; lease released.
- Docker daemon availability verified; pinned local environment used, no container created or claim that isolation repairs historical provenance. [Complete receipt](operations/runs/20261108-retrospective-text-diagnostic.md) contains every evaluated bill, every exclusion, numerical/settings tables, exact hashes and reproduction. Next: representative outcome-blind corpus/version audit and stronger dated context; keep stage reference, no extra search on this evaluated subset. External historical evidence/reviews remain unresolved.

## 2026-11-08 — BICAM inventory acquisition and source-defect audit

- Three agents implemented/reviewed bounded identity acquisition and dated-context acceptance. Six exact HTTP 206 ranges retained 29,415,382 bytes; both decoded members passed ZIP/deflate/CRC/hash checks. No bill text member, labels, outcomes or models examined.
- Preserved registered v1 malformed-CSV failure. Separately registered offline v2 introduced a reversible, title-only carriage-return compatibility assumption and exact-integral Congress parsing; it stopped on actual missing fields. No census/sample or version-reference interpretation completed.
- Post-failure diagnosis and independent replay agree: 414,277 logical rows under the declared dialect, 99 reversible title escapes, 43 blank Congress/introduction records, including five target-period Senate IDs. All case/offset ledgers retained; no silent reconstruction or exclusion. Reconcile official identities before a new sample; stop parser expansion.
- Root verified all 1,232 prior artifacts and frozen-model audit unchanged, plus nine registered code/test/protocol bindings. All 34 focused tests passed normally and optimized. All 675 full-suite tests passed in 81.593 seconds; lease released.
- [Complete receipt](operations/runs/20261108-bicam-inventory-audit.md) records six requests, both failures/registrations, every missing-field case, exact identities, limits and next decision. Context acceptance fixes four candidate features before scores and retains the stage benchmark; the previously evaluated 595 cases remain exposed. No predictive improvement, historical eligibility, gate release or model promotion claimed.

## 2026-11-09 — Five-case official-record reconciliation

- Preserved five failed introduced-edition MODS requests (302 error redirects) and five blocked Congress.gov requests (403). Separate adaptive five-PDF Congressional Record acquisition succeeded: 4,286,800 bytes, dated evidence for all five proposed identity/date repairs. Total 15 direct requests, distinct from search discovery.
- Recorded separate proposed dates: S4653/116 September 22, 2020; S4899/117 September 20, 2022; S5314/118 November 13, 2024; S5543/118 December 16, 2024; S5575/118 December 17, 2024. Two use explicit introduction-range membership; original blanks and all 38 other defects remain untouched.
- Visually checked relevant PDF pages and section continuity; retained corrected-rendition labels, day precision and incidental procedural-outcome exposure. Introduced-edition endpoint absence does not prove non-introduction. No historical-byte proof, sample release, outcomes modeled or predictive fitting.
- Verified 15 response hashes, three code bindings and 32 prior inventory files unchanged. All 34 focused inventory tests passed; three acquisition scripts compiled. Independent official-record review retained in docs/research/reviews. Full suite not repeated because predictive/production code unchanged.
- [Complete receipt](operations/runs/20261109-bicam-five-case-reconciliation.md) includes every case, all phase failures/limits, URLs/pages/hashes and explicit missingness rules. Next: separately registered scoped enrichment and official target-coverage check before sampling; no gate waiver or model promotion.

## 2026-11-09 — Target inventory and official directory comparison

- Registered offline target v3 retained reviewed repairs and explicit quarantine; preserved a negative result with 116 additional issues: 97 missing dates, five Congress-boundary dates, fourteen unsupported identifiers. Accepted candidate projection has 75,622 rows, but no sample released. All five repaired bills fail the calendar-only day-180 window; among accepted candidates 63,897 pass that calendar check and 11,725 do not. No at-risk eligibility claim.
- Retrieved twelve official directory pages: all HTTP 200, 35,211,033 bytes, 75,605 distinct XML identities. Preserved initial parser rejection of standard ZIP resource links; separately registered offline successor accepted the twelve listings without changing XML membership or making more requests.
- Registered comparison found 75,592 intersections, thirteen official-only and thirty candidate-only identities. Every mismatch and all 116 corpus errors retained; absence is not evidence of non-introduction or a negative outcome. Version reference independently parsed: 54 rows with IH/IS meanings confirmed, no per-bill text join certification.
- Independent replays agreed on all source partitions, calendar flags, directory identities and differences. Root ran all 30 new tests normally and optimized; all passed. All 98 prior artifacts and frozen-model audit unchanged. No full-suite rerun for this isolated source audit.
- [Complete receipt](operations/runs/20261109-bicam-target-and-official-inventory.md) includes every error/quarantine/difference and per-group counts. Continuing via a new official-directory 100-case source-readiness audit, rather than repeatedly relaxing the failed BICAM sample gate. No bill XML fetched in this batch, no fits or forecast improvement claimed.

## 2026-11-09 — Official hundred-case metadata readiness

- Registered a separate fixed hash sample of 100 from 75,605 current official identities. All 100 requests returned HTTP 200; 1,441,575 bytes retained, all 100 XMLs parsed with exact identity/date matches and no observed errors or replacements. This is an adaptive official-source study, not release of the failed BICAM sample.
- All introduction dates fit Congress; 88 have a day-180 window. Metadata includes 469 valid action dates, 100 sponsor identifiers, 984 valid cosponsor joining dates across 82 cases, three valid withdrawals and 122 text-version records. Eighteen absent cosponsor containers remain unknown. Introduced-edition metadata exists for 98 cases; 87 also pass calendar horizon. Both missing cases preserved.
- Independent replay verified exact sampling, all 100 bytes/identities/path fingerprints/allowed outputs and coverage counts. Sixteen new tests passed normal/optimized; root full suite passed all 721 tests in 83.818 seconds. Registration bindings verified; no model fits, labels imported, linked texts or historical certification.
- [Complete receipt](operations/runs/20261109-official-billstatus-readiness.md) includes every case, raw hashes, all failures/shortfalls and limits. Continuing with separately reviewed retrospective context methods and extraction, preserving original E3/paper gates and explicit source-proxy limitations. No tuning, promotion or 60% claim.

## 2026-11-09 — Official context acquisition and preserved adapter failure

- Independently preflighted a fixed 12,000-case official sample across six Congresses, excluding 695 protected/previously scored known identities. All 12,000 HTTP requests succeeded; 192,995,893 bytes retained, no retries/replacements. All 1,226 registered bindings verified.
- Independent replay reproduced 9,726 anchor-valid and 2,274 ineligible cases. Both procedural fields were missing for every anchor-valid row, so stopped before labels or fits. Bounded source-only diagnosis identified unsupported legitimate hyphenated action codes and named Senate sources without numeric codes, compounded by coupled procedural error handling.
- Preserved v1 and every case; a separate offline v2 correction reuses identical bytes and sample. No outcome-driven replacement or relaxed enactment evidence. All 771 pre-correction software tests passed in 86.429 seconds, illustrating why real-source coverage is a separate gate. All 523 preserved prior files and frozen-model audit unchanged.
- [Detailed receipt](operations/runs/20261109-official-context-diagnostic.md) records exact acquisition limits, counts, hashes, preflight fixes and failed readiness. Subsequent offline correction and conditional two-fit execution are recorded separately below when completed.

## 2026-11-09 — Offline context correction and one-class experiment halt

- Registered offline v2 recovered referrals for 9,717 and recency for 9,715 of 9,726 anchor-valid rows, with every baseline/cosponsor/cutoff/family field unchanged. Same 12,000 source bytes/identities; zero additional requests. Independent full replay passed.
- Registered v2 experiment froze 5,110 training, 1,382 Congress-117 and 1,464 Congress-118 candidates before labels. Resolved labels contained 7,112 negative proxies and 844 unknowns, with no positives. The mandatory both-class gate stopped before any fit. Independent replay matched all 7,956 labels and the exact failure; no predictions or improvement claimed.
- Full suite passed 798 tests in 88.897 seconds; final focused preflights passed 16 adapter and 21 runner checks normally/optimized. [Complete receipt](operations/runs/20261109-official-context-diagnostic.md) preserves all versions, counts, hashes and limitations. Separate post-failure diagnosis is investigating publication-metadata selection bias before another design is considered.

## 2026-11-09 — Publication-completeness selection bias established

- Preserved a registered conditioning-audit failure at case 4,972: its duplicate identity parser omitted a known legacy schema. Separately registered v2 reuses the frozen strict validator, with six normal/optimized tests; earlier exposure and failure are recorded.
- Independent full replay confirmed 333 current own-public-law assertions among 12,000 records, all publication-anchor-ineligible: 293 missing edition dates and 40 unreachable day-180 checkpoints. All 333 had empty enrolled-edition dates. This explains the eventless accepted population as outcome-associated metadata selection, not evidence of absent enactment.
- No new training labels, fits or scores. Reviewed a separate adaptive action-milestone/chamber baseline versus context design, applied uniformly to all saved cases with unchanged outcome proxy and family rules. Implementation is a new experiment; the failed predecessor remains immutable. [Receipt](operations/runs/20261109-official-context-diagnostic.md) retains every count and audit.

## 2026-11-09 — Action-based matched design and preserved label-contract stop

- Separately registered a two-column action-milestone/chamber baseline versus eight-column context challenger, uniformly on the original 12,000 sources. Preparation retained 10,095 records; independent source replay matched all artifacts and 5,287/1,421/1,497 family-selected candidates. All predecessor membership changes were saved before labels.
- Unchanged outcome resolver accepted no positives: 7,123 negative proxies and 1,082 unknowns, including 231 terminal-text identity failures and 851 lacking post-Congress update evidence. Both-class gate stopped before any optimization. Independent replay matched all 8,205 labels/exclusions and zero-fit failure. No probabilities, improvement or promotion.
- All 858 tests passed in 85.993 seconds; 39 focused checks passed normally/optimized. [Full receipt](operations/runs/20261109-action-context-diagnostic.md) preserves exact settings, denominator changes and failure. Bounded follow-up investigates the 231 source-label contract failures, retaining this stopped study unchanged.

## 2026-11-11 — Resolved publication exclusion and exact signing-annotation parsing

- Independently verified removal of the publication-completeness artifact: 292 of 333 current-law assertion cases now pass the action-feature gate (previously zero); 40 remain outside the day-180 horizon and one has a pre-introduction action. This does not claim all selection bias is removed.
- Implemented a separately versioned resolver accepting only an exact supported signing annotation alongside independent matching law-list/public-law-action/date evidence. Preserved all predecessors. Full 8,205-row comparison: 151 prior unknowns became eligible positives; 60 corroborated cases were already enacted/cutoff-ambiguous, 13 were outside/end-ambiguous; seven uncorroborated cases stayed unknown. All previously resolved labels and all unrelated records unchanged.
- Registered and completed exactly two fixed fits on 5,221 training rows (105 positives), evaluated on Congress 117: 944/25 positives and 118: 1,109/21 positives. Context mean Brier 0.020298322979578 versus baseline 0.020934701172014, rate 0.022199623156237 and milestone 0.020467246562650: relative gains 3.0398%,8.5646%,0.8253%. Context improves both periods against baseline, but the descriptive interval versus milestone includes zero. No promotion, historical validation or 60% claim.
- All 908 full-suite tests passed in 98.944 seconds; 39 focused checks passed normal/optimized. Independent all-label/transform/objective/gradient/probability/metric/bootstrap replay passed with no refits. Preserved dense-matrix numerical warnings and passing errors-as-exceptions einsum follow-up. [Complete receipt](operations/runs/20261111-action-context-resolution.md) contains all 2,053 evaluation cases, 231 audited label cases, 931 excluded labels, reliability bins, settings, hashes and reproduction. Raw runtime data remain ignored.
- Final preservation: all 85,304 prior files and frozen-model audit unchanged; all 36,034 new registration bindings verified. No live-model promotion or schedule change.

## 2026-11-12 — Independent failure-path audit

- Isolated audit from e61d0bf with separate evidence/runtime agents and reciprocal review. Replaced optimization-sensitive passage assertions, rejected duplicate/invalid scoring rows, normalized scoring chronology and blocked within-capture clock rollback. Added valid controls and real CLI subprocess rejection tests.
- Eight audit methods passed optimized Python with CLI child optimization propagated; two disposable guard-removal mutations were detected. Focused pre-final suite passed 43 tests. Final full-suite validation follows below.
- Remaining: legacy non-atomic artifact creation, external timestamp/paired issuance and broader runtime/source coverage. No real model fitting, predictive testing, source certification or promotion. See [complete receipt](operations/runs/20261112-independent-failure-audit.md).

- Final validation: 43 focused tests passed; eight audit methods passed optimized Python (CLI children inherit optimization); py_compile and diff whitespace checks passed. Full discovery ran 788 tests in 107.500 seconds with 14 errors and seven skips: missing optional NumPy and absent ignored research fixtures prevent a full-suite pass. A direct inventory-test rerun confirms missing data/research-runs/historical-dataset-options-20261108/zip-result.json. No artifacts were fabricated to clear those checks.
