# BICAM historical inventory audit — 8 November 2026

## Decision and scope

The bounded acquisition succeeded; both separately registered inventory attempts stopped on source compatibility or missing identity fields. No complete census, 100-case sample, version-reference interpretation, outcomes, text features, predictive fits, probabilities or promotion resulted. This batch measures source readiness, not prediction performance. The prior 595 evaluated bills remain exposed; they were not reused for tuning.

Three agents handled acquisition, prospective context acceptance, and independent review. The intended population was House/Senate bills in Congresses 113–118; the deterministic sample would have been selected without outcome values. CSV parsing traverses all source columns, but inspection/projection uses identity/date fields only. Raw downloads remain ignored local evidence.

## Frozen acquisition and limits

Source: https://downloads.bicam.net/bills/bicam_bills.zip. Existing archive directory identified two members: bills.csv and ref_bill_version_codes.csv. Exactly six GETs retrieved local headers, filename/extra fields and compressed payloads. Every actual response was HTTP 206. Total response bodies: **29,415,382 bytes**. Exact object ETag/version, Content-Range, lengths, ZIP headers, raw-deflate EOF, CRC32 and decoded hashes were checked. No text-member download or retry occurred.

Limits: 50,000,000 compressed-member bytes, 300,000,000 decoded bytes, six requests, no redirects/retries; up to 262,200 variable-header bytes. Socket timeout 20 seconds; 180-second elapsed checks before requests/reads are not a hard processing deadline and blocking reads can overshoot. Parsing/decompression are outside that deadline. HTTP-error bodies are not guaranteed retained; all actual requests succeeded.

| Request | Member part | Range start | Bytes | Status | Body SHA-256 |
|---|---|---:|---:|---:|---|
| request-01 | bills.csv.header.bin | 0 | 30 | 206 | `512e80735bda68a03572ed0697540970e431e30799f35ab6c655ec181f910f7e` |
| request-02 | bills.csv.name-extra.bin | 30 | 9 | 206 | `5c2fdbdebe8dfad9964893ffab12b9deccbddbbe81372743efddf94ace582845` |
| request-03 | bills.csv.deflate.bin | 39 | 29412214 | 206 | `aa9b95221a707eeb7380ba1884d9399656ec1b645b8c54b040cb182a4e0b736e` |
| request-04 | ref_bill_version_codes.csv.header.bin | 1934544123 | 30 | 206 | `368f6e4a2dc82264624515f68663b235478daaed21e832acad1581c943debf4b` |
| request-05 | ref_bill_version_codes.csv.name-extra.bin | 1934544153 | 26 | 206 | `1c3745cf2e5fa540831af48cff6402b42aa84bea31d1e0fa2b223294745b5bc1` |
| request-06 | ref_bill_version_codes.csv.deflate.bin | 1934544179 | 3073 | 206 | `40b592861c224d3526522c62ef67dee0a4f24ec8ff9527b019a64b4c40f0332a` |

| Decoded member | Bytes | SHA-256 |
|---|---:|---|
| bills.csv | 129706006 | `b1c21c729eedcc9868424d9f8813bf8d40c074d120445428ea90bbca99025832` |
| ref_bill_version_codes.csv | 14192 | `903dc1df42f67b401228efb5ec25adbac283ed5c8c8573f0ed24c133f0783f66` |

## Preserved failures and adaptive successor

v1 stopped with “Malformed CSV row.” Conventional reading yielded 414,376 parser records: 414,178 with 24 fields, 99 with five and 99 with twenty. These are parser records, not certified bill counts. The source also contains integral-decimal Congress strings. No malformed rows were silently discarded.

Separately registered offline v2 declared an LF/CRLF-record compatibility assumption. Its quote-aware scanner escapes only unquoted bare carriage returns in the fifth/title field, records exact offsets and requires inverse byte equality. Quoted CR/LF and doubled quotes remain preserved. It accepts positive integer Congress strings with optional all-zero decimal suffix, rejecting fractional, exponent, nonfinite and whitespace values. This is an identity projection, not a model text transformation or proof of publisher intent. No new network request occurred.

