# Source-render coverage and provenance-edge readiness audit

2026-11-08. Design-source accounting and synthetic validation only. **All forty source views reconcile at the parser-text level, but a real table-boundary defect and fractional-number ambiguity remain.** No semantic completeness, historical eligibility, human qualification or forecasting gain is established.

## Questions, population and versions

Question 1: which parser-visible text/tails and structural components of the official source survive the frozen reading view? Question 2: do explicit identity and availability checks reject mismatched versions and facts learned after a prediction cutoff in fixed synthetic scenarios?

The actual-source audit uses the same forty design bills (eight per Congress 113–117), fixed source bytes and frozen renderer `block-boundaries-v2`. Its 337,823 rendered characters and existing references/locators are not changed. The other ten original design cases are not pooled; all fifty quality cases remain unopened. This run does not re-score the 501 reference effects or change the 449/501 previous locator diagnostic. No source acquisition, individual outcome access, model fitting or predictive testing occurred.

The provenance exercise is a distinct 25-case synthetic manifest, not 25 real bills. It checks supplied identity/time assertions; it does not obtain evidence that those assertions are historically true. No new production feature builder is wired to these helpers.

## First registered attempt: failure preserved

The first audit rejected all DOCTYPE declarations. All 40 actual sources contain such declarations, so **0/40 source audits completed and 40/40 failed** with `DTD declarations forbidden in coverage audit`. The 25 synthetic provenance cases passed. The original fixtures had omitted this official-source convention. This was a compatibility mistake in the new audit, not proof of missing bill content.

First registration: `c1a28a2c91260f4c083e1dd5ffa8e993e7af7811125c82d9a0caf0d79b255b40`. First result: `b28fd1e13ec0cc21d690402953a188722d952c7b3685707069e470b6ba9505ec`. All original code, tests and forty failure artifacts remain immutable in `data/research-runs/readiness-coverage-20261108/`.

A separately named audit v2 permits external DOCTYPE identifiers without loading external resources, rejects internal subsets/entities, and records unresolved declarations. A pre-freeze independent test then exposed ExpatError escaping the retained-failure boundary; the new version normalizes parser errors to ValueError. These failures were fixed before the second registration, not overwritten after its result.

## Second registration and measurement definitions

The second run pins the first result, identical population/source views, 83 input files and 19 code/test/fixture files before parsing. Source digest/length and view identity are authenticated first: missing/corrupt inputs would block before registration. After registration, parse/accounting failures are recorded per bill without replacement. Each audit repeats to check determinism and nonmutation; all registered bytes are rechecked at completion.

The audit independently reconstructs parser-visible text/tail events but shares the renderer's frozen BLOCKS vocabulary. It inventories qualified XML names, attributes, node hierarchy, represented/unrepresented spans, table/row/cell relationships and exact text offsets. Text segments are measured after XML normalization and character-reference decoding; this is not a raw-byte-to-character map. Comments, processing instructions, external resources and visual or attribute semantics are not thereby verified.

Second registration: `0451d73edc7bfdcd1e097fe07659d3c34727fff9d9753c9597a549b196cae2f0`. Second result: `9c82fc612cef6d480d6afcaa7c18e41431c9fbc806f885acd1aadff0b178b9c6`. Synthetic result: `73a2f764c16a441da4fbd1b2b089d6c4fbf18310a99f22c0760c09619ccfaa99`.

## Actual-source results

| Measurement | Result |
| --- | ---: |
| Authenticated design bills |40|
| Successful source audits |40/40|
| Post-registration failures |0|
| XML elements inventoried |8,331|
| Elements represented as renderer spans |6,667|
| Elements without their own renderer span |1,664|
| Parsed text/tail segments accounted for |9,299|
| Parsed source-text characters |324,489|
| Inserted block-newline characters |13,334|
| Total rendered characters |337,823|
| Nodes with attributes inventoried outside rendered text |2,903|
| Table-related nodes / rows / cells |35 / 10 / 20|
| Recognized nontext-tag matches |0|

`324,489 + 13,334 = 337,823`. All supplied text and spans equal a fresh rendering of authenticated bytes, and every parser-visible text/tail segment is accounted for. **Unrepresented nodes do not mean missing characters.** Their semantic structure may still be absent from the flattened view. Likewise zero recognized nontext-tag matches does not mean no mathematical content: the inventory contains three `fraction` elements outside that narrow flag vocabulary.

