# Legislative forecasting research workspace

A local, working first implementation of the supplied revision 2 plan: historical replay **and** current-bill monitoring, with a point-in-time evidence store, saved statistical forecasts and a browser research console. Product name remains undecided.

## Run

Requires Python 3.9+. No package installation or frontend build is required. On macOS, double-click `Start Workspace.command` to start the local service and open the browser. Keep its terminal window open while using monitoring or background research.

```sh
python3 -m engine serve --port 8765
```

Open http://127.0.0.1:8765. The service binds only to loopback. First launch seeds 315 explicitly fictional bills across six Congresses. Official records occupy a separate namespace. A fresh clone contains no downloaded government data or credentials.

The local workspace includes a saved 100-bill historical development sample: all 100 records imported with no import failures, while 25 designated human reviews remain pending. This is source ingestion, not validated forecasting performance. See [audited sampling](docs/AUDITED_SAMPLING.md) for the frozen selection and eligibility limits. Current monitoring supports on-demand checks and optional scheduled local checks while the server runs.

## Organization and evidence workflows

Home → **Organization workspace** creates a local organization/client profile. Enter issue terms and optional Congress filters to discover imported matching bills with explicit reasons. Follow bills for the existing local monitor; use assignments for owner labels, due dates, notes, priority and user-assessed impact. Stakeholder positions require a citation, source date and quoted statement, and remain unverified user records. Create a 7-day briefing to freeze the current workspace and download Markdown. Profiles are organizational labels, not authenticated or access-controlled accounts.

Research → **Explore evidence patterns** opens the general analysis layer. Choose official or synthetic evidence, an information cutoff and filters, then compare up to three groups. Exact disjoint intersections and known/unknown outcomes are calculated from retained evidence. Results are saved immutably and export as JSON. Saved forecast comparison includes only compatible recent prospective receipts; it may return no usable ranking. Scenario records retain hypotheses and assumptions with explicit capability gaps; they do not compute political or stakeholder effects.

The same operations are available through eleven allowlisted chat tools. For example: “Compare imported energy and tax bills as of October 1, 2026; show the overlap and unknown outcomes.” Chat needs the configured provider, but the direct organization/analysis screens work without paid model calls. No unrestricted web browsing or external message sending was added.

See [implementation plan](docs/intelligence-implementation-plan.md) and [full architecture/release roadmap](docs/INTELLIGENCE_ROADMAP.md). Predictive accuracy remains unvalidated; these workflows do not change the frozen research model or clear human audit gates.

## Chat workspace

The home page opens followed bills and meaningful legislative changes. Primary navigation is Home, Bills, Research and Chat, with a sidebar on laptops and a bottom bar on narrow screens. Bills searches imported official records and provides Follow, saved lists and the visual map. Research guides question, sample and readiness review; advanced controls remain available. Chat keeps persistent conversations and contextual bill questions. Use Connections in the sidebar to choose a tool-capable model, replace the locally stored API key, or test the connection. The existing key is retained when the key field is blank.

Try these prompts:

- “Show me our official sources and explain their coverage limits.”
- “Import H.R. 22 from the 119th Congress.”
- “Run a demo experiment for the 118th Congress at 180 days.”
- “Rerun the last experiment and compare its results.”

Completed experiments appear as clickable report artifacts with a small data-derived visual. Open the report for reliability bars, scores and per-bill availability; use Rerun to create a separate run without overwriting the prior report. The Experiments tab also lets you specify collection, Congress and checkpoint age directly. Results are scoped to that run, not accumulated across unrelated experiments.

Chats and reports persist in SQLite. Requests run in background workers; leaving a tab does not cancel the run. On server restart, interrupted requests become explicit failures with retry guidance. Already-created reports remain accessible. Sources supports searching, importing and refreshing official bills. Explore preserves the historical research view; Watching holds saved monitoring activity.

## Research-view journey

1. Historical replay opens the synthetic 118th-Congress collection.
2. Select a marker, search by issue, or choose Flat/Table. Filtering preserves the selected dossier and labels it when outside the visible filter.
3. Inspect evidence timestamps and source details. Open Analogs for the actual rows behind the reference rate.
4. Move the cutoff date. Forecasts are generated and locked on first access for eligible bill/date/model combinations. Repeat access returns the identical saved record, including its original input snapshot.
5. Reveal the actual outcome and its Brier score. Reveal does not mutate the forecast.
6. Open Research lab for descriptive scores, reliability bins and coverage. Results are not an untouched holdout.
7. Bill monitor uses official data at today's cutoff. Import/refresh a bill by Congress, type and number. Add it to the persistent local watchlist. Estimates remain unavailable until audited prior data supports them.

