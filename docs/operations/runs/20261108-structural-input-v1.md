# Structural input v1 — registered design validation, 2026-11-08

## Outcome and question

All forty fixed design cases built successfully, without reference migration or changes to the frozen reading text. This tests structural fidelity, not legal interpretation or prediction accuracy.

Question: can a separately versioned input preserve parser-visible table/fraction structure, qualified attributes and exact existing view offsets? Baseline: frozen `block-boundaries-v2` text plus the prior coverage audit. New representation: `structural-input-v1`; no extraction/model rule changes.

## Frozen setup

The existing forty exposed design bills were used, eight from each Congress 113–117. No substitutions or post-registration tuning; zero failed cases. Protected quality texts were not opened. Raw sources and source-view envelopes were authenticated before registration. No acquisition, new outcome scoring, model fitting, forecast creation or predictive test occurred.

- Input envelope: `18ad3d6ca86b0656a8c427dad12337218c753f1ddebb29a360d2c15e8d669ca7`.
- Pilot envelope: `318eca5e2797e8d09c14f5d8efe66bbe69e556b05e3861c3ea3f9f3f52fd0c5a`.
- Prior coverage result: `9c82fc612cef6d480d6afcaa7c18e41431c9fbc806f885acd1aadff0b178b9c6`.
- Registration: `eb98b86390cfafde53c3806f9d47511b54848ee5ecdaded3e2226cb1f653b815`; 83 input files and 23 code/test/fixture files pinned.
- Result: `f3505ea7c8618d686c0401790130ad619c0c73a0812fca21e05a0559706c3bb0`.

[Registration](../../../data/research-runs/structural-input-v1-20261108/registration.json) and [full result](../../../data/research-runs/structural-input-v1-20261108/result.json) are ignored local runtime artifacts; their public hashes are recorded here.

## Representation and mapping contract

Every parsed element retains its original local path, expanded namespace name, parsed attributes, ordered child paths and start/end offsets. Full frozen text, every text/tail segment and inserted block separator are preserved. Source binding includes raw XML SHA-256/length, the sealed view identity, renderer identity and rendered-text SHA-256. Canonical validation recomputes the complete sidecar and rejects any field alteration.

Offsets are zero-based half-open Unicode code-point indices into the unchanged reading view. They are not XML byte offsets. Character references and XML newline normalization have already been applied. Original namespace prefix spelling/declaration placement, attribute lexical order, comments, processing instructions and external DTD defaults are not reconstructed. Exact original XML remains available through its authenticated raw asset.

Tables retain ordered rows and cells with nearest-table ownership and explicit orphan lists. Ordinals denote source order, not visual grid coordinates; CALS/HTML span attributes remain literal, uninterpreted attributes. Nested table descendants remain in parent cell text, while ownership lists isolate inner rows/cells. Fractions (`fraction` and `mfrac`) retain exact substrings, child topology, attributes and up to 32 code points of context on either side; no numeric normalization is performed.

## Exact measured results

| Measure | Baseline audit | New input |
|---|---:|---:|
| Bills successfully reconciled | 40/40 | 40/40 |
| Parsed elements | 8,331 inventoried | 8,331 structural nodes |
| Elements with attributes | 2,903 inventoried | 2,903 preserved |
| Attribute key/value pairs | Not previously aggregated | 3,726 preserved |
| Text/tail segments | 9,299 | 9,299 |
| Reading-view Unicode characters | 337,823 | 337,823 unchanged |
| Explicit table objects | 0 in frozen renderer | 1 |
| Explicit table row/cell objects | 0 in frozen renderer | 10 / 20 |
| Dedicated fraction objects | 0 in frozen renderer | 3 |

The prior audit already inventoried table/fraction nodes; the change adds an authenticated consumption format and explicit relationships, not newly discovered source content. Frozen renderer has 6,667 block spans; all 8,331 parsed nodes now have structural mappings, including the 1,664 nodes absent from those block spans. Source text accounting remains 324,489 parsed characters + 13,334 inserted newlines = 337,823. No semantic precision/recall or predictive loss was measured.

## Every bill

