# Research workspace visual contract
The supplied plan pins the visual direction: an olive/graphite cartographic research desk with warm paper for reading. Operate mode. A wide evidence landscape and adjacent dossier carry the first viewport; no marketing hero or decorative metrics.
Typography: locally served Source Sans 3 for controls and reading, Source Serif 4 for the page title. Etched fine rules, rectangular controls, a muted clay selection marker, ample reading gaps. The Explore map groups bills by policy topic on a shared tilted survey plane; prism height shows the latest evidenced legislative stage, not enactment probability. Flat view uses the same data as rows. Table view is the accessible full record alternative.
Selection is stable through filters, date changes and view changes. Every estimate says demonstration or experimental, names its horizon, as-of date and actual issue date. User action reveals outcomes separately.
Mobile stacks the inspector below the landscape and retains map pan, zoom and fit controls. Focus, empty, pending, unavailable and error states are first-class. Reduced motion disables authored transitions.

## Collection Explore map

The requested reference direction is a continuous warm-paper SVG isometric survey plane, with etched topic strips sharing one ground surface. Each visible evidence row contributes one labeled bill prism. Olive faces convey recorded stage; clay marks selection, and pale dashed faces identify unavailable evidence. Position within a topic arranges bills for reading and carries no additional metric. Replay controls sit below the map; the inspector sits alongside it on desktop and stacks below on narrow screens.

Dragging pans the map; zoom buttons and Fit map control its extent. Selecting a bill retains the current pan and zoom. Bill marks expose selection state and accessible labels, with visible keyboard focus, Enter/Space selection, arrow-key navigation and Home/End navigation. Flat and Table remain linked alternatives.

## Chat-first shell (user-requested update)
The main entry is now a simple Codex-like operating surface: persistent left sidebar, compact top bar, centered conversation, bottom composer. One Source Sans family carries the shell. The existing olive and warm neutral palette is retained with lighter chrome. Chat, Collections, Explore, Experiments and Watching are primary destinations; Data & imports, Research methods, All source records and Connections provide supporting views. Model settings are a dedicated view; credentials never appear in chat history. Experiments produce real report links and data-derived reliability visuals, with independent run identities. Mobile collapses the sidebar and keeps the composer accessible.

## Consumer bill overview
Sources and chat bill artifacts open a reading page within the shell. An identifier, bill title, evidence status and retrieval date precede a local watch control. The main reading column uses the retained official CRS summary, falling back explicitly to the source title. A quieter forecast column gives eligibility reasons or an experimental estimate. The timeline groups identical date/text entries for display while preserving all source records in the backend. Research metadata is progressively disclosed beneath it. Mobile stacks columns and timeline dates; native details controls preserve keyboard access. Watches persist locally, with optional scheduled refresh and in-app notifications while the local server runs.

## Connected research workflow

Primary navigation is Chat, Collections, Explore, Experiments and Watching, with Data & imports, Research methods and All source records as supporting tools. Collections use flat list rows and an explicit membership editor. Unexecuted sessions expose the design and preflight before Run; completed sessions lead with a shared-scale Brier comparison and put design, per-bill predictions and audit fields behind native disclosures. One-assumption revision and unchanged replication remain separate controls. Watching shows the schedule state, source freshness and dated feed; opt-in notifications use a sidebar badge and deduplicated toast. Narrow layouts stack forms and retain horizontal table scrolling. Desktop and 390px mobile reports were visually checked after integration.

## Sampling and shared icons

The shared SVG icon registry in `web/icons.js` gives shell navigation and actions consistent 24-unit geometry. Icons accompany readable labels; decorative SVGs are hidden from assistive technology. Page structure follows the task: Data & imports uses a progress queue beside a saved-record ledger, the sample builder uses numbered steps and a protocol sidebar, and sample detail separates imported records, readiness blockers and the human review form. The review form records evidence checks and notes without implying that a successful download establishes historical eligibility. Saved population and selection facts stay visible while users move between source evidence, audit receipts and experiment preflight.

## User-oriented navigation and research campaigns

My priorities is the initial reading/task surface; Bills & collections, Research lab, Activity and Chat are the primary destinations. The visual map, Data coverage, worker settings, experiment history and audit tools remain under Workspace tools. Priorities uses a reading column and quiet interest editor. Research lab separates campaign evidence/results from settings; meaningful notifications and fresh-result notices preserve in-progress edits. Activity uses a chronological ledger and persistent filters. Coverage uses a coverage ledger, per-Congress table and resumable import plans alongside population selection. Unknown eligibility is spelled out.

Long headings wrap within their flex column; small screens stack the settings panels. SVG icons come from the shared registry. Related-bill titles and additional relationships use native disclosures to avoid overwhelming the dossier. Captures explicitly distinguish an evidence decision from an available numerical forecast.

## Everyday navigation (November 2026)

This supersedes the earlier primary-navigation descriptions: Home, Bills, Research and Chat are the four main destinations. Laptop layouts use a scrolling sidebar; narrow layouts use a persistent bottom bar and a collapsible tools drawer. Home leads with followed bills and meaningful changes, compressing operational health into one summary. Bills searches imported official records with query-preserving return navigation. Research guides question, sample and readiness, with advanced controls disclosed. Exact evidence rules and unavailable-estimate reasons remain inspectable. Custom SVG icons retain visible text labels.

Checked at 1280×720 and 390×844. Mobile Bills and Research have no horizontal page overflow; the expanded tools drawer scrolls to Connections. Search survives reload and bill return. These are developer checks, not a user study or full accessibility certification.

## Model learning extension

Model learning inherits the olive/paper Operate shell and the Research ledger: fine horizontal rules, plain reading sections and labeled controls within the existing 960px content width. The evidence-type selector separates official records from synthetic demonstrations. Training history lists saved sessions with dates, fitted-case counts, fixed/adaptive Brier scores and blockers; the latest 100 sessions are filtered by evidence type, without pooling scores across populations.

Inspect training opens an inline detail section above the history. A bill-checkpoint selector exposes its cutoff, fixed/adaptive predictions, outcome, feature policy and regularization. The coefficient table pairs fixed and adaptive values by feature, uses tabular numerals and fine row rules, and scrolls horizontally within a keyboard-focusable labeled region. Explanatory text distinguishes standardized log-odds associations from causal effects or feature importance. Native disclosure holds training and validation evidence.

Inspection and completed training move focus to the detail heading; loading, errors and training progress have status or alert announcements. Historical availability and audit blockers remain visible, and blocked or already-trained sessions disable the training action. Empty histories and checkpoints without fitted weights explain the missing evidence. The surface describes local experimental forecasting updates: saved predictions stay locked, models are not promoted to production, and the hosted chat model is not fine-tuned.

Desktop detail was visually checked at 1280×720 in `.impeccable/review/learning-desktop.png`. The implementation inherits stacked research rows below 640px and constrains selects and table overflow; mobile behavior for this extension has not been browser-verified.
