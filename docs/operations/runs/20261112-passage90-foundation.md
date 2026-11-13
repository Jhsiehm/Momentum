# Passage90 foundation and source pilot — November 12, 2026

**Outcome:** implemented the separate study contract, a stronger reference and paired-evaluation machinery, and an append-only source/forecast ledger; completed a bounded live source pilot. All 22 HTTP requests succeeded and all 20 selected bills passed source identity and inspection. One current-record action is a candidate passage within the target window. No certified labels, historically eligible feature rows, real model fits, predictive scores, or real prospective forecasts were produced. Independent prospective launch remains blocked.

## Plan, question and execution scope

The [comprehensive plan](../../research/FORECASTING_FIRST_PLAN_V1.md) orders definition, source feasibility, ledger, matched comparisons, model development, future issuance, and outcome evaluation. The [new protocol](../../research/PASSAGE90_PROTOCOL_V1.md) defines first originating-chamber passage in the 90 days after a day-30 checkpoint, requiring a complete window before Congress end. Existing enactment and passage-by-Congress-end studies retain their targets and evidence.

This execution asks whether a fixed outcome-independent sample can be collected with exact source identity and immutable provenance, and whether its current records contain narrowly recognized first-passage candidates. It is a source-feasibility and software study, not a predictive model comparison. The first prospective cohort remains a proposal: Congress 120 introductions January 3–June 30, 2027, fixed November 15, 2027 analysis, conditional on prelaunch gates.

## Versions and frozen configuration

Collector `forecast-ledger-v1`; runner `passage90-source-pilot-v1`; inventory parser reuses the prior strict directory parser plus its exact ZIP-link amendment; source metadata validation reuses `official-billstatus-readiness-v1`. The live runner, collector, parser dependencies, runner tests and overarching plan were bound by SHA-256 before requests, checked again before each request, and rechecked after acquisition. The new predictive contract was not used to fit or score this pilot.

Exactly two Congress-118 chamber directory URLs, then ten identities per chamber selected by ascending SHA256(`passage90-source-pilot-v1` + newline + canonical bill ID). Sample identities were sealed before requesting bill bodies. Maximum 22 requests, zero retries, redirects or replacements; 5,000,000-byte inventory cap and 2,000,000-byte bill cap plus one sentinel byte. Timeout 20 seconds per socket operation; this is not a strict total wall-clock budget. No time or monetary-cost measurement is claimed.

Passage candidates require the correct originating-chamber LOC action code (House 8000, Senate 17000), source-system code 9, matching chamber text prefix, valid date and unambiguous scalar fields. The first such recorded action is used, with explicit boundary and early-passage dispositions. This narrow screen cannot establish that all possible source encodings or earlier passage actions are complete. No missing code is assigned a negative outcome.

## Population, denominators and result

The observed directory frame contained 16,213 identities: 10,564 House and 5,649 Senate. Independent census completeness is not certified. All 20 deterministic selections (10 per chamber) were retained; no candidate was replaced or excluded after inspection. All 20 have a complete calendar window.

- Requests: 22/22 HTTP 200; 2/2 inventories accepted and 20/20 bill bodies identity-valid and inspected.
- Retained bytes: 7,537,420 inventory bytes plus 425,236 bill bytes = 7,962,656 total.
- Current-record dispositions: 1/20 candidate within-window passage; 2/20 later passage with earlier negative coverage unverified; 17/20 no recognized passage, unresolved.
- House: 0/10 within-window candidates, 1/10 later, 9/10 unresolved. Senate: 1/10 within-window candidate, 1/10 later, 8/10 unresolved.
- Certified positive labels 0/20; certified negative labels 0/20; historically certified predictor rows 0/20; independently attested captures 0/22.
- Ledger: 45 receipts (one registration, 22 starts, 22 completions), zero pending captures, zero forecast pairs; local integrity verification passed.
- Real fitting, predictive testing, calibration fitting, model promotion and live forecast issuance: none. No before/after predictive comparison exists for this execution.

