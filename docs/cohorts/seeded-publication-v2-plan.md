# Seeded publication study v2: evidence amendment plan

Status: design draft, not a registered executable protocol and not permission to score. Prepared after inspecting v1 eligibility and outcome counts. Any implementation must register its exact rules and source requirements before computing v2 predictions or comparative scores. This is a development revision; the same evaluation sample can no longer be described as an unseen holdout.

## Why a new version is necessary

The immutable v1 result is blocked: its 53 provisionally eligible training bills contain two enactments, and its 32 provisionally eligible evaluation bills contain zero enactments. The 116th Congress compiled Statutes evidence has a conservative availability date of 2025-02-13, later than the earliest eligible evaluation checkpoint, 2023-07-19T23:59:59Z. Separately, 118-H.R.5925 has conflicting introduction/publication metadata. These are evidence failures, not reasons to change the sample or optimize the model.

Preserve v1 protocol hash `22df1d85456fbce2994a358ef644be0cb46b91fb8f9d9f5a70f72ed38a690a8a` and result hash `a0243f2d596ae2b70984b710fa06c121c945c03da83fbbcd3bd5c7afcffb036e`. Keep v1 files and frozen core modules untouched. Store a v2 protocol, source receipts, code snapshot, row-level amendment ledger and result independently, with explicit references to v1.

## Fixed components

Copy these fields verbatim from the v1 registered specification, asserting equality before execution:

- All 100 bill IDs, original seed/sample/inventory hashes, and sample `51ee0efb-22bc-406a-87d4-75494e573623`. No replacement, oversampling enacted bills, or dropping an unresolved audit failure.
- Training Congresses 114 and 116; evaluation Congress 118; 180-day checkpoint relative to verified introduction date; own-bill public-law enactment before the constitutional end of Congress.
- The same six version-based features, stage mapping, normalization/caps, version-availability rule, model preprocessing, L2 0.05, learning rate 0.12 and 300 steps. No modern model, summary, action-history, sponsor, topic or outcome text features.
- Beta(1,1)-smoothed training-rate baseline, paired candidate-minus-baseline Brier difference, secondary log loss, and 2,000 evaluation-family bootstrap resamples with seed 20261024.
- Existing family screening and deterministic training-family deduplication; at least 20 eligible training families and both training labels; existing already-enacted and end-of-Congress exclusions. A source audit failure blocks the study instead of disappearing from the denominator.

The amendment is limited to proof of training-outcome availability and independent verification of introduction dates. Any other change requires a separately disclosed subsequent protocol.

## Training-outcome evidence requirements

Retain the original 114th Congress Statutes proof unchanged. Investigation of all 344 individual116 public-law packages found that the complete slip-law set cannot supply an early bound: PL116-283 has late2025 package availability. Preserve this negative finding. Do not call the slips an early complete census.

The proposed primary116 replacement is the final House calendar `CCAL-116hcal-S2`, PUBLIC LAWS section (part7). It must pass all of these checks before scoring:

1. Verify exact official package identity, final-calendar status, referenced PDF identity and successful preservation events under the existing conservative availability rule. Preserve original bytes, URLs, retrieval times and SHA-256 receipts. The complete-list availability bound must precede the earliest eligible evaluation checkpoint, no earlier than Congress end. Package history supports bounded publication availability, not byte-identical historical rendition proof.
2. Extract the entire public-law table and match exactly law numbers1–344 and originating bill identities to the retained complete NARA census. Reject any gap, duplicate, unresolved parse, mismatch or ambiguous mapping. Include originating joint resolutions even though the sample contains only H.R./S. A final contemporaneous calendar supplies closure evidence; today's NARA listing only validates the reconstructed census.
3. Distinguish membership from dates: the calendar table lacks enactment dates. For every sampled116 positive, require a separate official dated law source with exact bill/law identity, enactment date matching NARA and audited historical availability before the earliest evaluation checkpoint. Missing, late or conflicting date evidence blocks all scoring. Do not take a historical date from a presently retrieved source without the original availability audit.
4. Preserve the original already-enacted exclusion, constitutional endpoint and same-day enactment ambiguity rule. Negative labels rely on the historically closed complete membership set; positive labels and checkpoint eligibility also require the dated proof. Do not switch the target to sidestep unavailable dates.

