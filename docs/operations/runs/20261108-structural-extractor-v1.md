# Structural-boundary extractor v1 — null design result

2026-11-08. **No real-bill hit changed boundary eligibility:** all 2,722 raw locators remain structurally usable; combined context-filter retention stays 2,403, and quotation overlap stays 449/501. This is an informative null design result, not improved semantic accuracy or a forecasting experiment.

## Question, versions and pre-run setup

Question: does screening frozen lexical matches against explicit table-cell boundaries remove concatenation-derived locators while preserving full bill/fraction context? Baseline is frozen v5 lexical extraction plus filter v3. The new `mechanism-structural-extractor-v1` uses authenticated `structural-input-v1` sidecars without altering lexical rules, original candidates, reference offsets or text.

The exact forty exposed design bills were used, eight each from Congresses 113–117. References remain corrected v3: 501 provisional effects. Protected quality was excluded, with no substitutions, new outcomes, acquisition, model fits or forecasts. All source/view/sidecar/raw-baseline/filter bindings and canonical sidecars were checked before registration.

A cell start or end strictly inside a hit flags structural usability; endpoint touches remain usable. Empty, nested and orphan cell boundaries are included conservatively. Every raw hit and complete candidate context remain in `raw_output`, and `full_context_text` retains the whole bill. Fractions attach literal ±32-code-point context when that context intersects a hit; no value is inferred. This is a deterministic locator consumer, not a learned semantic extractor.

- Prior v5 result: `e75c04b8b4b29e4e9665c3b91cfee3699ee4d5789edd99154daf7fbbbe3cfb79`.
- Structural input result: `f3505ea7c8618d686c0401790130ad619c0c73a0812fca21e05a0559706c3bb0`.
- Reference: `8d6da3e94e901c953334548d60617112fe8ea3408219d6e6d4b9d009a2805bd5`.
- Registration: `59f6003bd437cfc88b3aa3c4d1b8031d4826b997f3086bad2c8706fde2d1dcc0`; 205 input files and 52 code/test/fixture files pinned before extraction.
- Result: `7e65d21b79de0c1bf1a01c2b6192e3aa0c1641fdf877f7e7d88fa5f286c7c2af`.

[Registration](../../../data/research-runs/structural-extractor-v1-20261108/registration.json), [result](../../../data/research-runs/structural-extractor-v1-20261108/result.json) and forty `<bill_id>.json` output envelopes are retained in ignored local runtime data. Code is reproducible with those exact frozen inputs.

## Metrics and complete category results

Raw hits count unique mechanism/start/end identities. Boundary-usable means no explicit cell edge lies strictly inside that hit. Combined retention is boundary-usable AND retained by the unchanged filter v3. Quote overlap counts provisional reference effects whose half-open interval intersects at least one same-mechanism hit. It is not semantic precision or recall.

| Mechanism | Raw before / after | Boundary flagged | Context-retained before / combined after | Quote overlap before / after | Reference effects |
|---|---:|---:|---:|---:|---:|
| amend | 525 / 525 | 0 | 484 / 484 | 33 / 33 | 34 |
| appropriate | 156 / 156 | 0 | 124 / 124 | 4 / 4 | 5 |
| authorize | 335 / 335 | 0 | 298 / 298 | 89 / 89 | 97 |
| create_programme | 274 / 274 | 0 | 205 / 205 | 15 / 15 | 28 |
| deadline | 301 / 301 | 0 | 287 / 287 | 58 / 58 | 60 |
| prohibit | 98 / 98 | 0 | 86 / 86 | 49 / 49 | 56 |
| rename_designate | 92 / 92 | 0 | 80 / 80 | 13 / 13 | 18 |
| repeal | 137 / 137 | 0 | 137 / 137 | 6 / 6 | 6 |
| reporting | 221 / 221 | 0 | 175 / 175 | 50 / 50 | 54 |
| require | 507 / 507 | 0 | 478 / 478 | 123 / 123 | 127 |
| sunset | 48 / 48 | 0 | 34 / 34 | 6 / 6 | 9 |
| tax | 28 / 28 | 0 | 15 / 15 | 3 / 3 | 7 |
| **Total** | **2,722 / 2,722** | **0** | **2,403 / 2,403** | **449 / 449** | **501** |