v2 then stopped with “Congress not exact positive integral decimal.” No census or sample was persisted. A subsequent explicitly post-failure structural diagnostic saved the offset ledger and complete Congress-error list: **414,277 logical rows**, **99 reversible title escapes**, **43 blank Congress fields**, all also blank introduction dates. This does not establish that all other fields are valid. Five IDs indicate target-period Senate bills: s5543-118, s5314-118, s4653-116, s4899-117 and s5575-118. Identifier-derived membership is not a replacement for missing authoritative fields.

The registered v2 attempt computed offsets in memory but failed before saving them. The later diagnostic ledger is separate evidence; it is not represented as successful registered output. Both original failures, code, tests and protocols remain frozen.

## Every missing-Congress case

Rows below are logical data-row positions under the declared v2 dialect. Congress and introduced_at are empty in every listed case. No outcome-based exclusions were made.

| Row | Bill ID | Type | Number |
|---:|---|---|---:|
| 1154 | sres350-116 | sres | 350 |
| 2833 | sres259-103 | sres | 259 |
| 4715 | s2650-103 | s | 2650 |
| 22084 | sres742-116 | sres | 742 |
| 32124 | hconres134-118 | hconres | 134 |
| 33314 | s5543-118 | s | 5543 |
| 35600 | sres5-103 | sres | 5 |
| 40504 | sres897-118 | sres | 897 |
| 40505 | sres902-118 | sres | 902 |
| 40508 | sres924-118 | sres | 924 |
| 42091 | hres1611-118 | hres | 1611 |
| 46151 | s5314-118 | s | 5314 |
| 49317 | hres477-107 | hres | 477 |
| 60159 | s4653-116 | s | 4653 |
| 63047 | sres913-118 | sres | 913 |
| 71753 | sres915-118 | sres | 915 |
| 82932 | sjres117-118 | sjres | 117 |
| 83004 | sres905-118 | sres | 905 |
| 83005 | sres906-118 | sres | 906 |
| 85340 | sres4-103 | sres | 4 |
| 90701 | sres528-112 | sres | 528 |
| 91663 | hres351-106 | hres | 351 |
| 96874 | s4899-117 | s | 4899 |
| 101002 | sres900-118 | sres | 900 |
| 102622 | sres925-118 | sres | 925 |
| 108660 | s2452-103 | s | 2452 |
| 109760 | sres514-113 | sres | 514 |
| 109761 | sres515-113 | sres | 515 |
| 113376 | sres6-103 | sres | 6 |
| 115427 | sres904-118 | sres | 904 |
| 117145 | sres261-103 | sres | 261 |
| 120994 | sres256-107 | sres | 256 |
| 123128 | sres260-103 | sres | 260 |
| 128579 | sres907-118 | sres | 907 |
| 131125 | sres499-111 | sres | 499 |
| 132730 | sres68-105 | sres | 68 |
| 160885 | hres1585-118 | hres | 1585 |
| 163033 | sres899-118 | sres | 899 |
| 193400 | sres926-118 | sres | 926 |
| 194544 | sres448-116 | sres | 448 |
| 196435 | sres892-118 | sres | 892 |
| 196436 | sres921-118 | sres | 921 |
| 201305 | s5575-118 | s | 5575 |

## Validation and interpretation

Independent preflight: 22 v1 tests and 12 v2 tests passed normally and under optimized Python. Root reran all 34 in both modes successfully. Tests cover hostile HTTP metadata, archive integrity, identity conflicts, deterministic sampling, quoted/multiline CSV, exact-integral syntax and reversible offsets. These software tests do not certify source completeness or historical timing.

Root preservation verification: all 1,232 inventoried prior artifacts unchanged; frozen paper/model audit identical. Independent replay verified all six ranges and both CRCs, reproduced both registered failures, reconstructed and reversed all 99 offsets, and matched all 43 missing-field records. Full suite: **675 tests passed in 81.593 seconds**. All nine registered code/test/protocol bindings match. Research lease released after validation.

## Next bounded decision

Stop parser expansion. Reconcile the five target-period missing-field cases against official identity and introduction records in a separately specified enrichment study; retain all 43 source defects. Define any eligibility/missingness rules before sampling, preserve raw values and explicit provenance, and audit selected-period coverage against an official inventory. Missing dates must not be inferred merely from identifiers. Only then freeze an outcome-blind sample and inspect introduced editions and dated context. The version-reference member is downloaded but not semantically inspected in this run.

