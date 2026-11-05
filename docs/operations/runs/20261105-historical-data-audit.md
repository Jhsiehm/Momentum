# Historical data and forecasting audit — November 5, 2026

**Conclusion: expansion is warranted; meaningful independent predictive evaluation is still blocked.** The full 114th import has substantially more natural enactments than the tiny sampled studies, but record presence does not establish point-in-time eligibility. No model was fitted, tuned, rescored or promoted in this audit. No UI, immutable evidence, forecasts, frozen experiment, live label, human receipt or worker setting was changed.

See the [expansion design](../../cohorts/multicongress-expansion-v1-plan.md), documented before any proposed scoring, and [machine-readable audit receipt](20261105-historical-data-audit.json). The design proposes a full 113–117 census and future 120/121 protected temporal boundaries, with hard source/family/positive-count gates. It does not claim those datasets or protections already exist.

## Scope and concurrency

Audited `engine/store.py`, `ingest.py`, `sampling.py`, `coverage_pipeline.py`, `import_quality.py`, `cohort.py`, `sample_publication_v2.py`, `earlier_labels.py`, `model.py`, `evaluate.py`, saved studies and research receipts. Took a consistent SQLite backup from a read-only connection to the live database; all subsequent detailed counts use that retained snapshot. Inspected official records only; fictional demo cases are excluded. No private chats are included in this report or committed artifacts.

An active lease owned by `expanded-experiments-20261105-01a1aada` was present. Its protocol registers 200 additional 116 cases and 500 118 cases partitioned 250/250. That concurrent run was not executed, mutated, rescored, or certified here. Merely inspecting its registered sample sizes does not establish completed acquisition or eligible counts. No bulk import job was queued/running in the initial job-table inspection; the separate lease still prevented treating the workspace as idle. Read-only snapshot auditing continued without acquiring or displacing its lease. Counts below are not a claim about later live database state.

## Actual inventory and local cohort counts

Saved GovInfo inventory `17c9bbca-5edb-470e-816d-d5a7ec72f611`, discovered October 26, 2026: **40,435 IDs**, hash `c69000c5d0a2d6c72af0cc139872217ffcdfce370a072b170b22134a1d709575`.

| Congress | H.R. directory | S. directory | Total directory | Imported bills |
|---|---:|---:|---:|---:|
| 114 | 6,526 | 3,548 | 10,074 | 10,074 |
| 116 | 9,062 | 5,086 | 14,148 | 35 |
| 117 | Not in saved inventory | Not in saved inventory | Unknown | 1 |
| 118 | 10,564 | 5,649 | 16,213 | 260 |
| 119 | Not in saved inventory | Not in saved inventory | Unknown | 22 |

The full 114 coverage plan completed 41 batches, 10,074 imports, zero job failures; its saved population hash and exact inventory population checks pass. Directory completeness means the received listing was complete, not independently established completeness of all legislative introductions. The older 16,053 figure is the five-experiment selection pool after excluding prior imported/study IDs, not the complete 118 inventory.

Snapshot totals: **10,392 official bills**, 60,131 event records, 335 positive resolution records, **zero negative resolution records**, and **10,057 unresolved bills**. Do not infer that those unresolved bills failed. A separate publication study can have audited negative labels in its frozen files while the main temporal store has none.

| Congress | Recorded positive bills | Before Congress deadline | After deadline | Positive after day180 and before deadline | All bills with checkpoint before end |
|---|---:|---:|---:|---:|---:|
| 114 | 326 | 325 | 1 | 179 | 8,768 |
| 116 | 1 | 1 | 0 | 1 | 30 |
| 117 | 1 | 1 | 0 | 0 | 1 |
| 118 | 6 | 4 | 2 | 3 | 234 |
| 119 | 1 | 1 | 0 | 0 | 2 |
| **Total** | **335** | **332** | **3** | **183** | **9,035** |

These are timing diagnostics from current recorded introduction/outcome dates, **not eligible positive families**. They exclude same-day checkpoint ambiguity conservatively; no endpoint-day or conflicting positive-date record appeared in this snapshot. No positive is converted into a negative by the audit. The 119th Congress is incomplete, and most of its 22 currently imported bills have a day180 checkpoint after its end.

All **10,392** latest official bill records are marked family-unadjudicated; **zero** bill metadata snapshots are available by their day180 checkpoint under the store's recorded availability rules. All have current bulk receipts. Thus the main store currently supplies **zero metadata-qualified day180 positive cases**, while the number passing the complete proposed provenance/family gates is **not established** (`null` in the receipt), not 183. The historical publication studies use separate bounded publication evidence and cannot be equated with a backdated main-store import.

