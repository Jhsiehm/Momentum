# Momentum

A local-first workspace for researching U.S. federal legislation, monitoring bills, and testing legislative forecasts against dated evidence.

Momentum brings official-source imports, bill collections, research conversations, and reproducible experiments into one browser interface. It is an experimental research prototype: predictive accuracy has not been independently validated.

## Current research priority

Momentum now follows a [forecasting-first execution plan](docs/research/FORECASTING_FIRST_PLAN_V1.md). A separate [day-30 / next-90-day originating-chamber passage study](docs/research/PASSAGE90_PROTOCOL_V1.md) adds explicit target and population contracts, a strong stage/chamber/time-remaining reference, paired metrics, and an immutable source/forecast ledger. The [first source pilot](docs/operations/runs/20261112-passage90-foundation.md) collected 20 bills and was independently replayed; it produced no certified labels, fitted passage model or validated forecasts. Prospective launch remains blocked on reviewed evidence, model artifacts and independent timestamps.

The existing enactment programme evaluates own-bill forecasts at day 180. The [paper protocol](docs/research/PAPER_PROTOCOL_V1.md), [validation-readiness audit](docs/research/VALIDATION_READINESS.md) and [working paper draft](docs/research/PAPER_DRAFT_V1.md) distinguish exposed historical development from proposed prospective evaluation. No independent historical validation cohort is currently established; real scoring remains blocked pending evidence review and prospective controls. The [cross-Congress campaign receipt](docs/operations/runs/20261105-cross-congress-campaign.md) records the data, methods, limitations, and results. The separate [day-30 originating-chamber passage benchmark](docs/SEQUENTIAL_BENCHMARK.md) still requires additional evidence. Reliable forecasting improvement remains unestablished; research results do not automatically promote models.

The [experiment validity recovery plan](docs/research/EXPERIMENT_VALIDITY_RECOVERY_PLAN.md) separates source-integrity fixes, provisional bill annotation, protected quality evaluation and predictive testing. Candidate quotation coverage is not semantic accuracy.

## What you can do

- Import bill records from GovInfo and Congress.gov, inspect source evidence, and follow legislative changes.
- Organize bills around issue priorities, collections, and organization workspaces.
- Run historical research with information cutoffs, immutable forecast records, and explicit evidence eligibility checks.
- Compare fixed and adaptive statistical models, inspect saved results, and export reproducible research bundles.
- Use optional OpenRouter-powered research chat and evidence extraction.
- Schedule local monitoring and bounded background research while the server is running.

Official records and fictional demonstration data are kept separate. Missing evidence and unavailable forecasts are shown explicitly.

## Quick start

Requires Python 3.9 or later. The application uses the Python standard library and browser-native JavaScript; no package installation or frontend build is required.

```sh
git clone https://github.com/Jhsiehm/Momentum.git
cd Momentum
python3 -m engine serve --port 8765
```

