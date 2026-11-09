# Independent target inventory v3 review

November 9, 2026. This separately versioned offline inventory follows the two preserved parser failures and five-case official-record reconciliation. The review covers a source-readiness census and sample, not a new predictive evaluation.

## Preflight

The reviewed scope policy validates canonical identity before determining whether a record belongs to Congresses 113–118 H.R./S. Valid identifiers outside that scope may retain missing metadata in a quarantine ledger; this does not repair their source values. All target identity/date errors, duplicate identities, unexpected repairs or missing required repair cases block sampling. Five exact, previously reviewed corrections are bound through the immutable sidecar hash and retain original blank values. Unknown target metadata cannot be imputed from an identifier suffix.

Eight independent tests supplement nine author tests. **All 17 passed in normal and optimized Python before execution.** They cover exact SHA-256 ordering of the 100-case sample, outcome sentinel exclusion, case-equivalent duplicates, out-of-scope resolution quarantine, target missing-date rejection, exact-original repair matching, missing registered repairs, and calendar boundaries. The final preflight also reviewed preserving the earlier parser's explicit midnight-only date forms, rather than accidentally narrowing accepted input to date-only strings. Canonical date output retains the original input value separately.

The day-180 check uses introduction civil date plus 180 calendar days, strictly before January 3 of the Congress's ending year. Equality fails. It is a calendar-horizon description only: it does not establish event-free status, source timing or forecast eligibility. All five reconciled bills lack a day-180 checkpoint before Congress end. They remain in the introduced-bill source inventory, and the fixed 100-case source-readiness sample is not filtered using this diagnostic. Every sample row carries an exposure warning; none is represented as untouched confirmatory evaluation.

The bounded official-directory collector was also inspected before acquisition. It registers twelve exact Congress/type directories, permits no redirects/retries, bounds HTML responses with a size sentinel, requires exact official HTTPS XML-link paths and scopes, reports duplicates and rejects visible pagination or malformed relevant links. Accepted directory parsing establishes observed identifiers only; the implementation explicitly does not certify official completeness or historical availability. No independent network requests were issued.

## Postrun

An independent parser replayed all **414,277** logical source records from the unchanged source bytes and recorded reversible offsets. The replay exactly reproduced **75,622** individually valid target records, **338,501** valid outside-scope records, **38** outside-scope missing-metadata quarantines, and **116 errors**: 102 invalid target introduction dates and 14 invalid identities. All five sidecar corrections were reproduced with their original values; every target date and day-180 flag matched. The five reconciled records all lack a day-180 window before Congress end. No other source fields were interpreted as outcomes.

All 116 errors remain in the error ledger; the 100-case sample correctly contains **zero** cases, a shortfall of 100. Individually valid rows are not a released complete census. The independent replay also reproduced all **54** version-reference rows and all registered input/code/output hashes. Reference mappings alone do not establish actual introduced-text joins or availability.

The official collector received twelve HTTP 200 responses totaling **35,211,033 bytes**, exposing **75,605** unique XML identifiers. Its first parser conservatively rejected all twelve indexes because each also linked its directory ZIP archive. A separately reviewed and registered offline successor classified only that exact same-directory official ZIP link separately. Independent HTML parsing reproduced all twelve identifier sets and confirmed XML membership unchanged between versions. Each directory has one separately classified ZIP link; no extra network request was needed. No official completeness or historical availability was certified.

The separately reviewed offline set comparison has **75,592** shared identifiers, **13** official identifiers absent from the valid candidate rows, and **30** candidate identifiers absent from the observed official directories. Independent set calculations reproduced every per-group mismatch and all 116 retained error records with their presence flags. Presence is not a verdict on introduction, eligibility or final outcome; absence is not proof a bill never existed.

| Verified runtime receipt | SHA-256 |
|---|---|
| Target v3 independent review | `4ad60ab45b746d10755e1a8c8fd8fa7daafce49a96e77711ffd5ee9801240097` |
| Official offline v2 independent review | `89411324a54fa306482a4ceb6b38d0a5be38d953bd8ab956d8d3cdc6b59a6b08` |
| Identity comparison independent review | `445e4c626966d417b3f26b8cce6a607c4f9a82e2162ca253bf7d3b9d201cf893` |

These receipts are `independent-review.json` in `data/research-runs/bicam-inventory-target-v3-20261109/`, `bicam-official-inventory-offline-v2-20261109/`, and `bicam-inventory-compare-v1-20261109/`, respectively. Standalone independent replay scripts are retained for the first two. All checks were offline; independent review made no network requests and fitted no models. No predictive performance was measured. Prior five-case procedural exposure remains explicitly disclosed; the identity-only passes do not erase it.
