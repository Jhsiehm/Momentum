# Legislative Forecasting Engine
## Research, backtesting, data, and product plan

**Revision:** 2 — integrated research and implementation specification, October 24, 2026

**Status:** Working plan; product name intentionally undecided; no model performance has yet been established  
**Purpose:** Build a transparent, historically tested system that estimates how U.S. federal legislation is likely to move through Congress and become law, based only on evidence available at each forecast date.

---

## 1. Product thesis

This is a legislative forecasting and research system, not a bill-status page with a decorative probability badge. It should answer four questions for every tracked bill:

1. **What is likely to happen next?**
2. **What is the probability of reaching each legislative milestone, and by when?**
3. **What changed in the evidence or political environment to move that estimate?**
4. **Which past bills provide useful comparisons, and where do the comparisons break down?**

Its defining product feature should be a point-in-time replay: select a historical bill and date, reconstruct the information available then, and see the forecast the system could have made at that moment. Historical replay is the development and audit interface. It demonstrates reconstructed forecasts, not proof that a modern AI had no prior knowledge of outcomes; prospective evaluation is required for the complete AI system.

The core statistical object is a set of calibrated, time-stamped probabilities for clearly defined outcomes. “Momentum” is a set of observed changes in the bill’s conditions and trajectory; it is not a substitute for the probability forecast. A bill can receive more attention while still facing a low probability of passage.

The system has three connected jobs: **recognize a policy development**, **identify the relevant bill or legislative vehicle**, and **forecast what that bill is likely to do**. Keep these as separate, testable tasks. Correctly spotting a policy story does not by itself prove the passage forecast is accurate.

For each forecast, provide a historical reference class: what happened to earlier bills with a similar topic, stage, procedural route, sponsor/committee context, action history, and—when already observed—vote pattern or result. Display the underlying sample size and observed outcomes. The AI can retrieve and explain those records; the baseline statistical model estimates the probability, with AI and combined forecasters evaluated as separate challengers in Section 6.

---

## 2. Scope and forecasting targets

### 2.1 Initial universe

Start with public U.S. House and Senate bills (H.R. and S.) and, after the bill-history pipeline is stable, add joint resolutions when the target outcome is well defined. Keep simple and concurrent resolutions out of the initial “becomes law” target because their constitutional and procedural purposes differ. Store each measure and its companion or related versions, but do not count companion bills as independent successes when evaluating bill families.

Separate the universe into meaningful types:

- Regular public bills
- Appropriations and continuing resolutions
- Reconciliation measures
- Reauthorization bills
- Joint resolutions with lawmaking effect
- Omnibus or packaged measures, when identifiable

Do not force one model to treat these procedurally different objects as interchangeable. Begin with a core public-bill model, then add specialized cohorts when there is enough data to validate them.

### 2.2 Outcomes and horizons

Forecast multiple outcomes, each with its own definition and deadline:

| Forecast | Suggested operational definition |
|---|---|
| Committee advancement | Reported or otherwise formally advanced from the relevant committee, with bypass routes recorded separately |
| Chamber passage | Passed the originating chamber by the specified horizon |
| Bicameral passage | Both chambers passed the same legislative text or an agreed version by the specified horizon |
| Enactment | Became public law by the end of the Congress |
| Next action | Probability and expected time to the next material legislative event |

Use fixed horizons such as 30, 90, and 180 days where suitable, plus “by the end of this Congress.” A bill may be enacted through a route that skips the ordinary sequence, so do not calculate final passage by mechanically multiplying independent stage probabilities. Model the observed procedural pathways and their alternatives.

Treat enactment as the primary headline forecast, but keep intermediate stage forecasts visible. At each stage, competing outcomes can include advancement, continued inactivity, withdrawal, expiration at adjournment, or another route. A “no action yet” observation is not a failure until the chosen horizon or Congress ends.

### 2.3 The forecast record

Every stored forecast should be reproducible and include:

- Bill identifier and bill-family identifier
- Outcome definition and horizon
- Forecast timestamp and as-of cutoff
- Data snapshot and feature versions
- Model, code, prompt, and calibration versions
- Probability, uncertainty method and interval when justified, and calibration cohort
- Evidence items with source, publication/event time, retrieval time, and provenance
- Actual resolution and resolution date, added only after the forecast is locked

---

## 3. Data foundation and honest coverage

A 50-plus-year record is feasible for important bill metadata and outcomes, but the historic record is not uniformly complete. The plan must label what is available for each period rather than imply that every bill has modern-quality text, committee events, news coverage, or machine-readable timestamps.

### 3.1 Primary sources and coverage strategy