| Warning category | Bills affected | Interpretation |
| --- | ---: | --- |
| Attributes not rendered |40/40|Attributes remain in the audit inventory; their semantic role is not interpreted|
| Namespace identity collapsed |40/40|At least one qualified name per bill loses namespace identity in renderer paths|
| External DTD not resolved |40/40|Identifiers recorded offline; external/default semantics not fetched or certified|
| Unrepresented table structure |1/40|114-HR3803 table relationships lack dedicated frozen-renderer spans|
| Adjacent cells without whitespace |1/40|All ten within-row cell boundaries in that table concatenate|

These warning prevalences describe only the fixed design set; no corpus-wide frequency estimate or accuracy interval is claimed.

## Table source case: 114-HR3803

The table has ten rows and twenty cells, including a header row. Within every row, the left-cell end equals the right-cell start with an empty gap. The audit preserves original offsets and cell relationships in its new inventory; the old reading view remains unchanged. A model reading only the old flattened text can lose the date/action pairing.

| Row | Left cell | Right cell | Shared boundary offset |
| --- | --- | --- | ---: |
|1|On or before:|Action to be completed:|1779|
|2|First Monday in February|President submits budget recommendations.|1835|
|3|February 15|Congressional Budget Office submits report to Budget Committees.|1896|
|4|Not later than 6 weeks after budget submission|Committees submit views and estimates to Budget Committees.|2015|
|5|April 1|Budget Committees report joint resolution on the budget.|2090|
|6|April 15|Congress completes action on joint resolution on the budget.|2163|
|7|May 15|Appropriation bills may be considered in the House of Representatives.|2238|
|8|June 10|House Appropriations Committee reports last appropriation bill.|2324|
|9|June 30|House completes action on appropriation bills.|2403|
|10|October 1|Fiscal year begins.|2467|

A supplemental audit checked the nine between-row boundaries: each contains a newline and eight tabs. They are **not** additional literal concatenations, although explicit table topology is still absent from renderer spans. These table dates describe proposed statutory budget procedures; they must not be reclassified as observed legislative-calendar events or historical opportunities to pass a bill.

## Fraction cases and the narrow flag limitation

Two fraction nodes in 113-HR128 occur after the digit 4, yielding `41/2 hours` in flattened text. The XML distinguishes the adjoining whole-number text from the `1/2` fraction node; losing that distinction creates a mixed-number ambiguity. A third node in 117-HR1597 produces `NW1/4`, a land-description expression that must not be blindly normalized as an ordinary mixed number. No model misinterpretation or legal error was measured. All three nodes and their source offsets are retained in the inventory; recognized-nontext count 0 is a narrow tag-list result, not proof of mathematical completeness.

## All forty source cases

Every case failed in the first run and passed text accounting in the second. Warnings and structural qualification remain separate from that pass.

