# Publication-gate and outcome-parser resolution — November 11, 2026

**Outcome:** the specific publication-metadata selection defect is removed in the separate action-based design, and a narrow outcome-parser amendment recovered 151 eligible positives without changing any feature, family, previously resolved label or unrelated record. Exactly two models were fitted. Context reduced equal-period mean Brier loss by 3.0398245822% against the two-column baseline and 8.5645605931% against the training-rate reference. The advantage over the stronger action-milestone reference was 0.8253361416%, with descriptive uncertainty including no advantage. No model promotion, historical forecast certification or 60% claim.

## Question, versions and adaptation

Question: do active cosponsorship, committee referral breadth and procedural recency improve probability estimates beyond recorded pre-cutoff action milestone and chamber? Type: adaptive retrospective matched comparison using current official records. The experiment uses `action_context_diagnostic_v2`, frozen `action_context_features_v1`, new `action_outcome_resolver_v1`, and the unchanged `matched_text_sparse_v1` optimizer. This is not a head-to-head comparison with the previously failed six-feature publication baseline.

The original publication-completeness rule excluded all 333 records with current public-law assertions. The separate action representation uniformly reprocessed the same 12,000 records and retains 292 of those 333; 40 remain outside the day-180 horizon and one has an action before introduction. Removing that particular exclusion does not prove absence of other selection bias. Whole-history structural validation still considers later record quality.

The unchanged predecessor resolver rejected 231 records because an exact `Signed by President.` annotation used source 9/code 36000 alongside other actions. The registered 231-case contract audit independently found 224 with complete, separate law-list/public-law-action/date agreement, and seven without it. The new resolver treats only that exact supported signing tuple as additional history. It contributes no law identity or enactment date; every such annotation must match the date independently obtained from the existing law evidence. Unsupported wording/sources, contradictions and signature-only records remain unknown. No general grammar expansion or looser law evidence requirement.

All failures remain immutable: [publication-source and selection audit](20261109-official-context-diagnostic.md), [stopped action experiment](20261109-action-context-diagnostic.md). The same exposed data informed these design corrections; this is exploratory development, not untouched confirmation. No scores existed for either stopped predecessor.

## Data, selection and exclusions

Original source: fixed hash-selected 2,000 identities from each Congress113–118, from twelve verified current GovInfo BILLSTATUS directory listings. Excluded 695 protected/previously scored identities under available known-family manifests before sampling. Acquired all 12,000 XMLs, all HTTP200, 192,995,893 bytes. This amendment made zero new requests and no replacements. Exact introduction-plus-180-day cutoff; feature events require calendar date strictly before cutoff. No historical availability of retrieved bytes is asserted.

| Stage | Rows |
| --- | --- |
| Original fixed source sample | 12000 |
| Action-feature eligible | 10095 |
| Feature-ineligible | 1905 |
| Family-selected candidates, identical to stopped run | 8205 |
| Source/feature/family exclusions from original sample | 3795 |
| Final training rows | 5221 |
| Final evaluation rows | 2053 |
| Unknown or out-of-risk labels excluded | 931 |

Feature exclusions: 1,884 unreachable day-180 checkpoints; 20 histories with action dates before introduction;one unsupported action container. Families use current related-bill links plus frozen known edges, including external nodes; priority118 over117 over training, one deterministic representative with the unchanged selection salt. The entire 8,205-row feature/family population matches the stopped action run exactly; no new representative selection based on labels.

| Role | Candidates | Negative proxies | Positive labels | Unknown/out-of-risk | Used |
| --- | --- | --- | --- | --- | --- |
| Training113–116 | 5287 | 5116 | 105 | 66 | 5221 |
| Evaluation117 | 1421 | 919 | 25 | 477 | 944 |
| Evaluation118 | 1497 | 1088 | 21 | 388 | 1109 |

| Label-audit result | Count |
| --- | --- |
| Candidate label records compared | 8205 |
| Previously rejected contract cases | 231 |
| Corroborated contract cases | 224 |
| Unknown→positive, all within prediction horizon | 151 |
| Corroborated but already enacted or cutoff-day ambiguous | 60 |
| Corroborated but outside horizon or end-day ambiguous | 13 |
| Uncorroborated signing-only cases still unknown | 7 |
| Unchanged missing-post-Congress-update unknowns | 851 |
| Changes to previously resolved labels | 0 |
| Changes outside contract cases | 0 |
| Label-delta violations | 0 |

Negative labels are uncertified current-record proxies: supported history, post-Congress update and no enactment assertion. They are not independently certified failures. Seven unsupported cases remain unknown: hr267-115, hr274-115, hr3949-115, hr4661-115, hr624-115, hr863-115 and s585-115.

## Frozen configuration

Baseline: two columns, recorded action milestone/3 and Senate indicator. Challenger: same two plus log1p(active cosponsors), log1p(distinct top-level referred committees), bounded days since action/180, and three missingness indicators—eight columns total. Exact LOC source 9 milestones are origin reporting 5000/14000, origin passage 8000/17000 and presidential presentation 28000. Milestone 0 means no recognized milestone recorded, not certified legislative inactivity.

Fit context medians, means and population standard deviations on training rows only; scaling floor 0.1. Logistic L-BFGS-B, zero initialization, unpenalized intercept, slope L2=0.05, max 20,000 iterations, gradient infinity tolerance1e-6. Exactly one fit per arm, two total, no retries/calibration/tuning/final refit. Both converged after 11 iterations, 12 objective/gradient evaluations. Training rows 5,221, including 105 positive labels. Numerical gradient norms: baseline 7.672356575581796e-7; context 5.646592671874895e-7.

Historical-rate reference: Beta(1,1) on the same training rows. Action-milestone reference: `(category positives + 5 × global rate)/(category rows + 5)`. Both references use training data only. Predictions were saved before evaluation metrics.

## Metrics and denominators

Brier loss is mean squared probability error `(p-y)^2`; log loss is mean binary negative log likelihood, with probabilities clipped to[1e-15,1-1e-15] for scoring. Lower is better. Summary means give equal weight to the two evaluation Congresses, not pooled row weighting. Brier skill is `1 - model Brier/reference Brier`; it is relative loss reduction, not percentage-point accuracy.

| Congress | Cases | Positive labels | Model | Brier | Log loss | Expected positives |
| --- | --- | --- | --- | --- | --- | --- |
| 117 | 944 | 25 | Two-column baseline | 0.024605135149743 | 0.109896824649975 | 17.967344238900 |
| 117 | 944 | 25 | Baseline + context | 0.023638166028822 | 0.099422497734013 | 18.584341380813 |
| 117 | 944 | 25 | Training-rate reference | 0.025819992698670 | 0.123175349363543 | 19.158338119854 |
| 117 | 944 | 25 | Action-milestone reference | 0.023973248836199 | 0.108127650306348 | 16.513191153347 |
| 118 | 1109 | 21 | Two-column baseline | 0.017264267194285 | 0.080102010459599 | 21.700120645559 |
| 118 | 1109 | 21 | Baseline + context | 0.016958479930334 | 0.075243602179661 | 19.914506736540 |
| 118 | 1109 | 21 | Training-rate reference | 0.018579253613804 | 0.093916220901318 | 22.506988320888 |
| 118 | 1109 | 21 | Action-milestone reference | 0.016961244289102 | 0.077282081579112 | 19.898299040153 |

| Model | Equal-period Brier | Equal-period log loss |
| --- | --- | --- |
| Two-column baseline | 0.020934701172014 | 0.094999417554787 |
| Baseline + context | 0.020298322979578 | 0.087333049956837 |
| Training-rate reference | 0.022199623156237 | 0.108545785132431 |
| Action-milestone reference | 0.020467246562650 | 0.092704865942730 |

| Context relative Brier reduction against | Percent |
| --- | --- |
| Two-column baseline | 3.039824582197015 |
| Training-rate reference | 8.564560593116187 |
| Action-milestone reference | 0.8253361416036831 |

Context reduced Brier versus baseline by 3.9299484235% in 117 and 1.7712148480% in 118. Equal-period log loss improved 8.0699101061%. The stronger action-milestone comparison is nearly tied in 118; do not substitute baseline gains for reliable superiority over that reference.

| Congress | Model | Negative n | Negative-class Brier | Positive n | Positive-class Brier |
| --- | --- | --- | --- | --- | --- |
| 117 | Two-column baseline | 919 | 0.0005426974268990793 | 25 | 0.9091403458414965 |
| 117 | Baseline + context | 919 | 0.0007985585998779488 | 25 | 0.8632221351167989 |
| 117 | Training-rate reference | 919 | 0.0004118809244769257 | 25 | 0.9598221815180057 |
| 117 | Action-milestone reference | 919 | 0.0011738657771735849 | 25 | 0.8620785700859642 |
| 118 | Two-column baseline | 1088 | 0.0005491792683604155 | 21 | 0.8832650130707582 |
| 118 | Baseline + context | 1088 | 0.0006328183219250341 | 21 | 0.8627832337374115 |
| 118 | Training-rate reference | 1088 | 0.0004118809244769258 | 21 | 0.9598221815180058 |
| 118 | Action-milestone reference | 1088 | 0.001136740588743409 | 21 | 0.8368212455267361 |

Context improves positive-class loss over baseline but worsens negative-class loss in both periods. Positive-class losses remain high; this is not uniformly strong case-level prediction.

## Uncertainty, validation and limits

Descriptive paired global-family bootstrap: 10,000 draws, seed 20261108,2,053 evaluation families, all 10,000 valid. Reported intervals are 2.5th/97.5th percentiles of equal-period mean loss differences; negative favors context. They do not account for adaptive method development, historical source error or all political-period uncertainty.

| Context minus comparator, Brier | Lower | Upper |
| --- | --- | --- |
| context_minus_anchor | -0.001073071429346582 | -0.0002399131446775514 |
| context_minus_rate | -0.0030400577230656023 | -0.000926778064233621 |
| context_minus_stage | -0.0006906735411425659 | 0.00038242335738182905 |

The descriptive interval favors context over the simple baseline and rate, but spans zero versus the action-milestone reference. Only 46 positive evaluation outcomes across two periods; provisional family graph, missing updates and retrospective timing assertions limit generalization. No historical forecast certification, self-learning deployment, causal claim, promotion or 60%achievement.

All 908 full-suite tests passed in 98.944 seconds; 39 amendment preflight checks passed normally and optimized. Independent replay covered every 8,205 candidate label/family record, 151 label changes, 231 record changes, 931 exclusions, training medians/scales, both objectives/gradients, all 2,053 evaluation probability rows, metrics and 10,000 bootstrap draws, with zero optimizer calls and zero requests. Dense NumPy matrix replay emitted numerical warnings despite finite matching outputs; a separate non-BLAS einsum replay under floating-point errors-as-exceptions passed with maximum probability difference≤8.33e-17. Both verification artifacts are preserved. Software tests are not evidence of forecasting efficacy.

## Exact artifacts, code and reproduction

- [registration.json](../../../data/research-runs/action-context-diagnostic-v2-20261111/registration.json) — SHA-256 `a64e3698372467c6bc540a83ccb9fc76061c5c18f77a2a0b4afa191171953ed1`
- [result.json](../../../data/research-runs/action-context-diagnostic-v2-20261111/result.json) — SHA-256 `cc88b8c446f07901fd6988859c37f338e4cffacda168e0012f34be90a626ca22`
- [feature-population.json](../../../data/research-runs/action-context-diagnostic-v2-20261111/feature-population.json) — SHA-256 `e16f6def45bd5787b336580796e8af1c664879891b37ae7ee310f953d3de0541`
- [label-ledger.json](../../../data/research-runs/action-context-diagnostic-v2-20261111/label-ledger.json) — SHA-256 `80facee9e4d5a7fcb2f7f718e3b4582d3736c8f6867cce17edf43bca35563848`
- [label-delta.json](../../../data/research-runs/action-context-diagnostic-v2-20261111/label-delta.json) — SHA-256 `44554a92909e6353cc61fedfc28910885bfa0e4d5fa55a7d6fc9c0328a4228d9`
- [label-exclusions.json](../../../data/research-runs/action-context-diagnostic-v2-20261111/label-exclusions.json) — SHA-256 `4b9d6d45ae753e18442dea73b3673aa47ae1450972dc2a48e54cf3324dd17f30`
- [fit-inputs.json](../../../data/research-runs/action-context-diagnostic-v2-20261111/fit-inputs.json) — SHA-256 `a97c2bdc9df790ff2e4b45e9b39080fe457c6e7bd6f360db6bf384f280c86ef9`
- [probabilities.json](../../../data/research-runs/action-context-diagnostic-v2-20261111/probabilities.json) — SHA-256 `97e7156f89f8541b17dcfbc39db14f7d4f576522a78f109c150d9b6ff5e564f3`
- [anchor-fit.json](../../../data/research-runs/action-context-diagnostic-v2-20261111/anchor-fit.json) — SHA-256 `cf1b3e69ac33fa64b3641b8b04cbb8187f4f5e4a96631448abbfed58b8075db5`
- [context-fit.json](../../../data/research-runs/action-context-diagnostic-v2-20261111/context-fit.json) — SHA-256 `a8fb1ac72376a265b3aea9918667abe9e734b539bd04dafe046fc1a66ec2c193`
- [independent-review.json](../../../data/research-runs/action-context-diagnostic-v2-20261111/independent-review.json) — SHA-256 `e02428e892ed99520111d7a98a37db23a8be8a0096b58ae1b2e6a04051d03ed1`
- [independent-numerical-einsum.json](../../../data/research-runs/action-context-diagnostic-v2-20261111/independent-numerical-einsum.json) — SHA-256 `ac374995cbae6b2a74607eeda7b9addd865b3a07951c014557da5a108e2f2f20`

These links target ignored local runtime artifacts, not files published to GitHub. Raw XML and complete 12,000-case source/feature ledgers remain in their original acquisition/preparation directories. No timing or monetary-cost measurements are claimed beyond recorded test runtime.

- [Runner](../../../scripts/action_context_diagnostic_v2.py)
- [Resolver](../../../scripts/action_outcome_resolver_v1.py)
- [Fit protocol](../../research/ACTION_CONTEXT_DIAGNOSTIC_FIT_V2.md)
- [Resolver amendment](../../research/20261111-action-outcome-resolver-v1.md)
- [Independent review](../../research/reviews/20261111-action-label-amendment-review.md)

```sh
python3 -m scripts.action_context_diagnostic_v2 --source data/research-runs/official-context-acquisition-v1-20261109 --features data/research-runs/action-context-features-v1-20261109 --predecessor data/research-runs/official-context-diagnostic-v2-20261109/feature-population.json --stopped-run data/research-runs/action-context-diagnostic-v1-20261109 --contract-audit data/research-runs/action-label-contract-diagnostic-v1-20261109 --output data/research-runs/FRESH_REPRODUCTION_DIRECTORY
```

Reproduction would perform two additional fits and is not part of this execution; independent validation above did not refit. Existing output directories must never be overwritten.

## Every audited label-contract case

| Bill | Role | Old y | New y | Enactment date | Final disposition |
| --- | --- | --- | --- | --- | --- |
| hr1071-113 | train | None | None | 2013-05-17 | already_enacted_or_cutoff_date_ambiguous |
| hr1074-115 | train | None | 1 | 2018-12-11 | concordant_own_bill_public_law_action |
| hr1138-114 | train | None | None | 2015-08-07 | already_enacted_or_cutoff_date_ambiguous |
| hr1171-113 | train | None | None | 2013-08-09 | already_enacted_or_cutoff_date_ambiguous |
| hr1193-117 | 117 | None | 1 | 2022-12-20 | concordant_own_bill_public_law_action |
| hr1208-115 | train | None | 1 | 2018-03-20 | concordant_own_bill_public_law_action |
| hr1209-115 | train | None | 1 | 2018-12-06 | concordant_own_bill_public_law_action |
| hr1216-113 | train | None | 1 | 2014-07-25 | concordant_own_bill_public_law_action |
| hr1412-113 | train | None | None | 2013-09-30 | already_enacted_or_cutoff_date_ambiguous |
| hr1448-117 | 117 | None | None | 2021-08-25 | already_enacted_or_cutoff_date_ambiguous |
| hr1492-116 | train | None | None | 2021-01-13 | outside_horizon_or_end_date_ambiguous |
| hr1505-118 | 118 | None | 1 | 2024-12-01 | concordant_own_bill_public_law_action |
| hr1624-114 | train | None | 1 | 2015-10-07 | concordant_own_bill_public_law_action |
| hr1660-115 | train | None | None | 2019-01-03 | outside_horizon_or_end_date_ambiguous |
| hr1830-116 | train | None | 1 | 2020-12-22 | concordant_own_bill_public_law_action |
| hr1858-115 | train | None | 1 | 2018-03-20 | concordant_own_bill_public_law_action |
| hr1972-116 | train | None | 1 | 2019-12-13 | concordant_own_bill_public_law_action |
| hr2030-116 | train | None | None | 2019-04-16 | already_enacted_or_cutoff_date_ambiguous |
| hr208-114 | train | None | 1 | 2015-11-25 | concordant_own_bill_public_law_action |
| hr2137-114 | train | None | 1 | 2016-06-22 | concordant_own_bill_public_law_action |
| hr2151-116 | train | None | 1 | 2019-12-13 | concordant_own_bill_public_law_action |
| hr2167-113 | train | None | None | 2013-08-09 | already_enacted_or_cutoff_date_ambiguous |
| hr2252-114 | train | None | None | 2015-05-19 | already_enacted_or_cutoff_date_ambiguous |
| hr2319-113 | train | None | 1 | 2013-12-26 | concordant_own_bill_public_law_action |
| hr2336-116 | train | None | None | 2019-08-23 | already_enacted_or_cutoff_date_ambiguous |
| hr2359-116 | train | None | 1 | 2020-10-30 | concordant_own_bill_public_law_action |
| hr2372-116 | train | None | 1 | 2020-10-20 | concordant_own_bill_public_law_action |
| hr2423-116 | train | None | 1 | 2019-11-25 | concordant_own_bill_public_law_action |
| hr2458-114 | train | None | 1 | 2016-06-13 | concordant_own_bill_public_law_action |
| hr2544-118 | 118 | None | None | 2023-09-22 | already_enacted_or_cutoff_date_ambiguous |
| hr2600-113 | train | None | 1 | 2014-09-26 | concordant_own_bill_public_law_action |
| hr263-117 | 117 | None | 1 | 2022-12-20 | concordant_own_bill_public_law_action |
| hr267-113 | train | None | 1 | 2013-08-09 | concordant_own_bill_public_law_action |
| hr267-115 | train | None | None | — | Uncorroborated latest-action public-law assertion |
| hr2678-113 | train | None | 1 | 2014-12-16 | concordant_own_bill_public_law_action |
| hr2719-113 | train | None | 1 | 2014-12-18 | concordant_own_bill_public_law_action |
| hr274-115 | train | None | None | — | Uncorroborated latest-action public-law assertion |
| hr2747-113 | train | None | None | 2013-11-21 | already_enacted_or_cutoff_date_ambiguous |
| hr2815-115 | train | None | 1 | 2018-03-23 | concordant_own_bill_public_law_action |
| hr2922-113 | train | None | None | 2013-12-20 | already_enacted_or_cutoff_date_ambiguous |
| hr2928-114 | train | None | 1 | 2016-06-13 | concordant_own_bill_public_law_action |
| hr299-116 | train | None | None | 2019-06-25 | already_enacted_or_cutoff_date_ambiguous |
| hr3059-114 | train | None | None | 2015-11-05 | already_enacted_or_cutoff_date_ambiguous |
| hr3060-113 | train | None | 1 | 2014-06-09 | concordant_own_bill_public_law_action |
| hr3082-114 | train | None | 1 | 2016-06-13 | concordant_own_bill_public_law_action |
| hr3114-114 | train | None | 1 | 2016-07-06 | concordant_own_bill_public_law_action |
| hr324-114 | train | None | 1 | 2015-11-05 | concordant_own_bill_public_law_action |
| hr3262-114 | train | None | 1 | 2016-02-29 | concordant_own_bill_public_law_action |
| hr33-114 | train | None | None | 2015-02-27 | already_enacted_or_cutoff_date_ambiguous |
| hr3302-113 | train | None | None | 2013-11-13 | already_enacted_or_cutoff_date_ambiguous |
| hr3359-117 | 117 | None | 1 | 2022-08-03 | concordant_own_bill_public_law_action |
| hr3375-113 | train | None | 1 | 2014-12-16 | concordant_own_bill_public_law_action |
| hr3383-115 | train | None | 1 | 2018-12-21 | concordant_own_bill_public_law_action |
| hr3460-115 | train | None | None | 2019-01-03 | outside_horizon_or_end_date_ambiguous |
| hr3487-113 | train | None | None | 2013-12-26 | already_enacted_or_cutoff_date_ambiguous |
| hr3508-117 | 117 | None | 1 | 2022-10-11 | concordant_own_bill_public_law_action |
| hr3534-113 | train | None | 1 | 2014-12-16 | concordant_own_bill_public_law_action |
| hr3539-117 | 117 | None | 1 | 2022-10-11 | concordant_own_bill_public_law_action |
| hr3572-113 | train | None | 1 | 2014-12-18 | concordant_own_bill_public_law_action |
| hr3608-118 | 118 | None | 1 | 2024-11-25 | concordant_own_bill_public_law_action |
| hr3614-114 | train | None | None | 2015-09-30 | already_enacted_or_cutoff_date_ambiguous |
| hr3655-115 | train | None | 1 | 2018-03-23 | concordant_own_bill_public_law_action |
| hr3656-115 | train | None | 1 | 2018-03-16 | concordant_own_bill_public_law_action |
| hr3672-118 | 118 | None | None | 2023-07-28 | already_enacted_or_cutoff_date_ambiguous |
| hr3731-115 | train | None | 1 | 2018-04-03 | concordant_own_bill_public_law_action |
| hr3735-114 | train | None | 1 | 2016-06-13 | concordant_own_bill_public_law_action |
| hr3765-113 | train | None | 1 | 2014-08-08 | concordant_own_bill_public_law_action |
| hr3797-118 | 118 | None | 1 | 2024-12-23 | concordant_own_bill_public_law_action |
| hr3893-115 | train | None | None | 2018-03-23 | already_enacted_or_cutoff_date_ambiguous |
| hr3947-118 | 118 | None | 1 | 2024-05-07 | concordant_own_bill_public_law_action |
| hr3949-115 | train | None | None | — | Uncorroborated latest-action public-law assertion |
| hr3996-115 | train | None | 1 | 2018-12-19 | concordant_own_bill_public_law_action |
| hr4010-114 | train | None | 1 | 2016-07-29 | concordant_own_bill_public_law_action |
| hr4028-113 | train | None | None | 2014-08-08 | already_enacted_or_cutoff_date_ambiguous |
| hr4030-113 | train | None | 1 | 2014-12-19 | concordant_own_bill_public_law_action |
| hr4076-113 | train | None | None | 2014-03-21 | already_enacted_or_cutoff_date_ambiguous |
| hr4104-116 | train | None | 1 | 2020-12-04 | concordant_own_bill_public_law_action |
| hr4192-113 | train | None | None | 2014-05-16 | already_enacted_or_cutoff_date_ambiguous |
| hr4194-113 | train | None | 1 | 2014-11-26 | concordant_own_bill_public_law_action |
| hr423-118 | 118 | None | 1 | 2023-07-28 | concordant_own_bill_public_law_action |
| hr4285-115 | train | None | None | 2018-03-23 | already_enacted_or_cutoff_date_ambiguous |
| hr4360-113 | train | None | None | 2014-08-08 | already_enacted_or_cutoff_date_ambiguous |
| hr4406-115 | train | None | 1 | 2018-07-24 | concordant_own_bill_public_law_action |
| hr441-117 | 117 | None | 1 | 2022-12-27 | concordant_own_bill_public_law_action |
| hr4425-114 | train | None | None | 2016-07-29 | already_enacted_or_cutoff_date_ambiguous |
| hr4467-118 | 118 | None | 1 | 2024-12-23 | concordant_own_bill_public_law_action |
| hr4574-115 | train | None | 1 | 2018-07-24 | concordant_own_bill_public_law_action |
| hr4581-118 | 118 | None | 1 | 2024-07-12 | concordant_own_bill_public_law_action |
| hr4605-114 | train | None | None | 2016-06-13 | already_enacted_or_cutoff_date_ambiguous |
| hr4618-114 | train | None | 1 | 2016-12-16 | concordant_own_bill_public_law_action |
| hr4661-115 | train | None | None | — | Uncorroborated latest-action public-law assertion |
| hr4665-114 | train | None | 1 | 2016-12-08 | concordant_own_bill_public_law_action |
| hr4689-115 | train | None | None | 2019-01-10 | outside_horizon_or_end_date_ambiguous |
| hr4693-117 | 117 | None | 1 | 2022-10-19 | concordant_own_bill_public_law_action |
| hr4743-115 | train | None | None | 2018-06-21 | already_enacted_or_cutoff_date_ambiguous |
| hr4751-113 | train | None | None | 2014-09-26 | already_enacted_or_cutoff_date_ambiguous |
| hr4761-114 | train | None | None | 2016-07-29 | already_enacted_or_cutoff_date_ambiguous |
| hr4913-115 | train | None | 1 | 2018-12-06 | concordant_own_bill_public_law_action |
| hr4958-115 | train | None | 1 | 2018-10-09 | concordant_own_bill_public_law_action |
| hr5028-114 | train | None | None | 2016-07-29 | already_enacted_or_cutoff_date_ambiguous |
| hr5111-114 | train | None | 1 | 2016-12-14 | concordant_own_bill_public_law_action |
| hr5309-114 | train | None | 1 | 2016-12-16 | concordant_own_bill_public_law_action |
| hr5356-114 | train | None | 1 | 2016-12-16 | concordant_own_bill_public_law_action |
| hr540-116 | train | None | 1 | 2019-08-21 | concordant_own_bill_public_law_action |
| hr5443-118 | 118 | None | None | 2025-01-04 | outside_horizon_or_end_date_ambiguous |
| hr5536-118 | 118 | None | 1 | 2024-12-11 | concordant_own_bill_public_law_action |
| hr5737-115 | train | None | 1 | 2018-12-06 | concordant_own_bill_public_law_action |
| hr5772-115 | train | None | None | 2018-09-18 | already_enacted_or_cutoff_date_ambiguous |
| hr5784-115 | train | None | 1 | 2018-12-06 | concordant_own_bill_public_law_action |
| hr5792-115 | train | None | 1 | 2018-12-21 | concordant_own_bill_public_law_action |
| hr5799-118 | 118 | None | 1 | 2024-12-11 | concordant_own_bill_public_law_action |
| hr5809-117 | 117 | None | 1 | 2022-10-11 | concordant_own_bill_public_law_action |
| hr588-113 | train | None | None | 2013-07-18 | already_enacted_or_cutoff_date_ambiguous |
| hr594-113 | train | None | 1 | 2014-09-26 | concordant_own_bill_public_law_action |
| hr5943-117 | 117 | None | 1 | 2022-12-27 | concordant_own_bill_public_law_action |
| hr6059-115 | train | None | 1 | 2018-12-21 | concordant_own_bill_public_law_action |
| hr606-115 | train | None | 1 | 2018-12-06 | concordant_own_bill_public_law_action |
| hr6188-118 | 118 | None | 1 | 2025-01-02 | concordant_own_bill_public_law_action |
| hr6192-116 | train | None | None | 2021-01-05 | outside_horizon_or_end_date_ambiguous |
| hr624-115 | train | None | None | — | Uncorroborated latest-action public-law assertion |
| hr6324-118 | 118 | None | 1 | 2024-11-25 | concordant_own_bill_public_law_action |
| hr6427-117 | 117 | None | 1 | 2022-12-27 | concordant_own_bill_public_law_action |
| hr667-113 | train | None | 1 | 2014-01-16 | concordant_own_bill_public_law_action |
| hr6960-118 | 118 | None | 1 | 2024-12-23 | concordant_own_bill_public_law_action |
| hr697-113 | train | None | 1 | 2014-07-25 | concordant_own_bill_public_law_action |
| hr710-114 | train | None | 1 | 2016-12-16 | concordant_own_bill_public_law_action |
| hr7132-117 | 117 | None | 1 | 2022-12-07 | concordant_own_bill_public_law_action |
| hr724-113 | train | None | 1 | 2014-06-09 | concordant_own_bill_public_law_action |
| hr728-114 | train | None | None | 2015-07-20 | already_enacted_or_cutoff_date_ambiguous |
| hr735-117 | 117 | None | 1 | 2022-06-24 | concordant_own_bill_public_law_action |
| hr7607-118 | 118 | None | None | 2025-01-04 | outside_horizon_or_end_date_ambiguous |
| hr7735-117 | 117 | None | 1 | 2022-12-27 | concordant_own_bill_public_law_action |
| hr7791-117 | 117 | None | None | 2022-05-21 | already_enacted_or_cutoff_date_ambiguous |
| hr7903-117 | 117 | None | 1 | 2022-12-20 | concordant_own_bill_public_law_action |
| hr8026-117 | 117 | None | 1 | 2022-12-27 | concordant_own_bill_public_law_action |
| hr8226-117 | 117 | None | 1 | 2022-12-27 | concordant_own_bill_public_law_action |
| hr829-116 | train | None | 1 | 2019-08-21 | concordant_own_bill_public_law_action |
| hr8413-118 | 118 | None | 1 | 2024-12-23 | concordant_own_bill_public_law_action |
| hr845-114 | train | None | 1 | 2016-11-28 | concordant_own_bill_public_law_action |
| hr863-115 | train | None | None | — | Uncorroborated latest-action public-law assertion |
| hr866-116 | train | None | None | 2019-07-25 | already_enacted_or_cutoff_date_ambiguous |
| hr8841-118 | 118 | None | None | 2025-01-04 | outside_horizon_or_end_date_ambiguous |
| hr893-114 | train | None | None | 2015-07-06 | already_enacted_or_cutoff_date_ambiguous |
| hr91-117 | 117 | None | 1 | 2022-10-11 | concordant_own_bill_public_law_action |
| hr984-115 | train | None | 1 | 2018-01-29 | concordant_own_bill_public_law_action |
| s1023-115 | train | None | None | 2019-01-14 | outside_horizon_or_end_date_ambiguous |
| s1044-113 | train | None | 1 | 2014-06-30 | concordant_own_bill_public_law_action |
| s1050-115 | train | None | 1 | 2018-12-20 | concordant_own_bill_public_law_action |
| s1170-114 | train | None | 1 | 2015-12-11 | concordant_own_bill_public_law_action |
| s1172-114 | train | None | 1 | 2016-03-18 | concordant_own_bill_public_law_action |
| s1252-114 | train | None | 1 | 2016-07-20 | concordant_own_bill_public_law_action |
| s1254-113 | train | None | 1 | 2014-06-30 | concordant_own_bill_public_law_action |
| s1351-118 | 118 | None | 1 | 2024-12-23 | concordant_own_bill_public_law_action |
| s1434-113 | train | None | 1 | 2014-12-16 | concordant_own_bill_public_law_action |
| s1436-116 | train | None | None | 2019-06-12 | already_enacted_or_cutoff_date_ambiguous |
| s1471-113 | train | None | None | 2013-12-20 | already_enacted_or_cutoff_date_ambiguous |
| s1608-118 | 118 | None | 1 | 2024-09-13 | concordant_own_bill_public_law_action |
| s1629-114 | train | None | 1 | 2016-01-28 | concordant_own_bill_public_law_action |
| s1638-114 | train | None | 1 | 2016-04-29 | concordant_own_bill_public_law_action |
| s1678-116 | train | None | 1 | 2020-03-26 | concordant_own_bill_public_law_action |
| s1749-116 | train | None | None | 2019-07-25 | already_enacted_or_cutoff_date_ambiguous |
| s1826-114 | train | None | 1 | 2016-03-18 | concordant_own_bill_public_law_action |
| s1858-118 | 118 | None | 1 | 2024-03-18 | concordant_own_bill_public_law_action |
| s1878-114 | train | None | 1 | 2016-09-30 | concordant_own_bill_public_law_action |
| s188-115 | train | None | 1 | 2018-03-27 | concordant_own_bill_public_law_action |
| s1890-114 | train | None | 1 | 2016-05-11 | concordant_own_bill_public_law_action |
| s2036-114 | train | None | None | 2015-11-25 | already_enacted_or_cutoff_date_ambiguous |
| s2101-115 | train | None | 1 | 2018-12-20 | concordant_own_bill_public_law_action |
| s2109-114 | train | None | None | 2016-02-29 | already_enacted_or_cutoff_date_ambiguous |
| s2141-113 | train | None | 1 | 2014-11-26 | concordant_own_bill_public_law_action |
| s2142-113 | train | None | 1 | 2014-12-18 | concordant_own_bill_public_law_action |
| s2152-114 | train | None | None | 2016-02-08 | already_enacted_or_cutoff_date_ambiguous |
| s2152-115 | train | None | 1 | 2018-12-07 | concordant_own_bill_public_law_action |
| s2154-113 | train | None | 1 | 2014-09-26 | concordant_own_bill_public_law_action |
| s216-116 | train | None | 1 | 2019-12-20 | concordant_own_bill_public_law_action |
| s2195-113 | train | None | None | 2014-04-18 | already_enacted_or_cutoff_date_ambiguous |
| s2276-114 | train | None | 1 | 2016-06-22 | concordant_own_bill_public_law_action |
| s231-113 | train | None | 1 | 2014-09-19 | concordant_own_bill_public_law_action |
| s2330-116 | train | None | 1 | 2020-10-30 | concordant_own_bill_public_law_action |
| s2333-117 | 117 | None | None | 2023-01-05 | outside_horizon_or_end_date_ambiguous |
| s2338-113 | train | None | 1 | 2014-12-18 | concordant_own_bill_public_law_action |
| s24-116 | train | None | None | 2019-01-16 | already_enacted_or_cutoff_date_ambiguous |
| s2444-113 | train | None | 1 | 2014-12-18 | concordant_own_bill_public_law_action |
| s2490-117 | 117 | None | 1 | 2022-10-17 | concordant_own_bill_public_law_action |
| s2539-113 | train | None | None | 2014-11-26 | already_enacted_or_cutoff_date_ambiguous |
| s2687-117 | 117 | None | 1 | 2022-06-07 | concordant_own_bill_public_law_action |
| s2734-115 | train | None | None | 2018-07-27 | already_enacted_or_cutoff_date_ambiguous |
| s2771-117 | 117 | None | 1 | 2022-10-17 | concordant_own_bill_public_law_action |
| s2779-115 | train | None | None | 2018-08-08 | already_enacted_or_cutoff_date_ambiguous |
| s2795-118 | 118 | None | None | 2023-10-06 | already_enacted_or_cutoff_date_ambiguous |
| s2834-117 | 117 | None | None | 2023-01-05 | outside_horizon_or_end_date_ambiguous |
| s2840-114 | train | None | None | 2016-07-22 | already_enacted_or_cutoff_date_ambiguous |
| s2845-114 | train | None | None | 2016-07-15 | already_enacted_or_cutoff_date_ambiguous |
| s2850-115 | train | None | None | 2018-08-01 | already_enacted_or_cutoff_date_ambiguous |
| s2854-114 | train | None | 1 | 2016-12-16 | concordant_own_bill_public_law_action |
| s2893-114 | train | None | None | 2016-07-29 | already_enacted_or_cutoff_date_ambiguous |
| s2904-116 | train | None | 1 | 2020-12-23 | concordant_own_bill_public_law_action |
| s2971-114 | train | None | 1 | 2016-12-16 | concordant_own_bill_public_law_action |
| s30-118 | 118 | None | None | 2023-07-18 | already_enacted_or_cutoff_date_ambiguous |
| s3031-115 | train | None | None | 2019-01-03 | outside_horizon_or_end_date_ambiguous |
| s309-113 | train | None | 1 | 2014-05-30 | concordant_own_bill_public_law_action |
| s3105-116 | train | None | 1 | 2020-10-01 | concordant_own_bill_public_law_action |
| s3170-115 | train | None | None | 2018-12-21 | already_enacted_or_cutoff_date_ambiguous |
| s3201-116 | train | None | None | 2020-02-06 | already_enacted_or_cutoff_date_ambiguous |
| s324-115 | train | None | 1 | 2018-03-27 | concordant_own_bill_public_law_action |
| s337-114 | train | None | 1 | 2016-06-30 | concordant_own_bill_public_law_action |
| s3419-118 | 118 | None | 1 | 2024-11-25 | concordant_own_bill_public_law_action |
| s3470-117 | 117 | None | 1 | 2022-10-17 | concordant_own_bill_public_law_action |
| s3510-117 | 117 | None | 1 | 2022-12-05 | concordant_own_bill_public_law_action |
| s3587-116 | train | None | 1 | 2020-12-04 | concordant_own_bill_public_law_action |
| s3655-117 | 117 | None | 1 | 2022-12-05 | concordant_own_bill_public_law_action |
| s3706-118 | 118 | None | 1 | 2024-07-30 | concordant_own_bill_public_law_action |
| s3773-117 | 117 | None | None | 2023-01-05 | outside_horizon_or_end_date_ambiguous |
| s3826-117 | 117 | None | 1 | 2022-12-02 | concordant_own_bill_public_law_action |
| s3938-118 | 118 | None | 1 | 2024-12-23 | concordant_own_bill_public_law_action |
| s4351-118 | 118 | None | None | 2024-09-26 | already_enacted_or_cutoff_date_ambiguous |
| s461-116 | train | None | 1 | 2020-12-31 | concordant_own_bill_public_law_action |
| s474-118 | 118 | None | 1 | 2024-05-07 | concordant_own_bill_public_law_action |
| s476-113 | train | None | 1 | 2014-09-26 | concordant_own_bill_public_law_action |
| s540-113 | train | None | 1 | 2014-02-15 | concordant_own_bill_public_law_action |
| s578-117 | 117 | None | None | 2021-04-23 | already_enacted_or_cutoff_date_ambiguous |
| s585-115 | train | None | None | — | Uncorroborated latest-action public-law assertion |
| s670-118 | 118 | None | 1 | 2024-10-01 | concordant_own_bill_public_law_action |
| s693-116 | train | None | 1 | 2019-11-07 | concordant_own_bill_public_law_action |
| s744-116 | train | None | None | 2019-07-25 | already_enacted_or_cutoff_date_ambiguous |
| s808-114 | train | None | 1 | 2015-12-18 | concordant_own_bill_public_law_action |
| s812-117 | 117 | None | 1 | 2022-05-13 | concordant_own_bill_public_law_action |
| s979-116 | train | None | 1 | 2020-12-31 | concordant_own_bill_public_law_action |
| s982-116 | train | None | 1 | 2020-10-10 | concordant_own_bill_public_law_action |
| s984-114 | train | None | None | 2015-07-30 | already_enacted_or_cutoff_date_ambiguous |
| s994-113 | train | None | 1 | 2014-05-09 | concordant_own_bill_public_law_action |

