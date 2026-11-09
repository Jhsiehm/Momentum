# Official historical-bill context diagnostic — November 9, 2026

Status: source acquisition, offline correction and independent replay completed. The separately registered v2 experiment stopped before optimization because no positive training labels survived its population rules. Zero predictive fits and no performance result.

## Question and scope

Does dated cosponsorship, referral breadth and procedural recency improve a six-feature publication-stage anchor on the same later-period bills? This is a separately registered **retrospective diagnostic using current official records**. It does not establish historical availability, certified negative labels, untouched evaluation, E3 eligibility or model promotion.

The earlier text diagnostic remains unchanged. This comparison adds three context features and three explicit missingness flags, yielding twelve columns. Sponsor party and text modeling are outside this comparison. Training-only medians and scaling, two fixed fits, no calibration or tuning, and the strong stage reference were chosen before outcomes.

## Fixed acquisition

From 75,605 identities in twelve previously verified official directory listings, exclude the protected pilot and previously scored cases and their known families. The available frozen family manifests cover 1,200 source-record assignments. They identify 695 distinct excluded identities; this is not complete legislative genealogy. Select 2,000 identities per Congress, 113–118, using the registered hash order, with no replacements or outcome balancing.

The registration binds 1,226 inputs. Four workers retrieve at most 12,000 XMLs, with a 2,000,000-byte response cap plus sentinel, a 500,000,000-byte total body ceiling and no retries. A 30-minute scheduling window stops new requests; socket inactivity timeouts, pending requests and offline processing do not constitute a hard total wall-time cap. Every selected case receives a disposition.

Runtime: `data/research-runs/official-context-acquisition-v1-20261109/`. Registration SHA-256: `d5383a5942f7494e223a64f8449375b20dab9ce7bb3ef982a8327939b880c219`.

## Preflight corrections and evidence

Independent adversarial review corrected unsupported source URLs, out-of-period introductions, XML containers that could hide records, invalid timestamps truncated into dates, and signing-only assertions that could otherwise become false negative labels. Delayed introduced-edition printing before the checkpoint is allowed; its asserted date does not prove historical availability. Ordinary actions from supported systems can legitimately lack action codes.

The fitting runner additionally checks exact feature-file membership against the acquisition ledger, saves unknown-label exclusions even when eligibility gates stop execution, and independently recalculates the optimizer objective and gradient. Family assignment precedes labels; later periods take priority, with one fixed representative per known family and no label-dependent replacement. Source-only population and label ledgers precede fitting; saved probabilities precede scoring.

Source preflight: 32 tests passed normally and optimized. Fit preflight: 18 tests passed normally and optimized. These synthetic orchestration tests use mocked optimization and are not model results. Independent review: [review record](../../research/reviews/20261109-official-context-diagnostic-review.md).

An author attempted to start collection concurrently with the root process at the same exclusive output directory. The attempt stopped immediately at directory creation, before any extra request or artifact. The root owns the only acquisition run.

## Registered interpretation

An enacted label requires concordant own-bill public-law identity and dated terminal action. A negative is only an uncertified current-record proxy with a post-Congress update and no enactment assertion. Inconsistent, unsupported or insufficient records remain unknown. Target maturity dates do not certify that these source bytes were available then.

Two fitted artifacts train on Congresses 113–116 and are evaluated separately on 117 and 118. Report Brier loss, log loss, event counts, calibration, paired family-bootstrap uncertainty, and skill against training-rate and stage references on identical rows. A 60% target would mean 60% relative Brier-loss reduction against the specified reference, not accuracy or percentage-point improvement.

## Results and disposition

All 12,000 requests returned HTTP 200, retaining 192,995,893 bytes. All XMLs passed acquisition identity/parse checks. There were 9,726 anchor-valid records and 2,274 feature-ineligible records, with no retries, replacements or cap-related omissions.

