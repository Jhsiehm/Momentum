# Legislative forecasting engine architecture

Implementation plan, recorded before application implementation, 24 October 2026.

## Boundaries and engineering order

1. Temporal domain and append-only SQLite store: bills, versioned metadata, raw payload hashes, actions, resolution records, immutable forecasts, AI runs, ingestion checkpoints, watchlist.
2. Official GovInfo XML imports and Congress.gov incremental ingestion, preserving raw responses and retrieval times. Existing source dates alone do not prove historical availability. Strict replay uses observed time; an audited archive may supply independently verified availability with provenance.
3. Deterministic as-of snapshots: filter metadata and events before deriving stage, age, action counts and inactivity. Never infer absent events as negatives. Unknown metadata remains unknown. Fingerprint all eligible inputs.
4. Baselines: empirical resolved training base rate, a stage/chamber reference class with family deduplication and shrinkage, and L2 logistic regression. Training uses earlier Congresses and labels already resolved and observable at origin. Fixture forecasts are demonstration-only.
5. Forward evaluation: lock predictions before independent scoring; score Brier/log loss and reliability bins with bill/family counts. A separate evaluator CLI reads outcome files. This process separation is an operational boundary, not a secure sandbox; deployment must provide access controls for untouched holdouts.
6. HTTP API: list, snapshot, forecast lock/retrieve, explicit outcome reveal, watchlist, coverage, research, source-grounded AI extraction. No API accepts raw SQL, arbitrary remote URLs, or code execution.
7. Interface: prominent topic landscape; flat/table views; dated evidence inspector; analogs; replay cutoff; outcome reveal; research and coverage; local watchlist. All visual coordinates have labeled meanings. Missing forecasts stay missing.
8. Prospective ledger: new forecast records receive actual issue times; retrospective reconstructions are labeled. Stored predictions never acquire invented historic issue dates.

## Technology decision

Python 3.9+ standard library keeps the local prototype runnable without package installation. SQLite WAL is a transactional single-machine canonical store and ledger, chosen in place of DuckDB because the first slice needs transactions and concurrent API reads. Raw files are content addressed. Export JSONL for research; add DuckDB/Parquet for large analytical backfills. A PostgreSQL migration is required before multi-user deployment. Browser-native ES modules and CSS avoid a build dependency for the research console. Bind to loopback only.

## Temporal contract

Store effective_at, published_at (nullable), observed_at and optional verified_available_at with archive_proof. Eligibility requires event time <= cutoff and known availability <= cutoff. Default known availability is observation time; verified availability is permitted only with an explicit audit artifact. Date-only events become end-of-day UTC, conservatively preventing same-day intraday leakage. Bill metadata is versioned under the same rule. Late corrections create new versions. Raw snapshots cannot be overwritten. Latest eligible version wins per source record. Outcomes are resolved only with known positive evidence, or explicit audited complete coverage at Congress end; missing enactment is never automatically failure.

## Immutable forecast contract

Each record contains bill/family, target, Congress-end horizon, cutoff, issue timestamp, retrospective/prospective track, dataset namespace, snapshot hash, eligible evidence IDs, model artifact and training IDs, code/feature/calibration/prompt versions, cohort counts and probability. Unique bill/cutoff/model identity returns the existing record even if new evidence arrives. Explicit model-version change is needed to produce a new experiment. Resolution is stored separately. Source timestamps remain distinct.

## Model and uncertainty contract

Candidate A: (successes + 1)/(n + 2), a declared Beta(1,1) smoothed prior rate. Conditional cohort estimate shrinks with five pseudo-observations toward the global rate. Candidate B: deterministic standardized L2 logistic regression. No calibration claim; calibration artifact is `none`. No invented probability interval. Analogs use prior bills at a matched age and stage, never their final stage. One resolved example per family. Current implementation requires 20 resolved prior families and both outcome classes; otherwise unavailable. Training selection and minimum sample rule are protocol v1, not release thresholds.

## AI boundary

OpenRouter key is server-only, loaded from environment or ignored local .env. Evidence is untrusted data. The model may return claims with exact supporting quotes and evidence IDs; code verifies those spans. Unsupported claims are rejected. Model failures, latency, usage, model and input/output hashes remain in a run log. Model output cannot change official outcomes or saved statistical probabilities. Retrospective model-weight contamination remains disclosed.

## Acceptance and phase gates

Automated tests cover late arrivals, metadata versions, unresolved training labels, family duplication, future events, immutable forecasts and reveal, score formulas, ingestion idempotence, unsupported AI spans, unavailable states, and API errors. Browser review covers selection/filter/date persistence and responsive flat/table alternatives.