## Every evaluation case

Probabilities are from the saved fixed fits; y=0 is a negative proxy. All cases contribute to both models and both references.

| Bill | Congress | y | Baseline p | Context p | Rate p | Milestone p | Baseline squared error | Context squared error |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hr100-117 | 117 | 0 | 0.015139467208 | 0.017286702898 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000298830097 |
| hr1007-117 | 117 | 0 | 0.015139467208 | 0.020335357937 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000413526782 |
| hr103-117 | 117 | 0 | 0.015139467208 | 0.011712276748 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000137177427 |
| hr1034-117 | 117 | 0 | 0.015139467208 | 0.023924535976 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000572383422 |
| hr1043-117 | 117 | 0 | 0.015139467208 | 0.011786590837 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000138923724 |
| hr1046-117 | 117 | 0 | 0.015139467208 | 0.014875921549 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000221293042 |
| hr1047-117 | 117 | 0 | 0.015139467208 | 0.015253973817 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000232683717 |
| hr106-117 | 117 | 0 | 0.015139467208 | 0.011320126269 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128145259 |
| hr1069-117 | 117 | 0 | 0.015139467208 | 0.012194701213 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000148710738 |
| hr107-117 | 117 | 0 | 0.015139467208 | 0.012350703999 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000152539889 |
| hr1072-117 | 117 | 0 | 0.015139467208 | 0.022259094577 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000495467291 |
| hr1086-117 | 117 | 0 | 0.015139467208 | 0.013061520738 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000170603324 |
| hr1104-117 | 117 | 0 | 0.015139467208 | 0.015784510929 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000249150785 |
| hr1110-117 | 117 | 0 | 0.015139467208 | 0.019753561137 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000390203178 |
| hr1112-117 | 117 | 0 | 0.104531149070 | 0.089434021146 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.007998444138 |
| hr1128-117 | 117 | 0 | 0.015139467208 | 0.010679581838 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114053468 |
| hr1140-117 | 117 | 0 | 0.015139467208 | 0.023529640814 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000553643997 |
| hr1143-117 | 117 | 0 | 0.015139467208 | 0.021496794541 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000462112176 |
| hr116-117 | 117 | 0 | 0.015139467208 | 0.018011181240 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000324402650 |
| hr1169-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr1175-117 | 117 | 0 | 0.015139467208 | 0.011786590837 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000138923724 |
| hr1182-117 | 117 | 0 | 0.015139467208 | 0.025468319726 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000648635310 |
| hr1185-117 | 117 | 0 | 0.015139467208 | 0.012806271724 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000164000595 |
| hr119-117 | 117 | 0 | 0.015139467208 | 0.010679581838 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114053468 |
| hr1193-117 | 117 | 1 | 0.015139467208 | 0.016422609794 | 0.020294849703 | 0.010486655910 | 0.969950269051 | 0.967424482524 |
| hr1198-117 | 117 | 0 | 0.015139467208 | 0.020355618797 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000414351217 |
| hr1204-117 | 117 | 0 | 0.015139467208 | 0.028406498205 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000806929140 |
| hr1233-117 | 117 | 0 | 0.015139467208 | 0.012843534864 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000164956388 |
| hr124-117 | 117 | 0 | 0.015139467208 | 0.013858334388 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000192053432 |
| hr1265-117 | 117 | 0 | 0.015139467208 | 0.018729398319 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000350790361 |
| hr1267-117 | 117 | 0 | 0.015139467208 | 0.015760670105 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000248398722 |
| hr1269-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr127-117 | 117 | 0 | 0.015139467208 | 0.014419401022 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000207919126 |
| hr1287-117 | 117 | 0 | 0.015139467208 | 0.014686705028 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000215699305 |
| hr1301-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr131-117 | 117 | 0 | 0.015139467208 | 0.014419401022 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000207919126 |
| hr1313-117 | 117 | 0 | 0.015139467208 | 0.017782876653 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000316230702 |
| hr1316-117 | 117 | 0 | 0.015139467208 | 0.024468137945 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000598689775 |
| hr1348-117 | 117 | 0 | 0.015139467208 | 0.010085800166 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000101723365 |
| hr1366-117 | 117 | 0 | 0.015139467208 | 0.021587065049 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000466001377 |
| hr1367-117 | 117 | 0 | 0.015139467208 | 0.012492693490 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000156067391 |
| hr1381-117 | 117 | 0 | 0.015139467208 | 0.015454972762 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000238856183 |
| hr1384-117 | 117 | 0 | 0.015139467208 | 0.015914092459 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000253258339 |
| hr1387-117 | 117 | 0 | 0.015139467208 | 0.019353608630 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000374562167 |
| hr1411-117 | 117 | 0 | 0.015139467208 | 0.015373841665 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000236355008 |
| hr1431-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr1435-117 | 117 | 0 | 0.015139467208 | 0.017312811515 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000299733443 |
| hr1440-117 | 117 | 0 | 0.015139467208 | 0.023414576408 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000548242388 |
| hr1441-117 | 117 | 0 | 0.015139467208 | 0.021694929289 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000470669957 |
| hr146-117 | 117 | 0 | 0.015139467208 | 0.011320126269 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128145259 |
| hr1479-117 | 117 | 0 | 0.015139467208 | 0.012717265088 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000161728831 |
| hr1481-117 | 117 | 0 | 0.015139467208 | 0.018258349280 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000333367318 |
| hr1486-117 | 117 | 0 | 0.015139467208 | 0.011320126269 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128145259 |
| hr1487-117 | 117 | 0 | 0.104531149070 | 0.088238826713 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.007786090540 |
| hr1501-117 | 117 | 0 | 0.015139467208 | 0.011712276748 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000137177427 |
| hr1526-117 | 117 | 0 | 0.015139467208 | 0.017250537775 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000297581054 |
| hr1527-117 | 117 | 0 | 0.015139467208 | 0.023223052130 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000539310150 |
| hr1561-117 | 117 | 0 | 0.015139467208 | 0.013641761555 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000186097658 |
| hr1580-117 | 117 | 0 | 0.015139467208 | 0.011786590837 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000138923724 |
| hr1594-117 | 117 | 0 | 0.015139467208 | 0.013612083986 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000185288830 |
| hr1611-117 | 117 | 0 | 0.015139467208 | 0.014171638720 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000200835344 |
| hr1616-117 | 117 | 0 | 0.015139467208 | 0.011399467400 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000129947857 |
| hr1622-117 | 117 | 0 | 0.015139467208 | 0.014041694633 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000197169188 |
| hr1632-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr1634-117 | 117 | 0 | 0.015139467208 | 0.012225484268 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000149462466 |
| hr1637-117 | 117 | 0 | 0.015139467208 | 0.013499397979 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000182233746 |
| hr164-117 | 117 | 0 | 0.015139467208 | 0.033141743929 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.001098375191 |
| hr1649-117 | 117 | 0 | 0.015139467208 | 0.011712276748 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000137177427 |
| hr1663-117 | 117 | 0 | 0.015139467208 | 0.020470703839 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000419049716 |
| hr1666-117 | 117 | 0 | 0.015139467208 | 0.011320126269 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128145259 |
| hr1677-117 | 117 | 0 | 0.015139467208 | 0.013698285222 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000187643018 |
| hr1687-117 | 117 | 0 | 0.015139467208 | 0.022297101296 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000497160726 |
| hr1699-117 | 117 | 0 | 0.015139467208 | 0.026709045174 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000713373094 |
| hr1734-117 | 117 | 0 | 0.015139467208 | 0.025108132709 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000630418328 |
| hr1747-117 | 117 | 0 | 0.015139467208 | 0.012575593925 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000158145563 |
| hr1755-117 | 117 | 0 | 0.015139467208 | 0.022750350475 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000517578447 |
| hr1757-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr1761-117 | 117 | 0 | 0.015139467208 | 0.013002133056 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000169055464 |
| hr1773-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr1779-117 | 117 | 0 | 0.015139467208 | 0.020501521022 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000420312364 |
| hr1786-117 | 117 | 0 | 0.015139467208 | 0.014767978405 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000218093186 |
| hr1803-117 | 117 | 0 | 0.015139467208 | 0.013490551133 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000181994970 |
| hr1815-117 | 117 | 0 | 0.015139467208 | 0.023337779925 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000544651972 |
| hr1816-117 | 117 | 0 | 0.015139467208 | 0.013828825768 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000191236422 |
| hr1824-117 | 117 | 0 | 0.015139467208 | 0.009822460138 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000096480723 |
| hr1828-117 | 117 | 0 | 0.015139467208 | 0.011320126269 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128145259 |
| hr1831-117 | 117 | 0 | 0.015139467208 | 0.011320126269 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128145259 |
| hr1832-117 | 117 | 0 | 0.015139467208 | 0.014357061203 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000206125206 |
| hr1835-117 | 117 | 0 | 0.015139467208 | 0.015195442338 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000230901468 |
| hr1837-117 | 117 | 0 | 0.015139467208 | 0.013478361472 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000181666228 |
| hr1851-117 | 117 | 0 | 0.015139467208 | 0.020976258454 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000440003419 |
| hr1869-117 | 117 | 0 | 0.015139467208 | 0.020831666703 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000433958338 |
| hr1894-117 | 117 | 0 | 0.015139467208 | 0.015566502002 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000242315985 |
| hr1910-117 | 117 | 0 | 0.015139467208 | 0.021068498841 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000443881643 |
| hr1913-117 | 117 | 0 | 0.015139467208 | 0.011712276748 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000137177427 |
| hr192-117 | 117 | 0 | 0.015139467208 | 0.011862182148 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000140711365 |
| hr1943-117 | 117 | 0 | 0.015139467208 | 0.017074060535 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000291523543 |
| hr1947-117 | 117 | 0 | 0.015139467208 | 0.011320126269 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128145259 |
| hr1952-117 | 117 | 0 | 0.015139467208 | 0.015139337378 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000229199536 |
| hr1961-117 | 117 | 0 | 0.015139467208 | 0.018818392590 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000354131900 |
| hr1964-117 | 117 | 0 | 0.015139467208 | 0.012957535080 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000167897715 |
| hr1981-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr199-117 | 117 | 0 | 0.015139467208 | 0.013002133056 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000169055464 |
| hr201-117 | 117 | 0 | 0.015139467208 | 0.012028945978 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000144695541 |
| hr2017-117 | 117 | 0 | 0.015139467208 | 0.009822460138 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000096480723 |
| hr202-117 | 117 | 0 | 0.015139467208 | 0.011712276748 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000137177427 |
| hr2039-117 | 117 | 0 | 0.015139467208 | 0.012225484268 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000149462466 |
| hr2042-117 | 117 | 0 | 0.015139467208 | 0.011712276748 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000137177427 |
| hr2045-117 | 117 | 0 | 0.015139467208 | 0.012082662097 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000145990723 |
| hr205-117 | 117 | 0 | 0.015139467208 | 0.011862182148 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000140711365 |
| hr2054-117 | 117 | 0 | 0.015139467208 | 0.015144426328 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000229353649 |
| hr2061-117 | 117 | 0 | 0.015139467208 | 0.020401789284 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000416233006 |
| hr2062-117 | 117 | 0 | 0.104531149070 | 0.150247684599 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.022574366727 |
| hr2065-117 | 117 | 0 | 0.015139467208 | 0.011320126269 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128145259 |
| hr2076-117 | 117 | 0 | 0.015139467208 | 0.015576809541 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000242636995 |
| hr2078-117 | 117 | 0 | 0.015139467208 | 0.010085800166 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000101723365 |
| hr2087-117 | 117 | 0 | 0.015139467208 | 0.022524817155 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000507367388 |
| hr2111-117 | 117 | 0 | 0.015139467208 | 0.026949050997 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000726251350 |
| hr212-117 | 117 | 0 | 0.015139467208 | 0.011704587199 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000136997361 |
| hr2136-117 | 117 | 0 | 0.015139467208 | 0.012194701213 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000148710738 |
| hr2143-117 | 117 | 0 | 0.015139467208 | 0.014991757982 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000224752807 |
| hr215-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr2151-117 | 117 | 0 | 0.015139467208 | 0.011712276748 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000137177427 |
| hr2157-117 | 117 | 0 | 0.015139467208 | 0.009822460138 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000096480723 |
| hr2163-117 | 117 | 0 | 0.015139467208 | 0.015632548124 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000244376561 |
| hr2166-117 | 117 | 0 | 0.015139467208 | 0.015182800002 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000230517416 |
| hr2168-117 | 117 | 0 | 0.015139467208 | 0.015272780027 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000233257810 |
| hr218-117 | 117 | 0 | 0.015139467208 | 0.020327909734 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000413223914 |
| hr2224-117 | 117 | 0 | 0.015139467208 | 0.013612083986 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000185288830 |
| hr2227-117 | 117 | 0 | 0.015139467208 | 0.013935088555 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000194186693 |
| hr2257-117 | 117 | 0 | 0.015139467208 | 0.012238746089 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000149786906 |
| hr2261-117 | 117 | 0 | 0.015139467208 | 0.013396853133 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000179475674 |
| hr2271-117 | 117 | 0 | 0.015139467208 | 0.013245770830 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000175450445 |
| hr229-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr2312-117 | 117 | 0 | 0.015139467208 | 0.011320126269 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128145259 |
| hr2328-117 | 117 | 0 | 0.015139467208 | 0.046703034467 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.002181173428 |
| hr2338-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr2341-117 | 117 | 0 | 0.015139467208 | 0.012413983372 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000154106983 |
| hr2346-117 | 117 | 0 | 0.015139467208 | 0.012843534864 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000164956388 |
| hr2349-117 | 117 | 0 | 0.015139467208 | 0.013328326107 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000177644277 |
| hr2350-117 | 117 | 0 | 0.015139467208 | 0.012413983372 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000154106983 |
| hr2352-117 | 117 | 0 | 0.015139467208 | 0.012933413670 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000167273189 |
| hr2359-117 | 117 | 0 | 0.015139467208 | 0.018556624753 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000344348322 |
| hr236-117 | 117 | 0 | 0.015139467208 | 0.010327977552 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000106667120 |
| hr2362-117 | 117 | 0 | 0.015139467208 | 0.012717265088 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000161728831 |
| hr2368-117 | 117 | 0 | 0.015139467208 | 0.022609848364 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000511205243 |
| hr2369-117 | 117 | 0 | 0.015139467208 | 0.011399467400 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000129947857 |
| hr237-117 | 117 | 0 | 0.015139467208 | 0.014073277742 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000198057146 |
| hr2384-117 | 117 | 0 | 0.015139467208 | 0.014465872857 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000209261478 |
| hr2385-117 | 117 | 0 | 0.015139467208 | 0.027132281913 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000736160722 |
| hr2396-117 | 117 | 0 | 0.015139467208 | 0.014027273096 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000196764391 |
| hr2410-117 | 117 | 0 | 0.015139467208 | 0.011786590837 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000138923724 |
| hr2413-117 | 117 | 0 | 0.015139467208 | 0.011712276748 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000137177427 |
| hr2419-117 | 117 | 0 | 0.015139467208 | 0.016065229424 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000258091596 |
| hr242-117 | 117 | 0 | 0.015139467208 | 0.016263639634 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000264505974 |
| hr2421-117 | 117 | 0 | 0.015139467208 | 0.013328326107 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000177644277 |
| hr2432-117 | 117 | 0 | 0.015139467208 | 0.022975928428 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000527893287 |
| hr2440-117 | 117 | 0 | 0.015139467208 | 0.013944222799 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000194441349 |
| hr2443-117 | 117 | 0 | 0.015139467208 | 0.017193028853 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000295600241 |
| hr2452-117 | 117 | 0 | 0.015139467208 | 0.015351457155 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000235667237 |
| hr2453-117 | 117 | 0 | 0.015139467208 | 0.013747747432 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000189000559 |
| hr2476-117 | 117 | 0 | 0.015139467208 | 0.011794333617 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000139106305 |
| hr2482-117 | 117 | 0 | 0.015139467208 | 0.012717265088 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000161728831 |
| hr2484-117 | 117 | 0 | 0.015139467208 | 0.013698285222 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000187643018 |
| hr2486-117 | 117 | 0 | 0.015139467208 | 0.014384163206 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000206904151 |
| hr2487-117 | 117 | 0 | 0.015139467208 | 0.014831652528 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000219977917 |
| hr249-117 | 117 | 0 | 0.015139467208 | 0.012943013729 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000167521604 |
| hr2491-117 | 117 | 0 | 0.015139467208 | 0.014969565775 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000224087899 |
| hr2493-117 | 117 | 0 | 0.015139467208 | 0.012640300391 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000159777194 |
| hr2496-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr2517-117 | 117 | 0 | 0.015139467208 | 0.015839162174 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000250879058 |
| hr2518-117 | 117 | 0 | 0.015139467208 | 0.019219982407 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000369407724 |
| hr2527-117 | 117 | 0 | 0.015139467208 | 0.017312811515 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000299733443 |
| hr2544-117 | 117 | 0 | 0.015139467208 | 0.013478361472 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000181666228 |
| hr2546-117 | 117 | 0 | 0.015139467208 | 0.014319345380 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000205043652 |
| hr2555-117 | 117 | 0 | 0.015139467208 | 0.011712276748 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000137177427 |
| hr256-117 | 117 | 0 | 0.104531149070 | 0.214042209976 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.045814067651 |
| hr2561-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr2562-117 | 117 | 0 | 0.015139467208 | 0.018217045927 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000331860762 |
| hr2573-117 | 117 | 0 | 0.015139467208 | 0.015875086464 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000252018370 |
| hr2582-117 | 117 | 0 | 0.015139467208 | 0.012413983372 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000154106983 |
| hr2590-117 | 117 | 0 | 0.015139467208 | 0.014246414326 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000202960321 |
| hr260-117 | 117 | 0 | 0.015139467208 | 0.017638280202 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000311108929 |
| hr2603-117 | 117 | 0 | 0.015139467208 | 0.011712276748 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000137177427 |
| hr2608-117 | 117 | 0 | 0.015139467208 | 0.014297256556 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000204411545 |
| hr2609-117 | 117 | 0 | 0.015139467208 | 0.011712276748 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000137177427 |
| hr2627-117 | 117 | 0 | 0.015139467208 | 0.012225484268 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000149462466 |
| hr263-117 | 117 | 1 | 0.015139467208 | 0.021631202124 | 0.020294849703 | 0.010486655910 | 0.969950269051 | 0.957205504657 |
| hr2633-117 | 117 | 0 | 0.015139467208 | 0.011712276748 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000137177427 |
| hr2640-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr2642-117 | 117 | 0 | 0.015139467208 | 0.018621535280 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000346761576 |
| hr2648-117 | 117 | 0 | 0.015139467208 | 0.013707266403 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000187889152 |
| hr2652-117 | 117 | 0 | 0.015139467208 | 0.011320126269 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128145259 |
| hr2654-117 | 117 | 0 | 0.015139467208 | 0.016273788211 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000264836183 |
| hr2699-117 | 117 | 0 | 0.015139467208 | 0.012413983372 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000154106983 |
| hr2705-117 | 117 | 0 | 0.015139467208 | 0.014592654134 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000212945555 |
| hr2716-117 | 117 | 0 | 0.015139467208 | 0.015159852915 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000229821140 |
| hr2722-117 | 117 | 0 | 0.015139467208 | 0.012717265088 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000161728831 |
| hr2731-117 | 117 | 0 | 0.015139467208 | 0.014517229888 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000210749964 |
| hr2734-117 | 117 | 0 | 0.015139467208 | 0.044845982009 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.002011162102 |
| hr2743-117 | 117 | 0 | 0.015139467208 | 0.011399467400 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000129947857 |
| hr2765-117 | 117 | 0 | 0.015139467208 | 0.011998623593 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000143966968 |
| hr2770-117 | 117 | 0 | 0.015139467208 | 0.013769514092 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000189599518 |
| hr2776-117 | 117 | 0 | 0.015139467208 | 0.011712276748 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000137177427 |
| hr2789-117 | 117 | 0 | 0.015139467208 | 0.018751432432 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000351616218 |
| hr2792-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr2799-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr2801-117 | 117 | 0 | 0.015139467208 | 0.010156578956 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000103156096 |
| hr2829-117 | 117 | 0 | 0.015139467208 | 0.022334645035 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000498836369 |
| hr2837-117 | 117 | 0 | 0.015139467208 | 0.023671059776 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000560319071 |
| hr2839-117 | 117 | 0 | 0.015139467208 | 0.044928880836 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.002018604333 |
| hr2843-117 | 117 | 0 | 0.015139467208 | 0.009822460138 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000096480723 |
| hr2880-117 | 117 | 0 | 0.015139467208 | 0.009822460138 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000096480723 |
| hr2881-117 | 117 | 0 | 0.015139467208 | 0.013093107009 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000171429451 |
| hr2886-117 | 117 | 0 | 0.015139467208 | 0.014698022481 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000216031865 |
| hr2887-117 | 117 | 0 | 0.015139467208 | 0.012895893170 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000166304061 |
| hr2896-117 | 117 | 0 | 0.015139467208 | 0.013061520738 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000170603324 |
| hr2919-117 | 117 | 0 | 0.015139467208 | 0.017172818366 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000294905691 |
| hr2920-117 | 117 | 0 | 0.015139467208 | 0.014613366162 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000213550471 |
| hr2921-117 | 117 | 0 | 0.015139467208 | 0.012957535080 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000167897715 |
| hr2931-117 | 117 | 0 | 0.104531149070 | 0.115423623260 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.013322612807 |
| hr2936-117 | 117 | 0 | 0.015139467208 | 0.013991995998 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000195775952 |
| hr2959-117 | 117 | 0 | 0.104531149070 | 0.065264637743 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.004259472940 |
| hr2966-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr2976-117 | 117 | 0 | 0.015139467208 | 0.013061520738 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000170603324 |
| hr2979-117 | 117 | 0 | 0.015139467208 | 0.012194701213 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000148710738 |
| hr2984-117 | 117 | 0 | 0.015139467208 | 0.013002133056 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000169055464 |
| hr2986-117 | 117 | 0 | 0.015139467208 | 0.016137158558 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000260407886 |
| hr2987-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr2990-117 | 117 | 0 | 0.015139467208 | 0.010085800166 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000101723365 |
| hr2995-117 | 117 | 0 | 0.015139467208 | 0.011998623593 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000143966968 |
| hr3006-117 | 117 | 0 | 0.015139467208 | 0.010679581838 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114053468 |
| hr3011-117 | 117 | 0 | 0.015139467208 | 0.011998623593 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000143966968 |
| hr3020-117 | 117 | 0 | 0.015139467208 | 0.013603164310 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000185046079 |
| hr3021-117 | 117 | 0 | 0.015139467208 | 0.011712276748 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000137177427 |
| hr3023-117 | 117 | 0 | 0.015139467208 | 0.012716007248 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000161696840 |
| hr3025-117 | 117 | 0 | 0.015139467208 | 0.011960155147 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000143045311 |
| hr3027-117 | 117 | 0 | 0.015139467208 | 0.018174547009 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000330314159 |
| hr3031-117 | 117 | 0 | 0.015139467208 | 0.014082501273 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000198316842 |
| hr3062-117 | 117 | 0 | 0.015139467208 | 0.009960837708 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000099218288 |
| hr3064-117 | 117 | 0 | 0.015139467208 | 0.012575593925 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000158145563 |
| hr3068-117 | 117 | 0 | 0.015139467208 | 0.011320126269 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128145259 |
| hr3075-117 | 117 | 0 | 0.015139467208 | 0.042838717693 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.001835155734 |
| hr3083-117 | 117 | 0 | 0.015139467208 | 0.013612083986 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000185288830 |
| hr3087-117 | 117 | 0 | 0.015139467208 | 0.014103946445 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000198921305 |
| hr3100-117 | 117 | 0 | 0.015139467208 | 0.021038911082 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000442635780 |
| hr3106-117 | 117 | 0 | 0.015139467208 | 0.011712276748 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000137177427 |
| hr3114-117 | 117 | 0 | 0.015139467208 | 0.014690618221 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000215814264 |
| hr312-117 | 117 | 0 | 0.015139467208 | 0.011761794655 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000138339813 |
| hr3137-117 | 117 | 0 | 0.015139467208 | 0.012225484268 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000149462466 |
| hr3144-117 | 117 | 0 | 0.015139467208 | 0.011320126269 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128145259 |
| hr3145-117 | 117 | 0 | 0.015139467208 | 0.013780040115 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000189889506 |
| hr316-117 | 117 | 0 | 0.015139467208 | 0.011786590837 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000138923724 |
| hr3168-117 | 117 | 0 | 0.015139467208 | 0.012413983372 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000154106983 |
| hr3171-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr318-117 | 117 | 0 | 0.015139467208 | 0.012194701213 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000148710738 |
| hr3189-117 | 117 | 0 | 0.015139467208 | 0.013028875827 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000169751605 |
| hr3195-117 | 117 | 0 | 0.015139467208 | 0.013504316132 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000182366554 |
| hr3207-117 | 117 | 0 | 0.015139467208 | 0.012957535080 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000167897715 |
| hr3215-117 | 117 | 0 | 0.015139467208 | 0.014167052697 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000200705382 |
| hr3216-117 | 117 | 0 | 0.015139467208 | 0.015077096115 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000227318827 |
| hr3225-117 | 117 | 0 | 0.015139467208 | 0.014167052697 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000200705382 |
| hr3265-117 | 117 | 0 | 0.015139467208 | 0.013245770830 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000175450445 |
| hr3266-117 | 117 | 0 | 0.015139467208 | 0.013673905423 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000186975690 |
| hr3271-117 | 117 | 0 | 0.015139467208 | 0.014526740096 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000211026178 |
| hr3276-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr329-117 | 117 | 0 | 0.015139467208 | 0.013733223138 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000188601418 |
| hr3299-117 | 117 | 0 | 0.015139467208 | 0.045328094035 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.002054636109 |
| hr3301-117 | 117 | 0 | 0.015139467208 | 0.012640300391 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000159777194 |
| hr3305-117 | 117 | 0 | 0.015139467208 | 0.014969565775 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000224087899 |
| hr3309-117 | 117 | 0 | 0.015139467208 | 0.012791917696 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000163633158 |
| hr3316-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr3335-117 | 117 | 0 | 0.015139467208 | 0.049795433737 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.002479585221 |
| hr3336-117 | 117 | 0 | 0.015139467208 | 0.047081455789 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.002216663479 |
| hr3339-117 | 117 | 0 | 0.015139467208 | 0.018645430581 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000347652082 |
| hr3345-117 | 117 | 0 | 0.015139467208 | 0.012806271724 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000164000595 |
| hr3349-117 | 117 | 0 | 0.015139467208 | 0.009822460138 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000096480723 |
| hr3358-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr3359-117 | 117 | 1 | 0.015139467208 | 0.044142118716 | 0.020294849703 | 0.010486655910 | 0.969950269051 | 0.913664289213 |
| hr3362-117 | 117 | 0 | 0.015139467208 | 0.014207340378 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000201848521 |
| hr3373-117 | 117 | 0 | 0.015139467208 | 0.045459413528 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.002066558278 |
| hr3376-117 | 117 | 0 | 0.015139467208 | 0.009822460138 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000096480723 |
| hr3382-117 | 117 | 0 | 0.015139467208 | 0.047929349299 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.002297222524 |
| hr3388-117 | 117 | 0 | 0.015139467208 | 0.038649153902 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.001493757097 |
| hr34-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr341-117 | 117 | 0 | 0.015139467208 | 0.011437822982 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000130823795 |
| hr3413-117 | 117 | 0 | 0.015139467208 | 0.013813341638 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000190808407 |
| hr3418-117 | 117 | 0 | 0.015139467208 | 0.010156578956 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000103156096 |
| hr3425-117 | 117 | 0 | 0.015139467208 | 0.012575593925 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000158145563 |
| hr343-117 | 117 | 0 | 0.015139467208 | 0.014693601465 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000215901924 |
| hr3437-117 | 117 | 0 | 0.015139467208 | 0.013828825768 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000191236422 |
| hr3446-117 | 117 | 0 | 0.015139467208 | 0.014321210337 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000205097066 |
| hr3448-117 | 117 | 0 | 0.015139467208 | 0.011998623593 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000143966968 |
| hr3453-117 | 117 | 0 | 0.015139467208 | 0.017808525515 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000317143581 |
| hr346-117 | 117 | 0 | 0.015139467208 | 0.012717265088 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000161728831 |
| hr3460-117 | 117 | 0 | 0.015139467208 | 0.017396427127 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000302635677 |
| hr3480-117 | 117 | 0 | 0.015139467208 | 0.015646390491 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000244809535 |
| hr3482-117 | 117 | 0 | 0.015139467208 | 0.014931793638 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000222958461 |
| hr3489-117 | 117 | 0 | 0.015139467208 | 0.013673905423 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000186975690 |
| hr349-117 | 117 | 0 | 0.015139467208 | 0.014811273299 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000219373817 |
| hr3494-117 | 117 | 0 | 0.015139467208 | 0.013789074148 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000190138566 |
| hr3508-117 | 117 | 1 | 0.015139467208 | 0.014082501273 | 0.020294849703 | 0.010486655910 | 0.969950269051 | 0.972033314296 |
| hr351-117 | 117 | 0 | 0.015139467208 | 0.013729866335 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000188509230 |
| hr3510-117 | 117 | 0 | 0.015139467208 | 0.012728775305 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000162021721 |
| hr3523-117 | 117 | 0 | 0.015139467208 | 0.011786590837 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000138923724 |
| hr3539-117 | 117 | 1 | 0.015139467208 | 0.014419401022 | 0.020294849703 | 0.010486655910 | 0.969950269051 | 0.971369117081 |
| hr3547-117 | 117 | 0 | 0.015139467208 | 0.012311091907 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000151562984 |
| hr3575-117 | 117 | 0 | 0.015139467208 | 0.011712276748 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000137177427 |
| hr3577-117 | 117 | 0 | 0.015139467208 | 0.017124700945 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000293255382 |
| hr3578-117 | 117 | 0 | 0.015139467208 | 0.010299614588 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000106082061 |
| hr36-117 | 117 | 0 | 0.015139467208 | 0.011320126269 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128145259 |
| hr3616-117 | 117 | 0 | 0.104531149070 | 0.161853408056 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.026196525699 |
| hr3620-117 | 117 | 0 | 0.015139467208 | 0.011704587199 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000136997361 |
| hr3621-117 | 117 | 0 | 0.015139467208 | 0.014803180042 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000219134139 |
| hr364-117 | 117 | 0 | 0.015139467208 | 0.015431488889 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000238130849 |
| hr3668-117 | 117 | 0 | 0.015139467208 | 0.010156578956 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000103156096 |
| hr374-117 | 117 | 0 | 0.015139467208 | 0.012957535080 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000167897715 |
| hr3755-117 | 117 | 0 | 0.104531149070 | 0.167224540033 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.027964046789 |
| hr3756-117 | 117 | 0 | 0.015139467208 | 0.011794333617 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000139106305 |
| hr380-117 | 117 | 0 | 0.015139467208 | 0.014321210337 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000205097066 |
| hr3849-117 | 117 | 0 | 0.015139467208 | 0.015265043512 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000233021553 |
| hr3858-117 | 117 | 0 | 0.015139467208 | 0.017320919416 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000300014249 |
| hr3891-117 | 117 | 0 | 0.015139467208 | 0.011320126269 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128145259 |
| hr3892-117 | 117 | 0 | 0.015139467208 | 0.012290667808 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000151060515 |
| hr39-117 | 117 | 0 | 0.015139467208 | 0.013259666238 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000175818749 |
| hr3906-117 | 117 | 0 | 0.015139467208 | 0.014379008182 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000206755876 |
| hr3976-117 | 117 | 0 | 0.015139467208 | 0.011320126269 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128145259 |
| hr400-117 | 117 | 0 | 0.015139467208 | 0.014852836338 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000220606747 |
| hr4009-117 | 117 | 0 | 0.015139467208 | 0.022322544151 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000498295977 |
| hr401-117 | 117 | 0 | 0.015139467208 | 0.015277060070 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000233388564 |
| hr4026-117 | 117 | 0 | 0.104531149070 | 0.164749162065 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.027142286401 |
| hr407-117 | 117 | 0 | 0.015139467208 | 0.013240530073 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000175311637 |
| hr4075-117 | 117 | 0 | 0.015139467208 | 0.013641761555 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000186097658 |
| hr4089-117 | 117 | 0 | 0.104531149070 | 0.127073200418 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.016147598264 |
| hr41-117 | 117 | 0 | 0.015139467208 | 0.014419401022 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000207919126 |
| hr4107-117 | 117 | 0 | 0.015139467208 | 0.011704587199 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000136997361 |
| hr4110-117 | 117 | 0 | 0.015139467208 | 0.014790997519 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000218773608 |
| hr4113-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr4124-117 | 117 | 0 | 0.015139467208 | 0.012069109217 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000145663397 |
| hr4134-117 | 117 | 0 | 0.015139467208 | 0.015056254055 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000226690786 |
| hr4197-117 | 117 | 0 | 0.015139467208 | 0.011320126269 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128145259 |
| hr42-117 | 117 | 0 | 0.015139467208 | 0.014419401022 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000207919126 |
| hr4200-117 | 117 | 0 | 0.015139467208 | 0.011998623593 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000143966968 |
| hr4207-117 | 117 | 0 | 0.015139467208 | 0.011712276748 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000137177427 |
| hr427-117 | 117 | 0 | 0.015139467208 | 0.013170771593 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000173469224 |
| hr4270-117 | 117 | 0 | 0.015139467208 | 0.011998623593 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000143966968 |
| hr428-117 | 117 | 0 | 0.015139467208 | 0.013170771593 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000173469224 |
| hr4321-117 | 117 | 0 | 0.015139467208 | 0.012405838909 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000153904839 |
| hr434-117 | 117 | 0 | 0.015139467208 | 0.013497463163 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000182181512 |
| hr4349-117 | 117 | 0 | 0.015139467208 | 0.021864654201 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000478063103 |
| hr4375-117 | 117 | 0 | 0.015139467208 | 0.020658453604 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000426771705 |
| hr4381-117 | 117 | 0 | 0.015139467208 | 0.009960837708 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000099218288 |
| hr4382-117 | 117 | 0 | 0.015139467208 | 0.013991995998 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000195775952 |
| hr440-117 | 117 | 0 | 0.015139467208 | 0.011862182148 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000140711365 |
| hr441-117 | 117 | 1 | 0.015139467208 | 0.012264824329 | 0.020294849703 | 0.010486655910 | 0.969950269051 | 0.975620777257 |
| hr446-117 | 117 | 0 | 0.104531149070 | 0.116140206964 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.013488547674 |
| hr4464-117 | 117 | 0 | 0.015139467208 | 0.011712276748 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000137177427 |
| hr4470-117 | 117 | 0 | 0.015139467208 | 0.012036022863 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000144865846 |
| hr4494-117 | 117 | 0 | 0.015139467208 | 0.023106596586 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000533914806 |
| hr4509-117 | 117 | 0 | 0.015139467208 | 0.013842931080 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000191626741 |
| hr4575-117 | 117 | 0 | 0.015139467208 | 0.024200473284 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000585662907 |
| hr462-117 | 117 | 0 | 0.015139467208 | 0.012225484268 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000149462466 |
| hr4686-117 | 117 | 0 | 0.104531149070 | 0.104497640327 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.010919756834 |
| hr469-117 | 117 | 0 | 0.015139467208 | 0.015085478855 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000227571672 |
| hr4693-117 | 117 | 1 | 0.015139467208 | 0.015416035260 | 0.020294849703 | 0.010486655910 | 0.969950269051 | 0.969405583623 |
| hr4718-117 | 117 | 0 | 0.015139467208 | 0.013354410576 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000178340282 |
| hr4794-117 | 117 | 0 | 0.015139467208 | 0.023362662064 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000545813979 |
| hr4799-117 | 117 | 0 | 0.015139467208 | 0.014131596724 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000199702026 |
| hr4821-117 | 117 | 0 | 0.015139467208 | 0.015339868471 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000235311565 |
| hr4823-117 | 117 | 0 | 0.015139467208 | 0.012843534864 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000164956388 |
| hr4860-117 | 117 | 0 | 0.015139467208 | 0.011320126269 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128145259 |
| hr4892-117 | 117 | 0 | 0.015139467208 | 0.014998310975 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000224949332 |
| hr491-117 | 117 | 0 | 0.015139467208 | 0.013837361946 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000191472586 |
| hr4936-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr4946-117 | 117 | 0 | 0.015139467208 | 0.016857616792 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000284179244 |
| hr498-117 | 117 | 0 | 0.015139467208 | 0.015638001797 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000244547100 |
| hr4996-117 | 117 | 0 | 0.104531149070 | 0.170350478031 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.029019285365 |
| hr5050-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr5139-117 | 117 | 0 | 0.015139467208 | 0.011320126269 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128145259 |
| hr515-117 | 117 | 0 | 0.015139467208 | 0.018121690094 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000328395652 |
| hr5151-117 | 117 | 0 | 0.015139467208 | 0.018818392590 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000354131900 |
| hr5153-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr5173-117 | 117 | 0 | 0.015139467208 | 0.014639746100 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000214322166 |
| hr522-117 | 117 | 0 | 0.015139467208 | 0.015229324553 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000231932326 |
| hr5235-117 | 117 | 0 | 0.015139467208 | 0.013115037468 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000172004208 |
| hr5245-117 | 117 | 0 | 0.015139467208 | 0.012843534864 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000164956388 |
| hr5251-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr5273-117 | 117 | 0 | 0.015139467208 | 0.012252487098 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000150123440 |
| hr5274-117 | 117 | 0 | 0.015139467208 | 0.013240530073 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000175311637 |
| hr5285-117 | 117 | 0 | 0.015139467208 | 0.015120865617 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000228640577 |
| hr529-117 | 117 | 0 | 0.015139467208 | 0.017564239983 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000308502526 |
| hr5292-117 | 117 | 0 | 0.015139467208 | 0.010299614588 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000106082061 |
| hr5309-117 | 117 | 0 | 0.015139467208 | 0.013782596312 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000189959961 |
| hr532-117 | 117 | 0 | 0.015139467208 | 0.018838823336 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000354901265 |
| hr5321-117 | 117 | 0 | 0.015139467208 | 0.012054298498 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000145306112 |
| hr5330-117 | 117 | 0 | 0.015139467208 | 0.012413983372 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000154106983 |
| hr5370-117 | 117 | 0 | 0.015139467208 | 0.015137743862 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000229151289 |
| hr5455-117 | 117 | 0 | 0.015139467208 | 0.012413983372 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000154106983 |
| hr5462-117 | 117 | 0 | 0.015139467208 | 0.011320126269 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128145259 |
| hr5479-117 | 117 | 0 | 0.015139467208 | 0.011794333617 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000139106305 |
| hr5486-117 | 117 | 0 | 0.015139467208 | 0.010754482320 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000115658890 |
| hr5490-117 | 117 | 0 | 0.015139467208 | 0.013780040115 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000189889506 |
| hr552-117 | 117 | 0 | 0.015139467208 | 0.015673535255 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000245659707 |
| hr5585-117 | 117 | 0 | 0.015139467208 | 0.015416035260 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000237654143 |
| hr5597-117 | 117 | 0 | 0.015139467208 | 0.012843534864 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000164956388 |
| hr5653-117 | 117 | 0 | 0.015139467208 | 0.013707266403 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000187889152 |
| hr5671-117 | 117 | 0 | 0.104531149070 | 0.060962827349 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.003716466318 |
| hr5685-117 | 117 | 0 | 0.015139467208 | 0.013061520738 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000170603324 |
| hr5687-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr5715-117 | 117 | 0 | 0.015139467208 | 0.029963955512 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000897838630 |
| hr5716-117 | 117 | 0 | 0.015139467208 | 0.012571482408 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000158042170 |
| hr5738-117 | 117 | 0 | 0.015139467208 | 0.035886035359 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.001287807534 |
| hr5774-117 | 117 | 0 | 0.015139467208 | 0.012082662097 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000145990723 |
| hr5791-117 | 117 | 0 | 0.015139467208 | 0.012413983372 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000154106983 |
| hr5798-117 | 117 | 0 | 0.015139467208 | 0.012109892996 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000146649508 |
| hr5802-117 | 117 | 0 | 0.015139467208 | 0.014756341157 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000217749604 |
| hr5809-117 | 117 | 1 | 0.015139467208 | 0.043259747636 | 0.020294849703 | 0.010486655910 | 0.969950269051 | 0.915351910493 |
| hr582-117 | 117 | 0 | 0.015139467208 | 0.014803180042 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000219134139 |
| hr5828-117 | 117 | 0 | 0.015139467208 | 0.014698022481 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000216031865 |
| hr5870-117 | 117 | 0 | 0.015139467208 | 0.024300073702 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000590493582 |
| hr5880-117 | 117 | 0 | 0.015139467208 | 0.010172030204 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000103470198 |
| hr59-117 | 117 | 0 | 0.015139467208 | 0.013355683504 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000178374282 |
| hr5914-117 | 117 | 0 | 0.015139467208 | 0.012599239709 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000158740841 |
| hr5918-117 | 117 | 0 | 0.015139467208 | 0.011217668973 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000125836097 |
| hr5943-117 | 117 | 1 | 0.015139467208 | 0.014456504829 | 0.020294849703 | 0.010486655910 | 0.969950269051 | 0.971295980874 |
| hr5950-117 | 117 | 0 | 0.015139467208 | 0.013276943213 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000176277221 |
| hr5953-117 | 117 | 0 | 0.015139467208 | 0.011320126269 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128145259 |
| hr5954-117 | 117 | 0 | 0.015139467208 | 0.013061520738 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000170603324 |
| hr596-117 | 117 | 0 | 0.015139467208 | 0.016605569693 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000275744945 |
| hr597-117 | 117 | 0 | 0.015139467208 | 0.021927164821 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000480800557 |
| hr598-117 | 117 | 0 | 0.015139467208 | 0.014701016073 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000216119874 |
| hr5992-117 | 117 | 0 | 0.015139467208 | 0.013961772167 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000194931082 |
| hr6015-117 | 117 | 0 | 0.104531149070 | 0.247193653621 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.061104702391 |
| hr6028-117 | 117 | 0 | 0.015139467208 | 0.017779852934 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000316123170 |
| hr6056-117 | 117 | 0 | 0.015139467208 | 0.015851398224 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000251266826 |
| hr606-117 | 117 | 0 | 0.015139467208 | 0.015195933018 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000230916380 |
| hr607-117 | 117 | 0 | 0.015139467208 | 0.012957535080 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000167897715 |
| hr6084-117 | 117 | 0 | 0.015139467208 | 0.009822460138 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000096480723 |
| hr6147-117 | 117 | 0 | 0.015139467208 | 0.014859845092 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000220814996 |
| hr6152-117 | 117 | 0 | 0.015139467208 | 0.014655458767 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000214782472 |
| hr6182-117 | 117 | 0 | 0.015139467208 | 0.011320126269 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128145259 |
| hr62-117 | 117 | 0 | 0.015139467208 | 0.012350703999 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000152539889 |
| hr620-117 | 117 | 0 | 0.015139467208 | 0.015353193592 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000235720553 |
| hr6201-117 | 117 | 0 | 0.104531149070 | 0.178206864296 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.031757686482 |
| hr6215-117 | 117 | 0 | 0.015139467208 | 0.013499397979 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000182233746 |
| hr622-117 | 117 | 0 | 0.015139467208 | 0.015077096115 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000227318827 |
| hr6258-117 | 117 | 0 | 0.015139467208 | 0.012761910653 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000162866364 |
| hr626-117 | 117 | 0 | 0.015139467208 | 0.020149498197 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000406002278 |
| hr6271-117 | 117 | 0 | 0.015139467208 | 0.010400438007 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000108169111 |
| hr6291-117 | 117 | 0 | 0.015139467208 | 0.015710295285 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000246813378 |
| hr6338-117 | 117 | 0 | 0.015139467208 | 0.015179286894 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000230410751 |
| hr6343-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr6369-117 | 117 | 0 | 0.015139467208 | 0.022789799821 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000519374976 |
| hr6400-117 | 117 | 0 | 0.015139467208 | 0.013234371311 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000175148584 |
| hr642-117 | 117 | 0 | 0.015139467208 | 0.014198462155 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000201596328 |
| hr6427-117 | 117 | 1 | 0.015139467208 | 0.015784510929 | 0.020294849703 | 0.010486655910 | 0.969950269051 | 0.968680128927 |
| hr643-117 | 117 | 0 | 0.015139467208 | 0.019134855660 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000366142701 |
| hr6451-117 | 117 | 0 | 0.015139467208 | 0.010757119609 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000115715622 |
| hr6467-117 | 117 | 0 | 0.015139467208 | 0.012841506141 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000164904280 |
| hr6472-117 | 117 | 0 | 0.015139467208 | 0.011998623593 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000143966968 |
| hr6475-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr6483-117 | 117 | 0 | 0.015139467208 | 0.009822460138 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000096480723 |
| hr6513-117 | 117 | 0 | 0.015139467208 | 0.009960837708 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000099218288 |
| hr6519-117 | 117 | 0 | 0.015139467208 | 0.013231415261 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000175070350 |
| hr6520-117 | 117 | 0 | 0.015139467208 | 0.012986133558 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000168639665 |
| hr6541-117 | 117 | 0 | 0.015139467208 | 0.012492693490 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000156067391 |
| hr6556-117 | 117 | 0 | 0.015139467208 | 0.011985163834 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000143644152 |
| hr6562-117 | 117 | 0 | 0.015139467208 | 0.010156578956 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000103156096 |
| hr6563-117 | 117 | 0 | 0.015139467208 | 0.014311832729 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000204828556 |
| hr6572-117 | 117 | 0 | 0.015139467208 | 0.012311091907 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000151562984 |
| hr6587-117 | 117 | 0 | 0.015139467208 | 0.009822460138 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000096480723 |
| hr6628-117 | 117 | 0 | 0.015139467208 | 0.014198036259 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000201584234 |
| hr6635-117 | 117 | 0 | 0.015139467208 | 0.013337569137 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000177890750 |
| hr6645-117 | 117 | 0 | 0.015139467208 | 0.012125107169 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000147018224 |
| hr6656-117 | 117 | 0 | 0.015139467208 | 0.012225484268 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000149462466 |
| hr667-117 | 117 | 0 | 0.015139467208 | 0.015155325931 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000229683904 |
| hr6680-117 | 117 | 0 | 0.015139467208 | 0.011320126269 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128145259 |
| hr6682-117 | 117 | 0 | 0.015139467208 | 0.012640300391 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000159777194 |
| hr6695-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr671-117 | 117 | 0 | 0.015139467208 | 0.014659199730 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000214892137 |
| hr6766-117 | 117 | 0 | 0.015139467208 | 0.014125469728 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000199528895 |
| hr6801-117 | 117 | 0 | 0.015139467208 | 0.012931370936 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000167220354 |
| hr6826-117 | 117 | 0 | 0.040639412606 | 0.050396023120 | 0.020294849703 | 0.058283987399 | 0.001651561857 | 0.002539759146 |
| hr6834-117 | 117 | 0 | 0.015139467208 | 0.009960837708 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000099218288 |
| hr693-117 | 117 | 0 | 0.015139467208 | 0.016638657893 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000276844936 |
| hr695-117 | 117 | 0 | 0.015139467208 | 0.017105139771 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000292585807 |
| hr6950-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr6975-117 | 117 | 0 | 0.015139467208 | 0.012413983372 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000154106983 |
| hr7020-117 | 117 | 0 | 0.015139467208 | 0.012225484268 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000149462466 |
| hr7050-117 | 117 | 0 | 0.015139467208 | 0.013245770830 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000175450445 |
| hr7082-117 | 117 | 0 | 0.015139467208 | 0.013061520738 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000170603324 |
| hr7095-117 | 117 | 0 | 0.015139467208 | 0.013157170994 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000173111149 |
| hr7110-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr7118-117 | 117 | 0 | 0.015139467208 | 0.012413983372 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000154106983 |
| hr7128-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr7132-117 | 117 | 1 | 0.104531149070 | 0.150054926480 | 0.020294849703 | 0.202248763446 | 0.801864462985 | 0.722406628002 |
| hr7136-117 | 117 | 0 | 0.015139467208 | 0.010085800166 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000101723365 |
| hr7150-117 | 117 | 0 | 0.015139467208 | 0.014985947536 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000224578624 |
| hr7154-117 | 117 | 0 | 0.015139467208 | 0.009960837708 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000099218288 |
| hr717-117 | 117 | 0 | 0.015139467208 | 0.016761148709 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000280936106 |
| hr7180-117 | 117 | 0 | 0.104531149070 | 0.151003291407 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.022801994016 |
| hr7194-117 | 117 | 0 | 0.015139467208 | 0.015882647132 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000252258480 |
| hr7196-117 | 117 | 0 | 0.040639412606 | 0.057213524531 | 0.020294849703 | 0.058283987399 | 0.001651561857 | 0.003273387389 |
| hr724-117 | 117 | 0 | 0.015139467208 | 0.011399467400 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000129947857 |
| hr7262-117 | 117 | 0 | 0.015139467208 | 0.011985163834 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000143644152 |
| hr727-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr7293-117 | 117 | 0 | 0.015139467208 | 0.013991995998 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000195775952 |
| hr730-117 | 117 | 0 | 0.015139467208 | 0.044068682693 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.001942048794 |
| hr7312-117 | 117 | 0 | 0.015139467208 | 0.013715485032 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000188114530 |
| hr7326-117 | 117 | 0 | 0.015139467208 | 0.012225484268 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000149462466 |
| hr735-117 | 117 | 1 | 0.015139467208 | 0.040980045325 | 0.020294849703 | 0.010486655910 | 0.969950269051 | 0.919719273464 |
| hr736-117 | 117 | 0 | 0.015139467208 | 0.012167281959 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000148042750 |
| hr7369-117 | 117 | 0 | 0.015139467208 | 0.010101144837 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000102033127 |
| hr7385-117 | 117 | 0 | 0.015139467208 | 0.012957535080 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000167897715 |
| hr7424-117 | 117 | 0 | 0.015139467208 | 0.010085800166 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000101723365 |
| hr7466-117 | 117 | 0 | 0.015139467208 | 0.014425950534 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000208108049 |
| hr7467-117 | 117 | 0 | 0.015139467208 | 0.012575593925 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000158145563 |
| hr7481-117 | 117 | 0 | 0.015139467208 | 0.012069109217 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000145663397 |
| hr7509-117 | 117 | 0 | 0.015139467208 | 0.018428397865 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000339605848 |
| hr7529-117 | 117 | 0 | 0.015139467208 | 0.012492693490 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000156067391 |
| hr7561-117 | 117 | 0 | 0.015139467208 | 0.013157170994 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000173111149 |
| hr7592-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr7621-117 | 117 | 0 | 0.015139467208 | 0.011998623593 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000143966968 |
| hr765-117 | 117 | 0 | 0.015139467208 | 0.015965338937 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000254892047 |
| hr7667-117 | 117 | 0 | 0.104531149070 | 0.075684794019 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.005728188046 |
| hr7685-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr7689-117 | 117 | 0 | 0.015139467208 | 0.040255263665 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.001620486253 |
| hr7692-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr7701-117 | 117 | 0 | 0.040639412606 | 0.090334320366 | 0.020294849703 | 0.058283987399 | 0.001651561857 | 0.008160289436 |
| hr7714-117 | 117 | 0 | 0.015139467208 | 0.011869162101 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000140877009 |
| hr7717-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr7720-117 | 117 | 0 | 0.015139467208 | 0.010156578956 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000103156096 |
| hr7722-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr7732-117 | 117 | 0 | 0.015139467208 | 0.010101144837 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000102033127 |
| hr7735-117 | 117 | 1 | 0.104531149070 | 0.132737150243 | 0.020294849703 | 0.202248763446 | 0.801864462985 | 0.752144850569 |
| hr7740-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr7795-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr7818-117 | 117 | 0 | 0.015139467208 | 0.035916190373 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.001289972731 |
| hr7894-117 | 117 | 0 | 0.015139467208 | 0.016646299632 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000277099291 |
| hr790-117 | 117 | 0 | 0.015139467208 | 0.014082501273 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000198316842 |
| hr7903-117 | 117 | 1 | 0.104531149070 | 0.199836139029 | 0.020294849703 | 0.202248763446 | 0.801864462985 | 0.640262204405 |
| hr7914-117 | 117 | 0 | 0.015139467208 | 0.039689056348 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.001575221194 |
| hr7918-117 | 117 | 0 | 0.015139467208 | 0.017435902941 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000304010711 |
| hr7938-117 | 117 | 0 | 0.015139467208 | 0.012225484268 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000149462466 |
| hr7945-117 | 117 | 0 | 0.015139467208 | 0.015673678644 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000245664202 |
| hr7947-117 | 117 | 0 | 0.015139467208 | 0.011960155147 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000143045311 |
| hr7988-117 | 117 | 0 | 0.015139467208 | 0.045139490064 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.002037573563 |
| hr8023-117 | 117 | 0 | 0.015139467208 | 0.011320126269 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128145259 |
| hr8026-117 | 117 | 1 | 0.015139467208 | 0.037176606781 | 0.020294849703 | 0.010486655910 | 0.969950269051 | 0.927028886529 |
| hr8040-117 | 117 | 0 | 0.015139467208 | 0.013894587315 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000193059557 |
| hr8048-117 | 117 | 0 | 0.015139467208 | 0.032916113517 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.001083470529 |
| hr8065-117 | 117 | 0 | 0.015139467208 | 0.012413983372 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000154106983 |
| hr8092-117 | 117 | 0 | 0.015139467208 | 0.034597794737 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.001197007401 |
| hr81-117 | 117 | 0 | 0.015139467208 | 0.014419401022 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000207919126 |
| hr8108-117 | 117 | 0 | 0.015139467208 | 0.018878542328 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000356399360 |
| hr8112-117 | 117 | 0 | 0.015139467208 | 0.011320126269 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128145259 |
| hr8133-117 | 117 | 0 | 0.015139467208 | 0.010085800166 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000101723365 |
| hr8136-117 | 117 | 0 | 0.015139467208 | 0.012413983372 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000154106983 |
| hr8138-117 | 117 | 0 | 0.015139467208 | 0.009822460138 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000096480723 |
| hr8185-117 | 117 | 0 | 0.015139467208 | 0.013157170994 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000173111149 |
| hr8187-117 | 117 | 0 | 0.015139467208 | 0.013157170994 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000173111149 |
| hr8211-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr8226-117 | 117 | 1 | 0.104531149070 | 0.194786420703 | 0.020294849703 | 0.202248763446 | 0.801864462985 | 0.648368908284 |
| hr8245-117 | 117 | 0 | 0.015139467208 | 0.010085800166 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000101723365 |
| hr8250-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr8264-117 | 117 | 0 | 0.015139467208 | 0.035572480869 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.001265401395 |
| hr8282-117 | 117 | 0 | 0.040639412606 | 0.020960575631 | 0.020294849703 | 0.058283987399 | 0.001651561857 | 0.000439345731 |
| hr834-117 | 117 | 0 | 0.015139467208 | 0.012791917696 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000163633158 |
| hr844-117 | 117 | 0 | 0.015139467208 | 0.013093107009 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000171429451 |
| hr849-117 | 117 | 0 | 0.015139467208 | 0.016426451492 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000269828309 |
| hr85-117 | 117 | 0 | 0.015139467208 | 0.014553789317 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000211812783 |
| hr86-117 | 117 | 0 | 0.015139467208 | 0.012575593925 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000158145563 |
| hr870-117 | 117 | 0 | 0.015139467208 | 0.013115037468 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000172004208 |
| hr878-117 | 117 | 0 | 0.015139467208 | 0.013137609186 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000172596775 |
| hr887-117 | 117 | 0 | 0.015139467208 | 0.011960155147 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000143045311 |
| hr895-117 | 117 | 0 | 0.015139467208 | 0.014654417100 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000214751941 |
| hr901-117 | 117 | 0 | 0.015139467208 | 0.011320126269 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128145259 |
| hr902-117 | 117 | 0 | 0.015139467208 | 0.011320126269 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128145259 |
| hr91-117 | 117 | 1 | 0.015139467208 | 0.024844173705 | 0.020294849703 | 0.010486655910 | 0.969950269051 | 0.950928885557 |
| hr910-117 | 117 | 0 | 0.015139467208 | 0.016379395944 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000268284611 |
| hr914-117 | 117 | 0 | 0.015139467208 | 0.019638509366 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000385671050 |
| hr930-117 | 117 | 0 | 0.015139467208 | 0.012456054509 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000155153294 |
| hr949-117 | 117 | 0 | 0.015139467208 | 0.009822460138 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000096480723 |
| hr952-117 | 117 | 0 | 0.015139467208 | 0.011320126269 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128145259 |
| hr96-117 | 117 | 0 | 0.015139467208 | 0.015491079150 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000239973533 |
| hr967-117 | 117 | 0 | 0.015139467208 | 0.009753986798 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000095140258 |
| hr985-117 | 117 | 0 | 0.015139467208 | 0.012413983372 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000154106983 |
| hr99-117 | 117 | 0 | 0.015139467208 | 0.016721988434 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000279624897 |
| hr992-117 | 117 | 0 | 0.015139467208 | 0.013694725768 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000187545514 |
| s1001-117 | 117 | 0 | 0.016448914161 | 0.013574070368 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000184255386 |
| s1008-117 | 117 | 0 | 0.016448914161 | 0.023135843594 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000535267259 |
| s1010-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s1048-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s1055-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s1056-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s1067-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s1068-117 | 117 | 0 | 0.016448914161 | 0.014882446286 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000221487207 |
| s1084-117 | 117 | 0 | 0.016448914161 | 0.015680315072 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000245872281 |
| s1085-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s1093-117 | 117 | 0 | 0.016448914161 | 0.013955696475 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000194761464 |
| s1096-117 | 117 | 0 | 0.016448914161 | 0.013955696475 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000194761464 |
| s1107-117 | 117 | 0 | 0.016448914161 | 0.013783072558 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000189973089 |
| s1117-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s1120-117 | 117 | 0 | 0.016448914161 | 0.013574070368 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000184255386 |
| s1137-117 | 117 | 0 | 0.016448914161 | 0.014796743692 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000218943624 |
| s1158-117 | 117 | 0 | 0.016448914161 | 0.013574070368 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000184255386 |
| s1172-117 | 117 | 0 | 0.016448914161 | 0.011859687770 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140652194 |
| s1173-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s1183-117 | 117 | 0 | 0.016448914161 | 0.014119323821 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000199355305 |
| s1194-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s1195-117 | 117 | 0 | 0.016448914161 | 0.016085882982 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000258755631 |
| s1196-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s12-117 | 117 | 0 | 0.044055747086 | 0.027841272055 | 0.020294849703 | 0.058283987399 | 0.001940908851 | 0.000775136430 |
| s1203-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s1214-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s122-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s1221-117 | 117 | 0 | 0.016448914161 | 0.013322522345 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000177489602 |
| s1239-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s1244-117 | 117 | 0 | 0.016448914161 | 0.013962254517 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000194944551 |
| s1247-117 | 117 | 0 | 0.016448914161 | 0.013962254517 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000194944551 |
| s1250-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s1254-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s1309-117 | 117 | 0 | 0.016448914161 | 0.013322522345 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000177489602 |
| s1310-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s1312-117 | 117 | 0 | 0.016448914161 | 0.015479430837 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000239612779 |
| s1315-117 | 117 | 0 | 0.016448914161 | 0.016887479261 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000285186956 |
| s1339-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s1341-117 | 117 | 0 | 0.016448914161 | 0.013322522345 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000177489602 |
| s1361-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s1368-117 | 117 | 0 | 0.016448914161 | 0.020222197822 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000408937285 |
| s137-117 | 117 | 0 | 0.016448914161 | 0.015583421730 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000242843033 |
| s1381-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s14-117 | 117 | 0 | 0.044055747086 | 0.089400160079 | 0.020294849703 | 0.058283987399 | 0.001940908851 | 0.007992388622 |
| s1411-117 | 117 | 0 | 0.016448914161 | 0.041705086158 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.001739314211 |
| s1421-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s1462-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s1474-117 | 117 | 0 | 0.016448914161 | 0.013574070368 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000184255386 |
| s1487-117 | 117 | 0 | 0.016448914161 | 0.013322522345 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000177489602 |
| s1509-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s1510-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s1515-117 | 117 | 0 | 0.016448914161 | 0.013004996570 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169129936 |
| s1526-117 | 117 | 0 | 0.016448914161 | 0.015895187296 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000252656979 |
| s1527-117 | 117 | 0 | 0.016448914161 | 0.015895187296 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000252656979 |
| s1544-117 | 117 | 0 | 0.016448914161 | 0.014796743692 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000218943624 |
| s1547-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s1552-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s1560-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s1567-117 | 117 | 0 | 0.016448914161 | 0.013783072558 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000189973089 |
| s1570-117 | 117 | 0 | 0.016448914161 | 0.014705228634 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000216243749 |
| s1586-117 | 117 | 0 | 0.016448914161 | 0.013004996570 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169129936 |
| s1604-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s1606-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s1613-117 | 117 | 0 | 0.016448914161 | 0.015632691909 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000244381056 |
| s1619-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s1625-117 | 117 | 0 | 0.016448914161 | 0.013574070368 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000184255386 |
| s1642-117 | 117 | 0 | 0.016448914161 | 0.014607011119 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000213364774 |
| s1652-117 | 117 | 0 | 0.016448914161 | 0.015111285145 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000228350939 |
| s1653-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s1656-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s1660-117 | 117 | 0 | 0.016448914161 | 0.014500975667 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000210278295 |
| s1669-117 | 117 | 0 | 0.016448914161 | 0.013962254517 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000194944551 |
| s1677-117 | 117 | 0 | 0.016448914161 | 0.013962254517 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000194944551 |
| s1686-117 | 117 | 0 | 0.016448914161 | 0.013263368158 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000175916935 |
| s1696-117 | 117 | 0 | 0.016448914161 | 0.013574070368 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000184255386 |
| s1713-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s172-117 | 117 | 0 | 0.016448914161 | 0.036462819253 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.001329537188 |
| s1732-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s1738-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s174-117 | 117 | 0 | 0.016448914161 | 0.013004996570 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169129936 |
| s1740-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s1761-117 | 117 | 0 | 0.016448914161 | 0.013962254517 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000194944551 |
| s1762-117 | 117 | 0 | 0.016448914161 | 0.013574070368 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000184255386 |
| s1769-117 | 117 | 0 | 0.016448914161 | 0.015928557031 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000253718929 |
| s1773-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s1789-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s1803-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s182-117 | 117 | 0 | 0.016448914161 | 0.031764719104 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.001008997380 |
| s1820-117 | 117 | 0 | 0.016448914161 | 0.016981635476 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000288375943 |
| s1833-117 | 117 | 0 | 0.016448914161 | 0.014385697229 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000206948285 |
| s1835-117 | 117 | 0 | 0.016448914161 | 0.013004996570 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169129936 |
| s1841-117 | 117 | 0 | 0.016448914161 | 0.014500975667 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000210278295 |
| s1850-117 | 117 | 0 | 0.016448914161 | 0.044422422198 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.001973351594 |
| s1852-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s1854-117 | 117 | 0 | 0.016448914161 | 0.013783072558 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000189973089 |
| s1874-117 | 117 | 0 | 0.016448914161 | 0.011859687770 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140652194 |
| s1879-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s1880-117 | 117 | 0 | 0.016448914161 | 0.021511410202 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000462740769 |
| s1883-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s1884-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s1887-117 | 117 | 0 | 0.016448914161 | 0.013574070368 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000184255386 |
| s1926-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s1933-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s1936-117 | 117 | 0 | 0.016448914161 | 0.041705086158 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.001739314211 |
| s1955-117 | 117 | 0 | 0.016448914161 | 0.013574070368 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000184255386 |
| s1956-117 | 117 | 0 | 0.016448914161 | 0.013004996570 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169129936 |
| s1965-117 | 117 | 0 | 0.016448914161 | 0.017800806066 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000316868697 |
| s1998-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s2003-117 | 117 | 0 | 0.016448914161 | 0.014259313582 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000203328024 |
| s202-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s2041-117 | 117 | 0 | 0.016448914161 | 0.018431660175 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000339726097 |
| s2076-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s2095-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s2139-117 | 117 | 0 | 0.016448914161 | 0.013322522345 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000177489602 |
| s2172-117 | 117 | 0 | 0.016448914161 | 0.017114620321 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000292910229 |
| s2178-117 | 117 | 0 | 0.016448914161 | 0.013322522345 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000177489602 |
| s2205-117 | 117 | 0 | 0.112687626852 | 0.109369212784 | 0.020294849703 | 0.202248763446 | 0.012698501245 | 0.011961624705 |
| s2209-117 | 117 | 0 | 0.016448914161 | 0.013004996570 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169129936 |
| s2212-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s224-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s2249-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s2279-117 | 117 | 0 | 0.016448914161 | 0.013574070368 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000184255386 |
| s2300-117 | 117 | 0 | 0.016448914161 | 0.013322522345 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000177489602 |
| s2323-117 | 117 | 0 | 0.016448914161 | 0.013187612175 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000173913115 |
| s2332-117 | 117 | 0 | 0.016448914161 | 0.013574070368 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000184255386 |
| s242-117 | 117 | 0 | 0.016448914161 | 0.013004996570 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169129936 |
| s2429-117 | 117 | 0 | 0.044055747086 | 0.064087133464 | 0.020294849703 | 0.058283987399 | 0.001940908851 | 0.004107160676 |
| s244-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s2448-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s2472-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s2482-117 | 117 | 0 | 0.016448914161 | 0.021810832943 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000475712434 |
| s2490-117 | 117 | 1 | 0.016448914161 | 0.027695149012 | 0.020294849703 | 0.010486655910 | 0.967372738455 | 0.945376723254 |
| s2508-117 | 117 | 0 | 0.016448914161 | 0.044187130999 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.001952502546 |
| s2511-117 | 117 | 0 | 0.016448914161 | 0.013322522345 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000177489602 |
| s2513-117 | 117 | 0 | 0.016448914161 | 0.034214941666 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.001170662233 |
| s2527-117 | 117 | 0 | 0.016448914161 | 0.013574070368 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000184255386 |
| s2545-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s255-117 | 117 | 0 | 0.016448914161 | 0.015856401008 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000251425453 |
| s2559-117 | 117 | 0 | 0.016448914161 | 0.014153497581 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000200321494 |
| s259-117 | 117 | 0 | 0.016448914161 | 0.014705228634 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000216243749 |
| s2597-117 | 117 | 0 | 0.016448914161 | 0.013783072558 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000189973089 |
| s262-117 | 117 | 0 | 0.016448914161 | 0.013322522345 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000177489602 |
| s2646-117 | 117 | 0 | 0.016448914161 | 0.013783072558 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000189973089 |
| s2651-117 | 117 | 0 | 0.016448914161 | 0.013004996570 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169129936 |
| s2659-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s2660-117 | 117 | 0 | 0.016448914161 | 0.014500975667 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000210278295 |
| s2666-117 | 117 | 0 | 0.016448914161 | 0.013004996570 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169129936 |
| s2673-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s268-117 | 117 | 0 | 0.016448914161 | 0.014882446286 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000221487207 |
| s2687-117 | 117 | 1 | 0.016448914161 | 0.031306592868 | 0.020294849703 | 0.010486655910 | 0.967372738455 | 0.938366917020 |
| s2716-117 | 117 | 0 | 0.016448914161 | 0.014385697229 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000206948285 |
| s2746-117 | 117 | 0 | 0.016448914161 | 0.013004996570 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169129936 |
| s2748-117 | 117 | 0 | 0.016448914161 | 0.013004996570 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169129936 |
| s2749-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s2750-117 | 117 | 0 | 0.016448914161 | 0.013574070368 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000184255386 |
| s2768-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s2771-117 | 117 | 1 | 0.112687626852 | 0.180085652740 | 0.020294849703 | 0.202248763446 | 0.787323247542 | 0.672259536842 |
| s2782-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s2806-117 | 117 | 0 | 0.016448914161 | 0.016302306179 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000265765187 |
| s2816-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s2828-117 | 117 | 0 | 0.016448914161 | 0.013574070368 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000184255386 |
| s2836-117 | 117 | 0 | 0.016448914161 | 0.016189399749 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000262096664 |
| s285-117 | 117 | 0 | 0.016448914161 | 0.013574070368 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000184255386 |
| s2859-117 | 117 | 0 | 0.016448914161 | 0.013004996570 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169129936 |
| s286-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s288-117 | 117 | 0 | 0.016448914161 | 0.013574070368 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000184255386 |
| s2923-117 | 117 | 0 | 0.112687626852 | 0.091324770779 | 0.020294849703 | 0.202248763446 | 0.012698501245 | 0.008340213758 |
| s294-117 | 117 | 0 | 0.016448914161 | 0.014796743692 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000218943624 |
| s2955-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s2964-117 | 117 | 0 | 0.016448914161 | 0.014385697229 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000206948285 |
| s303-117 | 117 | 0 | 0.016448914161 | 0.013004996570 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169129936 |
| s3043-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s3061-117 | 117 | 0 | 0.016448914161 | 0.013004996570 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169129936 |
| s307-117 | 117 | 0 | 0.016448914161 | 0.014385697229 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000206948285 |
| s3083-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s3106-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s3123-117 | 117 | 0 | 0.016448914161 | 0.036908861637 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.001362264067 |
| s3141-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s3150-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s3156-117 | 117 | 0 | 0.016448914161 | 0.013962254517 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000194944551 |
| s3167-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s3175-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s3180-117 | 117 | 0 | 0.016448914161 | 0.013322522345 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000177489602 |
| s319-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s3191-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s3192-117 | 117 | 0 | 0.016448914161 | 0.013962254517 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000194944551 |
| s3210-117 | 117 | 0 | 0.016448914161 | 0.013322522345 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000177489602 |
| s3214-117 | 117 | 0 | 0.016448914161 | 0.013574070368 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000184255386 |
| s3264-117 | 117 | 0 | 0.016448914161 | 0.014964136549 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000223925383 |
| s3275-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s330-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s3316-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s333-117 | 117 | 0 | 0.016448914161 | 0.015111285145 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000228350939 |
| s3338-117 | 117 | 0 | 0.016448914161 | 0.036409885528 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.001325679764 |
| s338-117 | 117 | 0 | 0.016448914161 | 0.013004996570 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169129936 |
| s3388-117 | 117 | 0 | 0.016448914161 | 0.012658103707 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000160227589 |
| s3389-117 | 117 | 0 | 0.016448914161 | 0.013322522345 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000177489602 |
| s3412-117 | 117 | 0 | 0.016448914161 | 0.015479430837 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000239612779 |
| s3431-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s3434-117 | 117 | 0 | 0.016448914161 | 0.024300904416 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000590533955 |
| s344-117 | 117 | 0 | 0.016448914161 | 0.020022547202 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000400902396 |
| s3445-117 | 117 | 0 | 0.016448914161 | 0.013004996570 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169129936 |
| s3462-117 | 117 | 0 | 0.016448914161 | 0.016610619525 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000275912681 |
| s3464-117 | 117 | 0 | 0.016448914161 | 0.016610619525 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000275912681 |
| s3466-117 | 117 | 0 | 0.016448914161 | 0.016610619525 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000275912681 |
| s3469-117 | 117 | 0 | 0.016448914161 | 0.016610619525 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000275912681 |
| s3470-117 | 117 | 1 | 0.044055747086 | 0.069779936538 | 0.020294849703 | 0.058283987399 | 0.913829414680 | 0.865309366467 |
| s3474-117 | 117 | 0 | 0.016448914161 | 0.013322522345 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000177489602 |
| s35-117 | 117 | 0 | 0.112687626852 | 0.099826060015 | 0.020294849703 | 0.202248763446 | 0.012698501245 | 0.009965242258 |
| s350-117 | 117 | 0 | 0.016448914161 | 0.013574070368 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000184255386 |
| s3509-117 | 117 | 0 | 0.016448914161 | 0.013004996570 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169129936 |
| s3510-117 | 117 | 1 | 0.112687626852 | 0.173911514964 | 0.020294849703 | 0.202248763446 | 0.787323247542 | 0.682422185110 |
| s3516-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s3518-117 | 117 | 0 | 0.016448914161 | 0.014963058180 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000223893110 |
| s3530-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s3540-117 | 117 | 0 | 0.016448914161 | 0.014607011119 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000213364774 |
| s3556-117 | 117 | 0 | 0.016448914161 | 0.013004996570 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169129936 |
| s3558-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s3565-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s3578-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s358-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s361-117 | 117 | 0 | 0.016448914161 | 0.013004996570 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169129936 |
| s3621-117 | 117 | 0 | 0.016448914161 | 0.014259313582 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000203328024 |
| s3639-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s3647-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s3655-117 | 117 | 1 | 0.044055747086 | 0.086527138461 | 0.020294849703 | 0.058283987399 | 0.913829414680 | 0.834432668768 |
| s3677-117 | 117 | 0 | 0.016448914161 | 0.017298591124 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000299241255 |
| s3703-117 | 117 | 0 | 0.016448914161 | 0.013322522345 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000177489602 |
| s3708-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s3712-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s3727-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s3729-117 | 117 | 0 | 0.016448914161 | 0.013004996570 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169129936 |
| s3730-117 | 117 | 0 | 0.016448914161 | 0.016477691529 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000271514318 |
| s376-117 | 117 | 0 | 0.016448914161 | 0.013004996570 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169129936 |
| s3798-117 | 117 | 0 | 0.016448914161 | 0.014500975667 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000210278295 |
| s3826-117 | 117 | 1 | 0.112687626852 | 0.102221557343 | 0.020294849703 | 0.202248763446 | 0.787323247542 | 0.806006132099 |
| s384-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s3880-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s3888-117 | 117 | 0 | 0.016448914161 | 0.013322522345 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000177489602 |
| s3906-117 | 117 | 0 | 0.044055747086 | 0.047822619467 | 0.020294849703 | 0.058283987399 | 0.001940908851 | 0.002287002933 |
| s3923-117 | 117 | 0 | 0.016448914161 | 0.013667031872 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000186787760 |
| s3932-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s3948-117 | 117 | 0 | 0.016448914161 | 0.011375870289 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000129410425 |
| s395-117 | 117 | 0 | 0.016448914161 | 0.014385697229 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000206948285 |
| s3960-117 | 117 | 0 | 0.016448914161 | 0.013962254517 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000194944551 |
| s3975-117 | 117 | 0 | 0.016448914161 | 0.015039173024 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000226176725 |
| s399-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s4025-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s4030-117 | 117 | 0 | 0.044055747086 | 0.065452540888 | 0.020294849703 | 0.058283987399 | 0.001940908851 | 0.004284035109 |
| s4033-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s4034-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s4058-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s4062-117 | 117 | 0 | 0.016448914161 | 0.020734931665 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000429937391 |
| s4063-117 | 117 | 0 | 0.016448914161 | 0.014119323821 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000199355305 |
| s4064-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s4114-117 | 117 | 0 | 0.044055747086 | 0.079012084314 | 0.020294849703 | 0.058283987399 | 0.001940908851 | 0.006242909468 |
| s4115-117 | 117 | 0 | 0.016448914161 | 0.014500975667 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000210278295 |
| s4145-117 | 117 | 0 | 0.016448914161 | 0.014252411128 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000203131223 |
| s4148-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s4155-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s4159-117 | 117 | 0 | 0.016448914161 | 0.013004996570 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169129936 |
| s4163-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s4164-117 | 117 | 0 | 0.016448914161 | 0.015821841786 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000250330677 |
| s4169-117 | 117 | 0 | 0.016448914161 | 0.013783072558 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000189973089 |
| s4185-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s4187-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s419-117 | 117 | 0 | 0.016448914161 | 0.016374252307 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000268116139 |
| s4198-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s4201-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s4214-117 | 117 | 0 | 0.016448914161 | 0.014385697229 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000206948285 |
| s4229-117 | 117 | 0 | 0.016448914161 | 0.014119323821 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000199355305 |
| s4242-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s427-117 | 117 | 0 | 0.016448914161 | 0.013004996570 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169129936 |
| s429-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s43-117 | 117 | 0 | 0.016448914161 | 0.014385697229 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000206948285 |
| s430-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s4312-117 | 117 | 0 | 0.016448914161 | 0.013322522345 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000177489602 |
| s4313-117 | 117 | 0 | 0.016448914161 | 0.013004996570 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169129936 |
| s4344-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s4353-117 | 117 | 0 | 0.044055747086 | 0.031347565137 | 0.020294849703 | 0.058283987399 | 0.001940908851 | 0.000982669840 |
| s436-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s4373-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s4384-117 | 117 | 0 | 0.016448914161 | 0.013783072558 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000189973089 |
| s4395-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s4398-117 | 117 | 0 | 0.016448914161 | 0.013962254517 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000194944551 |
| s441-117 | 117 | 0 | 0.016448914161 | 0.015039173024 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000226176725 |
| s4425-117 | 117 | 0 | 0.016448914161 | 0.013004996570 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169129936 |
| s444-117 | 117 | 0 | 0.016448914161 | 0.022117471554 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000489182548 |
| s4451-117 | 117 | 0 | 0.016448914161 | 0.013783072558 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000189973089 |
| s457-117 | 117 | 0 | 0.016448914161 | 0.013783072558 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000189973089 |
| s476-117 | 117 | 0 | 0.016448914161 | 0.013783072558 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000189973089 |
| s478-117 | 117 | 0 | 0.016448914161 | 0.013574070368 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000184255386 |
| s492-117 | 117 | 0 | 0.016448914161 | 0.013004996570 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169129936 |
| s504-117 | 117 | 0 | 0.016448914161 | 0.014119323821 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000199355305 |
| s510-117 | 117 | 0 | 0.016448914161 | 0.014259313582 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000203328024 |
| s511-117 | 117 | 0 | 0.016448914161 | 0.011859687770 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140652194 |
| s512-117 | 117 | 0 | 0.016448914161 | 0.014607011119 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000213364774 |
| s524-117 | 117 | 0 | 0.016448914161 | 0.013574070368 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000184255386 |
| s528-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s538-117 | 117 | 0 | 0.016448914161 | 0.013004996570 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169129936 |
| s547-117 | 117 | 0 | 0.016448914161 | 0.016252969175 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000264159007 |
| s552-117 | 117 | 0 | 0.016448914161 | 0.013574070368 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000184255386 |
| s554-117 | 117 | 0 | 0.016448914161 | 0.026033466467 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000677741376 |
| s556-117 | 117 | 0 | 0.016448914161 | 0.015039173024 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000226176725 |
| s565-117 | 117 | 0 | 0.016448914161 | 0.022477347725 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000505231161 |
| s575-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s577-117 | 117 | 0 | 0.016448914161 | 0.013322522345 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000177489602 |
| s58-117 | 117 | 0 | 0.016448914161 | 0.014385697229 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000206948285 |
| s585-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s590-117 | 117 | 0 | 0.112687626852 | 0.101190297643 | 0.020294849703 | 0.202248763446 | 0.012698501245 | 0.010239476337 |
| s624-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s625-117 | 117 | 0 | 0.016448914161 | 0.013004996570 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169129936 |
| s640-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s649-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s664-117 | 117 | 0 | 0.016448914161 | 0.014252411128 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000203131223 |
| s681-117 | 117 | 0 | 0.016448914161 | 0.015111285145 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000228350939 |
| s682-117 | 117 | 0 | 0.016448914161 | 0.015039173024 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000226176725 |
| s693-117 | 117 | 0 | 0.044055747086 | 0.057215414433 | 0.020294849703 | 0.058283987399 | 0.001940908851 | 0.003273603649 |
| s705-117 | 117 | 0 | 0.016448914161 | 0.013004996570 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169129936 |
| s720-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s722-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s728-117 | 117 | 0 | 0.016448914161 | 0.014963058180 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000223893110 |
| s730-117 | 117 | 0 | 0.016448914161 | 0.015245103232 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000232413173 |
| s740-117 | 117 | 0 | 0.016448914161 | 0.014796743692 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000218943624 |
| s760-117 | 117 | 0 | 0.016448914161 | 0.013574070368 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000184255386 |
| s764-117 | 117 | 0 | 0.016448914161 | 0.014119323821 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000199355305 |
| s802-117 | 117 | 0 | 0.016448914161 | 0.014259313582 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000203328024 |
| s803-117 | 117 | 0 | 0.016448914161 | 0.013574070368 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000184255386 |
| s807-117 | 117 | 0 | 0.016448914161 | 0.026455336488 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000699884829 |
| s812-117 | 117 | 1 | 0.112687626852 | 0.167252065385 | 0.020294849703 | 0.202248763446 | 0.787323247542 | 0.693469122606 |
| s818-117 | 117 | 0 | 0.016448914161 | 0.027518292038 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000757256397 |
| s827-117 | 117 | 0 | 0.016448914161 | 0.014705228634 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000216243749 |
| s835-117 | 117 | 0 | 0.016448914161 | 0.010832933372 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000117352445 |
| s846-117 | 117 | 0 | 0.016448914161 | 0.015179810659 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000230426652 |
| s852-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s860-117 | 117 | 0 | 0.016448914161 | 0.013004996570 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169129936 |
| s869-117 | 117 | 0 | 0.016448914161 | 0.013322522345 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000177489602 |
| s884-117 | 117 | 0 | 0.016448914161 | 0.014119323821 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000199355305 |
| s887-117 | 117 | 0 | 0.016448914161 | 0.031521550091 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000993608120 |
| s89-117 | 117 | 0 | 0.112687626852 | 0.223689302530 | 0.020294849703 | 0.202248763446 | 0.012698501245 | 0.050036904067 |
| s892-117 | 117 | 0 | 0.016448914161 | 0.013574070368 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000184255386 |
| s900-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s910-117 | 117 | 0 | 0.016448914161 | 0.016155008893 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000260984312 |
| s912-117 | 117 | 0 | 0.016448914161 | 0.013783072558 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000189973089 |
| s933-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s936-117 | 117 | 0 | 0.016448914161 | 0.014119323821 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000199355305 |
| s946-117 | 117 | 0 | 0.016448914161 | 0.012570113761 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158007760 |
| s951-117 | 117 | 0 | 0.016448914161 | 0.027772143145 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000771291935 |
| s960-117 | 117 | 0 | 0.016448914161 | 0.014385697229 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000206948285 |
| s966-117 | 117 | 0 | 0.016448914161 | 0.015424416149 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000237912614 |
| s967-117 | 117 | 0 | 0.016448914161 | 0.014119323821 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000199355305 |
| s97-117 | 117 | 0 | 0.016448914161 | 0.013783072558 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000189973089 |
| s977-117 | 117 | 0 | 0.016448914161 | 0.013322522345 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000177489602 |
| s986-117 | 117 | 0 | 0.016448914161 | 0.015245103232 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000232413173 |
| s990-117 | 117 | 0 | 0.016448914161 | 0.011859687770 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140652194 |
| hr1006-118 | 118 | 0 | 0.015139467208 | 0.012736619538 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000162221477 |
| hr1008-118 | 118 | 0 | 0.015139467208 | 0.013650786866 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000186343982 |
| hr1011-118 | 118 | 0 | 0.015139467208 | 0.012972072509 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000168274665 |
| hr1021-118 | 118 | 0 | 0.015139467208 | 0.014841661145 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000220274906 |
| hr1050-118 | 118 | 0 | 0.015139467208 | 0.012131452490 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000147172140 |
| hr1084-118 | 118 | 0 | 0.015139467208 | 0.010691591249 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114310123 |
| hr1089-118 | 118 | 0 | 0.015139467208 | 0.019083298432 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000364172279 |
| hr1136-118 | 118 | 0 | 0.015139467208 | 0.014539685276 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000211402448 |
| hr1137-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr114-118 | 118 | 0 | 0.015139467208 | 0.014641257662 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000214366426 |
| hr1157-118 | 118 | 0 | 0.015139467208 | 0.009473118461 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000089739973 |
| hr1168-118 | 118 | 0 | 0.015139467208 | 0.012999777047 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000168994203 |
| hr117-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr1176-118 | 118 | 0 | 0.104531149070 | 0.166753382906 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.027806690711 |
| hr1192-118 | 118 | 0 | 0.015139467208 | 0.011572789939 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133929467 |
| hr1206-118 | 118 | 0 | 0.015139467208 | 0.012731536429 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000162092020 |
| hr1209-118 | 118 | 0 | 0.015139467208 | 0.037727586903 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.001423370813 |
| hr1227-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr1229-118 | 118 | 0 | 0.015139467208 | 0.013959851564 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000194877456 |
| hr1239-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr1250-118 | 118 | 0 | 0.015139467208 | 0.013983988429 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000195551932 |
| hr1261-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr1282-118 | 118 | 0 | 0.040639412606 | 0.092929477720 | 0.020294849703 | 0.058283987399 | 0.001651561857 | 0.008635887829 |
| hr1286-118 | 118 | 0 | 0.015139467208 | 0.012096230010 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000146318780 |
| hr130-118 | 118 | 0 | 0.015139467208 | 0.013884568159 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000192781233 |
| hr1310-118 | 118 | 0 | 0.015139467208 | 0.013076173285 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000170986308 |
| hr1314-118 | 118 | 0 | 0.015139467208 | 0.023777116649 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000565351276 |
| hr1322-118 | 118 | 0 | 0.015139467208 | 0.014337255489 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000205556895 |
| hr1338-118 | 118 | 0 | 0.040639412606 | 0.064396738888 | 0.020294849703 | 0.058283987399 | 0.001651561857 | 0.004146939979 |
| hr1374-118 | 118 | 0 | 0.015139467208 | 0.011062211715 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000122372528 |
| hr1384-118 | 118 | 0 | 0.015139467208 | 0.011725433683 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000137485795 |
| hr1385-118 | 118 | 0 | 0.015139467208 | 0.014708558097 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000216341681 |
| hr14-118 | 118 | 0 | 0.015139467208 | 0.015832812924 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000250677965 |
| hr1404-118 | 118 | 0 | 0.015139467208 | 0.012662792076 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000160346303 |
| hr1417-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr1447-118 | 118 | 0 | 0.015139467208 | 0.013171929411 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000173499724 |
| hr1449-118 | 118 | 0 | 0.015139467208 | 0.010159523563 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000103215919 |
| hr1468-118 | 118 | 0 | 0.015139467208 | 0.013076173285 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000170986308 |
| hr1474-118 | 118 | 0 | 0.015139467208 | 0.009810379037 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000096243537 |
| hr1483-118 | 118 | 0 | 0.015139467208 | 0.012589708309 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000158500755 |
| hr1497-118 | 118 | 0 | 0.015139467208 | 0.009741989088 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000094906351 |
| hr1505-118 | 118 | 1 | 0.015139467208 | 0.021895321626 | 0.020294849703 | 0.010486655910 | 0.969950269051 | 0.956688761858 |
| hr1509-118 | 118 | 0 | 0.015139467208 | 0.016002776792 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000256088865 |
| hr1510-118 | 118 | 0 | 0.015139467208 | 0.014629733781 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000214029110 |
| hr1588-118 | 118 | 0 | 0.015139467208 | 0.018070336694 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000326537068 |
| hr1589-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr1599-118 | 118 | 0 | 0.015139467208 | 0.010086249371 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000101732426 |
| hr1602-118 | 118 | 0 | 0.015139467208 | 0.014373145936 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000206587324 |
| hr1616-118 | 118 | 0 | 0.015139467208 | 0.011227524631 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000126057309 |
| hr1617-118 | 118 | 0 | 0.015139467208 | 0.014954226317 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000223628885 |
| hr1622-118 | 118 | 0 | 0.015139467208 | 0.012472851792 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000155572032 |
| hr1625-118 | 118 | 0 | 0.015139467208 | 0.010691591249 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114310123 |
| hr1637-118 | 118 | 0 | 0.015139467208 | 0.014239974444 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000202776872 |
| hr1644-118 | 118 | 0 | 0.040639412606 | 0.043363113733 | 0.020294849703 | 0.058283987399 | 0.001651561857 | 0.001880359633 |
| hr1651-118 | 118 | 0 | 0.040639412606 | 0.041956219186 | 0.020294849703 | 0.058283987399 | 0.001651561857 | 0.001760324328 |
| hr1654-118 | 118 | 0 | 0.015139467208 | 0.013343273913 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000178042959 |
| hr1686-118 | 118 | 0 | 0.015139467208 | 0.011465262765 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000131452250 |
| hr1687-118 | 118 | 0 | 0.015139467208 | 0.030648198033 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000939312043 |
| hr1691-118 | 118 | 0 | 0.015139467208 | 0.015121549243 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000228661251 |
| hr1699-118 | 118 | 0 | 0.015139467208 | 0.014585254091 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000212729637 |
| hr170-118 | 118 | 0 | 0.015139467208 | 0.009948588121 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000098974406 |
| hr171-118 | 118 | 0 | 0.015139467208 | 0.011945476515 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000142694409 |
| hr1724-118 | 118 | 0 | 0.015139467208 | 0.012589708309 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000158500755 |
| hr1742-118 | 118 | 0 | 0.015139467208 | 0.013595208356 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000184829690 |
| hr1749-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr1770-118 | 118 | 0 | 0.015139467208 | 0.015338254235 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000235262043 |
| hr1777-118 | 118 | 0 | 0.015139467208 | 0.015174413441 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000230262823 |
| hr1794-118 | 118 | 0 | 0.015139467208 | 0.014458802640 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000209056974 |
| hr1815-118 | 118 | 0 | 0.015139467208 | 0.027993176808 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000783617948 |
| hr1816-118 | 118 | 0 | 0.015139467208 | 0.013076173285 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000170986308 |
| hr1833-118 | 118 | 0 | 0.015139467208 | 0.015284316396 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000233610328 |
| hr185-118 | 118 | 0 | 0.104531149070 | 0.085187212292 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.007256861138 |
| hr1877-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr1927-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr1933-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr1934-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr1936-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr1996-118 | 118 | 0 | 0.015139467208 | 0.012295987933 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000151191319 |
| hr2023-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr2031-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr2038-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr2043-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr2064-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr2090-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr2098-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr2101-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr2121-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr2122-118 | 118 | 0 | 0.015139467208 | 0.011628181964 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000135214616 |
| hr2124-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr221-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr2216-118 | 118 | 0 | 0.015139467208 | 0.012295987933 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000151191319 |
| hr2225-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr2288-118 | 118 | 0 | 0.015139467208 | 0.016021807942 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000256698330 |
| hr2324-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr2332-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr2368-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr2377-118 | 118 | 0 | 0.015139467208 | 0.014606525742 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000213350594 |
| hr2380-118 | 118 | 0 | 0.015139467208 | 0.014163560689 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000200606451 |
| hr2384-118 | 118 | 0 | 0.015139467208 | 0.013232975662 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000175111645 |
| hr2442-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr2456-118 | 118 | 0 | 0.015139467208 | 0.012210484023 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000149095920 |
| hr2460-118 | 118 | 0 | 0.015139467208 | 0.009948588121 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000098974406 |
| hr2464-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr2469-118 | 118 | 0 | 0.015139467208 | 0.010691591249 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114310123 |
| hr2487-118 | 118 | 0 | 0.015139467208 | 0.009741989088 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000094906351 |
| hr249-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr2529-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr254-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr2546-118 | 118 | 0 | 0.015139467208 | 0.011332847735 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128433438 |
| hr2547-118 | 118 | 0 | 0.015139467208 | 0.013746236141 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000188959008 |
| hr2550-118 | 118 | 0 | 0.015139467208 | 0.013098960246 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000171582760 |
| hr2570-118 | 118 | 0 | 0.015139467208 | 0.011945476515 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000142694409 |
| hr2589-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr259-118 | 118 | 0 | 0.104531149070 | 0.095104117525 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.009044793170 |
| hr2604-118 | 118 | 0 | 0.015139467208 | 0.014076223821 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000198140077 |
| hr2620-118 | 118 | 0 | 0.015139467208 | 0.013171929411 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000173499724 |
| hr2621-118 | 118 | 0 | 0.015139467208 | 0.011878188213 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000141091355 |
| hr2631-118 | 118 | 0 | 0.015139467208 | 0.009810379037 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000096243537 |
| hr2633-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr2701-118 | 118 | 0 | 0.015139467208 | 0.010691591249 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114310123 |
| hr2739-118 | 118 | 0 | 0.015139467208 | 0.012662792076 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000160346303 |
| hr2744-118 | 118 | 0 | 0.015139467208 | 0.012131452490 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000147172140 |
| hr2761-118 | 118 | 0 | 0.015139467208 | 0.012012098285 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000144290505 |
| hr2767-118 | 118 | 0 | 0.015139467208 | 0.010691591249 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114310123 |
| hr2787-118 | 118 | 0 | 0.015139467208 | 0.012730629741 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000162068934 |
| hr2791-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr2793-118 | 118 | 0 | 0.104531149070 | 0.079479866741 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.006317049217 |
| hr2800-118 | 118 | 0 | 0.015139467208 | 0.013420672703 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000180114456 |
| hr2802-118 | 118 | 0 | 0.015139467208 | 0.011062211715 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000122372528 |
| hr2817-118 | 118 | 0 | 0.015139467208 | 0.010691591249 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114310123 |
| hr2823-118 | 118 | 0 | 0.015139467208 | 0.013025260080 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000169657400 |
| hr2833-118 | 118 | 0 | 0.015139467208 | 0.011878188213 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000141091355 |
| hr2841-118 | 118 | 0 | 0.015139467208 | 0.010691591249 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114310123 |
| hr2846-118 | 118 | 0 | 0.015139467208 | 0.012337503650 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000152213996 |
| hr288-118 | 118 | 0 | 0.104531149070 | 0.173124597845 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.029972126379 |
| hr2895-118 | 118 | 0 | 0.015139467208 | 0.012301954714 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000151338090 |
| hr290-118 | 118 | 0 | 0.104531149070 | 0.061917355598 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.003833758924 |
| hr2905-118 | 118 | 0 | 0.015139467208 | 0.012239210572 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000149798275 |
| hr2909-118 | 118 | 0 | 0.015139467208 | 0.010691591249 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114310123 |
| hr2910-118 | 118 | 0 | 0.015139467208 | 0.010691591249 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114310123 |
| hr298-118 | 118 | 0 | 0.104531149070 | 0.071824722714 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.005158790793 |
| hr2990-118 | 118 | 0 | 0.015139467208 | 0.013398803580 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000179527937 |
| hr3005-118 | 118 | 0 | 0.015139467208 | 0.013748206121 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000189013172 |
| hr3007-118 | 118 | 0 | 0.015139467208 | 0.013651771972 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000186370878 |
| hr3012-118 | 118 | 0 | 0.015139467208 | 0.011725433683 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000137485795 |
| hr3016-118 | 118 | 0 | 0.015139467208 | 0.012511669996 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000156541886 |
| hr3023-118 | 118 | 0 | 0.015139467208 | 0.014709898806 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000216381123 |
| hr3024-118 | 118 | 0 | 0.015139467208 | 0.012337503650 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000152213996 |
| hr3031-118 | 118 | 0 | 0.015139467208 | 0.010895117284 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000118703581 |
| hr3064-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr3071-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr3079-118 | 118 | 0 | 0.015139467208 | 0.012972072509 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000168274665 |
| hr3090-118 | 118 | 0 | 0.015139467208 | 0.016641296693 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000276932756 |
| hr3100-118 | 118 | 0 | 0.015139467208 | 0.012312545128 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000151598768 |
| hr3116-118 | 118 | 0 | 0.015139467208 | 0.011616504907 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000134943186 |
| hr3121-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr3127-118 | 118 | 0 | 0.015139467208 | 0.015288215390 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000233729530 |
| hr3132-118 | 118 | 0 | 0.015139467208 | 0.009407057280 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000088492727 |
| hr3134-118 | 118 | 0 | 0.015139467208 | 0.010918106525 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000119205050 |
| hr3170-118 | 118 | 0 | 0.015139467208 | 0.014768148187 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000218098201 |
| hr3174-118 | 118 | 0 | 0.015139467208 | 0.014267887542 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000203572615 |
| hr3179-118 | 118 | 0 | 0.015139467208 | 0.012972072509 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000168274665 |
| hr3181-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr3182-118 | 118 | 0 | 0.015139467208 | 0.010228304782 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000104618219 |
| hr3188-118 | 118 | 0 | 0.015139467208 | 0.014007677548 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000196215030 |
| hr3193-118 | 118 | 0 | 0.015139467208 | 0.010691591249 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114310123 |
| hr3210-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr3212-118 | 118 | 0 | 0.015139467208 | 0.015035681478 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000226071717 |
| hr3224-118 | 118 | 0 | 0.040639412606 | 0.043498139471 | 0.020294849703 | 0.058283987399 | 0.001651561857 | 0.001892088137 |
| hr3321-118 | 118 | 0 | 0.015139467208 | 0.010766575042 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000115919138 |
| hr3330-118 | 118 | 0 | 0.015139467208 | 0.009473118461 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000089739973 |
| hr3356-118 | 118 | 0 | 0.015139467208 | 0.011412276999 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000130240066 |
| hr3382-118 | 118 | 0 | 0.015139467208 | 0.014279250629 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000203896999 |
| hr3385-118 | 118 | 0 | 0.040639412606 | 0.062300982199 | 0.020294849703 | 0.058283987399 | 0.001651561857 | 0.003881412383 |
| hr3403-118 | 118 | 0 | 0.015139467208 | 0.012012098285 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000144290505 |
| hr3415-118 | 118 | 0 | 0.015139467208 | 0.028372214680 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000804982566 |
| hr3444-118 | 118 | 0 | 0.015139467208 | 0.013983988429 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000195551932 |
| hr3467-118 | 118 | 0 | 0.015139467208 | 0.010691591249 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114310123 |
| hr3472-118 | 118 | 0 | 0.015139467208 | 0.011062211715 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000122372528 |
| hr3478-118 | 118 | 0 | 0.015139467208 | 0.014220211476 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000202214414 |
| hr3490-118 | 118 | 0 | 0.015139467208 | 0.010766575042 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000115919138 |
| hr3498-118 | 118 | 0 | 0.015139467208 | 0.012662792076 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000160346303 |
| hr353-118 | 118 | 0 | 0.015139467208 | 0.012796447318 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000163749064 |
| hr3538-118 | 118 | 0 | 0.015139467208 | 0.012662792076 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000160346303 |
| hr3549-118 | 118 | 0 | 0.015139467208 | 0.011628181964 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000135214616 |
| hr3552-118 | 118 | 0 | 0.015139467208 | 0.010691591249 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114310123 |
| hr3561-118 | 118 | 0 | 0.015139467208 | 0.014906792988 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000222212477 |
| hr358-118 | 118 | 0 | 0.015139467208 | 0.011332847735 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128433438 |
| hr3602-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr3608-118 | 118 | 1 | 0.015139467208 | 0.014250909575 | 0.020294849703 | 0.010486655910 | 0.969950269051 | 0.971701269274 |
| hr3625-118 | 118 | 0 | 0.015139467208 | 0.014030935936 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000196867163 |
| hr3646-118 | 118 | 0 | 0.015139467208 | 0.014789727097 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000218736028 |
| hr3660-118 | 118 | 0 | 0.015139467208 | 0.012514925858 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000156623369 |
| hr3695-118 | 118 | 0 | 0.015139467208 | 0.011961393398 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000143074932 |
| hr3698-118 | 118 | 0 | 0.015139467208 | 0.017424984561 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000303630087 |
| hr3699-118 | 118 | 0 | 0.015139467208 | 0.010766575042 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000115919138 |
| hr3709-118 | 118 | 0 | 0.015139467208 | 0.014353200837 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000206014374 |
| hr3713-118 | 118 | 0 | 0.015139467208 | 0.014973309328 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000224199992 |
| hr3715-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr3734-118 | 118 | 0 | 0.015139467208 | 0.011062211715 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000122372528 |
| hr3738-118 | 118 | 0 | 0.015139467208 | 0.036832542108 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.001356636158 |
| hr3771-118 | 118 | 0 | 0.015139467208 | 0.010842078959 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000117550676 |
| hr3776-118 | 118 | 0 | 0.015139467208 | 0.011062211715 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000122372528 |
| hr3793-118 | 118 | 0 | 0.015139467208 | 0.011375666778 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000129405795 |
| hr3797-118 | 118 | 1 | 0.104531149070 | 0.060697702698 | 0.020294849703 | 0.202248763446 | 0.801864462985 | 0.882288805717 |
| hr3829-118 | 118 | 0 | 0.015139467208 | 0.014121518198 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000199417276 |
| hr3833-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr3836-118 | 118 | 0 | 0.040639412606 | 0.047382630071 | 0.020294849703 | 0.058283987399 | 0.001651561857 | 0.002245113632 |
| hr3845-118 | 118 | 0 | 0.015139467208 | 0.011807581629 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000139418984 |
| hr387-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr3875-118 | 118 | 0 | 0.015139467208 | 0.014203887080 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000201750408 |
| hr3887-118 | 118 | 0 | 0.015139467208 | 0.017815957865 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000317408355 |
| hr3937-118 | 118 | 0 | 0.040639412606 | 0.024231528573 | 0.020294849703 | 0.058283987399 | 0.001651561857 | 0.000587166977 |
| hr3939-118 | 118 | 0 | 0.015139467208 | 0.012337503650 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000152213996 |
| hr3940-118 | 118 | 0 | 0.015139467208 | 0.013776683890 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000189797019 |
| hr3947-118 | 118 | 1 | 0.015139467208 | 0.027234732592 | 0.020294849703 | 0.010486655910 | 0.969950269051 | 0.946272265475 |
| hr3952-118 | 118 | 0 | 0.015139467208 | 0.017034320937 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000290168090 |
| hr3977-118 | 118 | 0 | 0.015139467208 | 0.010691591249 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114310123 |
| hr3988-118 | 118 | 0 | 0.015139467208 | 0.013129749252 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000172390315 |
| hr3999-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr4-118 | 118 | 0 | 0.015139467208 | 0.014453051690 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000208890703 |
| hr4003-118 | 118 | 0 | 0.015139467208 | 0.022981873499 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000528166510 |
| hr4032-118 | 118 | 0 | 0.015139467208 | 0.011412276999 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000130240066 |
| hr4038-118 | 118 | 0 | 0.015139467208 | 0.012779571845 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000163317457 |
| hr4040-118 | 118 | 0 | 0.015139467208 | 0.012214478935 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000149193496 |
| hr4056-118 | 118 | 0 | 0.015139467208 | 0.014952544038 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000223578573 |
| hr4073-118 | 118 | 0 | 0.015139467208 | 0.012131452490 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000147172140 |
| hr4120-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr4146-118 | 118 | 0 | 0.015139467208 | 0.010766575042 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000115919138 |
| hr4162-118 | 118 | 0 | 0.015139467208 | 0.019333067293 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000373767491 |
| hr4165-118 | 118 | 0 | 0.015139467208 | 0.010691591249 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114310123 |
| hr4176-118 | 118 | 0 | 0.015139467208 | 0.012511669996 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000156541886 |
| hr4186-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr4194-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr4210-118 | 118 | 0 | 0.015139467208 | 0.012131452490 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000147172140 |
| hr4213-118 | 118 | 0 | 0.015139467208 | 0.016471101508 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000271297185 |
| hr4229-118 | 118 | 0 | 0.015139467208 | 0.011807581629 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000139418984 |
| hr423-118 | 118 | 1 | 0.104531149070 | 0.168715742554 | 0.020294849703 | 0.202248763446 | 0.801864462985 | 0.691033516678 |
| hr4232-118 | 118 | 0 | 0.015139467208 | 0.013627345633 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000185704549 |
| hr4241-118 | 118 | 0 | 0.015139467208 | 0.014711048272 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000216414941 |
| hr4245-118 | 118 | 0 | 0.015139467208 | 0.012731536429 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000162092020 |
| hr4249-118 | 118 | 0 | 0.015139467208 | 0.018788231007 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000352997624 |
| hr4255-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr4263-118 | 118 | 0 | 0.015139467208 | 0.013570430280 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000184156578 |
| hr4319-118 | 118 | 0 | 0.015139467208 | 0.012662792076 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000160346303 |
| hr4321-118 | 118 | 0 | 0.015139467208 | 0.012662792076 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000160346303 |
| hr4332-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr4346-118 | 118 | 0 | 0.015139467208 | 0.011878188213 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000141091355 |
| hr4368-118 | 118 | 0 | 0.040639412606 | 0.039661108666 | 0.020294849703 | 0.058283987399 | 0.001651561857 | 0.001573003541 |
| hr4372-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr4375-118 | 118 | 0 | 0.015139467208 | 0.012855915089 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000165274553 |
| hr4398-118 | 118 | 0 | 0.015139467208 | 0.013076173285 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000170986308 |
| hr4401-118 | 118 | 0 | 0.015139467208 | 0.010691591249 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114310123 |
| hr4408-118 | 118 | 0 | 0.015139467208 | 0.012851713116 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000165166530 |
| hr4467-118 | 118 | 1 | 0.040639412606 | 0.044287717855 | 0.020294849703 | 0.058283987399 | 0.920372736645 | 0.913385966244 |
| hr4472-118 | 118 | 0 | 0.015139467208 | 0.014808414231 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000219289132 |
| hr4478-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr4481-118 | 118 | 0 | 0.015139467208 | 0.011725433683 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000137485795 |
| hr4519-118 | 118 | 0 | 0.015139467208 | 0.015212943064 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000231433637 |
| hr4534-118 | 118 | 0 | 0.015139467208 | 0.013450279439 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000180910017 |
| hr4562-118 | 118 | 0 | 0.015139467208 | 0.013311990950 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000177209103 |
| hr4577-118 | 118 | 0 | 0.015139467208 | 0.013682854954 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000187220520 |
| hr4581-118 | 118 | 1 | 0.015139467208 | 0.014180153493 | 0.020294849703 | 0.010486655910 | 0.969950269051 | 0.971840769767 |
| hr4591-118 | 118 | 0 | 0.015139467208 | 0.012012098285 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000144290505 |
| hr4592-118 | 118 | 0 | 0.015139467208 | 0.009741989088 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000094906351 |
| hr4624-118 | 118 | 0 | 0.015139467208 | 0.012514925858 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000156623369 |
| hr4625-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr466-118 | 118 | 0 | 0.015139467208 | 0.010086249371 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000101732426 |
| hr4689-118 | 118 | 0 | 0.015139467208 | 0.014419641778 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000207926069 |
| hr469-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr4695-118 | 118 | 0 | 0.015139467208 | 0.012337503650 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000152213996 |
| hr4709-118 | 118 | 0 | 0.015139467208 | 0.013858447913 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000192056579 |
| hr4712-118 | 118 | 0 | 0.015139467208 | 0.011296489408 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000127610673 |
| hr4718-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr4722-118 | 118 | 0 | 0.015139467208 | 0.011062211715 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000122372528 |
| hr4723-118 | 118 | 0 | 0.015139467208 | 0.025834756597 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000667434648 |
| hr4777-118 | 118 | 0 | 0.015139467208 | 0.013436602281 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000180542281 |
| hr4785-118 | 118 | 0 | 0.015139467208 | 0.013309549890 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000177144118 |
| hr4799-118 | 118 | 0 | 0.015139467208 | 0.010691591249 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114310123 |
| hr4809-118 | 118 | 0 | 0.015139467208 | 0.011765199116 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000138419910 |
| hr4818-118 | 118 | 0 | 0.015139467208 | 0.014437434444 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000208439513 |
| hr482-118 | 118 | 0 | 0.015139467208 | 0.014037562378 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000197053158 |
| hr4826-118 | 118 | 0 | 0.015139467208 | 0.011874301967 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000140999047 |
| hr4832-118 | 118 | 0 | 0.015139467208 | 0.013760874983 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000189361680 |
| hr4884-118 | 118 | 0 | 0.015139467208 | 0.013246255840 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000175463294 |
| hr4930-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr4950-118 | 118 | 0 | 0.015139467208 | 0.011492256494 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000132071959 |
| hr4957-118 | 118 | 0 | 0.040639412606 | 0.046390121441 | 0.020294849703 | 0.058283987399 | 0.001651561857 | 0.002152043367 |
| hr4963-118 | 118 | 0 | 0.015139467208 | 0.015600448170 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000243373983 |
| hr4964-118 | 118 | 0 | 0.015139467208 | 0.013829471784 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000191254290 |
| hr4969-118 | 118 | 0 | 0.015139467208 | 0.013829471784 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000191254290 |
| hr4976-118 | 118 | 0 | 0.015139467208 | 0.012131452490 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000147172140 |
| hr4992-118 | 118 | 0 | 0.015139467208 | 0.013171929411 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000173499724 |
| hr5001-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr5018-118 | 118 | 0 | 0.015139467208 | 0.012662792076 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000160346303 |
| hr5025-118 | 118 | 0 | 0.015139467208 | 0.013562217462 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000183933742 |
| hr5034-118 | 118 | 0 | 0.015139467208 | 0.013526561028 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000182967853 |
| hr5040-118 | 118 | 0 | 0.015139467208 | 0.016624786488 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000276383526 |
| hr5048-118 | 118 | 0 | 0.015139467208 | 0.015481535472 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000239677941 |
| hr5049-118 | 118 | 0 | 0.015139467208 | 0.014658584087 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000214874087 |
| hr5053-118 | 118 | 0 | 0.015139467208 | 0.012131452490 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000147172140 |
| hr5054-118 | 118 | 0 | 0.015139467208 | 0.012662792076 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000160346303 |
| hr5073-118 | 118 | 0 | 0.015139467208 | 0.013719067590 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000188212816 |
| hr5077-118 | 118 | 0 | 0.015139467208 | 0.013858447913 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000192056579 |
| hr5085-118 | 118 | 0 | 0.015139467208 | 0.019684944070 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000387497023 |
| hr5086-118 | 118 | 0 | 0.015139467208 | 0.019986130011 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000399445393 |
| hr5100-118 | 118 | 0 | 0.015139467208 | 0.011878188213 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000141091355 |
| hr5128-118 | 118 | 0 | 0.015139467208 | 0.009407057280 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000088492727 |
| hr5149-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr5194-118 | 118 | 0 | 0.015139467208 | 0.011878188213 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000141091355 |
| hr5199-118 | 118 | 0 | 0.015139467208 | 0.015139589970 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000229207184 |
| hr5205-118 | 118 | 0 | 0.015139467208 | 0.010691591249 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114310123 |
| hr5214-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr5244-118 | 118 | 0 | 0.015139467208 | 0.012851713116 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000165166530 |
| hr528-118 | 118 | 0 | 0.015139467208 | 0.011878188213 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000141091355 |
| hr5283-118 | 118 | 0 | 0.104531149070 | 0.123039107865 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.015138622064 |
| hr5294-118 | 118 | 0 | 0.015139467208 | 0.014281503204 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000203961334 |
| hr5315-118 | 118 | 0 | 0.015139467208 | 0.012999777047 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000168994203 |
| hr5333-118 | 118 | 0 | 0.015139467208 | 0.012589708309 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000158500755 |
| hr5353-118 | 118 | 0 | 0.015139467208 | 0.013076173285 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000170986308 |
| hr536-118 | 118 | 0 | 0.015139467208 | 0.014442111315 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000208574579 |
| hr5372-118 | 118 | 0 | 0.015139467208 | 0.019863776598 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000394569621 |
| hr5381-118 | 118 | 0 | 0.015139467208 | 0.012113396980 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000146734386 |
| hr5404-118 | 118 | 0 | 0.015139467208 | 0.016726342988 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000279770550 |
| hr5409-118 | 118 | 0 | 0.015139467208 | 0.012398754749 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000153729119 |
| hr5411-118 | 118 | 0 | 0.015139467208 | 0.012776248023 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000163232514 |
| hr5428-118 | 118 | 0 | 0.015139467208 | 0.014952309037 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000223571546 |
| hr5452-118 | 118 | 0 | 0.015139467208 | 0.011492256494 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000132071959 |
| hr5467-118 | 118 | 0 | 0.015139467208 | 0.012423885828 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000154352939 |
| hr5488-118 | 118 | 0 | 0.015139467208 | 0.011725433683 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000137485795 |
| hr5506-118 | 118 | 0 | 0.015139467208 | 0.012096230010 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000146318780 |
| hr5522-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr5525-118 | 118 | 0 | 0.015139467208 | 0.012660975629 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000160300304 |
| hr553-118 | 118 | 0 | 0.015139467208 | 0.011725433683 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000137485795 |
| hr5535-118 | 118 | 0 | 0.015139467208 | 0.013927143455 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000193965325 |
| hr5536-118 | 118 | 1 | 0.015139467208 | 0.012662792076 | 0.020294849703 | 0.010486655910 | 0.969950269051 | 0.974834762150 |
| hr5552-118 | 118 | 0 | 0.015139467208 | 0.011628181964 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000135214616 |
| hr5561-118 | 118 | 0 | 0.015139467208 | 0.014373405119 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000206594775 |
| hr5568-118 | 118 | 0 | 0.015139467208 | 0.013978362346 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000195394614 |
| hr5571-118 | 118 | 0 | 0.015139467208 | 0.010691591249 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114310123 |
| hr5575-118 | 118 | 0 | 0.015139467208 | 0.009810379037 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000096243537 |
| hr5582-118 | 118 | 0 | 0.015139467208 | 0.040955695094 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.001677368961 |
| hr5588-118 | 118 | 0 | 0.015139467208 | 0.013625047557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000185641921 |
| hr5606-118 | 118 | 0 | 0.015139467208 | 0.013356857358 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000178405638 |
| hr5634-118 | 118 | 0 | 0.015139467208 | 0.013025260080 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000169657400 |
| hr5649-118 | 118 | 0 | 0.015139467208 | 0.010691591249 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114310123 |
| hr5668-118 | 118 | 0 | 0.015139467208 | 0.013657152588 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000186517817 |
| hr569-118 | 118 | 0 | 0.015139467208 | 0.011332847735 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128433438 |
| hr5692-118 | 118 | 0 | 0.104531149070 | 0.049248816286 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.002425445906 |
| hr5696-118 | 118 | 0 | 0.015139467208 | 0.012012098285 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000144290505 |
| hr572-118 | 118 | 0 | 0.015139467208 | 0.012427918653 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000154453162 |
| hr5721-118 | 118 | 0 | 0.040639412606 | 0.038240969041 | 0.020294849703 | 0.058283987399 | 0.001651561857 | 0.001462371713 |
| hr5731-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr5744-118 | 118 | 0 | 0.015139467208 | 0.010842078959 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000117550676 |
| hr5746-118 | 118 | 0 | 0.015139467208 | 0.010842078959 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000117550676 |
| hr5756-118 | 118 | 0 | 0.015139467208 | 0.011725433683 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000137485795 |
| hr5760-118 | 118 | 0 | 0.015139467208 | 0.015171268887 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000230167400 |
| hr5779-118 | 118 | 0 | 0.015139467208 | 0.028701143824 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000823755657 |
| hr5792-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr5799-118 | 118 | 1 | 0.015139467208 | 0.013062838916 | 0.020294849703 | 0.010486655910 | 0.969950269051 | 0.974044959929 |
| hr5803-118 | 118 | 0 | 0.015139467208 | 0.010691591249 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114310123 |
| hr5810-118 | 118 | 0 | 0.015139467208 | 0.014781236635 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000218484956 |
| hr5813-118 | 118 | 0 | 0.015139467208 | 0.013457612642 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000181107338 |
| hr5830-118 | 118 | 0 | 0.015139467208 | 0.010592163887 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000112193936 |
| hr5837-118 | 118 | 0 | 0.015139467208 | 0.011878188213 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000141091355 |
| hr5840-118 | 118 | 0 | 0.015139467208 | 0.013125006371 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000172265792 |
| hr5864-118 | 118 | 0 | 0.015139467208 | 0.012686631376 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000160950616 |
| hr5869-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr5876-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr5888-118 | 118 | 0 | 0.015139467208 | 0.010895117284 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000118703581 |
| hr5895-118 | 118 | 0 | 0.015139467208 | 0.015319074148 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000234674033 |
| hr5902-118 | 118 | 0 | 0.015139467208 | 0.012208731656 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000149053129 |
| hr5904-118 | 118 | 0 | 0.015139467208 | 0.014365531428 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000206368493 |
| hr5954-118 | 118 | 0 | 0.015139467208 | 0.013005891809 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000169153222 |
| hr6001-118 | 118 | 0 | 0.015139467208 | 0.013343129665 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000178039109 |
| hr6004-118 | 118 | 0 | 0.015139467208 | 0.014134657790 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000199788551 |
| hr6029-118 | 118 | 0 | 0.015139467208 | 0.012880081083 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000165896489 |
| hr6040-118 | 118 | 0 | 0.015139467208 | 0.012427918653 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000154453162 |
| hr6042-118 | 118 | 0 | 0.015139467208 | 0.010691591249 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114310123 |
| hr6049-118 | 118 | 0 | 0.015139467208 | 0.015432244026 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000238154156 |
| hr6063-118 | 118 | 0 | 0.015139467208 | 0.014141298723 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000199976330 |
| hr6074-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr6079-118 | 118 | 0 | 0.015139467208 | 0.013076173285 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000170986308 |
| hr6081-118 | 118 | 0 | 0.015139467208 | 0.024807873671 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000615430596 |
| hr6082-118 | 118 | 0 | 0.015139467208 | 0.011332847735 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128433438 |
| hr6085-118 | 118 | 0 | 0.015139467208 | 0.029423169823 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000865722922 |
| hr6129-118 | 118 | 0 | 0.015139467208 | 0.012599256059 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000158741253 |
| hr6140-118 | 118 | 0 | 0.015139467208 | 0.030913892857 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000955668772 |
| hr6152-118 | 118 | 0 | 0.015139467208 | 0.013154231957 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000173033818 |
| hr6176-118 | 118 | 0 | 0.015139467208 | 0.013901040597 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000193238930 |
| hr6188-118 | 118 | 1 | 0.015139467208 | 0.023137419873 | 0.020294849703 | 0.010486655910 | 0.969950269051 | 0.954260500453 |
| hr6196-118 | 118 | 0 | 0.015139467208 | 0.012427918653 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000154453162 |
| hr6206-118 | 118 | 0 | 0.015139467208 | 0.010691591249 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114310123 |
| hr6226-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr6231-118 | 118 | 0 | 0.040639412606 | 0.034530783152 | 0.020294849703 | 0.058283987399 | 0.001651561857 | 0.001192374985 |
| hr6239-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr6243-118 | 118 | 0 | 0.015139467208 | 0.010691591249 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114310123 |
| hr6245-118 | 118 | 0 | 0.104531149070 | 0.161258369283 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.026004261664 |
| hr6276-118 | 118 | 0 | 0.104531149070 | 0.108559224451 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.011785105213 |
| hr628-118 | 118 | 0 | 0.015139467208 | 0.011217856879 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000125840313 |
| hr6303-118 | 118 | 0 | 0.015139467208 | 0.009341452436 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000087262734 |
| hr6308-118 | 118 | 0 | 0.015139467208 | 0.010691591249 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114310123 |
| hr6311-118 | 118 | 0 | 0.015139467208 | 0.012180943722 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000148375390 |
| hr6317-118 | 118 | 0 | 0.040639412606 | 0.047279986305 | 0.020294849703 | 0.058283987399 | 0.001651561857 | 0.002235397105 |
| hr6324-118 | 118 | 1 | 0.015139467208 | 0.035629637248 | 0.020294849703 | 0.010486655910 | 0.969950269051 | 0.930010196555 |
| hr6334-118 | 118 | 0 | 0.015139467208 | 0.017412136338 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000303182492 |
| hr6337-118 | 118 | 0 | 0.015139467208 | 0.014896464173 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000221904645 |
| hr6341-118 | 118 | 0 | 0.015139467208 | 0.012337503650 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000152213996 |
| hr6345-118 | 118 | 0 | 0.015139467208 | 0.011062211715 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000122372528 |
| hr6350-118 | 118 | 0 | 0.015139467208 | 0.010766575042 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000115919138 |
| hr6352-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr6357-118 | 118 | 0 | 0.015139467208 | 0.013343273913 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000178042959 |
| hr6364-118 | 118 | 0 | 0.015139467208 | 0.013765712170 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000189494832 |
| hr6384-118 | 118 | 0 | 0.015139467208 | 0.011062211715 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000122372528 |
| hr6392-118 | 118 | 0 | 0.015139467208 | 0.010691591249 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114310123 |
| hr6393-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr6422-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr6450-118 | 118 | 0 | 0.015139467208 | 0.011791695372 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000139044080 |
| hr6455-118 | 118 | 0 | 0.015139467208 | 0.012916387309 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000166833061 |
| hr6462-118 | 118 | 0 | 0.015139467208 | 0.042337357723 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.001792451859 |
| hr6465-118 | 118 | 0 | 0.015139467208 | 0.012129534863 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000147125616 |
| hr6467-118 | 118 | 0 | 0.015139467208 | 0.011725433683 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000137485795 |
| hr6485-118 | 118 | 0 | 0.015139467208 | 0.012662792076 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000160346303 |
| hr6494-118 | 118 | 0 | 0.015139467208 | 0.011900538475 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000141622816 |
| hr650-118 | 118 | 0 | 0.015139467208 | 0.010669073815 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000113829136 |
| hr6507-118 | 118 | 0 | 0.015139467208 | 0.011279662402 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000127230784 |
| hr6520-118 | 118 | 0 | 0.015139467208 | 0.012337503650 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000152213996 |
| hr6523-118 | 118 | 0 | 0.015139467208 | 0.013343273913 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000178042959 |
| hr6524-118 | 118 | 0 | 0.015139467208 | 0.014533893167 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000211234051 |
| hr6525-118 | 118 | 0 | 0.015139467208 | 0.017615565658 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000310308153 |
| hr6531-118 | 118 | 0 | 0.015139467208 | 0.035763424154 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.001279022507 |
| hr6542-118 | 118 | 0 | 0.015139467208 | 0.013528324150 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000183015554 |
| hr6543-118 | 118 | 0 | 0.040639412606 | 0.076059406294 | 0.020294849703 | 0.058283987399 | 0.001651561857 | 0.005785033286 |
| hr6566-118 | 118 | 0 | 0.015139467208 | 0.011062211715 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000122372528 |
| hr6567-118 | 118 | 0 | 0.015139467208 | 0.013786196154 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000190059204 |
| hr6569-118 | 118 | 0 | 0.015139467208 | 0.018181866397 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000330580266 |
| hr6581-118 | 118 | 0 | 0.015139467208 | 0.012239210572 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000149798275 |
| hr6587-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr659-118 | 118 | 0 | 0.015139467208 | 0.012514925858 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000156623369 |
| hr6593-118 | 118 | 0 | 0.015139467208 | 0.012731536429 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000162092020 |
| hr6601-118 | 118 | 0 | 0.015139467208 | 0.012131452490 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000147172140 |
| hr6652-118 | 118 | 0 | 0.015139467208 | 0.014030935936 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000196867163 |
| hr6699-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr6705-118 | 118 | 0 | 0.015139467208 | 0.011375666778 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000129405795 |
| hr6712-118 | 118 | 0 | 0.015139467208 | 0.010691591249 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114310123 |
| hr6731-118 | 118 | 0 | 0.015139467208 | 0.012266243344 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000150460726 |
| hr6745-118 | 118 | 0 | 0.015139467208 | 0.011878188213 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000141091355 |
| hr6747-118 | 118 | 0 | 0.015139467208 | 0.019680917440 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000387338511 |
| hr676-118 | 118 | 0 | 0.104531149070 | 0.123880846760 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.015346464194 |
| hr6778-118 | 118 | 0 | 0.015139467208 | 0.011332847735 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128433438 |
| hr6788-118 | 118 | 0 | 0.015139467208 | 0.010691591249 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114310123 |
| hr6809-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr6820-118 | 118 | 0 | 0.015139467208 | 0.012939792478 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000167438229 |
| hr6822-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr6834-118 | 118 | 0 | 0.015139467208 | 0.011628181964 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000135214616 |
| hr6837-118 | 118 | 0 | 0.015139467208 | 0.010766575042 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000115919138 |
| hr6878-118 | 118 | 0 | 0.015139467208 | 0.009407057280 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000088492727 |
| hr6886-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr6888-118 | 118 | 0 | 0.015139467208 | 0.013343273913 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000178042959 |
| hr6896-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr6902-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr6915-118 | 118 | 0 | 0.015139467208 | 0.010994661292 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000120882577 |
| hr6920-118 | 118 | 0 | 0.015139467208 | 0.014883684740 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000221524071 |
| hr6929-118 | 118 | 0 | 0.015139467208 | 0.015927703457 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000253691737 |
| hr693-118 | 118 | 0 | 0.015139467208 | 0.018278723710 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000334111740 |
| hr6936-118 | 118 | 0 | 0.015139467208 | 0.011332847735 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128433438 |
| hr6960-118 | 118 | 1 | 0.104531149070 | 0.138914843777 | 0.020294849703 | 0.202248763446 | 0.801864462985 | 0.741467646268 |
| hr6964-118 | 118 | 0 | 0.015139467208 | 0.012398754749 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000153729119 |
| hr70-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr7006-118 | 118 | 0 | 0.015139467208 | 0.014301813238 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000204541862 |
| hr7011-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr7022-118 | 118 | 0 | 0.015139467208 | 0.010691591249 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114310123 |
| hr703-118 | 118 | 0 | 0.015139467208 | 0.014262376891 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000203415395 |
| hr7033-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr7043-118 | 118 | 0 | 0.015139467208 | 0.010766575042 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000115919138 |
| hr7060-118 | 118 | 0 | 0.015139467208 | 0.012589708309 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000158500755 |
| hr7064-118 | 118 | 0 | 0.015139467208 | 0.010691591249 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114310123 |
| hr7081-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr7101-118 | 118 | 0 | 0.015139467208 | 0.012865662094 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000165525261 |
| hr7102-118 | 118 | 0 | 0.104531149070 | 0.071057932406 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.005049229758 |
| hr7112-118 | 118 | 0 | 0.015139467208 | 0.010372339948 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000107585436 |
| hr7114-118 | 118 | 0 | 0.015139467208 | 0.011062211715 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000122372528 |
| hr7122-118 | 118 | 0 | 0.040639412606 | 0.035185170539 | 0.020294849703 | 0.058283987399 | 0.001651561857 | 0.001237996226 |
| hr7145-118 | 118 | 0 | 0.015139467208 | 0.013658674189 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000186559381 |
| hr7150-118 | 118 | 0 | 0.015139467208 | 0.017496746193 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000306136127 |
| hr7184-118 | 118 | 0 | 0.015139467208 | 0.011957480259 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000142981334 |
| hr7227-118 | 118 | 0 | 0.015139467208 | 0.035131057333 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.001234191189 |
| hr7231-118 | 118 | 0 | 0.015139467208 | 0.011725433683 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000137485795 |
| hr7274-118 | 118 | 0 | 0.015139467208 | 0.013446783551 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000180815988 |
| hr7297-118 | 118 | 0 | 0.015139467208 | 0.014337255489 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000205556895 |
| hr7316-118 | 118 | 0 | 0.015139467208 | 0.009606622297 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000092287192 |
| hr7323-118 | 118 | 0 | 0.015139467208 | 0.018405928677 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000338778210 |
| hr7326-118 | 118 | 0 | 0.015139467208 | 0.009341452436 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000087262734 |
| hr7341-118 | 118 | 0 | 0.015139467208 | 0.009341452436 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000087262734 |
| hr7351-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr7364-118 | 118 | 0 | 0.015139467208 | 0.009276300835 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000086049757 |
| hr7369-118 | 118 | 0 | 0.015139467208 | 0.011332847735 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128433438 |
| hr7372-118 | 118 | 0 | 0.015139467208 | 0.012731536429 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000162092020 |
| hr7422-118 | 118 | 0 | 0.015139467208 | 0.013621153684 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000185535828 |
| hr7457-118 | 118 | 0 | 0.015139467208 | 0.012796447318 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000163749064 |
| hr7462-118 | 118 | 0 | 0.040639412606 | 0.055530963945 | 0.020294849703 | 0.058283987399 | 0.001651561857 | 0.003083687957 |
| hr7469-118 | 118 | 0 | 0.015139467208 | 0.012511669996 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000156541886 |
| hr747-118 | 118 | 0 | 0.015139467208 | 0.011332847735 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128433438 |
| hr7497-118 | 118 | 0 | 0.015139467208 | 0.010691591249 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114310123 |
| hr7516-118 | 118 | 0 | 0.015139467208 | 0.018728225250 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000350746421 |
| hr7543-118 | 118 | 0 | 0.015139467208 | 0.028319383715 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000801987494 |
| hr7561-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr7569-118 | 118 | 0 | 0.015139467208 | 0.012337503650 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000152213996 |
| hr7570-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr7574-118 | 118 | 0 | 0.015139467208 | 0.011725433683 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000137485795 |
| hr758-118 | 118 | 0 | 0.015139467208 | 0.012796447318 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000163749064 |
| hr7584-118 | 118 | 0 | 0.015139467208 | 0.012662792076 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000160346303 |
| hr7600-118 | 118 | 0 | 0.015139467208 | 0.014007398356 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000196207209 |
| hr7601-118 | 118 | 0 | 0.015139467208 | 0.010691591249 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114310123 |
| hr7611-118 | 118 | 0 | 0.015139467208 | 0.009473118461 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000089739973 |
| hr7614-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr7620-118 | 118 | 0 | 0.015139467208 | 0.012589708309 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000158500755 |
| hr7623-118 | 118 | 0 | 0.015139467208 | 0.020378284984 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000415274499 |
| hr7637-118 | 118 | 0 | 0.104531149070 | 0.103209588827 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.010652219226 |
| hr765-118 | 118 | 0 | 0.015139467208 | 0.015093975175 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000227828087 |
| hr7653-118 | 118 | 0 | 0.015139467208 | 0.015047520242 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000226427865 |
| hr7659-118 | 118 | 0 | 0.104531149070 | 0.088152815861 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.007770918944 |
| hr7665-118 | 118 | 0 | 0.015139467208 | 0.011890298175 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000141379191 |
| hr7679-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr7685-118 | 118 | 0 | 0.040639412606 | 0.038941376203 | 0.020294849703 | 0.058283987399 | 0.001651561857 | 0.001516430781 |
| hr771-118 | 118 | 0 | 0.015139467208 | 0.012337503650 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000152213996 |
| hr7724-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr7772-118 | 118 | 0 | 0.015139467208 | 0.012337503650 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000152213996 |
| hr7779-118 | 118 | 0 | 0.015139467208 | 0.009276300835 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000086049757 |
| hr7828-118 | 118 | 0 | 0.015139467208 | 0.013665325469 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000186741120 |
| hr7831-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr7849-118 | 118 | 0 | 0.015139467208 | 0.013343273913 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000178042959 |
| hr7856-118 | 118 | 0 | 0.015139467208 | 0.015400920193 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000237188343 |
| hr787-118 | 118 | 0 | 0.015139467208 | 0.011725433683 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000137485795 |
| hr7878-118 | 118 | 0 | 0.015139467208 | 0.011062211715 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000122372528 |
| hr7879-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr7880-118 | 118 | 0 | 0.015139467208 | 0.010691591249 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114310123 |
| hr7884-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr7909-118 | 118 | 0 | 0.104531149070 | 0.167793758052 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.028154745241 |
| hr7944-118 | 118 | 0 | 0.015139467208 | 0.012886000908 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000166049019 |
| hr7988-118 | 118 | 0 | 0.104531149070 | 0.079469237004 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.006315359630 |
| hr800-118 | 118 | 0 | 0.015139467208 | 0.014339483555 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000205620789 |
| hr8025-118 | 118 | 0 | 0.015139467208 | 0.013343273913 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000178042959 |
| hr8032-118 | 118 | 0 | 0.015139467208 | 0.011572789939 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133929467 |
| hr8084-118 | 118 | 0 | 0.104531149070 | 0.143625035906 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.020628150939 |
| hr8086-118 | 118 | 0 | 0.015139467208 | 0.011616504907 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000134943186 |
| hr8094-118 | 118 | 0 | 0.015139467208 | 0.009674071239 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000093587654 |
| hr8100-118 | 118 | 0 | 0.015139467208 | 0.012337503650 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000152213996 |
| hr8133-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr820-118 | 118 | 0 | 0.015139467208 | 0.011983898322 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000143613819 |
| hr8210-118 | 118 | 0 | 0.015139467208 | 0.021989508911 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000483538502 |
| hr8218-118 | 118 | 0 | 0.015139467208 | 0.011725433683 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000137485795 |
| hr8222-118 | 118 | 0 | 0.015139467208 | 0.010691591249 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114310123 |
| hr823-118 | 118 | 0 | 0.015139467208 | 0.011306224153 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000127830705 |
| hr8246-118 | 118 | 0 | 0.015139467208 | 0.010842078959 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000117550676 |
| hr8250-118 | 118 | 0 | 0.015139467208 | 0.009473118461 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000089739973 |
| hr8254-118 | 118 | 0 | 0.015139467208 | 0.011332847735 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128433438 |
| hr8280-118 | 118 | 0 | 0.015139467208 | 0.011062211715 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000122372528 |
| hr8292-118 | 118 | 0 | 0.104531149070 | 0.154231757571 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.023787435044 |
| hr8298-118 | 118 | 0 | 0.015139467208 | 0.012427918653 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000154453162 |
| hr8318-118 | 118 | 0 | 0.015139467208 | 0.012511669996 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000156541886 |
| hr8324-118 | 118 | 0 | 0.015139467208 | 0.009276300835 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000086049757 |
| hr8328-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr8334-118 | 118 | 0 | 0.015139467208 | 0.012673689139 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000160622396 |
| hr8338-118 | 118 | 0 | 0.015139467208 | 0.011149366738 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000124308379 |
| hr835-118 | 118 | 0 | 0.104531149070 | 0.130814185811 | 0.020294849703 | 0.202248763446 | 0.010926761126 | 0.017112351209 |
| hr8370-118 | 118 | 0 | 0.015139467208 | 0.014997479724 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000224924398 |
| hr8373-118 | 118 | 0 | 0.015139467208 | 0.012012098285 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000144290505 |
| hr8405-118 | 118 | 0 | 0.015139467208 | 0.029934392383 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000896067847 |
| hr8413-118 | 118 | 1 | 0.015139467208 | 0.028277925009 | 0.020294849703 | 0.010486655910 | 0.969950269051 | 0.944243791025 |
| hr8436-118 | 118 | 0 | 0.015139467208 | 0.019822328787 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000392924719 |
| hr8446-118 | 118 | 0 | 0.040639412606 | 0.088223855140 | 0.020294849703 | 0.058283987399 | 0.001651561857 | 0.007783448616 |
| hr8473-118 | 118 | 0 | 0.015139467208 | 0.011332847735 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128433438 |
| hr8494-118 | 118 | 0 | 0.015139467208 | 0.009341452436 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000087262734 |
| hr8534-118 | 118 | 0 | 0.040639412606 | 0.037513902455 | 0.020294849703 | 0.058283987399 | 0.001651561857 | 0.001407292877 |
| hr8544-118 | 118 | 0 | 0.015139467208 | 0.012210484023 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000149095920 |
| hr8568-118 | 118 | 0 | 0.015139467208 | 0.013382585488 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000179093594 |
| hr857-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr8571-118 | 118 | 0 | 0.015139467208 | 0.017804823744 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000317011749 |
| hr8596-118 | 118 | 0 | 0.015139467208 | 0.011062211715 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000122372528 |
| hr860-118 | 118 | 0 | 0.015139467208 | 0.011878188213 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000141091355 |
| hr8601-118 | 118 | 0 | 0.015139467208 | 0.012352132825 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000152575185 |
| hr8606-118 | 118 | 0 | 0.040639412606 | 0.037154995792 | 0.020294849703 | 0.058283987399 | 0.001651561857 | 0.001380493712 |
| hr8662-118 | 118 | 0 | 0.040639412606 | 0.044550604324 | 0.020294849703 | 0.058283987399 | 0.001651561857 | 0.001984756346 |
| hr8664-118 | 118 | 0 | 0.040639412606 | 0.044550604324 | 0.020294849703 | 0.058283987399 | 0.001651561857 | 0.001984756346 |
| hr8683-118 | 118 | 0 | 0.015139467208 | 0.026495712189 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000702022764 |
| hr8689-118 | 118 | 0 | 0.040639412606 | 0.075398414923 | 0.020294849703 | 0.058283987399 | 0.001651561857 | 0.005684920973 |
| hr8729-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr8742-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr8751-118 | 118 | 0 | 0.015139467208 | 0.010691591249 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114310123 |
| hr878-118 | 118 | 0 | 0.015139467208 | 0.011062211715 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000122372528 |
| hr8780-118 | 118 | 0 | 0.015139467208 | 0.011332847735 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000128433438 |
| hr8792-118 | 118 | 0 | 0.015139467208 | 0.011765199116 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000138419910 |
| hr8816-118 | 118 | 0 | 0.015139467208 | 0.009341452436 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000087262734 |
| hr8840-118 | 118 | 0 | 0.015139467208 | 0.010691591249 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000114310123 |
| hr8853-118 | 118 | 0 | 0.015139467208 | 0.009276300835 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000086049757 |
| hr8863-118 | 118 | 0 | 0.015139467208 | 0.012731536429 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000162092020 |
| hr8865-118 | 118 | 0 | 0.015139467208 | 0.038716110094 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.001498937181 |
| hr8898-118 | 118 | 0 | 0.015139467208 | 0.011725433683 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000137485795 |
| hr8902-118 | 118 | 0 | 0.015139467208 | 0.012012098285 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000144290505 |
| hr8907-118 | 118 | 0 | 0.015139467208 | 0.011725433683 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000137485795 |
| hr891-118 | 118 | 0 | 0.015139467208 | 0.014759565541 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000217844775 |
| hr8913-118 | 118 | 0 | 0.040639412606 | 0.089449815437 | 0.020294849703 | 0.058283987399 | 0.001651561857 | 0.008001269482 |
| hr8926-118 | 118 | 0 | 0.015139467208 | 0.013032204741 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000169838360 |
| hr926-118 | 118 | 0 | 0.015139467208 | 0.014686825237 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000215702836 |
| hr937-118 | 118 | 0 | 0.015139467208 | 0.011547267557 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000133339388 |
| hr953-118 | 118 | 0 | 0.015139467208 | 0.014242965431 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000202862064 |
| hr955-118 | 118 | 0 | 0.015139467208 | 0.013595405848 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000184835060 |
| hr968-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr978-118 | 118 | 0 | 0.015139467208 | 0.009211599406 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000084853564 |
| hr991-118 | 118 | 0 | 0.015139467208 | 0.013498858399 | 0.020294849703 | 0.010486655910 | 0.000229203467 | 0.000182219178 |
| s1001-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s1005-118 | 118 | 0 | 0.016448914161 | 0.012584222072 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158362645 |
| s102-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s1023-118 | 118 | 0 | 0.016448914161 | 0.013019586545 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169509634 |
| s1025-118 | 118 | 0 | 0.016448914161 | 0.013337463730 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000177887939 |
| s1035-118 | 118 | 0 | 0.016448914161 | 0.013977903206 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000195381778 |
| s1036-118 | 118 | 0 | 0.016448914161 | 0.013977903206 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000195381778 |
| s1044-118 | 118 | 0 | 0.016448914161 | 0.012584222072 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158362645 |
| s1048-118 | 118 | 0 | 0.016448914161 | 0.013188975810 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000173949083 |
| s1054-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s1055-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s1058-118 | 118 | 0 | 0.016448914161 | 0.012822011099 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000164403969 |
| s1080-118 | 118 | 0 | 0.044055747086 | 0.085426195383 | 0.020294849703 | 0.058283987399 | 0.001940908851 | 0.007297634858 |
| s1092-118 | 118 | 0 | 0.016448914161 | 0.012584222072 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158362645 |
| s110-118 | 118 | 0 | 0.016448914161 | 0.013891381114 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000192970469 |
| s1143-118 | 118 | 0 | 0.016448914161 | 0.013589289982 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000184668802 |
| s1148-118 | 118 | 0 | 0.016448914161 | 0.012584222072 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158362645 |
| s115-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s1154-118 | 118 | 0 | 0.016448914161 | 0.013019586545 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169509634 |
| s1179-118 | 118 | 0 | 0.016448914161 | 0.012584222072 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158362645 |
| s1190-118 | 118 | 0 | 0.016448914161 | 0.014340080096 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000205637897 |
| s1192-118 | 118 | 0 | 0.016448914161 | 0.013798523233 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000190399243 |
| s1197-118 | 118 | 0 | 0.016448914161 | 0.013019586545 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169509634 |
| s1199-118 | 118 | 0 | 0.044055747086 | 0.034693377879 | 0.020294849703 | 0.058283987399 | 0.001940908851 | 0.001203630469 |
| s120-118 | 118 | 0 | 0.016448914161 | 0.014768284140 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000218102216 |
| s1209-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s1217-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s1222-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s1239-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s1245-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s1246-118 | 118 | 0 | 0.016448914161 | 0.014899110729 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000221983501 |
| s1247-118 | 118 | 0 | 0.016448914161 | 0.013019586545 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169509634 |
| s1265-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s1268-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s1287-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s1292-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s1304-118 | 118 | 0 | 0.016448914161 | 0.013337463730 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000177887939 |
| s1316-118 | 118 | 0 | 0.016448914161 | 0.012584222072 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158362645 |
| s1317-118 | 118 | 0 | 0.016448914161 | 0.013019586545 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169509634 |
| s1320-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s1335-118 | 118 | 0 | 0.016448914161 | 0.012584222072 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158362645 |
| s1340-118 | 118 | 0 | 0.016448914161 | 0.012584222072 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158362645 |
| s1351-118 | 118 | 1 | 0.016448914161 | 0.014058930763 | 0.020294849703 | 0.010486655910 | 0.967372738455 | 0.972079792008 |
| s1358-118 | 118 | 0 | 0.016448914161 | 0.013188975810 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000173949083 |
| s1359-118 | 118 | 0 | 0.016448914161 | 0.012822011099 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000164403969 |
| s1361-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s1368-118 | 118 | 0 | 0.016448914161 | 0.012584222072 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158362645 |
| s1375-118 | 118 | 0 | 0.016448914161 | 0.014135146027 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000199802353 |
| s1379-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s1382-118 | 118 | 0 | 0.016448914161 | 0.013698275182 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000187642743 |
| s1385-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s1387-118 | 118 | 0 | 0.112687626852 | 0.122028689161 | 0.020294849703 | 0.202248763446 | 0.012698501245 | 0.014891000978 |
| s1388-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s1396-118 | 118 | 0 | 0.044055747086 | 0.049287034556 | 0.020294849703 | 0.058283987399 | 0.001940908851 | 0.002429211775 |
| s1408-118 | 118 | 0 | 0.016448914161 | 0.013337463730 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000177887939 |
| s1416-118 | 118 | 0 | 0.016448914161 | 0.012467415835 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000155436458 |
| s1418-118 | 118 | 0 | 0.016448914161 | 0.021435307326 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000459472400 |
| s1428-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s1445-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s1446-118 | 118 | 0 | 0.016448914161 | 0.013798523233 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000190399243 |
| s1464-118 | 118 | 0 | 0.044055747086 | 0.074909815645 | 0.020294849703 | 0.058283987399 | 0.001940908851 | 0.005611480480 |
| s1495-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s1507-118 | 118 | 0 | 0.016448914161 | 0.013798523233 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000190399243 |
| s1533-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s1547-118 | 118 | 0 | 0.016448914161 | 0.012822011099 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000164403969 |
| s156-118 | 118 | 0 | 0.016448914161 | 0.014058930763 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000197653534 |
| s1563-118 | 118 | 0 | 0.016448914161 | 0.013469807445 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000181435713 |
| s1572-118 | 118 | 0 | 0.016448914161 | 0.013716872630 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000188152595 |
| s1591-118 | 118 | 0 | 0.016448914161 | 0.013698275182 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000187642743 |
| s1608-118 | 118 | 1 | 0.112687626852 | 0.103985896547 | 0.020294849703 | 0.202248763446 | 0.787323247542 | 0.802841273586 |
| s1611-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s1613-118 | 118 | 0 | 0.016448914161 | 0.013019586545 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169509634 |
| s1614-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s1621-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s1622-118 | 118 | 0 | 0.016448914161 | 0.015226911400 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000231858831 |
| s1626-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s1647-118 | 118 | 0 | 0.016448914161 | 0.013798523233 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000190399243 |
| s1651-118 | 118 | 0 | 0.016448914161 | 0.012822011099 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000164403969 |
| s1672-118 | 118 | 0 | 0.016448914161 | 0.013469807445 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000181435713 |
| s1682-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s1683-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s1684-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s1694-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s1698-118 | 118 | 0 | 0.016448914161 | 0.015018440667 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000225553560 |
| s1706-118 | 118 | 0 | 0.016448914161 | 0.014940058396 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000223205345 |
| s1707-118 | 118 | 0 | 0.016448914161 | 0.012822011099 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000164403969 |
| s1717-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s1718-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s1745-118 | 118 | 0 | 0.016448914161 | 0.013019586545 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169509634 |
| s1753-118 | 118 | 0 | 0.016448914161 | 0.013698275182 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000187642743 |
| s1759-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s182-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s1833-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s1834-118 | 118 | 0 | 0.016448914161 | 0.012584222072 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158362645 |
| s1848-118 | 118 | 0 | 0.016448914161 | 0.013337463730 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000177887939 |
| s1858-118 | 118 | 1 | 0.112687626852 | 0.090370177858 | 0.020294849703 | 0.202248763446 | 0.787323247542 | 0.827426413330 |
| s1875-118 | 118 | 0 | 0.016448914161 | 0.013469807445 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000181435713 |
| s1890-118 | 118 | 0 | 0.016448914161 | 0.015048039530 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000226443494 |
| s1891-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s1893-118 | 118 | 0 | 0.016448914161 | 0.014517219257 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000210749655 |
| s1897-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s190-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s1925-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s1948-118 | 118 | 0 | 0.016448914161 | 0.013188975810 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000173949083 |
| s1952-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s1953-118 | 118 | 0 | 0.016448914161 | 0.013589289982 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000184668802 |
| s1963-118 | 118 | 0 | 0.016448914161 | 0.013698275182 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000187642743 |
| s1986-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s1996-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s1997-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s2000-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s2002-118 | 118 | 0 | 0.016448914161 | 0.012584222072 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158362645 |
| s2018-118 | 118 | 0 | 0.016448914161 | 0.026014039750 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000676730264 |
| s2019-118 | 118 | 0 | 0.016448914161 | 0.013977903206 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000195381778 |
| s2025-118 | 118 | 0 | 0.016448914161 | 0.013019586545 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169509634 |
| s2032-118 | 118 | 0 | 0.016448914161 | 0.015798859614 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000249603965 |
| s207-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s2083-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s2089-118 | 118 | 0 | 0.016448914161 | 0.013469807445 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000181435713 |
| s2096-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s2116-118 | 118 | 0 | 0.044055747086 | 0.086417477665 | 0.020294849703 | 0.058283987399 | 0.001940908851 | 0.007467980446 |
| s2139-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s2140-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s2142-118 | 118 | 0 | 0.016448914161 | 0.013589289982 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000184668802 |
| s2151-118 | 118 | 0 | 0.016448914161 | 0.024388565765 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000594802140 |
| s216-118 | 118 | 0 | 0.016448914161 | 0.013182776120 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000173785586 |
| s2175-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s2188-118 | 118 | 0 | 0.016448914161 | 0.011201533735 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000125474358 |
| s2190-118 | 118 | 0 | 0.044055747086 | 0.071882511289 | 0.020294849703 | 0.058283987399 | 0.001940908851 | 0.005167095429 |
| s2192-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s2194-118 | 118 | 0 | 0.016448914161 | 0.013469807445 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000181435713 |
| s2209-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s2214-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s2216-118 | 118 | 0 | 0.016448914161 | 0.017018114954 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000289616237 |
| s2219-118 | 118 | 0 | 0.044055747086 | 0.072915994493 | 0.020294849703 | 0.058283987399 | 0.001940908851 | 0.005316742253 |
| s2241-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s2263-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s2266-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s2272-118 | 118 | 0 | 0.044055747086 | 0.045707929871 | 0.020294849703 | 0.058283987399 | 0.001940908851 | 0.002089214853 |
| s2279-118 | 118 | 0 | 0.016448914161 | 0.014275290390 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000203783916 |
| s228-118 | 118 | 0 | 0.016448914161 | 0.014571354486 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000212324372 |
| s2281-118 | 118 | 0 | 0.016448914161 | 0.024778468431 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000613972498 |
| s229-118 | 118 | 0 | 0.016448914161 | 0.024665491951 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000608386493 |
| s2290-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s2293-118 | 118 | 0 | 0.016448914161 | 0.013000226600 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169005892 |
| s2298-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s2299-118 | 118 | 0 | 0.016448914161 | 0.014460777427 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000209114084 |
| s230-118 | 118 | 0 | 0.016448914161 | 0.013891381114 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000192970469 |
| s2313-118 | 118 | 0 | 0.016448914161 | 0.013977903206 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000195381778 |
| s2322-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s2346-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s235-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s236-118 | 118 | 0 | 0.016448914161 | 0.012584222072 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158362645 |
| s2363-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s2366-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s2386-118 | 118 | 0 | 0.016448914161 | 0.012822011099 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000164403969 |
| s239-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s2390-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s2398-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s2412-118 | 118 | 0 | 0.016448914161 | 0.013019586545 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169509634 |
| s2432-118 | 118 | 0 | 0.016448914161 | 0.013019586545 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169509634 |
| s2441-118 | 118 | 0 | 0.016448914161 | 0.013019586545 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169509634 |
| s2442-118 | 118 | 0 | 0.016448914161 | 0.012822011099 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000164403969 |
| s2448-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s2452-118 | 118 | 0 | 0.016448914161 | 0.012584222072 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158362645 |
| s2464-118 | 118 | 0 | 0.016448914161 | 0.012584222072 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158362645 |
| s2468-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s2483-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s2488-118 | 118 | 0 | 0.016448914161 | 0.014940058396 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000223205345 |
| s2491-118 | 118 | 0 | 0.016448914161 | 0.013019586545 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169509634 |
| s2499-118 | 118 | 0 | 0.016448914161 | 0.012584222072 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158362645 |
| s250-118 | 118 | 0 | 0.016448914161 | 0.013977903206 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000195381778 |
| s2509-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s2515-118 | 118 | 0 | 0.016448914161 | 0.015092579314 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000227785950 |
| s2516-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s2522-118 | 118 | 0 | 0.016448914161 | 0.012822011099 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000164403969 |
| s2524-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s2538-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s254-118 | 118 | 0 | 0.016448914161 | 0.013891381114 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000192970469 |
| s255-118 | 118 | 0 | 0.016448914161 | 0.012584222072 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158362645 |
| s2573-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s2575-118 | 118 | 0 | 0.016448914161 | 0.013798523233 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000190399243 |
| s2576-118 | 118 | 0 | 0.016448914161 | 0.013188975810 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000173949083 |
| s2588-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s2590-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s2594-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s2607-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s2614-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s2621-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s2629-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s2630-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s2650-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s2654-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s266-118 | 118 | 0 | 0.016448914161 | 0.013019586545 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169509634 |
| s2660-118 | 118 | 0 | 0.016448914161 | 0.013188975810 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000173949083 |
| s2662-118 | 118 | 0 | 0.016448914161 | 0.013019586545 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169509634 |
| s2683-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s2692-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s2699-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s2705-118 | 118 | 0 | 0.016448914161 | 0.013019586545 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169509634 |
| s2710-118 | 118 | 0 | 0.016448914161 | 0.013019586545 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169509634 |
| s2728-118 | 118 | 0 | 0.016448914161 | 0.013891381114 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000192970469 |
| s273-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s2735-118 | 118 | 0 | 0.016448914161 | 0.014058930763 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000197653534 |
| s2739-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s2740-118 | 118 | 0 | 0.016448914161 | 0.012822011099 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000164403969 |
| s2760-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s2761-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s2772-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s2776-118 | 118 | 0 | 0.016448914161 | 0.014673437079 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000215309756 |
| s2789-118 | 118 | 0 | 0.016448914161 | 0.013337463730 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000177887939 |
| s2791-118 | 118 | 0 | 0.016448914161 | 0.013337463730 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000177887939 |
| s2796-118 | 118 | 0 | 0.016448914161 | 0.031223283904 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000974893458 |
| s28-118 | 118 | 0 | 0.016448914161 | 0.012822011099 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000164403969 |
| s2803-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s2810-118 | 118 | 0 | 0.016448914161 | 0.012584222072 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158362645 |
| s2812-118 | 118 | 0 | 0.016448914161 | 0.013469807445 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000181435713 |
| s2818-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s2831-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s2848-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s2855-118 | 118 | 0 | 0.016448914161 | 0.015153108607 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000229616700 |
| s2857-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s2864-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s2868-118 | 118 | 0 | 0.016448914161 | 0.031510205443 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000992893047 |
| s287-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s2871-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s2877-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s2879-118 | 118 | 0 | 0.016448914161 | 0.013019586545 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169509634 |
| s2894-118 | 118 | 0 | 0.016448914161 | 0.014135146027 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000199802353 |
| s290-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s2916-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s2938-118 | 118 | 0 | 0.016448914161 | 0.013589289982 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000184668802 |
| s2942-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s296-118 | 118 | 0 | 0.016448914161 | 0.012584222072 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158362645 |
| s2963-118 | 118 | 0 | 0.016448914161 | 0.013589289982 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000184668802 |
| s2964-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s2965-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s2999-118 | 118 | 0 | 0.016448914161 | 0.013019586545 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169509634 |
| s3011-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s3023-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s3028-118 | 118 | 0 | 0.016448914161 | 0.014460777427 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000209114084 |
| s3052-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s3054-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s3077-118 | 118 | 0 | 0.016448914161 | 0.013188975810 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000173949083 |
| s308-118 | 118 | 0 | 0.044055747086 | 0.067984576640 | 0.020294849703 | 0.058283987399 | 0.001940908851 | 0.004621902661 |
| s3092-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s3094-118 | 118 | 0 | 0.016448914161 | 0.015162927798 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000229914379 |
| s3107-118 | 118 | 0 | 0.016448914161 | 0.013469807445 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000181435713 |
| s3114-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s3123-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s3134-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s3159-118 | 118 | 0 | 0.016448914161 | 0.013188975810 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000173949083 |
| s3167-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s3169-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s3182-118 | 118 | 0 | 0.016448914161 | 0.012584222072 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158362645 |
| s3190-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s3194-118 | 118 | 0 | 0.016448914161 | 0.013469807445 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000181435713 |
| s3195-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s3213-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s3216-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s3219-118 | 118 | 0 | 0.016448914161 | 0.012584222072 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158362645 |
| s3224-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s3230-118 | 118 | 0 | 0.016448914161 | 0.024160730080 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000583740878 |
| s3238-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s3239-118 | 118 | 0 | 0.016448914161 | 0.014275290390 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000203783916 |
| s3251-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s3252-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s3260-118 | 118 | 0 | 0.016448914161 | 0.011201533735 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000125474358 |
| s3262-118 | 118 | 0 | 0.016448914161 | 0.015728414294 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000247383016 |
| s3270-118 | 118 | 0 | 0.016448914161 | 0.012584222072 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158362645 |
| s3279-118 | 118 | 0 | 0.016448914161 | 0.012822011099 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000164403969 |
| s328-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s33-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s3319-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s3321-118 | 118 | 0 | 0.016448914161 | 0.013188975810 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000173949083 |
| s3322-118 | 118 | 0 | 0.016448914161 | 0.012822011099 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000164403969 |
| s3328-118 | 118 | 0 | 0.016448914161 | 0.013469807445 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000181435713 |
| s333-118 | 118 | 0 | 0.016448914161 | 0.014460777427 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000209114084 |
| s3333-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s3347-118 | 118 | 0 | 0.016448914161 | 0.013188975810 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000173949083 |
| s335-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s3356-118 | 118 | 0 | 0.016448914161 | 0.014571354486 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000212324372 |
| s3365-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s3367-118 | 118 | 0 | 0.016448914161 | 0.014340080096 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000205637897 |
| s3400-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s3407-118 | 118 | 0 | 0.016448914161 | 0.012584222072 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158362645 |
| s3408-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s3410-118 | 118 | 0 | 0.016448914161 | 0.013798523233 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000190399243 |
| s3415-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s3419-118 | 118 | 1 | 0.112687626852 | 0.148029036731 | 0.020294849703 | 0.202248763446 | 0.787323247542 | 0.725854522254 |
| s3435-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s3442-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s3445-118 | 118 | 0 | 0.016448914161 | 0.013469807445 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000181435713 |
| s3455-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s3460-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s3470-118 | 118 | 0 | 0.016448914161 | 0.013589289982 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000184668802 |
| s3474-118 | 118 | 0 | 0.016448914161 | 0.034672477729 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.001202180712 |
| s3476-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s3513-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s3524-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s3527-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s3535-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s3537-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s3540-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s3541-118 | 118 | 0 | 0.016448914161 | 0.012584222072 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158362645 |
| s3557-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s3559-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s3563-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s3567-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s3576-118 | 118 | 0 | 0.016448914161 | 0.013977903206 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000195381778 |
| s3593-118 | 118 | 0 | 0.016448914161 | 0.033054837962 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.001092622313 |
| s3595-118 | 118 | 0 | 0.016448914161 | 0.013337463730 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000177887939 |
| s3611-118 | 118 | 0 | 0.016448914161 | 0.013337463730 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000177887939 |
| s3612-118 | 118 | 0 | 0.016448914161 | 0.015523505594 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000240979226 |
| s3622-118 | 118 | 0 | 0.016448914161 | 0.013698275182 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000187642743 |
| s3636-118 | 118 | 0 | 0.016448914161 | 0.012822011099 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000164403969 |
| s3650-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s3652-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s3657-118 | 118 | 0 | 0.016448914161 | 0.015018440667 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000225553560 |
| s3658-118 | 118 | 0 | 0.016448914161 | 0.013188975810 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000173949083 |
| s3664-118 | 118 | 0 | 0.016448914161 | 0.013621624429 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000185548652 |
| s3668-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s3672-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s3684-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s3687-118 | 118 | 0 | 0.112687626852 | 0.105391865523 | 0.020294849703 | 0.202248763446 | 0.012698501245 | 0.011107445318 |
| s3698-118 | 118 | 0 | 0.016448914161 | 0.019321667575 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000373326838 |
| s3705-118 | 118 | 0 | 0.016448914161 | 0.013337463730 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000177887939 |
| s3706-118 | 118 | 1 | 0.259242165451 | 0.350477625751 | 0.020294849703 | 0.183579041419 | 0.548722169446 | 0.421879314650 |
| s3712-118 | 118 | 0 | 0.016448914161 | 0.014207110147 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000201841979 |
| s3715-118 | 118 | 0 | 0.016448914161 | 0.013188975810 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000173949083 |
| s372-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s3730-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s3733-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s3734-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s3741-118 | 118 | 0 | 0.016448914161 | 0.013188975810 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000173949083 |
| s375-118 | 118 | 0 | 0.016448914161 | 0.013337463730 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000177887939 |
| s3755-118 | 118 | 0 | 0.016448914161 | 0.013698275182 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000187642743 |
| s3770-118 | 118 | 0 | 0.016448914161 | 0.014058930763 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000197653534 |
| s3778-118 | 118 | 0 | 0.016448914161 | 0.012822011099 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000164403969 |
| s3780-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s3784-118 | 118 | 0 | 0.016448914161 | 0.012822011099 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000164403969 |
| s3808-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s3809-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s3819-118 | 118 | 0 | 0.016448914161 | 0.024866170961 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000618326458 |
| s3820-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s3823-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s3829-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s3842-118 | 118 | 0 | 0.016448914161 | 0.012822011099 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000164403969 |
| s3847-118 | 118 | 0 | 0.016448914161 | 0.013337463730 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000177887939 |
| s3852-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s3864-118 | 118 | 0 | 0.016448914161 | 0.012584222072 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158362645 |
| s3883-118 | 118 | 0 | 0.016448914161 | 0.013589289982 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000184668802 |
| s3902-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s3917-118 | 118 | 0 | 0.016448914161 | 0.013589289982 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000184668802 |
| s3930-118 | 118 | 0 | 0.016448914161 | 0.013188975810 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000173949083 |
| s3938-118 | 118 | 1 | 0.112687626852 | 0.155185233099 | 0.020294849703 | 0.202248763446 | 0.787323247542 | 0.713711990374 |
| s3962-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s3966-118 | 118 | 0 | 0.016448914161 | 0.013019586545 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169509634 |
| s3983-118 | 118 | 0 | 0.016448914161 | 0.013698275182 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000187642743 |
| s3995-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s4018-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s4047-118 | 118 | 0 | 0.016448914161 | 0.014275290390 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000203783916 |
| s4049-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s4055-118 | 118 | 0 | 0.016448914161 | 0.013555495145 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000183751449 |
| s4057-118 | 118 | 0 | 0.016448914161 | 0.013188975810 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000173949083 |
| s406-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s4060-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s4070-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s4076-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s4089-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s4090-118 | 118 | 0 | 0.016448914161 | 0.012584222072 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158362645 |
| s4091-118 | 118 | 0 | 0.016448914161 | 0.015196802936 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000230942819 |
| s4103-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s4111-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s4117-118 | 118 | 0 | 0.016448914161 | 0.014460777427 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000209114084 |
| s4120-118 | 118 | 0 | 0.016448914161 | 0.014721697605 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000216728380 |
| s4134-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s4143-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s4159-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s4177-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s4182-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s4186-118 | 118 | 0 | 0.016448914161 | 0.012822011099 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000164403969 |
| s419-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s4194-118 | 118 | 0 | 0.016448914161 | 0.013188975810 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000173949083 |
| s4198-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s4206-118 | 118 | 0 | 0.016448914161 | 0.013337463730 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000177887939 |
| s4210-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s4226-118 | 118 | 0 | 0.016448914161 | 0.014275290390 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000203783916 |
| s423-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s4235-118 | 118 | 0 | 0.112687626852 | 0.134641375145 | 0.020294849703 | 0.202248763446 | 0.012698501245 | 0.018128299901 |
| s4238-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s4260-118 | 118 | 0 | 0.016448914161 | 0.013698275182 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000187642743 |
| s4264-118 | 118 | 0 | 0.016448914161 | 0.012584222072 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158362645 |
| s4269-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s4270-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s4278-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s4279-118 | 118 | 0 | 0.016448914161 | 0.013337463730 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000177887939 |
| s428-118 | 118 | 0 | 0.016448914161 | 0.014207110147 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000201841979 |
| s4288-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s4299-118 | 118 | 0 | 0.016448914161 | 0.013698275182 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000187642743 |
| s4310-118 | 118 | 0 | 0.016448914161 | 0.015048039530 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000226443494 |
| s4314-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s4318-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s4375-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s4377-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s4383-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s4384-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s4387-118 | 118 | 0 | 0.016448914161 | 0.013188975810 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000173949083 |
| s4388-118 | 118 | 0 | 0.016448914161 | 0.013891381114 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000192970469 |
| s4391-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s4397-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s4404-118 | 118 | 0 | 0.044055747086 | 0.062717034594 | 0.020294849703 | 0.058283987399 | 0.001940908851 | 0.003933426428 |
| s4408-118 | 118 | 0 | 0.016448914161 | 0.012584222072 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158362645 |
| s4412-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s4416-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s4432-118 | 118 | 0 | 0.016448914161 | 0.011765606484 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000138429496 |
| s4442-118 | 118 | 0 | 0.016448914161 | 0.024949756742 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000622490362 |
| s4454-118 | 118 | 0 | 0.044055747086 | 0.084212390280 | 0.020294849703 | 0.058283987399 | 0.001940908851 | 0.007091726677 |
| s4458-118 | 118 | 0 | 0.016448914161 | 0.024418560192 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000596266082 |
| s4470-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s4484-118 | 118 | 0 | 0.016448914161 | 0.013891381114 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000192970469 |
| s4491-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s4498-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s45-118 | 118 | 0 | 0.016448914161 | 0.012584222072 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158362645 |
| s4509-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s4519-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s4531-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s4532-118 | 118 | 0 | 0.016448914161 | 0.015788696883 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000249282949 |
| s4553-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s4555-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s460-118 | 118 | 0 | 0.112687626852 | 0.164674409177 | 0.020294849703 | 0.202248763446 | 0.012698501245 | 0.027117661038 |
| s4612-118 | 118 | 0 | 0.016448914161 | 0.012584222072 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158362645 |
| s47-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s470-118 | 118 | 0 | 0.016448914161 | 0.014058930763 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000197653534 |
| s474-118 | 118 | 1 | 0.044055747086 | 0.060006175473 | 0.020294849703 | 0.058283987399 | 0.913829414680 | 0.883588390149 |
| s491-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s498-118 | 118 | 0 | 0.016448914161 | 0.019847503215 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000393923384 |
| s499-118 | 118 | 0 | 0.016448914161 | 0.014135146027 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000199802353 |
| s501-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s516-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s517-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s52-118 | 118 | 0 | 0.016448914161 | 0.013337463730 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000177887939 |
| s521-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s525-118 | 118 | 0 | 0.016448914161 | 0.012584222072 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158362645 |
| s530-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s559-118 | 118 | 0 | 0.016448914161 | 0.014234959755 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000202634079 |
| s565-118 | 118 | 0 | 0.016448914161 | 0.013019586545 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169509634 |
| s571-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s581-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s586-118 | 118 | 0 | 0.016448914161 | 0.013188975810 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000173949083 |
| s602-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s606-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s609-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s623-118 | 118 | 0 | 0.044055747086 | 0.065255422341 | 0.020294849703 | 0.058283987399 | 0.001940908851 | 0.004258270145 |
| s629-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s634-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s641-118 | 118 | 0 | 0.016448914161 | 0.013337463730 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000177887939 |
| s646-118 | 118 | 0 | 0.016448914161 | 0.013337463730 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000177887939 |
| s651-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s670-118 | 118 | 1 | 0.044055747086 | 0.041358773710 | 0.020294849703 | 0.058283987399 | 0.913829414680 | 0.918993000743 |
| s671-118 | 118 | 0 | 0.016448914161 | 0.013019586545 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169509634 |
| s677-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s696-118 | 118 | 0 | 0.016448914161 | 0.013019586545 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000169509634 |
| s698-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s713-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s719-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s728-118 | 118 | 0 | 0.044055747086 | 0.084186667523 | 0.020294849703 | 0.058283987399 | 0.001940908851 | 0.007087394989 |
| s741-118 | 118 | 0 | 0.016448914161 | 0.013977903206 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000195381778 |
| s755-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s76-118 | 118 | 0 | 0.016448914161 | 0.013977903206 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000195381778 |
| s767-118 | 118 | 0 | 0.016448914161 | 0.013798523233 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000190399243 |
| s770-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s780-118 | 118 | 0 | 0.044055747086 | 0.042782192398 | 0.020294849703 | 0.058283987399 | 0.001940908851 | 0.001830315986 |
| s806-118 | 118 | 0 | 0.016448914161 | 0.013589289982 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000184668802 |
| s809-118 | 118 | 0 | 0.016448914161 | 0.012822011099 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000164403969 |
| s813-118 | 118 | 0 | 0.016448914161 | 0.013188975810 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000173949083 |
| s827-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s834-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s841-118 | 118 | 0 | 0.044055747086 | 0.038910093975 | 0.020294849703 | 0.058283987399 | 0.001940908851 | 0.001513995413 |
| s843-118 | 118 | 0 | 0.044055747086 | 0.059342779396 | 0.020294849703 | 0.058283987399 | 0.001940908851 | 0.003521565466 |
| s855-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s862-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s868-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s875-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s885-118 | 118 | 0 | 0.044055747086 | 0.086417477665 | 0.020294849703 | 0.058283987399 | 0.001940908851 | 0.007467980446 |
| s888-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s891-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s896-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s914-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s927-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s94-118 | 118 | 0 | 0.016448914161 | 0.012584222072 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158362645 |
| s945-118 | 118 | 0 | 0.044055747086 | 0.050331305055 | 0.020294849703 | 0.058283987399 | 0.001940908851 | 0.002533240269 |
| s952-118 | 118 | 0 | 0.016448914161 | 0.010231169163 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000104676822 |
| s955-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s970-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s972-118 | 118 | 0 | 0.016448914161 | 0.011873008309 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000140968326 |
| s982-118 | 118 | 0 | 0.016448914161 | 0.012284073693 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000150898466 |
| s987-118 | 118 | 0 | 0.016448914161 | 0.012584222072 | 0.020294849703 | 0.010486655910 | 0.000270566777 | 0.000158362645 |

