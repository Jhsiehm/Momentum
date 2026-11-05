# Legislative intelligence: architecture and release gates

Implementation and evidence plan, November 3, 2026.

## Product objective

A user can describe an organization's interests, find relevant bills, monitor changes, investigate historical patterns, compare conditional hypotheses and obtain qualified forecasts. Chat, bill pages, research tables and the visual map must operate on the same evidence and numerical results. The interface should help answer what matters, what changed, what happens next and what requires attention.

Relevance, impact and probability are different quantities. Matching an interest does not establish organizational impact. A stakeholder's stated position does not establish influence. An experimental forecast does not establish validated predictive accuracy. These distinctions belong in the returned data contract and the interface, rather than relying on the chat model to remember a disclaimer.

## Architecture

1. **Evidence layer.** Append-only official bill metadata, actions, outcomes and raw source hashes retain effective, publication, observation and verified-availability dates. Imports are resumable and report coverage, failures and freshness. Organization notes and stakeholder assertions remain separately attributed user records; they cannot overwrite official evidence.
2. **Organization workspace.** Profiles describe issues, jurisdictions and client interests. Watchlists, assignments, notes, stakeholder evidence and briefings organize work. Matching rules explain why a bill was selected and the universe searched. The local single-user workspace does not imply access-controlled client isolation.
3. **Reusable analytical layer.** A validated query specification identifies population, dataset, cutoff, checkpoint, target and filters. Supported operations discover bills, form descriptive cohorts, compute intersections, retrieve historical comparisons and rank eligible model outputs. Queries return exact counts, exclusions, missingness, source references and reproducible input identities. They never execute generated SQL or code.
4. **Model layer.** Versioned baselines and candidates consume historically eligible features. Scenario models, milestone models and political/stakeholder variables require separate implementations and evidence audits. Hypothetical values cannot alter observed data or train on imagined outcomes.
5. **Research and evaluation layer.** Frozen protocols, sessions and prediction receipts separate exploratory work, development selection, final evaluation and prospective monitoring. Adaptation stays within prior-data training/validation and records every trial. Repeating evidence is replication, not additional independent learning.
6. **Chat orchestration.** The language model interprets the question and invokes allowlisted tools. Numerical answers come from tools, not prose. A free-text hypothesis is an annotation until mapped to an executable, supported design. Unsupported questions return the missing variables/methods and any narrower analysis the user can review.
7. **Presentation layer.** Home prioritizes important changes; Bills supports discovery and evidence inspection; Research holds hypotheses and results; Chat operates across them. A map links assumptions, evidence and affected bills without turning correlation into causation. Responsive layouts retain the same definitions and gates on laptop and mobile.

Every analytical response should carry the executed specification, dataset scope, target/horizon, information cutoff, selected and eligible counts, exclusions, outcome denominator, version, sources, limitations and destination links. Saved analyses additionally freeze input membership and hashes. A bounded subset must never be labeled a census.

## Existing evidence and limits

The fixed-sample v2 result documents 53 training cases with two enactments and 33 evaluated cases with zero enactments. Candidate Brier loss is 0.00605899; baseline loss is 0.00297521. The candidate did not demonstrate added value on the primary metric. Zero evaluation enactments prevents assessing discrimination. This is a post-inspection evidence amendment, not an untouched final holdout. Human audit receipts and family adjudication remain outstanding. See `cohorts/seeded-publication-v2-results.md`.

Existing fixed-model prediction uses stage, age, activity, inactivity and chamber. Bounded adaptation can compare three regularization values across structured and frozen title/topic-hash feature policies, using prior-data inner validation. This does not implement learning from all available bill information. Current title/topic matches are search matches, not semantic policy understanding.

Current research code and existing frozen studies must remain unchanged by this product expansion. New analytical and workspace modules may reuse their public functions while maintaining versioned boundaries. No product feature can grant research-release eligibility.

## Delivery phases and exit criteria

### Phase 1: Useful organization workflow

Deliver profiles, explicit matching reasons, watchlists, bill ownership/notes, attributed stakeholder records and source-grounded briefings. Retain separate client/workspace identifiers where implemented, but do not advertise permissions or collaboration until tested authorization exists.

Exit criteria: invalid fields are rejected; edits persist; filters and counts agree; matched interests are traceable; source timestamps are visible; empty and stale states have useful actions; mobile navigation and keyboard controls remain usable. Source refresh alone must not create a substantive change alert. No external communication occurs without authorization.

### Phase 2: General grounded investigation

Deliver a shared supported-query interface for descriptive cohorts, intersections, historical examples and bounded experimental rankings. Topic/chamber/stage or other supported filters must use metadata valid at the stated cutoff. Unavailable estimates remain unavailable rather than becoming zero or being replaced with language-model guesses.