| Source | Use | Coverage / caveat |
|---|---|---|
| [Congress.gov API](https://api.congress.gov/) | Current bill metadata, actions, sponsors, cosponsors, committees, related bills, amendments, summaries, and available votes | Official Library of Congress API; collection coverage varies by era and endpoint. Record endpoint-specific coverage and missingness. |
| [GovInfo Congressional Bills](https://www.govinfo.gov/help/bills) | Published bill text versions and related bill documents | Published bill texts start with the 103rd Congress (1993–94). Useful for the text-model era. |
| [GovInfo Bill Status](https://www.govinfo.gov/developers) | Bulk bill-status XML and action histories | Bulk status packages begin with the 108th Congress (2003–04), according to GovInfo’s developer materials. |
| [Congressional Bills Project / Policy Agendas Project](https://www.comparativeagendas.net/project/us/datasets) | Long-run bill records, policy topics, sponsor and progress information | Useful for extending historical metadata back to 1947; codebook and available years must be checked before ingestion. |
| [Voteview](https://voteview.com/data) | Historical roll-call votes, member voting records, and ideology estimates | Roll-call records extend far earlier than the core bill-status period. Measures derived from votes must be time-appropriate; never use future votes to characterize a member at an earlier forecast date. |
| [Center for Effective Lawmaking](https://thelawmakers.org/data-download) | Member-level legislative effectiveness and related historical measures | Useful as contextual data from 1973 onward; completed-Congress effectiveness scores must be lagged to avoid using future accomplishments. It is an aggregate member measure, not a bill’s passage probability. |
| [FRED API](https://fred.stlouisfed.org/docs/api/fred/) and [ALFRED](https://alfred.stlouisfed.org/) | Macroeconomic context and point-in-time data vintages | Use the vintage available on the forecast date, not today’s revised historical series. |

**Recommended coverage bands**

- **1947–1972:** long-run metadata and outcome patterns where the Congressional Bills Project supports them; limited modern-style bill text and event granularity.
- **1973–1992:** core bill status and contextual modeling; text features only where reliable historical text is available.
- **1993–2002:** add published bill texts and version-aware text features.
- **2003–present:** richest structured bill-status and text coverage, still subject to endpoint-specific gaps and changes in procedure.

The core production model should begin with **1973 onward**, while earlier records support long-run priors, historical comparisons, and sensitivity analyses. The 50-year claim should refer to the historical learning and replay span, not uniform feature completeness.

### 3.2 Events, news, public sentiment, and financial data

Treat news, speeches, polling, social activity, and financial data as optional, dated context layers. Their usefulness should be established through out-of-time feature ablation.

For every item, preserve at least:

- What happened or was said
- Publication, event, observation, and retrieval timestamps when available
- Original source and link
- Geographic, policy, and bill relevance
- Whether the item is primary evidence, reporting, opinion, polling, or social content
- Extraction method and confidence

Do not create a single “public sentiment” score from mixed sources. Public opinion, elite rhetoric, media attention, sponsor statements, committee activity, and market prices represent different phenomena. Model them separately. Do not treat social media volume as national opinion. Market conditions may reflect the same news as legislative action, so a predictive association is not evidence that markets caused the bill’s progress.

For historical replay, include these features only where an actual contemporaneous archive exists and its timestamps can be defended. A modern language model’s recollection of a historic event is not a historical source.

### 3.3 Data engineering requirements

Build a versioned canonical data layer with:

- Stable IDs for bills, bill families, people, committees, Congresses, actions, and documents
- Raw source snapshots retained unchanged
- Normalized event records with source-specific fields preserved
- Effective time (when an action occurred) and observed time (when the system could have known it)
- Explicit “unknown,” “not collected,” and “not applicable” values
- Deduplication and links among companion, successor, amended, and incorporated measures
- Data-quality checks for chronology, missing stages, conflicting actions, and final outcomes
- A coverage report by Congress, chamber, bill type, feature, and source

Never convert “no recorded event” into “event did not happen” unless the source’s coverage supports that inference.

### 3.4 Rate limits, bulk ingestion, and spreadsheets

**Do not hand-build one giant spreadsheet with a row and many manual annotations for every bill.** The historical corpus already contains hundreds of thousands of bills; adding a row for every bill-date snapshot, event, text version, and evidence item would make one workbook fragile, hard to audit, and poorly suited to incremental updates. The spreadsheet would become a manually maintained shadow database.

Use the official API for targeted lookups, gap filling, and incremental refreshes. The [Congress.gov API repository](https://github.com/LibraryOfCongress/api.congress.gov) currently documents a limit of 5,000 requests per hour, with up to 250 results per list request; check rate-limit headers and current documentation during implementation because limits can change. More importantly, GovInfo publishes [bulk Congressional Bills](https://www.govinfo.gov/bulkdata/BILLS) and [Bill Status XML](https://www.govinfo.gov/bulkdata/BILLSTATUS) repositories, and official bulk packages should be the first route for large backfills where coverage fits. The API is not a reason to manually re-enter the records.

Recommended ingestion pattern:

1. **Bulk backfill:** download available GovInfo XML/bulk packages and compatible historical project datasets by Congress; preserve original files and source metadata.
2. **Incremental sync:** query Congress.gov for new or recently changed records, using pagination, a durable cursor/watermark, caching, and conditional retries. Honor `Retry-After` or rate-limit headers; on 429 or transient errors, use exponential backoff with jitter. Do not repeat successful requests unnecessarily.
3. **Normalize once:** parse raw XML/JSON into normalized tables or Parquet files, keyed by bill, bill family, actor, committee, action, document version, and forecast snapshot. Keep raw payloads so parser improvements can be replayed.
4. **Review exceptions:** route missing, contradictory, low-confidence, and historically important cases into a small human-review queue.
5. **Rebuild reproducibly:** make each import and annotation job idempotent, logged, versioned, and restartable. A failed batch should resume from its last verified checkpoint.

Use DuckDB plus Parquet for a low-cost research prototype, or PostgreSQL when concurrent users and live updates become important. Keep workbook exports as review tools, not the authoritative store.

**Where spreadsheets help:** define the codebook, taxonomy, allowed labels, annotation instructions, adjudication rules, and QA sample. A review sheet can contain a stratified sample of bills with source links, the model’s proposed tags, reviewer decisions, disagreements, and adjudication notes. For broad manual labeling, begin with a pilot sample across eras, chambers, bill types, stages, and outcomes; estimate reviewer agreement and time per record before scaling. Use targeted sampling or active learning to review ambiguous cases rather than manually annotating every measure.

For AI-assisted mass annotation, store model-generated labels and human-verified labels as separate fields. Record document hash, model/prompt version, extracted source span, confidence, and reviewer status. Evaluate each label type against a human-coded sample before feeding it into the probability model. High-impact variables such as bill outcome and official committee action should come from official event records or be manually adjudicated when those records conflict—not inferred solely by an LLM.

---

### 3.5 Context data: economic pressure, public preferences, and institutional response

Treat the following as candidate predictive mechanisms, not established causal effects. Bad economic conditions near an election could encourage agreement, symbolic activity, or obstruction. Estimate effects separately for introduction, committee activity, floor passage, and enactment. A macro variable must be relevant to the bill’s policy mechanism; avoid applying an identical “crisis boost” to every bill.

| Evidence family | Primary sources | Candidate features | Historical controls |
|---|---|---|---|
| National economic conditions | FRED/ALFRED; original BLS and BEA releases | Unemployment, claims, payroll changes, inflation, real earnings, GDP growth; levels and trailing changes | Vintage and original release availability, not observation period alone; series-specific coverage audit |
| Credit conditions | Federal Reserve Senior Loan Officer Opinion Survey; eligible FRED credit series | Tightening lending standards, demand for credit, credit spreads, borrowing costs | Retain question definitions, release lags, and changes in series methodology |
| Local economic exposure | BLS Local Area Unemployment Statistics; later audited sector employment and income sources | State labor-market deterioration, exposure to affected sectors, national/local divergence | Geography valid at cutoff; vintage availability; no present-day district boundary joins to old districts |
| Economic perceptions | University of Michigan Surveys of Consumers | Sentiment, expectations, recent deterioration | Preliminary/final release distinction; method changes; not direct policy support |
| Policy preferences and political attitudes | Roper/iPoll; ANES; original poll releases | Issue support, salience, approval, trust, economic concerns | Exact question and population; fieldwork and publication dates; survey weights; archive availability is not contemporary availability |
| Electoral incentives | MIT Election Lab; House Clerk election statistics; official calendars | Days to election, previous margin, reelection status, prior party control | No eventual future election results or retrospective competitiveness labels |
| Institutional attention | Congress.gov, GovInfo, Comparative Agendas Project, audited CoCoHD hearing records | Relevant hearings, scheduled markups, leadership positions, cross-chamber action | Hearing event, announcement, transcript publication, and retrieval dates are distinct |
| Fiscal and procedural feasibility | CBO cost estimates; official committee reports and procedural records | Published cost, offsets, fiscal exposure, legislative route, deadlines | Cost estimate availability partly reflects stage; missing estimate is not zero cost |
| Coalition and voting context | Official roll calls; Voteview | Previous voting alignment, bipartisan coalition composition, committee support | Estimate from votes already observed; avoid full-career or full-Congress scores in earlier snapshots |
| Broader context, later extensions | Audited official statements, lobbying disclosures, news archives, disaster/sector statistics | Named actor support/opposition, issue attention, filing-based activity, relevant shocks | Source and commercial-use audit; reporting lags; deduplication; not a generic sentiment composite |

**Source URLs and concrete coverage anchors**

- [ALFRED real-time periods](https://fred.stlouisfed.org/docs/api/fred/realtime_period.html) and [observations API](https://fred.stlouisfed.org/docs/api/fred/series_observations.html): explicitly set the as-of vintage; defaults refer to today. FRED hosts series from many producers, not only Federal Reserve measurements.
- [Fed lending survey](https://www.federalreserve.gov/data/sloos.htm): survey questions and coverage vary; inspect each chosen series.
- [BLS LAUS](https://www.bls.gov/lau/) and [state history](https://www.bls.gov/web/laus/lauhsthl.htm): published state unemployment series begin January 1976; this does not guarantee complete first-release vintages back to that date.
- [Michigan tables](https://www.sca.isr.umich.edu/tables.html) and [reports](https://www.sca.isr.umich.edu/reports.html): distinguish economic perceptions from support for a proposed policy.
- [Roper collections](https://ropercenter.cornell.edu/data-highlights/featured-collections): historical polling; verify access, redistribution, and commercial licensing.
- [ANES cumulative file](https://electionstudies.org/data-center/anes-time-series-cumulative-data-file/): recurring questions since 1948, harmonized with a dedicated codebook; not a daily signal or automatically contemporaneously public data.
- [MIT House returns](https://doi.org/10.7910/DVN/IG0UN2) and [House Clerk election statistics](https://history.house.gov/Institution/Election-Statistics/): previous electoral results; track redistricting and special elections.
- [Comparative Agendas datasets](https://www.comparativeagendas.net/project/us/datasets): topic-coded attention across institutions; latest hearing year may be incomplete.
- [CoCoHD paper](https://arxiv.org/abs/2410.03099): reports hearings from 1997–2024; audit raw records before production use.
- [CBO estimates](https://www.cbo.gov/cost-estimates) and [process](https://www.cbo.gov/about/our-processes): fiscal evidence and its publication timing.

### 3.6 Feature registry and information-time contract

Maintain a machine-readable registry before adding a source to forecasts. Each feature needs: definition and units; source; geography; policy relevance; coverage years; update frequency; release lag; revision policy; missingness semantics; transformation; permitted forecast cutoffs; provenance; licensing; quality checks; and owner/review status.

Each evidence record stores `event_at`, `first_public_at`, `retrieved_at`, `version_available_at`, document hash, source URL, and extraction spans. A later retrieval can support a historical reconstruction only if contemporary availability is documented. Maintain a separate ingestion-latency measure for actual live operations. Where intraday ordering cannot be established, apply a conservative lag or mark the feature ineligible.

Do not use a recession label retrospectively assigned after the cutoff as an observable crisis indicator. Use contemporary stress measurements or an explicitly dated announcement. Do not standardize features using the full historical dataset: fit scaling, imputation, topic vocabularies, similarity weights, and feature selection within each training window.

**Data release tiers:** (A) validated point-in-time structured backbone; (B) richer historical features with demonstrated availability; (C) modern-only features. Missing older features remain missing, not zero. Publish which tier supplied each forecast. Compare full-history, recent-window, and recency-weighted fits; 50 years of history does not require equal weight for every year.

### 3.7 Prespecified pressure hypotheses

Begin with a short registry, recording expected direction as uncertain where appropriate:

| Hypothesis | Outcomes to test | Required comparisons |
|---|---|---|
| Labor deterioration increases movement of relevant relief bills | Hearing, passage, enactment separately | Same stage/topic/horizon, plus session and party context |
| Election proximity changes responses to distress | Same outcomes; time to action | Election proximity × distress × policy relevance; distinguish session-end pressure |
| Local exposure changes sponsor/coalition behavior | Cosponsorship and advancement | Affected versus less-affected places using valid historical geography |
| Public support adds information beyond economic conditions | Passage and enactment | Poll availability and topic match; compare against macro-only model |
| Committee attention adds information beyond media attention | Committee and floor transitions | Source-specific attention with fixed windows and denominators |

Do not search unlimited combinations and report only winners. Use regularization/partial pooling, log every attempted specification, and validate interaction terms on later periods. Thousands of bills exposed to one crisis are not thousands of independent crises. Include leave-one-crisis-period-out sensitivity analyses without treating them as substitutes for forward validation.

---

## 4. Historical replay and backtest protocol

### 4.1 Point-in-time reconstruction

For each bill, generate forecast snapshots at meaningful points:

- Introduction
- Committee referral
- Addition of notable cosponsors
- Hearing announcement or hearing
- Markup
- Committee report
- Scheduling or rules action
- First-chamber passage
- Second-chamber action
- Conference, reconciliation, or other final route

Also create regular calendar snapshots—such as weekly—so the test includes bills that receive no discrete event for long periods.

At cutoff time (t), the feature set must contain only information that was publicly available to the system by (t). Distinguish event date from publication/retrieval date. If a record is backfilled later, do not expose it to an earlier replay unless it was demonstrably available then.

Freeze the forecast before revealing its outcome. Store immutable model/data versions and write a replay audit that lists all input records available at the cutoff.

### 4.2 Rolling-origin evaluation

Use forward-in-time evaluation, not random train/test splits:

1. Train on prior Congresses.
2. Forecast the next Congress or next set of sessions using point-in-time snapshots.
3. Advance the training window and repeat.
4. Reserve the latest completed Congresses for a final untouched holdout.
5. Repeat results by chamber, bill type, policy area, stage, and historical era.

Split or cluster companion and near-duplicate bill families so their shared outcome does not create misleadingly easy evaluation. Historical analogs may include genuinely earlier related bills, because that information was available at the time; same-session duplicate measures should be handled as linked cases.

Build separate tests at each stage. The information available at introduction is much thinner than the information available after a hearing or first-chamber passage. Report the forecast’s performance by cutoff stage and horizon.

### 4.3 Baselines and metrics

Every advanced model must beat transparent baselines:

- Overall and historical Congress-level base-rate models estimated only from resolved outcomes available at training time; never the test Congress’s eventual enactment rate
- Base rate conditional on chamber, bill type, issue, stage, and time remaining
- Regularized logistic regression using structured political and procedural features
- Historical analog model using only prior comparable bills
- Sponsor/committee context-only model
- Text-only model where text coverage is adequate

Evaluate probability forecasts with:

- Brier score and log loss
- Reliability diagrams, calibration intercept, and calibration slope
- Precision-recall and ROC curves as secondary ranking diagnostics
- Top-k lift for research prioritization, clearly separate from probability calibration
- Survival/time-to-event calibration and integrated Brier score for timing forecasts
- Confidence intervals clustered or bootstrapped by Congress and bill family

Do not announce one universal accuracy number. A Brier score depends on the outcome’s base rate; compare against relevant baselines and show the score by forecast cohort. Report calibration uncertainty for sparse subgroups and suppress or aggregate cells with too few resolved examples.

### 4.4 Release gates

A model is eligible for customer-facing performance claims only when it:

- For promotion beyond the baseline, beats the appropriate historical and structured-feature baselines in untouched forward tests
- Remains reasonably calibrated across multiple Congresses, not just one favorable session
- Shows no critical calibration collapse by chamber, bill type, forecast stage, or major era
- Passes automated leakage tests and manual replay audits
- Produces a material incremental improvement when new feature families are added
- Has documented limitations, data coverage, and reproducible code/model versions

Set numerical thresholds after the data audit and baseline run; choosing targets before measuring the base rates would create arbitrary pass marks.

### 4.5 Project success criteria

Define success at three levels so that a compelling demonstration does not get mistaken for proof of general forecasting skill.

**Level 1 — End-to-end historical demonstration.** Select a recent, consequential policy event and the bill or bills associated with it. For several cutoff dates before the relevant outcome, reconstruct only information available by that date; identify the event and its legislative vehicle; show the reference-class rates and model probability; then reveal what happened. The replay must include evidence links, the analog sample size, and an audit of information timing. This proves the product can perform the complete workflow on a real case.

**Level 2 — Historical evidence of predictive signal.** Lock the inclusion rules and model design, then score all eligible bills in multiple later Congresses that were not used to fit that forecast. Include bills that pass, fail, stall, or take unusual routes. Compare the model with overall and conditional historical rates, structured political/procedural baselines, and the reference-class-only estimate. Report calibration and proper scores by stage, topic, bill type, horizon, and Congress. A result counts as promising when the model improves on suitable baselines across multiple forward periods, with uncertainty reported; do not make a general performance claim from a handful of selected successful bills.

**Level 3 — Prospective shadow performance.** Before making public reliability claims, log live forecasts with immutable timestamps and evaluate them only after outcomes resolve. Report missed events, calibration drift, source delays, and subgroup performance as well as successful predictions.

Dozens of cases are useful for debugging and an initial signal check. Enactment is a rare outcome, so credible calibration requires the full eligible cohort across multiple Congresses and enough resolved cases to quantify uncertainty. Keep the demo case separate from the final holdout whenever possible.

---

### 4.6 AI contamination and three separate evaluation tracks

A closed evidence packet restricts external information, not knowledge already encoded in model weights. Prompts instructing a model to act in a historical year, disabled networking, Docker, and masked names cannot establish the absence of future knowledge. Embeddings, retrieval rankings, fine-tuning data, and outcome-informed question selection can also leak information.

Report three tracks separately:

1. **Structured historical backtest:** fit statistical models and preprocessing only on earlier eligible information. Use audited dated features and transparent text baselines.
2. **AI-assisted retrospective experiment:** evaluate extraction or forecasts using modern models, explicitly labeling residual pretraining contamination. Use identity/date masking, evidence-only extraction, and unsupported-outcome probes as diagnostics, not proof of cleanliness. Explore chronologically restricted models only where appropriate checkpoints and training provenance exist.
3. **Prospective ledger:** record the complete system’s predictions before outcomes occur. This is the decisive test of the deployed AI forecasting pipeline.

Select evaluation bills using eligibility rules fixed without inspecting outcomes. Include inactive and failed measures. Prefer archived source contents over modern date-filtered web search. Check revisions, delayed transcripts, and documents that summarize later events despite an earlier page date.

### 4.7 Locked evaluation, dependence, and uncertainty

- Separate fitting, model selection, calibration, and final testing chronologically. At every training origin, labels must already be resolved or handled through a prespecified censoring method.
- Keep repeated snapshots from a bill within their appropriate time partition and account for their dependence. Link companions, reintroductions, and shared legislative vehicles. Earlier related bills can be legitimate predictors; report family-sensitive robustness checks rather than deleting all historical relationships.
- Fix snapshot sampling and weighting before evaluation. Report results by bill as well as snapshot so heavily covered bills cannot dominate the score.
- Protect final labels, scoring code, and holdout access from the agent conducting model experiments. Log all trials, errors, retries, exclusions, and configuration changes.
- Compare scores on identical cases and information cutoffs. Estimate paired differences with uncertainty respecting bill families and shared legislative periods. With few Congresses or crises, disclose limited effective sample size; do not claim precise confidence from naive row resampling.
- Calibration alone is insufficient: a constant base rate can look calibrated while offering little discrimination. Report proper scores, baseline-relative skill, calibration, ranking usefulness, and coverage together.
- Pending cases are not failures. For simple fixed-horizon rates use mature, resolved cohorts; for incomplete follow-up use an appropriate validated survival approach. Separate a bill’s enactment from incorporation of its provisions into another vehicle.
- Prespecify whether subgroup checks are exploratory or confirmatory. Do not repeatedly reuse an opened holdout as an untouched test.

**Uncertainty contract:** every interval must state its estimand, method, assumptions, and validation. Parameter uncertainty, disagreement between models, sensitivity to assumptions, and reference-class sampling error are not interchangeable. A conformal prediction set for a binary outcome is not a confidence interval for its true enactment probability. Temporal dependence and distribution shift require explicit treatment; never advertise unconditional guarantees.

**Probability consistency checks:** probabilities lie in [0,1]; mutually exclusive exhaustive outcomes sum to one where defined; longer-horizon cumulative event probabilities do not decrease for the same evidence snapshot. Enforce implication constraints only for genuinely nested outcomes. Committee reporting is not universally necessary for enactment, so do not impose an invalid universal stage chain. Changing evidence over time may legitimately raise or lower a probability.

---

## 5. Model architecture

### 5.1 Start simple; add complexity only when it earns its place

**Baseline layer:** hierarchical or regularized logistic models for milestone outcomes, plus event-history or competing-risk models for the time and type of next transition. Include historical Congress- and era-level structure to accommodate changes in institutions and procedure; new-Congress effects must use an estimable prior, not that Congress’s future outcomes.

**Structured context layer:** sponsor and committee context, majority control, time remaining, bill type, number and party distribution of cosponsors, committee referral, leadership position, procedural route, relevant recent roll calls, and measure-level links.

**Text layer:** classify issue area and bill scope; compare text to prior bills; detect amendments and scope changes across versions. Start with TF-IDF and established topic/embedding baselines. Add modern language embeddings only after historical contamination and version-availability audits.

**Momentum layer:** calculate changes over defined windows in cosponsors, hearings, committee activity, bill version, leadership attention, scheduled votes, and relevant external events. Use both levels and rates of change; a count alone has different meaning across committees and Congresses.

**Evidence/context layer:** add dated event, speech, polling, news, and macro variables only if they improve forward tests over the existing system.

**Ensemble layer:** combine stage-specific probability models and calibrate by outcome, horizon, and forecast stage using training-period data only. Keep the final probability model separate from the language model that writes the explanation.

### 5.2 Reference classes and historical analog retrieval

For each forecast snapshot, calculate explicit historical rates from **prior bills only**. The reference class should answer concrete questions such as: “Among earlier bills in this topic that had reached this stage and received a similar vote or committee action, what share advanced to the next stage within the horizon, and what share became law by the end of the Congress?”

Build comparable groups using a transparent combination of:

- Bill type and procedural stage
- Policy-agenda topic and text similarity
- Committee and jurisdiction
- Legislative route and session timing
- Sponsor/member characteristics available at the time
- Coalition and support pattern
- Scope, fiscal content, and whether the measure is standalone or part of a package

Use a hierarchy rather than requiring an exact match on every field. Start broad, then narrow where the historical sample supports it: overall base rate → chamber and bill type → topic → topic plus stage/action → sponsor/committee/procedural context. Use partial pooling or another validated shrinkage method so a tiny subgroup does not produce an extreme rate from a few examples. Where it is helpful, weight more recent analogs more heavily, but tune any time-decay rule inside the training period.

Show the user the reference-class definition, number of bills, successes/total, time horizon, time period, and uncertainty. For example, the interface should show a form like “X of N comparable bills reached the next stage within 90 days; Y of N became law before adjournment,” with actual values computed from the eligible historical cohort. A vote or action can be a matching feature only after it has occurred by the forecast cutoff. Do not compare a bill before a committee vote with cases selected for having passed that vote.

Public releases can add structured context when they were actually available by the cutoff: committee reports, official cost estimates, administration positions, public statements, hearing materials, and recorded votes. Preserve their dates and source types. Do not collapse them into a vague sentiment score, and do not let a later analysis or revised estimate leak into the earlier replay.

Show analogs with their similarity components, dates, outcomes, and differences from the current bill. Avoid claiming that similarity explains causation. Evaluate the reference-class-only estimate as its own baseline. The adjusted model should demonstrate that sponsor, committee, current-session conditions, text, and other features add predictive value beyond the observed historical rate.

### 5.3 Explainability and uncertainty

The user-facing “why” panel should show evidence, not hidden chain-of-thought. It can display:

- Top model factors and direction of effect
- New evidence since the prior forecast
- Relevant analogs and their outcomes
- Model uncertainty and historical calibration cohort
- Scenarios such as “if scheduled for a floor vote” or “if bipartisan support reaches X,” only when the scenario is supported by a validated model

Show a rounded probability, evidence limitations, and a range only when its statistical meaning and estimation method are defined. A small sample does not itself justify inventing a range. Do not expose a precise number such as 63.7% unless the model’s calibration and sample size warrant it.

---

## 6. AI reasoning, forecasting, and reproducible execution

### 6.1 Explicit responsibilities

The AI retrieves and classifies dated evidence, extracts structured claims with source spans, proposes relevant analogs, flags contradictions, and explains recorded outputs. Official actions and outcomes come from source records with deterministic validation or adjudication. Model-written explanations are summaries, not a complete causal trace of internal computation.

An LLM probability is permitted as an explicitly evaluated candidate forecast. It must not be silently substituted for a statistical output or be validated by another model agreeing with it. Separate extraction confidence, confidence that a statement is supported, and probability of a legislative outcome.

### 6.2 Model comparison ladder

| Candidate | Inputs and role | Promotion condition |
|---|---|---|
| A: historical baseline | Eligible reference classes and prior base rates | Reproducible and correctly scored |
| B: structured statistical model | Legislative, political, timing, and selected economic features | Improves suitable baseline on forward development tests |
| C: B plus AI-extracted features | Audited text, stance, scope, attention and event features | Incremental gains survive ablation; extraction quality documented |
| D: AI forecaster | Same allowed evidence, outcome and horizon; explicit probability output | Evaluated independently, including contamination status and prospective results |
| E: combination | Statistical and AI forecasts | Weights/calibration learned only on development data; improves held-out performance |
| F: advanced reasoning architecture | Faithful implementation of a research architecture, such as HybridAgent | Beats simpler alternatives at comparable evidence and resource budgets |

No candidate is assumed to win. Begin with A/B and source extraction, then C/D. More agents, longer reasoning, or a larger model is not automatically better.

### 6.3 Hybrid Reasoning Agents: research option, not required infrastructure

The October 2026 preprint [Hybrid Reasoning Agents](https://arxiv.org/abs/2610.18861) describes latent/text switching using a learned HybridLink, specialized supervised and reinforcement post-training, and persistent hybrid working memory. Its reasoning/tool benchmark results do not establish legislative calibration. It is not reproduced by a prompt or by ordinary multi-agent orchestration.

Keep the engine model-provider-neutral. Evaluate this architecture later only after checking available code, weights, licensing, implementation fidelity, compute requirements, and independent reproducibility. Report decoded latent representations, if studied, as diagnostics—not certified faithful explanations. Do not block the first engine on training a custom language model.

### 6.4 Agent and extraction evaluation

Construct a stratified, independently human-reviewed set across eras, topics, document types, and difficult procedural cases. Measure field-level precision/recall, source support, date correctness, entity linking, contradiction handling, and abstention. Keep human reference annotations separate from model labels and adjudicate disagreements.

Test missing evidence, conflicting dates, delayed publications, irrelevant articles, paraphrased questions, repeated runs, and retrieved text containing instructions. Documents are evidence, never authority to alter the forecast task or tools. Check stability without treating deterministic wording as correctness.

The research harness records model/provider identifier, weight/checkpoint hash when available, prompt and schema versions, generation settings, inputs, tool arguments/results, outputs, failures, cost, and latency. Provider model names may not identify immutable weights. Preserve outputs for audit even when exact regeneration is impossible.

### 6.5 Docker and execution boundaries

Docker is recommended for ingestion, feature building, training, and evaluation jobs because it packages dependencies. It is optional, is not a requirement of HybridAgent, and does not remove future knowledge from model weights. A container cannot guarantee bit-identical GPU or remote-API results.

Use pinned dependency locks and image digests, versioned read-only data snapshots, recorded seeds and hardware settings, resource limits, and controlled network access. Keep the experiment worker separate from the evaluator. The worker receives training/development data and permitted evidence; the evaluator owns final labels and locked scoring. Untrusted generated code requires appropriately restricted execution; ordinary containers should not be described as an absolute security boundary.

For each run, retain a manifest linking code commit, environment, source snapshot hashes, feature registry version, model artifact, prompt configuration, split rules, calibration artifact, and output hashes. Reproducible calculations and logged API outputs together form the audit record.

---

## 7. Product and interface plan

### 7.1 Product modes

**Historical Replay:** select a bill and historical cutoff date; scrub forward through its actions; see forecast updates using only information available at each step. Keep actual outcome hidden until the user chooses “reveal outcome” during a demo.

**Live Monitor:** show current bill state and forecast, with source freshness and explicit data timestamps. Do not call a feed live unless its actual ingestion interval supports that claim.

**Research Lab:** compare cohorts, model versions, historical eras, and forecast errors; inspect calibration and feature ablations.

### 7.2 Functional spatial interface and visual direction

Current direction supersedes the earlier literal pixel-art Capitol concept. Build a distinctive govtech research workspace with ancient/modern material cues: restrained olive and graphite, warm reading surfaces, etched geometry, subtle stippling, and precise contemporary controls. Avoid generic patriotic symbols, fake tactical displays, decorative particle objects, and excessive dashboard cards. Pixel/particle rendering may supply character, but data semantics and legibility govern its use.

**Central bill landscape:** a selectable unit represents a bill; labeled groups represent topics, committees, or other explicit cohorts. Use a stable bill identity across filtering, grouping, replay, and selection. Every position, height, color, and motion that appears analytical must have a documented meaning. Do not force all analysis into 3D; provide equivalent flat and table views.

**Default workflow:** tracked/current-session bills → identify meaningful forecast changes → select a bill → inspect dated evidence → bring in historical comparables → replay. Historical outcomes should not overwhelm current work. Replay mode can deliberately open a historical cohort.

- Keep the canvas prominent and visible in the first viewport. Collapse secondary filters; anchor controls outside its plotting area.
- Distinguish stage, probability, and change in probability. Offer explicitly labeled views with consistent scales, outcome/horizon, and change interval. Missing forecasts must not appear as zero probability.
- Selecting a topic expands a readable group; selecting a bill opens an adjacent inspector with probability, deadline, as-of date, forecast issue date, evidence changes, uncertainty method, and analogs.
- Filtering operates on records and recomputes counts and denominators. A filter changing the visible cohort must not silently alter the selected bill’s saved forecast or model definition.
- A historical comparison displays eligibility rules, successes, resolved denominator, pending cases, differences, and uncertainty. Sample rate and model estimate remain separate.
- Replay updates eligible evidence, positions, and saved forecast snapshots together. If no new forecast exists at a new date, retain the previous estimate and visibly retain its issue date. Revealing an outcome never rewrites the original forecast.
- Scenario mode branches from a saved forecast and lists changed assumptions. Hypothetical conditional predictions are distinct from replay and are not causal intervention estimates without a separate causal design.
- Use progressive detail, keyboard selection, adequate hit targets, readable labels, reduced motion, and responsive flat/list alternatives. Require no camera rotation to read essential information.
- The assistant provides contextual queries and reproducible research runs; it complements bill pages, watchlists, evidence, and the research lab.

**Prototype contract:** a small internally consistent demonstration dataset must support actual selection, filtering, counting, comparison, and replay. Mock probabilities/scenarios are clearly labeled. Test all view toggles for overlap and clipping; the reviewed Flat view had a layout defect that must be fixed. No claim of a validated engine from an interactive mockup.

**Acceptance journey:** a first-time user can locate a tracked issue, identify a forecast change, inspect the selected bill and evidence, compare earlier cases, and move the replay date without losing context. Observe task completion and misunderstanding with intended users, including lobbyists and policy researchers.

### 7.3 Trust and source display

Every forecast should have a visible as-of timestamp and a source drawer. Separate:

- Legislative event date
- Document publication date
- Data retrieval date
- Forecast generation date

Show missing data and coverage limitations in context. Make it easy to open the official bill page or source document. Keep AI-generated summaries visibly grounded in citations to the source records they summarize.

---

## 8. Implementation sequence and acceptance gates

| Phase | Deliverables | Acceptance gate |
|---|---|---|
| 0: protocol | Outcome dictionary, source/feature registry, bill-family rules, temporal contract, hypothesis registry, licensing inventory | Definitions are executable; demo cases separated from evaluation; unresolved coverage flagged |
| 1: evidence backbone | Bulk/incremental ingestion, raw snapshots, normalized entities, coverage matrix, date audits | Rebuild selected Congresses; no silent missing-to-zero conversions; adjudicated chronology fixtures |
| 2: baseline and replay | Fixed snapshots, analog cohorts, structured baseline, forward splits, score report, immutable forecast schema | Demonstration reconstructs permitted evidence and scores correct outcome; baseline reproducible |
| 3: context experiments | Macro vintages, election timing/prior margins, committee attention; later polls/news | Each source passes temporal audit; paired ablations and crisis/era sensitivity recorded |
| 4: AI experiments | Human-reviewed extraction benchmark, candidates C/D/E, protected evaluator, repeated-run checks | Measured extraction/source/date quality and incremental forecasting value; contamination limitations explicit |
| 5: integrated workspace | Functional landscape, dossier, watchlist, assistant, replay, analog and model-performance views | Complete acceptance journey; consistent counts and dates; flat/table accessibility; no layout overlap |
| 6: prospective evaluation | Append-only forecast ledger, refresh/failure monitoring, resolution adjudication, drift reports | Predictions logged before outcomes; scope-specific performance and limitations reported |
| 7: advanced research | Optional HybridAgent, richer context, state expansion, provision tracking | Each extension independently evaluated; no assumed transfer of federal accuracy to state legislatures |

Begin a small prospective logging pilot as soon as the baseline is operational, in parallel with later development; do not wait until every feature or UI is finished. Keep experimental forecasts internal and clearly labeled until release criteria are met.

**First bounded experiment:** one jurisdiction (federal initially), public H.R./S. bills, enactment by Congress end, introduction and fixed calendar checkpoints. Use a tractable, audited modern subset to debug the pipeline, then extend the historical coverage toward the 50-year objective. Add milestone/timing models after outcome and date handling are stable. State-level products require separate rules, calendars, data audits and validation; a federal model is not automatically transferable.

**Engineering order for Codex:** implement data schemas and fixture-based chronology tests; ingestion; as-of feature construction; outcome resolution; baselines; protected evaluation; saved forecast API; AI extraction; UI integration. Claude Design may develop the interaction prototype in parallel using the same schema. Demo data stays separate from real forecast records.

**Core acceptance tests:** no input version after cutoff; no unresolved future label in training; same bill/date returns the same saved forecast; denominators match source rows; outcome reveal preserves original forecast; late/backfilled data is handled under the temporal contract; view switches preserve selection/date and do not overlap; AI failures remain recorded; predictions without supporting data return an explicit unavailable state.

Numerical promotion thresholds must be registered after inspecting development baselines and before opening the final holdout. Specify minimum useful improvement, acceptable calibration error, extraction-error tolerance, coverage, and latency/cost budget. Distinguish internal shadow eligibility (reliable logging and honest experimental status) from customer-facing performance claims (validated forecasting evidence).

---

## 9. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Historical coverage varies by era | Explicit coverage bands, source-level missingness, and era-specific evaluation |
| Future information leaks into backtests | Bitemporal event store, frozen snapshots, code-level cutoff tests, replay audits |
| Companion bills inflate apparent performance | Bill-family IDs and family-clustered evaluation |
| Procedure changes over time | Era effects, route-specific models, robust tests across procedural regimes |
| Severe outcome imbalance | Calibration, proper scores, cohort base rates, and appropriate precision-recall reporting |
| “Momentum” becomes a vague composite | Define each component and test its incremental value separately |
| News/sentiment adds noise or ideological bias | Source taxonomy, separate constructs, coverage checks, subgroup error audits |
| Market variables create spurious causal stories | Treat as predictive context; use ablations and avoid causal language |
| LLMs hallucinate or remember future outcomes | Source spans and human audits for support; contamination diagnostics and separate retrospective/prospective tracks for model knowledge |
| UI implies certainty or live coverage | Display horizon, uncertainty, as-of time, freshness, and source evidence |
| Political use encourages overreliance | Present probabilities as calibrated estimates with model limitations, never as guaranteed outcomes |

---

## 10. First concrete milestone

The first meaningful prototype should do one thing end to end:

> Choose a bill from a completed Congress, select a historical cutoff date, reconstruct its information set, generate a baseline probability for a defined milestone, show comparable earlier bills and sourced factors, then reveal the actual outcome and score the forecast.

That test will expose the hardest issues early: historical coverage, event timing, bill-family links, outcome definitions, and whether the visual explanation matches the statistical record. Use that workflow to build broader historical tests, then add context in controlled ablations. Begin prospective logging once the baseline pipeline is reliable. A successful selected replay is a demonstration, not proof of general skill.

---

## 11. Research and source bibliography

### Official and data sources

- Library of Congress, [Congress.gov API](https://api.congress.gov/)
- Library of Congress, [Congress.gov API documentation and usage details](https://github.com/LibraryOfCongress/api.congress.gov)
- U.S. Government Publishing Office, [Congressional Bills](https://www.govinfo.gov/help/bills) and [GovInfo developer resources](https://www.govinfo.gov/developers)
- Comparative Agendas Project, [U.S. datasets](https://www.comparativeagendas.net/project/us/datasets)
- Lewis et al., [Voteview data and documentation](https://voteview.com/data)
- Center for Effective Lawmaking, [Legislative Effectiveness Score data](https://thelawmakers.org/data-download)
- Federal Reserve Bank of St. Louis, [FRED API documentation](https://fred.stlouisfed.org/docs/api/fred/) and [ALFRED vintages](https://alfred.stlouisfed.org/)

### Research starting points

- John J. Nay (2017), [“Predicting and understanding law-making with word vectors and an ensemble model,” PLOS ONE](https://doi.org/10.1371/journal.pone.0176999). Uses sequential Congress-by-Congress forecasting and compares text and contextual signals.
- Yano, Smith, and Wilkerson (2012), [“Textual Predictors of Bill Survival in Congressional Committees”](https://homes.cs.washington.edu/~nasmith/papers/yano%2Bsmith%2Bwilkerson.naacl12.pdf). Directly studies committee survival using sponsor, committee, and bill-text information.
- Volden and Wiseman, [Center for Effective Lawmaking methods and data](https://thelawmakers.org/methodology). Provides established member-level measures of legislative effectiveness.
- Gneiting and Raftery (2007), [“Strictly Proper Scoring Rules, Prediction, and Estimation,” Journal of the American Statistical Association](https://doi.org/10.1198/016214506000001437). Foundation for evaluating probability forecasts with proper scoring rules.


### AI forecasting, validity, and evaluation additions

The following are research inputs, not evidence that this engine is already accurate. Findings from generic forecasting or classification benchmarks may not transfer to legislation. New preprints require implementation and independent evaluation before architectural adoption.

| Source | Design implication | Limitation |
|---|---|---|
| [Halawi et al., Approaching Human-Level Forecasting with Language Models, NeurIPS 2024](https://papers.nips.cc/paper_files/paper/2024/hash/5a5acfd0876c940d81619c1dc60e7748-Abstract-Conference.html) | Test retrieval, reasoning, and aggregation as a challenger | Generic forecasting evaluation is not legislative validation |
| [Paleka et al., Pitfalls in Evaluating Language Model Forecasters, 2025 preprint](https://arxiv.org/abs/2506.00723) | Audit question construction, retrieval dates, cutoff assumptions, and benchmark selection | Methodological critique; no universal correction removes all leakage |
| [He et al., Chronologically Consistent Large Language Models, 2025](https://arxiv.org/abs/2502.21206) | Explore models with temporally restricted training provenance | Bias is application-specific; availability across our eras is unverified |
| [Karger et al., ForecastBench, 2024–25](https://arxiv.org/abs/2409.19839) | Evaluate predictions submitted while outcomes are unresolved | Reported model/human rankings are study-specific, not current universal rankings |
| [Chen et al., Reasoning Models Don’t Always Say What They Think, 2025 preprint](https://arxiv.org/abs/2505.05410) | Explanation monitoring cannot certify faithful reasoning | Controlled hint experiments do not measure every deployment failure |
| [Kapoor et al., AI Agents That Matter, 2024](https://arxiv.org/abs/2407.01502) | Evaluate cost, complexity, holdouts, and reproducibility | General agent methodology rather than legislation-specific evidence |
| [Guo et al., On Calibration of Modern Neural Networks, ICML 2017](https://proceedings.mlr.press/v70/guo17a.html) | Test calibration on separate development periods | Image/document classification findings do not select the best legislative calibration method |
| [Barber et al., Conformal Prediction Beyond Exchangeability](https://arxiv.org/abs/2202.13415) | Explicitly address drift and dependence before coverage claims | Predictive coverage is not certainty about an individual bill’s true probability |
| [Zou et al., Hybrid Reasoning Agents, October 2026 preprint](https://arxiv.org/abs/2610.18861) | Optional model-architecture challenger after simpler pipeline works | Specialized training/inference required; no legislative calibration demonstrated |

[Docker build documentation](https://docs.docker.com/build/ci/) supports using containers for repeatable software environments. Statistical validity, evidence-time correctness, and remote-model reproducibility remain separate responsibilities.

## 12. Decision log and open research questions

**Decided in revision 2:** product name remains undecided; statistical and AI probability models may compete; Docker is recommended but optional; historical AI contamination is explicitly tracked; prospective logging begins early; pressure variables are hypotheses tested by policy relevance; source availability and coverage are mandatory; the main visual is an interactive data-bearing bill landscape, with flat/table alternatives.

**Not yet established:** attainable calibration/skill, usable vintage coverage for each source, commercial permissions for polling/news, exact training windows, best calibration/uncertainty method, viable custom latent-reasoning deployment, state transfer performance, and provision-incorporation ground truth. Resolve through phase gates rather than presenting assumptions as implemented capabilities.

**Revision summary:** preserved the original targets, historical coverage strategy, bulk ingestion, analogs, and staged modeling. Integrated economic/public/electoral/institutional evidence; corrected the AI leakage and probability restrictions; expanded validation and execution contracts; replaced the obsolete literal Capitol/pixel-art layout; connected research to implementation and acceptance tests.
