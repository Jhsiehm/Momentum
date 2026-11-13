# Originating-chamber passage within 90 days — protocol v1

Dated November 12, 2026 (America/New_York). **Local research specification and software foundation; prospective launch remains blocked. This is not an externally timestamped preregistration, a fitted model, a live forecast, or a completed predictive experiment.** Seal the final protocol, software, training manifests and artifacts with independent timestamp evidence before activating the proposed future cohort. A missed launch deadline requires a separately registered successor cohort, never a backdated forecast.

The target identifier is `originating_chamber_passage_within_90_days_at_day_30`. This study is distinct from both the [day-180 own-bill enactment paper](PAPER_PROTOCOL_V1.md) and the [day-30 passage-by-Congress-end benchmark](../SEQUENTIAL_BENCHMARK.md). Their forecasts, targets, evidence and gates remain unchanged.

## 1. Scientific question and lessons informing this version

Among H.R. and S. bills awaiting their first originating-chamber passage 30 days after introduction, does a frozen structured model improve probabilities of first passage during the following 90 days over a strong training-only stage/chamber/time-remaining reference?

The [November 11 matched context study](../operations/runs/20261111-action-context-resolution.md) found a 3.0398% relative Brier improvement over a simple two-column baseline but only 0.8253% over the stronger action-milestone reference, with descriptive uncertainty spanning no improvement. The reference is therefore a primary comparator, not an optional secondary plot. Those findings concern enactment and cannot be relabeled as passage evidence.

The preceding publication-completeness rule excluded all 333 current public-law assertion cases in its source sample. This study retains the full candidate inventory and every eligibility, source and label disposition. Missing stage is an explicit unknown category; no requirement for rich text, cosponsor totals or publication metadata may silently change the baseline/challenger population. Current official records and printed action dates do not prove historical availability. Existing source parser failures, negative transfer and repeated exposure findings remain part of the development record.

## 2. Population and exact probability

Bill identity is canonical `hr<number>-<congress>` or `s<number>-<congress>`, with positive integer bill number and matching type/Congress. Resolutions, other-chamber passage, amendment votes, repassage, and another vehicle carrying similar provisions are different outcomes.

For introduction instant `I`, the checkpoint is `C = I + 30 days` and the horizon is `H = C + 90 days`. The target is first originating-chamber passage in `(C, H]`, conditional on no such passage by `C`. Once first passage occurs, later repassage cannot restore risk-set eligibility. Neither enactment labels nor stage increments alone substitute for adjudicated first-passage labels.

Date-only introduction follows the repository convention of 23:59:59 UTC. Normalize timezone-bearing instants to UTC and retain subsecond precision; naive datetimes are invalid. A date-only passage on the checkpoint or horizon calendar day is conservatively uncertain until precision is adjudicated. Precise passage at `C` is already passed; precise passage at `H` is positive.

Require `H` strictly before `engine.store.congress_end(congress)`. Late-Congress introductions lacking a complete 90-day window are retained as `incomplete_90_day_window`, not counted negative, truncated to a different target, or carried into a reintroduced bill. This deliberately estimates a restricted population. Report every such exclusion by Congress and chamber.

The proposed prospective pilot is all eligible H.R./S. introductions in Congress 120 from its opening on January 3, 2027 at 17:00 UTC through June 30, 2027 at 23:59:59 UTC. Register the discovery/census rule before the opening boundary, reconcile missed discovery against the final inventory, and save one paired issue at each eligible day-30 checkpoint. Primary analysis is fixed for November 15, 2027, after the last scheduled horizon has matured. If required outcome adjudication is incomplete then, retain the blocked disposition; do not keep sampling or monitoring scores until a desired result appears. This one-Congress pilot cannot establish consistency across congressional periods.

## 3. Data contract and selection accounting

`engine.passage90.prepare(candidates, labels, as_of, mode)` accepts only `retrospective` development or `synthetic` mode. Neither mode can certify historical or prospective evidence. It emits one disposition per candidate, candidate/label hashes, raw inventory and per-disposition counts, and eligible rows. Duplicate candidate identities, duplicate labels and labels outside the inventory are fatal input errors. An empty inventory is not evidence of successful collection.

Candidates contain bill identity/type/Congress, `introduced_at`, `family_id`, checkpoint `stage` (`introduced`, `reported`, or `unknown`), and optional `feature_available_at`. The output states whether availability is asserted by the checkpoint; this assertion is never source certification. Retrospective rows may retain current-rendition proxies explicitly identified as such. Do not pass these rows off as historically available predictors for independent evaluation.

