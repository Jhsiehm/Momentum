# Live-agent research workflow: real-source review and exposure gate repair

November 5, 2026 (America/New_York). User explicitly requested a real workflow with live agents. This run advanced source-review preparation using retained official evidence; it did not repeat only synthetic tests or claim new predictive performance.

## Round 1 — evidence and methods

- `/root/source_audit`: [source report](../../research/reviews/20261105-source-audit.md). Independently audited 12 final-training bills selected by canonical JSON SHA-256 of bill ID, then bill ID, without selecting by outcome. Verified 40 distinct retained source files (4,376,740 bytes), 14 package versions, identity/introduction metadata, normalized UTC preservation events, availability bounds and feature-eligible package membership. Machine checks passed; original human-review flags remain unsatisfied. Source receipts lack per-source parser-version fields, and preservation bounds cannot prove historical byte identity.
- `/root/methods_audit`: [methods report](../../research/reviews/20261105-methods-audit.md). Verified actual survivor and candidate memberships, hashes, 9,496/2,375 core/calibration separation, known family boundaries and recorded temporal eligibility. All 12,749 eligible publication versions remain without satisfied human introduction-review flags; current retrieval timestamps are preserved. Original survivor training rows lack an explicit label-availability field for the new adapter. Exposed development membership cannot become independent validation.

The bounded advancement was to assemble an actual evidence-review packet, with reproducible source resolution and explicit pending human work. The methods agent also found a concrete software gap: training-family separation did not implement the protocol's separate exposed-development identity/family exclusion rule.

## Execution

Added `scripts.paper_review_packet.py` and its tests. The exporter freezes its deterministic selection and code/training hashes before byte checks, resolves only exact matching retained scale/reserve source bytes and sidecars, retains all versions with explicit feature-use flags, and saves immutable sealed output. A missing/corrupt source blocks the packet and leaves a separate failure receipt. Identical replay compares without overwriting; changed code/selection/results fail closed. No structured outcome, prediction or score fields are exported. Raw retrospective source documents may themselves contain later outcomes, so the packet is not an outcome-blinded holdout.

Actual packet: `data/research-runs/live-paper-review-20261105/packet.json` (ignored).

- Packet digest: `5d4f1fe361e9efe466b9850bd671ba836c61cc0f6285a619378abf780d3fc8e1`.
- Protocol digest: `38d34f93dc2e2f03980e2443b37f7e3226ddf7045ea18591bd1392686eb9a69e`.
- 12 cases, 40 source references, 14 versions; all human review decisions pending.

Fixed the methods finding in `engine.paper_evaluation`: new registrations require an exposure registry with bill IDs, family IDs, scope and a subject-bound review. Preparation verifies review evidence bytes and rejects declared exposed-development overlaps. New tests cover a missing registry, bill/family overlap and tampered review. This enforces declared exposure only; it cannot certify registry completeness, family correctness or reviewer qualifications. Existing immutable registrations/results were not migrated or edited, and prospective scoring still blocks.

## Round 2 — independent implementation review

`/root/independent_verifier` reviewed the exporter, independently reconstructed the selected IDs and exported fields, and checked every retained source/sidecar. No blocking exporter defect found. The methods agent independently reviewed the exposure-gate repair and reran all 16 paper-evaluation tests successfully, preserving its pre-fix finding and appending the disposition.

## Round 3 — independent replay and final checks

The verifier executed both other agents' embedded reproduction scripts against actual retained evidence, verified packet/protocol hashes, performed byte-identical replay, and reran the corrected 20-test focused suite. Its [verification report](../../research/reviews/20261105-independent-verification.md) records a passed software/artifact-integrity verdict with scientific limits. An initial verifier command named a nonexistent test module; it was corrected and disclosed. No failed check was hidden or counted as passed.

Root validation: **302 tests passed in 188.321 seconds** with `python3 -m unittest discover -s tests -q`. Focused 20-test run also passed. Real packet replay returned the same digest; frozen artifact audits matched before/after creation and independent replay. Diff whitespace and research-document link checks passed. No frontend changes required UI checks.

## Operations, preservation and release decision

Shared lease owner: `live-paper-review-20261105-01a1ae51`; acquired and renewed during work, released at completion. Read-only local `/api/learning`, `/api/autoresearch` and `/api/monitoring` checks returned HTTP 200. Autoresearch reported six blocked jobs and a running scheduler; no job/settings changes were made. No competing source acquisition was started.

Sources downloaded: 0. Models fitted: 0. New real outcomes scored: 0. Prospective forecasts issued: 0. No paid provider calls, model promotion or recurring-schedule changes. Existing source bytes and model/results were read only; new runtime evidence stays ignored. The agents' judgments are machine audits, not designated human certifications.

**Decision:** real evidence-review preparation and the scoped gate repair pass verification. Independent scientific validation remains blocked. Next work is source/parser lineage association, reviewed global exposure/family manifests and a genuine paired day-180 issuance system with independent custody; do not manufacture missing survivor label times or historic forecasts. A human source/family reviewer can now inspect the concrete bounded packet. More favorable historical scores would not clear these gates.
