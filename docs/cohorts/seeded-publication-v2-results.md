# Fixed-sample evidence amendment: version 2

The two version-1 evidence blockers were resolved in a separate registered amendment. The original blocked study and older pilot remain unchanged.

## Evidence

- All 100 selected bills pass source identity checks; 14 remain excluded under the unchanged checkpoint/family rules.
- Introduction uses the explicit official MODS introduction action, distinct from publication issue date. This uniform rule reconciles H.R.5925 without changing its checkpoint.
- The final House calendar CCAL-116hcal-S2 lists all 344 public-law/originating-bill pairs, matching NARA. Its bounded availability is May 8, 2021.
- Every sampled 116th law-positive also requires separately dated historical evidence. H.R.748 / Public Law136 passes, available August20,2020.
- The late individual package for Public Law283 remains documented; that bill is not sampled. The calendar establishes complete membership; sampled dated-law evidence establishes the unchanged date-bound target.

## Result

53 training cases (2 enacted); 33 evaluated cases (0 enacted).

| Metric | Candidate | Baseline |
|---|---:|---:|
| Brier loss, lower better | 0.00605899 | 0.00297521 |
| Log loss, lower better | 0.04397273 | 0.05608947 |

Primary paired Brier difference: **+0.00308378**, worse for the candidate. Conditional family-bootstrap 95% interval: [-0.00242816, 0.01294043]. This interval does not account for training or Congress-level uncertainty.

The candidate has no demonstrated added value. Lower secondary log loss does not reverse the primary-metric result. With zero evaluation enactments, discrimination cannot be assessed; these scores do not establish useful forecasting of successful bills. No model promotion or adaptive tuning occurred.

## Reproduction

`python3 -m engine.sample_publication_v2 reproduce`

PDF extraction requires `pypdf==6.14.2`; its version and extracted-text hash are retained. Cached source bytes, all rows, exclusions, protocol and code hashes are checked offline.

Fingerprint: `27f393350b69eed8bab575114063bc190a5f657880082b496b697402816f1dd9`

This is a post-inspection evidence amendment, not a new protected holdout. Current preservation metadata does not prove historically identical document bytes. Automated family linkage is incomplete; all human audit receipts remain pending. Action-history eligibility is unchanged.

## Next research decision

Keep the baseline and collect a larger, separately registered temporal evaluation cohort with enough naturally occurring enactments to assess discrimination. Preserve population sampling weights if enrichment is used. Finalize family adjudication and keep a protected future evaluation set before selecting or promoting any adaptive candidate. Do not tune repeatedly on these 33 outcomes.
