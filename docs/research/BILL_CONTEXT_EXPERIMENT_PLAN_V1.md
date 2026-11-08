# Bill context and controlled learning: experimental plan v1

Date: November 8, 2026 (America/New_York). Status: **complete staged research plan; experiments not executed by this planning task**. Authoring baseline: repository commit `866f590`. This plan defines the programme and decision rules. Each execution still requires a sealed, machine-readable registration of exact rows, features, code, sources and computational budget before new predictions or fitting. It is not an external preregistration, a claim of available data, or permission to bypass existing gates.

## 1. Objective and research contribution

Determine whether richer, point-in-time representations of individual bills improve day-180 own-bill public-law enactment probabilities across successive Congresses, beyond procedural stage and a historical-rate reference. Preserve full bill language alongside structured attributes, events and context. A bill's unique tracking ID is not a predictor to memorize. Multiple subjects and mechanisms may coexist; never force a bill into one exclusive category.

The proposed paper contribution is an auditable test of **content + political support + procedural opportunity**, with component ablations, temporal evaluation and preserved negative findings. The adaptive system is a separate research contribution: determine when learning from newly resolved bills helps, and when retaining a model is preferable.

The long-term 60% ambition means BSS_rate = 1 − Brier_model/Brier_rate ≥ 0.60 on identical cases. For an illustrative rate loss of 0.020, the target is at most 0.008; these are examples, not measured new results. The baseline is trained only on eligible earlier data, never the future period's observed rate. Report skill versus a credible stage baseline and survivor too. Sixty percent is an aspiration, not a stopping rule, sample-size rule or promised attainable effect.

## 2. Evidence motivating the programme

| Observed evidence | Implication for the next experiment |
| --- | --- |
| Six inputs produce only about 200 distinct vectors per exposed period | Add distinguishing information; unique IDs alone do not solve this |
| L2=0.05 improves matched exposed controls by 8.3911% after convergence checks | Retain this procedure as a development reference, not an independently proven winner |
| Updating improves two periods and worsens one | Test update policies across time; do not equate additional data with progress |
| The 2,315-case/29-positive campaign comparison effectively ties the survivor | Stronger development results do not establish transfer |
| Real-source audit verified 40 files across 12 bills, but historical byte identity and human reviews remain unresolved | Improve provenance before expanding empirical claims |
| Missing exposed-development exclusion was repaired | Register the complete exposure/family universe, not only direct training IDs |

Sources: [granular audit](../operations/runs/20261105-granular-transfer-audit.md), [convergence](../operations/runs/20261105-convergence.md), [campaign](../operations/runs/20261105-cross-congress-campaign.md), [live-agent review](../operations/runs/20261105-live-agent-paper-review.md). Counts overlap and are not independent replications. No source supports a guaranteed 60% gain.

## 3. Scope, frozen studies and chronological design

Preserve [PAPER_PROTOCOL_V1](PAPER_PROTOCOL_V1.md), all models, manifests, source bytes and forecasts. Its outcome, day-180 risk set, date precision, negative-label coverage, human gates and no-promotion rules remain controlling. The day-30 passage project and provision-incorporation targets stay separate.

Use Congresses 115, 116 and 117 as **exposed development folds**, with earlier eligible training per fold. The existing memberships are starting manifests, not automatically certified data. Known 114 development results are part of exposure history; 118 is exposed audit evidence and excluded from new candidate ranking in this programme. Do not backtest the frozen survivor into checkpoints before its training labels were available. Period-specific refits are the legitimate historical controls; the survivor is reserved for temporally admissible comparisons.

For E1–E5, reuse the exact existing per-fold core/calibration/evaluation identities when all required evidence passes. Where an additional feature's required source is unavailable, freeze a feature-specific matched subset **before viewing its model scores**, and rerun its control on that identical subset. Never compare a full-sample control score with a restricted-sample treatment. Keep all candidates in a flow ledger, including exclusions and missing labels. Different subsets support different conditional estimands and cannot be ranked as though interchangeable.

Training labels must be effective and knowable before the earliest evaluation checkpoint; training Congresses must precede the test Congress. Preprocessing fits on core training only. Calibration uses its separate earlier calibration families. Purge training/evaluation family overlap using the registered global graph. New conflicting links block affected execution rather than silently changing saved membership. Record exposure honestly: these folds can support development hypotheses, never an independent success claim.

