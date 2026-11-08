# Mechanism v2: resumed annotation and reciprocal review

November 8, 2026. User requested resumption after the prior spending-cap interruption. Agents resumed successfully. The [earlier partial receipt](20261108-mechanism-rubric-v2.md) and all sealed outputs remain preserved. The [frozen rubric](../../research/BILL_MECHANISM_RUBRIC_V2.md) was not changed.

## Completed primary and peer work

Both annotators read their complete assigned sources and sealed separate 20-case primary submissions before peer review. Together: **40 bills, 480 mechanism statuses and 463 evidence-linked effects**. Original statuses are 205 present, 261 absent and 14 uncertain, with ten additional unresolved-effect notes. These are original provisional counts, not corrected final labels or evidence of accuracy.

Each annotator then read the other batch's complete sources and reviewed its summaries, statuses and effects. A reviewed B's 222,948 text characters and 266 effects; B reviewed A's 114,875 characters and 197 effects. This is one primary annotation plus a later peer challenge per case, not blinded duplicate annotation or an agreement study.

| Peer reviewer | Cases supported without findings | Corrections requested | Uncertain | Findings |
| --- | ---: | ---: | ---: | ---: |
| A reviewing B | 11 | 9 | 0 | 25 |
| B reviewing A | 12 | 7 | 1 | 9 |
| Total | 23 | 16 | 1 | 34 |

No finding does not imply correctness. Common challenges include direction relative to the named mechanism, omitted duties or waivers, insufficient quote scope, and missing external dependencies. Original annotations and disagreements remain immutable; a later corrected representation must be a separate version bound to these originals.

## Predictive readiness remains unchanged

This work strengthens representation design; it does not train a model. Every calibration subset in the already-exposed readiness intersection has zero positive outcomes, and two training cores also have none. See the original receipt's full counts. Do not fit or claim predictive skill from this selected design cohort. Broader dated source coverage and sufficient natural outcomes must precede a separately registered matched predictive comparison; choosing evaluation bills by outcome would bias that comparison.

The next representation step is a separate correction addendum retaining uncertainty and missing referenced law, followed by a frozen extraction/encoding design. Original human, historical-source, family and prospective audit gates remain intact. Quality cases remain unparsed and protected for later measurement. No new sources acquired, fits, scores, forecasts, promotion or scheduler changes.

## Sealed evidence

Runtime directory: `data/research-runs/mechanism-rubric-v2-20261108/` (ignored).

- B primary: `a6b4afea6290bfe99855bb52b7db5d4d79236a3422fafebeecc306fa03842daa`.
- Primary audit: `0d33aeae7724b3ffc9b200afbb4241d53bbd1c75178455f0554d09d762bb64ba`.
- A peer: `0c578da1e49847c07d1ce3aa8783cd3c8329c75d583a28082b06dc2e515cee1d`.
- B peer: `eb06cbf09aecf8a3c771add50faae0423809b41c3e10656ba67d6197b4554b75`.
- Peer integrity audit: `38ed1b7318c4f7588b9821c1fb2a83b56f6b4245ec72b5edfc8d4f7e8fb85119`.
- Methods subset audit: `8cd0f132cbc23ca173ee26b74ab95fe8d9feb66f0fe43cd3dba59b7870df3f3d`.

Replay primary/peer validation with `python3 -m scripts.mechanism_rubric_v2_audit data/research-runs/mechanism-rubric-v2-20261108 --peers`. Validation checks artifact structure, evidence offsets and binding, not semantic truth or historical feature eligibility.

## Root validation

Eleven focused tests passed after resumption (the v2 rubric, v1 design audit and boundary-aware text-rendering suites). Primary and peer integrity replay passed for all 40 cases and 34 peer findings. All 40 input views matched the preserved source envelopes; all 359 original pilot files, frozen model audit and the previously sealed A submission remain unchanged. No full-suite rerun claimed for this annotation/review batch. Runtime preservation receipt is saved separately. Shared research lease was acquired for this resumption and released at close.

## Independent methods audit completed

The methods reviewer audited all 120 statuses and 86 effects in the fixed ten-case subset after reading those sources first. It recorded 13 findings: eleven concrete correction recommendations and two rubric-boundary disputes (individual-voucher termination and database naming). These overlap some peer findings and must not be added to them as independent error counts.

It then reviewed all **34 peer findings** against the complete relevant source texts and original effect inventories: **33 accepted with stated qualifications; one remains uncertain**. Acceptance means a challenge is supported, not that every replacement label is settled. The uncertain appropriation classification requires referenced law not present in the supplied text. The reviewer also identified one additional reversed sunset direction in 116-hr3777. A later finding explicitly revises its initial acceptance of uncertainty in 116-hr846, based on an overlooked scoped denial of authorization; both receipts remain preserved.

[Detailed methods report](../../research/reviews/20261108-rubric-v2-methods-audit.md). Methods peer-audit digest: `dc7f58246d2da130367c455e5dade8bd118f235fad6ed7ce5e1e7717b6ab80d3`. Root independently checked exact coverage of all 34 finding identities, peer/primary/source bindings, decision counts and every evidence quote, plus the additional finding. All passed. These are recommendations with explicit uncertainty, not a consolidated ground-truth dataset. No automatic correction or claim that the remaining labels are error-free.