| Bill | XML nodes | Represented / unrepresented | Text segments | Source characters | Added separators | Rendered characters | Cells |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
|113-hr4429|53|23 / 30|88|1771|46|1817|0|
|113-s2088|132|95 / 37|226|6120|190|6310|0|
|113-hr1979|74|44 / 30|103|3533|88|3621|0|
|113-s439|236|200 / 36|274|9666|400|10066|0|
|113-hr128|111|85 / 26|139|5964|170|6134|0|
|113-s5|69|27 / 42|116|2485|54|2539|0|
|113-s848|47|25 / 22|72|1390|50|1440|0|
|113-hr1257|93|67 / 26|121|4712|134|4846|0|
|114-s1259|232|206 / 26|247|7752|412|8164|0|
|114-s375|111|59 / 52|132|2656|118|2774|0|
|114-hr3803|247|140 / 107|294|8129|280|8409|20|
|114-s2940|68|43 / 25|79|2463|86|2549|0|
|114-hr2575|30|12 / 18|54|887|24|911|0|
|114-hr5053|107|84 / 23|132|3392|168|3560|0|
|114-s2769|58|33 / 25|87|2584|66|2650|0|
|114-s2388|178|155 / 23|188|7336|310|7646|0|
|115-hr5527|203|182 / 21|226|7863|364|8227|0|
|115-s1372|70|49 / 21|92|3013|98|3111|0|
|115-s1809|529|489 / 40|569|21383|978|22361|0|
|115-hr1714|34|16 / 18|42|922|32|954|0|
|115-hr5589|86|68 / 18|106|2761|136|2897|0|
|115-s284|140|117 / 23|149|10190|234|10424|0|
|115-hr2259|407|328 / 79|470|17107|656|17763|0|
|115-s1657|1033|836 / 197|1200|35277|1672|36949|0|
|116-hr2943|27|12 / 15|34|814|24|838|0|
|116-hr846|177|135 / 42|205|6263|270|6533|0|
|116-hr7433|98|76 / 22|83|2809|152|2961|0|
|116-hr3024|62|35 / 27|79|1390|70|1460|0|
|116-hr3777|282|261 / 21|306|13823|522|14345|0|
|116-s1076|351|317 / 34|273|12827|634|13461|0|
|116-s2089|70|51 / 19|91|1914|102|2016|0|
|116-s856|107|85 / 22|95|4263|170|4433|0|
|117-s4377|36|19 / 17|40|1137|38|1175|0|
|117-s1230|132|89 / 43|133|3851|178|4029|0|
|117-hr1662|126|96 / 30|116|4365|192|4557|0|
|117-s825|397|374 / 23|297|14211|748|14959|0|
|117-hr2448|71|50 / 21|64|3567|100|3667|0|
|117-hr6835|69|39 / 30|79|2611|78|2689|0|
|117-hr1597|1662|1367 / 295|1935|66363|2734|69097|0|
|117-hr5229|316|278 / 38|263|14925|556|15481|0|

## All unrepresented tag categories

These counts include inline formatting and metadata as well as potentially material structure; absence of a dedicated span is not itself text loss.

| Tag | Count |
| --- | ---: |
|act-name|4|
|action|40|
|action-date|40|
|action-desc|40|
|after-quoted-block|70|
|bill|40|
|bold|2|
|colspec|2|
|committee-name|52|
|continuation-text|1|
|cosponsor|123|
|date|40|
|distribution-code|40|
|dublinCore|40|
|entry|20|
|enum-in-header|2|
|external-xref|149|
|format|40|
|fraction|3|
|header-in-text|17|
|internal-xref|7|
|item|21|
|language|40|
|metadata|40|
|publisher|40|
|quote|449|
|quoted-block-continuation-text|1|
|rights|40|
|row|10|
|short-title|38|
|sponsor|40|
|subpart|1|
|table|1|
|tbody|1|
|term|73|
|tgroup|1|
|title|47|
|toc|7|
|toc-entry|42|

## Synthetic identity and time cases

All 25 fixed cases matched expected behavior. Groups: 7 identity, 6 day-180/horizon, 8 availability/feature and 4 schedule-selection cases. “Pass” includes rejecting invalid input as expected; it does not mean all scenarios became eligible.

Identity binds Congress, bill type, number, version token, raw hash and rendered-byte hash against a caller-trusted expected identity. The `view_sha256` here is a hash of rendered bytes, not an existing sealed-view envelope hash. Version spelling is syntactic, not validation against official version vocabulary. Actual byte checking is separately tested; self-matching metadata proves nothing about source authenticity.

All timestamps require zones and normalize to UTC. The synthetic day-180 rule uses 180 elapsed UTC days and requires a strictly positive remaining horizon; it does not determine whether a bill was already enacted/withdrawn or otherwise at risk. Availability equality at the cutoff is inclusive. A future scheduled event can be represented if its announcement/version was known by cutoff; future revisions, cancellations and realized adjournment facts cannot leak backward. For cancellation, `event_at` is the cancellation instant, not the cancelled meeting's original date. Missing schedules remain unknown. Family metadata is screening-only, not an automatically eligible historical predictor.