## All excluded candidate label cases

| Bill | Role | Reason |
| --- | --- | --- |
| hr1010-118 | 118 | No postCongress update assertion |
| hr1017-118 | 118 | No postCongress update assertion |
| hr1022-118 | 118 | No postCongress update assertion |
| hr1052-118 | 118 | No postCongress update assertion |
| hr1055-118 | 118 | No postCongress update assertion |
| hr1057-118 | 118 | No postCongress update assertion |
| hr1071-113 | train | already_enacted_or_cutoff_date_ambiguous |
| hr1138-114 | train | already_enacted_or_cutoff_date_ambiguous |
| hr1138-118 | 118 | No postCongress update assertion |
| hr1142-118 | 118 | No postCongress update assertion |
| hr1171-113 | train | already_enacted_or_cutoff_date_ambiguous |
| hr1175-118 | 118 | No postCongress update assertion |
| hr1201-118 | 118 | No postCongress update assertion |
| hr1203-118 | 118 | No postCongress update assertion |
| hr1223-118 | 118 | No postCongress update assertion |
| hr1326-118 | 118 | No postCongress update assertion |
| hr1347-118 | 118 | No postCongress update assertion |
| hr1356-118 | 118 | No postCongress update assertion |
| hr1357-118 | 118 | No postCongress update assertion |
| hr136-118 | 118 | No postCongress update assertion |
| hr138-118 | 118 | No postCongress update assertion |
| hr1383-118 | 118 | No postCongress update assertion |
| hr1412-113 | train | already_enacted_or_cutoff_date_ambiguous |
| hr1433-118 | 118 | No postCongress update assertion |
| hr1448-117 | 117 | already_enacted_or_cutoff_date_ambiguous |
| hr1454-118 | 118 | No postCongress update assertion |
| hr147-118 | 118 | No postCongress update assertion |
| hr1477-118 | 118 | No postCongress update assertion |
| hr1478-118 | 118 | No postCongress update assertion |
| hr1492-116 | train | outside_horizon_or_end_date_ambiguous |
| hr1512-118 | 118 | No postCongress update assertion |
| hr1519-118 | 118 | No postCongress update assertion |
| hr1542-118 | 118 | No postCongress update assertion |
| hr1597-118 | 118 | No postCongress update assertion |
| hr1604-118 | 118 | No postCongress update assertion |
| hr1621-118 | 118 | No postCongress update assertion |
| hr1628-118 | 118 | No postCongress update assertion |
| hr1660-115 | train | outside_horizon_or_end_date_ambiguous |
| hr1694-118 | 118 | No postCongress update assertion |
| hr1779-118 | 118 | No postCongress update assertion |
| hr1828-118 | 118 | No postCongress update assertion |
| hr183-118 | 118 | No postCongress update assertion |
| hr1832-118 | 118 | No postCongress update assertion |
| hr184-118 | 118 | No postCongress update assertion |
| hr1853-118 | 118 | No postCongress update assertion |
| hr186-118 | 118 | No postCongress update assertion |
| hr1861-118 | 118 | No postCongress update assertion |
| hr1863-118 | 118 | No postCongress update assertion |
| hr1870-118 | 118 | No postCongress update assertion |
| hr1894-118 | 118 | No postCongress update assertion |
| hr19-118 | 118 | No postCongress update assertion |
| hr1920-118 | 118 | No postCongress update assertion |
| hr1929-118 | 118 | No postCongress update assertion |
| hr1955-118 | 118 | No postCongress update assertion |
| hr1960-118 | 118 | No postCongress update assertion |
| hr1963-118 | 118 | No postCongress update assertion |
| hr1992-118 | 118 | No postCongress update assertion |
| hr2004-118 | 118 | No postCongress update assertion |
| hr2007-118 | 118 | No postCongress update assertion |
| hr2030-116 | train | already_enacted_or_cutoff_date_ambiguous |
| hr2047-118 | 118 | No postCongress update assertion |
| hr2056-118 | 118 | No postCongress update assertion |
| hr2109-118 | 118 | No postCongress update assertion |
| hr2154-118 | 118 | No postCongress update assertion |
| hr2167-113 | train | already_enacted_or_cutoff_date_ambiguous |
| hr2190-118 | 118 | No postCongress update assertion |
| hr2196-118 | 118 | No postCongress update assertion |
| hr2222-118 | 118 | No postCongress update assertion |
| hr2244-118 | 118 | No postCongress update assertion |
| hr2252-114 | train | already_enacted_or_cutoff_date_ambiguous |
| hr2252-118 | 118 | No postCongress update assertion |
| hr2258-118 | 118 | No postCongress update assertion |
| hr2310-118 | 118 | No postCongress update assertion |
| hr2317-118 | 118 | No postCongress update assertion |
| hr2336-116 | train | already_enacted_or_cutoff_date_ambiguous |
| hr2336-118 | 118 | No postCongress update assertion |
| hr2347-118 | 118 | No postCongress update assertion |
| hr2350-118 | 118 | No postCongress update assertion |
| hr2351-118 | 118 | No postCongress update assertion |
| hr2357-118 | 118 | No postCongress update assertion |
| hr2359-118 | 118 | No postCongress update assertion |
| hr2369-118 | 118 | No postCongress update assertion |
| hr242-118 | 118 | No postCongress update assertion |
| hr2447-118 | 118 | No postCongress update assertion |
| hr2462-118 | 118 | No postCongress update assertion |
| hr2474-118 | 118 | No postCongress update assertion |
| hr2488-118 | 118 | No postCongress update assertion |
| hr2510-118 | 118 | No postCongress update assertion |
| hr2544-118 | 118 | already_enacted_or_cutoff_date_ambiguous |
| hr2555-118 | 118 | No postCongress update assertion |
| hr2573-118 | 118 | No postCongress update assertion |
| hr2581-118 | 118 | No postCongress update assertion |
| hr2586-118 | 118 | No postCongress update assertion |
| hr2587-118 | 118 | No postCongress update assertion |
| hr2619-118 | 118 | No postCongress update assertion |
| hr2635-118 | 118 | No postCongress update assertion |
| hr2643-118 | 118 | No postCongress update assertion |
| hr2644-118 | 118 | No postCongress update assertion |
| hr2648-118 | 118 | No postCongress update assertion |
| hr267-115 | train | Uncorroborated latest-action public-law assertion |
| hr267-118 | 118 | No postCongress update assertion |
| hr2726-118 | 118 | No postCongress update assertion |
| hr2737-118 | 118 | No postCongress update assertion |
| hr274-115 | train | Uncorroborated latest-action public-law assertion |
| hr2745-118 | 118 | No postCongress update assertion |
| hr2747-113 | train | already_enacted_or_cutoff_date_ambiguous |
| hr2779-118 | 118 | No postCongress update assertion |
| hr2807-118 | 118 | No postCongress update assertion |
| hr2810-118 | 118 | No postCongress update assertion |
| hr2825-118 | 118 | No postCongress update assertion |
| hr2859-118 | 118 | No postCongress update assertion |
| hr2862-118 | 118 | No postCongress update assertion |
| hr2922-113 | train | already_enacted_or_cutoff_date_ambiguous |
| hr2927-118 | 118 | No postCongress update assertion |
| hr296-118 | 118 | No postCongress update assertion |
| hr299-116 | train | already_enacted_or_cutoff_date_ambiguous |
| hr2994-118 | 118 | No postCongress update assertion |
| hr3040-118 | 118 | No postCongress update assertion |
| hr3053-118 | 118 | No postCongress update assertion |
| hr3054-118 | 118 | No postCongress update assertion |
| hr3059-114 | train | already_enacted_or_cutoff_date_ambiguous |
| hr3102-118 | 118 | No postCongress update assertion |
| hr3117-118 | 118 | No postCongress update assertion |
| hr3140-118 | 118 | No postCongress update assertion |
| hr317-118 | 118 | No postCongress update assertion |
| hr3185-118 | 118 | No postCongress update assertion |
| hr3186-118 | 118 | No postCongress update assertion |
| hr3190-118 | 118 | No postCongress update assertion |
| hr3201-118 | 118 | No postCongress update assertion |
| hr3219-118 | 118 | No postCongress update assertion |
| hr3243-118 | 118 | No postCongress update assertion |
| hr33-114 | train | already_enacted_or_cutoff_date_ambiguous |
| hr33-118 | 118 | No postCongress update assertion |
| hr3302-113 | train | already_enacted_or_cutoff_date_ambiguous |
| hr3340-118 | 118 | No postCongress update assertion |
| hr3350-118 | 118 | No postCongress update assertion |
| hr3363-118 | 118 | No postCongress update assertion |
| hr3376-118 | 118 | No postCongress update assertion |
| hr3394-118 | 118 | No postCongress update assertion |
| hr3460-115 | train | outside_horizon_or_end_date_ambiguous |
| hr3487-113 | train | already_enacted_or_cutoff_date_ambiguous |
| hr3514-118 | 118 | No postCongress update assertion |
| hr3535-118 | 118 | No postCongress update assertion |
| hr3614-114 | train | already_enacted_or_cutoff_date_ambiguous |
| hr3626-118 | 118 | No postCongress update assertion |
| hr3660-117 | 117 | No postCongress update assertion |
| hr3663-117 | 117 | No postCongress update assertion |
| hr3666-118 | 118 | No postCongress update assertion |
| hr3672-118 | 118 | already_enacted_or_cutoff_date_ambiguous |
| hr3673-117 | 117 | No postCongress update assertion |
| hr3676-118 | 118 | No postCongress update assertion |
| hr3681-118 | 118 | No postCongress update assertion |
| hr3688-118 | 118 | No postCongress update assertion |
| hr3699-117 | 117 | No postCongress update assertion |
| hr3704-117 | 117 | No postCongress update assertion |
| hr3707-117 | 117 | No postCongress update assertion |
| hr3731-118 | 118 | No postCongress update assertion |
| hr3732-117 | 117 | No postCongress update assertion |
| hr3744-118 | 118 | No postCongress update assertion |
| hr3746-117 | 117 | No postCongress update assertion |
| hr3749-118 | 118 | No postCongress update assertion |
| hr3762-117 | 117 | No postCongress update assertion |
| hr3775-118 | 118 | No postCongress update assertion |
| hr3791-117 | 117 | No postCongress update assertion |
| hr3798-117 | 117 | No postCongress update assertion |
| hr3799-117 | 117 | No postCongress update assertion |
| hr3819-117 | 117 | No postCongress update assertion |
| hr3819-118 | 118 | No postCongress update assertion |
| hr3823-118 | 118 | No postCongress update assertion |
| hr3824-118 | 118 | No postCongress update assertion |
| hr3846-117 | 117 | No postCongress update assertion |
| hr3852-117 | 117 | No postCongress update assertion |
| hr3854-117 | 117 | No postCongress update assertion |
| hr3859-117 | 117 | No postCongress update assertion |
| hr3859-118 | 118 | No postCongress update assertion |
| hr3893-115 | train | already_enacted_or_cutoff_date_ambiguous |
| hr3894-118 | 118 | No postCongress update assertion |
| hr3902-117 | 117 | No postCongress update assertion |
| hr3904-118 | 118 | No postCongress update assertion |
| hr3907-117 | 117 | No postCongress update assertion |
| hr3908-118 | 118 | No postCongress update assertion |
| hr3909-118 | 118 | No postCongress update assertion |
| hr3921-118 | 118 | No postCongress update assertion |
| hr3928-117 | 117 | No postCongress update assertion |
| hr3934-118 | 118 | No postCongress update assertion |
| hr3939-117 | 117 | No postCongress update assertion |
| hr3947-117 | 117 | No postCongress update assertion |
| hr3949-115 | train | Uncorroborated latest-action public-law assertion |
| hr3951-117 | 117 | No postCongress update assertion |
| hr3957-117 | 117 | No postCongress update assertion |
| hr3961-118 | 118 | No postCongress update assertion |
| hr3964-118 | 118 | No postCongress update assertion |
| hr3969-117 | 117 | No postCongress update assertion |
| hr3970-117 | 117 | No postCongress update assertion |
| hr3973-117 | 117 | No postCongress update assertion |
| hr3977-117 | 117 | No postCongress update assertion |
| hr3979-118 | 118 | No postCongress update assertion |
| hr398-118 | 118 | No postCongress update assertion |
| hr3994-118 | 118 | No postCongress update assertion |
| hr3995-117 | 117 | No postCongress update assertion |
| hr3998-117 | 117 | No postCongress update assertion |
| hr40-118 | 118 | No postCongress update assertion |
| hr4011-117 | 117 | No postCongress update assertion |
| hr4012-117 | 117 | No postCongress update assertion |
| hr4015-118 | 118 | No postCongress update assertion |
| hr4028-113 | train | already_enacted_or_cutoff_date_ambiguous |
| hr4029-118 | 118 | No postCongress update assertion |
| hr4030-117 | 117 | No postCongress update assertion |
| hr4048-117 | 117 | No postCongress update assertion |
| hr4050-117 | 117 | No postCongress update assertion |
| hr4061-117 | 117 | No postCongress update assertion |
| hr4063-117 | 117 | No postCongress update assertion |
| hr4076-113 | train | already_enacted_or_cutoff_date_ambiguous |
| hr414-118 | 118 | No postCongress update assertion |
| hr4156-117 | 117 | No postCongress update assertion |
| hr4163-117 | 117 | No postCongress update assertion |
| hr4167-117 | 117 | No postCongress update assertion |
| hr4169-117 | 117 | No postCongress update assertion |
| hr4173-118 | 118 | No postCongress update assertion |
| hr4192-113 | train | already_enacted_or_cutoff_date_ambiguous |
| hr4196-117 | 117 | No postCongress update assertion |
| hr4199-118 | 118 | No postCongress update assertion |
| hr4211-117 | 117 | No postCongress update assertion |
| hr4214-117 | 117 | No postCongress update assertion |
| hr4216-117 | 117 | No postCongress update assertion |
| hr4217-118 | 118 | No postCongress update assertion |
| hr4225-117 | 117 | No postCongress update assertion |
| hr4247-117 | 117 | No postCongress update assertion |
| hr4273-118 | 118 | No postCongress update assertion |
| hr4278-117 | 117 | No postCongress update assertion |
| hr4284-118 | 118 | No postCongress update assertion |
| hr4285-115 | train | already_enacted_or_cutoff_date_ambiguous |
| hr4298-117 | 117 | No postCongress update assertion |
| hr4318-118 | 118 | No postCongress update assertion |
| hr4319-117 | 117 | No postCongress update assertion |
| hr4329-117 | 117 | No postCongress update assertion |
| hr4337-117 | 117 | No postCongress update assertion |
| hr4354-117 | 117 | No postCongress update assertion |
| hr4359-117 | 117 | No postCongress update assertion |
| hr4360-113 | train | already_enacted_or_cutoff_date_ambiguous |
| hr4362-117 | 117 | No postCongress update assertion |
| hr4367-117 | 117 | No postCongress update assertion |
| hr4393-118 | 118 | No postCongress update assertion |
| hr4394-117 | 117 | No postCongress update assertion |
| hr4395-117 | 117 | No postCongress update assertion |
| hr4396-117 | 117 | No postCongress update assertion |
| hr4413-117 | 117 | No postCongress update assertion |
| hr4415-117 | 117 | No postCongress update assertion |
| hr4425-114 | train | already_enacted_or_cutoff_date_ambiguous |
| hr4452-118 | 118 | No postCongress update assertion |
| hr4484-117 | 117 | No postCongress update assertion |
| hr4495-118 | 118 | No postCongress update assertion |
| hr4499-118 | 118 | No postCongress update assertion |
| hr4514-117 | 117 | No postCongress update assertion |
| hr4522-117 | 117 | No postCongress update assertion |
| hr4537-118 | 118 | No postCongress update assertion |
| hr4543-117 | 117 | No postCongress update assertion |
| hr4578-117 | 117 | No postCongress update assertion |
| hr4593-118 | 118 | No postCongress update assertion |
| hr4595-118 | 118 | No postCongress update assertion |
| hr4603-117 | 117 | No postCongress update assertion |
| hr4605-114 | train | already_enacted_or_cutoff_date_ambiguous |
| hr4610-118 | 118 | No postCongress update assertion |
| hr4613-117 | 117 | No postCongress update assertion |
| hr4617-117 | 117 | No postCongress update assertion |
| hr4624-117 | 117 | No postCongress update assertion |
| hr4643-117 | 117 | No postCongress update assertion |
| hr4655-117 | 117 | No postCongress update assertion |
| hr4661-115 | train | Uncorroborated latest-action public-law assertion |
| hr4661-117 | 117 | No postCongress update assertion |
| hr4666-117 | 117 | No postCongress update assertion |
| hr4667-117 | 117 | No postCongress update assertion |
| hr4680-118 | 118 | No postCongress update assertion |
| hr4689-115 | train | outside_horizon_or_end_date_ambiguous |
| hr4724-117 | 117 | No postCongress update assertion |
| hr4724-118 | 118 | No postCongress update assertion |
| hr4728-118 | 118 | No postCongress update assertion |
| hr4743-115 | train | already_enacted_or_cutoff_date_ambiguous |
| hr4751-113 | train | already_enacted_or_cutoff_date_ambiguous |
| hr4761-114 | train | already_enacted_or_cutoff_date_ambiguous |
| hr4775-118 | 118 | No postCongress update assertion |
| hr4782-117 | 117 | No postCongress update assertion |
| hr4789-117 | 117 | No postCongress update assertion |
| hr479-118 | 118 | No postCongress update assertion |
| hr480-118 | 118 | No postCongress update assertion |
| hr4809-117 | 117 | No postCongress update assertion |
| hr4810-117 | 117 | No postCongress update assertion |
| hr4835-118 | 118 | No postCongress update assertion |
| hr4842-117 | 117 | No postCongress update assertion |
| hr4844-117 | 117 | No postCongress update assertion |
| hr4857-118 | 118 | No postCongress update assertion |
| hr4871-118 | 118 | No postCongress update assertion |
| hr4883-117 | 117 | No postCongress update assertion |
| hr4896-117 | 117 | No postCongress update assertion |
| hr4904-117 | 117 | No postCongress update assertion |
| hr4906-117 | 117 | No postCongress update assertion |
| hr4923-118 | 118 | No postCongress update assertion |
| hr4936-118 | 118 | No postCongress update assertion |
| hr4941-118 | 118 | No postCongress update assertion |
| hr495-118 | 118 | No postCongress update assertion |
| hr4958-117 | 117 | No postCongress update assertion |
| hr4963-117 | 117 | No postCongress update assertion |
| hr4965-118 | 118 | No postCongress update assertion |
| hr4967-117 | 117 | No postCongress update assertion |
| hr4973-117 | 117 | No postCongress update assertion |
| hr4978-117 | 117 | No postCongress update assertion |
| hr4993-118 | 118 | No postCongress update assertion |
| hr5002-118 | 118 | No postCongress update assertion |
| hr5009-117 | 117 | No postCongress update assertion |
| hr5013-118 | 118 | No postCongress update assertion |
| hr5022-117 | 117 | No postCongress update assertion |
| hr5028-114 | train | already_enacted_or_cutoff_date_ambiguous |
| hr5036-118 | 118 | No postCongress update assertion |
| hr5057-117 | 117 | No postCongress update assertion |
| hr5061-117 | 117 | No postCongress update assertion |
| hr5075-117 | 117 | No postCongress update assertion |
| hr5080-117 | 117 | No postCongress update assertion |
| hr5081-117 | 117 | No postCongress update assertion |
| hr5089-117 | 117 | No postCongress update assertion |
| hr5090-118 | 118 | No postCongress update assertion |
| hr5105-117 | 117 | No postCongress update assertion |
| hr5106-117 | 117 | No postCongress update assertion |
| hr5108-118 | 118 | No postCongress update assertion |
| hr5113-117 | 117 | No postCongress update assertion |
| hr5117-117 | 117 | No postCongress update assertion |
| hr5120-117 | 117 | No postCongress update assertion |
| hr5125-118 | 118 | No postCongress update assertion |
| hr5137-117 | 117 | No postCongress update assertion |
| hr5138-117 | 117 | No postCongress update assertion |
| hr5147-118 | 118 | No postCongress update assertion |
| hr5152-117 | 117 | No postCongress update assertion |
| hr5160-117 | 117 | No postCongress update assertion |
| hr5166-118 | 118 | No postCongress update assertion |
| hr5168-117 | 117 | No postCongress update assertion |
| hr5178-117 | 117 | No postCongress update assertion |
| hr5186-117 | 117 | No postCongress update assertion |
| hr5192-117 | 117 | No postCongress update assertion |
| hr5207-118 | 118 | No postCongress update assertion |
| hr5212-117 | 117 | No postCongress update assertion |
| hr5215-117 | 117 | No postCongress update assertion |
| hr5236-118 | 118 | No postCongress update assertion |
| hr5263-117 | 117 | No postCongress update assertion |
| hr5296-117 | 117 | No postCongress update assertion |
| hr5308-118 | 118 | No postCongress update assertion |
| hr5318-117 | 117 | No postCongress update assertion |
| hr5318-118 | 118 | No postCongress update assertion |
| hr5319-117 | 117 | No postCongress update assertion |
| hr5334-117 | 117 | No postCongress update assertion |
| hr5341-117 | 117 | No postCongress update assertion |
| hr5356-117 | 117 | No postCongress update assertion |
| hr5357-117 | 117 | No postCongress update assertion |
| hr5358-118 | 118 | No postCongress update assertion |
| hr5360-118 | 118 | No postCongress update assertion |
| hr5374-118 | 118 | No postCongress update assertion |
| hr5382-117 | 117 | No postCongress update assertion |
| hr5384-117 | 117 | No postCongress update assertion |
| hr5386-117 | 117 | No postCongress update assertion |
| hr5389-117 | 117 | No postCongress update assertion |
| hr5396-117 | 117 | No postCongress update assertion |
| hr5397-117 | 117 | No postCongress update assertion |
| hr5406-117 | 117 | No postCongress update assertion |
| hr5414-117 | 117 | No postCongress update assertion |
| hr5417-118 | 118 | No postCongress update assertion |
| hr5421-117 | 117 | No postCongress update assertion |
| hr5423-118 | 118 | No postCongress update assertion |
| hr5443-118 | 118 | outside_horizon_or_end_date_ambiguous |
| hr5445-117 | 117 | No postCongress update assertion |
| hr5447-118 | 118 | No postCongress update assertion |
| hr5456-117 | 117 | No postCongress update assertion |
| hr546-118 | 118 | No postCongress update assertion |
| hr5471-118 | 118 | No postCongress update assertion |
| hr5483-118 | 118 | No postCongress update assertion |
| hr5488-117 | 117 | No postCongress update assertion |
| hr5491-117 | 117 | No postCongress update assertion |
| hr5501-118 | 118 | No postCongress update assertion |
| hr5507-117 | 117 | No postCongress update assertion |
| hr5508-117 | 117 | No postCongress update assertion |
| hr5546-117 | 117 | No postCongress update assertion |
| hr5568-117 | 117 | No postCongress update assertion |
| hr5570-117 | 117 | No postCongress update assertion |
| hr5573-117 | 117 | No postCongress update assertion |
| hr5579-117 | 117 | No postCongress update assertion |
| hr5582-117 | 117 | No postCongress update assertion |
| hr5584-118 | 118 | No postCongress update assertion |
| hr5592-118 | 118 | No postCongress update assertion |
| hr5625-117 | 117 | No postCongress update assertion |
| hr5627-117 | 117 | No postCongress update assertion |
| hr5632-117 | 117 | No postCongress update assertion |
| hr5635-117 | 117 | No postCongress update assertion |
| hr5637-117 | 117 | No postCongress update assertion |
| hr5648-118 | 118 | No postCongress update assertion |
| hr5652-118 | 118 | No postCongress update assertion |
| hr5661-118 | 118 | No postCongress update assertion |
| hr5686-117 | 117 | No postCongress update assertion |
| hr5699-117 | 117 | No postCongress update assertion |
| hr5709-118 | 118 | No postCongress update assertion |
| hr5714-117 | 117 | No postCongress update assertion |
| hr5717-117 | 117 | No postCongress update assertion |
| hr5731-117 | 117 | No postCongress update assertion |
| hr5732-117 | 117 | No postCongress update assertion |
| hr5734-117 | 117 | No postCongress update assertion |
| hr5745-117 | 117 | No postCongress update assertion |
| hr5747-117 | 117 | No postCongress update assertion |
| hr5765-118 | 118 | No postCongress update assertion |
| hr5772-115 | train | already_enacted_or_cutoff_date_ambiguous |
| hr5772-117 | 117 | No postCongress update assertion |
| hr5776-118 | 118 | No postCongress update assertion |
| hr5785-117 | 117 | No postCongress update assertion |
| hr5787-117 | 117 | No postCongress update assertion |
| hr5804-118 | 118 | No postCongress update assertion |
| hr5817-118 | 118 | No postCongress update assertion |
| hr5827-117 | 117 | No postCongress update assertion |
| hr5829-118 | 118 | No postCongress update assertion |
| hr5840-117 | 117 | No postCongress update assertion |
| hr5851-117 | 117 | No postCongress update assertion |
| hr5859-118 | 118 | No postCongress update assertion |
| hr5864-117 | 117 | No postCongress update assertion |
| hr5866-117 | 117 | No postCongress update assertion |
| hr588-113 | train | already_enacted_or_cutoff_date_ambiguous |
| hr5882-117 | 117 | No postCongress update assertion |
| hr5895-117 | 117 | No postCongress update assertion |
| hr5897-117 | 117 | No postCongress update assertion |
| hr5938-117 | 117 | No postCongress update assertion |
| hr5939-117 | 117 | No postCongress update assertion |
| hr5946-117 | 117 | No postCongress update assertion |
| hr5959-117 | 117 | No postCongress update assertion |
| hr5993-117 | 117 | No postCongress update assertion |
| hr6004-117 | 117 | No postCongress update assertion |
| hr6016-117 | 117 | No postCongress update assertion |
| hr6025-118 | 118 | No postCongress update assertion |
| hr6044-117 | 117 | No postCongress update assertion |
| hr6091-117 | 117 | No postCongress update assertion |
| hr6097-117 | 117 | No postCongress update assertion |
| hr6111-118 | 118 | No postCongress update assertion |
| hr6117-118 | 118 | No postCongress update assertion |
| hr612-118 | 118 | No postCongress update assertion |
| hr6122-117 | 117 | No postCongress update assertion |
| hr613-118 | 118 | No postCongress update assertion |
| hr6133-117 | 117 | No postCongress update assertion |
| hr6137-118 | 118 | No postCongress update assertion |
| hr6146-117 | 117 | No postCongress update assertion |
| hr6146-118 | 118 | No postCongress update assertion |
| hr6149-117 | 117 | No postCongress update assertion |
| hr6156-117 | 117 | No postCongress update assertion |
| hr6169-118 | 118 | No postCongress update assertion |
| hr617-118 | 118 | No postCongress update assertion |
| hr6172-118 | 118 | No postCongress update assertion |
| hr6189-117 | 117 | No postCongress update assertion |
| hr6192-116 | train | outside_horizon_or_end_date_ambiguous |
| hr6212-117 | 117 | No postCongress update assertion |
| hr6212-118 | 118 | No postCongress update assertion |
| hr6217-117 | 117 | No postCongress update assertion |
| hr6228-118 | 118 | No postCongress update assertion |
| hr624-115 | train | Uncorroborated latest-action public-law assertion |
| hr6253-117 | 117 | No postCongress update assertion |
| hr6255-117 | 117 | No postCongress update assertion |
| hr6261-117 | 117 | No postCongress update assertion |
| hr6266-117 | 117 | No postCongress update assertion |
| hr6266-118 | 118 | No postCongress update assertion |
| hr6276-117 | 117 | No postCongress update assertion |
| hr6281-117 | 117 | No postCongress update assertion |
| hr6310-117 | 117 | No postCongress update assertion |
| hr6330-117 | 117 | No postCongress update assertion |
| hr6339-117 | 117 | No postCongress update assertion |
| hr6347-118 | 118 | No postCongress update assertion |
| hr6349-117 | 117 | No postCongress update assertion |
| hr6354-117 | 117 | No postCongress update assertion |
| hr6379-117 | 117 | No postCongress update assertion |
| hr6389-117 | 117 | No postCongress update assertion |
| hr6390-118 | 118 | No postCongress update assertion |
| hr6391-118 | 118 | No postCongress update assertion |
| hr6415-118 | 118 | No postCongress update assertion |
| hr6425-117 | 117 | No postCongress update assertion |
| hr6428-117 | 117 | No postCongress update assertion |
| hr6428-118 | 118 | No postCongress update assertion |
| hr6431-118 | 118 | No postCongress update assertion |
| hr6457-117 | 117 | No postCongress update assertion |
| hr6478-118 | 118 | No postCongress update assertion |
| hr6479-118 | 118 | No postCongress update assertion |
| hr6488-118 | 118 | No postCongress update assertion |
| hr6494-117 | 117 | No postCongress update assertion |
| hr6507-117 | 117 | No postCongress update assertion |
| hr6516-117 | 117 | No postCongress update assertion |
| hr6530-117 | 117 | No postCongress update assertion |
| hr6535-117 | 117 | No postCongress update assertion |
| hr6540-117 | 117 | No postCongress update assertion |
| hr6546-118 | 118 | No postCongress update assertion |
| hr6551-118 | 118 | No postCongress update assertion |
| hr6590-118 | 118 | No postCongress update assertion |
| hr6593-117 | 117 | No postCongress update assertion |
| hr6624-118 | 118 | No postCongress update assertion |
| hr6627-117 | 117 | No postCongress update assertion |
| hr6634-117 | 117 | No postCongress update assertion |
| hr6648-117 | 117 | No postCongress update assertion |
| hr6663-117 | 117 | No postCongress update assertion |
| hr6668-117 | 117 | No postCongress update assertion |
| hr6681-117 | 117 | No postCongress update assertion |
| hr6685-118 | 118 | No postCongress update assertion |
| hr6688-117 | 117 | No postCongress update assertion |
| hr6699-117 | 117 | No postCongress update assertion |
| hr6708-117 | 117 | No postCongress update assertion |
| hr6715-117 | 117 | No postCongress update assertion |
| hr6739-117 | 117 | No postCongress update assertion |
| hr6742-118 | 118 | No postCongress update assertion |
| hr6757-117 | 117 | No postCongress update assertion |
| hr6772-117 | 117 | No postCongress update assertion |
| hr6798-117 | 117 | No postCongress update assertion |
| hr6807-117 | 117 | No postCongress update assertion |
| hr6808-117 | 117 | No postCongress update assertion |
| hr6817-117 | 117 | No postCongress update assertion |
| hr6832-117 | 117 | No postCongress update assertion |
| hr6847-117 | 117 | No postCongress update assertion |
| hr6853-117 | 117 | No postCongress update assertion |
| hr6879-117 | 117 | No postCongress update assertion |
| hr6893-117 | 117 | No postCongress update assertion |
| hr6897-117 | 117 | No postCongress update assertion |
| hr6906-117 | 117 | No postCongress update assertion |
| hr6921-117 | 117 | No postCongress update assertion |
| hr6928-117 | 117 | No postCongress update assertion |
| hr6931-117 | 117 | No postCongress update assertion |
| hr6932-118 | 118 | No postCongress update assertion |
| hr6941-118 | 118 | No postCongress update assertion |
| hr6955-117 | 117 | No postCongress update assertion |
| hr6956-118 | 118 | No postCongress update assertion |
| hr6968-118 | 118 | No postCongress update assertion |
| hr6985-117 | 117 | No postCongress update assertion |
| hr6986-117 | 117 | No postCongress update assertion |
| hr6999-118 | 118 | No postCongress update assertion |
| hr7013-117 | 117 | No postCongress update assertion |
| hr7028-118 | 118 | No postCongress update assertion |
| hr7035-118 | 118 | No postCongress update assertion |
| hr7036-117 | 117 | No postCongress update assertion |
| hr7041-117 | 117 | No postCongress update assertion |
| hr7042-118 | 118 | No postCongress update assertion |
| hr7043-117 | 117 | No postCongress update assertion |
| hr7049-118 | 118 | No postCongress update assertion |
| hr7054-117 | 117 | No postCongress update assertion |
| hr7068-117 | 117 | No postCongress update assertion |
| hr7076-118 | 118 | No postCongress update assertion |
| hr7084-118 | 118 | No postCongress update assertion |
| hr7087-117 | 117 | No postCongress update assertion |
| hr7090-117 | 117 | No postCongress update assertion |
| hr7102-117 | 117 | No postCongress update assertion |
| hr7104-117 | 117 | No postCongress update assertion |
| hr7107-118 | 118 | No postCongress update assertion |
| hr7110-118 | 118 | No postCongress update assertion |
| hr7111-117 | 117 | No postCongress update assertion |
| hr7133-118 | 118 | No postCongress update assertion |
| hr7148-117 | 117 | No postCongress update assertion |
| hr7156-117 | 117 | No postCongress update assertion |
| hr7171-117 | 117 | No postCongress update assertion |
| hr7178-117 | 117 | No postCongress update assertion |
| hr7178-118 | 118 | No postCongress update assertion |
| hr7190-118 | 118 | No postCongress update assertion |
| hr7206-118 | 118 | No postCongress update assertion |
| hr7220-117 | 117 | No postCongress update assertion |
| hr7223-118 | 118 | No postCongress update assertion |
| hr7242-118 | 118 | No postCongress update assertion |
| hr7243-117 | 117 | No postCongress update assertion |
| hr7253-117 | 117 | No postCongress update assertion |
| hr7264-118 | 118 | No postCongress update assertion |
| hr7270-117 | 117 | No postCongress update assertion |
| hr728-114 | train | already_enacted_or_cutoff_date_ambiguous |
| hr7287-118 | 118 | No postCongress update assertion |
| hr73-118 | 118 | No postCongress update assertion |
| hr7302-117 | 117 | No postCongress update assertion |
| hr7303-117 | 117 | No postCongress update assertion |
| hr7320-117 | 117 | No postCongress update assertion |
| hr7325-118 | 118 | No postCongress update assertion |
| hr7330-118 | 118 | No postCongress update assertion |
| hr7345-117 | 117 | No postCongress update assertion |
| hr7365-117 | 117 | No postCongress update assertion |
| hr7374-117 | 117 | No postCongress update assertion |
| hr7378-117 | 117 | No postCongress update assertion |
| hr7384-117 | 117 | No postCongress update assertion |
| hr7391-118 | 118 | No postCongress update assertion |
| hr7397-117 | 117 | No postCongress update assertion |
| hr74-118 | 118 | No postCongress update assertion |
| hr7401-117 | 117 | No postCongress update assertion |
| hr7402-118 | 118 | No postCongress update assertion |
| hr7407-117 | 117 | No postCongress update assertion |
| hr7415-118 | 118 | No postCongress update assertion |
| hr7418-117 | 117 | No postCongress update assertion |
| hr7420-118 | 118 | No postCongress update assertion |
| hr7440-117 | 117 | No postCongress update assertion |
| hr7442-118 | 118 | No postCongress update assertion |
| hr7473-118 | 118 | No postCongress update assertion |
| hr7484-118 | 118 | No postCongress update assertion |
| hr7508-117 | 117 | No postCongress update assertion |
| hr7515-118 | 118 | No postCongress update assertion |
| hr7517-118 | 118 | No postCongress update assertion |
| hr7522-118 | 118 | No postCongress update assertion |
| hr7534-117 | 117 | No postCongress update assertion |
| hr7538-118 | 118 | No postCongress update assertion |
| hr7539-117 | 117 | No postCongress update assertion |
| hr7540-118 | 118 | No postCongress update assertion |
| hr7548-117 | 117 | No postCongress update assertion |
| hr7549-117 | 117 | No postCongress update assertion |
| hr7554-118 | 118 | No postCongress update assertion |
| hr7562-118 | 118 | No postCongress update assertion |
| hr7607-118 | 118 | outside_horizon_or_end_date_ambiguous |
| hr7646-118 | 118 | No postCongress update assertion |
| hr7650-117 | 117 | No postCongress update assertion |
| hr7655-117 | 117 | No postCongress update assertion |
| hr7657-117 | 117 | No postCongress update assertion |
| hr7674-118 | 118 | No postCongress update assertion |
| hr7690-117 | 117 | No postCongress update assertion |
| hr7693-118 | 118 | No postCongress update assertion |
| hr7716-118 | 118 | No postCongress update assertion |
| hr7728-117 | 117 | No postCongress update assertion |
| hr7740-118 | 118 | No postCongress update assertion |
| hr7744-118 | 118 | No postCongress update assertion |
| hr7746-118 | 118 | No postCongress update assertion |
| hr7751-118 | 118 | No postCongress update assertion |
| hr7757-117 | 117 | No postCongress update assertion |
| hr7773-117 | 117 | No postCongress update assertion |
| hr7791-117 | 117 | already_enacted_or_cutoff_date_ambiguous |
| hr7805-117 | 117 | No postCongress update assertion |
| hr7819-117 | 117 | No postCongress update assertion |
| hr7827-118 | 118 | No postCongress update assertion |
| hr7836-118 | 118 | No postCongress update assertion |
| hr7839-118 | 118 | No postCongress update assertion |
| hr7847-118 | 118 | No postCongress update assertion |
| hr7848-118 | 118 | No postCongress update assertion |
| hr7851-118 | 118 | No postCongress update assertion |
| hr7852-118 | 118 | No postCongress update assertion |
| hr7870-118 | 118 | No postCongress update assertion |
| hr7874-118 | 118 | No postCongress update assertion |
| hr7875-117 | 117 | No postCongress update assertion |
| hr7880-117 | 117 | No postCongress update assertion |
| hr7883-117 | 117 | No postCongress update assertion |
| hr79-118 | 118 | No postCongress update assertion |
| hr7902-117 | 117 | No postCongress update assertion |
| hr7902-118 | 118 | No postCongress update assertion |
| hr7904-118 | 118 | No postCongress update assertion |
| hr7907-117 | 117 | No postCongress update assertion |
| hr7922-117 | 117 | No postCongress update assertion |
| hr7928-117 | 117 | No postCongress update assertion |
| hr7942-118 | 118 | No postCongress update assertion |
| hr7964-117 | 117 | No postCongress update assertion |
| hr7967-118 | 118 | No postCongress update assertion |
| hr7974-117 | 117 | No postCongress update assertion |
| hr7991-118 | 118 | No postCongress update assertion |
| hr8001-117 | 117 | No postCongress update assertion |
| hr8010-117 | 117 | No postCongress update assertion |
| hr8041-118 | 118 | No postCongress update assertion |
| hr8060-117 | 117 | No postCongress update assertion |
| hr8061-118 | 118 | No postCongress update assertion |
| hr8064-117 | 117 | No postCongress update assertion |
| hr8072-117 | 117 | No postCongress update assertion |
| hr8080-118 | 118 | No postCongress update assertion |
| hr8090-118 | 118 | No postCongress update assertion |
| hr8097-117 | 117 | No postCongress update assertion |
| hr8102-117 | 117 | No postCongress update assertion |
| hr8130-118 | 118 | No postCongress update assertion |
| hr8138-118 | 118 | No postCongress update assertion |
| hr8141-118 | 118 | No postCongress update assertion |
| hr8172-117 | 117 | No postCongress update assertion |
| hr8197-117 | 117 | No postCongress update assertion |
| hr8211-118 | 118 | No postCongress update assertion |
| hr8220-118 | 118 | No postCongress update assertion |
| hr8230-117 | 117 | No postCongress update assertion |
| hr8249-117 | 117 | No postCongress update assertion |
| hr8252-118 | 118 | No postCongress update assertion |
| hr8261-117 | 117 | No postCongress update assertion |
| hr8269-117 | 117 | No postCongress update assertion |
| hr8274-117 | 117 | No postCongress update assertion |
| hr8274-118 | 118 | No postCongress update assertion |
| hr8348-118 | 118 | No postCongress update assertion |
| hr8350-118 | 118 | No postCongress update assertion |
| hr8352-118 | 118 | No postCongress update assertion |
| hr8359-118 | 118 | No postCongress update assertion |
| hr8398-118 | 118 | No postCongress update assertion |
| hr8411-118 | 118 | No postCongress update assertion |
| hr8422-118 | 118 | No postCongress update assertion |
| hr843-118 | 118 | No postCongress update assertion |
| hr8435-118 | 118 | No postCongress update assertion |
| hr8447-118 | 118 | No postCongress update assertion |
| hr8459-118 | 118 | No postCongress update assertion |
| hr8463-118 | 118 | No postCongress update assertion |
| hr85-118 | 118 | No postCongress update assertion |
| hr8500-118 | 118 | No postCongress update assertion |
| hr8522-118 | 118 | No postCongress update assertion |
| hr8561-118 | 118 | No postCongress update assertion |
| hr8582-118 | 118 | No postCongress update assertion |
| hr863-115 | train | Uncorroborated latest-action public-law assertion |
| hr8630-118 | 118 | No postCongress update assertion |
| hr866-116 | train | already_enacted_or_cutoff_date_ambiguous |
| hr8670-118 | 118 | No postCongress update assertion |
| hr8672-118 | 118 | No postCongress update assertion |
| hr8678-118 | 118 | No postCongress update assertion |
| hr8684-118 | 118 | No postCongress update assertion |
| hr8703-118 | 118 | No postCongress update assertion |
| hr8726-118 | 118 | No postCongress update assertion |
| hr8738-118 | 118 | No postCongress update assertion |
| hr8749-118 | 118 | No postCongress update assertion |
| hr8775-118 | 118 | No postCongress update assertion |
| hr8778-118 | 118 | No postCongress update assertion |
| hr880-118 | 118 | No postCongress update assertion |
| hr8823-118 | 118 | No postCongress update assertion |
| hr8837-118 | 118 | No postCongress update assertion |
| hr8841-118 | 118 | outside_horizon_or_end_date_ambiguous |
| hr8861-118 | 118 | No postCongress update assertion |
| hr8869-118 | 118 | No postCongress update assertion |
| hr8873-118 | 118 | No postCongress update assertion |
| hr8876-118 | 118 | No postCongress update assertion |
| hr8885-118 | 118 | No postCongress update assertion |
| hr8917-118 | 118 | No postCongress update assertion |
| hr893-114 | train | already_enacted_or_cutoff_date_ambiguous |
| hr894-118 | 118 | No postCongress update assertion |
| hr904-118 | 118 | No postCongress update assertion |
| hr952-118 | 118 | No postCongress update assertion |
| hr959-118 | 118 | No postCongress update assertion |
| s1023-115 | train | outside_horizon_or_end_date_ambiguous |
| s1126-118 | 118 | No postCongress update assertion |
| s1436-116 | train | already_enacted_or_cutoff_date_ambiguous |
| s1471-113 | train | already_enacted_or_cutoff_date_ambiguous |
| s17-118 | 118 | No postCongress update assertion |
| s1749-116 | train | already_enacted_or_cutoff_date_ambiguous |
| s1966-117 | 117 | No postCongress update assertion |
| s1972-117 | 117 | No postCongress update assertion |
| s1977-117 | 117 | No postCongress update assertion |
| s2002-117 | 117 | No postCongress update assertion |
| s2005-117 | 117 | No postCongress update assertion |
| s2019-117 | 117 | No postCongress update assertion |
| s2031-117 | 117 | No postCongress update assertion |
| s2036-114 | train | already_enacted_or_cutoff_date_ambiguous |
| s2050-117 | 117 | No postCongress update assertion |
| s2052-118 | 118 | No postCongress update assertion |
| s2063-117 | 117 | No postCongress update assertion |
| s2064-117 | 117 | No postCongress update assertion |
| s2068-117 | 117 | No postCongress update assertion |
| s2070-117 | 117 | No postCongress update assertion |
| s2081-117 | 117 | No postCongress update assertion |
| s2084-117 | 117 | No postCongress update assertion |
| s2092-117 | 117 | No postCongress update assertion |
| s2109-114 | train | already_enacted_or_cutoff_date_ambiguous |
| s2128-117 | 117 | No postCongress update assertion |
| s2136-117 | 117 | No postCongress update assertion |
| s2140-117 | 117 | No postCongress update assertion |
| s2152-114 | train | already_enacted_or_cutoff_date_ambiguous |
| s2156-117 | 117 | No postCongress update assertion |
| s2190-117 | 117 | No postCongress update assertion |
| s2195-113 | train | already_enacted_or_cutoff_date_ambiguous |
| s2207-117 | 117 | No postCongress update assertion |
| s2221-117 | 117 | No postCongress update assertion |
| s2224-117 | 117 | No postCongress update assertion |
| s2234-117 | 117 | No postCongress update assertion |
| s2252-117 | 117 | No postCongress update assertion |
| s2272-117 | 117 | No postCongress update assertion |
| s2292-117 | 117 | No postCongress update assertion |
| s2333-117 | 117 | outside_horizon_or_end_date_ambiguous |
| s2343-117 | 117 | No postCongress update assertion |
| s2359-117 | 117 | No postCongress update assertion |
| s24-116 | train | already_enacted_or_cutoff_date_ambiguous |
| s2406-118 | 118 | No postCongress update assertion |
| s2408-117 | 117 | No postCongress update assertion |
| s2436-117 | 117 | No postCongress update assertion |
| s2437-117 | 117 | No postCongress update assertion |
| s2449-117 | 117 | No postCongress update assertion |
| s2466-117 | 117 | No postCongress update assertion |
| s2496-117 | 117 | No postCongress update assertion |
| s2498-117 | 117 | No postCongress update assertion |
| s2500-117 | 117 | No postCongress update assertion |
| s2503-117 | 117 | No postCongress update assertion |
| s2504-117 | 117 | No postCongress update assertion |
| s2536-117 | 117 | No postCongress update assertion |
| s2539-113 | train | already_enacted_or_cutoff_date_ambiguous |
| s2548-117 | 117 | No postCongress update assertion |
| s2553-117 | 117 | No postCongress update assertion |
| s2584-117 | 117 | No postCongress update assertion |
| s2585-117 | 117 | No postCongress update assertion |
| s2595-117 | 117 | No postCongress update assertion |
| s2596-117 | 117 | No postCongress update assertion |
| s2609-118 | 118 | No postCongress update assertion |
| s2627-117 | 117 | No postCongress update assertion |
| s2636-117 | 117 | No postCongress update assertion |
| s2655-117 | 117 | No postCongress update assertion |
| s2675-117 | 117 | No postCongress update assertion |
| s2680-117 | 117 | No postCongress update assertion |
| s2683-117 | 117 | No postCongress update assertion |
| s2684-117 | 117 | No postCongress update assertion |
| s2698-117 | 117 | No postCongress update assertion |
| s2732-117 | 117 | No postCongress update assertion |
| s2734-115 | train | already_enacted_or_cutoff_date_ambiguous |
| s2742-117 | 117 | No postCongress update assertion |
| s2748-118 | 118 | No postCongress update assertion |
| s2772-117 | 117 | No postCongress update assertion |
| s2774-117 | 117 | No postCongress update assertion |
| s2779-115 | train | already_enacted_or_cutoff_date_ambiguous |
| s2795-118 | 118 | already_enacted_or_cutoff_date_ambiguous |
| s2818-117 | 117 | No postCongress update assertion |
| s2830-117 | 117 | No postCongress update assertion |
| s2834-117 | 117 | outside_horizon_or_end_date_ambiguous |
| s2840-114 | train | already_enacted_or_cutoff_date_ambiguous |
| s2845-114 | train | already_enacted_or_cutoff_date_ambiguous |
| s2850-115 | train | already_enacted_or_cutoff_date_ambiguous |
| s2851-117 | 117 | No postCongress update assertion |
| s2854-117 | 117 | No postCongress update assertion |
| s2856-117 | 117 | No postCongress update assertion |
| s2868-117 | 117 | No postCongress update assertion |
| s2879-117 | 117 | No postCongress update assertion |
| s2892-117 | 117 | No postCongress update assertion |
| s2893-114 | train | already_enacted_or_cutoff_date_ambiguous |
| s2907-117 | 117 | No postCongress update assertion |
| s2915-117 | 117 | No postCongress update assertion |
| s2929-117 | 117 | No postCongress update assertion |
| s2933-117 | 117 | No postCongress update assertion |
| s2948-117 | 117 | No postCongress update assertion |
| s2969-117 | 117 | No postCongress update assertion |
| s2980-117 | 117 | No postCongress update assertion |
| s2985-117 | 117 | No postCongress update assertion |
| s2994-117 | 117 | No postCongress update assertion |
| s30-118 | 118 | already_enacted_or_cutoff_date_ambiguous |
| s3002-118 | 118 | No postCongress update assertion |
| s3008-117 | 117 | No postCongress update assertion |
| s3010-117 | 117 | No postCongress update assertion |
| s3014-117 | 117 | No postCongress update assertion |
| s3020-117 | 117 | No postCongress update assertion |
| s3025-117 | 117 | No postCongress update assertion |
| s3028-117 | 117 | No postCongress update assertion |
| s3031-115 | train | outside_horizon_or_end_date_ambiguous |
| s3097-117 | 117 | No postCongress update assertion |
| s3105-117 | 117 | No postCongress update assertion |
| s3116-117 | 117 | No postCongress update assertion |
| s3145-117 | 117 | No postCongress update assertion |
| s3158-117 | 117 | No postCongress update assertion |
| s3170-115 | train | already_enacted_or_cutoff_date_ambiguous |
| s3172-118 | 118 | No postCongress update assertion |
| s3199-117 | 117 | No postCongress update assertion |
| s3201-116 | train | already_enacted_or_cutoff_date_ambiguous |
| s3206-117 | 117 | No postCongress update assertion |
| s3238-117 | 117 | No postCongress update assertion |
| s3258-117 | 117 | No postCongress update assertion |
| s3260-117 | 117 | No postCongress update assertion |
| s3263-117 | 117 | No postCongress update assertion |
| s3269-117 | 117 | No postCongress update assertion |
| s3272-117 | 117 | No postCongress update assertion |
| s3299-117 | 117 | No postCongress update assertion |
| s3320-117 | 117 | No postCongress update assertion |
| s3339-117 | 117 | No postCongress update assertion |
| s3341-117 | 117 | No postCongress update assertion |
| s3357-117 | 117 | No postCongress update assertion |
| s3386-118 | 118 | No postCongress update assertion |
| s3391-117 | 117 | No postCongress update assertion |
| s3402-117 | 117 | No postCongress update assertion |
| s3426-117 | 117 | No postCongress update assertion |
| s3443-117 | 117 | No postCongress update assertion |
| s3472-117 | 117 | No postCongress update assertion |
| s3486-117 | 117 | No postCongress update assertion |
| s3494-117 | 117 | No postCongress update assertion |
| s3495-117 | 117 | No postCongress update assertion |
| s3509-118 | 118 | No postCongress update assertion |
| s3513-117 | 117 | No postCongress update assertion |
| s3521-117 | 117 | No postCongress update assertion |
| s3545-117 | 117 | No postCongress update assertion |
| s3561-117 | 117 | No postCongress update assertion |
| s3577-117 | 117 | No postCongress update assertion |
| s3583-117 | 117 | No postCongress update assertion |
| s3589-117 | 117 | No postCongress update assertion |
| s3611-117 | 117 | No postCongress update assertion |
| s3625-117 | 117 | No postCongress update assertion |
| s3626-117 | 117 | No postCongress update assertion |
| s3636-117 | 117 | No postCongress update assertion |
| s3640-117 | 117 | No postCongress update assertion |
| s3665-117 | 117 | No postCongress update assertion |
| s3671-117 | 117 | No postCongress update assertion |
| s3674-117 | 117 | No postCongress update assertion |
| s3716-117 | 117 | No postCongress update assertion |
| s3738-117 | 117 | No postCongress update assertion |
| s3766-117 | 117 | No postCongress update assertion |
| s3773-117 | 117 | outside_horizon_or_end_date_ambiguous |
| s3780-117 | 117 | No postCongress update assertion |
| s3785-117 | 117 | No postCongress update assertion |
| s3786-117 | 117 | No postCongress update assertion |
| s3812-117 | 117 | No postCongress update assertion |
| s3828-117 | 117 | No postCongress update assertion |
| s3831-118 | 118 | No postCongress update assertion |
| s3832-117 | 117 | No postCongress update assertion |
| s3849-117 | 117 | No postCongress update assertion |
| s3881-117 | 117 | No postCongress update assertion |
| s3925-117 | 117 | No postCongress update assertion |
| s3929-117 | 117 | No postCongress update assertion |
| s3974-118 | 118 | No postCongress update assertion |
| s3977-118 | 118 | No postCongress update assertion |
| s3987-117 | 117 | No postCongress update assertion |
| s3994-117 | 117 | No postCongress update assertion |
| s4018-117 | 117 | No postCongress update assertion |
| s4026-118 | 118 | No postCongress update assertion |
| s4051-117 | 117 | No postCongress update assertion |
| s4053-117 | 117 | No postCongress update assertion |
| s4054-117 | 117 | No postCongress update assertion |
| s4056-117 | 117 | No postCongress update assertion |
| s4076-117 | 117 | No postCongress update assertion |
| s4088-117 | 117 | No postCongress update assertion |
| s4129-117 | 117 | No postCongress update assertion |
| s4134-117 | 117 | No postCongress update assertion |
| s4137-118 | 118 | No postCongress update assertion |
| s4142-117 | 117 | No postCongress update assertion |
| s4143-117 | 117 | No postCongress update assertion |
| s4184-117 | 117 | No postCongress update assertion |
| s4221-117 | 117 | No postCongress update assertion |
| s4247-117 | 117 | No postCongress update assertion |
| s4264-117 | 117 | No postCongress update assertion |
| s4275-118 | 118 | No postCongress update assertion |
| s4315-117 | 117 | No postCongress update assertion |
| s4322-117 | 117 | No postCongress update assertion |
| s4334-117 | 117 | No postCongress update assertion |
| s4344-118 | 118 | No postCongress update assertion |
| s4346-117 | 117 | No postCongress update assertion |
| s4349-117 | 117 | No postCongress update assertion |
| s4351-118 | 118 | already_enacted_or_cutoff_date_ambiguous |
| s4368-117 | 117 | No postCongress update assertion |
| s4400-117 | 117 | No postCongress update assertion |
| s4437-117 | 117 | No postCongress update assertion |
| s4439-118 | 118 | No postCongress update assertion |
| s4445-117 | 117 | No postCongress update assertion |
| s4469-117 | 117 | No postCongress update assertion |
| s4471-118 | 118 | No postCongress update assertion |
| s4495-117 | 117 | No postCongress update assertion |
| s464-118 | 118 | No postCongress update assertion |
| s578-117 | 117 | already_enacted_or_cutoff_date_ambiguous |
| s585-115 | train | Uncorroborated latest-action public-law assertion |
| s701-118 | 118 | No postCongress update assertion |
| s71-118 | 118 | No postCongress update assertion |
| s730-118 | 118 | No postCongress update assertion |
| s744-116 | train | already_enacted_or_cutoff_date_ambiguous |
| s842-118 | 118 | No postCongress update assertion |
| s892-118 | 118 | No postCongress update assertion |
| s938-118 | 118 | No postCongress update assertion |
| s984-114 | train | already_enacted_or_cutoff_date_ambiguous |

