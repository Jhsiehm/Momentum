# Research sessions

## Implementation plan

A saved collection defines the evaluation population, not the training universe. At proposal time freeze the collection version and every record in its dataset. Evaluate selected bills only, using earlier-Congress training families and labels available at each fixed-age checkpoint. Unknown outcomes remain unknown. Record exclusions before explicit execution.

Proposals and results are immutable. Revisions create a linked proposal with exactly one changed assumption. Execution refits deterministic candidate B from the frozen records and never silently reuses forecasts from another evidence snapshot. Exports contain the frozen records, configuration, source hashes, fitted artifacts, scores and implementation hashes. Runs stay development diagnostics; they do not authorize forecast promotion.

## Public API and integration

- `initialize(store)` installs immutable proposal/result tables.
- `propose(store, args)` accepts `collection_id`, `hypothesis`, optional `title` and integer `age_days` (1–700, default 180). Unsupported targets, candidates, tracks and feature families fail closed. Returns the full proposal and preflight.
- `list_sessions(store)` and `get_session(store, id)` return proposal fields plus `result` (null before execution) and current status.
- `execute(store, id)` explicitly executes a ready proposal; subsequent calls return its original immutable result. Run this in the application's background worker for interactive use. Changed implementation hashes block execution; later imports cannot alter frozen evidence.
- `revise(store, id, changes)` accepts exactly one changed `age_days`, `collection_id` or `hypothesis`. Creates a linked child against the same frozen evidence. A replacement collection must use the same dataset. Bills absent from the frozen evidence are excluded honestly.
- `compare(store, left_id, right_id)` pairs matching bill/checkpoint/outcome cases only when evidence and checkpoint definitions agree. Changed checkpoint runs show aggregate scores with a non-comparability explanation.
- `export_bundle(store, id)` returns JSON with complete normalized evidence, configuration, fitted artifacts, training manifests and implementation/source hashes.
- `reproduce_bundle(bundle)` validates integrity and refits offline in an isolated database. It returns whether the recomputed reproducibility hash matches the exported run. It neither calls the network nor reads current application evidence.

Proposal status is `proposed` or `blocked`; executed status is `completed`. Preflight reports target, eligible and scoreable counts, unknown outcomes, each excluded case, and blockers. Results contain exact selected cases, Brier/log loss and reliability bins for candidate and historical-rate baseline, scored/family counts and a reproducibility hash. Missing outcomes do not enter either score.

## Honest boundaries

A frozen collection is the evaluation population; all eligible earlier Congresses remain available for training. Membership is snapshotted, including collection version, so subsequent collection edits cannot change a run. This does not make the population representative or independently sampled. Family deduplication applies to training; evaluation reports bill-weighted scores and family counts, without clustered intervals.

The normalized evidence bundle supports numerical reproduction with the exact implementation. Raw original source payloads are referenced by hashes in the local `data/raw` archive, not embedded in the JSON; source-level independent re-audit additionally requires those files. Code hashes identify source but do not bundle a Python runtime or source tree. Missing historical action evidence blocks official sessions and points to the separately audited publication-history pilot under Experiments; this runner does not silently substitute that pilot's different model.

The proposal records an explicit question before this execution, but remains exploratory. There is no claim of a globally untouched holdout, no causal scenario interpretation, no selectable unsupported model, and no calibrated forecast release.

`replicate(store, id)` creates a separate child proposal with unchanged collection, configuration and frozen evidence; execute it explicitly to obtain a separate result artifact. Matching reproduction hashes mean successful replication, not independent validation.

The fixed-age origin uses the earliest available metadata version, then validates that the eligible snapshot still has the same introduction date and requested age. Conflicting historical introduction metadata blocks that case; a later correction cannot move an old checkpoint or supply a hindsight title/family. Displayed case metadata comes from the eligible snapshot.

Bundle reproduction verifies the hash of the supplied result content, recalculates all reported score/count aggregates from its cases, and only then independently refits from frozen evidence. Rehashing a modified outer bundle cannot make altered scores pass reproduction.