| Congress | Selected | Anchor-valid | Feature-ineligible | Observed cosponsor feature | Observed referral / recency |
|---|---:|---:|---:|---:|---:|
| 113 | 2,000 | 1,618 | 382 | 1,252 | 0 / 0 |
| 114 | 2,000 | 1,675 | 325 | 1,358 | 0 / 0 |
| 115 | 2,000 | 1,590 | 410 | 1,302 | 0 / 0 |
| 116 | 2,000 | 1,568 | 432 | 1,302 | 0 / 0 |
| 117 | 2,000 | 1,627 | 373 | 1,303 | 0 / 0 |
| 118 | 2,000 | 1,648 | 352 | 1,344 | 0 / 0 |

Independent replay matched every feature and disposition. Both procedural fields are missing for every anchor-valid row, making the all-missing-training-field stop inevitable before outcomes. Consequently **zero labels were resolved and zero fits ran**. This is a software-adapter failure, not evidence of absent legislative history or failed predictive efficacy.

An allowlisted schema diagnosis restricted to pre-cutoff action fields found 6,316 `Intro-H` and 368 `H11100-A` values rejected by the alphanumeric-only code rule, plus 4,853 actions whose source system is explicitly named Senate but lacks a numeric code. The coupled procedural parser also erased committee breadth when action recency failed. Preserve this v1 and its registration; resolve representation handling in a separately registered offline version using exactly the same saved bytes and sample. Do not relax label rules or fetch replacements.

Acquisition result SHA-256: `eb542110bdcf309e8c29f07ae3372137e5bcb38e452ba536c9871843f99776f7`. Population ledger: `217cdc3dec25fd09f92d8ddfedc6b74945f7acdfd1407e9726f1893658a26ff2`. Independent source replay: `688848eafef8bc0055368d244de9190da48f8caf93807e29f31fe7ae7fc69a64`.

All 771 full-suite tests passed in 86.429 seconds. Those tests did not capture the actual source representation gap; software pass counts do not override the failed source-readiness gate. All 523 prior preserved files and the frozen-model audit remained unchanged. Exact 12,000-case records, failures, raw-source hashes and input bindings remain in ignored runtime storage; reproducible code, protocols and this research summary belong in Git.

## Separate offline correction v2

Independent preflight passed 16 source-adapter tests and 21 fit-runner tests normally and optimized. The corrected adapter accepts only the two observed hyphenated activity codes and the explicit name-only Senate source; no numeric source is invented. Referral and recency errors are now independent. The outcome adapter changes only ordinary-history representation; terminal enactment evidence requirements remain unchanged. No real outcomes were resolved before this correction was registered.

The offline run used the same 12,000 sources and made zero requests. Every baseline, cosponsor, stage, cutoff and family output matched v1. The same 2,274 exclusions remain: 1,884 unreachable day-180 checkpoints, 293 missing edition dates, 95 missing/ambiguous introduced editions and two missing text histories.

Among 9,726 anchor-valid rows, observed context counts are 7,861 cosponsor, 9,717 referral and 9,715 recency; 7,848 have all three. Missing counts are 1,865 / 9 / 11. These are source-preparation denominators, not final model populations.

Independent full replay passed. After frozen family selection, before labels, there are 5,110 training candidates, 1,382 Congress-117 candidates and 1,464 Congress-118 candidates, with 4,044 source/feature/family exclusions. Training candidates have 4,097 / 5,107 / 5,103 observed context values, passing the source-only nonempty-field check. Outcome gates remain mandatory.

Offline registration: `d6c1177afb6d53ea74130e02e9d0bcd83b6b69c6ffb6d7490694595d14c0357b`. Result: `d29fa6e6549d27aac9db0c5c29e5163dfe9fef22a53f2cf5b703196ee610d97f`. Coverage summary: `3d6d6fc1961d51d26ba2cf8866c3d6258f8b7b9ea930f6885fe091d92cce9cb2`. Independent replay: `d438573c445f252660fd741e143b9e60135313f5bd5dc6fa2b3d1f033a638044`.

