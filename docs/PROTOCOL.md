# Protocol v1

Primary target: own-bill public-law enactment by the end of the Congress. A bill's provisions appearing in another vehicle are a different, unimplemented target. H.R. and S. only. Committee stage is not a necessary precursor to enactment.

The temporal store rejects unknown kinds/datasets, invalid bill types, nonbinary outcomes, invalid event stages, unproven early availability assertions, negative resolutions without complete coverage, and negative resolutions before session end. Eligibility compares normalized UTC timestamps. Date-only source events become end-of-day UTC. Missing publication times remain null.

## Canonical audit import

`python3 -m engine import-audited records.jsonl` accepts one object per line with `kind` (`bill`, `event`, `resolution`) and `record`. Imports resume after the last verified line; records and raw input are content addressed. Metadata must precede events/resolutions in the file.

All records require `bill_id`, `family_id`, `dataset` = `official`, `source_key` (stable within kind), `source_name`, `source_url`, `effective_at`, `observed_at`. Optional `published_at` is a real release timestamp, not an event date. `verified_available_at` requires `archive_proof` identifying the audited historical artifact and its provenance. This is an operator assertion, not automatic proof verification. Audit the archived text for retrospective contamination before using it. Never invent archive proof to make replay work.

Bill records also require `congress`, `type` (`hr`/`s`), `title`, `introduced_at`; `topic` and `sponsor` may be unknown. Event records require `text` and integer `stage`: 0 introduced/other, 1 committee advancement, 2 origin passage, 3 agreed bicameral text, 4 enacted. Use audited action mappings; unknown action codes remain stage 0. Resolution records require `value` 0/1, `definition` and `complete_coverage`; negatives require `complete_coverage: true` and a resolution date no earlier than session end. Supply family links from adjudicated related-bill records.

## Training and evaluation

At each target cutoff, use earlier Congresses only and outcomes both effective and knowable by that cutoff. Match each earlier bill at the target bill's age; exclude snapshots at or after resolution. Deduplicate training families and exclude the target family. Minimum 20 resolved families and both outcome classes; this is a computation eligibility floor, not validated predictive sufficiency.

Logistic features: normalized procedural stage, age, action count, inactivity, originating chamber and 30-day action count. Standardization is fitted to training rows. L2 penalty .05, 300 deterministic gradient steps, learning rate .12. Global rate uses Beta(1,1) smoothing. Reference cohort narrows to chamber/topic/stage when at least 10 cases exist; otherwise broadens. Five prior pseudo-observations shrink the conditional rate toward the training global rate. No calibrated interval is emitted.

The `backtest` command chooses a test Congress and fixed bill age; the model builds its prior-only training origin per target. Run prespecified multiple Congresses separately. The UI research report is cumulative development inspection, not a final locked evaluation report. For independent scoring export one prespecified prediction per bill and provide the separate evaluator with JSONL labels: `bill_id`, `value`, `resolved_at`. It rejects a forecast cutoff on/after resolution and prospective forecasts issued on/after resolution. Missing labels are pending. The evaluator returns Brier, log loss, reliability counts, family count, and input hashes.

Real-data promotion requires registered splits, label provenance, family- and Congress-clustered uncertainty, development-only calibration, paired model comparisons, and a permission-protected final holdout. These remain gates, not claims of the local development report.

## Source and licensing register

- GovInfo/Library of Congress official bill metadata: used in targeted imports, current snapshots. Endpoint-specific historical coverage unverified. Raw source URL/hash retained.
- Congress.gov: optional incremental discovery; requires its own API key. Endpoint pagination and rate-limit retry supported. Exhaustive corpus not yet imported.
- OpenRouter: optional remote processing of source packets; outputs retained. Model-weight provenance and historical contamination not controlled.
- Synthetic fixtures: deterministic project-generated demonstration data, never evaluation evidence.
- Polls, commercial news, social, macro vintages, Voteview and effectiveness measures: not ingested. Licensing, coverage and temporal audits pending per source.
