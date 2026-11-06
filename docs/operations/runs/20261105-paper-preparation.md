# Paper preparation and independent-validation audit

Date: November 5, 2026 (America/New_York). Scope: audit, formal protocol, first paper draft and isolated future-evaluation preparation. No new final outcomes scored, hyperparameters searched, model refitted/promoted, source imported or scheduled setting changed. Existing frozen research artifacts were read only.

## Audit finding

The 49-case survivor has one training enactment and was retained after mixed/negative development updates. The 30,500-candidate campaign's 2,315-case/29-positive comparison is effectively tied on primary Brier, with a conditional interval crossing zero. Chronological updates improve two exposed periods and worsen one. Converged L2=0.05 improves three exposed period-specific controls by 8.3911% on average, but has not independently beaten the survivor. Both frozen model digests and final training membership were rechecked; no result was regenerated as a new empirical test.

No historical period is established as a genuinely unexposed forward evaluation of the selected candidate. Unused 118 bill identities cannot undo calendar exposure, repeated selection and period-level adaptation. Earlier 110–112 passage evidence is a different target and precedes training; 119 is already partly imported and unfinished. Future 120–121 shadow evaluation is the proposed scientific route, not a currently running experiment.

## Deliverables

- `docs/research/PAPER_PROTOCOL_V1.md`: explicit estimand, four-method comparison, stage baseline, frozen-model lineage, prospective sequence, uncertainty, practical success/failure/inconclusive rules and publication limitations. Preserves original event-count floors as readiness gates, not power guarantees; explicitly records the fixed-artifact family exclusion choice versus the earlier proposed pre-fit purge.
- `docs/research/VALIDATION_READINESS.md`: exposure history, non-additive event counts, evidence tiers and exact blockers.
- `docs/research/PAPER_DRAFT_V1.md`: substantive introduction, related-work verification questions, methods, exploratory findings and limitations; no invented references.
- `docs/research/INFRASTRUCTURE.md` and `READINESS_AUDIT_V1.json`: API/schema documentation and deterministic aggregate artifact audit.
- `engine/paper_evaluation.py`: exclusive sealed manifests, code/model/training/source hashes, common cases, earlier-only fixed rate/stage baselines, strict timing/family/label checks and synthetic metric reports. Real scoring is deliberately blocked pending certified prospective issuance, even with a supplied custodian receipt.
- `scripts/paper_readiness_audit.py`: read-only model/training/fold audit; no fitting or new scoring.
- `tests/test_paper_evaluation.py`: synthetic replay, independent Decimal arithmetic and adversarial gate checks.
- Public README, changelog, development log and operational status updated.

## Review scope and limits

This was a single-author preparation task, not a scheduled three-round research cycle. No independent agent or human review is claimed. Diff review and separate Decimal arithmetic are implementation/numerical checks only. All 15 focused tests use synthetic source/review fixtures and cannot satisfy human evidence gates. Runtime corpus/private chats/raw government files remain outside Git. Raw byte hashes for the nine inspected frozen artifacts appear in `READINESS_AUDIT_V1.json`; the full historical source corpus was not rehashed in this task.

The existing live prospective capture uses arbitrary capture age and a different model/input path. It cannot be repurposed by relabeling receipts. No paired day-180 ledger was activated or backdated. Required follow-up is reviewed adapters, family/exposure manifests, rolling census registration, independently attested atomic issuance, protected label custody and verified clustered inference. The runnable next check is synthetic preparation/replay; the next scientific study is specified but blocked.

## Decisions requiring human involvement

Designate an independent outcome custodian and qualified source/family reviewers, arrange external preregistration/timestamping, and accept the proposed multi-year prospective timetable or commission a separately audited alternative. Routine documentation, implementation and verification required no additional permission. No affirmative result is required; negative and inconclusive outcomes remain valid publication results.

## Validation completed

- Final complete suite: `python3 -m unittest discover -s tests -q` — **297 tests passed in 62.580 seconds**. Earlier iteration also passed 294 tests in 95.944 seconds; the final run includes the added gate regressions on unchanged final source.
- Focused suite: 15 tests passed, including exact paired replay and independent 45-digit Decimal probabilities, Brier/log loss, BSS and calibration reconciliation.
- `scripts.paper_readiness_audit.audit()` exactly equals committed `READINESS_AUDIT_V1.json`; both frozen model hashes and the inspected artifact byte hashes remain unchanged.
- Python compilation and local-link checks for all four research Markdown files passed. Staged diff whitespace check passed. No frontend changes or browser checks required.
- Source review found no need to modify prior frozen modules/results. New code rejects shape mismatches instead of allowing the underlying generic predictor's zip truncation; the existing predictor is preserved for historical replay.

Conclusion: research-preparation software and documentation verified; independent predictive validation remains unestablished, and real scoring remains blocked.
