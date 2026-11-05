# Everyday workspace implementation plan

Keep the existing olive/paper visual identity and scientific gates. Simplify tasks, not evidence rules.

1. Home leads with search, followed bills and meaningful legislative changes. Aggregate source health; keep the full activity ledger.
2. Bills offers bounded local search by title/number/topic, Follow, saved lists and a visual map. Clearly state imported-data scope.
3. Research separates guided campaign creation from results. Name blockers with direct repair links; advanced scheduling stays in disclosures. Standalone reproducible studies remain discoverable beside campaign runs without mixing their methods.
4. Home / Bills / Research / Chat form the primary navigation. Laptop uses the sidebar; mobile uses a persistent four-item bar with a collapsible tools drawer. All controls have readable labels and touch targets. Preserve return context and browser navigation.
5. Bill pages lead with plain stage labels and source dates. Explain unavailable estimates simply, with exact rules retained. Deduplicate display events without discarding evidence. Add contextual Ask action.
6. Provide a local launcher, a useful disconnected-state message and honest monitoring status. Local operation still requires an awake computer and running app. No remote hosting or hidden startup services.
7. Validate backend search/gating, JavaScript syntax, browser routes, search/follow and return context, campaign reports, laptop and 390px mobile layout. Keep human reviews and unresolved family checks pending.

Acceptance: find an imported bill without knowing a collection ID; follow from search; return to the same search/map; distinguish source-service events from bill changes; see why research is blocked and where to act; find completed standalone reports; navigate every primary task on phone without horizontal page overflow.

## Implementation and verification

Implemented all seven workstreams in the local app. Backend suite: 172 tests passed. JavaScript syntax checks passed for shell, consumer flow, Research and map. Browser checks covered laptop Home, mobile Bills/Research, local title search, search preservation on reload and bill return, Research return routing, expanded drawer scrolling and research readiness. The static UI detector returned no findings in degraded regex mode, so it is not an accessibility certification.

Remaining: complete designated human reviews and family adjudication; validate forecasting performance on suitable historical evidence. Responsive layout does not expose the app to an actual phone: service remains loopback-only as requested. Real-device access and user testing remain separate next steps.