The one candidate is S.4367/118: introduction May 20, 2024; checkpoint June 19; horizon September 17; recognized Senate passage August 1. H.R.6229/118 passed December 10, 2024, after its March 2 horizon; S.2861/118 passed May 8, 2024, after its January 18 horizon. Both remain uncertified negatives. All other cases remain unresolved. These small source-screen counts do not estimate comparative event prevalence or prove passage has more usable labels than enactment.

## Every selected case

Each line gives introduction; checkpoint; horizon; recognized first passage (if any); disposition; raw bill SHA-256. All dates here are source day precision.

- **hr8104-118**: 2024-04-20; 2024-05-20; 2024-08-18; none recognized; `unresolved_no_recognized_passage`; `b727c05d711445c024d69dda27a6c260bfed5dfeff11fa9faa7b95d1b521e61d`.
- **hr3600-118**: 2023-05-23; 2023-06-22; 2023-09-20; none recognized; `unresolved_no_recognized_passage`; `8298977cb52677f5cbaceafa597b14ef57dffd5ade70c3bdad27af1c11ba57db`.
- **hr927-118**: 2023-02-09; 2023-03-11; 2023-06-09; none recognized; `unresolved_no_recognized_passage`; `98fb98fb31b4a1c6ef4b9194a864583990b0207a12763737195525c7223b24fd`.
- **hr6917-118**: 2024-01-05; 2024-02-04; 2024-05-04; none recognized; `unresolved_no_recognized_passage`; `d1d11f2d016e2150b9dd996aec879ad9db8f3677903eca500345cc1f2cb94c98`.
- **hr1041-118**: 2023-02-14; 2023-03-16; 2023-06-14; none recognized; `unresolved_no_recognized_passage`; `da97116cde9f9bdd9d7e8e1a48b42c3e3a220841291003da1da74e0f0d1999b7`.
- **hr5518-118**: 2023-09-14; 2023-10-14; 2024-01-12; none recognized; `unresolved_no_recognized_passage`; `b06df3efe71b905e1c512de19ac76a79be05387a6096505c31edfe7fe1a8fc27`.
- **hr438-118**: 2023-01-20; 2023-02-19; 2023-05-20; none recognized; `unresolved_no_recognized_passage`; `8c98f85e8b37defedeb0a45ae84274426ecb4c297049a36ef04c5a1ea431d4da`.
- **hr3401-118**: 2023-05-17; 2023-06-16; 2023-09-14; none recognized; `unresolved_no_recognized_passage`; `d18f55e2fd29028ffc5aa7a75f96d4656022ab186bdb5d1ce315fc2a079fb08d`.
- **hr6229-118**: 2023-11-03; 2023-12-03; 2024-03-02; 2024-12-10; `later_passage_negative_coverage_unverified`; `d27157483c00b55bf3ef86e42c8c84032ced0b741a2b16a2afc139f0ecbad789`.
- **hr1307-118**: 2023-03-01; 2023-03-31; 2023-06-29; none recognized; `unresolved_no_recognized_passage`; `d431bf74242266ec644ba0e5693029bd0f1ff20e748d7aec028ac777363c71cb`.
- **s883-118**: 2023-03-21; 2023-04-20; 2023-07-19; none recognized; `unresolved_no_recognized_passage`; `973c22d4a091c24879a55c13a3573eac079210b5e45a7d0644775ebb7cab73ec`.
- **s4621-118**: 2024-06-20; 2024-07-20; 2024-10-18; none recognized; `unresolved_no_recognized_passage`; `3243d7d8d7f06c710c7d498b2997c8d64ff2850dfc7174ee031326c15df880f1`.
- **s4010-118**: 2024-03-21; 2024-04-20; 2024-07-19; none recognized; `unresolved_no_recognized_passage`; `043fa0ea22e703ed1a2bee773e9e1ff5751693124b4ad59fb1884b884e42129a`.
- **s2861-118**: 2023-09-20; 2023-10-20; 2024-01-18; 2024-05-08; `later_passage_negative_coverage_unverified`; `ed05d0d652841a28987b00d9acbd4768380b9c041847660c056276f9bdab263a`.
- **s4627-118**: 2024-06-20; 2024-07-20; 2024-10-18; none recognized; `unresolved_no_recognized_passage`; `5caa2e62c8e46c15a7bc9afd6d1d290a9dbc61e94e45c2dbc801e42ecd0009e4`.
- **s1171-118**: 2023-04-17; 2023-05-17; 2023-08-15; none recognized; `unresolved_no_recognized_passage`; `6d2a0e7cda5c1a7750c52194a459313ce90bdc5401f840e44e1997d266f497e1`.
- **s4367-118**: 2024-05-20; 2024-06-19; 2024-09-17; 2024-08-01; `candidate_within_window_passage`; `92435c8f5873ab9bdeeb6e7b5a54c3f501fefcb1bc1d9870b40b2c3ba9953d58`.
- **s3843-118**: 2024-02-29; 2024-03-30; 2024-06-28; none recognized; `unresolved_no_recognized_passage`; `0248d31fe20b69f1b4e1f0c55749c2753abd21842617708deb84b50a8b2134bf`.
- **s1772-118**: 2023-05-31; 2023-06-30; 2023-09-28; none recognized; `unresolved_no_recognized_passage`; `9cf38a7404ed1f1f0c9871a64eee6bfe0c7e8296c8fc26b1e70b90a78a25e814`.
- **s4525-118**: 2024-06-12; 2024-07-12; 2024-10-10; none recognized; `unresolved_no_recognized_passage`; `100285cbbac1c155b75f4b5c61d26dd7ca91992263bdfa15e015f5e3f5d97a04`.

