# Independent experiment integrity audit

November 8, 2026. Scope: source identity, schema and provenance boundaries in the provisional reference exporter, graph-conditional evaluator, locator runners and context triage. This audit uses authored synthetic adversarial cases and already exposed design artifacts. It does not access quality texts or outcomes, reannotate all effects, or certify legal meaning.

## Reproduced boundary gaps

1. **Candidate triage does not authenticate all incoming candidate claims.** `classify` rejects mismatched top-level bill/text/view bindings and invalid hit spans, but a synthetic input with a forged candidate context quotation, negative candidate context start, `human_certified=True` and 99 claimed accepted labels still produces triage decisions. Its returned certification remains false. A source-valid selected hit is not proof that its supplied context or upstream claims are valid.
2. **The effect evaluator has an explicitly unverified source boundary.** Length-correct invented evidence with a syntactically valid source hash can receive a graph-conditional true positive when an external compatibility edge supplies the match. The result correctly says `source_content_verified=False`. This is a documented limitation, not a covert assertion of factual correctness; source authentication must precede any future use that depends on real evidence.
3. **The reference amendment helper validates targeted changes, not the entire parent reference.** A synthetic eight-question fixture passes `apply_decisions` with wrong-bill view bodies and an absent mechanism status containing effects. The helper verifies the targeted before/after text and peer agreement but does not independently establish complete parent consistency.

These are interface-level reproductions. The registered runners pin known parent and output hashes and regenerate source-dependent artifacts. The reproductions do **not** establish that the preserved experimental exports are corrupted or that their disclosed diagnostic counts are false. They establish why accepting arbitrary resealed inputs requires a stricter supplemental boundary.

The sealed synthetic receipt is `data/research-runs/experiment-validity-integrity-20261108/reproductions.json`, hash `87c037664856d112bf1ec28de0658c3050c07b49aa5975009a0277f1efd6743a`. It records the inspected code hashes and observed results without modifying frozen files.

## Manifest checks

Independent read-only checks found no file hash mismatches in the context-v2, expansion-v3 and context-filter registrations: respectively 96, 98 and 102 bound file entries. All 40 output envelopes in each run unsealed successfully and matched the corresponding result mapping. This validates preserved bytes and envelope links, not semantic interpretation, historical availability or missing-reference completeness.

## Supplemental adversarial tests

`tests/test_experiment_validity_adversarial.py` targets the new, separate validity guard. It challenges cross-bill source substitution even with matching quote text; missing mechanism fields; unsupported present status; effects attached to absent status; unexplained uncertainty; invalid dimensions; Boolean offsets; missing actor/conditions fields; same-length fabricated evidence; unknown source hashes; forged output flags and counts; invalid candidate context and structural links. A positive contrast explicitly permits an actor-meaning disagreement when source evidence remains valid: a structural guard must not masquerade as an entailment judge.

The initial seven guard test methods passed. Three additional methods then reproduced missing rejection of explicit semantic-certification claims, malformed proposal collections/enums, and overlapping unrelated source nodes. These are development findings against the new supplemental guard, not changes to the frozen receipts; final rerun results are recorded separately below. The frozen evaluator, exporter and prior runners remain unchanged.

## Independent v4 scope review

Read-only review and seven synthetic probes confirmed the intended local expansion boundaries: cross-block provide/records and no/modal combinations do not gain new matches; the no-cost conjunction match is rejected; a normal governmental-entity bar remains locatable; inline XML emphasis does not split a valid information phrase; and a heading does not gain an expanded annual-report match. A double-negative legacy prohibition phrase still locates, but its legacy proposal is quarantined. In every probe all frozen-v2 hits were retained and all original proposals were copied to quarantine.

These checks concern the expanded rules and quarantine policy only. Legacy whole-view locator risks remain explicitly exposed. A phrase inside one text node can still be negated, descriptive, inserted, struck or dependent on other clauses. The narrowed noun-head grammar also sacrifices coverage of unlisted or complex subjects. Neither local scope nor quarantining proposals demonstrates semantic accuracy.

## Limits on promotion