| Case | Operation | Expected/observed disposition | Pass |
| --- | --- | --- | --- |
|exact_identity|identity|`{"result": true}`|True|
|wrong_congress|identity|`{"error": "identity/version/digest mismatch"}`|True|
|wrong_type|identity|`{"error": "identity/version/digest mismatch"}`|True|
|wrong_number|identity|`{"error": "identity/version/digest mismatch"}`|True|
|wrong_version|identity|`{"error": "identity/version/digest mismatch"}`|True|
|wrong_raw_sha256|identity|`{"error": "identity/version/digest mismatch"}`|True|
|wrong_view_sha256|identity|`{"error": "identity/version/digest mismatch"}`|True|
|day180_exact|day180|`{"result": "2021-06-30T00:00:00+00:00"}`|True|
|day180_equivalent_offset|day180|`{"result": "2021-06-30T00:00:00+00:00"}`|True|
|naive_cutoff|day180|`{"error": "naive timestamp"}`|True|
|day180_one_second_early|day180|`{"error": "cutoff is not introduction plus 180 days"}`|True|
|zero_horizon|day180|`{"error": "nonpositive prediction horizon"}`|True|
|negative_horizon|day180|`{"error": "nonpositive prediction horizon"}`|True|
|inclusive_availability|feature|`{"result": {"eligible": true, "historical_source_certified": false, "reasons": []}}`|True|
|future_known_at|feature|`{"result": {"eligible": false, "historical_source_certified": false, "reasons": ["known_at_after_cutoff"]}}`|True|
|future_source_available_at|feature|`{"result": {"eligible": false, "historical_source_certified": false, "reasons": ["source_available_at_after_cutoff"]}}`|True|
|future_version_available_at|feature|`{"result": {"eligible": false, "historical_source_certified": false, "reasons": ["version_available_at_after_cutoff"]}}`|True|
|missing_version_availability|feature|`{"error": "missing availability clock"}`|True|
|future_announced_event|feature|`{"result": {"eligible": true, "historical_source_certified": false, "reasons": []}}`|True|
|future_realized_adjournment|feature|`{"result": {"eligible": false, "historical_source_certified": false, "reasons": ["realized_event_after_cutoff"]}}`|True|
|family_screening_only|feature|`{"result": {"eligible": false, "historical_source_certified": false, "reasons": ["family_screening_only"]}}`|True|
|later_revision_excluded|schedule|`{"result": {"excluded_count": 1, "historical_source_certified": false, "selected": {"event_at": "2021-07-01T00:00:00Z", "event_id": "synthetic-hearing", "kind": "scheduled_event", "known_at": "2021-06-30T00:00:00Z", "source_available_at": "2021-06-30T00:00:00Z", "version_available_at": "2021-06-30T00:00:00Z"}, "status": "announced"}}`|True|
|later_cancellation_excluded|schedule|`{"result": {"excluded_count": 1, "historical_source_certified": false, "selected": {"event_at": "2021-07-01T00:00:00Z", "event_id": "synthetic-hearing", "kind": "scheduled_event", "known_at": "2021-06-30T00:00:00Z", "source_available_at": "2021-06-30T00:00:00Z", "version_available_at": "2021-06-30T00:00:00Z"}, "status": "announced"}}`|True|
|missing_schedule_unknown|schedule|`{"result": {"excluded_count": 1, "historical_source_certified": false, "selected": null, "status": "unknown"}}`|True|
|ambiguous_same_time_vintage|schedule|`{"error": "ambiguous same-time schedule vintages"}`|True|

The synthetic manifest contains exact inputs and expected outputs; the sealed result contains observed outputs. Every returned feature/schedule result denies historical-source certification. These pure helpers are not yet a production integration or independently verified historical clock ledger.

## Validation, independent review and preservation

- **535 full-suite tests passed in 79.337 seconds.** Final focused suite: **49 tests passed normally and 49 under optimized Python**.
- Normal and optimized v2 runners return the identical result hash. The independent reviewer separately counted raw XML elements, text/tails, exact segment partitions, all per-bill aggregates, warning counts and table cells, and authenticated every registered input/code/output binding. Independent replay agrees normally and optimized.
- All ten table rows received direct source review. Nine between-row gaps and all three fraction offsets received supplemental review and root exact-source verification. This is complete review of the identified table/fraction cases, not an exhaustive legal review of all unrepresented attributes/tags. No review sampling or replacement occurred; the broader semantic review remains unfinished.
- Three agents worked on XML accounting, provenance and independent challenges. These are collaborating AI reviews with known design exposure, not external blinded validation or qualified human certification.
- All **433 prior preserved files** and frozen-model audit remain unchanged. Preservation before: `76f1af18539c84e26340579793b6c00f1029f3479b08f5c865e45f0752a6deb1`; after: `706b254270dc82808348fe0116b2210ee8393efd154fef5f3c7e752486e2cdd0`, under `data/research-runs/readiness-coverage-20261108-audit/`.

