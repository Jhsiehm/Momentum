# Momentum paper protocol v1

Dated 2026-11-05 (America/New_York). Status: prospective research specification and blocked readiness gate, **not an executed independent evaluation or external preregistration**. This document fixes the proposed analysis before new final outcomes are scored. Deposit this version, its Git commit and SHA-256 with an independent timestamp service before activating the study. Later amendments require a new version with reasons and exposure disclosures; never rewrite frozen evidence.

## 1. Question and hypotheses

Can a statistical model learned from earlier Congresses improve probabilistic prediction of own-bill public-law enactment, conditional on a bill remaining unenacted at day 180, in later Congresses?

The primary operational hypothesis is that the frozen L2=0.05 challenger reduces Brier loss by at least 2% relative to **each** of the survivor, historical-rate baseline and stage-aware baseline on the prespecified future population. For comparator b define D_b = mean-period(Brier_challenger − 0.98 × Brier_b). The practical null is D_b ≥ 0. The overall claim requires rejecting all three practical nulls under the conditional uncertainty procedure below. Also report ordinary paired differences and Brier Skill Scores (BSS); do not replace the primary test with log loss.

Secondary hypotheses: the challenger does not worsen log loss in either period, and its reliability and positive-event errors improve. These are descriptive safeguards, not additional opportunities to declare primary success. A fixed trained-artifact comparison tests transfer of historical learning, not a causal benefit of each additional training bill and not an adaptive learning rule. The mixed chronological experiments remain exploratory evidence on updating.

A 60% Brier reduction is an aspiration only. It is neither the null hypothesis, a required outcome, a sample-size rule nor a stopping condition.

## 2. Population, outcome and checkpoint

Population: H.R. and S. bills introduced in the registered Congress; exclude resolutions. Predict the bill's own enactment as a **public law strictly before** `engine.store.congress_end(c)` (January 3, 17:00 UTC at the terminal boundary). Incorporation into another vehicle, private-law enactment, originating-chamber passage, and enactment after that boundary are different targets. The day-30 passage programme remains isolated and contributes no labels or features to this paper.

Checkpoint is verified introduction timestamp plus exactly 180 days. Preserve the existing date-only convention: end-of-day 23:59:59 UTC, with timezone normalization before comparison. Require checkpoint strictly before Congress end and no enactment by checkpoint. Positive labels require dated identity-matched public-law evidence, strictly after checkpoint and before the horizon. Enactment on the checkpoint or Congress-end calendar day requires precision adjudication; unresolved boundary ambiguity is excluded, not assigned whichever label improves a score. A negative requires an audited complete horizon census, not absence from a partial API response. A later enactment alone is insufficient negative evidence.

The estimand is restricted to the audited day-180 risk set. It does not describe every introduction, legislative importance or successful provisions. Report the full inventory, introductions, late checkpoints, early enactments, provenance failures, family exclusions, missing predictions, unresolved labels and final scored denominator separately for every Congress and chamber. Never silently replace candidates or treat missing labels as zero.

## 3. Provenance and feature availability

Retain official inventory responses, BILLSTATUS discovery/identity records, introduced bill publications, all eligible version documents, MODS/PREMIS records, final public-law calendars, independent census crosschecks and positive slip-law date proofs. Each retained source needs URL, retrieval time, raw SHA-256, byte length, parser version, effective time, availability bound and provenance rationale. Current imports retain actual observation times. Printed event dates do not establish historical availability.

The six frozen publication-v2 inputs are stage/4, 180/730, capped publication count/30, capped days since last available publication/730, Senate indicator, and capped recent publication count/10. Preserve `sample_publication_v2` version mapping and access-margin rules. These are **publication proxies**, not complete legislative action histories. Do not switch to the general live model's action-based vector merely because dimensions match. Every constituent must be effective and demonstrably available by checkpoint. Current summaries, sponsor totals, later related-bill changes and language-model outputs are excluded as predictors.

Preservation metadata supports availability bounds but does not prove unchanged historical rendition bytes. Human review must address retrospective contamination and source semantics. Keep existing designated human/action-history reviews pending until actually completed; no agent or hash check can certify them. The preparation adapter requires reviewed source receipts and blocks absent evidence. It does not itself verify reviewers' credentials or the truth of source contents.

## 4. Frozen models and baselines

| Method | Fixed specification |
| --- | --- |
| Survivor | Exact 49-row, one-positive structured L2=0.2 artifact from 114/116; 300 steps; no refit or calibration |
| Challenger | Exact accepted convergence-einsum L2=0.05 candidate on 11,871 family representatives from 113–117, 281 positives; 9,496 core and 2,375 calibration rows |
| Historical rate | Beta(1,1): (training positives+1)/(training families+2), on the reviewed registered 113–117 baseline risk set |
| Stage-aware | For stage s, (positive_s + 5 × historical_rate)/(n_s + 5); four fixed publication stages 0–3, empty stages fall back to global rate; no fitted shrinkage or tuning |

