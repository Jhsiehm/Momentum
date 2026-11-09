# BICAM offline identity projection v2

This is an adaptive separately registered parser compatibility diagnostic after the v1 inventory failed. No new network, source text study, outcomes, training or predictions. The v1 raw members and failure remain unchanged. Before registration we observed integral-decimal Congress strings, 99 five-column and 99 twenty-column fragments, and carriage-return bytes. These findings motivate an explicit LF/CRLF-record dialect assumption; they do not prove author intent.

Register all code/test/protocol and raw-input hashes before full parsing. A quote-aware scanner preserves doubled quotes, quoted CR/LF and CRLF record endings. Only unquoted bare CR within the fifth field, verified as title by the CSV header, may become literal backslash-r. Save every source/projected byte offset and replacement; reverse all replacements and require exact original bytes. Bare CR elsewhere, unsupported quoting, unclosed quotes or any resulting record not exactly 24 columns block execution. This is an identity-only compatibility projection, never a source text transformation usable for modeling.

Retain only bill ID/type/number/Congress/introduction date. Accept Congress only as a positive integer string with optional decimal point followed exclusively by zeroes; reject fractional/exponent/nonfinite/whitespace forms. Bill numbers retain the v1 rule. Reuse the frozen v1 identity checks with normalized Congress strings. All unresolved issues block the sample; no outcome-conditioned exclusion or silent row concatenation. Freeze complete identity census under this declared dialect, then a 100-case sample by ascending SHA-256 of v2 version, newline, canonical bill ID. Parse the reference table only after both artifacts are saved.

Coverage concerns this archive under the assumed dialect, not official completeness, prediction readiness, historical availability or class balance. Existing protocols/gates are unchanged. Actual structural errors and uncertainty must be reported. Raw bytes remain ignored. Independent synthetic tests and review precede execution; offline replay follows.

```sh
python3 -m unittest tests.test_bicam_inventory_offline_v2
python3 -m scripts.bicam_inventory_offline_v2 --output data/research-runs/bicam-inventory-offline-v2-NEW
```