Raw and boundary-only quotation overlap also both equal 449/501. No reference intersections were lost or recovered. All 480 mechanism statuses remain abstentions; five legacy proposals remain quarantined and no active proposal or accepted label is emitted. No confidence interval for predictive improvement is applicable because no predictive measurement occurred.

## Every bill

| Bill | Raw / boundary usable | Combined retained | Quotation overlap / effects | Output seal |
|---|---:|---:|---:|---|
| 113-hr4429 | 24 / 24 | 15 | 5 / 6 | `d101f5b67f485e3de780e434d681c08f90ac140c1857716b0b92fc2d058518d7` |
| 113-s2088 | 39 / 39 | 35 | 11 / 12 | `1566b7b9459acd3e5d7bff9fdba65dbc43246be9abb01ccedabfa82d115662f2` |
| 113-hr1979 | 28 / 28 | 21 | 5 / 8 | `22e248187e649f66555a8323a78a7a3c4be88e30df755bd3c4bcb9af019dad21` |
| 113-s439 | 61 / 61 | 48 | 14 / 14 | `97e63e5a4c0ae346fe5115714cd23da5707d029ecb5304ac5ab28976307b1029` |
| 113-hr128 | 57 / 57 | 55 | 10 / 12 | `7323cb79fb7d4d3bc774236bc2ed24d0ef115333822443c0b16ba190c23489c2` |
| 113-s5 | 1 / 1 | 0 | 0 / 0 | `86d3d85f68d2296f9d2ff6aaa7b63c2217ea3344eab9603093127edf0f3c3daa` |
| 113-s848 | 8 / 8 | 7 | 3 / 5 | `d16c2a1a8a00a18bc6105c4f9aaca0c9e26eb2044185e5d05b4d1e1e6e12e3d2` |
| 113-hr1257 | 16 / 16 | 10 | 1 / 2 | `6b5ba44411eae98f781da163ab04b605ab3ca0ea98d6e5f6eeea2fb737c8d292` |
| 114-s1259 | 66 / 66 | 54 | 20 / 20 | `90fb07aa78c247231e5a0e4312f46ffe88692ad3c8611f9837ae1d9ab4fa72df` |
| 114-s375 | 31 / 31 | 24 | 2 / 4 | `a0206c1f91e5166d035d2a4fb2584b5e427381ff2dbd1bb24015a20abfe17ab0` |
| 114-hr3803 | 113 / 113 | 100 | 6 / 8 | `0f01d90ff2f07c72adca88430edebdc98de4d268ecb223c90d4a7cde2d3b0faf` |
| 114-s2940 | 24 / 24 | 16 | 3 / 3 | `1a4f46044b53d2344b5b92ce2ac4564dce3eed6e60354159fc5d4e73a5341e74` |
| 114-hr2575 | 7 / 7 | 4 | 1 / 1 | `dc6797f82391abf72aa5920ff676250538b233d2fb7736b3f299453ad875d6d2` |
| 114-hr5053 | 36 / 36 | 29 | 4 / 6 | `c61fde567d8cb37432c7cb28f21d550197485ab0c411246ad3a66d2871fe31bc` |
| 114-s2769 | 16 / 16 | 12 | 7 / 7 | `5ee9f75b93a865ce7fcbc77e5d3bf79d46ed32ceae9a934100ffc721bee7dc3e` |
| 114-s2388 | 42 / 42 | 39 | 13 / 15 | `ef7ef8a4c0c134a722f8d9c1b9febe34ffd39a09f4b1d40309b227cb80b0fa06` |
| 115-hr5527 | 43 / 43 | 25 | 10 / 11 | `e7c60a704ea0a4c9b114a90bcc04c852b6e5787e8cede89438c87a62d0419fd8` |
| 115-s1372 | 22 / 22 | 19 | 9 / 9 | `a25c242fde4da18965227196bde77e97295fce9ba2525a06e24817daf854d19f` |
| 115-s1809 | 93 / 93 | 77 | 19 / 21 | `d805091f9d11d46416b8e6ad82881baeb50ac2ce675a9eb20f49656ddcc70747` |
| 115-hr1714 | 5 / 5 | 4 | 1 / 1 | `05e4c138983399c6ad14ed99abcbb2fcd089d5e61319764ab5ea068ad9425358` |
| 115-hr5589 | 24 / 24 | 21 | 9 / 9 | `93d604bdb7b4ab9d71f2c09d3df5a15f8b732210e7260cea4e6820759b277808` |
| 115-s284 | 50 / 50 | 47 | 8 / 10 | `5650e484f02b0e3bd8292261d7f9e308a5d2a8f7a096c414c18e7bb9db8644ef` |
| 115-hr2259 | 192 / 192 | 180 | 32 / 34 | `d580d1fbff36d7f20ac98eafe4ac77970a8388c8c56a48032b54974ec4fdc833` |
| 115-s1657 | 452 / 452 | 424 | 43 / 47 | `d981c30d373caabd700566069635237699c10aa4f8123f9daf2f1adaab1ad353` |
| 116-hr2943 | 2 / 2 | 1 | 1 / 1 | `b616702262c4f545388c5abe5d7b1efcbc56caf8ddc03b4a3f8c1c7bd2a7eb6d` |
| 116-hr846 | 73 / 73 | 62 | 14 / 15 | `2f9d3038abbd4aa9c60637066727ad107864170558309281a2bfa72ce70e4e9a` |
| 116-hr7433 | 21 / 21 | 19 | 4 / 6 | `d11aff1b3d7a6da1820fb4c86dd909122d0132189663fbc516ac3646593aba7e` |
| 116-hr3024 | 17 / 17 | 16 | 2 / 3 | `7677428e1c776ca1b9845680d83f6530012d4fac99d0c2489fb15fda61d5e089` |
| 116-hr3777 | 184 / 184 | 161 | 15 / 16 | `796b57374da8959a064c8ee51f3dfbec4de5893b292420422a3fde2b3b43b7b7` |
| 116-s1076 | 88 / 88 | 72 | 23 / 25 | `8f2fec2519dd9821abbf5cce7e746afe151c309ab7b45c1113e155e212bb7c2c` |
| 116-s2089 | 13 / 13 | 11 | 5 / 6 | `14bff5dbef9ed41894aa0e9b25ae1fc65f461d2da4b5c743b3b5b8bb2f31c394` |
| 116-s856 | 39 / 39 | 36 | 8 / 8 | `40a12995e493dfe157fb360ede58b07304e3a25c5c024a659894347b1e71c599` |
| 117-s4377 | 13 / 13 | 8 | 4 / 4 | `260c695ccd5feb7325750e52ceca04f606ad12a6d4162668e61826775183802f` |
| 117-s1230 | 44 / 44 | 43 | 8 / 9 | `822d847fea846f0d86d94e7670230209f1e5f6f31e0851745975a70e198a6b17` |
| 117-hr1662 | 45 / 45 | 35 | 12 / 12 | `503626924a2b572ee45775ac0b7b224043eaef0aa72954f671e382cb7e4e9d83` |
| 117-s825 | 117 / 117 | 104 | 30 / 36 | `355ab9b5e5e448739168d95df9eef11ce498f036914a79b699f13a3fe49c20a5` |
| 117-hr2448 | 21 / 21 | 16 | 3 / 3 | `aad26098f422262f1b59c18ab54098c8bf27e20fb0e04e724dce3a98552ed8d7` |
| 117-hr6835 | 12 / 12 | 11 | 3 / 4 | `68d837c2cfdfede04b1d22ac7df5578542f010573d0f0be2690956a18a43f90c` |
| 117-hr1597 | 437 / 437 | 417 | 57 / 64 | `e1f081b7aa5c04494c99370e1a1da5db11c7c130832f86ccaa088dbb9abb23b4` |
| 117-hr5229 | 146 / 146 | 125 | 24 / 24 | `ee36743bef06931991d5b776f367e11a11f96a1fab15b5c164be71e1749e000e` |