Independent whole-run review: `20faa12f802b458d963481f65219b58f4401b0ddc9a555a36ac05c18d9ec803e`. Supplemental row gaps: `2a0ad049eceb7ade8b95da67bda8b99d0025661972db7ed5148973a818d754dd`. Supplemental fractions: `b36cce4788f2a3daaa982045e85f3aa5d31e50e97793f064714b4ecc9ecaeb29`. Files in the v2 runtime directory: `independent-review.json`, `independent-row-boundary-review.json`, `independent-fraction-review.json`.

Root validation receipt: `validation.json`, hash `dc3f72d566b5060996f005ded3e7ef3c5806358879768b03f1c44ebf2ae79e0a`. The only reported timing is observed test duration; experiment cost/runtime was not instrumented.

Reviews: [original renderer audit](../../research/reviews/20261108-render-coverage-review.md), [versioned DTD correction](../../research/reviews/20261108-render-coverage-v2-review.md), [provenance edge checks](../../research/reviews/20261108-provenance-edge-review.md), [independent challenges/replay](../../research/reviews/20261108-readiness-independent-review.md).

## Decision and next actions

The source-accounting stage completed, with the first failed attempt preserved. The result establishes parser-visible character retention and exposes actual structural risks. **It does not qualify the flattened input for semantic learning.** Keep document-completeness, historical, human and semantic-certification flags false. A successful synthetic guard also does not establish actual source availability or risk-set membership.

Next, create a separate structural input representation preserving table row/column association, fraction nodes, namespace identity and attributes, while retaining original raw bytes and the frozen reading-view offset map. Test mixed numbers separately from land-description fractions; do not apply a blanket string rewrite. If a new reading view is introduced, version it and audit every evidence-anchor migration rather than overwriting existing reference offsets. Use the identified table and fraction cases as exposed design regressions, not future independent validation cases.

Then compose identity/time helpers into a source-evidence gate with genuinely supported version and availability assertions, explicit clock semantics and at-risk checks. Keep statutory/proposed deadlines separate from observed schedule announcements. Complete reference granularity/custody and required independent-review work before protected quality access. Historical availability remains unresolved, and the 60% predictive target remains untested. Follow the [recovery plan](../../research/EXPERIMENT_VALIDITY_RECOVERY_PLAN.md); no model fitting, automatic learning or promotion is authorized by these accounting results.

## Artifact index and reproduction

Both actual runs use the same source bytes, original pilot `318eca5e2797e8d09c14f5d8efe66bbe69e556b05e3861c3ea3f9f3f52fd0c5a` and input population `18ad3d6ca86b0656a8c427dad12337218c753f1ddebb29a360d2c15e8d669ca7`. Runtime data is ignored; a fresh clone does not contain source bytes.

```sh
python3 -m unittest tests.test_bill_render_coverage_audit tests.test_bill_render_coverage_audit_v2 tests.test_bill_provenance_preflight tests.test_readiness_independent tests.test_readiness_v2_independent tests.test_bill_readiness_runner
python3 -O -m unittest tests.test_bill_render_coverage_audit tests.test_bill_render_coverage_audit_v2 tests.test_bill_provenance_preflight tests.test_readiness_independent tests.test_readiness_v2_independent tests.test_bill_readiness_runner
python3 -m scripts.run_bill_readiness_audit --output data/research-runs/readiness-coverage-20261108
python3 -m scripts.run_bill_readiness_audit_v2 --output data/research-runs/readiness-coverage-v2-20261108
python3 -O -m scripts.run_bill_readiness_audit_v2 --output data/research-runs/readiness-coverage-v2-20261108
python3 -m unittest discover -s tests -q
```

`registration.json`, `result.json`, `provenance-fixtures.json` and every `<bill-id>.json` reside in each run directory. Each successful per-bill file contains all nodes/attributes, text/tail segments, separator spans, warnings, DOCTYPE identifiers and table boundaries. No schema or source was silently replaced. Different code/Python requires a new output directory; immutable writes reject differing existing bodies.