| Bill | Nodes | Attribute nodes / pairs | Tables / rows / cells | Fractions | Text segments | Characters | Output seal |
|---|---:|---:|---:|---:|---:|---:|---|
| 113-hr4429 | 53 | 25 / 32 | 0 / 0 / 0 | 0 | 88 | 1817 | `5d0d899bbc262611d73300033f3c6db6bca25e0add307ed519347c94ef20284b` |
| 113-s2088 | 132 | 45 / 59 | 0 / 0 / 0 | 0 | 226 | 6310 | `e0d19e9a28bdf4384dabb84fc4347593cc6398dc8526a07aee3473792250cfdf` |
| 113-hr1979 | 74 | 29 / 45 | 0 / 0 / 0 | 0 | 103 | 3621 | `2c9a3152ca08002a96bdbffec61ead96efb64555c464070856d49f157ce04159` |
| 113-s439 | 236 | 85 / 108 | 0 / 0 / 0 | 0 | 274 | 10066 | `3a205574fd24c93007ad4f95982c281de264e1ee170682b4a7c04762d6d78870` |
| 113-hr128 | 111 | 38 / 52 | 0 / 0 / 0 | 2 | 139 | 6134 | `32582d6c8a0c1cf062fac3beeb4f6698958bdbd87ac12ee6627bd145e2e711d5` |
| 113-s5 | 69 | 38 / 43 | 0 / 0 / 0 | 0 | 116 | 2539 | `635c4f63a251ba6178e8e3763bb9987dab10c097c4de80a428761b8aeceaa570` |
| 113-s848 | 47 | 16 / 22 | 0 / 0 / 0 | 0 | 72 | 1440 | `ddc18e522dce64df4833edac4d35cf4e6fbe3716c3b9bc6cd3dff3d6ea56225c` |
| 113-hr1257 | 93 | 31 / 42 | 0 / 0 / 0 | 0 | 121 | 4846 | `96d687cecfe9812305fabcc23495816f656599c76c869af6995b18aa25830f7c` |
| 114-s1259 | 232 | 73 / 79 | 0 / 0 / 0 | 0 | 247 | 8164 | `f3ed7effd34c7b50f8aae1f72f8186488d2f24643952052adbde89d5e0bebcc1` |
| 114-s375 | 111 | 51 / 57 | 0 / 0 / 0 | 0 | 132 | 2774 | `4f19701b83197432dc8aade1a0e1c6826e98289dd5569bd837d23a75eac52887` |
| 114-hr3803 | 247 | 106 / 223 | 1 / 10 / 20 | 0 | 294 | 8409 | `2422e54a12b181e6df2d927717a28ac5630b672c75b70db57f006095e7d0a2b0` |
| 114-s2940 | 68 | 25 / 38 | 0 / 0 / 0 | 0 | 79 | 2549 | `9fcd20eab3ef5ca5df5f4f851bc092b60c14446c1cfb728a7dfe61609afe96a9` |
| 114-hr2575 | 30 | 9 / 15 | 0 / 0 / 0 | 0 | 54 | 911 | `f34ff920281e31af9537189b19098ca003d333a65d4fa414258743bdabd3f0b0` |
| 114-hr5053 | 107 | 35 / 44 | 0 / 0 / 0 | 0 | 132 | 3560 | `9d33b58a96d0a372d8e82d586f420415ac17b0b64d2ea8feca7135cb288cc43f` |
| 114-s2769 | 58 | 21 / 26 | 0 / 0 / 0 | 0 | 87 | 2650 | `6c020a1ba82df5d4ec1cbca9a51fb747792c3a97696c0cacb09b83649f746966` |
| 114-s2388 | 178 | 63 / 82 | 0 / 0 / 0 | 0 | 188 | 7646 | `d2423428b36008686b0b26c7b91434604d70da388d2bc4fcb66c6311b2234dee` |
| 115-hr5527 | 203 | 73 / 95 | 0 / 0 / 0 | 0 | 226 | 8227 | `1012a88e42c97b2f6eb89195064cb91c14e68c6440da80a026ed5784c4a4e540` |
| 115-s1372 | 70 | 20 / 25 | 0 / 0 / 0 | 0 | 92 | 3111 | `cc40b4fb55a44aa3a28e7b3e53878152467c09af47c4f32ac17471380f4914db` |
| 115-s1809 | 529 | 170 / 208 | 0 / 0 / 0 | 0 | 569 | 22361 | `c148bfa7e079d3f1fac8e7045c8b50459d13e650ca0fee9406989c0a6a4dca82` |
| 115-hr1714 | 34 | 16 / 23 | 0 / 0 / 0 | 0 | 42 | 954 | `ad74b284f8a875079c284957784c337d690a79f92e5bde25f90a45c7212976fb` |
| 115-hr5589 | 86 | 30 / 36 | 0 / 0 / 0 | 0 | 106 | 2897 | `63f5923e5a23192bd11f6567f3e125cc09cb1b12f3567fe6f3f870ab6cd44bb4` |
| 115-s284 | 140 | 63 / 80 | 0 / 0 / 0 | 0 | 149 | 10424 | `04149ae61373c97fbe2402aa5a0e8eb498296c27658795d1a17de26322a00b37` |
| 115-hr2259 | 407 | 175 / 231 | 0 / 0 / 0 | 0 | 470 | 17763 | `87e05fb473fa9d7a066b32ccc1d4b0a7c6dcefd256e138a6e85b5fcf0a0ae261` |
| 115-s1657 | 1033 | 306 / 359 | 0 / 0 / 0 | 0 | 1200 | 36949 | `d5e49164f128b1a91f6aaefc7e23aa438ec827abda3ae538db5d1d6905ca5510` |
| 116-hr2943 | 27 | 13 / 19 | 0 / 0 / 0 | 0 | 34 | 838 | `2b31f11745acf9eae77d3b0f03a22ed0ec69c5d0aee5cb18a4690918ee318505` |
| 116-hr846 | 177 | 77 / 108 | 0 / 0 / 0 | 0 | 205 | 6533 | `0f2edd02aba60a9b0cd10ec2ba6ea272bc495241b597da360f60ce8a13ffc5d0` |
| 116-hr7433 | 98 | 40 / 52 | 0 / 0 / 0 | 0 | 83 | 2961 | `74f500f7b01fb52b9067356ad229d2d32c4d72e021773b41afb2bb7a8bc5ea8d` |
| 116-hr3024 | 62 | 24 / 33 | 0 / 0 / 0 | 0 | 79 | 1460 | `3eb02235abcd0889785b8efa7fbc0eec69bd37b87d385531cd04872b60bbd6da` |
| 116-hr3777 | 282 | 90 / 97 | 0 / 0 / 0 | 0 | 306 | 14345 | `09bc3d5087148cee0a619897548ebbf8616afaf7741bb62865576364ceab9c1b` |
| 116-s1076 | 351 | 109 / 121 | 0 / 0 / 0 | 0 | 273 | 13461 | `f8c1b6cc3399e014b8e3122c7b8088d62313bc579c025bea001bc5b28551deb3` |
| 116-s2089 | 70 | 25 / 28 | 0 / 0 / 0 | 0 | 91 | 2016 | `1b3269705194749afbc1df624eaa439ecdbddebadf9f543bfd2ea50a0129730a` |
| 116-s856 | 107 | 35 / 56 | 0 / 0 / 0 | 0 | 95 | 4433 | `eb3f2cc378f8fb5f3b8a5ad47de986d7ada2e3804f8f014df7bc06574e4fcc53` |
| 117-s4377 | 36 | 12 / 21 | 0 / 0 / 0 | 0 | 40 | 1175 | `8ff305fd50121f504c0841655fd490cecbf7c68a695d75f86bdf61bab50b7a6a` |
| 117-s1230 | 132 | 51 / 67 | 0 / 0 / 0 | 0 | 133 | 4029 | `23052472379d04bd71bfee9bc3080b85417d39a8a1e7e8a712da7b9b9d4f7c0e` |
| 117-hr1662 | 126 | 59 / 77 | 0 / 0 / 0 | 0 | 116 | 4557 | `6d56a38959def324341b08fa97795d54494e1b2dcdc85dc555f260beb0ba6fec` |
| 117-s825 | 397 | 121 / 126 | 0 / 0 / 0 | 0 | 297 | 14959 | `bc7a18bc8be0c97f8f47b4e742696acc9fa506cd8baa1a459bb87fb31d7bec44` |
| 117-hr2448 | 71 | 37 / 50 | 0 / 0 / 0 | 0 | 64 | 3667 | `98282c9a45a2ee2f5488da38e1b8f2289e681c3f99633f26422cd222cb1a4e3d` |
| 117-hr6835 | 69 | 36 / 45 | 0 / 0 / 0 | 0 | 79 | 2689 | `3b6e3f2025c8ffa665d35eb5237aa94e602aedd3ead2057ce5aa12a6d89ba328` |
| 117-hr1597 | 1662 | 520 / 674 | 0 / 0 / 0 | 1 | 1935 | 69097 | `0e1f6adec94edfc49829ce4e1e3e5f1281a3563c6415448f33e228724e7ba14d` |
| 117-hr5229 | 316 | 111 / 128 | 0 / 0 / 0 | 0 | 263 | 15481 | `8c7e86c8874502763aa98990411a2c8fac3d28a9e924bf8027a87b2d67c0798d` |