Exit criteria: known-fixture intersection counts are exact; unresolved outcomes are separately counted; denominators and family handling are disclosed; future information cannot enter historical queries; deterministic inputs reproduce outputs; limits are visible. Rankings state the entire searched population and evaluated/unavailable counts, common target, horizon and model. A ranked search page is not a ranking of all Congress. Historical passage rates are labeled descriptive rather than individual probabilities.

### Phase 3: Audited data expansion

Collect a larger, separately registered temporal cohort with official sources, audited outcome coverage, historical feature availability and family links. Size planning must account for rare enactments and the precision required for each intended evaluation, rather than relying on a convenient bill count. If positives are oversampled, retain the design and weights needed for population-level estimates.

Exit criteria: provenance and exclusion receipts reproduce; human reviews are real and attributable; outcome labels are supported; family contamination checks pass; missingness and source coverage are quantified by Congress and category. Bulk-imported current metadata alone does not qualify as historical training evidence.

### Phase 4: Demonstrate forecast value

Prespecify target, checkpoint policy, primary scoring rule, comparator and population. Use earlier Congresses for development, later temporal validation and a separately protected final evaluation. Fit transformations and calibration only on development data. Compare paired predictions using family/Congress-aware uncertainty and enough positive outcomes to assess discrimination. Report Brier/log loss, calibration, ranking performance and subgroup uncertainty without selecting the most favorable metric after inspection.

Exit criteria: the registered release criteria are met on protected data, reproduction succeeds, missing/abstained predictions are reported, and model selection has not repeatedly consumed the final evaluation. Engineering minimums such as 20 training families are not sufficient scientific release thresholds. Existing v2 outcomes cannot be reused as a new untouched holdout.

### Phase 5: Prospective reliability and bounded learning

Issue immutable forecast receipts before outcomes. Score matured outcomes using a declared schedule, account for pending cases and compare model versions on matched populations. Adapt only using newly eligible training evidence; keep a champion/challenger boundary and reversible deployment versioning. Human-readable status must explain retained, adjusted, blocked and reused results.

Exit criteria: prospective timestamps and target definitions survive audit; repeated runs do not manufacture sample size; target-label perturbation cannot change prior predictions; no automated promotion bypasses quality criteria; failures pause affected work and remain visible. Running many experiments does not guarantee improvement.

### Phase 6: Institutional context and scenarios

Add historically versioned political control, committee membership, sponsor/cosponsor networks and attributed stakeholder positions through audited sources. Prespecify ablations before claiming that each feature family improves prediction. Design conditional political scenarios separately from causal intervention estimates; explain assumptions, overlap and unsupported extrapolation.

Exit criteria: sources and availability are audited; retrospective corrections cannot leak; incremental value holds on unseen periods; conditional assumptions are reproducible; hypothetical outcomes never become labels. Until then, Democratic-wave and stakeholder-influence probability changes remain unsupported. Sourced qualitative discussion is possible but must not be presented as a validated scenario forecast.

### Phase 7: State coverage and firm deployment

State data requires jurisdiction-specific ingestion, action mappings, sessions, outcome definitions and separate validation. Federal performance does not transfer by assertion. Multi-user deployment requires authenticated access, server-side workspace authorization, tenant-isolation tests, audit trails, recovery, secrets management and an appropriate concurrent database. Network/mobile-device access, hosting, notifications and provider costs require explicit deployment choices.

Exit criteria: jurisdiction and tenant isolation hold under negative tests; backup recovery works; scheduled workers have durable ownership and limits; source licensing and retention are recorded; real mobile access is tested. Responsive layout on a local laptop server is not a hosted mobile service. The current default remains loopback-only and single-user.

## Cross-cutting acceptance matrix

- A historical metadata correction cannot change an earlier frozen answer.
- Unresolved bills are never silently negative outcomes.
- Related bill families cannot masquerade as independent outcome evidence.
- No synthetic score or model explanation grants real-data validation.
- Unsupported filter/target requests fail explicitly rather than silently substituting defaults.
- An identical query/evidence version reproduces numeric results; new evidence receives a new identity.
- Chat and direct API calls enforce the same bounds and return compatible results.
- An empty, partial or unsupported result includes reasons and a useful next step.
- Source content and user notes remain untrusted data; neither can trigger arbitrary execution.
- The UI never uses stakeholder support, relevance or user-assigned urgency as an undisclosed probability adjustment.

## Definition of completion

Each shipped increment must demonstrate functioning persistence, computation, error handling and interface integration, with targeted tests and a recorded coverage boundary. Product completeness and scientific validation are separate milestones. The ambitious full system includes both; unsupported research cannot be completed by presenting a richer interface or a more confident answer.
