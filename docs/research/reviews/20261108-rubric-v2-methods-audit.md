# Bill mechanism v2: independent methods and source audit

November 8, 2026. Completed design-only audit by `rubric_v2_methods`. This report covers the deterministic source subset and every finding from both sealed peer reviews. It is not human certification, an annotation-accuracy evaluation, historical-feature clearance or a predictive experiment.

## Scope and evidence separation

Before the rubric was frozen, the methods reviewer compared its category boundaries with the v1 adjudication and peer challenges. The final rubric incorporated explicit mechanism-relative directions and dimensions, selected quotation offsets, separate unresolved effects, and visible-text-only summaries. No rubric changes were made after observing the new batch.

The reviewer then read all ten complete registered subset texts and saved independent source-first notes before inspecting primary annotations. The subset is the first two remaining original design cases per Congress: 113-hr4429, 113-s2088, 114-s1259, 114-s375, 115-hr5527, 115-s1372, 116-hr2943, 116-hr846, 117-s4377 and 117-s1230. All 120 statuses and all 86 primary effects for those bills were reviewed against the supplied texts.

After the independent peer submissions were sealed, the reviewer inspected all 34 findings, corresponding primary effects and complete relevant bill texts. This required four additional sources for agent B's review of A, and nine additional sources for agent A's review of B: 23 distinct complete bill texts across the methods work. Long text displays were read in successive overlapping sections when output was truncated. Whitespace-normalized displays assisted reading; evidence offsets and validation use the original unmodified text.

No outcomes, quality-case texts, predictive-readiness artifacts, outside legal sources or subsequent bill versions were accessed. Primary annotations, peers, source-first notes and subset findings remain separate artifacts. This is one primary annotation plus peer challenge per bill, with a third-agent subset/challenge audit; it is not two blinded annotations of all 40 bills.

## Original annotation counts

The two sealed primary submissions contain 40 bills, 480 mechanism statuses and 463 action records. Their original status counts are **205 present, 261 absent and 14 uncertain**. These counts precede the corrections recommended here; they are not corrected final labels, error rates or estimates of accuracy.

## Deterministic subset findings

The subset audit recorded 13 findings: 11 concrete correction recommendations and two unresolved category boundaries. Seven bills had corrections requested; three were supported within this review. A supported disposition is a source-based machine judgment, not proof that every possible effect was exhaustively recovered.

| Bill | Disposition | Main finding |
| --- | --- | --- |
| 113-hr4429 | Supported | Whole-paragraph striking supports repeal; missing displaced expiry language correctly remains uncertain. |
| 113-s2088 | Corrections requested | A new scoped prohibition was labeled `restrict`; the amendment quote also stopped before operative deletion/addition instructions. |
| 114-s1259 | Corrections requested; boundary unresolved | Permission quotations omitted the permitted-use/selection lists. Individual-voucher termination does not unambiguously establish programme/authority sunset under the frozen definition. |
| 114-s375 | Supported | Replacement rates are visible; a relative rate reduction should not be inferred from unavailable earlier rates. |
| 115-hr5527 | Corrections requested | Record the explicit fellowship approval condition and distinct qualification/party-balance duties. |
| 115-s1372 | Corrections requested | Preserve the separate scientific-evidence/cumulative-health-risk constraint in action records. |
| 116-hr2943 | Supported | Making bilingual fact-sheet versions does not itself establish a submission or disclosure duty. |
| 116-hr846 | Corrections requested; boundary unresolved | Preserve the distinct training-centre duty. Whether naming an existing database qualifies as renaming a public entity/facility remains disputed. A later peer finding also revises the prohibition status, below. |
| 117-s4377 | Corrections requested | The designation's scoped denial of spending authority introduces a bar; `prohibit/restrict` reverses the direction convention. |
| 117-s1230 | Corrections requested | Correct the same prohibition-direction reversal and bind amendment claims to actual insertion/replacement instructions. |

## Audit of all peer findings

Both peer envelopes passed binding, coverage and evidence-offset checks. All 34 peer findings received a separate methods decision: **33 accepted with explicit qualifications and one retained as uncertain**. Acceptance means the proposed correction or uncertainty is supported under this design rubric; it does not make the corrected label ground truth. These findings overlap some subset findings and must not be added together as a count of independent errors.

| Peer-review target | Findings audited | Main supported changes |
| --- | ---: | --- |
| A's primary batch, challenged by B | 9 | Mechanism-relative prohibition direction; explicit budget timetable dimensions/scope; missing programme-context uncertainty; scoped denial of additional appropriation authorization; preserved State/Tribal powers. |
| B's primary batch, challenged by A | 25 | Missing conditional approval, consent, submission, destruction, notice and payment duties; missing deadline changes and waivers; citation dependencies; quotation scope; separate land-use powers and restrictions. |

Material qualifications and unresolved points:

