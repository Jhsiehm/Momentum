# Expanded follow-on experiments — November 5, 2026

Completed acquisition and scoring under protocol `f32d4e5421ba2b876554b9e6ca2703c345423b162ed0e01387c49b1460f267fd`. Runtime artifacts remain local in `data/research-runs/expanded-experiments-20261105/`. This is bounded historical research; no live model was promoted.

## Design and evidence

Building on the prior structured L2 .2 survivor configuration, registered ten candidates before fetching outcomes: structured L2 .05/.1/.2/.4/.8, context .2/.4, no-stage .2, no-activity .2/.4. Seed2026110510 selected200 new116Congress training bills and500 new118Congress evaluation bills, partitioned250 development/250 confirmation. Selection exactly reproduces from saved population hashes. Previously used IDs excluded; no replacements or outcome enrichment.

Acquired all700 bills with zero source failures;2,334 cached official-source documents,128,809,694 bytes. Official National Archives law censuses and GovInfo BILLSTATUS/MODS/PREMIS evidence supply labels and publication-based features. Target: own-bill enactment before Congress end, using a180-day checkpoint. Source processing sees labels for validation; model selection uses development only. This is a procedurally held-out same-Congress historical confirmation, not a later temporal/live forecast test.

Family graph includes original training, all700 new rows and previously exposed118 rows. Remove training families overlapping any new evaluation, evaluation linked to exposed families, and confirmation linked to any development family. Final training198/6 positives (49 original/1 positive plus149 new/5 positives), development194/1 positive, confirmation181/2 positives across180 identified families. Original-only comparison refits the49 surviving original rows; it is not the previous frozen model artifact.

Evaluation exclusions:86 late checkpoints,30 exposed-family overlaps,6 missing introduced publications,1 late introduced publication,2 development-family overlaps. Training exclusions:37 late checkpoints,15 duplicate families,1 evaluation overlap,1 already enacted,1 missing introduced publication. New200 training rows contained6 positives; snapshot eligibility161/5; final149/5. Six new positive-law identity/date proofs audited; five eligible. Latest effective training-label proof2021-05-08 precedes every evaluation checkpoint.

## Development results

Brier is mean squared probability error; lower is better.

| Candidate | Development Brier |
| --- | ---: |
| X1 | 0.005520420 |
| X2 | 0.005294199 |
| X3 | 0.005347684 |
| X4 | 0.005669845 |
| X5 | 0.005753852 |
| X6 | 0.005513751 |
| X7 | 0.005666938 |
| X8 | 0.005845733 |
| X9 | 0.005515619 |
| X10 | 0.005670487 |

X2 (structured L2 .05) selected using development only, tie rule fixed beforehand. Selection and artifact hash `0d3e8ed9d74b14d2080f2ee83fd5fcad75e0604f7088b1a402e88ef309c02782` written before any confirmation scores/count summaries. All ten model weights, scalers, predictions and scores retained.

## Locked confirmation

| Model | Brier | Log loss |
| --- | ---: | ---: |
| Selected X2, expanded training | 0.010401584 | 0.061477346 |
| Survivor X1, expanded training | 0.010963495 | 0.065409570 |
| Survivor configuration, original-only training | 0.010343199 | 0.057840269 |
| Smoothed training-rate baseline | 0.011501243 | 0.072276681 |

X2 lowers Brier5.13% relative to the expanded survivor and9.56% relative to the rate baseline on this sample. However, selected-minus-survivor95% paired family-bootstrap interval is[-0.00238696,+0.00048581], and selected-minus-rate[-0.00375688,+0.00040156]; both include zero. Two qualifying enactments are118-HR1097 and118-HR8663.

Adding training examples to the survivor configuration worsens Brier6.00% versus original-only refit. Expanded-minus-original difference is+0.00062030, conditional95% interval[+0.00000710,+0.00170044]. Selected X2 also does not beat the original-only refit on Brier. These results reject any claim that this batch demonstrates automatic improvement. Bootstrap intervals use2,000 family resamples, seed20261024, conditional on the fitted models and Congress; they do not establish generalization across Congresses.

## Audit and reproducibility

Round1 independent design review accepted the bounded historical protocol with family separation, explicit selection lock and no promotion. Round2 independent implementation review found no concrete blockers. Two metadata omissions (new positive label dates and imported prior runner hash) are supplemented in `audit-supplement.json`, without changing protocol or fitted results. Full initial engine dependency bytes retained locally because unrelated workspace code changed concurrently.

Round3 independent verifier passed: all2,334 cached sources, all10 development and3 confirmation predictions, scores and three paired intervals recomputed. Full isolated offline replay passed exactly; an initial missing docs symlink was fixed without changing evidence or models. Twelve reports (ten development, one confirmation, one verification) and seven100-bill collections saved in local chat “Expanded experiments · 700 bills · 10 models · audited results”; all12 report API endpoints checked. All700 current XMLs imported at actual observation time. Summary hash `30e54238c0449cc872997eaf267b60f6ae8a7f8fbcce1e56c7cb93046ed4c34c`; input hash `af9a8a7cdeac6deb01c594e8a1fdfe3a0016a46820385c2089f1d17148b602ca`. Code archive: `docs/operations/reproducers/expanded_experiments_20261105.py`; copy it to the runtime directory as `run.py` to use the registered path assumptions. It requires retained prior cohorts and source caches, which are deliberately excluded from Git. The isolated replay also needs the repository docs directory. Runtime manifests record original absolute paths; portability requires an explicit path mapping, never silently changing frozen artifacts.

## Decision and next checkpoint

Keep X2 as a candidate hypothesis, not an approved production replacement. The new confirmation set is now exposed and must not be reused as fresh validation. Further work should register a later independent Congress and test calibration/base-rate shift, with enough natural positive outcomes; do not repeatedly mine this holdout or add cases until favorable. Research updates change this fitted logistic forecasting model's weights, not the underlying language model's weights.

The user authorized this manual700-bill/10-candidate batch. Scheduled limits and existing heartbeat remain unchanged; no paid provider calls. Source imports use actual current observation times, never backdated historical observations. Shared research lease held through mutation and released at completion.