## Audit findings and corrections before acquisition

The independent methods agent found that equivalent timezone spellings could bypass duplicate-forecast rejection, and that conflicting XML identity fields, multiple bill elements and mixed identity schemas could be accepted. Both were repaired and independently retested with valid controls before live acquisition. Passage checks were tightened for synthetic-to-real artifact mixing, pre-Congress checkpoints, first-passage/boundary semantics and future evaluation cutoffs. An integration test also caught the runner using a nonexistent successful-capture disposition; the whole mocked collector pipeline now exercises all 22 requests, both successful and failed inventory behavior. Parser/selection failures and code changes stop explicitly without replacements.

The separate user-requested audit chat produced [legacy failure-path fixes and evidence](20261112-independent-failure-audit.md), originally committed as `a6daeb4318ac2ce7f2f168329bbfad887ab9994f` and integrated as `99e0601`. It found optimized-Python assertion loss, duplicate-label overwrites, offset chronology errors, invalid unpaired rows and capture clock rollback. Its independent agents used actual CLI subprocesses and two disposable guard-removal experiments. The new-method reviewer independently removed a probability guard in a disposable copy and verified the test detected it. These tests establish sensitivity for those guards, not exhaustive correctness.

Independent new-method review and exact source replay are recorded in [the review](../../research/reviews/20261112-passage90-plan-review.md). All 20 cases, 22 raw responses, 45 receipt hashes and seven frozen code/protocol bindings passed independent replay under normal and optimized Python. Disposable raw corruption, sample reordering and invented negative-label certification were rejected. The unchanged original passed again. Independent verifier source SHA-256 is `85417a29cad9a9573c9b421f3b6fba50bfd32689c33d94775494003962603ca0`; independent verification JSON SHA-256 is `0d7ef33bbb891c4f443e322ccfc88a476d1bb741b8f6c043d8e54a736593f7bb`; adversarial receipt SHA-256 is `b34e3aeb3691e62d56a7ff3088cbe87dafd97f265943a429e4b46c7226333e37`.

The separate audit chat's follow-up found no new high-impact actionable failure within its inspected scope, ran 69 focused tests and independently replayed the source pilot. Its reviewed hashes were: passage contract `4773b387550f551a859155e976e00387080254b737a578c7521e6c67dcd79754`, ledger `23db7ff6d99242f9b46a94027d1ba942326e494d1ce0b7f83eba9285f912365c`, runner `b65986b6811390d5878add075d615c831e2b7c93fe8812249326dea9322ebfe3`, protocol `4caeb76b109a36a099bfaa9ccd6da2d1a3bb24a474813665269aa98216fdb59b`, and plan `1eab3ceff659ce3ce7f9571371ce39267d8ea7230d39579994fa199e8c494f4b`. It explicitly did not claim exhaustive failure-mode coverage or qualified human review.