All forty outputs reside at `data/research-runs/structural-input-v1-20261108/<bill_id>.json`. Each is sealed and named in the result.

## Actual table and fraction cases

114-HR3803 contains the one table. Each row has two explicit cells despite their ten within-row boundaries having no whitespace in the frozen text. The nine between-row gaps retain source whitespace. These are proposed statutory budget timetable provisions, not observed legislative events.

| Row | First cell [start,end) | Second cell [start,end) |
|---:|---|---|
| 1 | On or before: [1766,1779) | Action to be completed: [1779,1802) |
| 2 | First Monday in February [1811,1835) | President submits budget recommendations. [1835,1876) |
| 3 | February 15 [1885,1896) | Congressional Budget Office submits report to Budget Committees. [1896,1960) |
| 4 | Not later than 6 weeks after budget submission [1969,2015) | Committees submit views and estimates to Budget Committees. [2015,2074) |
| 5 | April 1 [2083,2090) | Budget Committees report joint resolution on the budget. [2090,2146) |
| 6 | April 15 [2155,2163) | Congress completes action on joint resolution on the budget. [2163,2223) |
| 7 | May 15 [2232,2238) | Appropriation bills may be considered in the House of Representatives. [2238,2308) |
| 8 | June 10 [2317,2324) | House Appropriations Committee reports last appropriation bill. [2324,2387) |
| 9 | June 30 [2396,2403) | House completes action on appropriation bills. [2403,2449) |
| 10 | October 1 [2458,2467) | Fiscal year begins. [2467,2486) |

