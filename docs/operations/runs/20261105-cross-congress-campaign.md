# Cross-Congress acquisition and learning campaign

User authorized the complete staged plan and additional official congressional acquisition if bill counts are insufficient. Target remains day180 own-bill enactment before Congress end; day30 passage is separate. Original survivor retained throughout. No paid APIs or production promotion.

## Completed feasibility and diagnosis

Official inventories:113=8,905;114=10,074;115=11,199;116=14,148;117=15,066;118=16,213 House/Senate bill identities. Inventory completeness does not establish historical feature or label eligibility.

Registered100 new candidates per113–117 Congress,500 total. All audited without source failures and exactly replayed offline.426 eligible checkpoints; within-Congress family representatives411;7 positive outcomes. Eligible/family/positive counts:113=89/89/0;114=86/83/3;115=85/83/3;116=86/77/0;117=80/79/1. Retained1,688 source documents,188,189,627 bytes. No forecasting scores computed on this feasibility batch.

Exposed-data diagnosis: retraining changed the raw stage coefficient from3.1394 to1.7237. On the previous696-case evaluation, mean probability for686 negatives increased2.47%→3.10%, while mean for10 positives fell5.56%→4.48%. Retraining weakened separation and worsened both outcome-group Brier errors. These are descriptive mechanisms, not proof of why the additional data caused those changes; original training has only one positive.

Crosschecked full final-calendar public-law tables against NARA:113=296,114=329,115=442,116=344,117=362. Bounded historical availability dates:2015-04-19,2017-03-24,2019-03-15,2021-05-08,2023-04-13, each end-of-day UTC. Original117 audit retained a disagreement: NARA Public Law117-354 links s4296, while calendar and individual law metadata link s4926. New evidence-v2 and expanded dataset explicitly adjudicate to s4926; prior frozen runs remain unchanged. Individual-law date proofs remain required for sampled law-bearing training cases. PDF table extraction used pypdf; first115 table page visually inspected. Publication preservation proxies do not establish complete historical action histories or human certification.

## Frozen acquisition and evaluation contract

- Development acquisition:15,000 candidates,3,000 per113–117, seed2026110515000. Exclude prior acquired/registered identities, retain source failures, no replacements. Audit all candidates, no accuracy-based stopping.
- Reserve:10,000 additional identities,2,000 perperiod. Acquire all reserves if the first batch contains fewer than200 temporally eligible, family-separated113–116 training positives or50 eligible117 development positives. Cap25,000 development candidates; if still insufficient, report blocked rather than continue until a favorable score appears.
- Confirmation:5,000 reserved new118 identities, not acquired for this campaign until one challenger is locked. Exclude known training/development/prior-exposed families.118 has prior broad exposure, so this is protected by identity within a historical development programme, not untouched-Congress or prospective validation.
- Forward folds114,115,116,117: training Congresses precede evaluation, and every training label must be available before the earliest evaluation checkpoint. Remove train/evaluation family overlap. Minimum per fold:200 training cases/5 positives and200 evaluation cases/10 positives. Report all folds separately.
- Fixed comparisons: nested250, nested1000, all-history structured L2 .2; most-recent-Congress structured L2 .2; all-history calibration variant with disjoint deterministic20% family calibration subset and the prior fixed monotone affine-logit algorithm. No hyperparameter search or unproven new historical feature.
- Choose one challenger using equal-weight mean fold Brier skill versus each fold's smoothed training-rate baseline; fixed-order tie break. Lock final artifact trained on113–117 before confirmation acquisition.
- Confirmation compares this challenger against the unchanged49-row survivor using identical eligible cases. Exploratory success requires≥2% lower Brier, conditional paired95% bootstrap interval below zero, no worse log loss, at least50 positive outcomes and all provenance checks. Neither success nor machine audit bypasses independent-review/promotion gates.
- Development sensitivity calculation precedes confirmation. It estimates paired error variability; it cannot guarantee power under Congress shifts. Inadequate confirmation yields inconclusive, not outcome-driven sample extension.

## Operations and reproducibility

`engine.cross_congress` registers/audits cached fixed-ID batches. `scripts.cross_congress_labels` retains calendar evidence and the explicit correction. `scripts.diagnose_retraining` uses only previously exposed data. `scripts.register_cross_congress_scale` locks development/reserve/confirmation lists. `scripts.cross_congress_evaluate` checks earlier label availability and fits forward models. `scripts.cross_congress_pipeline` coordinates resumable acquisition, shared lease renewal, count-based expansion and eventual locked confirmation. It does not install a recurring schedule or promote any model.

Progress is recorded in ignored `data/research-runs/cross-congress-scale-20261105/progress.json` and `pipeline-progress.json`. Completed records are immutable and reused for retries; replay reconstructs from retained sources. Source interruptions remain visible and block scoring until resolved. Current-time imports must never be backdated.

Initial validation:27 focused temporal/family/calibration/source-label tests passed; exact500-case offline replay; complete five-period calendar sequence/identity crosschecks. Large-batch acquisition and later evaluation are still in progress at this receipt checkpoint. No large-batch improvement is claimed.

## Acquisition compatibility amendment

The initial scale pass encountered one network timeout and a legacy identifier-schema record (115-hr3354). Same-ID retries recovered both. Explicit adapter maps only unambiguous billType/billNumber aliases, records original and parsed SHA256, and leaves source cache bytes unchanged.115-hr3354 remains excluded because its official list lacks an introduced publication. Platform import supports these aliases while retaining original raw bytes.56 focused tests passed; no scoring, selection or model-setting change. Amendment hashes and original failed-attempt records are retained locally.

A third initial-pass issue was116-s4935's conflicting introduction date (BILLSTATUS2020-12-01; introduced-publication action2020-11-30). Both imply day180 in May2021, after Congress end. An explicit named adjudication excludes it under every candidate date while retaining the unresolved conflict and all original sources. No date/outcome was selected; conflicts that could affect eligibility still block.58 focused tests passed.
