# Provisional reference v3 and structural-context extractor v2

Date: 2026-11-08. Executed the eight-question source adjudication and a separately versioned structural-context experiment on the same forty design bills. Original references, extractor code and outputs remain immutable. No quality evaluation or predictive fitting occurred.

## Eight adjudicated corrections

The primary agent reread all six relevant source views (131,586 characters) and the frozen mechanism rubric. A methods agent independently reviewed each decision against its operative clause and surrounding context: eight agree, no challenges, no unresolved decisions. This is agent adjudication of targeted design corrections, not human certification, blinded agreement or general reference accuracy.

Seven deadline effects change dimension from `procedure` to `duration`. The `117-hr1597:37` effect changes from `require/expand/duration` to `require/create/procedure`: the visible text imposes a conditional duty to extend a plan/permit, rather than establishing expansion of a preexisting duty. Four quotations expand to include governing context; the testing-waiver conditions are explicit. All forty bills, 501 effects and 480 mechanism statuses remain in place. Only the eight selected effects change; the parent reference is preserved.

The [decision report](../../research/reviews/20261108-reference-v3-adjudication.md) explains every correction. New provisional dataset: `data/research-runs/mechanism-reference-v3-20261108/corrected-dataset.json`, hash `8d6da3e94e901c953334548d60617112fe8ea3408219d6e6d4b9d009a2805bd5`. It binds primary adjudication `1f2d212154b7e651dd00c985fbce6868b5d06b887b1dccc3a0d7cf2ae7e8b1c0` and peer review `ea6234e64ec8b162712eb5b6b041604d7c5aa377c24c208cc874a4a2537c3219`. Export blocks unresolved or challenged decisions and preserves false certification flags.

## Structural-context experiment

The new extractor wraps the frozen v1 implementation. It adds a deduplicated pool of exact source spans and links each hit to containing text/header, preceding direct text from an ancestor, ancestor headings and quoted-block boundaries where represented. These relations describe source hierarchy and order, **not proven legal governance or sufficient evidence**. Whole-section context remains available, including following exceptions that must not be mislabeled as preceding parent clauses. No lexical vocabulary, proposals, mechanism decisions or semantic scoring rules change.

Actual run:

| Quantity | Result |
| --- | ---: |
| Design bills | 40 |
| Characters scanned | 337,823 |
| Candidates, unchanged | 706 |
| Lexical hits, unchanged | 2,654 |
| Hits with structural context links | 2,567 |
| Deduplicated structural spans, summed across bills | 1,932 |
| Mechanism abstentions, unchanged | 480 |
| Accepted labels | 0 |

The 87 hits without the new context links are in official titles (65), other form text (12), or text without a containing represented boundary (10). Their existing candidate context remains available. This attachment coverage is not semantic recall or complete XML-structure certification.

The exact same lexical output intersects 399/501 effect quotations under the old reference and 401/501 under v3. The two additional intersections result from expanded reference quotations, **not extractor improvement**. No compatibility graph or semantic accuracy estimate is inferred from quote overlap. The five original narrow suggestions remain unchanged and unvalidated.

## Checks and review

Independent code review identified an inherited malformed relative-path traversal that could hang; the v2 entry point now rejects malformed paths before invoking frozen v1. The old implementation was not changed. Methods review also prompted stronger runner checks: every supplied structural span must match the source path/tag/range and exact text; ancestor links must be direct children preceding the hit's branch; quoted-block links must bind actual containing ancestors. These checks validate supplied relations, not whether every legally relevant relation was found.

Fifty-four focused tests passed. Coverage includes unchanged v1 behavior, source-offset and Unicode cases, quote/list/negation context, malformed paths, parent preservation, targeted correction scope, blocking peer disagreement and tampered structural links. Normal and optimized execution reproduce the same result. An independent agent replay also reproduced the result, verified every hit/context binding and confirmed all four code hashes in the original extractor registration remained unchanged. No full-suite claim is made.

```sh
python3 -m scripts.mechanism_reference_v3 --directory data/research-runs/mechanism-reference-v3-20261108
python3 -m scripts.run_mechanism_context_v2 --output data/research-runs/mechanism-context-v2-20261108 --reference-directory data/research-runs/mechanism-reference-v3-20261108
python3 -O -m scripts.run_mechanism_context_v2 --output data/research-runs/mechanism-context-v2-20261108 --reference-directory data/research-runs/mechanism-reference-v3-20261108
```

Run registration: `4dc0bb3d75381f654dd9d8b349df516653eb08071ec32f87063fb3f7b3775655`. Result: `82c28b7f07e49b7f6ea963951cb8dc0139caf3b7f0e8ea6e26fc99aa93e1ba0e`. Runtime sources, outputs and reviews remain ignored under `data/`.

Preservation replay verified all 133 inventoried prior reference, review, source-view and extractor files unchanged, with an identical frozen-model audit. Receipt: `ca0c5dbd31d7a0d5fa75d80747913bc02283b66043e6a394c807ca7c468e9549`. No protected quality text was parsed, no new source was fetched, no outcome was scored, and no model, schedule or promotion changed. The shared research lease was released.

## Next experiment boundary

This batch supplies corrected provisional examples and auditable context associations. A separate candidate-rule experiment can now test the reviewed vocabulary gaps against fixed v3 references and held design contrast fixtures, while preserving these outputs as a baseline. Legal-effect matching still requires an explicit reviewed compatibility graph; historical prediction still requires eligible source evidence. The work establishes neither 60% predictive improvement nor autonomous self-learning.
