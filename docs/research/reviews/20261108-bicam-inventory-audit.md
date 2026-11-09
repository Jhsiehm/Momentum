# Independent BICAM inventory audit — November 8, 2026

## Preflight review

Independent review covered `scripts/bicam_inventory_audit_v1.py`, its author tests, and `BICAM_INVENTORY_AUDIT_V1.md` before network acquisition or registration. The purpose is an identity-only corpus inventory and deterministic future source-audit sample, not model fitting, outcome measurement, text inspection or historical availability certification.

Preflight found and corrected four validity issues: case-equivalent bill IDs could evade duplicate detection; unknown bill types could silently fall outside scope; an inconsistent bill ID/type could hide behind out-of-scope classification; and an empty selected population could report a successful census. Canonical lowercase identities, validation of the eight recognized legislative types and identity consistency before exclusion, and an explicit empty-population issue now address these cases. Sample shortfall must describe the actual sample, including a sample blocked by issues. Invalid identities anywhere in the source table conservatively block sampling; introduction-date checks apply only to selected Congress 113–118 H.R./S. rows. Source issues are retained rather than repaired after acquisition.

Ten independently authored test methods supplement twelve author methods. **All 22 passed in ordinary and optimized Python.** Independent tests cover case-equivalent duplicates, invalid/mismatched type, exact hash-ranked 100-case sampling, outcome sentinel exclusion, date boundaries, legitimate excluded resolution types, trailing deflate payload, encrypted local headers, redirect rejection, and five mocked HTTP identity errors. For incorrect status, ETag, object version, Content-Range or Content-Length, the test confirms rejection before reading any body, one attempted request only, retained request intent/receipt and failure, and no successful result.

The frozen prior ZIP tail binds the directory. Acquisition requires exact current object ETag and version, range/total/length and HTTP 206. It verifies local directory/header agreement and filenames, bounds compressed/decompressed sizes, checks raw-deflate completeness, rejects trailing bytes and validates CRC before saving SHA-256 member identities. The selected bill and reference members require six bounded GETs; the text member is excluded. No independent network requests occurred during review.

Limits: elapsed checks concern network requests/reads, with blocking socket timeout overshoot; parsing and decompression are not a hard wall-clock limited execution. Rejected response bodies need not be read or retained; transport/HTTP exceptions may have only error type/message rather than response-body evidence. Accepted ranges and partial read bytes are retained as documented. A complete identity projection concerns this archive, not completeness against an official congressional inventory. CSV decoding necessarily traverses all raw columns, but only allowlisted identity/date values are selected, examined and retained in the inventory. Source bytes remain ignored. No source licensing or first-publication timing is certified by this review.

## Postrun review

The registered first run retrieved all six ranges successfully, totaling **29,415,382 bytes**, and verified both member CRCs. Independent offline replay reproduced every range offset, exact object ETag/version, receipt length/hash, local header, CRC and decompressed byte identity. All four registered code/test/protocol bindings still match. No extra requests or model fits were made.

Inventory then failed on a malformed CSV row; no census or sample was written. A separate independent structural scan found a 24-column header, 414,178 24-field parser records, 99 five-field records and 99 twenty-field records. None of the short records is blank. These are parser-record counts, not certified bill counts. The failure remains preserved; the source was not silently repaired. Independent review examined row widths only, not title/outcome values.

The independent verifier and complete structural error positions are retained under `data/research-runs/bicam-inventory-audit-v1-20261108/`. The review JSON SHA-256 is `3d21f3a3c03e54d7ddceaa5ec80c7c5ed77150a4b8e2984f8d6a6da16c4f46d8`. Timeout/HTTP-error retention clarifications in this review arrived after the initial registration; the registered protocol was preserved rather than edited. The review's more precise limitations govern interpretation of those claims.


## Separately registered offline successor

A separately reviewed offline v2 declares an LF/CRLF-record interpretation and reversibly escapes unquoted bare carriage returns only within the title field. It preserves raw bytes and restricts the output to identities. This is an adaptive compatibility hypothesis motivated by the observed source structure, not proof of the author's intended dialect or a model-ready text transformation. Congress normalization accepts only positive integer strings optionally followed by a decimal point and zeroes. Seven author tests and five independent adversarial tests passed in normal and optimized Python before execution. Independent tests cover multi-offset reversal, quoted commas/newlines/CR and doubled quotes, wrong-column CR rejection, trailing characters after a closing quote, and explicit fifth-column header binding.

The registered offline run also failed closed: a Congress value did not match the permitted exact integral-decimal syntax. An independent replay reproduced this failure, verified all five registered code/test/protocol bindings and the raw source hash, and confirmed that neither census nor sample exists. The scanner's offset ledger was computed in memory but not saved because the projection failed before return; no persisted ledger or completed normalization result is claimed. No network requests, models or outcome analysis occurred.

Registration SHA-256: `ba32c1ea6f68e50921871d75c1b9744acd28c5b08f558c72a1f08ac6db02b252`. Independent review JSON SHA-256: `d1f44db9abb819bffb767a54976a362246a7765a49545e318075a5a8e4727c2b`. The failed version remains frozen. A full identity-error inventory is more informative than silently relaxing source acceptance until it passes.


## Post-failure identity diagnosis

A separate diagnostic retained the 99 title-CR byte offsets and every invalid Congress record. Independent code (without importing the production scanner or identity parser) applied all 99 recorded replacements, reversed them, and recovered the exact original source bytes. Parsing the declared compatibility projection yields **414,277 logical records, all 24 columns**. This remains a dialect-conditioned structural count, not an accepted target-period census. The independent identity-only pass reproduced all **43** error records exactly; each has both Congress and introduction date blank. Five source identifiers suggest H.R./S.-scope Congresses 113–118: `s4653-116`, `s4899-117`, `s5314-118`, `s5543-118`, and `s5575-118`. Identifier suffixes alone do not supply genuine introduction dates or establish cohort eligibility. No identity values were inferred to repair them.

The next decision is source reconciliation, not further permissive parser changes. Neither frozen version produced a complete census or deterministic sample; no label prevalence, model fitting or predictive test occurred. The version reference file was acquired and byte-verified but not parsed under these failed registered runs.

- Full 43-case diagnosis: `data/research-runs/bicam-inventory-offline-v2-20261108/diagnostic-congress-issues.json`, SHA-256 `ff20ebb3681061c404f9fb86bcc98b02b084f5302bb4e5886718a4e38487706f`.
- All 99 reversible offsets: `diagnostic-title-cr-offsets.json`, SHA-256 `3f8745ff673110e43cf38cc26dd03e6582db8af316d35df0bee05b9cef5f4989`.
- Independent replay: `independent_diagnosis.py` and `independent-diagnostic-review.json` in the same runtime directory; review SHA-256 `699da472e67c77c103c93bfcd72160d525314e9e1c7380e5117ac40796f6fe76`. No independent network requests, protected evaluation-case analysis or outcome inspection occurred.