| Bill | Fraction [start,end) | Exact surrounding context |
|---|---|---|
| 113-hr128 | `1/2` [3812,3815) | `ster shall allot more 				than 41/2 hours per week of free broadcas` |
| 113-hr128 | `1/2` [3971,3974) | `			this paragraph would exceed 41/2 hours, the time required 				to` |
| 117-hr1597 | `1/4` [54863,54866) | `ding the east 100 feet of the NW1/4 sec. 21, T. 23 S., R. 61 E., id` |

The two `1/2` nodes follow `4` in hours wording; `1/4` follows `NW` in a land description. These remain distinct structural inputs without guessing a numeric value.

## Validation and independent review

- Full suite: **552 tests passed in 78.230 seconds**; [raw log](../../../data/research-runs/structural-input-v1-20261108/full-tests.log).
- Focused tests: **17/17 passed normally and under optimized Python**. Complete registered runner replay under `-O` produced the identical result seal.
- Independent review reconstructed all forty raw XML trees without calling the builder/auditor: all nodes, ordered relationships, attributes, text/tail offsets, full text, table memberships and fraction contexts matched. No review sampling or case shortfall: 40/40 bills, 20/20 table cells and 3/3 fractions checked. No observed implementation/test/run failure or post-result correction in this batch.
- Reviewer authenticated all 83 input files, 23 code/test/fixture files and 40 output envelopes. It uses the same standard-library XML parser family; independence is in traversal/verification, not the parser itself.
- All **536 prior inventoried files** and frozen-model audit remained unchanged. Research lease released.
- [Independent review](../../research/reviews/20261108-structural-input-review.md); [sealed evidence](../../../data/research-runs/structural-input-v1-20261108/independent-review.json): `fe80b9071803af6428b3810c5ada68e11cdb3a2b7f92e5d016dcea4bb0127913`.
- [Validation](../../../data/research-runs/structural-input-v1-20261108/validation.json): `c75abfe1a0765205579c423322259ed4b3afb5675e18a977c7f44b9cd0376133`.
- Preservation before: `ddf4476d4c10b8d75792735bb843080e9d62c83b7773a17997c722c3fa90d959`; after: `ae2d58a0e657ae419180cd457c7f79e11f46b88c57617fa888393ccf0a0887be`.