Existing stricter provenance, human and positive-family gates remain in force. Legacy computation floors are not scientific adequacy. The paper protocol's 200 reviewed positive training-family and 100 reviewed positive development-family requirements must be checked for a new selection study; counts must be distinct at the applicable study level, not sums of reused folds. A methods reviewer must record the gate's precise population in the execution manifest. A fold or study that fails an applicable gate is blocked, not granted an exception because a score is computable. Current receipt counts do not establish that these reviewed floors are met.

## 4. The bill record: retain meaning and produce controlled inputs

The evidence store holds the full record; experiments select explicit views from it. A classifier label never replaces the original text.

| Record component | Stored representation | First-cycle predictive view |
| --- | --- | --- |
| Identity | Congress/chamber/number, stable internal ID, version ID | Chamber only; IDs join records and enforce exclusions |
| Original language | Exact source bytes, parsed sections, headings, amendments, citations and version history | Introduced-text features first; later text only in a separate as-of contrast |
| Policy subjects | Multiple official or extracted subjects with source spans and availability | Fixed vocabulary from core training; unknown allowed |
| Legal mechanisms | Create programme; authorize; appropriate; tax; prohibit; require; amend; repeal; rename/designate; reporting; deadline; sunset | Twelve independent presence flags plus unknown indicators; no inference from title alone |
| Meaning at provision level | Action, affected entity/population, statutory object, amount/unit, exception, condition, effective date, supporting span | First cycle uses mechanism flags; detailed values retained for review and later registered studies |
| Political support | Sponsor and dated affiliations/roles; cosponsor additions/removals | Majority-party indicator, committee-role indicators, log(1+known cosponsors), bipartisan share |
| Procedure | Dated, sourced referrals, hearings, markups and passage events | Audited event counts and elapsed times; never equate missing actions with no actions |
| Relationships | Typed edges: companion, reintroduction, related bill, shared text; evidence and as-of dates | Counts/existence of known companions; no related bill's future outcome |
| Calendar | Bill age, Congress/session position, terminal boundary, announcements and their versions | Remaining days, annual session, announced next-14-day activity where complete evidence exists |
| Review/provenance | Source, parser, extraction and review identities; uncertainty and missingness | Eligibility/missingness controls; review verdict itself is not an outcome predictor |

Every attribute carries: value; status (`observed`, `derived`, `unknown`, `disputed`, `not_applicable`); source URL/hash; document/version and exact span; effective time; original publication/availability evidence; actual retrieval time; parser/model/prompt version where applicable; extraction method; review state. Human approval may only be recorded by its actual reviewer. An AI confidence value is not a calibrated probability of correctness unless separately validated.

Example meaning record: “expands eligibility” → specified beneficiary group → amends named statute → income condition and exceptions → effective date → exact supporting section. Preserve cross-references and negation. Funding authorization and appropriation are distinct labels. A renamed facility and a nationwide entitlement change can share a policy area without sharing their substantive mechanisms.

Current summaries, subjects, affiliations and related-bill lists are not automatically historic facts. A bill-level label assigned today may be unavailable at day 180. The record can retain it for navigation while excluding it from historical prediction.

## 5. E0 — establish a reviewed representation before fitting

**Hypothesis:** the proposed fields can be extracted reproducibly with adequate source support, without future information or loss of substantive meaning. This is an evidence/measurement study, not a prediction contest.

Freeze 100 existing earlier-development bills: 20 from each of 113–117, selected by ascending `digest(bill_id)` within Congress, one per registered family across the pilot. Preserve the existing 12-case packet separately; do not retroactively call it a random quality holdout. If a period cannot supply 20 eligible distinct families, block that pilot stratum, retain the shortfall, and do not replace identities by inspecting outcomes. The deterministic 100 selection is for field feasibility, not population prevalence estimation.

Within each 20, first 10 are extraction-design cases and last 10 are an extraction-quality check: 50/50 in total. Hide enactment outcomes from extractors/reviewers where practicable; use only the introduced/as-of source documents, not final BILLSTATUS narratives. Register and freeze vocabulary, annotation guide and extraction rules after the design 50, before opening quality annotations. Two qualified reviewers independently annotate the quality 50; a third adjudicates disagreements. Agent audits may help assemble evidence but cannot fill those human roles. Previously required human reviews remain separate unless their exact coverage is explicitly documented.

