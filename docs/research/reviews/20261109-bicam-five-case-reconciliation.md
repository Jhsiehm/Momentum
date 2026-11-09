# Independent five-case official-record reconciliation review

November 9, 2026. This review concerns five source identities with missing Congress and introduction dates in the BICAM archive: `s4653-116`, `s4899-117`, `s5314-118`, `s5543-118`, and `s5575-118`. These were selected because the prior identity diagnosis found missing fields in the declared target scope, not because of legislative outcomes. This is source reconciliation, not model fitting or a predictive experiment.

## Independent acceptance framework

The review was conducted in parallel with acquisition; this document is not evidence that a completed independent preflight approval preceded execution. The following framework guided the independent evidence assessment.

1. Freeze the five identities and expected introduced-Senate packages: `BILLS-116s4653is`, `BILLS-117s4899is`, `BILLS-118s5314is`, `BILLS-118s5543is`, and `BILLS-118s5575is`. Record source URLs, request limits, code and protocol hashes before requests. No replacement cases after failure.
2. Obtain only declared official GovInfo HTTPS metadata URLs under bounded request/response limits. Record timestamps, HTTP outcomes, byte lengths and hashes. Follow no arbitrary redirects; preserve missing/error evidence. Independent review makes no additional network requests.
3. Confirm identity from actual metadata, not just its URL: Congress, bill type/number, package identifier and introduced-Senate edition must agree. Reject unrelated or conflicting records. Verify successful XML parsing and retain exact field locators and values used as evidence.
4. Treat issue/publication dates according to their stated semantics. An introduced-edition package date can establish that edition's asserted issue date. Do not silently call a generic publication, update, ingestion or digitization date the bill's introduction date. A proposed introduction date requires explicit introduction/action evidence or a clearly documented, separately labeled inference; ambiguity remains unresolved.
5. Check any candidate date falls inside the identified Congress and agrees across available relevant source fields. Preserve precision and conflicts; do not invent intra-day ordering. A successful identity check does not certify an introduction date.
6. Keep the original BICAM blanks, raw archive and failed registered runs unchanged. Store proposed reconciled fields separately with original values, evidence locators/hashes, retrieval timestamps, acceptance disposition and reasons. Never overwrite the source to manufacture a passing census.
7. Today's official metadata is a retrospective assertion. It does not establish that today's bill bytes or metadata were publicly available at the historical forecast cutoff. Keep historical eligibility false and the existing source, family, label, review and model gates unchanged.

The five-case exercise cannot establish archive-wide completeness, resolve all 43 missing-field records, release the previously blocked 100-case sample or justify fitting a model. Any subsequent census must be separately versioned and registered with the reconciliation policy and remaining exclusions explicit.

## Execution and independent evidence review

The initial fixed five-request GovInfo MODS phase returned five HTTP 302 responses to an error route; no introduced bill rendition or MODS evidence was recovered. A separately fixed Congress.gov overview fallback returned five HTTP 403 responses. A third separately fixed Congressional Record fallback returned five HTTP 200 PDFs. These are adaptive acquisition phases, not one originally prespecified successful route. Independent replay verified all 15 saved bodies against receipts, lengths, SHA-256 hashes and expected URLs. Independent review made zero additional network requests.

All ten saved extracted evidence pages exactly match a fresh pypdf extraction. Five principal pages were also visually inspected. Complete additional heading/continuation pages were extracted and retained separately so the introduction category is not inferred merely from a nearby bill number.

| Bill | Retrospectively supported introduction date | Evidence and qualification |
|---|---|---|
| S. 4653, Congress 116 | 2020-09-22 | Record Senate pages S5787–S5788, PDF pages 55–56: introduction heading followed by the S. 4653 entry. S5788 visibly carries a CORRECTION marker. |
| S. 4899, Congress 117 | 2022-09-20 | Daily Digest D995, PDF page 1: introduction range S. 4886–4901 includes S. 4899. This is explicit range-membership reasoning, not a separately named introduction entry. |
| S. 5314, Congress 118 | 2024-11-13 | Daily Digest D1009, PDF page 1: introduction range S. 5303–5314 includes S. 5314. This likewise uses range membership. |
| S. 5543, Congress 118 | 2024-12-16 | Senate S7057, PDF page 100 explicitly describes introduction earlier that day; introduction heading/list continues on S7058–S7059, PDF pages 101–102. |
| S. 5575, Congress 118 | 2024-12-17 | Senate S7104–S7105, PDF pages 1–2: dated introduction heading/list includes S. 5575. S7105 visibly carries a CORRECTION marker. |

These civil Record dates fall within the identified Congresses and support a separate retrospective reconciliation ledger. No intraday timestamp, actual first-publication time or original introduced-text byte identity is established. The reviewed S. 5575 granule carries December 17 as its date; a different legislative-day convention must not silently replace it. Corrected current Record pages further prevent claims that these exact renditions existed unchanged at the historical cutoff. No sample, model or forecast gate is released.

Incidental passage/procedural information is visible on the fetched pages. All five cases must be marked exposed development material; this review does not claim outcome-blind reading. That exposure is not a newly computed outcome label or predictive performance measure. The archive's original missing values and failed versions remain unchanged, and the other 38 missing-field cases are outside this five-case reconciliation.

The independent verifier initially made two incorrect assumptions about the registration schema while checking URL bindings: the first two phases specify routes through pinned acquisition code rather than an explicit URL map. Those verifier errors were corrected before producing the review receipt; no source artifact was changed or refetched.

Runtime evidence is retained in `data/research-runs/bicam-five-record-20261109/`. `independent-context-pages.json` contains complete relevant context pages, SHA-256 `5d564754be880a00b7db3cb0608adb8376c617272bc975d363bfbebb882cae07`. The executable independent replay is `independent_verify.py`; its successful review receipt is `independent-review.json`, SHA-256 `f31aeb8d7c533a6e90c663cd1ba3b1aa6023065e5b1e19012e3b14f30d9e11c6`. The receipt contains every phase registration hash and all 15 source-body hashes. Review supports the five retrospective dates with the above qualifications, not historical forecasting eligibility.


## Final ledger and preservation check

Independent verification also confirmed all three acquisition-script hashes against their phase registrations, all **32** files in the before-run preservation inventory unchanged, and all five proposed ledger rows correctly bound to their saved PDF receipt/hash and original missing values. The separate reconciliation ledger hash is `8df8d519dc6206033a3130fd784de818c7ab3fa26eaedf1039d62f1531f88a67`; the independent ledger review receipt is `independent-ledger-review.json`, SHA-256 `4fe483c5a68e72568843333a2c75427fa1f909f7e02eb34b6717f0b7e0560e89`, in the Record runtime directory. This preservation inventory is bounded to the recorded 32 files and is not a claim about every repository artifact. Root reports 34 existing focused tests and three compilation checks; independent review here verifies source evidence and bindings, not new predictive performance. No full-suite run is claimed.