Each focused test method passed in both modes:

| Suite | Method |
|---|---|
| test_bill_structural_input_v1.py | `test_tables_empty_cells_spans_and_nested_ownership` |
| test_bill_structural_input_v1.py | `test_unicode_entities_inline_tails_partition` |
| test_bill_structural_input_v1.py | `test_namespace_collisions_and_qualified_attributes` |
| test_bill_structural_input_v1.py | `test_fraction_context_not_numeric_normalization` |
| test_bill_structural_input_v1.py | `test_orphan_rows_cells_and_cells_without_row` |
| test_bill_structural_input_v1.py | `test_authentication_rejects_forgery_and_identity` |
| test_bill_structural_input_v1.py | `test_canonical_validation_detects_every_component_change` |
| test_bill_structural_input_v1.py | `test_external_doctype_offline_and_internal_subset_rejection` |
| test_bill_structural_input_independent.py | `test_nested_table_membership_does_not_duplicate_inner_cells` |
| test_bill_structural_input_independent.py | `test_empty_cells_and_merged_cell_attributes_are_literal` |
| test_bill_structural_input_independent.py | `test_orphans_not_attached_to_inapplicable_ancestor_row` |
| test_bill_structural_input_independent.py | `test_fraction_context_preserves_ambiguity_and_mathml_children` |
| test_bill_structural_input_independent.py | `test_namespace_attribute_collision_retains_qualified_names` |
| test_bill_structural_input_independent.py | `test_hash_binding_and_bill_identity_fail_closed` |
| test_bill_structural_input_independent.py | `test_canonical_validation_rejects_tampering_without_mutation` |
| test_bill_structural_input_independent.py | `test_build_is_deterministic_and_inputs_remain_unchanged` |
| test_bill_structural_input_independent.py | `test_external_doctype_cannot_trigger_network` |

[Builder](../../../scripts/bill_structural_input_v1.py), [runner](../../../scripts/run_bill_structural_input_v1.py), [builder tests](../../../tests/test_bill_structural_input_v1.py), [independent tests](../../../tests/test_bill_structural_input_independent.py). Exact code SHA-256 values are pinned in the linked registration.

## Reproduction

```sh
python3 -m unittest tests.test_bill_structural_input_v1 tests.test_bill_structural_input_independent
python3 -O -m unittest tests.test_bill_structural_input_v1 tests.test_bill_structural_input_independent
python3 -m scripts.run_bill_structural_input_v1 --output data/research-runs/structural-input-v1-20261108
python3 -O -m scripts.run_bill_structural_input_v1 --output data/research-runs/structural-input-v1-20261108
python3 -m unittest discover -s tests
```

Requires the exact locally held frozen inputs; public code alone cannot recreate private/ignored source custody. Immutable writes compare existing envelopes and do not overwrite a prior run.

## Remaining gates

These forty cases are repeatedly exposed design examples, not held-out validation. The tests cover specified parser/topology edges, not every possible XML or legal edge case. No inference of rendered visual layout, table header semantics, arithmetic meaning, document completeness or historical availability is certified. Independent AI review does not satisfy the original human-review protocol. Protected quality, family/cutoff/source-availability and training/calibration gates remain unchanged. No 60% predictive improvement claim follows.

Next: evaluate a separately registered consumer that uses table-cell and fraction boundaries while retaining full contextual text; assess it on design fixtures before any protected quality or predictive evaluation.