## Existing publication cohorts and eligible positives

“Eligible” in this table means the respective study's bounded publication protocol, not fully human-adjudicated historical action evidence or independent validation.

| Frozen cohort / role | Selected | Publication eligible | Eligible positives |
|---|---:|---:|---:|
| Seeded v2, 114 training | 25 | 23 | 1 |
| Seeded v2, 116 training | 35 | 30 | 1 |
| Seeded v2, 118 evaluation | 40 | 33 | 0 |
| Five experiments, new 118 evaluation | 100 | 82 | 1 |

Seeded v2 excludes 14 late checkpoints; its training set contains 53 distinct identified families and 2 positives. The five-comparison cohort excludes 17 late checkpoints and 1 missing introduced publication; its 82 eligible cases occupy 81 identified families. It reuses the same 53 training families/2 positives, so the training evidence must not be added twice. Existing combined-family screening found no additional train/evaluation overlap, but incomplete adjudication prevents a guarantee of family independence.

The prior seeded v1 had 32 provisionally eligible evaluation cases with zero positives and remained blocked by label timing/introduction evidence. v2 is an explicit evidence amendment, not a new holdout. Earlier 114 calendar proof used by the full-cycle diagnostic leaves 23/1 train, 30/1 development-validation and 33/0 evaluation cases. None provides a meaningful estimate of successful-enactment detection.

## Baseline performance: saved observations only

Lower losses are better. These values were read from existing results/receipts and **not newly scored**. SHA-256s of saved result files are in the JSON receipt; five-experiment internal result/input hashes were checked.

| Existing evaluation | Candidate Brier | Prior-rate Brier | Candidate log loss | Prior-rate log loss |
|---|---:|---:|---:|---:|
| Publication v2, 33 cases / 0 positives | 0.00605899 | 0.00297521 | 0.04397273 | 0.05608947 |
| Full-cycle adaptive diagnostic, same 33 cases | 0.00455711 | 0.00297521 | 0.03678502 | 0.05608947 |
| Macro v2 exploratory reuse, same 33 cases | 0.00428752 | 0.00297521 | 0.03582386 | 0.05608947 |
| Five experiments E1 structured, 82 / 1 | 0.01310554 | 0.01383995 | 0.05431320 | 0.09087765 |
| Five experiments E2 context, same 82 / 1 | 0.01444596 | 0.01383995 | 0.05999858 | 0.09087765 |
| Five experiments E3 stronger penalty, same 82 / 1 | 0.01103274 | 0.01383995 | 0.05831082 | 0.09087765 |
| Five experiments E4 no stage, same 82 / 1 | 0.01172351 | 0.01383995 | 0.06572055 | 0.09087765 |
| Five experiments E5 no activity, same 82 / 1 | 0.01182164 | 0.01383995 | 0.05149454 | 0.09087765 |

The rate baseline is `(2+1)/(53+2) = 3/55`. It wins primary Brier on every listed 33-case variant. E2 fails to transfer against baseline. E3's lower observed Brier does not establish improvement: all five reported paired family-bootstrap intervals cross zero; evaluations share one positive, training cases and a Congress. Log-loss disagreement is not permission to switch the primary metric. Existing intervals omit training and Congress uncertainty. The synthetic 240→300 training experiment also slightly worsened fixed Brier (0.22643566→0.22688385); it is software evidence, not legislative predictive evidence.

Source reports: [full cycle](20261105-full-learning-cycle.md), [five experiments](20261105-five-experiments.md), [macro comparison](../../cohorts/macro-pilot-v2-results.md). Preserve all negative and blocked results.

## Pipeline findings and provenance gaps