| Bill | Final coverage output hash |
| --- | --- |
|113-hr1257|`827515d97d5efe24c17dfa1638334c90fde8392f1cd581f3dc770c330f6dc953`|
|113-hr128|`065a4607e18440f9ab532e57381991759ef618b025cf55b46223fa1bcdba20fb`|
|113-hr1979|`5fa65e718503f53cc9eee92dc94e2f190ae2a7ce3b593cfec41a3539450fbce6`|
|113-hr4429|`5fd3a9560e41f34bad13bd0f4c1d69ac330365ee9fb664231d0705a55a9a8f2d`|
|113-s2088|`10212cfe8b83cd3073aacbda6f65e2deb0892387e2f8072c9c9a7f6c812439b8`|
|113-s439|`78075496bf5efd00e20431f44303872a1f06f96d935be4534b8c44c3a0f14fa0`|
|113-s5|`f86bf4cbf29e4b79b7a6046784504d8e9b3d6e269f825fdd5fd78467e45e225d`|
|113-s848|`10dad9c649798e297f3f53b7642dbd74458aaa271645baf1323735c024a20b8d`|
|114-hr2575|`583984b5f5160d8e04aa04bc3f839788a94cae092f127d4fbbe24af2379845e0`|
|114-hr3803|`62a26b4f249863201ccd019e5c53e28ae21257126034b0a0d0823e885c2664e4`|
|114-hr5053|`69d35348e566f81def8ee24b33f8ce121ab715ca66f49fde4b2b84096bd01696`|
|114-s1259|`64251adb1ff7d562406a50869ef9835698b3d956cba03c6de915732303a0bb6b`|
|114-s2388|`3c4083a170a6de46a10dde6c92e0a6484e2016344c8d0062efc904340d8ef3ac`|
|114-s2769|`b8aef71e62abefd410e62791bfcf458e931e282a3fef677fd392a543cd7cd18e`|
|114-s2940|`471027cb65472a25d4bfd43b910e9c99ba7eee138ce72719c44742159bec88da`|
|114-s375|`f4bdf2d6f37e8620e4200d85719fa919b01e1c1705d487fd7ce42fb078fd5f09`|
|115-hr1714|`aed9180fc571d7794d8e122eba06ac3ee1f442116ead8f22f3a00f218584cadd`|
|115-hr2259|`efad749dc298e8f81aa37459b7012f213a7228546019d592daccafc8fbe79316`|
|115-hr5527|`17c4ccc7d7beb709c8510c45da93f00b281a090dd913683b26614b9791a41078`|
|115-hr5589|`11e21d990f213caeb580e4b88b178ff043605420d0b7fcd2753babffb27aca4f`|
|115-s1372|`da3e308123dd2c9de3203568a6cb36b09c58c59262a0ecc8a6ee10313b87d807`|
|115-s1657|`49d045ba7c4f1800599a31047ca30e16e4ac7686709f828a7b86fb29d7c7e78e`|
|115-s1809|`8ddf6688121c9962d60b6d67a40b8895fe9d68d5aa1954d1164e0bf07290fee7`|
|115-s284|`b27aeff8a6d2918d74b88a94302ba4292b718af42510f44dc40bad64cd862b37`|
|116-hr2943|`f4e6e25c923965fa0ca3c711910031a6fe1342512063a5c60638f000534ece18`|
|116-hr3024|`03eaa61215094787961b63ceb80f41079a1f7df73192e152c58e7260cf7f6b72`|
|116-hr3777|`5b5000782c96f67e1e802e76e1b0c47b45acf43fb8da93c696b4b658bb61ac0e`|
|116-hr7433|`46b2b5088d645fa394637ce6381b382fa41dde45b973768229103530b4b488b8`|
|116-hr846|`691201015f59bc7de237b42edbe509f8570f77d9ef9efeca6b93f21ed4abdcde`|
|116-s1076|`4198dc2b5066bf6c6bb410f529e109d8b74c7b065b05c17f684714dd71118c54`|
|116-s2089|`7c5bd97b5dd9d0725075fae762d3e6d7aac71d797fa13f57631bda76ff258869`|
|116-s856|`2b5970bf6dbb366a90a064e1ce6b2959192d4b8dcb4956dc1e34585427da9e38`|
|117-hr1597|`6cf8d1161c20020c60c35f8860070536d27e7c9fa2a93d4608bce31b3227c3bd`|
|117-hr1662|`32b01c913dc563eaacc17f4f4ae34bd3ac7dcef93e8bcd13ad9c98e20921ef2b`|
|117-hr2448|`a2f58ebfb22d22b6413b6a8ba836e6456a7f78922866621a7e4a491c8e379824`|
|117-hr5229|`378bb910deba24c4ca1fbd4de8e7e71b3da1a3c245356662497e9f3a6fb1dc32`|
|117-hr6835|`623a4cd0fad1b3610b8c6dbd335bec4beb775be7225102eea151185fb2cdc681`|
|117-s1230|`e04c9ddb8a366e23066087b72a53c049c60bae60edfc0dfce06e056066d81651`|
|117-s4377|`a36c15e8188bfb5876f3229f2753d7b3463926bb057ffc2ff7e849803504616c`|
|117-s825|`f6a71f2ac6cda60831215d1047f9947765698fa8261d86a05800f49fe3d1b744`|

