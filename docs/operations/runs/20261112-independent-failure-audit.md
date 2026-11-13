# Independent failure-path audit — November 12, 2026

Starting commit: `e61d0bf9f086ae96cd0ad381455d477d3896b969`; isolated worktree and branch `codex/failure-audit`. Two separate agents reviewed evidence and executable runtime failures, then cross-reviewed the other implementation and the capture-clock repair. These are agent/software reviews, not independent human/source/statistical certification.

## Findings and repairs

- **P1: identity validation disappeared under optimized Python.** `engine/passage_evidence.py:audit_bill` used `assert` to bind a requested bill to source identity. A mocked official XML for bill2 requested as bill1 rejected normally but was accepted under `python -O`. Explicit ValueError checks now enforce identity, introduced-version cardinality and existing frozen-output equality under both interpreters. The subprocess test includes a valid matching control. Production data were not modified.
- **P1: offset timestamps bypassed scoring chronology.** The real evaluation CLI accepted cutoff `2025-01-01T01:00:00Z` against resolution `2025-01-01T02:00:00+05:00`, although resolution was actually earlier. All comparison timestamps now normalize through the existing UTC timestamp function.
- **P2: duplicate outcomes silently overwrote.** Two contradictory labels for one bill were collapsed by dictionary construction. The CLI now rejects duplicates before pairing or scoring.
- **P2: malformed unpaired predictions escaped validation.** Every row now requires identity, family identity, finite numeric probability in [0,1], and valid timestamps, even when its outcome is unresolved. Boolean probabilities/labels now reject explicitly. Nonfinite/range rejection for paired rows was already present; it is not claimed as a newly discovered paired-case bug.
- **P2: a rollback during capture could issue a backdated receipt.** The legacy recorder now rejects a clock earlier than its capture cutoff before persistence, with a second check after available-forecast persistence. The unavailable-control test verifies no receipt is inserted on rollback and that a valid later capture still succeeds. This does not establish clock trust across runs or independent timestamp attestation.

## Reproduction and validation

`python3 -m unittest tests.test_audit_runtime tests.test_audit_clock tests.test_audit_evidence tests.test_passage_evidence tests.test_prospective tests.test_sequential tests.test_paper_evaluation -q` passed 43 tests before the final additional post-persist clock check. Final full-suite result is recorded in the development log.

`python3 -O -m unittest tests.test_audit_runtime tests.test_audit_clock tests.test_audit_evidence -q` passed eight test methods after final changes. The CLI harness explicitly propagates optimization to child processes. The source-identity test independently runs normal and optimized children.

Six CLI test methods execute the actual `engine.__main__.main` entrypoint in subprocesses with temporary files/database roots. The valid one-row synthetic control scores Brier 0.64 for p=0.2,y=1. A second valid control retains one unresolved prediction without turning it into a negative. Negative cases cover duplicates, offset chronology, booleans, NaN/infinity and out-of-range probabilities. No HTTP service or live official acquisition is claimed.

Two disposable copies were mutated separately: removal of the clock guard caused the clock test to fail; removal of duplicate-label rejection caused the CLI duplicate test to fail. Both mutations were detected. Originals were untouched; local outputs remain ignored at `data/audit-mutations/result.json`. The source normal/optimized identity counterexample separately demonstrates the original disabled-assert weakness.

## Remaining limits

Legacy passage output creation still has a check-then-write race; equality checks are not concurrent exclusive creation. The legacy prospective recorder remains locally timestamped, arbitrary-age, and neither atomic paired research issuance nor external attestation. `sequential.prepare` does not explicitly require label availability to follow its effective date, although both dates separately gate training. This audit does not comprehensively test all HTTP routes, thread/process races, source schemas, historical bytes, families or label semantics. A fresh clone lacks the prior ignored research corpus.

No real model was fitted, real predictive test performed, target changed, research gate released, model promoted or paid provider called. The synthetic controls establish rejection and valid execution behavior only. The parent's new passage90 and forecast-ledger implementations are separate work and require review of their final commit.

Final verification: all 43 focused tests passed after final changes. Full discovery ran 788 tests in 107.500 seconds, with 14 errors and seven skips; it did not pass. This Python environment lacks optional NumPy and the fresh checkout lacks ignored research fixture data (confirmed zip-result.json missing). No dependency installation or reconstruction of old runtime artifacts was attempted. Python compilation and diff whitespace checks passed.