The baseline population is the frozen final 11,871-row campaign training list, subject to certification before launch. This avoids artificially handicapping baselines with the survivor's tiny training sample. Report the legacy 2/51 survivor rate only as historical context, not an extra primary comparator. Use the same baseline training rows for both rate models; no evaluation labels enter either fit.

Survivor digest: `ffb089cff396415431c2e2b04cb99ebf7d75fe040a777da661bb58d6af9d255c` (canonical full artifact).

Challenger digest: `149b5f618cd74bcc1974cd502581490e8e8cb3c390baf25b9279e213bb35c0c5` (canonical candidate envelope excluding its self-hash). For the new registration additionally pin `digest(full candidate envelope)`, as required by the adapter; these are distinct hash conventions. Pin raw file SHA-256s too, using [the audit manifest](READINESS_AUDIT_V1.json).

Challenger base: unchanged six inputs, training-only standardization and scale floor 0.1, unpenalized intercept, L2 penalty on standardized slopes, learning rate 0.12, minimum 300 iterations, maximum 20,000, stop at maximum absolute penalized gradient ≤1e-6. Final base reached this after 3,917 iterations. Monotone affine-logit calibration remains 2,000 steps, rate 0.1, ridge 0.01 anchored to identity, nonnegative slope; convergence is claimed only for the base. No new fit is authorized here. Unlike the earlier calibrated L2=0.2 campaign candidate, this changes the penalty and base stopping rule. Unlike the survivor, it also changes training, scaling and calibration. Attribution solely to regularization is limited to the matched exploratory control experiments.

If review invalidates any frozen training member or reveals cross-partition leakage, block this version. Do not silently repair/refit the candidate or let baselines keep inadmissible rows. A changed training population requires a separately frozen successor study.

## 5. Forward-only sequence and protected access

No currently audited historical cohort qualifies as independent validation; see [readiness](VALIDATION_READINESS.md). New identities within 118 do not restore independence. Earlier 110–112 histories are not a forward test of a model trained on 113–117.

Use the proposed whole-Congress 120 and 121 sequence from the existing expansion plan. Freeze protocol, artifacts, baseline training and software before **2027-01-03 17:00 UTC**. A missed deadline requires a new future boundary; do not backdate registration. Register the census-generating inventory rule before the period starts, then append immutable identity discovery manifests before each checkpoint. Reconcile missed discoveries to the final census. A future census cannot honestly be enumerated today.

Keep all four procedures fixed across both periods. Do not update from 120 into 121 or inspect 120 scores to choose 121 rules. An independent custodian seals outcomes until 121 closes and its labels are adjudicated (not before 2031-01-03 17:00 UTC). Operational monitoring can inspect missing captures and hashes, not interim model losses. Public legislative outcomes cannot be made unknowable; record developer awareness and access incidents. Directory names and local Boolean flags are not access controls.

The tested adapter can register finite candidate batches and replay identical paired predictions. The multi-batch census coordinator, protected-label service and prospective issuance adapter are **not certified or activated**. Real scoring fails closed. A production-ready prospective study requires these controls before launch; no historical replay may substitute for them.

## 6. Pairing, family separation and exclusions

Use one prediction per bill/checkpoint, identical cases for all four models. Include all eligible evaluation bills, with related bills treated as clusters. Training uses one representative per adjudicated family. Freeze a global graph including cross-Congress reintroductions, companions and out-of-sample intermediaries; automated identical-title/related-ID links are screening tools only.

For the fixed-artifact study, families known to intersect frozen training or exposed development are excluded from future evaluation under the registered rule. This differs explicitly from the earlier proposed full-census *pre-fit* purge of earlier training rows: the models here already exist and cannot be refitted. Report the excluded population and restricted estimand. New links discovered after issuance invalidate the independence claim until reviewed; retain the original report and publish contamination sensitivity separately, never delete unfavorable predictions silently.

Required evidence failures block the prepared batch; source retries may only retry the same identities. Reviewed exclusions must enumerate every unscored candidate. No accuracy-driven stopping, outcome enrichment or replacement. Unresolved eligible outcomes block the primary complete-case analysis; report coverage, and prespecify missing-outcome sensitivity before unlocking outcomes. Do not imply missingness is random.

## 7. Metrics and aggregation

