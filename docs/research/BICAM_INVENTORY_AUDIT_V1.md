# BICAM identity inventory audit v1

This is a separately registered public corpus suitability audit, not a predictive experiment. No labels, final status, final counts, text, fits, or existing forecast-gate changes. Source CSV bytes necessarily contain other columns, but parsing retains and examines only bill identity, type, number, Congress and introduction date. Raw source bytes remain ignored and are not published.

Before network IO, register script/test/protocol hashes, prior directory hash, archive ETag/version/size and the two selected member directory entries. Use the already verified archive tail, SHA-256 `8fa40bc106615a3243e505e6d44d8bd4a02119c957412880175ff71166d68a49`. Retrieve only `bills.csv` and `ref_bill_version_codes.csv` from the BICAM bill ZIP. At most six requests: exact 30-byte local header, filename/extra, and compressed member for each. No redirects or retries; require exact status 206, range, length, ETag and object version. Record request intent before IO and preserve responses/failures. Never fetch the full archive or text member.

Aggregate directory compressed sizes must not exceed 50,000,000 bytes and uncompressed sizes 300,000,000 bytes. Variable local headers add at most 262,200 bytes. Socket timeout is 20 seconds and elapsed time is checked against 180 seconds before requests and reads; a blocking socket operation may extend that limit by up to the socket timeout. Check local/central metadata, filename, raw-deflate EOF, no trailing payload, exact uncompressed length, CRC32, and full SHA-256. Exclusive file creation prevents overwriting runs.

Enumerate all source identity rows; select completed Congresses 113–118 and H.R./S. bills, with positive integer bill number, consistent source identifier and introduction date inside Congress. Duplicate/missing IDs, malformed selected identities/dates or invalid Congress fields block sample creation rather than silently repairing records. IDs and types are canonicalized to lowercase before duplicate/identity checks; only the eight recognized legislative types are allowed. All identities are checked before scope exclusions. Other valid bill types and Congresses are counted as outside scope. An empty selected population blocks the census; fewer than 100 eligible identities is an explicit sample shortfall. The complete census claim concerns this archive's identity table, not independent official legislative completeness. Freeze the identity census then choose the first 100 cases sorted by SHA-256 of `bicam-inventory-audit-v1`, newline and source bill ID; selection occurs before outcomes or text are examined. No prevalence or predictive sample adequacy can be established here.

Parse the version-code reference only after census/sample persistence. Record its exact rows in ignored runtime. It can establish a documented code mapping, not actual bill/text joins, completeness or historical availability. Independent preflight review and offline tests precede requests. Independent replay of saved bytes should verify every selected identity and sample with no additional network requests. All prior paper and E3 gates remain unchanged.

Reproduce in a new directory only:

```sh
python3 -m unittest tests.test_bicam_inventory_audit_v1
python3 -m scripts.bicam_inventory_audit_v1 --output data/research-runs/bicam-inventory-audit-v1-NEW
```
