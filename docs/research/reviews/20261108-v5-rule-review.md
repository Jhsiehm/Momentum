# v5 bounded-subject rule implementation review

November 8, 2026. Engineering preparation on previously exposed design failures. This is the implementing agent's review, not independent semantic certification. No forty-bill rerun or quality-text access was performed by this agent.

## Question and changes

Can five bounded negative-subject rule families recover useful prohibition locators lost by v4 without reopening its observed no-cost, no-limit and cross-block expansion defects? `scripts/mechanism_design_extractor_v5.py` wraps frozen v4 and adds five generic rule families:

| Rule | Bounded subject form | Intended scope |
| --- | --- | --- |
| negative_franchise_authority | Optional state/local + franchise authority/authorities | Explicit authority noun head |
| negative_information_qualified | Information + concerning/obtained/acquired + 1–24 modifier words | Longer information subject |
| negative_evidence_derived | Evidence derived therefrom, or from + 1–24 words | Derived-evidence subject |
| negative_pay_rate_fixed | Rate of pay fixed under/pursuant to + 1–12 words | Compensation ceiling subject |
| negative_coordinated_roads | Optional new; permanent/temporary coordination; road(s), optionally coordinated route(s) with motorized/vehicle modifiers | Explicit transport noun coordination |

All end at may/shall and reject an immediately following not. Modifier words cannot be conjunctions, additional no/not, or modal verbs; punctuation stops them. Matching is confined to a complete leaf text node, retaining inline formatting continuity. No bill IDs, bill-specific offsets, names, reference labels or expected counts appear in rules. The rule choices nevertheless derive from reviewed design examples and are not independent of those bills.

The wrapper retains every v4 locator, its exclusions, all twelve abstentions and all quarantined legacy suggestions. New hit identities are deduplicated by mechanism/start/end; structural context and candidate counts are updated. The old exclusion list remains historical v4 provenance, explicitly labeled: a v5 rule may now recover a location that list describes. The previous and new rule-manifest hashes are both reported. No active proposals or accepted decisions are introduced.

## Actual checks

The five new unittest methods contain ten positive subject examples, ten clause/negation contrasts, three structural negatives, three length-bound negatives, a repeated Unicode/inline source case, and preservation/determinism assertions. Positive cases include changed wording beyond the exposed quotations. Tests check output using the new validity guard.

Executed successfully:

```sh
python3 -m unittest tests.test_mechanism_design_extractor_v5
python3 -m unittest tests.test_mechanism_design_extractor_v4 tests.test_mechanism_design_extractor_v5 tests.test_experiment_validity_adversarial
python3 -O -m unittest tests.test_mechanism_design_extractor_v4 tests.test_mechanism_design_extractor_v5 tests.test_experiment_validity_adversarial
```

Results: five new tests pass; combined suite passes 26 tests in each interpreter mode. These are software fixtures, not semantic or predictive accuracy measurements. No model fitting occurred. Actual forty-bill changes must be registered, executed and reported separately; no anticipated recovery count is asserted here.

## Remaining limitations

- A bounded word sequence is not a syntactic parser. Nonmodal finite verbs inside a modifier sequence can still cause ambiguity; generic semantic correctness is unproven.
- Narrative quotation, findings, negation beyond immediate modal-not, exceptions, later conditions and implied actors require full legal-context review. Retained locators are not affirmative effect decisions.
- The road grammar and modifier limits intentionally omit other coordination and punctuation patterns. Complex obtained-information/evidence coordination is not enabled by an unrestricted wildcard.
- Immediate modal-not rejection applies only to the five additional families. Frozen v4/v2 locators and their known whole-view or semantic false matches remain intact and warned; all legacy suggestions remain quarantined.
- Complete leaf text does not establish complete raw-XML rendering. Source identity, historical availability, reference completeness and human/quality gates remain separate unresolved prerequisites.
- This implementation agent has seen the prior changed-case review. Subsequent design recovery measures are exposed development diagnostics, not independent validation or justification to tune after the registered result.