First extraction implementation: deterministic XML/section/citation parsing, a fixed mechanism lexicon, and human-adjudicated interpretation. No paid LLM calls or historically contaminated general-model features in this initial pilot. Full text is preserved even when the parser cannot extract a field.

Report attribute-level precision/recall, exact date/unit agreement, disagreement, abstention and evidence coverage, including per-period differences. Proposed engineering acceptance: 100% retained evidence references resolve; zero uncorrected identity or future-availability errors; mechanism precision ≥95% and recall ≥90% on adjudicated quality annotations for a field with at least 20 positive examples. These are engineering thresholds, not significance or power claims. Sparse fields remain stored but are not certified predictive inputs. Zero observed errors does not establish zero population error. Freeze failed results; do not revise rules on the quality set and call its rescore independent. A new extractor version needs a separately registered quality sample.

**Deliverables:** versioned schema/dictionary, 100-case disposition list, section-preserving records, annotation guide, source/feature matrix, quality report and pending-review queue. Scaling occurs only for accepted fields and preserves failures.

## 6. Common modeling and measurement rules

For the first feature experiments, use standardized logistic regression with unpenalized intercept and mean negative log likelihood plus `(0.05/2) × sum(slope²)`. Core-only means/scales use the existing floor of 0.1. The low-dimensional solver retains learning rate 0.12, minimum 300 steps, maximum 20,000 and max absolute training-objective gradient ≤1e-6. Both control and additions must converge; any failure is a blocked comparison, not permission to increase the cap after seeing scores. Record unclipped finite gradients, iterations and scalar equivalence checks. No L2 grid search.

Apply the existing 2,000-step monotone affine-logit calibration to each arm on the identical earlier calibration set; report raw and calibrated losses. Refitting calibration is part of the procedure, not proof that its base alone improved. Both outcome classes must exist in core and calibration. Model and feature code, scaling, exact memberships and every trial artifact are retained.

Global historical-rate baseline: Beta(1,1) on the full eligible core+calibration training risk set. Stage baseline: `(positives_in_stage + 5 × global_rate)/(stage_n+5)` with stages 0–3. Fit both before evaluation and score on the same cases as the model. Do not substitute the old survivor's 2/51 rate as the main reference. A frozen survivor score is only included if its full training-label timing and family rules pass.

Report per-fold Brier, BSS against both baselines, log loss, fixed-decile reliability/counts, expected events, positive/negative Brier, event/family counts, coverage and exclusions. Primary aggregate is the mean of fold Brier losses, with equal period weights; aggregate BSS is a ratio of those mean losses. Report bill-weighted pooled loss secondarily. Display missing metrics as unavailable, never zero.

A **development lead** must improve calibrated Brier and not worsen log loss against its matched control in every eligible registered fold. If any required fold is blocked, the all-fold decision is blocked. Rank qualifying leads by equal-period Brier, tie tolerance 1e-12; break ties by fewer features and then the arm order below. All results remain exploratory because the periods informed the research direction. Average improvement with a reversed period is a mixed result, not a qualifying lead. No automatic promotion follows.

Use the paper protocol's 10,000 paired global-family bootstrap draws and fixed seed for descriptive conditional intervals; retain period memberships and report invalid draws. These intervals are not selection-adjusted significance tests. Two or three Congresses cannot justify a precise population-wide period-cluster claim. Do not bootstrap individual bills as independent when related. No fixed positive count guarantees power.

## 7. Ordered experiment matrix

E1 may proceed after its existing-source gate even while E0's richer annotation work continues. E2–E5 require their own reviewed sources. Each block below is registered before its first score; at most the listed arms are permitted. A failed feature block stays failed and is not silently redesigned in the same registration.

