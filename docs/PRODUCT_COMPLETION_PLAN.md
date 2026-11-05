# Local research workflow delivery plan

24 October 2026. User requested parallel agents to implement the connected workflow.

## Architecture and ownership

- Collections and import jobs: versioned named bill lists, bounded official import workers, honest coverage counts.
- Research sessions: immutable proposal, frozen evidence universe, exact selected test cohort, fixed prior-Congress training, explicit execution, one-assumption revisions, comparison and export.
- Monitoring: persisted opt-in preferences, local scheduler, semantic change feed, refresh failures and staleness. No external notification service.
- Product interface: Chat, Collections, Experiments, Watching; research audit and replay remain accessible. Existing bill pages and run history remain intact.
- Integration: allowlisted chat tools and HTTP routes; server lifecycle recovery; no arbitrary SQL/URLs/generated execution.

## Acceptance

1. Save a collection, inspect imported/missing coverage, and run a bounded bulk import with per-bill results.
2. Propose a session from that collection; see exact target, cutoff rule, baseline, cohort and preflight before execution.
3. Execute eligible sessions; unavailable historical evidence yields a useful blocked result, never fabricated probabilities.
4. Reproduce from frozen evidence; current source refreshes do not mutate past experiments. Change one assumption in a child session and compare honestly.
5. Download a research bundle containing the design, inputs, model/results and reproducibility identifiers.
6. Watch a bill, manually refresh or opt into scheduled local refresh, and inspect dated changes/failures. Disabling monitoring stops future scheduled fetches.
7. Reach these operations from chat through verified artifacts and show a concise computed result.
8. Check desktop/mobile rendering, keyboard semantics, errors, worker recovery and offline deterministic tests.

## Research boundaries

The separate publication-version pilot remains a development result with no established improvement over its baseline. New workflow features do not promote either model to validated status. Existing cohort.py, model.py, store.py and ingest.py are held unchanged to preserve that pilot's code fingerprint. Expanded cohorts and protected holdouts require their own registered sampling design, audited sources and actual evaluation; they must not be represented as completed by a UI feature.

This is a single-user loopback application. Scheduled work runs while its local server is running; external notifications and unattended hosted operation are outside this deployment.