- **Temporal storage is conservative but assertions are not proof.** `Store.records` gates effective and available timestamps; current imports stay at observation time, forecasts/evidence are immutable, and imports do not manufacture negatives. An `archive_proof` string enables an operator assertion; the code does not independently verify its historical content. Main-store history is consequently not forecast-ready merely because it contains dated events.
- **Labels have distinct targets and availability clocks.** Ingestion records observed public-law enactments, including later-than-Congress-end outcomes; the new audit exposes that difference without changing imported labels. A complete calendar membership census does not prove each positive's enactment date. Saved 116 calendar availability is May 8, 2021; the original compiled-statutes route was too late. The alternate 114 final calendar bound is March 24, 2017, versus November 30, 2022 for retained Statutes proof. Current preservation records do not establish identical historical bytes. The investigation of all 344 116 slip laws remains a negative result because one package's late availability defeats an early complete census.
- **Family IDs do not establish genealogy.** Current imports are unadjudicated singletons. Publication union-find joins related IDs and normalized identical titles, including known intermediaries, but cannot discover absent edges or adequately adjudicate generic titles. The general model uses stored family IDs and prior Congresses; mismatched family IDs across records or unknown cross-Congress relationships can defeat its intended separation. The new auditor flags inconsistent stored identities but does not certify a complete graph. New data must pass the design's global component/purge gate before any scoring.
- **Forecast eligibility floors are computational, not statistical.** Twenty training families and both labels allow computation, not reliable fitting. Six features, two training positives and zero/one evaluation positive are severe event scarcity. Publication versions are proxies for activity, not complete action histories. Keep that distinction when expanding.
- **Independent evaluation is not enforced by file naming.** The separate evaluator checks one prediction per bill and prediction/resolution ordering, but relies on externally protected labels. It does not itself enforce global family separation, positive-count minima, exposure history or adjudication; duplicate label IDs are collapsed by dictionary construction and timestamps are compared as supplied. A future scoring preflight must reject duplicates and normalize timestamps, require provenance/partition manifests, and enforce access controls. This audit leaves the frozen scorer unchanged and treats those checks as blockers, not assumed protections.
- **Missingness remains material.** Sixty imported bills have missing/unclassified topic; all have retained title/sponsor/introduction/raw hash and some action record. That says nothing about point-in-time completeness. There is no full 113/115/117 inventory or expanded source/label/family eligibility ledger. Existing designated human action-history reviews remain pending.

## Data-quality implementation and validation

Only `engine/import_quality.py` and its tests changed. Schema v2 adds a read-only per-Congress timing/availability diagnostic, checks all retained metadata versions rather than just the latest, reports family/metadata identity conflicts, label conflicts, positive-date conflicts and orphan resolutions, and explicitly leaves certified positive-family eligibility unknown. It reports after-deadline positives without rewriting them or treating unresolved bills as negatives. The endpoint-day category conservatively requests precision review even for an explicit timestamp; this audit is not an outcome adjudicator.

Validation:

- Focused import-quality suite: **7 tests passed**; regressions cover deadline/same-day cases, absent/conflicting labels, orphan resolutions, conflicting families, historical metadata hidden by newer imports, effective-time gating, invalid metadata/age, raw hash corruption and no database mutation.
- Full suite: **209 tests passed in 117.890 seconds** (`python3 -m unittest discover -s tests -q`). No UI edits; no frontend checks required for this batch.
- Snapshot integrity: **70,858** official record IDs and **10,398** raw hashes checked, zero invalid/missing/corrupt entries; **10,392** current bulk retrieval receipts checked, zero missing/mismatched entries; saved inventory hash valid.
- Frozen preservation: **5,321 files unchanged** across existing cohort directories and completed full-cycle/five-experiment runs. **2,625** source receipts checked (2,545 `.raw`, 80 macro `.csv`), zero hash failures. Initial generic verification assumed `.raw` for every receipt; corrected the verifier to the macro module's documented `.csv` contract before reporting this result. Six five-experiment input/result internal hashes pass. Preservation is not a rerun of every study or a provenance certification.

## Reproduction and remaining work

Runtime snapshot, source bytes and detailed audit files remain ignored under `data/audits/historical-expansion-20261105/`; they are not bundled in a fresh clone. The committed receipt identifies snapshot and result hashes. With that local snapshot and retained raw store:

```sh
python3 -m engine.import_quality \
  --database data/audits/historical-expansion-20261105/snapshot.sqlite \
  --raw-directory data/raw \
  --output data/audits/historical-expansion-20261105/import-quality-replay.json
python3 -m unittest tests.test_import_quality -v
```

Counts and integrity findings should match on the same snapshot/bytes; observation timestamps and thus the whole report hash differ on rerun. The snapshot was created with SQLite's backup API from `mode=ro`; its copied WAL-mode header initially prevented a standalone read-only open. Setting journal mode to DELETE on the **backup only** made it self-contained; the live database was not altered.

Next authorized scope remains data-quality work. Implement the proposal's missing acquisition/provenance/family manifests and scoring preflight under a new protocol, establish protected access and actual eligible-positive counts, and stop with a blocked report if minima fail. This audit establishes neither a completed expanded dataset nor validated predictive improvement. Product UI and promotion remain out of scope.