| ID | Falsifiable question | Registered arms and comparison | Interpretation / output |
| --- | --- | --- | --- |
| E1: time opportunity | Does remaining legislative time improve stage-based probabilities? | Six-feature converged control; control + `r`; control + `r` + `(stage/4)×r`, where `r=(Congress_end−checkpoint).total_seconds()/(86400×730)` | Three arms × three folds; first inexpensive test of a known omission |
| E2: meaning categories | Do policy/mechanism descriptors distinguish otherwise similar bills? | Fixed anchor A; A + accepted multi-label policy/mechanism flags with unknown indicators | Meaning gain against matched anchor; two arms per fold |
| E3: full text | Does preserved bill language add beyond categories? | A; A + text; A + E2 descriptors + text, only if descriptor quality passes | Three arms per fold; separate text contribution and joint representation |
| E4: support and progression | Do political support and actual procedural histories add information? | A; A + support block; A + procedural block | Three arms per fold; each block has a fixed field list and separate provenance audit |
| E5: schedule and relations | Do known agenda opportunities and bill relationships add information? | A; A + calendar/schedule block; A + relationship block | Three arms per fold; no actual future agenda or outcome leakage |
| E6: combined representation | Do individually supported blocks still help when combined? | A; A + union of qualifying E2–E5 blocks; leave-one-block-out versions of that union | At most six arms per fold; compare only on a single frozen common eligible population |
| E7: functional form | Does model flexibility add value beyond representation? | E6 logistic winner; fixed shallow boosted-tree model on the same structured features | Two arms per fold; no text-heavy tree model or architecture sweep |
| E8: controlled updating | Does a fixed update policy outperform retaining a model? | Frozen initial anchor; expanding-history refit; latest-two-eligible-Congress refit | Three policies × three folds; all are development diagnostics |
| E9: prospective validation | Does one frozen successor improve independent future predictions? | Requires a separately registered successor protocol; compare with credible rate/stage references and temporally admissible retained models | Not launched by this plan; no unexposed historical replacement is assumed |

**Anchor A:** freeze the qualifying E1 arm with lowest equal-period Brier; if neither addition qualifies, retain the six-feature control. A is an encoding/procedure refitted separately for each fold, not the final 113–117 artifact applied backward in time. E2–E5 always compare to A, not a moving winner from the preceding block. This makes each addition interpretable. Selection makes downstream results further exploratory; record that dependency.

If E3 joint descriptors+text qualifies, treat it as one composite block for E6; do not count a separately selected E2 descriptor block twice. E6 removes the composite together and may report its two component ablations as part of the preallocated six-arm cap; if the cap cannot accommodate them, omit component ablations rather than add unregistered runs. A standalone E2 or E3 text block is used only if that is the registered qualifying choice. E4 contributes at most two blocks and E5 at most two, so if more than four addition blocks qualify, rank by their matched mean-period relative Brier gain, then fewer dimensions and experiment/arm order, and carry forward only the first four. Disclose this cap and every omitted qualifying block.

Maximum modeling budget: E1 9, E2 6, E3 9, E4 9, E5 9, E6 18, E7 6, E8 9 = **75 model/period fits**, excluding one baseline calculation per matched cohort and fixed calibration fits. Missing prerequisites reduce this count; never fill unused slots with new searches. A multi-block common-case control refit is included in these caps. E8 runs only if its temporal initial-fit gate is met. Equivalent cached artifacts may replace computations when hashes/memberships match, but reuse is recorded and is not a new trial. No candidate may be introduced because an evaluation table suggested it.

## 8. Exact additional feature specifications

**E1:** remaining time is continuous, with the linear stage interaction above. Do not add session indicators simultaneously: with fixed day180, calendar coordinates are strongly related. Retain age for exact legacy comparability, while acknowledging it is constant. Dates and Congress-end convention are already derivable; this does not certify disputed introductions. No new source acquisition is needed for records passing the existing audit.

**E2:** start with the twelve mechanisms in section 4. Policy vocabulary is learned from core-training evidence only, retaining labels with at least 20 core families and mapping remaining known labels to `other`; unknown is separate. Official labels unavailable by checkpoint are excluded, even if present now. Parser/extractor rules and any field omissions are frozen after E0, before E2 scoring. Retain the source spans and complete text alongside the encoded flags.

