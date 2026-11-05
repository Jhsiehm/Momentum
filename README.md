# Momentum

A local-first workspace for researching U.S. federal legislation, monitoring bills, and testing legislative forecasts against dated evidence.

Momentum brings official-source imports, bill collections, research conversations, and reproducible experiments into one browser interface. It is an experimental research prototype: predictive accuracy has not been independently validated.

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

```sh
python3 -m unittest discover -s tests -v
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
