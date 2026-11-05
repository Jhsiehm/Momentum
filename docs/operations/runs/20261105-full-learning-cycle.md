# Full learning cycle — November 5, 2026

## Outcome

Completed an official-source evidence investigation, a separately registered historical adaptive-model diagnostic, a synthetic chronological-learning demonstration, independent result review and offline verification. No model was promoted. Training and audit machinery worked; general forecasting improvement was not established.

## Round 1 — evidence and methods

Agents `/root/cycle_evidence` and `/root/cycle_methods` reviewed existing evidence and model rules independently of execution. The 114th Congress complete-label proof was dated 2022-11-30, too late for the 116th inner-validation checkpoints. Recommended earlier final-calendar proof and a separate development protocol; preserved existing studies and human audits. Methods fixed all 15 demo118 cases, age180, existing six candidates, and before/after inclusion of resolved117 examples before scoring. Verdict: proceed with bounded investigation/demonstration, no release claim.

Protocol: `data/research-runs/full-cycle-20261105/protocol.json`, registered before acquisition/scoring. Official outcome class counts were already known; evaluation is exposed development evidence, not a protected holdout.

## New official evidence

Five source documents retrieved and hashed: CCAL-114hcal-S2 MODS, PREMIS and metadata-derived PUBLIC LAWS part6 PDF; PLAW-114publ140 MODS/PREMIS. Complete laws1–329 and unique originating bills exactly match the retained NARA census. Calendar bounded availability: March24,2017; sampled enacted law140/H.R.1831 date proof: May19,2016. Both precede earliest eligible116 checkpoint, July16,2019. This removes a temporal-label bottleneck for the new publication-based diagnostic only. Current preservation metadata does not prove historically identical rendition bytes or fulfill human action-history audits. No current BILLSTATUS records were backdated.

## Official training and scoring

Fixed eligible population/exclusions reused: 114 training23/1 enacted; 116 validation30/1; 118 diagnostic33/0. Six predeclared configurations selected only on116; chosen structured_context, L2=0.01, refit on53 earlier families. No identified train/diagnostic family overlap; automated family linkage remains incomplete.

| Method | Brier loss | Log loss |
|---|---:|---:|
| Fixed model | 0.00605899 | 0.04397273 |
| Adaptive model | 0.00455711 | 0.03678502 |
| Historical-rate baseline | 0.00297521 | 0.05608947 |

Adaptive Brier is24.8% lower than fixed, but53.2% higher (worse) than baseline. Paired adaptive-minus-fixed conditional family-bootstrap95% interval: [-0.00386638,0.00000703], includes zero. Adaptive-minus-baseline interval: [-0.00253737,0.00962594]. These omit training/Congress uncertainty and do not repair exposed/all-negative evaluation.

What changed: existing title-token hashing and structured publication features with weaker L2 regularization were favored on the prior validation set. Stage standardized coefficient0.67452→0.71583; inactivity−0.38929→−0.42400. These are model associations, not causal explanations. Example118-S.2231 estimate23.37%→15.11%, with negative outcome under the original own-bill/by-Congress-end target. Do not infer legislative importance or provision-level success from this target.

Original frozen study preserved. New result fingerprint: `9c925ba1f2d3dfbe70145a72c39afb901dfb9a77b0467eac78e60b5f27b75bbf`.

## Synthetic chronological-learning check

15 fictional118 cases,6 enacted; earlier training240 cases→300 after including resolved117 examples. Fixed before Brier0.22643566→after0.22688385: slightly worse. Adaptive Brier0.26081357, fixed0.22688385, rate baseline0.25566642. All15 adaptive configurations changed; this is evidence of functioning machinery, not real-world skill. Saved session `e8fadeef-c507-40f6-9319-2d564f07a807` is visible in Model learning. Reproduction and learning hashes match.

## Round 2 — independent results audit

Agent `/root/cycle_result_review` checked metadata identity, dates, source hashes, family separation, numerical comparisons and protocol compliance. Found missing coefficients for six inner trial fits. Corrected with a separate `official-audit-supplement.json`: all trial weights/scales retained, exact validation predictions and training hashes verified, no candidate reselection or change to original results. Reviewer verified correction and closed the finding. Verdict: acceptable development diagnostic, no outstanding material findings within review scope, no promotion.

## Round 3 — independent verification

Agent `/root/cycle_verifier` independently reran official and demo scripts offline, recomputed all15 chronological before/after fits and Brier/log loss, and reproduced the six-trial supplement. All matched. Reproduction byte hashes across2170 cycle/frozen-cohort/engine files remained unchanged. Verification checks implementation/reproducibility, not predictive validity. Focused verification suite: 26 tests passed (sessions, learning and publication-v2).

## Decision and next step

Do not promote: baseline still wins primary official metric; zero official diagnostic enactments; one positive in each inner partition; exposed evaluation; unvalidated family provenance. No production settings, hosted language-model weights or human audit receipts changed. No paid provider calls. Five new source requests, zero new bill imports, one new demo session, one new separately registered official diagnostic, and explicit verification reruns.

Next cycle: freeze a broader outcome-blind temporal cohort with naturally occurring positive outcomes, prior training/validation separation and later protected evaluation before selection. The new114 proof is reusable under a new protocol; do not overwrite v2 or repeatedly optimize on these33 outcomes. Preserve the failed synthetic improvement and baseline comparison.

Artifacts: `data/research-runs/full-cycle-20261105/` contains protocol, source bytes/manifests, official and demo results, full frozen demo bundle, selected/fixed/trial weights, supplementary uncertainty, and reproduction scripts. Reproduce from project root with `PYTHONPATH=. python3 data/research-runs/full-cycle-20261105/run_official.py --offline`, `run_demo.py`, and `supplement.py` under the same directory.