Final root validation used pinned NumPy 2.0.2 and SciPy 1.13.1 in ignored `.venv`: **978 tests in 55.764 seconds, no failures/errors, one existing integration skip because retained bill-context pilot data are absent**. All 88 selected new/affected/audit tests also passed with optimized Python. Both independent replay modes passed again. Earlier full attempts remain recorded in the development log: missing optional packages caused thirteen import errors, and one test unnecessarily depended on an ignored historical ZIP receipt. That test now constructs its own explicitly synthetic ZIP and runs both actual successful six-range transport and all five invalid-response controls. No historical evidence was fabricated and no test was simply skipped to obtain a passing suite.

## Exact artifacts and reproduction

- [registration.json](../../../data/research-runs/passage90-source-pilot-v1-20261112/registration.json) — SHA-256 `63bcaa56f46899bf97e75661a9c3528eaece58844c64e7c4a5de7e26dd8dffd2`.
- [sample.json](../../../data/research-runs/passage90-source-pilot-v1-20261112/sample.json) — SHA-256 `fd3df19b3e4cf062be9ad845abd99fdef0c651bf8b57d71d6324c0a1ba10f5bf`.
- [result.json](../../../data/research-runs/passage90-source-pilot-v1-20261112/result.json) — SHA-256 `a702124589deeacdbdfdaa87238a36ed7bd388319d84947a7260802da3ea190e`.
- Ledger final receipt hash: `176224e3103ed3dbf19b98d139ead437fbaeb617e197167f58f6d229b76b3e0a`; raw bytes and SQLite state remain ignored under the run directory. Hash chaining detects ordinary corruption but is not an external witness against rewriting the entire local ledger.
- [Pilot runner](../../../scripts/passage90_source_pilot.py), [ledger](../../../engine/forecast_ledger.py), [passage contract](../../../engine/passage90.py).

```sh
python3 -m scripts.passage90_source_pilot --output data/research-runs/NEW-UNUSED-RUN-DIRECTORY
python3 -m engine.forecast_ledger verify data/research-runs/passage90-source-pilot-v1-20261112/ledger
python3 -m scripts.verify_passage90_pilot_v1 data/research-runs/passage90-source-pilot-v1-20261112
python3 -O -m scripts.verify_passage90_pilot_v1 data/research-runs/passage90-source-pilot-v1-20261112
python3 -m unittest tests.test_passage90 tests.test_forecast_ledger tests.test_passage90_source_pilot -v
python3 -O -m unittest tests.test_passage90 tests.test_forecast_ledger tests.test_passage90_source_pilot -v
```

Repeating acquisition creates a separate current observation and may retrieve changed bytes; it does not reproduce the original network response. Use retained objects and immutable registration for exact offline replay. A fresh clone intentionally lacks these runtime files. Never overwrite the existing run directory.

## Remaining gates and interpretation

The implemented reference uses training-only stage/chamber/time-remaining shrinkage with frozen boundaries, and paired metrics include Brier, log loss, class-specific and pooled results, calibration bins, top-20 cohort prioritization and family-resampled practical 2% contrasts. These are tested research primitives; there is no fitted passage challenger or real scored comparison.

Next evidence requirements are reviewed first-passage/complete-negative labels and time-correct training features, family/exposure review, a fixed finite-fit manifest, passage-specific model artifacts, independent timestamp verification, inventory/discovery operations and custody. Current observations cannot repair historical availability. Certified issuance deliberately rejects; caller-supplied risk/family/model assertions in local receipts remain uncertified. The first live validation requires future matured outcomes and cannot be completed during implementation. No unrelated product work, automatic retraining, recurring acquisition schedule or promotion was introduced.