## Reliability bins

| Congress | Model | Bin | n | Mean probability | Observed proportion |
| --- | --- | --- | --- | --- | --- |
| 117 | Two-column baseline | 0 | 913 | 0.016049803195716077 | 0.018619934282584884 |
| 117 | Two-column baseline | 1 | 31 | 0.10689915874876019 | 0.25806451612903225 |
| 117 | Two-column baseline | 2 | 0 | None | None |
| 117 | Two-column baseline | 3 | 0 | None | None |
| 117 | Two-column baseline | 4 | 0 | None | None |
| 117 | Two-column baseline | 5 | 0 | None | None |
| 117 | Two-column baseline | 6 | 0 | None | None |
| 117 | Two-column baseline | 7 | 0 | None | None |
| 117 | Two-column baseline | 8 | 0 | None | None |
| 117 | Two-column baseline | 9 | 0 | None | None |
| 117 | Baseline + context | 0 | 920 | 0.016066523019472638 | 0.01847826086956522 |
| 117 | Baseline + context | 1 | 21 | 0.1484864303223859 | 0.38095238095238093 |
| 117 | Baseline + context | 2 | 3 | 0.22830838870925305 | 0.0 |
| 117 | Baseline + context | 3 | 0 | None | None |
| 117 | Baseline + context | 4 | 0 | None | None |
| 117 | Baseline + context | 5 | 0 | None | None |
| 117 | Baseline + context | 6 | 0 | None | None |
| 117 | Baseline + context | 7 | 0 | None | None |
| 117 | Baseline + context | 8 | 0 | None | None |
| 117 | Baseline + context | 9 | 0 | None | None |
| 117 | Training-rate reference | 0 | 944 | 0.02029484970323569 | 0.026483050847457626 |
| 117 | Training-rate reference | 1 | 0 | None | None |
| 117 | Training-rate reference | 2 | 0 | None | None |
| 117 | Training-rate reference | 3 | 0 | None | None |
| 117 | Training-rate reference | 4 | 0 | None | None |
| 117 | Training-rate reference | 5 | 0 | None | None |
| 117 | Training-rate reference | 6 | 0 | None | None |
| 117 | Training-rate reference | 7 | 0 | None | None |
| 117 | Training-rate reference | 8 | 0 | None | None |
| 117 | Training-rate reference | 9 | 0 | None | None |
| 117 | Action-milestone reference | 0 | 913 | 0.01121958322728693 | 0.018619934282584884 |
| 117 | Action-milestone reference | 1 | 0 | None | None |
| 117 | Action-milestone reference | 2 | 31 | 0.2022487634462609 | 0.25806451612903225 |
| 117 | Action-milestone reference | 3 | 0 | None | None |
| 117 | Action-milestone reference | 4 | 0 | None | None |
| 117 | Action-milestone reference | 5 | 0 | None | None |
| 117 | Action-milestone reference | 6 | 0 | None | None |
| 117 | Action-milestone reference | 7 | 0 | None | None |
| 117 | Action-milestone reference | 8 | 0 | None | None |
| 117 | Action-milestone reference | 9 | 0 | None | None |
| 118 | Two-column baseline | 0 | 1077 | 0.016838589634798146 | 0.012070566388115135 |
| 118 | Two-column baseline | 1 | 31 | 0.10663604656226759 | 0.22580645161290322 |
| 118 | Two-column baseline | 2 | 1 | 0.2592421654506161 | 1.0 |
| 118 | Two-column baseline | 3 | 0 | None | None |
| 118 | Two-column baseline | 4 | 0 | None | None |
| 118 | Two-column baseline | 5 | 0 | None | None |
| 118 | Two-column baseline | 6 | 0 | None | None |
| 118 | Two-column baseline | 7 | 0 | None | None |
| 118 | Two-column baseline | 8 | 0 | None | None |
| 118 | Two-column baseline | 9 | 0 | None | None |
| 118 | Baseline + context | 0 | 1088 | 0.015410084709372851 | 0.013786764705882353 |
| 118 | Baseline + context | 1 | 20 | 0.1398928473495711 | 0.25 |
| 118 | Baseline + context | 2 | 0 | None | None |
| 118 | Baseline + context | 3 | 1 | 0.3504776257513096 | 1.0 |
| 118 | Baseline + context | 4 | 0 | None | None |
| 118 | Baseline + context | 5 | 0 | None | None |
| 118 | Baseline + context | 6 | 0 | None | None |
| 118 | Baseline + context | 7 | 0 | None | None |
| 118 | Baseline + context | 8 | 0 | None | None |
| 118 | Baseline + context | 9 | 0 | None | None |
| 118 | Training-rate reference | 0 | 1109 | 0.020294849703235692 | 0.018935978358881875 |
| 118 | Training-rate reference | 1 | 0 | None | None |
| 118 | Training-rate reference | 2 | 0 | None | None |
| 118 | Training-rate reference | 3 | 0 | None | None |
| 118 | Training-rate reference | 4 | 0 | None | None |
| 118 | Training-rate reference | 5 | 0 | None | None |
| 118 | Training-rate reference | 6 | 0 | None | None |
| 118 | Training-rate reference | 7 | 0 | None | None |
| 118 | Training-rate reference | 8 | 0 | None | None |
| 118 | Training-rate reference | 9 | 0 | None | None |
| 118 | Action-milestone reference | 0 | 1077 | 0.012483758896842464 | 0.012070566388115135 |
| 118 | Action-milestone reference | 1 | 1 | 0.18357904141936307 | 1.0 |
| 118 | Action-milestone reference | 2 | 31 | 0.2022487634462609 | 0.22580645161290322 |
| 118 | Action-milestone reference | 3 | 0 | None | None |
| 118 | Action-milestone reference | 4 | 0 | None | None |
| 118 | Action-milestone reference | 5 | 0 | None | None |
| 118 | Action-milestone reference | 6 | 0 | None | None |
| 118 | Action-milestone reference | 7 | 0 | None | None |
| 118 | Action-milestone reference | 8 | 0 | None | None |
| 118 | Action-milestone reference | 9 | 0 | None | None |