| Registered code/test/fixture file | SHA-256 |
| --- | --- |
|`engine/paper_evaluation.py`|`956cb6ef22787c35221194c728130f9b1cc2ad79b376956c2ae2d4d1ed9e526c`|
|`engine/store.py`|`9b29d2cf269589b6a785ed5efb7407697f384c1ee244223fd6de1673107a40b5`|
|`scripts/bill_context_design_text_v2.py`|`2d75e268d073e5616a52a1c1682622b855cc1af060457415e07fe73c429b8ec9`|
|`scripts/bill_provenance_preflight.py`|`3aad59c4277c512c12e1a2077a0884d666f9de67921fc8881704255e554984c7`|
|`scripts/bill_render_coverage_audit.py`|`14863ddbeaebdc8c70282d58917db19af6aafa96c2997a43e725f101f6868119`|
|`scripts/bill_render_coverage_audit_v2.py`|`405550e70c26167187bab618d1e1e604bf78275d03b03851289ead42ca9c0b63`|
|`scripts/mechanism_design_extractor.py`|`b8b58af1f787a703b66ade28e59ebf6a6d8be65649d979bf6f87beeb3deef7a5`|
|`scripts/paper_readiness_audit.py`|`04ad6866134694df95ce6ff60381dacc8158cc52d5c5f19b34a0a28e8ca1b846`|
|`scripts/paper_review_packet.py`|`f8ea40c247f7c0b7e59c14c90ad0ea542ccb7010da2b8165e02bedc432ae8671`|
|`scripts/run_bill_readiness_audit.py`|`0ff2a25d50d2f3e3ccae8b12d44bee2f214c1ac19262bfc35d71282be605a1b4`|
|`scripts/run_bill_readiness_audit_v2.py`|`3915b9e44e80fe02dc8674e204b0bc90260eb45a08370a88df11c81c4b0ca325`|
|`scripts/run_mechanism_design_extractor.py`|`23f32e768e77198a43c6c271aefec811bc2a79ef90bcbd3ffe9a65e7be4d90ce`|
|`tests/fixtures/bill_provenance_preflight_v1.json`|`c1cb489075b3c0fa3118f852785e909d8327ebc1858bb0cb57cc6244a9d6f109`|
|`tests/test_bill_provenance_preflight.py`|`9ff104c761df5a9b48c3c29f200667472c5d6170ca52502a7ee52ebd23b70520`|
|`tests/test_bill_readiness_runner.py`|`7e86f8019dda3d0bee250a36dd1186fa6431462a7f22eb2eb74c276bece495ac`|
|`tests/test_bill_render_coverage_audit.py`|`debdbd01d1263295f198c7cf8431110ba75113be3d3e555de4147fe42a29012b`|
|`tests/test_bill_render_coverage_audit_v2.py`|`da99b42b28071d408fc645d5fbb129da978ab8696f97c96cce35019a02deda8a`|
|`tests/test_readiness_independent.py`|`efc2e7a2ee578b651fe7167abf01bcd04a564a82cb35099d4c2e823a5e78a189`|
|`tests/test_readiness_v2_independent.py`|`fff76b1ad4476a15d06f8c8b3988af9edf539055cd9bc71dfb493e33a0a54678`|