The numerical synthetic estimates are calculated by the model, but their inputs and outcomes are fictional. They establish pipeline behavior, not real forecasting performance.

## Architecture and protocol

- `docs/ARCHITECTURE.md`: architecture written before implementation, temporal contract, model assumptions, phase gates.
- `docs/PROTOCOL.md`: executable record semantics, audit imports and evaluation procedure.
- `docs/ROADMAP.md`: remaining research and deployment gates.
- `engine/store.py`: append-only evidence and immutable forecast ledger, SQLite WAL.
- `engine/ingest.py`: raw content-addressed snapshots, GovInfo imports, Congress.gov paginated sync, resumable audited JSONL.
- `docs/AUDITED_SAMPLING.md`: frozen population and sample selection, resumable imports, human audit receipts and sample-scoped experiment gates.
- `engine/sampling.py` and `engine/sample_research.py`: official directory inventories, immutable sampling records and exact sampled training/evaluation proposals.
- `engine/model.py`: as-of snapshots, family-deduplicated prior-Congress training, L2 logistic baseline and reference rates.
- `engine/evaluate.py`: separate label-reading evaluator entrypoint.
- `engine/ai.py`: OpenRouter extraction with exact-span checks and retained success/failure records.
- `engine/server.py` and `web/`: local HTTP API and responsive research workspace.

## Ingestion and research commands

```sh
python3 -m engine ingest 119 hr 22
python3 -m engine ingest 119 hr 22 --refresh
python3 -m engine import-xml /path/to/status.xml --source-url https://www.govinfo.gov/bulkdata/BILLSTATUS/119/hr/BILLSTATUS-119hr22.xml
python3 -m engine sync 119 --limit 20
python3 -m engine import-audited /path/to/reviewed-records.jsonl
python3 -m engine forecast demo-118-hr101 2023-07-01 --dataset demo
python3 -m engine backtest --dataset demo --test-congress 118 --age-days 180
python3 -m engine export data/predictions.jsonl --dataset demo
python3 -m engine evaluate data/locked-predictions.jsonl /separate-evaluator/labels.jsonl
```

Incremental discovery requires `CONGRESS_API_KEY`; an OpenRouter key is not a Congress.gov credential. GovInfo targeted imports need no API key. Sync checkpoints advance only after an entire page succeeds. Raw response hashes deduplicate repeated payloads. A bulk XML directory can be imported one file at a time using `import-xml`; Data & imports also supports resumable bulk jobs of up to 10,000 official bill IDs and reproducible samples from frozen GovInfo inventories. A complete historical backfill is not bundled.

Official XML imported today is known today. Historic action dates alone do not establish past availability; earlier replay will correctly show no eligible metadata. To enable legitimate historical research, import audited canonical records with archive proof. No public-law event does not establish a negative outcome. An adjudicated negative requires complete coverage through Congress end.

## OpenRouter

Copy `.env.example` to `.env`, set `OPENROUTER_API_KEY` and optionally `OPENROUTER_MODEL`, then restart the service. `.env` is ignored by Git and never served to the browser. The extraction button sends only the eligible event packet to OpenRouter. Default model: `openai/gpt-4o-mini`; change the environment value to evaluate another model.

A live smoke call succeeded and verified two exact source quotes. Exact quotation verifies a span, not the semantic correctness of every paraphrase. AI output cannot write official outcomes or change statistical probabilities. Inspect `ai_runs` in the local SQLite database for model, prompt, inputs, output, failures, usage, cost and latency.

## Verification

```sh
python3 -m unittest discover -s tests -v
node --check web/app.js
```

Tests cover late arrivals, future records, metadata versions, unresolved training labels, family deduplication, immutable records and backfill behavior, denominator integrity, unavailable predictions, deterministic fitting, idempotent official import, negative-outcome rules, AI source spans, probability scoring and prospective issue-time checks. Browser checks cover view switches, mobile layout, selection, comparisons, outcome reveal and official monitoring.

## Limits