All344 slip-law audits remain diagnostic artifacts, not mandatory early constituents of the replacement calendar proof. This source change is disclosed before scoring, follows the known v1 evidence failure, and cannot make the reused cohort a protected holdout. `data/investigations/earlier-labels/report.json` should preserve the investigation and any unresolved findings. Failed calendar completeness or sampled-positive date verification leaves v2 blocked.

## Introduction-date reconciliation requirements

Use the same deterministic rule for every selected bill. Distinguish three fields: legislative introduction date, publication issuance date, and conservative publication availability. They need not be identical. Do not modify publication availability to make a checkpoint pass.

For each bill, crosscheck BILLSTATUS introduction against a unique introduction action in the exact original introduced-version official MODS metadata. Its issue date must be on or after that introduction date. Original introduced text can additionally corroborate the statement, but does not replace a failed registered action check. Verify Congress, chamber, bill number and version identity. Retain the actual source bytes and provenance with an extracted evidence span and parser version. Where machine extraction is ambiguous, record unresolved status rather than guessing.

If the independent introduction statement agrees with BILLSTATUS while MODS dateIssued differs, retain the agreed introduction date for the 180-day cutoff, retain MODS dateIssued for the publication audit, and record the mismatch and its resolution explicitly. If the independent source disagrees with BILLSTATUS or sources remain ambiguous, block the source audit. Never pick whichever date improves eligibility. A contemporary rendition's textual agreement is not proof that its exact bytes existed at the historical cutoff; preserve that limitation and the original package-availability rule.

Apply the rule across all 100 IDs before fitting. Produce a ledger of old and new introduction date, cutoff, eligible package IDs, feature vector, exclusion and reason; unexpected changes outside the two allowed evidence amendments block execution pending investigation. Do not alter the audit status of the 25 human-review records.

## Execution and stopping rules

Register the complete v2 JSON specification and its digest before scores. Include parent hashes, evidence-rule rationale, known v1 outcome counts, parser/code hashes, exact required report fields, and strict completeness decision. Cache sources in an isolated directory and reconstruct completely offline; hash verification, census equality, denominator preservation, temporal checks and family separation are hard gates.

When any required evidence is missing, write a reproducible blocked report with no fitted model, predictions or numeric performance score. Do not repeatedly search source variants until one yields a favorable performance result. Source discovery must be driven by the predeclared evidentiary requirements and logged independently of model metrics.

If all gates pass, run the unchanged model once, publish all per-bill probabilities and exclusions, compare the paired predictions with the unchanged baseline, and reproduce the locked result offline. Preserve a machine-readable `release_eligible: false`. Reruns verify the registered result; they do not adapt on these evaluation outcomes.

## Interpretation and product constraints

The known zero-enactment evaluation set is a severe limitation. Brier and log loss may be computed if the evidence gates pass, but they only measure performance on observed non-enactments here. A constant low predictor can perform well without identifying successful bills. Discrimination between outcomes cannot be evaluated; calibration across outcomes, sensitivity to enactments, transport to another Congress and a claim of improving every bill are unsupported. Conditional family bootstrap intervals do not cure the missing positive class or account for Congress-level or training-sample uncertainty.

Two positive training examples also leave the fitted pattern unstable. Automatic family screening can miss shared provisions and can overmerge identical generic titles. The complete end-of-Congress inventory is a retrospective sampling frame, and the exclusion of late bills changes the estimand to bills surviving and eligible at 180 days. These limitations must accompany any numerical result.

The UI should label v2 as an evidence-amended development study and show resolved versus unresolved evidence separately from performance. Keep the v1 blocked report available. Do not mark human audits passed, replace live forecasts, promote a model, retune a checkpoint, or describe this revision as validated automatic learning. A subsequent accuracy study needs a newly prespecified larger cohort spanning multiple evaluation periods, sufficient outcome events, and a protected prospective or temporal evaluation process; its sampling must not be chosen to improve the present result.