**E3:** use introduced text first. Unicode normalization, lowercasing, word unigrams/bigrams, minimum five core-training documents, maximum document frequency 0.95, maximum 10,000 features, TF-IDF fitted on core only and L2-normalized text vectors. Retain negation; no stemming or generic stopword removal. Mask the focal bill identifier and document status boilerplate with a frozen tested rule; retain substantive statute references and section language. Never fit the vocabulary or IDF on calibration/test text. Concatenate core-standardized structured columns with the L2-normalized TF-IDF block; do not center or variance-standardize sparse text columns. Penalize all slopes with the same specified coefficient and leave the intercept unpenalized. Use deterministic sparse L-BFGS for that objective, a 20,000-iteration cap and max absolute gradient ≤1e-6, without the gradient-descent minimum-step rule; verify against the low-dimensional solver on fixtures and rerun the E3 structured control through this solver for a matched comparison. This requires an audited research-only dependency path; do not silently densify large matrices or change penalty semantics. No search over vocabulary sizes or embeddings. These text-plus-structured scaling and penalty rules are fixed here; implementation hashes and numerical equivalence checks are locked before execution.

Preserve all as-of versions in storage. A later “introduced versus latest-available text” contrast is deferred to a new registration, rather than using final text or adding another E3 arm after inspecting scores. Modern pretrained embeddings/LLM-derived features are also deferred: historical training contamination must be separately assessed. An LLM explanation is not outcome truth and cannot replace the bill's language.

**E4 support block:** sponsor majority status, sponsor membership in a referred committee, sponsor chair/ranking role, log1p cosponsors, and share of known cosponsors outside sponsor party. Unknown denominator/affiliation is missing, not zero. Do not add raw sponsor IDs or lifetime success statistics. **Procedure block:** distinct referred committees, verified hearings/markups, originating-chamber passage indicator, and days since last audited action capped at 730. Full historical action coverage is required for zero counts; otherwise the value is unknown. Retain source-tier distinction from the legacy publication proxies. No vote or action after checkpoint enters a feature.

**E5 schedule block:** annual session indicator; count of officially announced focal-bill hearings/markups/floor events within 14 days after checkpoint; announced chamber sitting days in that window. Count only announcements already available by checkpoint. Absence of a scraped event is not proof of no scheduled event; require the registered coverage source, otherwise mark missing. Preserve revisions/cancellations as separate dated announcements. Do not use eventual sitting days, eventual vote schedules or a hindsight “must-pass” label. **Relationship block:** existence/count of companions and reintroductions known by checkpoint, with relationship type and provenance. No related bill's future outcome; family lineage used for leakage exclusion can contain later-discovered links, but those later links cannot become predictors.

**E7:** first test structured features only, using the exact same structured feature set and population for logistic and trees. Fixed boosted-tree specification: binary log loss, 100 boosting iterations, learning rate 0.05, max depth 3, max 8 leaves per tree, minimum leaf size 50, L2 leaf regularization 1, no early stopping, seed 20261108. Pin the implementation/version and validate its semantics before registration. Fit calibration on the same earlier calibration rows. If the selected E6 model requires text, retain it as context but make the primary E7 contrast between its structured-only logistic counterpart and structured-only trees; this is a separate matched representation comparison, not proof trees beat the text winner. Counts remain two arms per fold.

## 9. Missingness, availability and coverage comparisons

Distinguish an unavailable historic fact, a negative/zero fact and an extractor failure. All model arms in a contrast share a frozen population and missingness representation. Required identity, date, outcome coverage or core source failures block eligibility. Optional attributes may use a training-core median (numeric) or explicit unknown category with missingness indicators only if that policy is registered before scoring. Text missingness excludes the row from the matched text contrast; the overall deployment coverage report must still include it.

For every feature block report coverage by Congress, chamber, stage and known outcome after the data process is frozen. Coverage shifts can make a small clean subset deceptively easy. Report all exclusions and the base rate of the resulting subset; do not attribute a changed sample's lower Brier to better features.

Before E6, freeze the intersection of populations required by its selected blocks and rerun A and every E6 arm on that intersection. Gains from earlier subsets are not used as the E6 control. If common coverage or positive-family gates fail, block combination rather than impute unknowable historical content or select a favorable subset. A deployment fallback to A for missing optional blocks must be separately registered and scored on the full eligible population before claiming deployment performance; no silent per-case winner selection.

## 10. Learning curves and the meaning of self-learning

E8 holds the chosen encoding/model procedure fixed and compares training-window policies, not a changing feature search. For a test Congress c, only earlier Congresses with knowable labels qualify. The initial frozen anchor must be fitted from evidence available before the first test checkpoint and must not be refitted thereafter; reserve/purge all evaluation families from its training at registration. If that leaves inadequate evidence, E8 blocks. Expanding and two-Congress policies refit only at registered boundaries using earlier eligible labels. Each policy uses the same target cases per fold and a deterministic disjoint family calibration split. Unequal training counts are part of the intervention and must be reported.

