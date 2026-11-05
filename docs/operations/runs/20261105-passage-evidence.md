# Passage labels and day-30 evidence audit — November 5, 2026

Executed the user's request to build evidence, not another synthetic scoring run. New module `engine.passage_evidence` preserves immutable protocol, source receipts, per-bill decisions and machine-corroborated positive labels. Run with `python3 -m engine.passage_evidence` from the repository root. It uses the retained earlier700-bill cache and acquires missing official sources. Runtime artifacts are in `data/research-runs/passage-evidence-20261105/`; source files and local databases remain ignored.

## Results

820 fixed candidates: the prior exposed700-bill sample plus the first20 H.R. and20 S. numbers in each Congress110–112. The early-bill expansion is deterministic and not population-representative. No outcome-based replacements, no scoring and no final-holdout claim.

802 bill audits completed;18 HTTP404 source failures retained in the denominator. 64 positive passage labels corroborated, 584 day-30 publication-proxy records, and32 bills with both. Zero certified negative labels, zero complete historical action-history rows, zero human-certified rows. This is tangible evidence progress, not a ready-to-score sequential dataset.

| Congress | Audited bills | Corroborated passage positives | Day-30 publication proxy available |
| --- | ---: | ---: | ---: |
| 110 | 36 | 7 | 0 |
| 111 | 32 | 4 | 0 |
| 112 | 34 | 7 | 7 |
| 116 | 200 | 16 | 187 |
| 118 | 500 | 30 | 390 |

## Evidence rules and source meaning

[GovInfo's bill documentation](https://www.govinfo.gov/help/bills) identifies originating-chamber engrossed versions EH/ES as passed by that chamber. [The official BILLSTATUS repository](https://github.com/usgpo/bill-status) documents the status source and ongoing updates. Current XML is an audit/discovery source, not evidence that all its contents were historically available.

For positives, require a matching bill identity, LOC source-system9 action code8000 for H.R. or17000 for S., matching originating-chamber passage text, and an official EH/ES version issued on that first coded passage date. Confirm package identity and successful preservation events; compute a conservative historical availability bound with the existing one-day margin. Both action and publication evidence are retained in every label. Verification additionally checked that passage did not precede introduction. Labels explicitly record `human_reviewed: false` and their bounded publication provenance tier. This is automated source corroboration, not independent human certification or proof of the historical identity of every byte.

For day30, verify introduced publication identity/date, then include only versions with both issuance and conservative availability by the checkpoint. Exclude before-checkpoint passage, post-Congress checkpoints, missing introduction and late introduction availability. Store publication-based feature vectors and source hashes separately. These features are not the sequential engine's complete action-count features; no main-store observations were backdated or historical action histories invented.

732 rows lack corroborated passage and complete negative coverage; they remain unknown. Six coded passage cases lack same-date corroboration:118-HR7324,110-S1,110-S4,110-S5,111-HR12,112-HR1. The last has an engrossed issue date five days after its coded passage; it remains unresolved under the fixed same-date rule. Absence of an action or engrossed version never becomes a negative.

Checkpoint blockers:172 introduction publications not demonstrably available by day30,21 missing introduced publications,17 checkpoints after Congress end and8 already passed. Missing/late preservation evidence is reported as a limit on demonstrated availability, not proof that the bill was unpublished at that historical date.

## Validation and delivery

14 focused tests passed: six new evidence tests and eight sequential tests. Tests reject wrong chamber/system, missing-action negatives, mismatched positive dates, late introductions and future passage features. All802 successful audit rows were independently rerun offline; all2,664 retained source documents passed SHA-256 and length checks. The18 original HTTP404 outcomes cannot be recreated offline and remain recorded failures. The full `--offline` run fails closed if required uncached slots remain; successful-row reconstruction does not clear those missing slots. Dependency bytes/hashes retained locally. Audit hash: `2fce5055c105ed1a10980570b7d5a03306f063dd39c9ae37a2552bf3ae8f2a41`.

Three reports saved and API-verified in platform chat “Passage labels and day-30 evidence · audited source bundle”: passage audit, day30 evidence and verification. Positive JSONL: `corroborated-positive-labels.jsonl`; per-bill evidence and blockers: `audit.json`. These JSONL records are provenance-tiered candidate positives; do not treat them as an independently human-adjudicated complete label set.

## Remaining requirements

Complete negative action coverage and independent review remain missing. Congress110/111 supplies no day30 proxy rows under the evidence rule, and112 only seven. Family adjudication and complete historical action features remain unresolved. The official sequential benchmark therefore stays blocked; no accuracy score, production promotion or change to its gates. The existing700-bill evaluation material remains exposed. A later acquisition must register a new manifest rather than overwriting these frozen results.