- **116-hr846:** B identified the explicit clause withholding additional appropriation authorization. Under the frozen definition of scoped power denial, this supports `prohibit/present`, with the unseen expedited-hiring rules retained as additional unresolved effects. This revises the methods subset's initial acceptance of the uncertain prohibition status. The original subset artifact is preserved; the revision is explicit in the peer-audit artifact. It does not imply that all spending is prohibited.
- **116-s1076:** Stamp-sale proceeds must be transferred at least twice yearly, and the transfer duty is supported. Whether this is itself an actual appropriation, rather than transfer of amounts already becoming available under the unseen referenced statute, remains unresolved. Recommend `appropriate/uncertain` with the specific section 416(d) dependency rather than certify `present` or retain an unexplained `absent`.
- **115-hr1714:** The inserted unmarried-person phrase is visible, but the complete grant criterion is absent. The title does not by itself establish a substantive programme-eligibility expansion. The peer's recommendation to retain programme uncertainty is supported.
- **114-hr3803:** Use the rubric's duration convention for replacement timing windows and explicitly identify the real action-deadline rows. The original rationale already excluded fiscal-year commencement; do not inaccurately report that it affirmatively labeled that row a deadline. Permissive consideration dates are also distinct from completion duties.
- **115-hr2259:** The supplied medical-benefit clause explicitly waives a 180-day limit until a final determination, supporting a contingent sunset of that stated permission. This is distinguishable from the unresolved individual-project disqualification boundary in 114-s1259. Unseen Council/survey expiry provisions remain unresolved.
- **115-s1657:** The emergency-acquisition destruction remedy and notice are separate from stored-acquisition notice and evidence-use prohibitions. The failure-to-terminate clause references paragraph (2)(B), although the supplied termination rule is in (2)(C). Retain this source dependency rather than silently correcting the bill. Notification delay also requires the supplied court process; a request alone does not grant delay.
- **116-hr3777:** The public-release clause cites section 110(a)/(b), which is absent from the complete supplied bill. Preserve an unresolved reporting note; do not silently substitute section 11. Subpoena approval conditions and termination of authority also require separate representation.
- **117-hr1597:** A quotation covering only Stump Springs cannot substantiate a target claiming nine special management areas. Extend the evidence through all nine or split/narrow the effects. Separate College/City powers, conditional retention notices, off-highway restrictions, payment obligations and the flood-control plan change from superficially similar effects elsewhere in the bill.

An additional methods challenge emerged while auditing the Commission termination finding: **116-hr3777 effect 9 uses `sunset/remove` for a clause that imposes expiry 60 days after the final report**. Recommend `sunset/create/duration`, while retaining the distinct removal of the programme and its authorities. Removing an entity is not the same operation as removing its sunset. This additional challenge is separately recorded, not counted as one of the 34 peer findings.

## Validator audit and verification

The earlier read-only code review demonstrated that a peer finding could point to an effect of a different mechanism and could claim historical eligibility. Both holes were repaired: indexed findings must match their mechanism, and peer historical eligibility must be false. Input/batch uniqueness and exact set coverage were also added. Source-view hashes bind preserved rendered-view envelopes, not just text; a text-only hash comparison would be incorrect.

The methods reviewer ran `python3 -m unittest discover -s tests -p test_mechanism_rubric_v2.py -v`: **four tests passed**, including the repaired mechanism/index and eligibility rejection checks. It separately unsealed both primaries, both peers, registration and inputs; validated both primary and peer submissions; checked the frozen rubric hash; and verified every recorded finding quotation against its exact original offsets. These checks establish integrity and source matching, not semantic entailment or completeness.

## Artifacts and disposition

Runtime artifacts are under ignored `data/research-runs/mechanism-rubric-v2-20261108/`:

| Artifact | Seal |
| --- | --- |
| Registration | `0833e20efeaa40bc641662a7433ffee910d1927cd3574438cd99138b2cee32dc` |
| A primary | `2a3e3715ac9024140fff6ce2d9d1eddbcc5beea17e1ff8eaecb13e7f99aaebef` |
| A peer review of B | `0c578da1e49847c07d1ce3aa8783cd3c8329c75d583a28082b06dc2e515cee1d` |
| B peer review of A | `eb06cbf09aecf8a3c771add50faae0423809b41c3e10656ba67d6197b4554b75` |
| Methods subset audit | `8cd0f132cbc23ca173ee26b74ab95fe8d9feb66f0fe43cd3dba59b7870df3f3d` |
| Methods peer audit | `dc7f58246d2da130367c455e5dade8bd118f235fad6ed7ce5e1e7717b6ab80d3` |

The peer-audit artifact binds both primary hashes, both peer hashes, registration and the earlier subset audit. It records one decision for every peer finding, exact source evidence, the additional termination-direction challenge and the explicit revision concerning 116-hr846.

The independent review batch is complete. **Correction recommendations remain unapplied to the immutable primaries; no consolidated corrected annotation set is certified by this report.** Resolve clear corrections in a separate versioned layer, preserve disputed cases, and validate that layer before using it to develop an extractor. These results do not authorize model fitting, establish historical source eligibility, satisfy human-review gates or demonstrate any predictive improvement. Shared model biases, omitted legal context and incomplete effect recovery remain material limitations.
