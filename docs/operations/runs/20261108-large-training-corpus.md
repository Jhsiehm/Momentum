# Larger training-source corpus and readiness audit

November 8, 2026. The user authorized the next staged research step: broader dated training/calibration evidence before predictive testing. This is source preparation and readiness work, not model training or an extraction-quality evaluation.

## Fixed acquisition design

Registered 1,000 new bills before acquisition, up to 250 each from Congresses 113–116. Selection follows canonical bill-ID digest order within Congress and uses only identities, eligibility, dates and existing training roles. Exclude all 100 original pilot identities and families and all 200 previously selected identities and families. Preserve the exact legacy core/calibration/evaluation memberships and global family separation. No failure replacements, outcome-selected positives, adaptive quota changes or additional model trials.

The immutable registration is `e7cf38e5576d9dc385dae8a74b8d5a8d214e1e3a398539147775f06ab130fc43`. Runtime: `data/research-runs/mechanism-training-expansion-20261108-v1/` (ignored). All ten cycle manifests were sealed before downloading. Each cycle contains at most 100 cases and completes source replay and preservation checks before the next cycle, respecting the original protocol's per-cycle acquisition cap. Sequential requests retain real retrieval timestamps, retry policy and a six-hour run deadline; no scheduled-worker settings changed.

Before expansion, replayed the existing 232 distinct source identities, including current XML checksums, retained publication metadata and exact reading-view identities. This baseline includes 32 eligible design identities and 200 acquired source cases; it is not 232 labeled extractor examples. Current rendition bytes linked to dated official package metadata remain historically uncertified.

## Historical rendition evidence

An independent agent audited the first two previously selected cases per Congress: eight cases fixed before inspecting preservation metadata. All eight current XML files match their named PREMIS object's SHA-256, byte size and URL. However, all eight matching renditions were created in January 2023, after their historical cutoffs. Earlier XML objects have historical fixity events but omit the digest values needed to bind them to current bytes.

This establishes a concrete gap in available historical byte identity. It neither proves the legislative meaning changed nor certifies unchanged meaning. The existing false historical-eligibility flags remain correct. Root checked all 16 retained metadata files and all 16 quoted evidence spans. [Detailed source audit](../../research/reviews/20261108-historical-text-eligibility-audit.md); sealed audit `4f8db6a2506056554f9220a641e9ffc2264d01565335d3bf4022fb4dd4d0a178`.

Next source work must recover older object bytes/digests and dated public-access bindings, or adequate official transformation/version evidence. A current URL plus an old package date is insufficient. Eight cases are not a corpus-wide prevalence estimate.

## Extractor evaluation design

Prepared a [draft extractor evaluation contract](../../research/MECHANISM_EXTRACTOR_EVALUATION_DRAFT_V1.md), without opening the 50 protected quality texts. It preserves the frozen rubric and quality identities, distinguishes exact source matching from semantic correctness, requires full-document coverage and explicit abstention, and proposes one-to-one effect matching so multiple omitted duties cannot disappear behind a single present flag.

The corrected 501 effect records come from only 40 bills; the five largest bills contribute 206 records. Appropriation has two positive design bills; tax and repeal have four each. This supports rule development and fixtures, not a demonstrated generalizable learned extractor. The draft is not an implemented or registered extractor and grants no quality-access or model-release approval. It discloses incidental exposure to already-published aggregate historical outcome/model summaries while inspecting registration metadata; no individual outcome or quality text was used in its design.

## Independent software review

Read-only review found no selection, family-exclusion, cycle-cap or deadline-propagation defect. It did find that the registered replay verifier omitted some result/cycle-level reported counts and certification flags. Registered acquisition code was preserved; a separate supplemental verifier and adversarial tests address those claims without rewriting this run's implementation history. The missing checks do not themselves imply corrupted source records or incorrect actual counts.

## Completed expansion and class coverage

Acquired **1,000/1,000 new XMLs**, 250 per Congress, with **zero failures** and **16,052,288 source bytes**. All ten cycles completed. Distinct metadata-dated current-text coverage increased **232 → 1,232 bills** across the training/calibration union. These are source documents, not new annotations or historically certified model inputs.

Only after the result was sealed, root counted already-exposed labels on the unchanged memberships. No new scores, predictions, reselection or adaptive acquisition followed.

| Evaluation fold | Core covered before → after | Calibration covered before → after | Recorded positive core / calibration outcomes after |
| --- | ---: | ---: | ---: |
| 115 | 82 → 443 | 22 → 114 | 6 / 5 |
| 116 | 130 → 693 | 32 → 176 | 16 / 1 |
| 117 | 184 → 970 | 44 → 236 | 25 / 5 |

Every covered core/calibration partition now contains both recorded classes. This resolves the earlier zero-positive calibration issue, **not statistical adequacy or predictive readiness**. One calibration subset has only one positive outcome; counts across rolling folds overlap and must not be added as independent observations. Reviewed positive-family floors, source/label/family certification, validated extraction and a registered matched comparison remain unmet or unestablished. No model fitting, scoring, production promotion or 60% improvement claim.

The next priority is historical rendition evidence and a design-only extractor implementation under the draft contract. Preserve the protected quality partition until the implementation and reference-review process are frozen. Any future predictive study must treat these historical cases as exposed development material and separately register its comparison and evidence eligibility.

## Validation and final receipts

**36 focused tests passed**, covering expansion, supplemental claim rejection, post-acquisition class counts, earlier coverage and correction integrity. No shared engine code changed and no full-suite rerun is claimed. The built-in replay checked all 1,000 new and 232 baseline sources and all ten cycle receipts, with 1,375 frozen files unchanged. Root's separate preservation inventory confirms all **1,401 prior research files** and the frozen-model audit unchanged; these inventories overlap.

The supplemental verifier independently replayed all global/cycle counts, failures, source-byte totals, baseline identities and false eligibility/certification flags. Its result was identical in normal and optimized Python. It closes the reported result-claim gap without modifying the registered acquisition code. Source-audit evidence spans and extractor-draft category counts were also independently checked by root. Shared lease released; schedules unchanged.

| Artifact | Seal |
| --- | --- |
| Expansion result | `82448ebb873ad95ca72ef6972ecf8591b61e608feeb46a11084ebb6ebfe28528` |
| Registered offline replay | `e5f7080e055960ab0cd3c18fa87c392fdf56bab498833183bca5b9efa0b32d72` |
| Supplemental claims replay | `abc075ed6400ef2b74331c6e7c56249c7ac3083383a000a0acab04c6e0ba3db7` |
| Postselection class readiness | `7dbb008938ba46d4a53b28e9243c8f30d70354f21f2c959e237290db389ad309` |

[Detailed source acquisition receipt](20261108-mechanism-training-expansion.md). Retained runtime evidence stays ignored under data/. Reproduce the additional checks with:

```sh
python3 -m scripts.verify_training_expansion_claims data/research-runs/mechanism-training-expansion-20261108-v1
python3 -m scripts.training_source_class_readiness data/research-runs/mechanism-training-expansion-20261108-v1
```
