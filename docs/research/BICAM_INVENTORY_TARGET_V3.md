# BICAM target-population inventory v3

This separately registered offline source-readiness audit preserves the failed v1/v2 runs and all raw bytes. No network, label inspection, model fitting or forecasting. The target remains Congresses 113–118 inclusive, H.R./S. bills. Prior source inspection and five official-record reviews are explicitly exposed; any released sample is for source readiness, not an untouched confirmatory evaluation.

Before full projection, freeze code/tests/protocol, original bill/reference SHA-256 and reviewed reconciliation sidecar SHA-256. Reuse v2's declared LF/CRLF dialect and reversible title-only bare-CR escaping; retain the 99 expected offsets without assuming actual count. Raw source bytes are unchanged. The dialect remains an explicit compatibility assumption, not publisher intent or modeled bill text.

Validate every canonical bill identifier/type/number and duplicates before scope. Accept exact-integral decimal Congress only where present and require identifier consistency. Missing Congress on a validated outside-target identifier is retained in an explicit quarantine, with original fields and identifier-derived scope; never silently dropped. Missing target metadata can be reconciled only for the five pinned reviewed cases and only when original blank fields match exactly. Preserve original values, proposed values and evidence hash. Do not infer dates or replace other missing values. Any unhandled target error or contradictory identity anywhere blocks sampling. Enumerate all recoverable row-level errors in one pass rather than successive guess-and-repair runs. Fatal schema/CSV failures remain explicit.

Retain v1-supported ISO date-only or midnight datetime suffix (space/T00:00:00 with optional zero fractional seconds); preserve original and canonicalize the output date. Require target introduction dates to fall within the identifier's Congress. Save internally consistent target census and every quarantine/error/repair separately. Choose up to 100 cases by ascending SHA-256 of `bicam-inventory-target-v3`, newline and canonical bill ID only after the entire target passes. Every candidate retains an exposure flag. This is internal consistency of the archive under the stated assumptions; independent official enumeration, labels, class coverage, text joins, date eligibility and predictive gates remain separate.

Parse the small version-code reference independently after registration, even if census/sample later fails. Its mapping does not establish that introduced text actually joins for any selected bill. Exact reference rows remain ignored runtime. Report denominators for all source rows, valid outside-target identities, outside-target quarantines, target candidates, repairs, errors and sample shortfall.

```sh
python3 -m unittest tests.test_bicam_inventory_target_v3 tests.test_bicam_target_independent
python3 -m scripts.bicam_inventory_target_v3 --output data/research-runs/bicam-inventory-target-v3-NEW
```

Predeclared calendar-only diagnostic: compute introduction plus 180 days and whether it is strictly before the next Congress starts on January 3. Report both counts per Congress and retain each case's date/flag. This is not actual at-risk eligibility because prior enactment/stage/outcomes are unexamined. It does not alter the inventory or hash sample. All five reconciled cases are expected to fall after their Congress end; verify rather than assume.