For an additional data-quantity learning curve, a **separate future registration** would compare nested hash-selected training fractions on the same evaluation fold. It is not included in the 75-fit budget. More data across different evaluation periods is not itself a causal learning curve.

Operational learning loop: collect timestamped evidence → produce paired immutable forecasts → await audited outcomes → create versioned training addition → fit challenger under the fixed budget → check prior-only development performance and calibration → retain or nominate candidate → independently validate before promotion. New negatives become usable only after the defined horizon and complete evidence, not because a bill has not yet enacted. Early available positive labels alone must not create a biased update sample that omits pending negatives.

For the first adaptive deployment study, retraining cadence is once per completed and adjudicated Congress, not hourly or after every apparent success. More frequent source monitoring does not imply more frequent statistical retraining. Drift monitors report coverage, feature distributions and matured-outcome calibration; they do not automatically rewrite models or stop a registered test. A failed challenger leaves the champion unchanged. No reinforcement-learning reward derived from agent confidence or the system's own forecasts is permitted.

## 11. Independent validation, multiplicity and the 60% claim

V1's survivor and L2=0.05 candidate remain fixed. Richer features create a **different candidate** and must not be substituted into V1. The plan's default is to preserve V1 and prepare a separately named successor protocol only if development and evidence gates justify it. No successor experiment is active yet.

To use the proposed 120/121 boundaries, the successor protocol, all candidate/baseline artifacts, capture rules, analysis and exposure handling must be frozen before 2027-01-03 17:00 UTC. If readiness misses that deadline, register a later untouched whole-Congress boundary. Do not rush provenance or retroactively issue predictions. If V1 and a successor both use those periods, a custodian must control a single shared analysis plan with multiplicity across all confirmatory candidate/comparator claims; they cannot be advertised as independent replications. The default safe choice is no additional 120/121 confirmatory candidate without that joint preregistration. Adaptive models must not consume protected 120 outcomes while 121 predictions or rules remain open.

Independent success uses the existing 2% practical improvement criteria and provenance/event gates, or the successor's explicitly registered joint criteria; it is not conditioned on reaching 60%. To claim the 60% aspiration specifically, prespecify the additional contrast `Brier_model − 0.40 × Brier_rate` and a simultaneous interval/accounting rule before unlocking evaluation outcomes. A point BSS of 0.60 is not a confident population claim; report its interval, period signs, positive-event errors and coverage. Beating rate by 60% does not imply beating stage by 60%.

Publish results as: **blocked** (invalid/missing evidence), **negative** (registered comparison favors control or fails its practical claim under the defined interval rule), **inconclusive** (uncertainty, sparse events or inconsistent periods), **development lead** (all-fold exploratory gate), or **independently supported within the registered periods** (protected prospective requirements passed). These are distinct states. A stronger forecast model may still fail generalization, and a scientifically useful paper may report no improvement.

## 12. Operational execution and resource limits

Before each run: inspect Git changes, active jobs and the shared research lease; acquire a unique owner and renew at least every ten minutes. Use a new ignored run directory; retain raw source bytes and exact observation times. No overwrite of old runs. Existing recurring limits and schedules remain unchanged. New official acquisition is capped at 100 bill records per bounded audit cycle, sequential with retry/backoff; follow existing stricter source policies. Source counts are not forecast sample sizes.

E0 may reuse retained evidence before downloading. E1 uses existing audited dates and requires no paid provider. E2–E5 can proceed only after source coverage and storage/runtime preflight are documented; paid services and a dependency-installation budget are not presumed. For each modeling block record a six-hour maximum computation allocation, with an unambiguous checkpoint/blocked result at the cap; resume unchanged computations only under a documented extension before results are inspected. No search expansion in response to disappointing scores. Follow any lower active worker budget; these ceilings do not authorize bypassing it.

Separation of roles: evidence auditor assembles/source-checks; methods auditor reviews splits, targets and inference; implementer writes the experiment; independent verifier replays source/numerical checks; qualified human reviewers certify designated evidence; custodian controls protected outcomes. This plan does not spawn agents or assign humans. If executed with agents, agent verdicts remain machine reviews and cannot replace the latter two roles.