Each adjudicated label contains the exact target, integer `value` 0 or 1, `first_passage_at` (null is permitted for an explicitly reviewed negative), `first_passage_verified: true`, `complete_coverage: true`, `coverage_from`, `coverage_through`, `available_at`, an HTTPS source URL, exact source SHA-256 and a readable audit note. These fields are operator assertions: a true Boolean and valid hash syntax do not independently establish source completeness or reviewer competence.

Coverage must begin no later than introduction. For a positive, it must include the adjudicated first passage, which must be in the window. A negative requires complete action-history coverage through `H`, with no first passage in `(C, H]`; a later first passage may support a negative only when the earlier history is explicitly complete. Label availability cannot precede covered history. Labels unavailable at the audit date and immature horizons remain pending. Missing, inconsistent, unsupported and boundary-ambiguous cases retain their own dispositions. Absence from a partial API response never creates a negative.

Freeze inventory membership before examining label frequencies. Report introductions, full-window cases, already-passed cases, unknown features, source failures, family exclusions, missing or pending labels, boundary uncertainty, late or missing predictions and scored cases. Report positive/negative counts only with the precise population and provenance level. An event count from a current-source feasibility pilot is not certified training-label coverage.

## 4. Development and family separation

Existing Congresses 113–118 are exposed development. The initial intended structured development uses 113–116 training and 117–118 forward evaluation, subject to source and label readiness. No claims of untouched historical validation follow from new bill IDs in those periods.

At each fold opening, use only earlier-Congress rows with label effective and available instants no later than that opening. `chronological_split` reserves current and future evaluation families before choosing one deterministic training representative per family. It emits every training exclusion. Do not use future family links as predictors; their restricted role is conservative contamination screening, with discovery/exposure recorded. Family review must cover companions, reintroductions and out-of-sample intermediaries. Heuristic family IDs do not certify complete genealogy.

The actual baseline and challenger must share training eligibility, checkpoint evidence and the identical evaluation cases. All preprocessing is training-only. The legacy frozen enactment artifacts are inapplicable to this outcome. The current implementation supplies no trained passage challenger; fitting it requires a separately sealed finite-fit execution manifest specifying reviewed training rows, feature definitions, optimizer, regularization, calibration, fit count, versions and hashes. No exploratory fit is authorized merely by an unused budget in an older experiment.

## 5. Strong reference and incremental model stages

The global rate is Beta(1,1): `(training positives + 1)/(training families + 2)`. For each chamber and checkpoint stage, shrink to the global rate with five prior observations: `(cell positives + 5 * global rate)/(cell n + 5)`. Split each stage/chamber cell by time remaining after the checkpoint: more than 90 and at most 365 days, or more than 365 days. Shrink each such cell with five observations at its parent stage/chamber rate. Empty time cells inherit the parent; empty stage/chamber cells inherit the global rate. These boundaries, missing-stage handling and smoothing counts are fixed, not selected on evaluation outcomes.

`fit_reference` requires nonempty training with both outcome classes and one representative per family. It binds source rows, identities, families, evidence mode, latest label availability/effective time and training Congress to the artifact hash. `predict_reference` rejects artifact alteration, mixed synthetic/real modes, overlapping families and same/future-Congress training or labels unavailable at fold opening. These are computation safeguards, not statistical sufficiency or historical-source certification.

The first challenger is structured information beyond the reference, with its exact feature/fit manifest sealed before fitting. An added bill-text arm is a later separately registered comparison on the same cases, admitted only after representation/extraction quality and source availability have been evaluated. Every extra model comparison must declare its exposure and multiplicity; text does not inherit a success claim from the structured arm.

## 6. Measurements and practical success

The primary practical hypothesis is at least 2% relative Brier improvement over the strong reference. For period `c`, define `D_c = Brier_challenger,c - 0.98 * Brier_reference,c`. If more than one evaluation period is registered, the primary aggregate equally weights period losses. Report the ordinary difference separately. A confidence interval for `model - reference` below zero does not itself establish the 2% practical threshold.

Brier is mean `(probability - outcome)^2`. Log loss is mean binary negative log likelihood, clipping only for its logarithms at `[1e-15, 1-1e-15]`. Brier skill is `1 - mean_period_model_loss / mean_period_reference_loss`; it is undefined when reference loss is zero. Report raw denominators, events, expected events, positive- and negative-class counts/Brier, each period's results and all ten fixed decile reliability bins, including empty bins. Also report pooled bill-weighted metrics as secondary diagnostics; they must not replace the equal-period primary aggregate. An absent class has undefined class-specific Brier, not zero error.