## Complete structural-associated review population

The predeclared review selects every flagged hit, every hit contained in/intersecting a cell, and every hit intersecting a fraction context. The result has **17 cases: 14 table-associated and three fraction-nearby hits; zero boundary flags**. This is a census of that definition, not a random sample or full semantic review of all 2,722 hits. The land-description fraction in 117-HR1597 has no hit within its ±32-character context; its literal input remains available.

| Bill | Mechanism | Hit [start,end) | Exact hit | Association |
|---|---|---:|---|---|
| 113-hr128 | prohibit | [3770,3790) | `no broadcaster shall` | fraction context |
| 113-hr128 | require | [3785,3790) | `shall` | fraction context |
| 113-hr128 | require | [3991,3999) | `required` | fraction context |
| 114-hr3803 | authorize | [2232,2235) | `May` | table cell |
| 114-hr3803 | authorize | [2258,2261) | `may` | table cell |
| 114-hr3803 | appropriate | [2330,2344) | `Appropriations` | table cell |
| 114-hr3803 | appropriate | [2368,2381) | `appropriation` | table cell |
| 114-hr3803 | appropriate | [2429,2442) | `appropriation` | table cell |
| 114-hr3803 | reporting | [1845,1852) | `submits` | table cell |
| 114-hr3803 | reporting | [1924,1931) | `submits` | table cell |
| 114-hr3803 | reporting | [1932,1938) | `report` | table cell |
| 114-hr3803 | reporting | [2026,2032) | `submit` | table cell |
| 114-hr3803 | reporting | [2108,2114) | `report` | table cell |
| 114-hr3803 | reporting | [2355,2362) | `reports` | table cell |
| 114-hr3803 | deadline | [1772,1778) | `before` | table cell |
| 114-hr3803 | deadline | [1969,1983) | `Not later than` | table cell |
| 114-hr3803 | deadline | [1992,1997) | `after` | table cell |

