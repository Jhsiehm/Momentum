# General legislative intelligence implementation

## Purpose
A local, evidence-backed operating workspace for organizations tracking federal bills, with a reusable research engine accessible through chat and direct controls. Preserve the existing olive/paper UI, mobile navigation and visual map. Separate relevance, user-assessed impact and modeled likelihood.

## Architecture and sequence
1. Audit existing temporal evidence, monitoring, saved experiments and chat tools. Do not change frozen historical study implementations.
2. Add a firm workspace domain: versioned organization profiles, explicit title/topic matches, assignments and notes, sourced stakeholder positions, and immutable briefing snapshots. Reuse official imports and meaningful monitoring receipts.
3. Add a general intelligence domain: validated structured filters, cohort intersections, resolved/unknown outcome accounting, immutable evidence packets, comparable saved forecast rankings, and explicit scenario assumptions/gaps. Never invent probability changes for unsupported interventions.
4. Expose the same domain functions through local HTTP and allowlisted chat tools. Chat interprets and explains; deterministic tools calculate and return evidence.
5. Extend Home with organization workspace entry and Research with evidence analysis entry. Add responsive organization and analysis surfaces, report retrieval/export and clickable source/bill links. No separate UI for every possible question.
6. Test correctness: unknown is not negative; current facts cannot leak into historical features; empty cohorts produce no fake rates; stale/resolved/incompatible predictions cannot become a ranking; stakeholder assertions remain user-recorded; profile updates detect conflicts; briefs preserve original evidence.
7. Integrate and test API/tool parity, offline tool use, syntax and existing regression suite. Browser testing is bounded and subject to the current browser policy; disclose if blocked.

## Delivery boundaries
The local app can provide useful monitoring, descriptive comparisons and reproducible evidence now. This implementation does not establish validated predictive skill, election causality, arbitrary natural-language statistical models, authenticated collaboration, state legislative coverage, external alerts or unrestricted internet browsing. Those are separate engineering and scientific release gates, detailed in INTELLIGENCE_ROADMAP.md. The app must disclose these limits at the relevant action, without claiming missing features are operational.

## Delivered in this implementation

- Additive intelligence and firm-workspace modules, local API routes and eleven allowlisted chat tools.
- Responsive organization workspace and evidence-analysis/report views, linked from Home and Research.
- Immutable evidence packets/briefs, CSV-free structured filtering, exact disjoint overlaps, unknown outcome accounting, saved-receipt comparability gates, user-recorded stakeholder citations, and optimistic edit conflicts.
- Scoped independent reviews corrected overlap semantics, historical cutoff navigation, stale asynchronous UI feedback and SQLite replacement immutability guards.
- Full regression suite passed 191 tests before final hardening; the final new-module/API/tool suite passed 23 tests after hardening. JavaScript syntax and Python compilation passed. Local capability/profile/report endpoints returned HTTP 200 after restart.
- Browser visual verification could not run because the browser tool previously rejected this localhost target under its URL policy. Responsive CSS was reviewed statically; new screens are not claimed browser-verified. The mechanical detector returned no findings in degraded regex mode, not a full accessibility pass.

No real profile, fabricated stakeholder evidence or test briefing was inserted into the user's database. Mutation journeys were tested in isolated temporary databases. The live server remains loopback-only.