The [context acceptance specification](../../research/BICAM_CONTEXT_ACCEPTANCE_V1.md) fixes candidate sponsor affiliation, dated cosponsorship, committee referrals and recent procedural activity before new scores. Current party, final cosponsor counts and undated annotations cannot stand in for historical values. Keep the stage benchmark in any later registered comparison. No additional fit on the already evaluated 595 cases; no 60% achievement claim, model promotion or self-labeling.

A primary [BICAM dataset paper](https://www.nature.com/articles/s41597-025-05737-8) supports the expansion route. The indexed Harvard Dataverse deposit is a distribution/license lead only: direct live verification was unavailable, and its text packaging must not be conflated with the website archive. Historical availability, complete coverage, source license applicability and predictive eligibility remain unestablished.

## Reproduction and artifact identities

Run tests with `python3 -m unittest tests.test_bicam_inventory_audit_v1 tests.test_bicam_inventory_independent tests.test_bicam_inventory_offline_v2 tests.test_bicam_offline_independent`; repeat with `python3 -O`. Frozen protocols describe their own execution commands. Do not overwrite existing run directories or rerun acquisition merely to reproduce arithmetic. Independent offline evidence is in the ignored run directories below.

[Independent review](../../research/reviews/20261108-bicam-inventory-audit.md), [v1 protocol](../../research/BICAM_INVENTORY_AUDIT_V1.md), [v2 protocol](../../research/BICAM_INVENTORY_OFFLINE_V2.md).

| Artifact under data/research-runs | SHA-256 |
|---|---|
| bicam-inventory-audit-v1-20261108/failure.json | `cde949b23d79bba1a57e24c352ea869e8cb0d05f7ce1a6646143d707e7537754` |
| bicam-inventory-audit-v1-20261108/independent-review.json | `3d21f3a3c03e54d7ddceaa5ec80c7c5ed77150a4b8e2984f8d6a6da16c4f46d8` |
| bicam-inventory-audit-v1-20261108/registration.json | `5c6884054e54e9f16c3f0dff4777a6de41d31af55906ee8cf258d1040c6580cf` |
| bicam-inventory-audit-v1-20261108/request-01-intent.json | `49262e20034969050665f81e4494617498bbec31805826b682c24aad64254890` |
| bicam-inventory-audit-v1-20261108/request-01.json | `68a0051ac2203ed8e2896c04495d58e8547163778634d0bd5f2f5aa59aa212f8` |
| bicam-inventory-audit-v1-20261108/request-02-intent.json | `0181f262861dfaf01af3552d0e7c8f25abc0e1b783acd826af3b273c2eb40ace` |
| bicam-inventory-audit-v1-20261108/request-02.json | `475a0f4f6cf8926af5ee93924108c070d79759709be760f645fae395cc690753` |
| bicam-inventory-audit-v1-20261108/request-03-intent.json | `c62df5757da19945f81df08ac9f88464bb07bda8eb2d82c80d693e198884568f` |
| bicam-inventory-audit-v1-20261108/request-03.json | `678ebfcce5929b1fd4b83a7a96f818c77343b9bc447135737f3111c94bd08e0a` |
| bicam-inventory-audit-v1-20261108/request-04-intent.json | `cb24d39fb98d8b5d87345ea1feb4c34ec74256b8132715dea1865612aa1f0ee8` |
| bicam-inventory-audit-v1-20261108/request-04.json | `b5711fea2233606bd4c94e3cc9920057f091ef328c2709bcd5f71b7034085fc5` |
| bicam-inventory-audit-v1-20261108/request-05-intent.json | `e9f79f36a3455a99757228639cce00f299b5eec58bf1c13265d47d105f6ab992` |
| bicam-inventory-audit-v1-20261108/request-05.json | `fcacbb7deedef5284fb606b8551c103745f9f4989c70b28a86f7b0abd42f1954` |
| bicam-inventory-audit-v1-20261108/request-06-intent.json | `dbb439786167e0c92ff5db98ad2abde23291a6049dabb01f7a096fb8946df91c` |
| bicam-inventory-audit-v1-20261108/request-06.json | `74a4b38c7711f81e5d05cda9e16176e1428146b01b3e536353dfd123c1098ead` |
| bicam-inventory-audit-v1-20261108/structural-diagnosis.json | `672c6d9bb27ac85215e20ec9e1c385348d4b35addcc6ce48a61dbca038fb0ff9` |
| bicam-inventory-offline-v2-20261108/diagnostic-congress-issues.json | `ff20ebb3681061c404f9fb86bcc98b02b084f5302bb4e5886718a4e38487706f` |
| bicam-inventory-offline-v2-20261108/diagnostic-title-cr-offsets.json | `3f8745ff673110e43cf38cc26dd03e6582db8af316d35df0bee05b9cef5f4989` |
| bicam-inventory-offline-v2-20261108/failure.json | `f4992ca870db342a70384972fbfb6a3f32ef865951ea729fff2cf4897d2a638e` |
| bicam-inventory-offline-v2-20261108/independent-diagnostic-review.json | `699da472e67c77c103c93bfcd72160d525314e9e1c7380e5117ac40796f6fe76` |
| bicam-inventory-offline-v2-20261108/independent-review.json | `d1f44db9abb819bffb767a54976a362246a7765a49545e318075a5a8e4727c2b` |
| bicam-inventory-offline-v2-20261108/registration.json | `ba32c1ea6f68e50921871d75c1b9744acd28c5b08f558c72a1f08ac6db02b252` |
| bicam-inventory-offline-v2-20261108/independent-diagnostic-review.json | `699da472e67c77c103c93bfcd72160d525314e9e1c7380e5117ac40796f6fe76` |

### Frozen code and protocol bindings

| Version | Registration field | SHA-256 |
|---|---|---|
| bicam-inventory-audit-v1-20261108 | code_sha256 | `e011581e6e93fb5b0dc94d82f1dca56358c467f41398348fb5acd723f01d6c02` |
| bicam-inventory-audit-v1-20261108 | independent_tests_sha256 | `990910e52d0573a4de57bba2659cc33192ec2df27d539f3bd5c548f67d5744f0` |
| bicam-inventory-audit-v1-20261108 | prior_result_sha256 | `cd41f8a2af88fd17ffc7abe27dea521f1367c52d3e231a97290d7a7d14202b5b` |
| bicam-inventory-audit-v1-20261108 | protocol_sha256 | `a444441c5e9bb3f888598d7ea75bce2137711f85e0a5529872a0a94568c94d97` |
| bicam-inventory-audit-v1-20261108 | tail_sha256 | `8fa40bc106615a3243e505e6d44d8bd4a02119c957412880175ff71166d68a49` |
| bicam-inventory-audit-v1-20261108 | tests_sha256 | `41cd6f24a42e437ae7e10c9b33c52460deb89f437949bd8adcc6b05a78f37b23` |
| bicam-inventory-offline-v2-20261108 | code_sha256 | `99e00643d24e3c9a78565c3e0d3f044d924468df38f2b0fd656b4445dbeccce3` |
| bicam-inventory-offline-v2-20261108 | imported_v1_sha256 | `e011581e6e93fb5b0dc94d82f1dca56358c467f41398348fb5acd723f01d6c02` |
| bicam-inventory-offline-v2-20261108 | independent_tests_sha256 | `165ea2db769794205e4daba870926e4e60ad02d116937abf1b6c02e9816e3fc6` |
| bicam-inventory-offline-v2-20261108 | previous_failure_sha256 | `cde949b23d79bba1a57e24c352ea869e8cb0d05f7ce1a6646143d707e7537754` |
| bicam-inventory-offline-v2-20261108 | previous_registration_sha256 | `5c6884054e54e9f16c3f0dff4777a6de41d31af55906ee8cf258d1040c6580cf` |
| bicam-inventory-offline-v2-20261108 | protocol_sha256 | `8cf97ad3ca9f5539a620887aecd3313d39a0ebb9c0ed1aefc21848da8a4593d0` |
| bicam-inventory-offline-v2-20261108 | source_sha256 | `b1c21c729eedcc9868424d9f8813bf8d40c074d120445428ea90bbca99025832` |
| bicam-inventory-offline-v2-20261108 | tests_sha256 | `d0bacd323c865042a56471e3f5c98962c684814f026d39f203833681829cc45b` |