For prioritization, rank the top 20 cases per evaluation period by probability, breaking ties by canonical bill identity. Report the actual number selected, hits, precision (hits/selected), recall (hits/all events) and lift (precision/period event rate). Recall and lift are undefined when there are no events. The pooled secondary view additionally reports top 20 across all supplied periods, explicitly distinct from the period-level lists. These are fixed-cohort diagnostics, not a weekly operational workload claim. A later weekly service needs separate registration and repeated-bill dependence handling.

`evaluate_paired` requires each model to have exactly one finite `[0,1]` probability for every supplied case, with matching target and checkpoint. It rejects missing, extra, duplicate, mismatched and nonfinite outputs. It returns per-period, equal-period and pooled summaries; an all-one-class evaluation is explicitly inconclusive. The recorded `evaluation_as_of` defaults to the actual current UTC time. For retrospective real rows, an explicit evaluation cutoff cannot exceed the actual clock, and every horizon and label effective/available instant must be no later than that cutoff. Synthetic tests may explicitly use future fixture cutoffs without granting real-evidence eligibility. Its coverage guarantee applies to the supplied rows, so the complete preparation inventory must accompany any report.

The descriptive paired bootstrap uses 10,000 draws with seed 20261112, resampling global family IDs with all member bills and periods carried together. Draws missing a registered period are invalid. Report valid/invalid counts and linearly interpolated 2.5th/97.5th percentiles for both ordinary and practical contrasts. At least 9,000 valid draws are required before interpreting a registered interval. The one primary reference comparison requires no multi-comparator correction; additional primary claims need a new multiplicity specification before exposure.

Conditional pilot success additionally requires all source/family/issuance/custody gates, complete disposition reporting, paired predictions for the entire registered eligible population, adjudicated outcomes for every scored candidate with prespecified missing-outcome sensitivity, both classes, upper 95% practical-contrast bound below zero, lower point Brier in each registered period, and no worse log loss in each period. No complete-case success may be claimed while unresolved eligible outcomes remain. No fixed positive-event count is presented as a power calculation; feasibility and a simulation-based design assessment must precede launch, and sparse evidence can remain inconclusive. Do not extend the cohort based on observed scores or event counts.

The current evaluator always returns `independent_success: false` and `release_eligible: false`. It has no custodian or source-certification adapter and therefore can produce descriptive development diagnostics only. Its family interval conditions on the observed periods and fixed artifacts and omits source error, training/model selection and future political-period uncertainty. The proposed single-Congress pilot cannot justify a general cross-Congress claim.

## 7. Prospective launch and evidence gates

Before launch, establish reviewed time-correct training labels, a reviewed family/exposure manifest, frozen passage-specific challenger/reference artifacts, independent source/family review, a complete inventory/discovery route, independently verifiable timestamp evidence, and an outcome-custody/access arrangement. Record developer awareness of public outcomes; local directories and flags are not access controls.

Capture exact source bytes, request/response metadata, actual observed times, source identity and hash before the checkpoint. Issuance must atomically bind the registration, bill/window, all paired probabilities, input snapshot, source/model/code hashes, actual issue time and predecessor receipt. The scheduled issue tolerance is 60 seconds after the checkpoint, and the bill must still be at risk at issue. A late capture, unavailable evidence, missed issue or already-passed bill gets an immutable failure disposition; it never becomes a retrospectively reconstructed live forecast.

Local observation receipts are useful engineering evidence but do not satisfy independent attestation. Current collection cannot retroactively authenticate old feature bytes. If audited historical training remains unavailable, a newly collected cohort must mature as development/training before a later untouched evaluation cohort can begin. The first possible matured day-30/90-day outcome is 120 days after introduction, not 90 days after starting setup.

## 8. Execution, review and preservation

Use independent agent review to challenge contracts and reproduce guard failures, with valid controls, before any live registration. Agent review is not independent qualified human certification. Exercise actual CLI/service/persistence boundaries in isolated data and temporarily disable critical guards in disposable copies to verify test sensitivity. Explicit production validation must survive optimized Python (`-O`).

Retain current and failed versions, registrations, all source dispositions, immutable predictions, code/artifact hashes, reproducible commands and per-case results under the repository workflow. Runtime bytes and private data remain in ignored `data/`. Update the development log and a complete operational receipt for each execution batch, including failures and unimplemented gates. Do not infer predictive value from passing tests, source download coverage or parser agreement.

Validation commands for the new research primitives:

```sh
python3 -m unittest tests.test_passage90 -v
python3 -O -m unittest tests.test_passage90 -v
```

No model fitting, real probability scoring or prospective issuance is recorded by this protocol document. See the separate execution receipt for what actually ran.
