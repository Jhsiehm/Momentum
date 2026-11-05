# Audited historical development sampling

This workflow freezes a reproducible official-record selection, imports its source records, records human evidence reviews and checks whether a sample-scoped development experiment is eligible. “Audited sample” names the workflow; it does not mean that a newly created sample has passed review. Neither successful imports nor a completed checklist establish model validation or a protected holdout.

## Browser workflow

1. Open **Data & imports → Create audited sample**. Discover House and Senate bill-status directories for 1–6 completed Congresses from the 113th onward, or choose a saved inventory. Defaults are 114, 116 and 118. GovInfo directory discovery requires no API key.
2. Choose a name, size, human-review size and seed, then **Save sample & audit plan**. The UI defaults to 100 bills, 25 reviews and `historical-development-v1`. Selection uses Congress/chamber strata with proportional largest-remainder allocation and seeded Python `Random.sample`; it does not inspect enactment outcomes. A separately seeded draw (`seed + ':human-audit-v1'`) fixes the review subset.
3. **Import selected bills** starts a background job. Data & imports displays processed, parsed and failed counts and per-record results. Import failures do not replace selected bills or change the denominator. A manually entered list can also be imported, but is not a random population sample.
4. Open the saved sample, download its audit CSV, inspect bill evidence and official XML, and record each designated human review. The five checks are identity, source support, historical availability, bill family and outcome. A passing receipt requires all five booleans and evidence notes; unresolved reviews use `needs_correction`. Downloading a sheet records no reviews. CSV is an export, not a review-upload endpoint.
5. Choose **Check experiment readiness** to save a proposal with the sample's exact evaluation membership, sampled evidence and audit context. Inspect its preflight in Experiments. An incomplete or unresolved designated audit, unadjudicated families or no scoreable cases blocks execution. Passing reviews do not rewrite evidence dates or automatically unlock a run.

## Frozen records and provenance

`sample_inventories`, `research_samples` and `sample_audits` reject updates and deletion through SQLite triggers. An inventory records its ordered population, Congress/chamber counts, directory URLs, retrieval dates, retained raw hashes and inventory hash. `directory_complete` means complete received directory listings whose rows and links passed validation; unsupported pagination or mismatched rows fails discovery. It does not certify archive coverage, historical availability or eligible outcomes. Discovery may reuse previously retained validated strata unless `refresh: true` is requested.

A sample records the inventory ID/hash, seed, algorithm version, selected IDs, audit IDs, stratum allocation, chronological protocol and sample hash. Whole-sample, training and evaluation collections are created in batches of at most 100; the sample freezes their IDs at collection version 1. Subsequent collection edits create other versions and do not revise sample membership.

Each human review is a new receipt with its own ID, sample/bill IDs, checks, decision, notes and timestamp. Prior receipts remain retained. Sample detail and exported CSV show the latest receipt per bill. These are local review records, not authenticated independent attestations. A proposal freezes the latest audit receipts alongside inventory/sample hashes and any excluded training IDs, so later review changes require a new proposal to affect that context.

## Exact experiment scope

The highest sampled Congress supplies evaluation bills; earlier sampled Congresses supply training bills. The sample proposal route loads the frozen evaluation collections at the saved version and requires their concatenated membership to equal the sample's evaluation list exactly, including ordering. It freezes official records only for selected bill IDs. It removes all earlier sampled bills whose recorded family IDs overlap any recorded evaluation family. Singleton or unadjudicated family IDs do not demonstrate independence and remain a review blocker.

Use `/api/sampling/propose` (the sample's readiness action) for this scope. A generic collection experiment may include additional eligible earlier-Congress imports in its training universe. The sample route fixes a 180-day checkpoint and compares the existing structured action-history model against the prior-training enactment rate for own-bill enactment by Congress end. Saved proposals retain the underlying normalized evidence; preflight evaluates checkpoint eligibility, prior training and observed outcomes, and carries the sample-specific audit/family blockers. Development readiness is not release eligibility. Repeated use of these evaluation cases is development, not independent validation.

## Resuming source imports

A bulk job accepts 1–10,000 official IDs (or a sample ID), normalizes and deduplicates identifiers, and persists each success or failure. Only one bulk job can be queued/running at once. A successful parse may reuse a cached unchanged record; the UI does not claim a separate download count. Retrieval and parsing never count as human audit.

On server restart, queued/running jobs become `interrupted`. Resume retains successful records and processes unfinished or failed records. `completed_with_errors` jobs support retrying failures. Retry saves the earlier attempt's results/status before requeueing the same job. Jobs are mutable progress records; inventory, sample and review receipts remain frozen.

## Local API routes

All routes are served by the local HTTP service. POST bodies are JSON objects.

| Method and route | Purpose / required inputs |
| --- | --- |
| GET `/api/sampling/inventories` | List saved inventories. |
| POST `/api/sampling/inventory` | Discover population; `congresses`, optional `refresh`. |
| GET `/api/sampling/samples` | List samples with current review/import readiness. |
| POST `/api/sampling/samples` | Freeze selection; `inventory_id`, optional `name`, `size`, `audit_size`, `seed`. |
| GET `/api/sampling/sample?id=…` | Retrieve sample and latest review receipts. |
| GET `/api/sampling/audit.csv?id=…` | Export designated review rows as CSV. |
| POST `/api/sampling/audit` | Append receipt; `sample_id`, `bill_id`, `status`, five boolean `checks`, `notes`. `/api/sampling/review` is an alias. |
| POST `/api/sampling/import` | Queue import; `sample_id` or `bill_ids`, optional boolean `refresh`. |
| GET `/api/sampling/jobs` | List import jobs. |
| GET `/api/sampling/job?id=…` | Retrieve one job and record-level results. |
| POST `/api/sampling/retry` | Resume interrupted/error job by `id`. |
| POST `/api/sampling/propose` | Save sample-scoped proposal; `sample_id`, optional `title`, `hypothesis`. |

## Saved development sample

The workspace's recorded example is sample `51ee0efb-22bc-406a-87d4-75494e573623`, selected with seed `historical-development-v1` from 40,435 directory records across Congresses 114, 116 and 118. Its frozen 100-bill selection contains 60 training bills and 40 evaluation bills. All 100 were imported with zero import failures; all 25 designated human reviews remain pending at this documentation snapshot. These local data are not bundled into a fresh clone, and the snapshot is not a live status counter.

Current BILLSTATUS downloads are known at retrieval time. Historical action dates alone do not prove availability at the 180-day checkpoint. Historical use requires independently supported availability provenance; family links and negative outcomes require adjudication, including complete Congress-end coverage for a negative label. The saved sample therefore establishes reproducible selection and working source ingestion, not eligible historical forecasts, predictive skill, calibration or a protected holdout. The separate publication-history pilot has its own design and evidence contract.

Implementation: `engine/sampling.py`, `engine/sample_research.py`, `engine/sessions.py`, `engine/server.py` and `web/sampling-flow.js`.