**Known residual error:** the authorize locator `May` at 2232:2235 in 114-HR3803 is the month in `May 15`, not an authorization modal. The structural rule correctly finds no cell crossing but does not resolve word meaning. Preserve this diagnostic without post-result tuning; it illustrates why boundary checks cannot establish semantic quality. Table language concerns proposed statutory budget timetables, not observed legislative scheduling. Other source-review judgments remain qualitative and provisional, not certified effect labels.

## Validation and independent review

- **566 tests passed in 81.463 seconds** in the full suite; [raw log](../../../data/research-runs/structural-extractor-v1-20261108/full-tests.log).
- **14 focused methods passed normally and optimized**. The complete optimized runner replay reproduced the same result seal. No observed test/run failure or post-result correction occurred in this batch.
- Independent verifier checked all 40 outputs, 2,722 decisions, 501 effect-overlap rows, 12 categories and 257 registered file hashes without invoking the extractor or runner metric function. All agreed. It uses previously authenticated sidecar positions; it does not supply a new XML parser.
- All 17 predeclared associated cases received contextual review; zero sampling shortfall, zero actual crossing cases to review. No whole-corpus semantic accuracy estimate was attempted. The three near-fraction hits do not overlap fraction characters themselves.
- Review also documents committee-name `Appropriations` at 2330:2344, timetable references to appropriation bills at 2368:2381 and 2429:2442, and header `before` at 1772:1778 in 114-HR3803. These require semantic/row interpretation; structural retention is not effect approval.
- [Complete independent review and every source rationale](../../research/reviews/20261108-structural-extractor-review.md); [sealed evidence](../../../data/research-runs/structural-extractor-v1-20261108/independent-review.json): `4649080a66b0037791175700f602991d910e8d69c1fb4daf704bd1036fca0e34`.
- Independent normal/optimized verifier outputs match. Verifier SHA-256: `dad6c146fc455cf27b75e47e9627fccfa0a521dfe714816c8d54ad62a91f9df4`.
- All 586 inventoried prior files and frozen-model audit unchanged. Shared research lease released.
- [Validation](../../../data/research-runs/structural-extractor-v1-20261108/validation.json): `2af2af0de6455b251fd0d717c23d37fa806ee384eeec1461ae80ef26c6e4cc28`.
- Preservation before: `c388dabbf00cd07b36ed444b513e45880a14ba7da36e4983e9a68e9106d6f023`; after: `a3a7b8e63050eab576c895922e6de6ec26da7ef3ba0be0af02e2a596cb6d317a`.