This is a local research prototype, not a production forecasting service. It has no validated real-data calibration, 50-year corpus, authenticated multi-user hosting, full family adjudication, registered untouched holdout, macro/poll vintages, milestone timing models, or independently evaluated AI forecaster. Official stage mappings are deliberately conservative and require procedural audit before model use. No probability interval is claimed. The separate evaluator process is not a security sandbox; protect labels and scoring access with deployment permissions. Research diagnostics score the earliest saved forecast per bill and are not family-independent confidence estimates.

Fonts: Adobe Source Sans 3 and Source Serif 4, locally served under their included OFL licenses. Official integration references: [Congress.gov API](https://github.com/LibraryOfCongress/api.congress.gov), [GovInfo Bill Status](https://github.com/usgpo/bill-status), [OpenRouter chat completions](https://openrouter.ai/docs/api/api-reference/chat/send-chat-completion-request).

## Research rigor from chat

Research methods shows the full capability map, current release blockers, saved protocols and the original plan by section. Chat receives a versioned research contract on every request and can retrieve exact plan sections. Try:

- “Read the plan's evaluation requirements and tell me which are actually implemented.”
- “Audit our official data for historical availability, missing outcomes and family links.”
- “Register a demo development protocol: my hypothesis is that structured features improve Brier score over the historical rate, testing Congress 118 at 180 days.”
- “Run that registered protocol, then audit one of its saved forecasts.”
- “Compare these two run IDs on the same resolved cases; distinguish replication from improvement.”
- “Can we run an AI forecaster with macroeconomic vintages and a protected holdout?” — chat must identify the missing implementations, not silently run the basic baseline.

Protocols are immutable. Unsupported designs remain blocked; registration after matching experiments is labeled post hoc. Data-record fingerprints bind registered runs to their source snapshot. Experiment preflight blocks empty/unusable cohorts, and comparisons compute paired descriptive scores without claiming clustered uncertainty. Audit reports state precisely what was checked and what remains unverified. Original document versions are retained locally when protocols are registered.

Chat orchestration is broader, but the scientific methods that are marked unimplemented are still unimplemented. Full plan coverage in the research interface is not a claim of full engine completion or validated predictive skill.

### Reproducible real-data pilot

The first bounded real-data pilot is complete: [design](docs/cohorts/pilot-v1.json) and [audit/results](docs/cohorts/pilot-v1-results.md). It compares a publication-version model with a historical-rate baseline; it does **not** validate the general action-history model. The primary Brier result did not beat the baseline, and the cohort contains very few positive outcomes.

`python3 -m engine.cohort reproduce` rebuilds features/labels from the frozen local source bundle and verifies the locked result offline. `python3 -m engine.cohort prepare` prepares/resumes the prespecified source audit; `python3 -m engine.cohort run` publishes its result to the workspace. Chat and the report's rerun button reproduce the same frozen cohort. Current BILLSTATUS snapshots are also visible in Sources with their actual retrieval time, while historical publication provenance stays in the cohort audit bundle.

## Connected local workflow

The primary destinations are Chat, Collections, Explore, Experiments and Watching. Data & imports, Research methods and All source records provide supporting research tools; Connections holds model settings.

1. Start in Data & imports to discover a population, freeze an audited development sample and import its records. Use Check experiment readiness on the sample to preserve its exact sampled training/evaluation scope. In Collections, save up to 100 official or synthetic bill identifiers. Manage an existing collection to import missing official records or refresh all its records. Imports retain per-bill progress and failures; collection revisions preserve earlier versions.
2. Choose Start research, specify a hypothesis and checkpoint age, then review the frozen proposal. The collection determines exactly which test bills are evaluated; prior-Congress training remains separate. Missing historical metadata or outcomes block scoring when no eligible cases remain.
3. Run the proposal. Completed reports lead with model/baseline scores, with bill-level predictions, design and evidence checks expandable below. Revise one assumption, repeat the same settings, compare with the original, verify reproduction or download the research bundle.
4. Chat can perform these operations through allowlisted tools. Example: “Use Demo · workflow walkthrough, propose and run a 180-day session comparing the structured action model against its historical-rate baseline, then show the report.” Synthetic results demonstrate the workflow only.
5. Save bills with Watch bill, then open Watching. Check now refreshes official sources. Scheduled checks are off by default; opt in under Refresh and notification settings. The local server must stay running. Notifications are in-app badges/toasts, not email. The feed records meaningful changes, recovery and failures; unchanged retrievals do not count as changes.

Research bundles include frozen normalized records and source hashes, configuration, model inputs and outputs. They do not contain credentials, chat history, original raw payload bytes or an embedded Python runtime. Offline verification requires the recorded implementation. See [session contract](docs/RESEARCH_SESSIONS.md) and [collections/monitoring contract](docs/COLLECTIONS_MONITORING.md).

The saved walkthrough and official evidence-check sessions demonstrate a successful synthetic run and an honest blocked official historical run. They do not replace the separate audited real-data pilot or establish predictive skill.

## Automatic learning and background research

Completed research sessions now automatically produce a separate immutable adaptive-learning record. The fixed model's original result stays intact. The bounded search compares three regularization settings across two feature policies: the original six dated activity features, and those features plus deterministic topic/title hashing and stage/activity interactions. Normalization is fitted on inner training data. The later prior Congress supplies inner validation; related families are separated, and inner training labels must have been available before validation began. Target evaluation outcomes never select the candidate. Selected candidates are refitted on the full eligible prior training set; insufficient data retains the fixed prediction with an explicit reason.

Learning receipts record feature policies, trials, training hashes, artifacts, matched fixed/adaptive scores and reproducibility hashes. Repeating identical evidence reuses the decision rather than counting as new independent learning. Exported session bundles include adaptive receipts, and reproduction verifies both fixed and adaptive results. Legacy completed sessions do not acquire a new implementation's adaptation retroactively. There is no global production-model promotion, guarantee of improvement, or OpenRouter weight training. Full bill text, sponsor networks, committee membership and external economic information are not yet learned features.

The **Background research** page configures a persistent local queue over selected audited samples. It considers 90-, 180- and 365-day checkpoints, skips previously attempted unchanged evidence (including blocked cases), preserves every sample gate, and recovers interrupted work. Controls allow 1–10 jobs per cycle, 1–100 jobs per UTC day, intervals of 15 minutes to one week, and at most 20 selected samples. Pause takes effect between jobs. The local server must remain running; this is not an always-on hosted service. The worker neither imports sources nor makes paid LLM calls. Imported evidence and human audits remain separate inputs; newly eligible data is considered in later cycles.

For this workspace, the existing 100-bill sample has been enabled at a 60-minute interval, three jobs per cycle and 12 jobs per day. Its first three checkpoint checks were correctly blocked by historical evidence and audit requirements. A separate synthetic demonstration exercised adaptation and reproduced exactly; its adaptive score was worse than its fixed score, so no accuracy gain is claimed.

API: `GET /api/autoresearch` reads status; `POST /api/autoresearch/settings` updates the schedule. Chat tools `inspect_background_research` and `configure_background_research` use the same boundaries. Adaptive learning applies to the collection-scoped research-session runner; legacy quick experiments and live bill forecasts retain their existing fixed-model implementation.

## Priorities, campaigns and coverage

The default home is **My priorities**, with saved issue terms, organization context, watched bills and source changes. Matching searches imported titles/topics; organization names do not establish relationships or impact. **Bills & collections** opens the existing saved bill groups and visual map. **Research lab** organizes exact audited samples into campaigns, with goals, budgets, pause/resume, source blockers, matched evaluation contexts and in-app notifications. **Activity** brings import, audit, source, forecast-capture and research receipts together; it polls without discarding the user's filter. Supporting tools remain accessible in the sidebar.

Campaigns do not silently enable the global worker. Active campaign samples join its effective selection; both global and campaign budgets apply. Paused campaigns suppress their managed samples, and restarting a campaign does not replay unchanged evidence. Results from different evidence snapshots, checkpoints or scored memberships are not grouped as directly comparable. Repeated or overlapping evaluations remain development work, even within one comparison group. Intermediate automatic proposals remain stored but are hidden from the campaign run list.

**Data coverage** separates inventory, imported records, human audit and unknown model-specific eligibility. Complete-Congress import plans freeze inventory membership and source hashes, process batches of 250 sequentially, retain successful records, resume interrupted batches and require an explicit resume after a failed batch. Pause takes effect after the current batch. The current plan imports the complete saved 114th-Congress H.R./S. inventory: 10,074 bill records across 41 batches. The existing 100-bill sample stays frozen. Plan completion is shown from actual receipts; it does not imply historical eligibility.

Bill workspaces now expose source-backed related bills and official text-version links. Observed title/topic/sponsor/summary changes are distinguished from full legislative-text comparison; inline full-text diffs are not implemented. Current forecast captures retain dated evidence, source records, implementation hashes and an available estimate or explicit unavailable/ineligible reason. Refreshing watched official bills also attempts a capture. Resolved bills and ended Congresses cannot become prospective forecasts; synthetic receipts remain separate. Local receipt timestamps are not independent timestamp attestations.

The application remains local at the user's preference. Both import and research workers require the server to remain running; pending work is stored in SQLite and recovered on restart. Scheduled watched-source refresh is enabled hourly in this workspace. No external notification service or hosted deployment has been configured.

New API surfaces: `GET/POST /api/priorities`, `GET /api/activity`, `GET/POST /api/campaigns`, `GET /api/campaign?id=…`, `POST /api/campaign/update`, `GET /api/coverage`, `GET /api/coverage/plans`, `POST /api/coverage/plan`, `POST /api/coverage/update`, `GET /api/prospective`, and `POST /api/prospective/capture`. Chat tools expose priorities, campaigns, activity and coverage plans through the same validations. The existing model still targets own-bill enactment; committee/chamber milestone targets require separately audited definitions and are not silently substituted.

## Model learning workspace

Open **More tools → Model learning** to inspect or execute the existing adaptive learning workflow. Official and synthetic evidence have separate views. Prepare a research session from a saved collection, then inspect it and choose **Train and evaluate** when its frozen evidence is eligible. Completed runs retain their original models; repeat execution returns the saved result. Automatic learning settings opens the existing bounded research scheduler, which requires eligible samples and a running local server.

Each bill checkpoint exposes fixed/adaptive predictions, learned standardized logistic coefficients, feature policy, regularization and the earlier-Congress training/validation split. Export evidence and models downloads the existing reproducible research bundle. Context hash bins are not semantic explanations or causal effects. Different checkpoints can have different fitted models; this is not one global continuously updated weight vector.

This surface uses the existing `learning.py` implementation without changing frozen study hashes. It does not fine-tune the hosted language model, unlock missing official evidence, or promote experimental weights into live forecasting. Training history reports matched fixed/adaptive development scores and does not pool unlike populations. A lower development score is not independently validated improvement.

API: `GET /api/learning?dataset=official|demo`, `GET /api/learning/detail?id=…`, `POST /api/learning/train` with `{"id":"session ID"}`. Training preserves the research session's implementation, evidence, audit and idempotence gates. The history view filters the latest 100 research sessions.
## Passage90 research foundation (November 12, 2026)

Start with the [forecasting-first plan](docs/research/FORECASTING_FIRST_PLAN_V1.md), [separate protocol](docs/research/PASSAGE90_PROTOCOL_V1.md) and [execution receipt](docs/operations/runs/20261112-passage90-foundation.md). The new target is first originating-chamber passage in the 90 days after a day-30 checkpoint, restricted to complete windows before Congress end. The older enactment and passage-by-Congress-end workflows remain distinct.

The new ledger supports exact official BILLSTATUS/inventory capture, immutable registration/source receipts and local-only paired issuance through its Python API. It does not fit models or certify prospective research. A caller-supplied probability, at-risk assertion or family ID is not independent validation. The certified issuance path deliberately rejects until an external verification route exists.

```sh
# A new source-feasibility run makes up to 22 live official requests.
# It must use a new directory; the existing receipt and raw bytes are immutable.
python3 -m scripts.passage90_source_pilot --output data/research-runs/NEW-PILOT

# Verify an existing local ledger without network requests.
python3 -m engine.forecast_ledger verify data/research-runs/NEW-PILOT/ledger

# Focused contracts and adverse-input tests, including optimized Python.
python3 -m unittest tests.test_passage90 tests.test_forecast_ledger tests.test_passage90_source_pilot -v
python3 -O -m unittest tests.test_passage90 tests.test_forecast_ledger tests.test_passage90_source_pilot -v
```

Current-source inspection never backdates observations or fills missing passage labels with negatives. The source pilot is a small engineering check, not a trained forecasting system or a full census. Future operations still require reviewed labels/features/families, a fixed fitting manifest and passage-specific model artifacts, discovery/custody controls, independent timestamps and matured outcomes. No recurring capture schedule or live model promotion is enabled by these commands.
