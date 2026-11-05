# Sequential passage benchmark v1

The active engineering milestone is a credible forward learning curve for originating-chamber passage by Congress end, predicted 30 days after introduction. Existing product surfaces are maintenance-only while this research question is unresolved. The enactment protocol and existing forecasts remain unchanged.

This first implementation is a **development benchmark**, not a registered final evaluation. It does not establish improved predictive validity. Do not use its output to select models for an already inspected final holdout.

## Run

```sh
python3 -m engine.sequential data/passage-labels.jsonl \
  --database data/engine.sqlite --start 110 --first-test 113 --last-test 118 \
  --as-of 2026-11-05 --output-dir data/sequential
```

Use `--dataset demo` only for synthetic software checks. A fresh clone has no official research corpus. The six tests in `tests/test_sequential.py` generate synthetic data locally and require no downloads or credentials.

The command writes a content-addressed JSON report exclusively; an existing report cannot be overwritten. Reports contain code hashes, label-manifest hash, exact snapshot/evidence identities, training manifests, fitted artifacts, inner-selection trials, per-case predictions, exclusions and per-Congress metrics. Keep these runtime files in ignored `data/`.

## Label contract

Provide one JSON object per line, one per bill, with these fields:

- `bill_id`: matching a bill in the selected evidence dataset.
- `target`: exactly `originating_chamber_passage_by_congress_end`.
- `value`: integer 0 or 1.
- `effective_at`: first originating-chamber passage date for positives; Congress end or later for negatives.
- `available_at`: when the adjudicated outcome was demonstrably knowable, supported by the audit record. Do not backdate a modern observation without historical provenance.
- `source_url`, `source_hash`, `audit_note`: provenance of the adjudicated action record, including the historical availability justification. These are operator assertions, not automated source verification.
- For negatives, `complete_coverage: true` and `coverage_through` at least Congress end, based on audited complete action history.

Use the originating chamber for the bill type, not a vote in the other chamber, an amendment vote, or passage of a related vehicle. Enactment resolutions are not passage labels. Missing labels are exclusions, never assumed negatives. Bills passing by the checkpoint are excluded, including when the later audit reveals passage not visible in the checkpoint evidence. Date-only timestamps follow the existing end-of-day UTC rule.

## Experimental design

The default initial training interval is Congresses 110–112; evaluation advances through 113–118. Fit once at each Congress opening using only earlier Congresses and labels both effective and available by that origin. This deliberately waits until the next fold to incorporate new labels. Freeze the initial structured model for all folds. Compare it with a structured model retrained on expanding data, a Beta(1,1) historical-rate baseline, and the existing bounded adaptive selector (six configurations, latest prior Congress as inner validation).

Training has one bill per family and excludes families appearing in the current or future evaluation folds. The frozen model excludes all evaluation families. Earlier test outcomes can enter later training only after becoming knowable. Inner validation retains the existing prior-only label timing gates. Sparse inner splits retain the fixed model; sparse outer splits are explicitly blocked. Twenty training families and both classes are computation floors, not statistical sufficiency.

All four methods share each fold's cases. Reports include Brier loss, log loss, reliability bins, event counts, detection counts at the prespecified 0.5 threshold, and paired Brier differences against frozen. Negative differences favor the comparison method. Fold composition and training counts must accompany any plot: differing test Congresses mean a descending curve alone cannot identify the causal value of additional data. Test outcomes are used for scoring, not that fold's fitting or selection.

## Outstanding research gates

Official passage labels and multi-Congress historical checkpoint coverage still need auditing. Imported source hashes and availability assertions require independent verification. Missing labels can bias the scored sample; examine every exclusion and the source sampling frame. Family counts, family/Congress-clustered uncertainty, protected final-test execution, a prespecified release decision, and a minimal dashboard remain follow-up work. No automatic worker schedule or promotion is enabled by this command. `release_eligible` is always false.

The decisive milestone remains an honestly reported official-data learning curve, including negative or inconclusive results. This implementation supplies the repeatable experiment; it does not claim to have completed that scientific milestone.
