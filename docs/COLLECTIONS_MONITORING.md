# Collections and local monitoring

## Architecture and implementation plan

1. Keep collection membership separate from immutable evidence. Save every edit as a new immutable version with optimistic concurrency, so research sessions can freeze membership.
2. Accept a bounded explicit set of official bill identifiers. Import through the existing GovInfo ingest path, preserve retrieval-time availability, record per-bill outcomes, and retain partial progress on failure.
3. Keep monitoring disabled until enabled by the user. A local daemon owns its SQLite connection and runs only while the server process remains alive. Persist settings and the change feed. Compare normalized legislative facts rather than retrieval timestamps or raw file hashes.
4. Exercise persistence, stale edits, namespace/bounds, partial imports, retrieval-only changes, failures and recovery with offline mocked network calls.

Implemented in `engine/collections.py` and `engine/monitoring.py`. Neither modifies the evidence store schema nor the frozen pilot model or ingestion logic.

## Collections API

- `initialize(store)` installs auxiliary tables/triggers.
- `list_collections(store)` returns the latest version of each collection.
- `get_collection(store, id, version=None)` returns current or requested immutable membership.
- `save_collection(store, args)` requires `name`, `dataset` (`official` or `demo`) and `bill_ids`. Updates also require `id` and the current integer `expected_version`; stale edits fail. Dataset cannot be changed.
- Collection fields: `id`, `name`, `dataset`, `bill_ids`, `version`, `created_at`, `updated_at`, `coverage`.
- `coverage` has `total`, `imported`, `missing`, `note`. This is current import coverage, never an assertion of historical experiment eligibility. It is recomputed when read and is not frozen with membership.

Up to 100 IDs per collection/job, deduplicated in input order. Official IDs use `119-hr22` or `118-s50`; demo IDs have `demo-` prefix. Only Congress 93–200, H.R./S., positive bill numbers at most six digits are accepted. No arbitrary URL can be supplied.

## Bulk import jobs

- `start_import_job(store, args)` accepts `collection_id` or explicit `bill_ids`, plus optional boolean `refresh`. It freezes the collection's current ID list and version when queued. It returns immediately and starts a daemon worker with its own Store.
- `get_import_job(store, id)`, `list_import_jobs(store)` report persisted progress.
- Job states: `queued`, `running`, `completed`, `completed_with_errors`, `interrupted`.
- Results contain `bill_id`, `status` (`success` or `failed`), and `result` or a sanitized `error`. No exception text, credentials, or arbitrary source response is exposed.
- At most two queued/running jobs per database. Each job handles at most 100 sequential imports. Workers claim queued jobs atomically.
- Call `recover_import_jobs(store)` **once at server startup, before new requests**, to mark prior unfinished jobs interrupted. This performs no network requests. Starting a new job retries safely through ingestion's existing content hash deduplication.

## Monitoring API and lifecycle

- `initialize(store)` installs settings, per-bill state and feed tables.
- `summary(store)` returns `settings`, `watched`, `feed`, `last_cycle`, `next_due`, `runtime_note`, `scheduler_running`.
- `configure(store,args)` accepts any subset of `enabled` (boolean), `interval_minutes` (integer 15–10080), and `notifications` (boolean). Defaults: off, 60 minutes, notifications enabled. Unknown fields fail.
- `refresh_watched(store)` explicitly refreshes official watched bills even when the schedule is disabled. It is synchronous; use the existing threaded HTTP handler. A second overlapping cycle returns `already_running`.
- Call `recover_monitoring(store)` once at server startup before accepting requests or starting the scheduler. It marks a prior running cycle interrupted, preserves completed results, and records one interruption event. Never call this during live requests.
- `start_scheduler(db_path=None)` starts one daemon per database path, with its own Store; returns a `threading.Event`. Call its `.set()` on shutdown. It checks every 30 seconds and does not fetch while disabled. Persisted opt-in resumes on subsequent server launches.
- Disabling scheduled monitoring stops additional bills from starting during a cycle; an in-flight network request may finish. Removing a watch also skips it before its next request.
- At most 100 official watches can be refreshed in a cycle. Demo watches are excluded. More than 100 returns a persisted `failed` cycle with an `error` message rather than silently starving the tail of the watchlist. The failed attempt advances the next scheduled time, preventing a retry on every 30-second check.
- `last_success` and `last_attempt` are distinct. Failed refreshes preserve existing evidence and last successful time. `stale` means no successful refresh or the successful refresh is older than the configured interval, independent of whether scheduling is enabled.
- The latest 100 feed entries are returned. Entries identify semantic `bill`, `events`, `resolutions`, or `initial_import` changes. Components are compared with persisted hashes from the last successful refresh, so changes imported by chat or bulk imports between cycles are detected. On the first refresh, the pre-fetch local record is the baseline. Retrieval-only and raw-hash-only changes do not create change notifications. Failed cycles and recovery appear in the feed.
- `notifications` controls the `notify` flag on feed entries. It does not suppress audit history. There are no email, push, or external messages.

The schedule cannot run while the computer/server is off. This is deliberately local monitoring, not a hosted background service. Source imports do not backdate historical public availability. A refresh does not create or validate a forecast.

## Verification

`python3 -m unittest tests.test_collections tests.test_monitoring -v`

Twelve offline tests cover immutable versions/stale edits, bounded namespaces, partial job failure and atomic claims, startup interruption, default opt-out and settings persistence, unchanged legislative facts after new retrieval, changed facts, failure/recovery, mute flags, scheduler shutdown without fetching, and exclusion of demo watches, out-of-band imports, oversized-watchlist backoff, and interrupted monitoring recovery.
