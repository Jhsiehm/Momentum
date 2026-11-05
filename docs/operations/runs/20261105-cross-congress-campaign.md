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

## Initial scale acquisition and automatic expansion

Initial15,000 audit recovered all four initial incidents: timeout113-s1390, legacy identifiers115-hr3354 and117-hr20, and explicitly disposed late-date conflict116-s4935. Clean acquisition has51,138 source documents,5,795,386,818 bytes. Per-Congress eligible/family/positive counts:113=2471/1914/45;114=2520/1831/40;115=2485/1782/51;116=2443/1831/35;117=2513/2017/46. Full temporal and cross-period family exclusion yields156 training and46 development positives, so the frozen10,000-candidate reserve was triggered. No model scores influenced expansion.

Reserve113-hr2793 has a complete downloaded introduced publication but lacks mandatory explicit introduction-date evidence. It is quarantined with no features/outcome assigned, not replaced or counted negative. The unresolved provenance limitation and pre-fitting exclusion amendment are explicit; included-row evidence requirements remain strict.60 focused tests passed.

Reserve114-s895's apparent date disagreement is explicitly explained by its official introduced header: March27 (legislative day, March26),2015. A named reconciliation checks the exact bill/package identity, both header dates, BILLSTATUS legislative date and MODS calendar action date. The original BILLSTATUS day180 convention remains unchanged; no inferred date correction. Default validation remains strict for all other records.68 focused tests passed before fitting.

## Final acquisition, development and reserved comparison

Completed500 feasibility audits,25,000 development/reserve audits and5,000 reserved comparison audits:30,500 candidate audits total. The existing-import check found5,000 scale/reserve114th-Congress records already present as current snapshots; the new work audits their historical evidence. None of the5,000 final-comparison identities was already imported. Do not describe all audited bills as newly acquired platform identities.

After combined temporal and family filtering, the latest development fold has8,812 training bills/227 enactments and3,059 evaluation bills/59 enactments, clearing200/50 evidence gates. All four registered folds completed:

| Evaluation Congress | Training bills / positives | Evaluation bills / positives | Calibrated all-history Brier | Rate-reference Brier |
| --- | ---: | ---: | ---: | ---: |
| 114 | 2302 / 67 | 2788 / 56 | 0.0186513 | 0.0197715 |
| 115 | 4462 / 116 | 2717 / 75 | 0.0251511 | 0.0268439 |
| 116 | 6591 / 158 | 2792 / 48 | 0.0162111 | 0.0169444 |
| 117 | 8812 / 227 | 3059 / 59 | 0.0179902 | 0.0189587 |

Equal-weight mean fold Brier skill versus rate: nested250=2.31%; nested1000=4.93%; all-history=5.08%; recent-Congress=4.66%; calibrated-all-history=5.35%. The last was selected under the frozen rule. These are selection/development statistics, not an independent success claim.

Final challenger trained on11,871 unique historical families with281 enactments;9,496 core cases and2,375 disjoint calibration cases. Calibration intercept0.2108720866, slope1.0764006857. Latest training label availability2023-04-13. Artifact locked2026-11-05T22:21:04Z, before confirmation registration/acquisition. Development fitting and selection replayed exactly. Before confirmation,500 resampling simulations under an assumed2% Brier effect and3,500 eligible cases gave85.2% normal-interval detection frequency; this is conditional sensitivity under exposed117 errors, not guaranteed power. Actual eligible confirmation was smaller.

Confirmation118-s4197 has unresolved introduction-date disagreement (BILLSTATUS2024-04-19 versus introduced-publication action/header2024-04-18). Unlike114-s895, its header does not explicitly explain a legislative day. An explicit pre-scoring amendment quarantines it without a date, feature vector, outcome label or replacement. Included-row evidence requirements remain strict, models remain locked, and the post-registration evidence disposition is disclosed. This is not an untouched confirmatory trial.

Final5,000-candidate screen yields2,315 eligible unique families,29 enactments and2,286 negatives.2,685 exclusions:1,656 known prior/training-family overlaps;794 checkpoints at/after Congress end;198 duplicate selected families;30 missing introduced publications;5 already enacted;1 unavailable introduction publication;1 unresolved introduction-date quarantine.

| Model | Brier (lower better) | Log loss |
| --- | ---: | ---: |
| Original49-row survivor | 0.012144114714759 | 0.066717044692459 |
| Locked calibrated all-history challenger | 0.012143970715225 | 0.065398264352287 |

Brier difference(challenger-original)=-0.000000143999534, only0.001186% relatively lower. Conditional paired95% interval[-0.000179614233499,+0.000214936935199] includes zero. Log loss is1.98% lower, a secondary result. Primary improvement threshold≥2% is unmet, uncertainty includes no difference, and29 positives is below the preregistered50-positive gate. **Preserve the original survivor. No established improvement or promotion.**

Descriptively, the challenger lowered mean prediction for negatives from2.597% to2.192%, but also lowered it for positives from5.259% to3.796%. More data improved several development comparisons but did not establish transfer superiority over the survivor. Do not claim the failure mechanism is causally proven. Further acquisition should support a new registered study; do not extend this scored comparison until it becomes favorable.

Result hash: `5f670ce379c5770d842d988bcae04e3cf7eb3d9ed621544b85e39c9280e5296e`. Challenger lock hash: `d690591ad5deeeaf5031ff5ea18ded283f1db2d69089e092f88696cb43bef9b1`.

## Final verification

70 focused tests passed. All feasibility, initial, reserve and confirmation acquisitions reconstructed exactly offline; development fitting/selection and final scoring replayed exactly. Separate verifier recalculated61,410 probabilities and all Brier/log-loss metrics, checked chronological label availability and family separation, verified102,417 main-campaign/dated-law source files totaling10,397,731,241 bytes, and repeated the conditional bootstrap. A separate check verified the19 calendar-evidence source files. Original survivor hash remains `ffb089cff396415431c2e2b04cb99ebf7d75fe040a777da661bb58d6af9d255c`.

These are machine reproducibility/source checks, not independent human certification. No paid calls, recurring-schedule changes or production model promotion. Publication-proxy, family-linkage, prior118 exposure and rare-outcome limitations remain.

## Platform delivery

Processed all 30,500 audited candidate records into the local platform: 25,400 new bill identities and 5,100 unchanged existing records. Imports retain actual observation timestamps; this does not backdate historical availability or make excluded records eligible for scoring. Four final reports (development comparison, locked model, verification, and reserved comparison) were saved and retrieved successfully through the platform API. Six collections each display the first 100 campaign candidates from one Congress; full memberships remain in the registered protocols. The campaign chat contains the results.

The campaign is complete; the research lease is released. Existing recurring schedules are unchanged. The original survivor remains retained.
