# Official BILLSTATUS source-readiness audit v1

This is an adaptive source change after the separately preserved BICAM v3 audit found unresolved metadata. It does not pass BICAM's gates. Sampling uses the accepted official offline-directory inventory's 75,605 current HR/S identifiers across Congresses 113–118, independently of BICAM metadata acceptance. No fitting, predictions, labels, outcome selection or replacements. The deterministic 100-case sample is a source-readiness diagnostic, not an untouched confirmatory evaluation.

Verify each proposed XML URL is an exact href in the preserved corresponding official directory HTML. Register complete input/code/test/protocol hashes and all 100 exact IDs/URLs before fetching. Rank by SHA-256 of `official-billstatus-readiness-v1`, newline and canonical ID; take first 100. Do not filter or replace cases based on subsequent success, metadata completeness, source differences, outcomes or calendar eligibility. The official directory review must pass before this run begins.

At most 100 GETs, one per case, zero retries/redirects, 20-second socket timeout. Each body read is capped at 2,000,000 bytes plus one sentinel, aggregate maximum 200,000,100 bytes. Save request intent before IO, response headers/status and retained raw bytes in ignored runtime. Preserve HTTP and parsing failures per case; network failure does not trigger replacement. A socket timeout is not a measured whole-run deadline. No linked text bodies are downloaded.

Reject DTD/entity declarations, NUL/UTF-16 encodings and oversized bodies before standard-library XML parsing. Preserve full tag-path/count fingerprint for parseable schema, without importing prohibited field values. Explicit identity schemas only: billStatus/bill with Congress, billNumber/billType (legacy) or number/type (modern), exactly one scalar each, introducedDate. Old documented H maps to HR; no fuzzy matching. Identity mismatch, invalid dates and unsupported schemas remain errors; report full known schema-path fingerprint rather than infer meaning.

Context audit reads dates/counts only for actions; sponsor identifier presence; cosponsor join/withdrawal dates; text-version date/type and source URL metadata. It never reads action text/codes, laws/final outcome values, titles, summaries or policy text into derived output. Tag-path counts can reveal structural presence, and version metadata can reveal procedural progress; therefore exposure is explicit and never used to claim pristine evaluation data. Final source bytes inevitably contain other fields but remain ignored raw evidence.

Identity-valid means exact requested identity plus syntactically valid introduction date; it does not include the separate calendar checks. Report both separately. Calendar diagnostics (introduction within Congress and introduction+180days strictly before end) do not establish actual at-risk eligibility or historical byte availability. Empty containers, absent fields and unsupported nested structures must be distinguishable through fingerprints/counts. Reference structure is based on the [official GPO XML guide](https://github.com/usgpo/bill-status/blob/main/BILLSTATUS-XML_User_User-Guide.md); actual schema is validated, not assumed from documentation. The current rendition is not a historical capture.

Independent synthetic/adversarial review precedes registration; independent replay follows without new requests. Report all 100 per-case results and errors, exact counts/denominators, configuration, immutable evidence, and remaining source/methods gates. No official legislative completeness or predictive improvement is established.

```sh
python3 -m unittest tests.test_official_billstatus_readiness_v1 tests.test_official_readiness_independent
python3 -m scripts.official_billstatus_readiness_v1 --output data/research-runs/official-billstatus-readiness-v1-NEW
```
