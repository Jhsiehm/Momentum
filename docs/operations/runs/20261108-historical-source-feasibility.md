# Historical-source feasibility and matched text specification — 2026-11-08

## Outcome

**All 16 requests succeeded, but no missing historical XML digest or matching historical object was recovered. Historical XML eligibility remains unresolved for all 8 cases.** The subsequently frozen E3 two-arm specification is blocked; no model fitting, outcome scoring or predictive test occurred.

## Question and frozen design

Can the same eight unresolved cases obtain a missing historical XML checksum/byte bridge through refreshed public PREMIS and package ZIPs? Cases remain the first two saved selection entries per Congress113–116 from the earlier 200-source run. This is a fixed feasibility subset, not a random corpus estimate. Original protocols, evidence, source statuses and protected quality remain unchanged.

Routes were chosen from official documentation before acquisition. Each case received exactly one GET for its retained PREMIS URL and one public package ZIP. The public ZIP pattern is documented by [GPO’s transition guide](https://github.com/usgpo/api/wiki/Transition-Guide). ZIPs describe distributed packages; internal archival objects are not thereby proven public. See [route review](../../research/reviews/20261108-historical-source-routes.md).

Budget: 8 cases, 16 requests, zero retries,zero followed redirects; 20,000,000 response bytes per request; 50,000,000 uncompressed bytes and 256 members per ZIP. Socket timeout 15 seconds; 30-second elapsed check between reads, not a hard 30-second deadline. No new request after 900 seconds from persisted acquisition start; an in-flight request can finish later. Interrupted intents prevent silent retries; failed/partial responses are preserved. No API keys, paid requests, messages or custodian contact.

Metadata and all archive members were hashed; PREMIS objects and DIP/METS metadata were parsed. Bill XML/PDF/HTML bodies were not rendered or used as model features. Archive files were read in memory rather than extracted to arbitrary paths. No extra bills or bulk acquisition occurred.

- Prior audit: `4f8db6a2506056554f9220a641e9ffc2264d01565335d3bf4022fb4dd4d0a178`.
- Registration: `6092a2a78fa2be4b33de987b0ca62479dff8dd038087ebbfff5b115d1fa32f81`; 17 input files and 8 code/test files frozen.
- Source result: `3f8c28344464b49319aa01d915caccca569a15b4e0404aed8a766ac08ea59076`.

[Registration](../../../data/research-runs/historical-source-feasibility-v1-20261108/registration.json), [source result](../../../data/research-runs/historical-source-feasibility-v1-20261108/result.json). Raw responses, request receipts, intent receipts, acquisition clock and per-bill inventories remain in ignored local runtime data.

## Exact results

| Measurement | Before | After |
|---|---:|---:|
| Cases with established historical XML eligibility | 0/8 | 0/8 |
| Cases with missing old-object checksum recovered | 0/8 | 0/8 |
| Cases with historical XML member matched to recovered digest | 0/8 | 0/8 |
| Current XML matching ZIP member | Not measured in this route | 8/8 |
| Successful HTTP responses | — | 16/16 |
| Successfully parsed routes | — | 16/16 |
| ZIP members inspected | — | 48 across 8 ZIPs |
| Runtime failures / replacement cases | — | 0 / 0 |

All 8 ZIPs contain six members: XML, HTML, PDF, MODS, PREMIS, DIP/METS. Their DIP manifests identify the expected package and enumerate distributed content; no historical digest bridge was recovered. The sixteen old XML object IDs still lack usable checksum values in refreshed metadata. An old checksum-calculation event without its checksum value cannot authenticate the current bytes. These results do not establish that legislative wording changed, or that historical objects cannot exist elsewhere.

## Every case

| Bill | Cutoff | Old XML object IDs | Current XML matches ZIP | New old digest / old-byte match | Disposition |
|---|---|---|---:|---|
| 113-hr3884 | 2014-07-14T23:59:59Z | `D09002ee186e098b4`, `D09002ee186e0b015` | True | 0 / 0 | Unresolved |
| 113-hr4267 | 2014-09-10T23:59:59Z | `D09002ee187ff44ba`, `D09002ee188028f4f` | True | 0 / 0 | Unresolved |
| 114-hr2776 | 2015-12-12T23:59:59Z | `D09002ee18cb21906`, `D09002ee18cb2247d` | True | 0 / 0 | Unresolved |
| 114-hr2447 | 2015-11-15T23:59:59Z | `D09002ee18c7db45c`, `D09002ee18c7dd2e7` | True | 0 / 0 | Unresolved |
| 115-hr4997 | 2018-08-12T23:59:59Z | `D09002ee1987f3892`, `D09002ee1987f47e3` | True | 0 / 0 | Unresolved |
| 115-s2712 | 2018-10-16T23:59:59Z | `D09002ee19a242cd1`, `D09002ee19a244023` | True | 0 / 0 | Unresolved |
| 116-s2862 | 2020-05-12T23:59:59Z | `D09002ee1a3cbb1d5`, `D09002ee1a3cbb595` | True | 0 / 0 | Unresolved |
| 116-s843 | 2019-09-10T23:59:59Z | `D09002ee1a03cf96e`, `D09002ee1a03d0a0f` | True | 0 / 0 | Unresolved |

## Every request

| Index | Bill | Route | HTTP | Bytes | Body SHA-256 | Receipt seal |
|---:|---|---|---:|---:|---|---|
| 00 | 113-hr3884 | premis | 200 | 368048 | `95dd180b17965907ab2dee3e42e5a5a9e0019959b4d0b620b516b5f1cad2b956` | `5361568d19cfb31630e932d15af80cf3e0408cb5564aa17aa49288f44c7e9a07` |
| 01 | 113-hr3884 | zip | 200 | 235301 | `616e5cd730f818c111d962ba2b474951ceb01cccba07c25dfefbb5761d659642` | `e6094801feb5c69e73bb80423dd53909cf275ff01d44396992e9770b7f256f98` |
| 02 | 113-hr4267 | premis | 200 | 392723 | `108d2ed2740d78706ed80781f59eaa95d29a552518b15bfa12a40c93ac5ef9e6` | `87177d334a18685cc28185d9f1198cef507e433ec0cb56872e0b39cf42340efe` |
| 03 | 113-hr4267 | zip | 200 | 225947 | `e479917a7d7c20c168189659938d9015a80766e7a93be2f144ac16c38b4941f5` | `c70b5a0a9d564e611862bce1213c693abc29971bd11622fbfd411b0ad0edf3b8` |
| 04 | 114-hr2776 | premis | 200 | 359499 | `6389613d596f9d19ddc1a6de33d1924c98886609028b31f0f8a866f748f0f227` | `2110a07a402eee472ff71116a11dbea3699c53019cde7c02158a28adeb406c73` |
| 05 | 114-hr2776 | zip | 200 | 224610 | `c81c5c86c48bcd6e31efe0cfcae37665a0c0d963cdf2ccfb8d1039a9d20ced5c` | `90101bb04031b3ad3c87f7d929603b6411d284ef82afaee405e4b5ca9c10df73` |
| 06 | 114-hr2447 | premis | 200 | 359499 | `88a313e845ccc880c054b98ea8ae932b76840a31fe65f4a229eceb1b22a46e3f` | `fe00e73d81992b11f78de402a54ab2681d7535ba38448ec2679443bae1942107` |
| 07 | 114-hr2447 | zip | 200 | 230911 | `005cab831b0b82cccce5a104d8a41456796fa7b06bcd15c0485a844db939af64` | `9fbd87679d4be81ec471de3ca234c321861ac95000ab1700353537ea9e10f8ca` |
| 08 | 115-hr4997 | premis | 200 | 304162 | `c24883265dfbf527183341ada42adfa86a9e40c4fc78cb7df32f17058e8ce819` | `7edd14ac1a8b894bd868fad40e4956728068a894d368c06281a475c649f1cacb` |
| 09 | 115-hr4997 | zip | 200 | 424238 | `3b1272025d0a19ed0b396fe0299ae3a72531a53dd081205e8c06fe15ee90fdc8` | `1ceea9655ec0619aa44a00c373295bcf0b4c521d3c92ccef4398afd49ee44653` |
| 10 | 115-s2712 | premis | 200 | 327092 | `c97c974ae2a2f2c68ae13c5ebda8c349e445b7439d5faf92a99ff2f8fafb0f9f` | `cd7209202345237f80fd29ef910e42457bc38cc32077b190d44674e83a906dc0` |
| 11 | 115-s2712 | zip | 200 | 239740 | `c2cc8ef9dc6f6df0552b87ee852cb83a8c8284a22c94e01f62d368fff14756bb` | `59aa2bce78bb87f8fa5d1ce9e0a8bc1fa2c415140881a02358c3affedeed7a07` |
| 12 | 116-s2862 | premis | 200 | 257349 | `0bce49e8aab4be748e1d60f2d3e1e668c1c5dd98c24d3c89942ee8b74ed668f5` | `9c539e6611d54a9bc1fadba4ea152c0c5af53218a3f28bfb817febb4f353df47` |
| 13 | 116-s2862 | zip | 200 | 226682 | `9f6f88651c5c7f06918a77718d75851db0cef5f0647b26fa4c499243465bc5a2` | `49ceb9d89df9a219c4ab6fe90850d36e62f3cda3f8014a287f216f358b96a6c0` |
| 14 | 116-s843 | premis | 200 | 272940 | `e70a1e4c196b88f2546dd3f95b104478022452737aaf931210d37981e996b419` | `84205199feab026ceec04ebb21107d207fa8d94c423c8e3a657547d74b27f9fb` |
| 15 | 116-s843 | zip | 200 | 225555 | `895d3d31b0132b58cf00063b89cdb1018dae83200afcf47bb670dad80fcfddcb` | `1180a58e09d6e4b5eb769464d2cdf3b23038ef8854a5e2ce7bbe0999c847cdb6` |

Total retained response bytes: **{total:,}**. Every URL, request/completion timestamp and selected HTTP header is in its immutable request receipt. HTTP headers are transport metadata, not historical-publication proof.

## Conditional predictive specification

E3 was selected on readiness and the user’s full-language hypothesis, before new scores. E2 descriptor quality is not certified, so a descriptor arm is excluded. This is a frozen **specification and candidate-identity snapshot**, not a frozen eligible execution population. Ten gates remain explicitly unsatisfied/unknown; eligible memberships and counts are null. The tool has no fitting path and cannot promote evidence.

Arms: six-feature structured anchor through sparse solver, versus the same anchor plus introduced text; two arms × three folds = six conditional predictive fits. Calibration fitting is separate and disclosed; neither model nor calibration was fitted in this batch.

| Evaluation fold | Planned core IDs | Planned calibration IDs | Planned evaluation IDs | Eligible rows |
|---|---:|---:|---:|---|
| 115 | 3569 | 893 | 2717 | Unknown |
| 116 | 5272 | 1319 | 2792 | Unknown |
| 117 | 7049 | 1763 | 3059 | Unknown |

Candidate memberships copy the sealed calendar registration’s identity lists only, with duplicate/partition/Congress checks. No outcome files were loaded. Both arms must use the same later-certified eligible population and record every exclusion before scores.

Original E3 settings retained: lowercased TF-IDF unigrams/bigrams, min_df=5, max_df=0.95, max_features=10,000, L2 row normalization; no stemming/generic stopwords; retain negation. Vocabulary/IDF and structured scaling fit on core only; structured scale floor 0.1. Mean negative-log-likelihood with slope L2=.05, unpenalized intercept; deterministic sparse L-BFGS, 20,000 iteration cap, max-gradient threshold 1e-6; no search. Existing monotone affine-logit calibration 2,000 steps on separate earlier calibration families; report historical-rate and stage baselines. Every required fold must improve calibrated Brier without worsening log loss; a blocked fold blocks lead selection. Overall programme cap 75 and six-hour block budget remain.

Exact normalization/tokenization/masking, dependency versions and sparse numerical implementation still need a pre-fit freeze and verification. Structure stays available as context, not a third predictive feature arm. Source/history, qualified review, positive-family scope, time/family eligibility, matched memberships, classes, preprocessing, numerical checks, runtime and execution-registration gates remain unresolved. The previous calendar exception is not inherited.

- [Frozen specification](../../research/MATCHED_TEXT_COMPARISON_V1.md).
- [Specification registration](../../../data/research-runs/matched-text-comparison-v1-20261108/registration.json): `6fcf636b2fa7801d6c6098ac54a82f5ee611ef56a5d4a447c690b8b9461e385a`.
- [Blocked preflight result](../../../data/research-runs/matched-text-comparison-v1-20261108/result.json): `ea4b02a6a02853f9c07edb5844dd7608e63587074f176ad51faef5c434e6e2af`.

## Validation, failures and independent review

- Full suite: **592 tests passed in 82.628 seconds**; [raw log](../../../data/research-runs/historical-source-feasibility-v1-20261108/full-tests.log). All 26 focused tests passed normally and optimized.
- An initial independent test run passed 10/11: UTF-16 XML bypassed the initial byte-string DTD/entity guard. Rejected null-containing/UTF-16 metadata before registration. Code review also corrected partial-response preservation, interrupted-request retry risk, resumed study-clock reset, weak package substring matching, blank object IDs and ambiguous fixity children before acquisition.
- Registered acquisition had zero HTTP/parse failures and no substitutions. Optimized replay with `fetch` mocked to raise on any network call reproduced the same source result offline.
- Independent verification checked 16 receipts, 4,674,296 bytes, 48 archive members with sizes and three hashes, manifest inventories, all 16 old IDs, all 8 dispositions,registered source/code bindings and exact planned memberships. Normal/optimized verification agreed. It uses the same XML/ZIP parser families, not an independent parser implementation.
- [Independent review](../../research/reviews/20261108-source-feasibility-review.md); [sealed evidence](../../../data/research-runs/historical-source-feasibility-v1-20261108/independent-review.json): `e7a9a744b634d2d6b8be79357f1c1bce9c3ffcae367f6107b2c1dff53c467ab1`.
- All 637 prior inventoried files and frozen-model audit unchanged. Shared lease released. [Validation](../../../data/research-runs/historical-source-feasibility-v1-20261108/validation.json): `4a0a73168a103e6a9e336ca3e3bcac75a1b9cad3841731076b999ca8fae3f8f3`.
- Preservation before: `e018f1ee8a050796075780fc63c930b5bff9cd30dc8df0df20e1239679266eae`; after: `a21764cbf3b859055ba49e9b0ea93e2b6faff64077a9ce57f073074affbae295`.

| Focused suite | Method: passed in normal and optimized Python |
|---|---|
| test_historical_source_feasibility_v1.py | `test_old_missing_digest_not_filled_by_current_object` |
| test_historical_source_feasibility_v1.py | `test_matching_old_bytes_still_need_public_access_chain` |
| test_historical_source_feasibility_v1.py | `test_invalid_digest_is_not_recovered_bytes` |
| test_historical_source_feasibility_v1.py | `test_xml_entities_and_wrong_root_rejected` |
| test_historical_source_feasibility_v1.py | `test_zip_inventory_without_extraction` |
| test_historical_source_feasibility_v1.py | `test_zip_traversal_and_substring_identity_rejected` |
| test_historical_source_feasibility_v1.py | `test_partial_error_body_retained` |
| test_historical_source_feasibility_independent.py | `test_utf16_entity_not_accepted` |
| test_historical_source_feasibility_independent.py | `test_duplicate_objects_rejected` |
| test_historical_source_feasibility_independent.py | `test_missing_object_id_rejected` |
| test_historical_source_feasibility_independent.py | `test_digest_and_size_remain_untrusted_strings` |
| test_historical_source_feasibility_independent.py | `test_matching_old_digest_does_not_establish_access` |
| test_historical_source_feasibility_independent.py | `test_other_object_digest_is_not_old_object_evidence` |
| test_historical_source_feasibility_independent.py | `test_ancient_date_cannot_upgrade_current_bytes` |
| test_historical_source_feasibility_independent.py | `test_traversal_never_extracted` |
| test_historical_source_feasibility_independent.py | `test_zip_member_limit` |
| test_historical_source_feasibility_independent.py | `test_missing_package_identity` |
| test_historical_source_feasibility_independent.py | `test_malformed_xml_error_normalized` |
| test_matched_text_comparison_v1.py | `test_blocked_and_no_outcomes_or_label_counts` |
| test_matched_text_comparison_v1.py | `test_fixed_six_fits_and_original_parameters` |
| test_matched_text_comparison_v1.py | `test_identity_snapshot_deterministic_and_nonmutating` |
| test_matched_text_comparison_v1.py | `test_extra_top_level_outcomes_never_copied` |
| test_matched_text_comparison_v1.py | `test_duplicate_and_role_overlap_rejected` |
| test_matched_text_comparison_v1.py | `test_missing_fold_empty_role_and_extra_fields_rejected` |
| test_matched_text_comparison_v1.py | `test_future_training_wrong_evaluation_and_bad_id_rejected` |
| test_matched_text_comparison_v1.py | `test_protected_output_path_rejected` |

## Separately disclosed post-result exploration

After the registered negative result, an agent inspected the already-retained PDF/HTML member metadata as possible alternate source leads. This was not a preregistered endpoint and did not change the primary result. All 16 PDF/HTML member hashes match their current PREMIS objects, but their checksum/rendition-creation events are also January 2023, after cutoff; all 8 PDF signature-assignment events are 2023. Older source-rendition IDs provide retrieval leads, not certified bytes/public access. No new requests, text extraction or fits occurred.

[Every alternative object, hash and event date](../../research/reviews/20261108-alternative-rendition-leads.md). Derived unsealed exploration artifact SHA-256: `aa075e85671c3264fdcda42b9f03b15d36b05dc75974a6278e6f1e7b50feecac`. Root independently checked all 16 member/object digest bindings. Its first ad hoc check used filenames relative to the wrong directory and failed with FileNotFoundError; correcting the base directory completed the check without changing any research input or result.

## Reproduction

```sh
python3 -m unittest tests.test_historical_source_feasibility_v1 tests.test_historical_source_feasibility_independent tests.test_matched_text_comparison_v1
python3 -O -m unittest tests.test_historical_source_feasibility_v1 tests.test_historical_source_feasibility_independent tests.test_matched_text_comparison_v1
python3 -m scripts.historical_source_feasibility_v1 --output data/research-runs/historical-source-feasibility-v1-20261108
python3 -m scripts.freeze_matched_text_comparison_v1 data/research-runs/matched-text-comparison-v1-20261108 --feasibility-result data/research-runs/historical-source-feasibility-v1-20261108/result.json
```

The source runner reuses sealed responses on replay; the original sixteen attempts are not repeated. The specification freezer deliberately refuses an existing output directory. Its exact original command is shown for provenance; inspect/unseal existing results or use a separately named preparation directory when reproducing. Do not retry failed routes or extend this study silently.

## Next dependency

Do not acquire thousands more current XMLs on the assumption that source volume solves historical evidence. The public routes tested here did not close the missing chain. A separate [historical-object evidence request packet](../../research/HISTORICAL_OBJECT_EVIDENCE_REQUEST_V1.md) identifies exactly what a custodian would need to provide. It is a local preparation artifact; no message was sent. Prospective source capture is an alternative route with a future evaluation clock, not a way to backdate this experiment.

No semantic or predictive performance was measured. The 60% relative Brier target remains untested. This run closes a specific feasibility question and preserves a concrete blocked comparison; it does not certify every possible source route or every edge case.
