# Five-case official-record reconciliation — 9 November 2026

## Result

All five target-period missing-date cases have separately recorded, official Congressional Record support for proposed Congress/introduction-date metadata. Two use membership in explicitly enumerated introduction ranges; three have individual entries or an explicit same-day introduction statement. Original BICAM blanks remain untouched. This is retrospective metadata reconciliation, not historical-byte certification, a complete census, a predictive experiment or a released training sample. The other 38 original missing-field cases remain unresolved.

Question: can official records supply the missing identity/date facts for the five already selected cases without silently imputing dates or changing frozen inventory versions? This was an adaptive source study, with each direct acquisition phase registered before its five requests. No models, training, scoring, calibration or performance comparisons ran. No accuracy gain or 60% target progress is measured here.

## Every case

| Original ID | Proposed Congress | Proposed introduction date | Evidence location and basis |
|---|---:|---|---|
| s4653-116 | 116 | 2020-09-22 | [S5787–S5788; PDF pages55–56](https://www.govinfo.gov/content/pkg/CREC-2020-09-22/pdf/CREC-2020-09-22-senate.pdf); Individual entry under introduction section; current page marked CORRECTION. |
| s4899-117 | 117 | 2022-09-20 | [D995; PDF page1](https://www.govinfo.gov/content/pkg/CREC-2022-09-20/pdf/CREC-2022-09-20-pt1-PgD995.pdf); Daily Digest explicit introduction range S4886–S4901 includes4899; range-based identity/date reconciliation. |
| s5314-118 | 118 | 2024-11-13 | [D1009; PDF page1](https://www.govinfo.gov/content/pkg/CREC-2024-11-13/pdf/CREC-2024-11-13-dailydigest.pdf); Daily Digest explicit introduction range S5303–S5314 includes5314; range-based identity/date reconciliation. |
| s5543-118 | 118 | 2024-12-16 | [S7057; PDF page100](https://www.govinfo.gov/content/pkg/CREC-2024-12-16/pdf/CREC-2024-12-16.pdf); Explicit statement introduced earlier today; date on page. |
| s5575-118 | 118 | 2024-12-17 | [S7104–S7105; PDF pages1–2](https://www.govinfo.gov/content/pkg/CREC-2024-12-17/pdf/CREC-2024-12-17-pt1-PgS7104-2.pdf); Individual entry under introduction section; current secondpage marked CORRECTION. Calendar date retained; legislative day may differ. |

Congress identity is reconciled by Senate bill number and the dated Record's congressional period, not by overwriting a blank from its identifier alone. Both original Congress and introduction fields were empty in all five cases. Dates have day precision; no midnight timestamp is invented. Range-based cases are explicitly distinguished from individual introduction entries.

## Acquisition, failures and scope changes

1. Fixed five expected introduced-Senate-edition GovInfo MODS URLs: all returned HTTP 302 to the GovInfo error page, zero response-body bytes. Redirects were not followed. No inference that an introduced bill does not exist is justified by these failures.
2. Separately registered fixed five Congress.gov overview URLs: all returned HTTP 403, retaining 27,730 response-body bytes. No retries or browser-protection circumvention.
3. Search-discovered Congressional Record evidence motivated a separately registered fixed five-PDF phase: all HTTP 200, **4,286,800 bytes** retained. All bodies hash-verified, decoded locally with pypdf; relevant pages rendered with PyMuPDF and visually reviewed. The system lacked pdftotext; that failed local extraction attempt made no source changes, and installed pypdf/PyMuPDF were used instead.

Each script binds its own code hash and five cases before requests; third phase also pins exact discovered URLs. Phases one/two cap each read at 1,000,001 bytes with acceptance at at most 1,000,000; third at 10,000,001 with acceptance at at most 10,000,000. A capped oversize prefix would be preserved and rejected. All actual responses stayed below limits. Socket timeout 20 seconds, zero redirects/retries; no hard total elapsed deadline. Errors and HTTP bodies are retained when available. No secrets/API keys used.

Search and web-open discovery calls are additional to these **15 direct acquisition requests**, not included in their byte totals. Browser opens of all five Congress.gov pages were restricted. Search returned irrelevant same-number bills from other Congresses; none were used as replacements. Search results and Record pages exposed procedural outcomes incidentally. Therefore these five cases are now explicitly design-exposed; neither outcome blindness nor untouched evaluation is claimed. No labels were imported into a model.

## Timing and missing-data rules

- Keep original values, proposed values, evidence URL/hash, page/section and review separately. Do not mutate registered inventory v1/v2 or acquired source bytes.
- Accept these five day-precision dates as retrospective official-record metadata only. Two pages visibly carry CORRECTION labels: S5788 for S4653 and S7105 for S5575. Current corrected renditions do not establish bytes or exact availability at historical checkpoints.
- For S5575 use the civil Record date December 17, 2024. The fetched introduction granule supports that date; it does not itself establish legislative-day timing. Do not substitute a legislative day or infer within-day ordering.
- Missing/ambiguous identity or date remains null with a reason, never zero or a fabricated date. Endpoint absence is not evidence of non-introduction. The remaining 38 records are not silently dropped or filled.
- A future inventory successor must explicitly register scoped missingness/enrichment policy, official population cross-check and version joins before sampling. These five repairs alone do not satisfy the old all-record census gate. No retrospective redefinition of the frozen success criteria.
- Do not require an IS rendition to establish that a bill was introduced. Its absence at one endpoint may reflect a source route/edition limitation. Actual introduced-text eligibility remains a separate question; later ES/PCS texts cannot silently substitute for introduction text.

## Verification and next decision

Root checked all 15 retained response hashes, all three registered code hashes and all 32 prior inventory artifacts unchanged. All 34 existing inventory tests passed; all three new acquisition scripts compiled. No full-suite rerun: production/predictive code is unchanged. These checks establish receipt consistency, not semantic forecasting accuracy. Independent reviewer checked page dates, section continuity/range membership, current corrections and all five proposed facts; see linked review for exact disposition.

Next: separately version the target-population identity projection with the reviewed enrichment sidecar and a predeclared treatment of the38 out-of-scope defects, then validate complete target coverage and inspect the frozen version-reference table. Freeze the outcome-blind sample only after those checks; maintain an exposure registry and keep the stage benchmark. No predictive fit becomes eligible from this receipt alone and no existing gate is marked passed.

## Evidence, code and reproduction

[Independent review](../../research/reviews/20261109-bicam-five-case-reconciliation.md).

Acquisition code: `scripts/bicam_five_reconciliation_v1.py`, `scripts/bicam_five_congress_v1.py`, `scripts/bicam_five_record_v1.py`. These are one-shot frozen executors tied to the paths below; do not rerun into existing directories. The first phase requires its output directory (created before registration); the others create exclusively. Reproduction should verify existing receipts offline; a fresh network rerun needs a separately versioned output location and registration, as live sources can change.

Checks: `python3 -m unittest tests.test_bicam_inventory_audit_v1 tests.test_bicam_inventory_independent tests.test_bicam_inventory_offline_v2 tests.test_bicam_offline_independent`; `python3 -m py_compile scripts/bicam_five_reconciliation_v1.py scripts/bicam_five_congress_v1.py scripts/bicam_five_record_v1.py`.

Runtime evidence stays in ignored `data/research-runs/`. Hashes below are raw-file SHA-256, not historical timestamp proofs.

| Artifact | SHA-256 |
|---|---|
| bicam-five-reconciliation-20261109/preservation.json | `b16760b4a015aa661d42ac41914892c9dffba854393d92ad2d802b9f78da5266` |
| bicam-five-reconciliation-20261109/registration.json | `be30b0eaec6ea27a836bfedff3b562d15d242a119d69673ab53e149c41f0b708` |
| bicam-five-reconciliation-20261109/s4653-116-intent.json | `83b5410430c3578e47af9b3fe15c23b72b47d6e5f261b0be6b73c9ebf8bbcae7` |
| bicam-five-reconciliation-20261109/s4653-116-receipt.json | `4dbf0d0ae9acc8ba87d147ae9f0b61648aaa3f49c98d465a9ad957bdb2ef1a1c` |
| bicam-five-reconciliation-20261109/s4899-117-intent.json | `22552ec096f78718db24cd49f817d6dd76720416114c096614604af8a631b1fb` |
| bicam-five-reconciliation-20261109/s4899-117-receipt.json | `e5ae5790c2d2f22ea571f02fa412f195e857dc6370f1cf6939c8f99bac9585bd` |
| bicam-five-reconciliation-20261109/s5314-118-intent.json | `c17184f780da7615966f6d5c65a8da9d9fd6b0197960b51922199c004a7e1436` |
| bicam-five-reconciliation-20261109/s5314-118-receipt.json | `9ff4ab0d93513e69823d215a3e49a7f17cdf8116c98c947ac19263a5c81d2d85` |
| bicam-five-reconciliation-20261109/s5543-118-intent.json | `9078692b92e6a05c69dc531cad1f27404b49e749d343d035f786e1b73a378505` |
| bicam-five-reconciliation-20261109/s5543-118-receipt.json | `a4784f2e8ebb226b20a6b02593907a458894b26b18b10d574b0171acb46b9348` |
| bicam-five-reconciliation-20261109/s5575-118-intent.json | `a42ac7d459fa0dce509bdbea2e414021dac45f3aff41bab45e02fd5bad24996a` |
| bicam-five-reconciliation-20261109/s5575-118-receipt.json | `8059e47edbdb0a094be5864d126e2a1bf9fb3f06144cf7ee4c3cbe4edd954dff` |
| bicam-five-congress-20261109/registration.json | `d8d7043505bee30ae16e88258767543758b492a935a30f936fdc54efd7358801` |
| bicam-five-congress-20261109/s4653-116-intent.json | `8749c64465fcc6942580ed666c956276525fea0e13515d8f58ec0b1610f1c9fc` |
| bicam-five-congress-20261109/s4653-116-receipt.json | `dfd8dedc0eff0d7163541995c3597a5d39574e8b1b4f0bf029ab43e95b9c2584` |
| bicam-five-congress-20261109/s4899-117-intent.json | `45fac61fe1b7c8e2ed8e92c714deebabfab8b374d7c45040b9e951eb1a49f497` |
| bicam-five-congress-20261109/s4899-117-receipt.json | `ab6babfe77e19c4790e5e889d0b91f22d547595b8074ca33edc48b6740f650d0` |
| bicam-five-congress-20261109/s5314-118-intent.json | `2af433002f135a4cad84f3b4dfed03e8ed1e1c8ba39016f30dfcc56eeb87119e` |
| bicam-five-congress-20261109/s5314-118-receipt.json | `15a2918176349cbf1295e25f8d5e5005cfd6423c012238dd253a00a3ca558d6b` |
| bicam-five-congress-20261109/s5543-118-intent.json | `f9d32d475d8f3e59476f72cd464c1e380e9ed14cd37d310518965a0bcff1e23a` |
| bicam-five-congress-20261109/s5543-118-receipt.json | `360b3fa80fdde756f82a6811aa1d0c41f212834e18c41dbe57458e712845710e` |
| bicam-five-congress-20261109/s5575-118-intent.json | `0e23319fcf2350142286186dbeb20821d1357aec3e02b3cca20a84ab9a427488` |
| bicam-five-congress-20261109/s5575-118-receipt.json | `c19e5d370985ed4f43748845fb3982b1ae7bb81abec562ef7d9e9c07dccef3da` |
| bicam-five-record-20261109/independent-context-pages.json | `5d564754be880a00b7db3cb0608adb8376c617272bc975d363bfbebb882cae07` |
| bicam-five-record-20261109/independent-review.json | `f31aeb8d7c533a6e90c663cd1ba3b1aa6023065e5b1e19012e3b14f30d9e11c6` |
| bicam-five-record-20261109/reconciliation.json | `8df8d519dc6206033a3130fd784de818c7ab3fa26eaedf1039d62f1531f88a67` |
| bicam-five-record-20261109/registration.json | `4335fd3e9c885b7f6b58c320d4529d4cf6e80d106258598e806564537e4f406a` |
| bicam-five-record-20261109/root-validation.json | `a6e613f43d90d5e0ba6bb098a7a1960777b0ef51ba6b47aee37f79fd753c58b3` |
| bicam-five-record-20261109/s4653-116-evidence-pages.json | `b1cb69b3d62bf933ad7c454a4b9bc9d459b0a7d602c923f12189f563010508c9` |
| bicam-five-record-20261109/s4653-116-intent.json | `302e7b32f110523415f41bea4f4a3c9747d40598cc36a6e98b82788379d0d8d4` |
| bicam-five-record-20261109/s4653-116-receipt.json | `bffa5d22349a6871ec59d54bb68c1192d6d9d106edd3a35dfe4ede0726342fc4` |
| bicam-five-record-20261109/s4899-117-evidence-pages.json | `82c24617c239fd828ca91172b6270f44e7d35442e0541a314686041ae305427e` |
| bicam-five-record-20261109/s4899-117-intent.json | `3e6e67306df86efa404ce8e29f5b33d91603e8a15ce51eb56c97d8bf1d407d88` |
| bicam-five-record-20261109/s4899-117-receipt.json | `6c09a415cbd06817017bed8b7e84e50c01cc90139d64e550605226819a64e177` |
| bicam-five-record-20261109/s5314-118-evidence-pages.json | `e4ee685c2cf68fddb70f93679e86fcd9350d52d7c425dbf06467823b3448d00d` |
| bicam-five-record-20261109/s5314-118-intent.json | `d20343b60efd278e8b9ae3f58cc07d119dc29c699cc159cf45c2e69fc0f6df1a` |
| bicam-five-record-20261109/s5314-118-receipt.json | `4a771b608c4c60bcb11a88d76f5796efd449412960b720402f4e4d61f8bae41a` |
| bicam-five-record-20261109/s5543-118-evidence-pages.json | `7b3d7437efb90a831a3c9c3c88cfef8769b6cdd3530049018f6ab7de9c46a33d` |
| bicam-five-record-20261109/s5543-118-intent.json | `14fb775964d49f6454a7e6027772a4cc027ec5afbde676e3ea1a0a23a45f4de7` |
| bicam-five-record-20261109/s5543-118-receipt.json | `b596992e14a76c2a185f06c71b9e67cf245ef53dbf34b9fac70f9f0d72dd840b` |
| bicam-five-record-20261109/s5575-118-evidence-pages.json | `3da03b94ec1077237b6d2ad06a7a9c427ffb8e1743a7049763f3422f6fb7c63d` |
| bicam-five-record-20261109/s5575-118-intent.json | `42f058ca46f7868467cd78489986b88bb0df7cc428e8f38ca6164277b1acc032` |
| bicam-five-record-20261109/s5575-118-receipt.json | `0090501ac0561c3205006f367dfa567034a5e0480ce08c28f86532208371372d` |

| Record PDF | Bytes | SHA-256 |
|---|---:|---|
| s4653-116 | 670386 | `049b485be8e06a3f5659956282c8b9e77eb26846f42c9223fed17c2a0aedbc83` |
| s4899-117 | 310582 | `78974d9559535c81d6b95bd510a2c4cc627f1af155cd2e3e241a5556aaef6e79` |
| s5314-118 | 404398 | `4208086b9e62006885076f62686b9d2503ebdf89eb7dfd5e03445f16c2925b6e` |
| s5543-118 | 2652948 | `4a1803b8bc8457f86168bc5ad87409c0477b1c889a5989b803fab8a3fa2709fc` |
| s5575-118 | 248486 | `920be124603c799ba259125b5f348b74c888820c4c88ba54a4f2e3ebc6c7cd4f` |

Independent review completed successfully. Its verifier first encountered two harness issues (context output directory ordering and assuming every registration held an explicit URL map); these were corrected without source changes or further network.

- `independent-review.json` SHA-256: `f31aeb8d7c533a6e90c663cd1ba3b1aa6023065e5b1e19012e3b14f30d9e11c6`.
- `independent-context-pages.json` SHA-256: `5d564754be880a00b7db3cb0608adb8376c617272bc975d363bfbebb882cae07`.
- `independent_verify.py` SHA-256: `618c18b90d0dde3c7374566444b6b94f7da4b93eeae642b667440944936f8b74`.