| Focused suite | Method, passed in both modes |
|---|---|
| test_mechanism_structural_extractor_v1.py | `test_cross_cell_actual_match_preserved_and_flagged` |
| test_mechanism_structural_extractor_v1.py | `test_same_cell_endpoint_touch_retains` |
| test_mechanism_structural_extractor_v1.py | `test_nested_cell_boundary_is_not_masked_by_outer` |
| test_mechanism_structural_extractor_v1.py | `test_empty_and_orphan_cells_conservatively_flag` |
| test_mechanism_structural_extractor_v1.py | `test_unicode_fraction_context_unchanged` |
| test_mechanism_structural_extractor_v1.py | `test_forged_binding_and_projections_rejected` |
| test_mechanism_structural_extractor_v1.py | `test_non_table_context_baseline_exact_and_all_retained` |
| test_mechanism_structural_independent.py | `test_nested_outer_containment_does_not_mask_inner_crossing` |
| test_mechanism_structural_independent.py | `test_exact_half_open_touch_and_inside_cell_are_retained` |
| test_mechanism_structural_independent.py | `test_empty_and_orphan_cells_are_conservative_barriers` |
| test_mechanism_structural_independent.py | `test_fraction_and_inline_nodes_preserve_ambiguous_unicode_context` |
| test_mechanism_structural_independent.py | `test_raw_v5_result_and_entire_inputs_unchanged` |
| test_mechanism_structural_independent.py | `test_metric_overlap_is_half_open_and_combines_prior_retention` |
| test_mechanism_structural_independent.py | `test_stale_view_source_and_structural_bindings_rejected` |

## Reproduction

```sh
python3 -m unittest tests.test_mechanism_structural_extractor_v1 tests.test_mechanism_structural_independent
python3 -O -m unittest tests.test_mechanism_structural_extractor_v1 tests.test_mechanism_structural_independent
python3 -m scripts.run_mechanism_structural_v1 --output data/research-runs/structural-extractor-v1-20261108
python3 -O -m scripts.run_mechanism_structural_v1 --output data/research-runs/structural-extractor-v1-20261108
python3 -m unittest discover -s tests
```

[Extractor](../../../scripts/mechanism_structural_extractor_v1.py), [runner](../../../scripts/run_mechanism_structural_v1.py), [implementation tests](../../../tests/test_mechanism_structural_extractor_v1.py), [independent tests](../../../tests/test_mechanism_structural_independent.py). Immutable persistence compares existing envelopes and does not overwrite results.

## Limits and next development decision

These forty bills and provisional references are repeatedly exposed. The real corpus has only one table, so zero observed crossings does not estimate robustness to all table layouts. Synthetic positive cases demonstrate the specific guard behavior, not predictive or semantic improvement. Offsets are Unicode reading-view positions, never raw XML byte offsets. Full context is retained as an input but this deterministic consumer does not learn legal meaning from it. API checks establish internal consistency; the runner additionally requires canonical source validation.

No quality, source-history, family, time, numerical or original human-review gate is waived. Independent agent review is not human certification. No 60% predictive claim is supported.

Close this locator iteration without automatic expansion. The [critical-path plan](../../research/20261108-model-experiment-critical-path.md) prioritizes a finite historical-evidence feasibility decision, one eligible feature block and matched train/calibration/evaluation populations before a fixed predictive contrast. Full text remains a distinct testable hypothesis, not something to discard after extracting categories.