This implementation is a first runnable vertical slice and infrastructure for phases 0–2, 4 extraction, 5 workspace and 6 logging. It does not establish 50-year coverage, validated calibration, milestone survival models, C/D/E challengers, macro/poll vintages, commercial source rights, or a hardened final-holdout environment. Those research gates require audited datasets and registered experiments; see ROADMAP.md. Synthetic fixtures cannot substantiate real predictive skill.

## Chat workspace implementation

`engine/workspace.py` adds persistent chats/messages and experiment runs alongside the immutable evidence ledger. `web/index.html` is the chat shell; the previous research UI lives at `/workspace.html` and is embedded for Replay/Monitor, retaining its domain behavior. Browser navigation does not discard conversations or run reports.

A chat submission is acknowledged immediately and processed by a bounded background worker. Per-chat serialization and client request IDs prevent duplicate submissions; pending work becomes a recorded failure after a server restart. OpenRouter receives recent conversation and bounded tool outputs. Tools are allowlisted: inspect sources/bills, import a GovInfo bill, run or rerun a fixed-age experiment, inspect run history, or provide a view link. No shell, arbitrary URL fetch, generated execution or deletion tool is exposed.

Experiment reports score only the exact run's cases, independently of the cumulative research ledger. Reruns get new report IDs and parent links; immutable forecast identities are reused when parameters have not changed. Finished tools emit server-derived artifacts; the browser renders report links and probability-bin visuals from these values. Failed provider calls preserve already-created reports.

OpenRouter settings accept a replacement key and model ID via same-origin JSON POST, write an atomic mode-0600 ignored environment file, and update the running server. GET returns only configuration status and model name, never the secret. Testing invokes a small provider completion. This remains a loopback-only, single-user local application.

## Research-contract layer

`engine/rigor.py` maps the full plan to an explicit capability registry. Every chat turn receives that registry, document fingerprints, invariants and recent immutable protocols. Allowlisted document retrieval exposes exact sections of the original plan and architecture; planned features are not treated as available tools. Protocol annotations and source contents remain untrusted data.

New tools cover readiness, source audits, protocol registration/execution, paired comparisons, saved-forecast audits, eligible forecast saving and existing exact-span extraction. A protocol freezes the hypothesis, target, track, candidate, features, population definition, data-record fingerprint and documentation versions. Original document contents are retained under content-addressed local research_documents files. Unsupported designs are saved as blocked. A matching previously run configuration is explicitly post hoc; no local registry can prove that an analyst has never inspected equivalent data elsewhere.

All experiment paths run preflight and report exclusions. Empty or unusable cohorts block execution. Unknown design fields, unsupported targets, model candidates and feature families fail closed. Registered runs and their reruns require the same data fingerprint; a changed dataset requires a superseding protocol. A change during execution invalidates scoring. Existing forecasts retain their immutable identity.

Comparisons require matching dataset/Congress/checkpoint definitions and pair identical bill/cutoff/label rows. Reusing the same forecast IDs is labeled replication, not independent validation. Audits verify stored rules only and retain limitations; they cannot authenticate archive provenance or certify calibration. Customer-facing release remains blocked until separate real-data, uncertainty, holdout and prospective gates are implemented and satisfied.

Chat has read access to the complete specification and can explain all phases, but only the explicitly implemented tools can execute. Milestone/survival models, context ablations, human extraction benchmarks, protected final evaluation, causal scenarios and advanced architectures remain unimplemented. No prompt can substitute for those methods.

## Connected product workflow

`engine/collections.py` stores immutable collection versions with optimistic update checks and bounded, persisted import jobs. `engine/sessions.py` freezes the normalized evidence universe and selected test membership, checks eligibility, fits on prior-Congress evidence, and saves immutable proposal/result records separately from the legacy forecast ledger. Revisions and replication receive new identities. Export/reproduction checks bind normalized inputs, configuration, code and computed results. Current data refreshes do not silently rewrite earlier sessions.

`engine/monitoring.py` adds an opt-in local scheduler and per-bill refresh state. Persisted semantic baselines detect updates from scheduled, manual or other import paths; retrieval-only changes do not generate evidence alerts. Errors are retained and retried at the configured interval. Startup recovers interrupted imports and monitor cycles before starting the scheduler. Each worker owns its SQLite connection; the server remains loopback-only and single-user.

`engine/product_tools.py` is the allowlisted chat adapter. The shell's `web/research-flow.js` presents collections, proposals, results, comparisons and watching. Chat emits real session artifacts and computes run summaries from saved scores. Monitoring preferences do not enable automatic forecast issuance or confer prospective validation. Existing research release gates remain in force.
