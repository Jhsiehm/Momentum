# Action-context retrospective diagnostic — November 9, 2026

Status: independently replayed stop before fitting. No positive labels were accepted under the unchanged resolver; zero fits and no probability scores.

## Why this is a new experiment

The preceding publication-based comparison stopped before fitting. Its independently replayed conditioning audit found that all 333 records with current public-law assertions were excluded: 293 because enrolled-edition dates were empty, 40 because the day-180 checkpoint was outside Congress. That outcome-associated metadata selection cannot be repaired by claiming the remaining eventless population is representative. [Preserved predecessor receipt](20261109-official-context-diagnostic.md).

This new adaptive question asks whether dated cosponsorship, referral breadth and action recency improve on an action-milestone/chamber baseline. It uniformly reconsiders the same 12,000 saved official records, with no new sources, replacements or outcome enrichment. All cases are development-exposed; no untouched, prospective or historically available-data claim is made.

## Fixed comparison

Train on Congresses 113–116; evaluate 117 and 118 separately using the same two fitted artifacts. The baseline has exactly two columns: milestone index divided by three, and Senate indicator. The challenger adds the unchanged three context transformations and three explicit missingness flags, for eight columns. Training-only median imputation and population-standard-deviation scaling (floor 0.1) precede fixed logistic optimization, L2=0.05, at most 20,000 iterations, gradient infinity norm at most 1e-6. Exactly two fits, no tuning, calibration, replacement or final refit.

Milestones use exact Library of Congress source-9 action codes before the cutoff: origin-chamber reporting, origin-chamber passage, presentation to the President. Index zero means no recognized recorded milestone, not certified absence of progress. The action-milestone reference is a training-only category rate with fixed shrinkage five toward the Beta(1,1) training rate. This is a different reference from the prior publication-stage benchmark.

The original family-selection salt, protected/exposed exclusions, external-node links, later-period priority and deterministic representative selection remain fixed. Every difference from the predecessor family population is saved before outcomes. The unchanged v2 outcome resolver is imported directly: own-public-law/date corroboration for positive labels, explicitly uncertified current-record negative proxies, and unknowns otherwise. Historical custody, source completeness and complete provision genealogy remain unresolved.

Whole-history structural eligibility still uses the quality of later source records; only pre-cutoff action assertions enter the baseline. This residual selection limitation is explicit. Current-record negative follow-up and missingness remain uncertain. No result automatically qualifies for promotion or the 60% forecast objective.

## Source preparation and independent preflight

All 12,000 original sources were reused with zero requests. Preparation retained 10,095 baseline-valid records and excluded 1,905: 1,884 unreachable day-180 checkpoints, 20 action histories predating introduction, and one unsupported action container. Baseline milestone counts among retained sources: 9,259 index0, 294 index1, 462 index2 and 80 index3.

After family selection, before labels: 5,287 training candidates, 1,421 Congress-117 candidates and 1,497 Congress-118 candidates; 3,795 source/feature/family exclusions. Training context observations: 4,263 cosponsor, 5,257 referral and 5,287 recency, so none is entirely missing before outcome gates. These are candidate counts, not final fitting denominators.

Thirty-nine focused synthetic checks passed normally and with optimized Python: 17 feature and 22 runner tests. Mocked optimization in software checks is not a model result. Independent complete source replay matched every binding, byte, feature and invariant. Source replay SHA-256: `f3f22ff5779f9eb5f9e4268a268c645cccbd618a5de586f52c5faa7062b028ae`.

Preparation runtime: `data/research-runs/action-context-features-v1-20261109/`. Fit runtime: `data/research-runs/action-context-diagnostic-v1-20261109/`. Every source disposition, feature, family membership/change, label exclusion, input matrix and model probability is retained in ignored runtime storage. Code, protocols and research summaries are committed; downloaded XML is not.

## Actual label gate and zero-fit result

| Role | Candidates | Negative proxies | Unknown | Positive labels |
|---|---:|---:|---:|---:|
| Training | 5,287 | 5,116 | 171 | 0 |
| Evaluation 117 | 1,421 | 919 | 502 | 0 |
| Evaluation 118 | 1,497 | 1,088 | 409 | 0 |

The required both-class gate stopped this registered study before optimization. There are **zero fit intents, zero fits and no probabilities or performance metrics**. Unknown reasons: 851 lacked a post-Congress update assertion; 231 failed terminal-action public-law-text identity validation. No tuning, refitting or representation change followed the failure.

Independent replay matched all 8,205 family-selected rows and labels, all 1,082 unknown exclusions, registered code/input bindings and the exact stop. The prelabel predecessor comparison recorded 284 added identities and 35 removed identities; 256 added families, seven removed families and 28 changed representatives. These changes arose from the new feature eligibility, not label-dependent replacement.

All 858 full-suite tests passed in 85.993 seconds. This software validation did not establish real-source label adequacy. A bounded source-label contract diagnostic is being separately registered on the existing 231 rejected identities; no replacement labels or efficacy claims are made here. The first checked source contains both matching law-number actions and a separately coded signing annotation, showing why the exact contract needs investigation rather than another model architecture.

Independent failure replay SHA-256: `19a9ee4d38139d7c6bf740a8295a8933c86e3e7a29b53a38f96647f91589deb7`.

Runtime artifact hashes: {"failure.json": "d43a148c8b24945233322276bdf08bb287c2dbb2ace3aab9abba8b58d1d227bb", "feature-population.json": "e16f6def45bd5787b336580796e8af1c664879891b37ae7ee310f953d3de0541", "independent-review.json": "19a9ee4d38139d7c6bf740a8295a8933c86e3e7a29b53a38f96647f91589deb7", "label-counts.json": "917b9919485d9303d20075eb9621a10ba7ce0e30aacb337ed9de0319317ad4ac", "label-exclusions.json": "a19a3e7114c755a303c3ca346775414a8ee0c4424060673d48941b3f263debf2", "label-ledger.json": "66bf0956c921a5b3432f32a50587ba38489e949f896edd5919e04b90eb92b014", "predecessor-population-changes.json": "a58b48d689a2dcde7170ecf9074c88e18903d4ed379f2c77fde2937d6b69c894", "registration.json": "b54720e9f7df14ae188f356b41f2826581112438cbc39d98fe2b1c72a508cb80"}.
