# Independent passage-90 methods and failure-path review

November 12, 2026. This is an independent agent review of a separately versioned engineering foundation. It is not qualified human source review, historical certification, a predictive experiment, or authorization to relax an existing study's gates. The reviewer did not implement the new passage contract or ledger. No real model fitting, outcome scoring, external source requests, or forecasts were performed by this review.

## Scope and evidence

Read the repository workflow, existing day-30 passage benchmark, paper readiness and prospective-source draft, the November 8 archival follow-up, November 9 action-context failure, November 11 action-context resolution, and the existing passage, storage, and evaluation code. Prior reported counts are historical receipts, not reruns in this review. The fresh checkout does not contain the ignored historical source corpus.

The new target is first originating-chamber passage after introduction plus 30 days and within the following 90 days, restricted to H.R./S. bills with a complete window strictly before Congress end. Existing enactment and Congress-end passage studies must retain their targets, immutable records, exposure histories, and release gates. This shorter target does not make already exposed Congresses independent again.

## Lessons that constrain the plan

- The publication-completeness gate removed all 333 records carrying current public-law assertions in the prior source sample. Retain the entire discovery population and every exclusion before interpreting a selected sample. Missing predictor values should normally be explicit categories/indicators, not a reason to select a more convenient bill. A fixed full-window rule deliberately excludes late-Congress introductions; report that population restriction.
- The action adapter and outcome resolver both halted before fitting despite large passing offline suites. Test actual source shapes and executable failure paths, with valid positive controls as well as corrupt fixtures. A validator that rejects every input is not successful. Explicit production checks must behave identically under normal and optimized Python.
- The November 11 context advantage was 3.0398% against the two-column control but 0.8253% against the stronger action-milestone reference, whose descriptive interval included zero. Fix the strong reference before results and compare identical cases. A favorable weak-baseline comparison cannot establish the primary claim.
- Sixteen archive requests found no captures for eight historical cases. Acquiring today's bytes does not repair old availability. Keep event time, publication claims, actual acquisition completion, feature availability, registration time, and issuance time distinct. Hashes detect altered bytes; they do not by themselves prove when those bytes were possessed.
- Missing labels and unsupported schema cases previously produced one-class samples. Unknown must never become zero. Parser coverage, label completeness, class balance, source review and predictive efficacy are different quantities.

## Conditions for accepting the new foundation

1. **Target and risk set:** use the first originating-chamber passage, never passage in the other chamber or later repassage. Require introduction inside the stated Congress. Exclude earlier passage; conservatively retain unresolved boundary-day ambiguity. State the exact timestamp precision and inclusive/exclusive horizon rules. A new Congress requires a new bill identity and never silently extends the old bill's horizon.
2. **Labels and selection:** a negative needs complete audited action coverage over the necessary interval and an availability time no earlier than that coverage. A positive needs identity/chamber/date evidence and an explicit first-passage assertion, with assertions distinguished from verified sources. Preserve malformed, missing, ambiguous, already-resolved, late-window and unavailable cases in a complete disposition ledger. An outcome-free source pilot supplies collection evidence, not a rate estimate or population validation.
3. **Chronology and families:** freeze training origin and require training labels to be effective and available before it. Purge intersecting evaluation families before fitting; family completeness remains a review gate. Repeated bills or family members are not independent events. Never use future outcomes to select representatives or to decide whether to retain a source.
4. **Comparison:** exact case, target, checkpoint and horizon pairing is required across challenger and reference. Stage/chamber smoothing and fallbacks must be fixed and training-only. Reject duplicate, missing, extra, non-finite and out-of-range predictions. Include a no-event evaluation without interpreting its attractive loss as event detection or successful validation.
5. **Practical success:** a 2% relative Brier reduction requires the paired contrast `Brier_challenger - 0.98 * Brier_reference`, with the prespecified upper uncertainty bound below zero. An interval for any improvement alone is insufficient. Report raw losses, denominators, period results, calibration counts, log loss and fixed-workload prioritization. A zero-loss reference makes relative skill undefined. Adequacy floors are not power calculations; two Congresses cannot support broad political-period generalization.
6. **Ledger and launch:** preserve exact raw bytes and failed/partial acquisition receipts, use atomic append-only operations, rehash existing content, and validate the predecessor chain. Test duplicate/concurrent writes, partial operations, clock rollback and source completion after cutoff, including subsecond boundaries. A local receipt or caller-provided `certified: true` must never satisfy independent attestation. Certified issuance remains blocked until a real verified external attestation adapter and applicable source/model/family/review gates exist.
7. **Failure evidence:** demonstrate a valid path, demonstrate rejection of bad evidence, and deliberately remove selected safeguards in a disposable copy to show the independent test catches the defect. Preserve each failed attempt and its disposition. Do not edit frozen real artifacts or retrospectively issue missed forecasts.

