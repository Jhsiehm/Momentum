# Paper preparation infrastructure

`engine.paper_evaluation` is an isolated standard-library module. It does not alter the application, old evaluators, frozen research runners, worker settings or model artifacts. Real outcome scoring is deliberately blocked pending prospective ledger certification; synthetic fixtures exercise the scoring path. Do not interpret the API as a live study launcher.

## Artifact contract

- `register(spec, path)` creates an exclusive sealed registration with actual current time, code SHA-256s and fixed candidate order. The spec pins target, feature version, mode (`synthetic` or `prospective`), periods, paper protocol SHA-256, both full artifact digests, per-model training digests and baseline-training digest. Historical-independent mode is rejected because no such cohort is certified.
- `prepare(registration, cases, exclusions, models, baseline_training, source_root)` checks the complete candidate disposition, reviewed evidence bytes, target/day-180 timing, same cases, earlier training/label clocks, family separation, exact artifacts and six-dimensional model shape. It fits only the two prescribed simple baseline rates and creates sealed paired predictions. Evaluation cases contain no outcome labels. Call `save(path, prepared)` before any later label process; existing paths cannot be overwritten.
- `evaluate(...)` replays preparation and requires exact one-to-one labels, complete negative coverage, positive timing and source/review proofs. Synthetic mode requires `dataset=demo`; prospective requires `dataset=official` and an external custodian release bound to the prepared hash, then still blocks because issuance certification is not implemented. A pass flag is not a substitute for that missing ledger.
- `save`/`seal`/`unseal` provide exclusive JSON files and canonical hashes, rejecting nonfinite JSON. These are integrity controls, not filesystem permissions, cryptographic signatures or independently attested timestamps. Replays reuse verified inputs and compare outputs in memory; they do not overwrite files.

Cases carry `bill_id`, `congress`, `type`, `dataset`, `family_id`, `target`, `feature_version`, verified `introduced_at`, `cutoff`, `at_risk`, stage, six-element `x`, aggregate feature effective/availability bounds, source references and a review. A review binds the exact record excluding its `review` field, with reviewer, decision and retained evidence references. Source references contain relative/local `path`, SHA-256 and URL. The reviewer must certify constituent-level source availability, source semantics, risk status and family graph; aggregate timestamps alone are not proof. This adapter does not manufacture those reviews for legacy rows.

Training records add a separate `label` with exact identity/target, integer value, effective/available timestamps, source/review evidence, and complete coverage through Congress end for negatives. Row reviews bind the feature record without its separate label; labels have their own review. Preserve all source retrieval/observation metadata in the retained source receipts. External reviewer identity, source truth and historical provenance remain human review responsibilities.

Model inputs are `{survivor: {artifact, training}, challenger: {artifact, training}}`. The challenger `artifact` is the full candidate-lock JSON including its existing hash; its `model` contains `base` and `calibration`. Registration pins the digest of that **full** JSON. Legacy receipts instead call the digest excluding the self-hash the “candidate digest”; do not confuse these. No arbitrary retraining or recalibration is performed by preparation.

## Verification

```sh
python3 -m unittest tests.test_paper_evaluation -v
python3 -m scripts.paper_readiness_audit
```

Tests synthesize their own source bytes and reviewed fixture rows, not actual human certifications. They verify exact replay, stage/rate arithmetic, independently calculated Decimal probabilities/losses, BSS and calibration counts, corruption, duplicates/missing labels, future information, family overlap, model tampering, invalid dimensions, candidate dispositions, code locks, and blocked real scoring. No network or local research data is needed for those tests.

The read-only audit requires the existing ignored research bundles. It checks both frozen model identities and training memberships, reads saved counts and returns raw artifact hashes. Compare its JSON output to `READINESS_AUDIT_V1.json`. It does not reacquire sources, fit a model, calculate new real forecasts or score a final evaluation. Missing runtime files are an explicit reproduction prerequisite, not a reason to substitute fixtures as empirical evidence.

## Remaining implementation gates

A complete prospective experiment still needs reviewed source adapters, global family/exposure manifests, rolling census registration, atomic timestamp-attested day-180 issuance, protected label custody, clustered uncertainty verification and a publication-grade standalone numerical verifier. Current metric reports contain per-period Brier/BSS/log loss, fixed-bin calibration, class-specific Brier and equal-period losses; they make no inferential claim. The paper protocol specifies future uncertainty and decision rules without pretending they are implemented. The existing general-purpose `engine.prospective.capture` must not be used as if it issued this frozen four-method experiment.
