# Proposed action-context successor after the blocked publication-anchor run

November 9, 2026. **Design only, pending the investigation of the blocked run. No implementation, new requests, labels or fits were executed for this proposal.** The prior diagnostic reached its label gate with no training positives and performed zero fits. An association between the publication-feature exclusions and enactment is under investigation; it is not assumed established here. All existing source acquisition, exclusions, labels and failed-run evidence remain immutable.

## Scientific decision

Replace the publication-dependent prediction question with a **separately registered action-context question**, on the same already acquired, now explicitly exposed sample: do the three reconstructed context fields improve probability estimates beyond a documented action-milestone/chamber baseline? This is a substantive new baseline, not a repair that discards inconvenient edition records or attempts to force positive cases into the old model. No publication-version completeness criterion applies to either new arm. Recompute new features for every acquired identity under identical rules, including prior successes and failures; never select only previously excluded, enacted or positive cases.

The reason to consider this change is structural: forecasts about an at-risk bill need not require that every later edition retain complete publication metadata. A baseline built exclusively from pre-cutoff action assertions tests a different, defensible source representation. This decision is adaptive to observed source/class failure and therefore exploratory. The 12,000 originally selected identities, all acquired bytes and any inspected labels remain development-exposed; no fresh-test or historical-availability claim is possible.

## Primary-source-supported milestone definition

Use the already retained [official GPO BILLSTATUS guide](https://github.com/usgpo/bill-status/blob/main/BILLSTATUS-XML_User_User-Guide.md), section3, with local SHA-256 `a10909696b2ed2244d75c76e75fa32bc3e4eb926deab7e4e00592a6a01c3ad3a`. The guide describes multiple source systems and explicitly warns that its code table is not a complete authoritative dictionary. Restrict the following semantic map to **numeric source system9 (Library of Congress)** and exact codes; preserve source/date/code evidence per feature.

| Recorded milestone index | Exact eligible action assertion before cutoff |
|---|---|
| 0 | No recognized milestone below observed; this means no selected milestone recorded, not proof that the bill never advanced |
| 1 | Origin-chamber reporting: `5000` for H.R.; `14000` for S. |
| 2 | Origin-chamber passage: `8000` for H.R.; `17000` for S. |
| 3 | `28000`, presentation to the President, for either bill type |

Take the maximum observed index over valid dates strictly before day180. Index3 means presentation, not enrolled publication or a general “both chambers passed” inference. Do not equate seeing both chamber passage codes with identical-text agreement. Never use enactment `36000`, presidential signing, final/latest action, later dates or outcomes as stage features. Already-enacted-at-cutoff removal belongs to the separate fixed outcome/risk-set resolver.

Unknown/other codes and Senate-named records are not assigned new milestone semantics. Their dates may remain ordinary activity inputs under the existing context rules. `H30000` is **consideration by House**, not passage: do not reuse the existing general ingestion helper as the scientific mapping. This proposal does not alter that helper or any frozen earlier result.

## Exactly two candidate arms

**A — action-milestone baseline:** exactly two columns: recorded milestone index divided by3, and Senate indicator. This is a newly named two-column baseline, not the previous six publication features. Require a valid introduced date/checkpoint and a nonempty supported top-level action history with valid dates and at least one pre-cutoff action. Source categories use the already reviewed ordinary-action source rules; only exact LOC9 codes receive milestone semantics. Histories with unsupported source representations or invalid dates are ineligible, not encoded as zero. Stage0 means no recognized advancement assertion in that supported history, not proof of complete legislative inactivity. The index is deliberately a lower-bound source-observation summary. Freeze exact validation and synthetic tests before re-extraction.

**B — A plus existing context:** active cosponsors, top-level referral breadth and action recency, retaining the already fixed transformations, three training medians and three missingness indicators. The challenger has exactly eight columns: two baseline, three imputed context, three missingness indicators. Implement a separately versioned eight-column training-only adapter; do not relabel the prior twelve-column input. Baseline and context semantics are explicitly recorded. Preserve the fixed optimizer and regularization, two artifacts maximum, no calibration/tuning or extra text arm. If any context field has no observed training values, stop the whole study rather than selecting a favorable subset.

References remain the matched Beta(1,1) historical rate and fixed shrinkage5 milestone-rate reference. The latter must be named **action-milestone reference**, not the prior publication-stage reference. Its categories are indices0–3; each uses training-only positives and counts, with empty categories falling back to the global rate. Unsupported baseline histories are excluded identically from both arms, not made a fifth category. All probabilities are evaluated on the same rows in each period.

## Population, labels and stopping remain fixed

Use the original12,000 selected identities and existing acquisition failures without replacements, new downloads, outcome enrichment or resampling. Train113–116; evaluate117 and118 separately. Preserve protected/exposed exclusions, external-node family graph, later-period priority, one deterministic family representative and the existing selection salt. Source-only action-feature/family membership must be sealed before invoking the outcome resolver again. Changes in representatives due to removing the obsolete publication gate must be recorded per family, not hidden.

Keep the registered current-official-record label-proxy rule unchanged: concordant own-bill public-law/action/date positives, strict after-cutoff/before-end horizon, post-Congress update plus supported history/no enactment assertion for uncertified negative proxies, otherwise unknown. Do not relax source-system codes, action assertions or post-Congress update requirements to recover classes. Report the investigation's label/exclusion association as development evidence and disclose that classes were already exposed in the failed predecessor.

Before two fits, freeze exact new features, missingness, family membership, proxy labels, all exclusions and class counts. Require both training classes and nonempty evaluations; report event sparsity without pretending operational checks establish power. No positive-count-driven acquisition, threshold changes or score-based tuning. If the same fixed source-proxy label policy still yields no trainable classes, stop and publish the specific source/label failure; do not try another representation solely to bypass the gate.

Report per-period and equal-period Brier/log loss, context-minus-baseline difference, skill against rate and the newly named milestone reference, class-specific losses/counts, expected events, reliability bins and the unchanged descriptive family bootstrap. Preserve zero/negative results and every case probability/exclusion. This study cannot release E3, demonstrate prospective self-learning or establish the60%forecast target.

## Go/no-go before implementation

Proceed only if the source-only investigation supports that removing the publication gate addresses a representation-dependent selection problem, and the independent methods reviewer accepts the exact new action/history-eligibility mapping and adaptation disclosure. Implementation must be separately versioned across extractor, protocol and runner; no frozen predecessor file changes. The irreducible limits remain current-rendition event assertions, imperfect proxy negatives, incomplete family genealogy and prior exposure. No new human certification prerequisite is introduced for this expressly retrospective diagnostic.
