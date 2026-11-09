# Synthetic bill identity and temporal-boundary preflight

2026-11-08. Engineering preparation only; no real source records, bill outcomes, protected quality texts, model fitting or predictive testing were accessed by this work.

## Purpose and implementation

The recovery plan requires exact bill/version identity and a distinct information-availability clock before predictive work. `scripts/bill_provenance_preflight.py` supplies a separate pure validation module. It changes no frozen adapter or experiment and is not wired into production feature construction.

- `validate_identity` compares Congress, bill type, number, text version, raw-byte SHA-256 and rendered-view SHA-256 against a caller-trusted expected object. It validates positive integer identity fields, allowed bill types, digest form and version syntax. **It does not validate the official version-code vocabulary or establish that the expected identity is true.** Two matching assertions are not independent source evidence.
- `verify_bytes` optionally binds both supplied byte streams to those digests. It cannot establish public availability or that the rendering is a complete faithful representation of the raw XML.
- `utc` requires an explicit timezone and normalizes instants to UTC. A date alone or timezone-naive timestamp is rejected rather than assigned an invented zone. `day180_cutoff` uses introduction plus 180 elapsed UTC days and requires a strictly positive remaining prediction horizon. This helper validates the asserted clock; it does not certify the introduction date or at-risk/enactment status.
- `feature_eligibility` requires `known_at`, `source_available_at` and `version_available_at` at or before the prediction cutoff, inclusively. An announced scheduled event may occur after the cutoff. Actual events and realized adjournment may not. A cancellation's `event_at` means the cancellation's effective instant, **not** the original event date. Cancellation and revision information learned after the cutoff is excluded.
- `select_schedule_vintage` operates on one explicit event identity, chooses the latest eligible known-at vintage, rejects equal-time ambiguity, and returns unknown when every supplied vintage is ineligible. It does not infer zero legislative opportunity from absent schedules. An empty history is an input error. A known cancellation can supersede an announcement.
- Family relationships receive `family_screening_only`; they cannot become historical features through this helper. Real family review remains necessary for leakage exclusion. A later-discovered tie may justify exclusion, but not a retrospective historical predictor.

Every feature/schedule decision and the fixture report carries `historical_source_certified: false`. `eligible` means only that these **asserted metadata clocks** pass conditional engineering checks. Retrieval dates, independent historical rendition identity, external source verification, reviewer certification and custody are not supplied or inferred. Identity validation and temporal eligibility are separate helpers; callers must compose both and authenticate their expected inputs.

## Exact synthetic cases

The committed manifest `tests/fixtures/bill_provenance_preflight_v1.json` specifies 25 cases and exact expected dispositions: exact identity; wrong Congress, type, number, version, raw digest and rendered digest; exact day 180; offset-equivalent boundary; naive cutoff; one-second-early checkpoint; zero and negative horizons; inclusive availability; each of three clocks one microsecond late; missing version availability; future announced event; future realized adjournment; family screening only; later schedule revision; later cancellation; all supplied schedule vintages unavailable; and ambiguous equal-time vintages.

The fixture uses artificial digest strings in identity-comparison cases and does not pretend they authenticate source bytes. A separate unit test calculates actual byte hashes and rejects wrong raw/rendered bytes. Additional unit checks cover boolean/zero identity integers, malformed type/version/digest, missing fields, known cancellation, mixed event identities and explicit certification nonpromotion.

## Validation and reproduction

Author checks: `python3 -m unittest tests.test_bill_provenance_preflight` and its `python3 -O` equivalent each passed six test methods. The manifest executes as part of that unit method; root execution will separately freeze inputs and retain its report. The design is deterministic; no random sampling, fit budget, timing or cost claim is involved.

Standalone execution after freeze:

```sh
python3 scripts/bill_provenance_preflight.py tests/fixtures/bill_provenance_preflight_v1.json
python3 -O scripts/bill_provenance_preflight.py tests/fixtures/bill_provenance_preflight_v1.json
```

The output includes each case ID, observed result/error, whether it exactly matches the prewritten expectation, synthetic-only scope, and explicit no-history-certification/no-predictive-test declarations. Passing synthetic fixtures establishes rejection/selection behavior for these cases, not completeness across all edge cases or accuracy on real bills. Independent review and consolidated immutable run receipts are recorded by the root workflow.

## Remaining work

A production adapter still needs source-authenticated identity/version mappings, independent availability evidence, explicit rendering completeness checks, real schedule-vintage coverage with unknowns, corrected introduction/at-risk clocks, reviewed family data, and previously required reference/source/human gates. The day-180 convention must remain aligned with the registered target, and labels at or before the checkpoint must remain excluded by the separate risk-set validation. This module neither proves nor implements those external facts.
