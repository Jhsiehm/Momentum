# Design-only mechanism candidate extraction

Date: 2026-11-08. Scope: implement and execute a source-local annotation assistant on the corrected forty design bills, test graph-conditional effect evaluation, and investigate historical source access. No predictive experiment or quality evaluation occurred.

## Executed result

The deterministic extractor scanned all 337,823 supplied characters across forty preserved boundary-aware views. It emitted 706 section-context candidates containing 2,654 exact lexical trigger locations and five narrow, unvalidated suggestions. All 480 bill–mechanism assessments abstain. Accepted labels: zero. The extractor is a rule-based review aid, not a trained model or a semantic certification system.

Full section context stays attached to each hit. Conditional language, deletion instructions, quoted blocks, findings and dependent lists suppress narrow suggestions or carry review warnings. Rendering does not retain every inline XML semantic distinction; retained text and sections do not prove legal interpretation. Lexical silence never becomes an absent label.

A design-only locator diagnostic found same-mechanism trigger intersection with 399 of 501 provisional reference effect quotations. The remaining 102 quotations had no such trigger intersection. This is **not semantic recall, precision or accuracy**: a trigger may be incidental or negated, quotations can cover multiple effects, and candidate context can be much broader than the relevant effect. No matching graph was inferred from these intersections.

| Mechanism | Reference effects | Effects with trigger intersection |
|---|---:|---:|
| Create programme | 28 | 14 |
| Authorize | 97 | 81 |
| Appropriate | 5 | 4 |
| Tax | 7 | 3 |
| Prohibit | 56 | 28 |
| Require | 127 | 122 |
| Amend | 34 | 33 |
| Repeal | 6 | 6 |
| Rename/designate | 18 | 10 |
| Reporting | 54 | 42 |
| Deadline | 60 | 50 |
| Sunset | 9 | 6 |

## Evaluation machinery and independent review

The separate evaluator accepts sealed predictions, reference effects and an externally adjudicated compatibility graph. It computes maximum-cardinality one-to-one matches with deterministic lexical tie-breaking. Duplicate predictions remain false positives and omitted reference effects remain false negatives. Reference-uncertain statuses are excluded from status metrics; predicted uncertainty on a positive reference counts as a false negative. Graph incompleteness can bias results. Evidence coordinates are structurally checked, but the evaluator does not authenticate source content or certify semantic compatibility.

Agent A independently audited the extractor and evaluator. Review exposed present statuses without effects, missing dimension constraints and cross-mechanism graph edges. The owner added rejection checks and tests. Deadline suggestions now use duration; the tax rule was narrowed to avoid assuming replacement of a prior rate. The methods agent reviewed the root runner's quality firewall and source bindings; root added end-of-run code-hash verification as recommended.

The evaluator was tested on synthetic fixtures only, including exhaustive comparison of all 512 possible three-by-three bipartite graphs against a maximum-cardinality/tie-break oracle. No semantic score was computed on real bills.

## Boundaries, reproduction and receipts

The runner checks corrected population equality, original design membership and disjointness from quality IDs before loading individual views. It authenticates each view against original inputs and corrected references, records code/input hashes before extraction, validates quotation offsets and tests deterministic extraction. Existing files cannot be overwritten with different output. Original acquisition and rendering code were unchanged.

```sh
python3 -m scripts.run_mechanism_design_extractor --output data/research-runs/mechanism-extractor-design-20261108-v1
python3 -O -m scripts.run_mechanism_design_extractor --output data/research-runs/mechanism-extractor-design-20261108-v1
python3 -m unittest tests.test_mechanism_design_extractor tests.test_mechanism_design_runner tests.test_mechanism_effect_evaluation tests.test_bill_context_design_text_v2 tests.test_mechanism_corrections tests.test_mechanism_rubric_v2
```

Runtime outputs remain ignored under `data/research-runs/mechanism-extractor-design-20261108-v1/`. Registration: `f8e9391905dbb0a8eb01af695f76c108edf1a591f3a0ed164316b97aca66f8a2`. Result: `0d350fd1bace59d990908268e71560a3dec87ba2f4df74a8e29eada728508bd8`. Normal and optimized replay agree. The focused suite passed 36 tests; no full-suite result is claimed.

The [historical access investigation](../../research/reviews/20261108-historical-text-resolution.md) made eight official documentation page requests and resolved zero of eight historical identities. It identifies documented API and architecture routes for further investigation without treating current retrieval, lineage or publication dates as historical byte identity.

Quality texts were not opened or parsed; no models were fitted, outcomes scored, schedules changed or releases promoted. Frozen-model audit and prior evidence preservation are checked separately in `data/research-runs/mechanism-extractor-preservation-20261108-v1/`. The preservation replay verified all 265,400 inventoried prior files unchanged and an identical frozen-model audit; receipt hash `e99573af0fdc239561e844a396996b8f4bc7f424a831a7b386ae930274bec949`. Hashing preserved files does not parse their texts. A shared research lease covered the run and was released. Independent agent replay reproduced the result hash and checked all forty views and every candidate, trigger and suggestion span.

## Next executable work

Review candidate misses and suggestions on design cases in a separately versioned layer; establish complete semantic reference judgments and a genuine externally reviewed compatibility graph before effect scoring. Expand design examples for sparse mechanism/direction combinations. Freeze implementation and quality protocol before protected evaluation, retaining original reference-review gates. Continue bounded archival retrieval research to bind historical bytes and public availability. None of these engineering results establish the requested 60% predictive improvement or autonomous self-learning.
