# Seeded publication-version development study

This separate study preserves all 100 IDs from sample `51ee0efb-22bc-406a-87d4-75494e573623`. It does not convert current BILLSTATUS action records into historical evidence, replace the original experiment, or satisfy human audit receipts.

## Prespecified method

Before scores, froze a 180-day checkpoint, fixed six document-version features, fixed L2 model hyperparameters, a smoothed training-rate baseline, 114th and 116th Congress training, and 118th Congress evaluation. Successful GovInfo MODS/PREMIS preservation events establish a bounded publication-metadata availability rule. Complete National Archives law censuses are crosschecked against Statutes volumes 129, 130, 133 and 134 for training labels. Family screening unions official related-bill references and identical normalized introduced titles; it is not complete human genealogy.

## Result: blocked, no forecasts or scores produced

- All 100 selected IDs remain in the denominator.
- 53 training rows pass bill-level filters, with two enactments.
- 32 evaluation rows pass bill-level filters, with zero enactments.
- 15 exclusions are recorded individually in cohort.json/result.json.
- One source audit fails: 118-H.R.5925 has conflicting introduction metadata. The whole study remains blocked rather than silently dropping the failed source.
- Complete 116th-Congress training-label provenance becomes available under the registered conservative rule on **2025-02-13**, after the 118th-Congress prediction checkpoints. The labels cannot be used for those historical predictions.

These counts are potential bill-level eligibility counts, not generated predictions. Training-label availability blocks the chronological comparison as a whole. Zero evaluation enactments would severely limit interpretation even if other blockers were resolved. No tuning, replacement sample, model promotion or backdating was performed.

## Reproduce

```sh
python3 -m engine.sample_publication reproduce
```

Offline reproduction verifies all cached source byte hashes, reconstructs all rows and exclusions, and checks the locked result. No network or API credential is required. `prepare` performs source preparation; `run` locks the reproducible result. Current pipeline results are development evidence, not a protected holdout.

Reproducibility hash: `a0243f2d596ae2b70984b710fa06c121c945c03da83fbbcd3bd5c7afcffb036e`

The older pilot and its frozen core modules were not changed.

## Frozen artifact and application schema

The locked result uses the inherited cohort schema: `kind: audited_cohort` names the method family and `available: 32` counts rows passing bill-level publication filters. In this blocked study it does **not** mean 32 predictions exist: `status` is `blocked`, `results` is empty, and neither metrics nor a fitted model is present. The application publishes an explicit semantic adapter with `kind: sample_publication_study`, `publication_eligible_count: 32`, and `available: 0`. The original reproducibility hash identifies the frozen analytical artifact, not the adapted application metadata. Dedicated rerun routing always reconstructs this study and never dispatches to the older pilot or action-history model.