Every run retains: protocol and exposure registry; candidate/source/family/disposition manifests; parser and schema versions; all trial artifacts; training/core/calibration/evaluation IDs; predictions; labels in the appropriate access boundary; metrics; numerical verifier output; source/code hashes; resource usage; deviations; decision and next checkpoint. Public receipts contain appropriate summaries, not private chats, credentials, databases or raw runtime corpora. Commit meaningful code/documentation after diff review and relevant tests; push without force.

Verification must include timestamp normalization and boundary days, same-case pairing, missing/duplicate labels, family/exposure overlap, unavailable features, corrupted source bytes, Unicode/negation handling, deterministic selection, full-text/version preservation, calibration independence and numerical metric/model reproduction. Run focused tests for each implementation and the full regression suite when shared engine code changes. Tests validate software, not forecast efficacy.

## 13. Order of work and deliverable gates

| Order | Concrete deliverable | Exit condition | If blocked |
| --- | --- | --- | --- |
| 1 | E0 schema, source/feature dictionary and 100-case registration | Identity/version/source lineage fixed; reviewers and missingness rules defined | Build review packets; no fabricated approvals |
| 2, in parallel | E1 sealed 3-arm registration and calendar encoder | Exact fold membership, source eligibility and solver replay verified | Resolve original provenance; do not score via a bypass |
| 3 | E0 measurement report and accepted field list | Frozen quality check completed; rejected/sparse fields excluded from modeling | Preserve failed extraction; new version/sample requires new registration |
| 4 | E2/E3 categories and text experiments | All planned arms reported on matched data; no extra search | Retain A; keep full text for future work |
| 5 | E4/E5 support, procedure, schedule and relation experiments | Genuine dated source coverage and matched comparisons | Mark unavailable blocks, continue independent work |
| 6 | E6 common-population combination and ablations | All-fold lead gate and adequate common data | No combined candidate claimed |
| 7 | E7 flexibility and E8 updating diagnostics | Fixed comparisons completed or honestly blocked | Retain simpler/frozen procedure |
| 8 | One successor candidate and prospective registration package | Evidence/custody/issuance/analysis gates; no implicit V1 change | Use later prospective boundary, preserve all development findings |

No reliable calendar estimate exists for human/source completion; the sequence is dependency-based rather than a promise to validate within weeks. The current dated milestone is a **readiness decision before the existing January 2027 freeze boundary**, not a guaranteed launch. The protected 121 horizon does not close before January 2031; historic backtesting cannot shorten it by relabeling known outcomes.

Human decisions needed before corresponding execution: nominate qualified source/family annotators and an independent custodian; agree to the long prospective timetable or separately review another truly untouched design; approve any paid-service budget if later proposed. Routine schema, local tooling, source assembly and documentation work can proceed without repeated confirmation within authorized scope. This planning task executes no experiment, acquisition, training, forecasts or schedule change.

## 14. Grounding and limitations of external sources

- [GovInfo congressional bills documentation](https://www.govinfo.gov/help/bills) describes published bill versions and structured text access. It supports retaining versions and raw language; it does not certify that today's bytes or metadata were available at an earlier checkpoint.
- [Senate Daily Digest guidance](https://www.senate.gov/legislative/Congressional_Records/Daily_Digest.htm) describes reported activities and announced upcoming chamber/committee schedules. It motivates an announcement-vintage feature, not use of eventual schedules.
- [Nay (2017), Predicting and understanding law-making with word vectors and an ensemble model](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0176999) reports chronological congressional prediction using text and context. It motivates a component comparison; different target timing and datasets prevent transferring its performance to this project.
- [Han, Huang and Wang (2024), Model Assessment and Selection under Temporal Distribution Shift](https://proceedings.mlr.press/v235/han24b.html) studies assessment/selection in changing environments. It motivates explicit temporal assessment; its guarantees are not automatically guarantees for our family-dependent legislative data.

Sources checked November 8, 2026. The feature order, bounded grid, engineering thresholds and decision rules above are our proposed design choices, not findings attributed to these sources. Preserve the exact paper target and distinguish agent understanding, representation quality, numerical convergence, development skill and independent predictive validity throughout the programme.
