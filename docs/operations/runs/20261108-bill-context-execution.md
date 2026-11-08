# Bill-context execution: real acquisition, design preparation and blocked model stages

November 8, 2026. User authorized execution of all stages of the [experimental plan](../../research/BILL_CONTEXT_EXPERIMENT_PLAN_V1.md). Executed the feasible source/preparation work and assessed dependencies for E0–E9. **This is not completion of all experiments.** Required human evidence gates prevent new fitting; prospective outcomes cannot be obtained now.

## Actual work and retained evidence

Added an isolated runner (`scripts.bill_context_execution`), read-only verifier (`scripts.verify_bill_context_execution`), design-review exporter (`scripts.bill_context_review_handoff`), focused tests and a [versioned record dictionary/annotation guide](../../research/BILL_CONTEXT_ANNOTATION_GUIDE_V1.md). No shared engine behavior changed. The runner is evidence preparation and gate assessment, not an implementation of all gated model experiments.

Runtime: `data/research-runs/bill-context-20261108-v1/` (ignored).

- Sealed 100-bill selection before acquisition: 20 per Congress 113–117, 50 design and 50 quality, global automated-family exclusion. Complete disposition ledger retains all 25,000 candidates. Family IDs still need qualified adjudication.
- Verified 326 retained metadata source references, then acquired 100 introduced XML renditions from exact official links in retained MODS. All 100 succeeded; 1,505,008 bytes retained with actual retrieval timestamps. No retrospective availability claim was made.
- Parsed 50 design bills, preserving full text and 213 sections, plus exact lexical-match spans for twelve mechanism categories. All mechanism labels remain null/unknown. Lexical matches are not assertions of what a bill does.
- Retained the 50 quality XML files without parsing their text or opening quality annotations. Quality evaluation waits for frozen design rules and independent human annotation.
- All 12 bills from the previous source packet overlap the design partition; none overlap the quality partition. The earlier packet remains unchanged and is not described as an independent pilot.
- Prepared 28,433 calendar-feature rows across three overlapping legacy training/evaluation folds. These are row appearances, not distinct independent bills. Exact core/calibration/evaluation identities are retained in `e1-unapproved-inputs.json`. No fitting or scoring is authorized by that file.
- User volunteered as first reviewer. Exported 50 readable design-review pages and an index, with no quality pages. Qualifications and actual annotations are not recorded; second independent reviewer and adjudicator remain unassigned. Volunteering is not evidence approval.

Registration digest: `318eca5e2797e8d09c14f5d8efe66bbe69e556b05e3861c3ea3f9f3f52fd0c5a`.
Result digest: `f8f4b2bfc2d82b7ef11e1bf4aa16a63a0c9a07baa054eabbfccbb5c250a7538e`.

## Stage dispositions

| Stage | Result and exact remaining dependency |
| --- | --- |
| E0 | Partial: selection, real source collection, design extraction, dictionary and annotation queue complete. Qualified annotation, historical rendition checks and field-quality acceptance remain pending. |
| E1 | Blocked before fitting. Legacy split and time arithmetic check out, but required subject-bound source/family/outcome reviews and methods population signoff are absent. |
| E2 | Blocked on E0 accepted categories and reviewed historical feature availability. |
| E3 | Blocked on text historical eligibility, matched population and sparse solver/dependency verification; current XML exists for pilot only. |
| E4 | Blocked on reviewed dated support/procedural feature matrices and shared evidence gates. |
| E5 | Blocked on reviewed announcement-vintage schedule and relationship matrices and shared evidence gates. |
| E6 | Blocked on qualifying feature results and anchor; no combination selected. |
| E7 | Blocked on E6 representation and registered/verified tree implementation. |
| E8 | Blocked on fixed selected encoding and reviewed temporally eligible initial training population. |
| E9 | Blocked on qualifying successor, shared preregistration/custody and future outcomes. Existing V1 remains unchanged. |

E1 existing populations: Congress 115 has 4,462 training / 2,717 evaluation rows; 116 has 6,591 / 2,792; 117 has 8,812 / 3,059. Every row in each combined fold has a pending introduction-review flag (7,179 / 9,383 / 11,871 appearances respectively); zero rows carry the required subject-bound review object. Reviewed positive-family floors are not established. Recorded temporal ordering and automated-family separation pass, but do not substitute for these reviews. The stage-status file reports missing prerequisites, not attempted model fits or measured negative predictive results.

## Validation and preservation

- Focused suite: **25 tests passed** (`tests.test_bill_context_execution`, `tests.test_paper_review_packet`, `tests.test_paper_evaluation`). Tests cover deterministic outcome-blind sampling, global-family shortfalls, date/timezone boundaries, identity mismatches, preserved Unicode/negation, unresolved reviews and existing corruption/immutability gates.
- Full regression suite: **307 tests passed in 57.302 seconds**, `python3 -m unittest discover -s tests -q`.
- Separate read-only replay checked all 326 metadata references and 100 XML hashes/receipts; all section hashes and lexical spans; exact recorded selection and split partitioning; all 28,433 time-feature rows; null annotations; and frozen artifact hashes. It is software verification, not independent human review or scientific validation.
- Review export check: exactly 50 design pages and zero quality pages. No approval written.
- Frozen survivor, challenger, original training and audited prior results matched before/after. Acquired/renewed/released a unique shared lease; no competing research Python job was observed at initial preflight.

Models fitted: **0**. New outcomes scored: **0**. Prospective forecasts issued: **0**. New bill-text downloads: **100**. No paid services, model promotion, scheduler changes or alteration of frozen evidence. Reaching the 75-fit ceiling is not a reason to bypass gates, and no new 60% performance claim is supported.

Next concrete work: user starts the design-review pages; recruit the second qualified reviewer/adjudicator, document qualifications, resolve historical-source/family/label evidence, then seal approved modeling registrations. The code intentionally has no switch to treat missing human approvals as passed.