## Every remaining public-law-assertion feature exclusion

These 41 cases remain excluded for the stated action-design reasons, not publication metadata. Assertions alone are not eligible positive labels.

| Bill | Feature exclusion |
|---|---|
| hr6513-115 | cutoff_at_or_after_congress_end |
| hr5889-114 | cutoff_at_or_after_congress_end |
| hr5331-113 | cutoff_at_or_after_congress_end |
| s2673-113 | cutoff_at_or_after_congress_end |
| hr6157-115 | Action predates introduction |
| hr6007-114 | cutoff_at_or_after_congress_end |
| s5016-117 | cutoff_at_or_after_congress_end |
| s8-114 | cutoff_at_or_after_congress_end |
| s2651-113 | cutoff_at_or_after_congress_end |
| s3456-115 | cutoff_at_or_after_congress_end |
| hr5462-113 | cutoff_at_or_after_congress_end |
| s5060-117 | cutoff_at_or_after_congress_end |
| hr9487-118 | cutoff_at_or_after_congress_end |
| s4791-117 | cutoff_at_or_after_congress_end |
| s3554-115 | cutoff_at_or_after_congress_end |
| s2759-113 | cutoff_at_or_after_congress_end |
| hr5722-114 | cutoff_at_or_after_congress_end |
| hr5687-114 | cutoff_at_or_after_congress_end |
| hr6405-115 | cutoff_at_or_after_congress_end |
| s4926-117 | cutoff_at_or_after_congress_end |
| hr6591-115 | cutoff_at_or_after_congress_end |
| hr5798-114 | cutoff_at_or_after_congress_end |
| hr8404-117 | cutoff_at_or_after_congress_end |
| hr6451-114 | cutoff_at_or_after_congress_end |
| hr8454-117 | cutoff_at_or_after_congress_end |
| s5036-116 | cutoff_at_or_after_congress_end |
| hr8354-116 | cutoff_at_or_after_congress_end |
| hr5739-113 | cutoff_at_or_after_congress_end |
| s3749-115 | cutoff_at_or_after_congress_end |
| hr6297-114 | cutoff_at_or_after_congress_end |
| s3509-115 | cutoff_at_or_after_congress_end |
| hr5106-113 | cutoff_at_or_after_congress_end |
| hr5771-113 | cutoff_at_or_after_congress_end |
| s5329-117 | cutoff_at_or_after_congress_end |
| hr7327-115 | cutoff_at_or_after_congress_end |
| hr6428-115 | cutoff_at_or_after_congress_end |
| s2921-113 | cutoff_at_or_after_congress_end |
| hr6431-114 | cutoff_at_or_after_congress_end |
| hr5030-113 | cutoff_at_or_after_congress_end |
| hr5108-113 | cutoff_at_or_after_congress_end |
| s3367-115 | cutoff_at_or_after_congress_end |

[Complete publication-gate removal check](../../../data/research-runs/action-context-resolution-root-20261111/publication-gate-removal-check.json).

- [Original acquisition](../../../data/research-runs/official-context-acquisition-v1-20261109/registration.json) — SHA-256 `d5383a5942f7494e223a64f8449375b20dab9ce7bb3ef982a8327939b880c219`

- [Action preparation](../../../data/research-runs/action-context-features-v1-20261109/registration.json) — SHA-256 `7b8a581d58a989a22c80b6bc4399770d1d155caf0a639db02580d5f897f482ae`

- [Label-contract audit](../../../data/research-runs/action-label-contract-diagnostic-v1-20261109/registration.json) — SHA-256 `ae0e1a008d13553eb27f4e68200fc9447d83bb230898f618610967772c09fdb2`

- [Every contract assertion](../../../data/research-runs/action-label-contract-diagnostic-v1-20261109/cases.json) — SHA-256 `b7234e778b7c6860ab4793c965db6832b784ead35def8527475e2521ff4f8997`

Final preservation check: all 85,304 prior files unchanged; frozen-model audit unchanged; all 36,034 new registration bindings verified. [Validation receipt](../../../data/research-runs/action-context-resolution-root-20261111/final-validation.json).
