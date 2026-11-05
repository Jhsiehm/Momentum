# Five legislative forecasting experiments — November 5, 2026

Five prespecified comparisons on one new sampled cohort. All completed. This is historical development evaluation, not five independent validations. No model promoted.

## Frozen design

100 bills selected without consulting outcome labels, from 16,053 saved 118th-Congress inventory IDs after excluding prior local study/import identities. Python Random seed 2026110505; exact selection registered before acquisition. Full census outcomes were already retained, so “outcome-blind selection” is not a claim that the historical outcome universe was unknowable. Age180 days, own-bill enactment before Congress end. No sample replacements. Five explicit user-requested manual experiments; scheduled budgets/settings unchanged.

## Evidence and denominator

338 official source artifacts retained (12,887,097 bytes); 100 bill records acquired with zero failures. 82 eligible evaluation cases, 81 negative and 1 qualifying positive, across81 identified families. Exclusions:17 checkpoints at/after Congress end;1 missing introduced publication. Training53 distinct families with2 enactments. Recomputed family linkage removed no additional training cases; no identified train/evaluation overlap. Latest required training-label proof May8,2021 precedes earliest evaluation checkpoint July24,2023. Publication/provenance limitations and designated human gates remain.

## Results

| Experiment | Brier | Log loss | Brier minus baseline | Conditional95% interval |
|---|---:|---:|---:|---|
| E1 — Structured reference | 0.01310554 | 0.05431320 | -0.00073441 | [-0.019559, 0.020349] |
| E2 — Previously selected context model | 0.01444596 | 0.05999858 | +0.00060601 | [-0.022318, 0.027238] |
| E3 — Stronger regularization | 0.01103274 | 0.05831082 | -0.00280722 | [-0.010056, 0.003616] |
| E4 — Without legislative stage | 0.01172351 | 0.06572055 | -0.00211644 | [-0.007395, 0.002590] |
| E5 — Without activity signals | 0.01182164 | 0.05149454 | -0.00201831 | [-0.018655, 0.015316] |

Baseline Brier: 0.01383995; log loss: 0.09087765. Lower is better. Baseline probability3/55, from the same53 training families.

## What this teaches us

The previously favored context configuration failed to beat the baseline on this new sample. Stronger structured regularization performed best descriptively on Brier, but this does not authorize selecting/promoting it as validated. The fifth model had the lowest log loss; the registered primary metric remains Brier. All five conditional bootstrap intervals include zero. The comparisons share a cohort and fitted training evidence; multiplicity, training uncertainty and Congress-level uncertainty prevent a winner claim. One qualifying enacted case is too little to establish success detection or calibration. Ablations test predictive feature dependence, not causal effects.

## Audit record

Round1: `/root/five_design_audit` reviewed evidence/methods before registration/scoring. Required exact population, no replacement, combined family filtering, complete provenance, matched metrics and no promotion. Accepted bounded design.

Round2: `/root/five_implementation_audit` reviewed implementation during acquisition and all final results. Dependency snapshot gap corrected via43-file supplementary manifest recorded before scoring. Verified sampling, source/input/result hashes, artifact predictions, direct metrics and bootstrap intervals. No blocking findings.

Round3: `/root/five_verifier` reproduced all5 offline with exact artifact equality, independently recomputed Brier/log loss and baseline, validated all43 dependency hashes, sample reproduction and identical evaluation memberships. PASS for reproducible historical development evidence only. No new broad test suite needed because core model code was unchanged; full numerical reproduction was the meaningful verification.

## Saved artifacts and next action

Protocol, population, source bytes/manifest, frozen training/evaluation inputs, all five weights/scales/predictions, metrics, intervals and hashes: `data/research-runs/five-experiments-20261105/`. Current source XMLs also imported into the main platform at actual retrieval time; no backdating. Collection: “Five experiments · new historical sample · November 5”.

Reproduce: `PYTHONPATH=. python3 data/research-runs/five-experiments-20261105/run.py --offline`.

This sample is now exposed development evidence. Preserve every result; do not tune again and call it a new validation. Next research should pre-register a larger population with enough natural enactments, and a later protected evaluation. Treat strong regularization as a candidate hypothesis, not a promoted winner. No production model or hosted chat weights changed.

Target clarification: H.R.8841 became law January4,2025, after the registered Congress-end deadline, so it is negative for this specific horizon. “One qualifying enactment” does not mean only one sampled bill ever became law.