## Concrete implementation findings and repairs

The reviewer challenged the independently authored new modules before live acquisition. These were development defects, not failures observed in historical predictive results.

- **Duplicate issuance through equivalent time spellings:** a valid local paired receipt using `2027-03-03T00:00:00.000000Z` could be issued again under the same registration and bill using `2027-03-03T00:00:00.000000+00:00`. The first implementation keyed duplicates on the raw string, and its verifier reported two forecast pairs. The implementer changed both issuance and verification keys to normalized instants. Independent replay now rejects the second receipt and preserves exactly one valid receipt.
- **Ambiguous source identity accepted:** separate synthetic XML probes with two contradictory `number` fields, two `bill` elements, and mixed contradictory modern/legacy identity fields each returned `identity_valid=True`. The implementer added exact root/bill/scalar cardinality and rejected unsupported mixed/legacy forms. Independent replay rejects all three while preserving the valid source and issuance control. Legacy support is an explicit future adapter decision, not a reason to accept ambiguous fields.
- **Synthetic/real reference crossover:** inspection found that reference artifacts did not bind evidence mode, allowing a synthetic-trained reference to predict a retrospective row. The implementer added artifact mode binding and prediction checks. Independent execution now rejects crossover.
- **Pre-Congress prepared row:** the original row validator checked the horizon against Congress end but did not reject a window entirely before the Congress. The implementer added the earliest possible day-30 checkpoint bound and stronger label time checks. Independent execution rejects the constructed pre-Congress row.
- **Collector/runner status mismatch:** the pilot runner originally expected `captured`, while the ledger reports successful captures as `complete`. This would have stopped after a successful first inventory request. It was found by interface inspection before live acquisition, corrected, and covered by an end-to-end mocked-transport pilot test. The pilot also binds capture receipts to its collection registration.

The equivalent-time bypass was reproduced against ledger SHA-256 `80383697fe725d0ea521e6a0944daede4770e2e7ecb7b5f4785ac136ba011a24`. The repaired ambiguity and duplicate probes passed against `23db7ff6d99242f9b46a94027d1ba942326e494d1ce0b7f83eba9285f912365c`. These identify intermediate reviewed snapshots, not a claim that later files remain byte-identical. The parent execution receipt records final code bindings.

## Independent checks actually executed

Ran `python3 -m unittest tests.test_passage90_source_pilot tests.test_passage90 tests.test_forecast_ledger -q`: all 67 tests in that snapshot passed. This includes a full collector/persistence pipeline with mocked transport. Later added tests and complete-suite totals belong to the parent execution receipt; this review does not retroactively claim those runs.

A separate four-case, two-period synthetic arithmetic probe used outcomes `[0, 1, 0, 1]`, challenger probabilities `[0.1, 0.8, 0.2, 0.7]`, and reference probabilities `[0.3, 0.4, 0.3, 0.4]`. Independent literal arithmetic agreed with equal-period Brier losses `0.045` and `0.225` and the practical contrast `0.045 - 0.98 * 0.225`. Reliability counts and top-one event precision also matched. The family bootstrap retained 8,728 of 10,000 draws in this deliberately tiny fixture; the required 9,000-valid-draw floor correctly remained unmet. These artificial probability values are controls, not fitted models or forecasting performance.

For a sensitivity check, copied the passage module into a temporary directory and removed only the probability-range rejection. The independent probe requires rejection of probability `1.2`. It passed against the real module and failed against the deliberately weakened copy; the valid arithmetic control passed. The tracked module and real evidence were never modified by this mutation test. Passage snapshot SHA-256 was `464deba397e211052417142c75ea42a1f8baf3d352c44ec4aa7dc7042d0f85c9`.

## Review disposition and remaining limits

