# Expanded candidate rules against fixed corrected references

Date: 2026-11-08. Tested 33 separately versioned lexical rule families on all forty design bills against the same corrected v3 reference used for the structural-context baseline. No reference edits or post-result rule tuning occurred. This is exploratory design evaluation, not held-out semantic or predictive validation.

## Result

Same-mechanism trigger intersection increased from **401 to 449 of 501 reference effect quotations**. Forty-eight previously unlocated quotations acquired a trigger intersection; none lost one. Fifty-two quotations still have no intersection. These numbers measure source location, not whether the proposed legal interpretation is correct.

| Mechanism | Effects | Baseline intersections | Expanded intersections | Recovered |
| --- | ---: | ---: | ---: | ---: |
| Create programme | 28 | 14 | 15 | 1 |
| Authorize | 97 | 81 | 89 | 8 |
| Appropriate | 5 | 4 | 4 | 0 |
| Tax | 7 | 3 | 3 | 0 |
| Prohibit | 56 | 28 | 49 | 21 |
| Require | 127 | 123 | 123 | 0 |
| Amend | 34 | 33 | 33 | 0 |
| Repeal | 6 | 6 | 6 | 0 |
| Rename/designate | 18 | 10 | 13 | 3 |
| Reporting | 54 | 42 | 50 | 8 |
| Deadline | 60 | 51 | 58 | 7 |
| Sunset | 9 | 6 | 6 | 0 |
| **Total** | **501** | **401** | **449** | **48** |

The expansion adds **73 unique mechanism/offset hits and 19 candidate groups**. Total candidates increase 706→725; hits increase 2,654→2,727. These additions create review work even when they do not recover a reference quotation. Twenty-one added hits do not intersect any same-mechanism reference quotation; they are not labeled false positives because the provisional reference quotations are neither exhaustive nor proof of incompatibility. All 480 mechanism decisions remain abstentions, the original five narrow suggestions remain unchanged, and no accepted effects are generated.

## What was tested

The rule manifest in `scripts/mechanism_design_extractor_v3.py` is derived from the prior design review's vocabulary-gap diagnoses. It covers bounded variants of actor-specific prohibitions, conditional permission limits, explicit rights/options, information filing/provision, recurring action timing and selected designation/programme phrases. It contains no bill IDs, outcomes or quality-case language. It does not claim to resolve implicit legal effects or unavailable prior law.

The new extractor wraps immutable v2 and preserves every original candidate field and hit structure; duplicate exact hits merge rule provenance. New hits receive the same source-hierarchy context relations, with exact character offsets and full section context. The structural attachment helper is locally reproduced because the frozen v2 module has no reusable attachment entry point; dependency hashes bind those source versions. No global monkeypatching or mutable shared extraction state is used.

A separate agent authored synthetic contrast fixtures before the forty-bill run. They distinguish annual reports from annual salary, filing documents from file cabinets, information provision from furnishing furniture, and constrained permissions from ordinary “only” wording. Misleading findings, negated instructions and struck/quoted text may still be retrieved, but never become accepted effects. These fixtures are design challenges informed by the same error analysis, not an independent test set.

Methods review inspected all 33 rules before the run. Root strengthened invariants to preserve candidate identity/context and old hit fields, require correct expanded candidate counts and explicit non-trained status. The implementation, runner, test fixtures, input hashes, fixed reference and deterministic review-sampling rule were sealed before extraction. No forty-bill metrics were used to revise rules afterward.

## Fixed source-context review

Before extraction, the runner fixed a sample of up to 24 added unique mechanism/offset hits, ordered by SHA-256 of compact JSON `[bill_id, mechanism, start, end]`. It selected 24 of the 73 additions. An agent who authored the separate contrast tests reviewed every sampled occurrence against its full candidate context and governing clauses; 21 unique contexts were inspected. This is a deterministic exploratory sample, not blinded reference annotation or a precision estimate.

The review classified 20 as supported locators and four as misleading contexts:

- `115-s1657`, offset 4228: the selected limitation is wording being struck, not the later operative occurrence.
- `115-s1809`, offset 13922: information provision describes an optional project feature, not a separate reporting duty.
- `117-s825`, offset 1894: “Authorities” is a heading, not an independent grant of power.
- `117-hr1662`, offset 604: the selected wording is in a purpose statement, outside operative sections.

“Supported locator” means useful for contextual review, not a correct effect prediction. The land-withdrawal rule also begins inside a map title in one sampled case; its retained full clause supplies the relevant action. That boundary behavior is recorded for later investigation, not repaired after seeing this run. These observations do not establish that the unsampled additions are correct or incorrect.

Sample hash: `62d76bf4be150707f37961a1fd3a0ccb8a10536080fe37c59c991e72f538d0ae`. Review: `e2189bd7ca958abf044fedc1777152d222ca300aa973e4cec55254a2d6ff21e2`. Root verified complete sample coverage, view bindings and all evidence offsets; integrity receipt: `8d1ca9c8b081e0fa90be5526a4f24bd8f589a711612f9affe9f8a2088f927ada`. No rules or reference labels were changed after this review.

## Validation and preserved evidence

Seventy focused tests passed, including all 33 rule-family synthetic positives, independent contrasts, source structure, baseline preservation, duplicate handling, concurrent determinism and runner arithmetic. An initial suite invocation occurred before the new owner test file existed and failed that import; after the file was complete, the full focused invocation passed. No full-repository suite result is claimed.

Normal and optimized runs reproduce result hash `e04abe0d2804f4e022a9885f5af76df4b4598ebdcd4897431b772cf41d8d0713`. An independent methods agent recomputed all forty comparisons, per-mechanism totals, sample selection and source/code bindings, then replayed the actual runner successfully. Its separate receipt is `880a4f4fd7aeb8c80a7f2eea0f7ac38bd9930e95388e2d8e4f586516bf9f5a4e`.

Registration: `3d70215f2acc3a62974bc0488a248d310d37cb402a0e06783938eb3a9013688a`. Fixed reference: `8d6da3e94e901c953334548d60617112fe8ea3408219d6e6d4b9d009a2805bd5`. Baseline result: `82c28b7f07e49b7f6ea963951cb8dc0139caf3b7f0e8ea6e26fc99aa93e1ba0e`. Ignored runtime directory: `data/research-runs/mechanism-expansion-v3-20261108/`.

```sh
python3 -m scripts.run_mechanism_expansion_v3 --output data/research-runs/mechanism-expansion-v3-20261108
python3 -O -m scripts.run_mechanism_expansion_v3 --output data/research-runs/mechanism-expansion-v3-20261108
python3 -m unittest tests.test_mechanism_design_extractor_v3 tests.test_mechanism_expansion_contrasts tests.test_mechanism_expansion_runner
```

All 151 inventoried prior source-view, reference, review and extractor files remained unchanged, as did the frozen-model audit. Preservation receipt: `3b1dbea28209bb506f5236d1d866fd82f6e6ac16d1af3c1bf528d8c461ddc3a1`. No protected quality text parsing, acquisition, outcome scoring, model fitting, promotion or schedule change occurred. The shared research lease was released.

## Interpretation

The result supports retaining this version as a better **design-set locator baseline**, with increased review burden and no established semantic accuracy. It does not demonstrate generalization, historical eligibility, autonomous learning or the requested predictive improvement. A next semantic experiment needs explicit effect predictions and a separately reviewed compatibility graph; source eligibility and original quality-reference gates remain in force.