Passing a supplemental guard would establish only the checked schema, source bindings and honest flags. It would not establish that a quoted clause entails the proposed actor, target, operation, dimension or conditions; that external compatibility edges are complete or correct; that all operative effects were annotated; or that the rendition was available at a historical cutoff. A shared quote or a retained locator is not a semantic match. Source-only annotations and agent reviews remain provisional and uncertified. Predictive or semantic-accuracy promotion still requires independently justified references and adjudication plus the existing eligibility gates.

## Final supplemental verification

After the guard owner added the missing checks, `python3 -m unittest tests.test_experiment_validity_adversarial -v` passed **13 independent test methods**, including parameterized corruptions. The final suite also covers source-manifest key and population validation for rows with no effects, malformed quarantine entries and reactivation, and the composed `evaluate_guarded` path. Guarded scoring rejects fabricated exact evidence and unknown graph endpoints while keeping semantic and human certification false. An initial test-fixture mutation reused an unsealed body; copying before mutation corrected that fixture issue without changing the expected rejection behavior.

The final guard was also applied read-only to the actual provisional reference and expansion outputs: **40 bills, 480 mechanism statuses, 501 effects and 2,727 locator hits** passed the structural/source checks. This is not a reannotation or an endorsement of those effects. The separate final receipt, `data/research-runs/experiment-validity-integrity-20261108/final-audit.json`, binds the guard, v4 module and independent test file hashes; receipt hash: `84538c4463f91e24a01d4bbf64c962d4e8c2a6eb88f8562474cc8b6031c7ecc2`.

The caller still must authenticate source envelopes and registered manifests before invoking the guard: a well-formed supplied hash is not self-authenticating. Quarantine validation checks the entries supplied, while replay or a bound baseline comparison is required to establish that no legacy proposal was omitted. The existing semantic, historical-eligibility and independent-evaluation blockers remain; none is removed by these integrity tests.

## Complete v4 changed-case source audit

The frozen 40-bill run (`950af33a265164374f41651dbd3bfdaf6f72bb8759626e602ccb4b3e82867178`) was followed by a complete source review of all 11 removed hit identities, one added identity, two lost reference intersections and two common flag-to-retain transitions. These are overlapping change categories, not 16 independently sampled observations. Exact selected spans and governing source context were checked; no reference labels or frozen rules were changed.

Of the 11 removed hits, **five were useful prohibition locators lost**: a franchise-renewal bar, a conditional geolocation-information use restriction, an evidence-exclusion clause, a staff-pay ceiling and a new-road construction bar. **Five were misleading or nonoperative occurrences removed**: two headings, a bill purpose statement, the previously exposed no-cost/conjunction match, and a no-limit-on-service-terms phrase incorrectly shaped as a prohibition. The remaining removed span improperly crossed a heading into a cause-of-action sentence; the single added span repairs it by selecting only the operative sentence.

The two lost reference intersections are useful coverage losses: 115-s1657 effect 26 (violation-conditioned evidence exclusion) and 117-hr1597 effect 27 (new-road construction bar). They reduce the raw and retained intersection count from 449 to 447 of 501 provisional effects. That is a locator tradeoff, not a measured change in semantic accuracy. The franchise-renewal reference still intersects a separate sanction-exclusion hit. The geolocation-use restriction and pay-ceiling hits intersect no existing prohibition reference quote, so their loss is invisible to this overlap metric. This audit neither repairs nor certifies reference completeness.

Both common flag-to-retain transitions occur in 115-s1657, on `authority` at 14274:14283 and `certification` at 14744:14757. Source context places both tokens in explicitly struck operands. The stricter classifier declines the qualified amendment-prefix forms and retains the occurrences with deletion provenance unestablished. This is conservative abstention with residual misleading context, not proof that the prior flags were wrong or that these are new operative effects.

The authoritative revised receipt is `data/research-runs/mechanism-validity-v4-20261108/changed-case-review-v2.json`, hash `f1921d14f67e85e844129d902b1813d03c57d4f36636191a1ee1b873af97b132`. The first receipt remains immutable; the revision corrects two initial explanations that incorrectly attributed unchanged overlap to other hits rather than no corresponding reference intersection. All 16 final record spans and context-evidence spans were verified. Existing legacy locator risks and all semantic/historical certification limits remain. This was a complete changed-case audit on exposed design bills, not fresh or independent validation.