For a period with n cases, Brier = mean((p−y)^2), log loss = −mean(y log p +(1−y)log(1−p)). Only log loss clips probabilities to [1e-12,1−1e-12]; Brier uses original probabilities. BSS_b = 1−Brier_model/Brier_b; report undefined if comparator loss is zero. Report raw losses, differences and denominators, not an ambiguous “accuracy” percentage.

Primary aggregate loss averages the two period losses equally. Aggregate BSS uses the ratio of these equal-period losses, not the mean of percentage gains. Bill-weighted pooled loss is secondary. Report each period even if signs disagree. Secondary reports include fixed decile reliability bins with counts, mean probabilities and event rates (including empty bins), mean prediction versus prevalence, positive- and negative-specific Brier, and expected event counts. Do not optimize probability bins or decision thresholds on evaluation outcomes. No classification-performance claim is primary.

## 8. Uncertainty and inferential limits

Prespecify 10,000 paired family-cluster bootstrap replicates, seed 20261105. Resample global evaluation-family IDs with replacement, retaining all member bills and their period labels and paired model probabilities. Thus a family spanning periods receives a common multiplicity. Compute period losses and equal-period contrasts in each draw. If a draw has an empty period, mark it invalid and report the count; fewer than 9,000 valid draws blocks interval-based success. Use sorted valid draws with linearly interpolated empirical quantiles.

Use 98.3333% two-sided intervals for each of the three practical-effect contrasts (Bonferroni family-wise 5% across three comparisons; tails 0.0083333333 and 0.9916666667). Also report 95% conditional intervals for ordinary paired differences, labeled descriptive. No subgroup interval is a confirmatory claim. The confidence statements condition on fitted artifacts and observed Congresses; they omit model-selection, training, provenance and future-Congress uncertainty.

Two Congresses do not support reliable Congress-clustered population inference. Account for this dependence by preserving periods, equal weighting, reporting both signs and the range of period effects, and **withholding general population significance claims**. Do not manufacture a precise population interval by treating thousands of bills as independent Congresses. A future design with more untouched periods must register its period-level inference separately. No power claim follows from a positive-event count or an exposed-data simulation. Clustered inference remains a future verified implementation gate, not an output of the current synthetic scoring adapter.

## 9. Success, failure, inconclusive and blocked

Retain the earlier expansion design's conservative readiness floors: at least 200 reviewed positive training families; at least 100 reviewed positive development families if a new selection study is proposed (none here); and at least 100 positive evaluation families in each Congress and 200 unique pooled. These are operational adequacy gates, **not power calculations**. No guarantee of significance follows; the actual reviewed counts remain unknown. Never extend this study until the floors or a desirable result appear.

Conditional success on the registered two-period population requires complete integrity/access gates, the event floors, upper simultaneous interval limits for all D_b below zero, lower point Brier than each comparator in both periods, and no worse challenger log loss in either period against any primary comparator. This does not establish generalized success across future Congresses or authorize promotion.

Failure to establish the practical hypothesis: with all data gates met, if a simultaneous lower bound for any D_b is ≥0, evidence rules out the registered joint practical success within this conditional analysis; report which comparator. Otherwise, unmet success criteria with intervals crossing the practical boundary, conflicting periods or insufficient events are **inconclusive**. A confidence interval above zero for ordinary loss difference is evidence of conditional harm. Missing source, family, issuance or protected-access evidence is **blocked/invalid for independent inference**, not model failure and not an excuse to change the target. Preserve every disposition and secondary finding.

## 10. Reproducibility and publication

Archive protocol/commit, environment and dependency versions, parser source, source hashes, complete candidate/disposition and family manifests, raw and canonical model hashes, exact training/core/calibration memberships, predictions, timestamps, labels and sealed reports. Preserve original warnings and failed attempts. Use exclusive creation and content hashes; external timestamping and custodian access controls must supplement local files. A fresh Git clone intentionally lacks runtime evidence: publish an appropriately licensed reproducibility bundle or a documented acquisition recipe and source availability limitations before submission.

Prospective ledger contract: snapshot the publication features at the exact checkpoint, issue all paired predictions in one atomic receipt within 60 seconds after it, reject if already resolved by issuance, retain actual cutoff/observation/issue times, registration/model/code/source hashes, previous-ledger hash and external timestamp receipt. Missed/late issuance is missing, never replayed as prospective. Review the 60-second operational tolerance as part of preregistration; it is not implemented by the existing live `prospective.capture`, which uses another model and an arbitrary capture age. No shadow forecast has been issued by this preparation task.

Publish a flow diagram, protocol deviations, all comparator results, uncertainty limitations, exposure history, negative findings and TODO citations. Keep public README claims conservative. Independent statistical/source review and the original human gates precede any validation claim. Separate publication acceptance from a future deployment decision; `release_eligible` remains false.