The staged plan and repaired foundation are suitable for the bounded source-only acquisition pilot. They are not a launch-ready prospective study. The new ledger records local-only caller-computed paired probabilities and explicitly blocks certification; it does not recompute a reviewed trained challenger or verify the truth of at-risk/source-completeness assertions. Socket timeout is an operation timeout, not an overall wall-clock acquisition deadline. A local hash chain cannot prevent complete malicious rewriting of the local ledger or supply an independent timestamp.

The review requested preservation of parser/selection failures and rechecking frozen bindings before dependent source requests; the parent implemented these before acquisition. Runtime service checks and complete-suite checks remain attributable to the execution that performs them. Qualified source/family review, a trained passage model, external attestation, future issue coverage and matured outcomes remain unresolved. No result here establishes predictive gain.

## Independent replay of the completed source pilot

The root agent completed the fixed pilot in `data/research-runs/passage90-source-pilot-v1-20261112/`. This reviewer made no additional requests. Wrote a separate [verifier](../../../scripts/verify_passage90_pilot_v1.py) that imports none of the collector, pilot, inventory, metadata or forecasting implementations. It opens the database read-only and independently recomputes canonical receipt hashes, raw hashes/sizes, chronological chain links, registration/source bindings, inventory identities, deterministic sample ordering, XML bill identities, introduction/window arithmetic, and every first recognized originating-chamber action/disposition.

Both normal and optimized Python replay passed for all seven registered code/protocol bindings, 45 ledger receipts, 22 raw responses, two directory inventories (10,564 H.R. and 5,649 S. identities), and all 20 selected bill cases. This is an all-case replay, not a sample audit. It reproduced 7,962,656 total response bytes, 20 captured/inspected/full-window cases, 17 unresolved records without a recognized passage, two later-passage records with unverified negative coverage, and one within-window candidate. Certified positive labels, certified negatives, historically eligible features, external attestations, fitted models, issued forecasts and predictive scores all remain zero.

The three recognized first-origin dates are H.R.6229/118 on December 10, 2024 (after horizon), S.2861/118 on May 8, 2024 (after horizon), and S.4367/118 on August 1, 2024 (within window). The other 17 individually checked identities are hr8104-118, hr3600-118, hr927-118, hr6917-118, hr1041-118, hr5518-118, hr438-118, hr3401-118, hr1307-118, s883-118, s4621-118, s4010-118, s4627-118, s1171-118, s3843-118, s1772-118 and s4525-118. Absence of a recognized action remains unresolved; this replay does not certify complete action histories or true first passage beyond the recorded exact action semantics.

Reproduction commands, run from the repository root:

```sh
python3 -m scripts.verify_passage90_pilot_v1 data/research-runs/passage90-source-pilot-v1-20261112
python3 -O -m scripts.verify_passage90_pilot_v1 data/research-runs/passage90-source-pilot-v1-20261112
```

Preserved independent evidence:

- Registration raw SHA-256: `63bcaa56f46899bf97e75661a9c3528eaece58844c64e7c4a5de7e26dd8dffd2`.
- Sample raw SHA-256: `fd3df19b3e4cf062be9ad845abd99fdef0c651bf8b57d71d6324c0a1ba10f5bf`.
- Result raw SHA-256: `a702124589deeacdbdfdaa87238a36ed7bd388319d84947a7260802da3ea190e`.
- Independent verifier source SHA-256: `85417a29cad9a9573c9b421f3b6fba50bfd32689c33d94775494003962603ca0`.
- [Independent all-case replay](../../../data/research-runs/passage90-source-pilot-v1-20261112/independent-verification.json), SHA-256 `0d7ef33bbb891c4f443e322ccfc88a476d1bb741b8f6c043d8e54a736593f7bb`.
- [Independent adversarial replay checks](../../../data/research-runs/passage90-source-pilot-v1-20261112/independent-adversarial-checks.json), SHA-256 `b34e3aeb3691e62d56a7ff3088cbe87dafd97f265943a429e4b46c7226333e37`.

Three disposable copies of the completed run were separately altered: one raw response gained a byte, the first two selected cases were swapped, and the summary claimed 17 certified negative labels. The independent verifier rejected each respectively with raw-hash mismatch, frozen-sample mismatch, and unsupported-certification errors. The unmodified original passed again afterward. No original bytes, registrations, samples or results were changed. Runtime evidence links require the ignored local run directory and are not publicly committed data.