Runtime: `data/research-runs/official-context-features-v2-20261109/`. Its complete `changes.json` preserves every before/after context value and missingness reason. The registered fitting run is separately stored at `data/research-runs/official-context-diagnostic-v2-20261109/`.

## Registered v2 experiment: stopped before optimization

| Role | Frozen candidates | Negative proxies | Unknown | Positive labels |
|---|---:|---:|---:|---:|
| Training 113–116 | 5,110 | 5,110 | 0 | 0 |
| Evaluation 117 | 1,382 | 916 | 466 | 0 |
| Evaluation 118 | 1,464 | 1,086 | 378 | 0 |

The class gate rejected this population with `Both training classes required`. **Zero fits started**, and no probabilities, loss scores, bootstrap intervals or promotion decision were produced. All 844 unknowns lacked a post-Congress update assertion. Neither these unknowns nor zero positive labels may be interpreted as actual non-enactment in the source population.

Independent replay verified every registered input/code binding, all 7,956 family-selected rows and labels, all 844 exclusions and the exact failure. It found no prediction/result artifact. A separately recorded post-failure diagnostic investigates whether publication-metadata completeness systematically excluded enacted bills; it cannot retrospectively make this failed registration successful.

Fit registration: `8959fbdf9cb6de5a246c179bff7a36b30c72ab17575753dc29cee64d728af3ad`. Failure: `d43a148c8b24945233322276bdf08bb287c2dbb2ace3aab9abba8b58d1d227bb`. Label ledger: `ad964c959cb0edde8cadfd1cdfe603ed7a4d22dfb1e20d4528b7ab38d25c4bd8`. Independent replay: `4d0655cbf5242ca81ad392f22edb179c0a679d8d6b4c935ebf7ff8189243cbbc`.

The full suite including v2 additions passed 798 tests in 88.897 seconds. Dedicated final preflights additionally passed 16 adapter and 21 runner tests normally/optimized. These remain software validation, not efficacy evidence.

## Post-failure conditioning audit

A separately registered diagnostic inspected own-public-law assertions across all 12,000 selected records, expressly widening outcome exposure without deriving new training labels. Its first version stopped at zero-based case 4,972, H.R.11/117, because a duplicate identity parser omitted the already supported `billNumber`/`billType` schema. Prior 4,972 cases had been inspected in memory; no aggregate result was saved. Preserve its registration and separately recorded failure. A reviewed v2 reuses the frozen strict dual-schema validator, with six tests normal/optimized; it changes no assertion classification.

The complete v2 diagnostic found **333 records with own-public-law assertions**, all excluded by the publication-feature gate: **293 failed on missing edition dates and 40 missed the day-180 horizon**. All 333 asserted-law records have empty enrolled-edition dates. Counts by Congress are 66, 71, 80, 41, 43 and 32. No anchor-valid record contains such an assertion. The 11,667 records without an observed public-law assertion are not thereby certified negatives.

This establishes an outcome-associated source-completeness selection problem in this acquired population. It does not establish how many of the 333 would meet the separate dated enactment/risk-set label rule. The failed publication-based registration remains failed; skipping undated editions after observing this result would not repair its scientific meaning. A separately defined action-milestone comparison, applying uniformly to all saved identities, is the proposed successor and must disclose the adaptive design and exposed data.

Conditioning v2 artifact hashes: {"cases.json": "c3754f687f648d2f0054150453a86c88ea74e9857fe37551e154767152780798", "independent-review.json": "a9a33ae458e85689a289c1987f6453f98ad75b27f419da9ecb2e4dab8d866185", "registration.json": "7addb0b3b7fcbacf4c69ffd943a3accab456c1403b94a63a39b54d80dc7b640a", "result.json": "1c06a8ae5d2c099b8a02d4e50aeaa39d36628ed86dc7281b5c7a7edf6d94d03d"}.
