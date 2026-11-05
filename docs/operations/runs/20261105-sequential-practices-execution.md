# Execution of the new sequential practices — November 5, 2026

The requested run uses the new `engine.sequential` implementation at commit `296e6c5`: originating-chamber passage by Congress end, predicted at day 30, with training Congresses 110–112 and six forward evaluation folds 113–118. This differs from the previous day-180 enactment experiments; their scores and labels are not interchangeable.

## Official-data result: blocked

A consistent SQLite backup captured 11,092 official bills: 10,074 from 114, 235 from 116, 1 from 117, 760 from 118 and 22 from 119. No adjudicated passage-label manifest was found among local JSONL files. The official benchmark was explicitly executed with that empty audited label set; it reports all 11,092 missing labels, six blocked folds and no fitted model or scores. This is a readiness run, not a completed official prediction study.

An independent checkpoint scan found zero bill-metadata snapshots at day 30 in the historical Congresses present in the corpus. Nineteen bills from 119 have checkpoint metadata, but 119 is outside this benchmark and unfinished. Training Congresses 110–112 have no local bills. Modern source retrieval and enactment outcomes do not repair these historical feature and passage-label gaps.

The new practices correctly prevent producing an apparent learning curve from unsuitable data. Required next inputs are independently audited passage positives, complete action histories for negatives, historically supported day-30 features, and earlier-Congress training coverage. Historical provenance, family and final-evaluation limitations documented in `docs/SEQUENTIAL_BENCHMARK.md` remain. No data was backdated or missing label treated as a negative.

## Separate synthetic workflow check

A fixed-seed fixture contains 1,080 synthetic bills, 120 per Congress 110–118. Simulated committee events affect passage probability; all records are labelled synthetic in an isolated database. The same target, day-30 checkpoint and temporal splits compare frozen, expanding retrained, adaptive and historical-rate models. Initial training is 360 cases, expanding by 120 per fold to 960; every fold evaluates the same 120 cases for all four methods.

These simulated results verify execution only. They supply no evidence that official legislative forecasting accuracy improved. Exact metrics and artifacts are retained separately in ignored runtime storage.

## Reproduction and scope

Runner: `docs/operations/reproducers/sequential_practices_20261105.py`. Run from repository root with `python3 -m docs.operations.reproducers.sequential_practices_20261105`. The script snapshots the local official database, writes immutable report files and verifies synthetic replay and temporal/equal-case assertions. It does not acquire sources or synthesize official labels. Local artifacts: `data/research-runs/sequential-practices-20261105/`.

Validation and platform-save completion are recorded below. No engine code, production model, scheduled budgets or previous experiment artifacts changed. Runtime databases, source material and private platform chats remain outside Git.

## Completion checkpoint

Eight sequential tests passed. Two synthetic benchmark executions produced identical reports. Independent arithmetic checks reproduced all 24 Brier scores, and both report hashes verified. Three reports were saved in local platform chat “New practices · sequential passage experiment · blocked official data”; all three report API endpoints were checked. No real-data accuracy result was produced.

| Synthetic Congress | Training | Test | Positive | Frozen Brier | Retrained | Adaptive | Rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 113 | 360 | 120 | 21 | 0.135289 | 0.135289 | 0.137015 | 0.145086 |
| 114 | 480 | 120 | 24 | 0.129452 | 0.131095 | 0.139179 | 0.160025 |
| 115 | 600 | 120 | 18 | 0.102953 | 0.103191 | 0.101407 | 0.129617 |
| 116 | 720 | 120 | 30 | 0.153620 | 0.154821 | 0.151391 | 0.191299 |
| 117 | 840 | 120 | 25 | 0.139433 | 0.139143 | 0.137906 | 0.165056 |
| 118 | 960 | 120 | 27 | 0.148056 | 0.147566 | 0.146219 | 0.175075 |

Synthetic performance is mixed; retraining does not monotonically improve even this fixture. These values are software-check results only.

Official report ID: `e8e3936df7d4fb3d6f2bda922683889840353fa4486e9d3047c8e53cb8ea36ae`. Synthetic report ID: `f744cc5a0b1757cb0fce613323f1d90e6b81fdee635355fb3fd13398feff1a42`. The runner retains the original registration commit on replay; report code hashes still detect changes in benchmark dependencies.
