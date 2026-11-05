# Sequential passage benchmark implementation — November 5, 2026

Implemented the separate day-30 originating-chamber passage development benchmark described in `docs/SEQUENTIAL_BENCHMARK.md`. Existing enactment predictions, immutable research evidence, audit gates, and automatic worker configuration were not changed.

Validation completed:

- Eight focused tests passed on the final source: deterministic replay, forward training growth, same-case scoring, test-label isolation, late-label exclusion, family separation, negative-label requirements, duplicate-label rejection, missing-label accounting, early-passage exclusion, sparse folds and unfinished Congresses.
- CLI smoke test used a temporary synthetic database and explicit audit date. Two runs returned the same identity and reused exactly one content-addressed report.
- CLI help, Python compilation and diff whitespace checks passed.

An initial full-suite run failed the source-sensitive reproducibility test while this task was editing the hashed module. The final focused run passed; a full-suite rerun is recorded in the development log.

No official passage benchmark was scored. Existing enactment labels do not supply complete audited passage labels. Label acquisition/adjudication, multi-Congress historical feature coverage, clustered uncertainty and protected final evaluation remain prerequisites for the scientific milestone. All reports remain development-only and ineligible for release. The synthetic fixture validates software behavior, not forecast quality.
