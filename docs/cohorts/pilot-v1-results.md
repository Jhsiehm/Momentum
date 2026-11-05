# Historical cohort pilot v1 — result

The candidate did not outperform the historical-rate baseline on the prespecified primary metric. This is a bounded development pilot, not a rejection of legislative forecasting generally.

## Locked design

H.R. and S. numbers 1–60, 114th Congress training and 118th Congress testing; one checkpoint 180 days after introduction. Target: own-bill public-law enactment before Congress ends. The design was frozen before cohort scoring. Neither features nor hyperparameters were tuned on this test set. Reserved/nonpublished slots remain accounted for and were not replaced.

Candidate `document-stage-l2-v1` uses dated publication-version stage, age, version count, inactivity, chamber and recent version count. It uses the existing deterministic L2 fitter, but differs from `structured-l2-v1`: published versions are not action histories. All scaling is fitted on the training rows. No LLM or OpenRouter call is involved in fitting, feature extraction or scoring.

## Result

| Measure | Candidate | Historical-rate baseline |
|---|---:|---:|
| Brier loss (primary; lower is better) | 0.019156 | 0.019005 |
| Log loss (secondary; lower is better) | 0.100309 | 0.102809 |

- 240 prespecified number/chamber/Congress slots; 88 eligible training bills (3 positives), 107 eligible test bills (2 positives, 92 identified families).
- Candidate minus baseline Brier difference: +0.000151.
- 95% test-family cluster bootstrap interval: [-0.000872, +0.001379], 2,000 draws, seed 20261024.
- The interval includes zero. The secondary log-loss improvement does not override the primary-metric result.
- Only three training and two test enactments make this an especially weak basis for model selection or calibration.

## Audit scope

798 source artifacts (106.3 MB) are retained with URLs, retrieval timestamps and SHA-256 checksums. Offline reproduction reparses the source artifacts, reconstructs cohort membership/features/labels/families, refits the model and rescores before comparing the locked result hash.

Version evidence comes from [GovInfo bill publications](https://www.govinfo.gov/help/bills), MODS identity/issuance/ingestion dates and successful PREMIS ingestion/access-package/parsing events. Availability is conservatively placed at the end of the latest relevant day plus one day. Model inputs use only package existence and version stage; no current summaries, policy-area metadata, modern text embeddings or outcome prose enter the features. This supports a narrow package-level historical audit, **not proof that today's rendition bytes equal historical bytes or an independently measured first-public-access time**.

The full [National Archives public-law lists](https://www.archives.gov/federal-register/laws/past) are checked for consecutive unique law numbers: all 329 laws from the 114th and all 274 from the 118th. The 114th census matches the bill identities and dates in Statutes volumes 129 and 130 exactly. Their successful public-access preservation events establish a conservative training-label availability of **2022-11-30 23:59:59 UTC**, before every test checkpoint. Each sampled bill's current official public-law references are cross-checked. Current BILLSTATUS retrievals remain current in the main source collection; they are not backdated.

Non-enactment labels require the complete census, not a missing action. Enactments after the Congress deadline count as negative for this horizon; ambiguous same-day deadlines are excluded. Already-enacted checkpoints are excluded. Related-bill links and identical normalized introduced titles form a conservative family graph; test-family overlap and duplicate training families are removed. This is automated screening, not exhaustive manual provision-lineage adjudication.

## Exclusions

### Congress 114

- 10: No BILLSTATUS entry in complete official chamber directory; no historical introduction audited.
- 3: Already enacted by checkpoint.
- 5: Duplicate training family.
- 4: Identified family overlaps test cohort.
- 3: No introduced publication in official text-version list.
- 7: Checkpoint at/after Congress end.

### Congress 118

- 10: No introduced publication in official text-version list.
- 2: Checkpoint at/after Congress end.
- 1: Already enacted by checkpoint.

The initial blocked audit remains saved as `audit-blocked.json`. Parsing corrections handled source encodings, a missing parenthesis in an original law-list date, and the official “Public Law” type label. Complete chamber directories distinguished absent/reserved slots from failed downloads; missing introduced publications were handled under the prespecified exclusion. No sample replacement or score-based protocol change occurred.

## Reproduce

From the project root:

```sh
python3 -m engine.cohort prepare
python3 -m engine.cohort reproduce
```

`prepare` resumes cached downloads. `reproduce` runs offline and rejects altered bytes, changed source reconstruction or a changed result. `run` additionally publishes an experiment and audit report into the workspace. The UI and chat's rerun action dispatch to this frozen cohort runner rather than the generic experiment runner.

The bundle is `data/cohorts/historical-pilot-v1/`: `protocol.json`, `source-manifest.json`, `cohort.json`, `cohort.csv`, `predictions.jsonl`, `result.json`, `code/`, and `sources/`. It is retained locally and ignored by Git. The specification and runner are tracked project files.

Reproduction hash: `420b4a09210301128128e3f384323700300b9b1951e1bf03299da9397a0557d8`.

## Decision

Do not promote this candidate or add complexity based on this pilot. Keep the baseline. A next experiment would need a separately specified, broader sample with substantially more resolved positives, more than one test Congress, and stronger family/publication validation. These scores do not justify a deployment, calibration claim or causal interpretation. Bootstrap uncertainty is conditional on this training fit and test Congress; it excludes training and Congress-level variation.