Open [localhost:8765](http://127.0.0.1:8765). On macOS, you can also double-click `Start Workspace.command`.

The server binds to loopback. First launch seeds fictional demonstration bills. A fresh clone does not include downloaded government records, saved local research databases, or credentials. Local state is stored in the ignored `data/` directory. Keep the server running for scheduled work.

## Optional connections

Copy the example configuration and edit it locally:

```sh
cp .env.example .env
```

Set `OPENROUTER_API_KEY` for research chat and AI extraction; optionally set `OPENROUTER_MODEL`. Congress.gov incremental discovery requires a separate `CONGRESS_API_KEY`. Targeted GovInfo XML imports do not require an API key. Restart the server after changing configuration. Provider calls may incur charges.

Never commit `.env` or API keys. You can use direct research and organization screens without a paid model connection.

## Development

The application itself needs no third-party packages. The complete research test suite also needs the pinned numerical packages in an isolated environment:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-research-text-v1.txt
.venv/bin/python -m unittest discover -s tests -v
node --check web/app.js
```

Node.js is needed only for JavaScript syntax checks, not to run the application.

| Directory | Purpose |
| --- | --- |
| `engine/` | Python service, ingestion, evidence store, models, and research workflows |
| `web/` | Browser interface and locally served fonts |
| `tests/` | Automated regression tests |
| `docs/` | Architecture, research protocols, plans, and operational receipts |
| `scripts/` | Local launch utilities |

See [repository instructions](AGENTS.md) for the commit and progress-log workflow.

## Documentation and progress

- [Historical corpus inventory audit](docs/operations/runs/20261108-bicam-inventory-audit.md): verified bounded acquisition; preserved parser failures and 43 missing identity/date records. Sampling and predictive use remain blocked pending source reconciliation.
- [Retrospective text diagnostic](docs/operations/runs/20261108-retrospective-text-diagnostic.md): four real-data fits on selected historical subsets; small, inconclusive text gain over the structured anchor, worse Brier loss than the stage reference. No validated forecasting or promotion claim.

- [Bill-context experimental plan](docs/research/BILL_CONTEXT_EXPERIMENT_PLAN_V1.md): staged research into bill meaning, text, political context, timing and controlled updates; proposed experiments, not measured gains.
- [Bill-context pilot execution](docs/operations/runs/20261108-bill-context-execution.md): 100 official texts acquired, design review prepared; the original forecasting programme remains gated on evidence reviews.
- [Reciprocal agent audit](docs/operations/runs/20261108-context-peer-audit.md): source, methods and software reviews, peer challenges, verified repairs and unresolved scientific gates.
- [Exploratory calendar results](docs/operations/runs/20261108-exploratory-calendar.md): nine real fits; small mixed gains, no qualifying lead or model promotion.
- [Context-triage experiment](docs/operations/runs/20261108-context-filter-experiment.md): flagged 322 of 2,727 hits while preserving 449/501 reference-quotation coverage; flags are review aids, not legal labels.
- [Expanded candidate-rule experiment](docs/operations/runs/20261108-expanded-candidate-rules.md): fixed-reference locator intersections increased 401→449/501, with 73 added hits; semantic accuracy remains unestablished.
- [Reference v3 and context extractor v2](docs/operations/runs/20261108-reference-v3-context-v2.md): eight separately adjudicated corrections and a forty-bill structural-context run, with unchanged lexical output.
- [Candidate error review](docs/operations/runs/20261108-candidate-error-review.md): source-based review of all 102 locator misses and five suggestions, with separate reference questions and archival follow-up.
- [Design-only mechanism extractor](docs/operations/runs/20261108-design-extractor.md): forty-bill candidate run, explicit abstention and tested effect-matching machinery; no predictive accuracy claim.
- [Larger corpus and readiness](docs/operations/runs/20261108-large-training-corpus.md): 1,000 additional sources, postselection class coverage, historical-rendition audit and extractor evaluation draft.
- [Corrected meanings and source expansion](docs/operations/runs/20261108-mechanism-corrections-and-coverage.md): separate corrected dataset and 200 new bill texts; readiness limits remain explicit.
- [Mechanism and direction review](docs/operations/runs/20261108-mechanism-rubric-v2-resume.md): all 40 design bills annotated and cross-reviewed; corrections and uncertainty preserved before predictive use.
- [Bill-meaning design pilot](docs/operations/runs/20261108-mechanism-design.md): independent agent annotations and reciprocal challenges; uncertain labels retained before predictive use.

- [Workspace guide](WORKSPACE_GUIDE.md): detailed workflows, command examples, and implementation notes. Saved-workspace observations describe development history, not data bundled with a clone.
- [Architecture](docs/ARCHITECTURE.md) and [research protocol](docs/PROTOCOL.md).
- [Roadmap](docs/ROADMAP.md) and [intelligence roadmap](docs/INTELLIGENCE_ROADMAP.md).
- [Changelog](CHANGELOG.md): repository milestones.
- [Development log](docs/DEVELOPMENT_LOG.md): changes, verification, and follow-up work.
- [Research operations status](docs/operations/status.md): research findings and audit receipts. Referenced local data artifacts are not bundled.

## Research limitations

Momentum is not a production forecasting service. Historical availability, outcome coverage, family relationships, and human audit gates constrain which records can be used. Synthetic results demonstrate software behavior, not real-world forecasting skill. Development comparisons do not establish independent validation or justify promoting experimental models into live forecasts.

The application has no authenticated multi-user hosting. Organization profiles are local organizational labels, not access-controlled accounts. Current background work requires a running local server.

## Font licenses

Bundled Source Sans and Source Serif fonts include their licenses in [`web/fonts/`](web/fonts/).
