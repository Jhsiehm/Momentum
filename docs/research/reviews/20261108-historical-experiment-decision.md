# Historical experiment decision review — November 8, 2026

## Decision

Proceed with a **separately registered retrospective association diagnostic**, conditional on the already available current introduced-text renditions. Its narrow question is whether adding this text improves held-out loss over the same six structured features **within this source-covered, already exposed historical subset**. It cannot establish what could have been forecast with information actually available at the historical checkpoint. Historical source eligibility remains unresolved; the original paper and matched E3 gates remain blocked and unchanged.

The user's current authorization asks agents to make routine research decisions and collect needed public data autonomously. This authorizes selecting and implementing this limited study; it does not turn agents into qualified human reviewers or certify missing historical custody. The separate study must explicitly record its own limited deviations from the original human-review and reviewed-positive-family floors. It does not inherit the calendar study's exceptions or claim those requirements passed.

This is a scientific scope change, not a way to make an unchanged forecasting claim pass easier gates. Irrespective of scores, no deployment, promotion, confirmatory success, general all-bill accuracy, or 60% improvement claim follows. A different, genuinely dated forecast study is still required.

## Fixed smallest useful experiment

- **Target:** original legacy own-bill public-law enactment after the day-180 checkpoint and before Congress end, among the legacy still-unenacted risk set. “Passed” must not ambiguously mean committee passage, one-chamber passage, or enactment through another bill. No new endpoint or relabeling.
- **Periods:** evaluation Congresses 115 and 116 only, selected because the existing acquisition contains evaluation sources there. Congress 117 has no source-covered evaluation cases and is excluded for that known readiness reason before scores. All periods have prior development exposure.
- **Training:** within each legacy fold, union its core and calibration identities and then apply the frozen source-availability and exclusion rules. Retain earlier-Congress, training-label-availability and provisional global-family-disjointness checks. This is one training population; no calibration is fitted.
- **Two arms per fold:** fixed six-feature anchor versus the identical anchor plus the frozen introduced-text representation. Exactly four model fits; no hyperparameter search, resampling fit, alternative endpoint, added arm or post-score population replacement. Failed/nonconverged fits remain failures and do not authorize replacement fits.
- **Source membership:** existing metadata-dated *current* introduced XML, not certified historical XML. Select by previously registered source receipts and identity/family/schema checks before loading labels. Retain every excluded candidate and reason. Exclude every identity and every provisional family in the entire 100-bill pilot, including protected quality cases; do not open those texts/labels. Both arms use exactly the same rows. A source failure excludes the row from both arms rather than becoming an all-zero missing-text vector.
- **Representation:** registered synthetic-tested preprocessing and sparse implementation without modification: retain substantive language/negation/citations; mask focal identity and external administrative boilerplate; preserve structural segment boundaries; core-only (here, unified training-only) TF-IDF, minimum document frequency five, maximum document frequency .95, at most 10,000 unigrams/bigrams, row L2 normalization. Fit means/scales for six structured columns on those same training rows only.
- **Numerics:** same frozen penalized logistic objective and convergence criterion. No calibration: sparse events make a separate fitted calibration map unstable, and splitting the limited source-covered training population further is not useful for this initial association diagnostic. This choice precedes scores and must not be reinterpreted as calibrated probability validation.
- **References:** training-only Beta(1,1) smoothed historical rate and the existing fixed stage smoothing formula, scored on the same evaluation rows. The model-to-model paired comparison is primary; historical-rate skill has a different denominator and must remain separately labeled.
- **Hard computational stops:** missing training class; empty learned text vocabulary; invalid identity/family/time binding; nonfinite values; failed convergence; input/code hash changes. Evaluation with no positive events permits negative-case loss summaries but makes positive-class/discrimination metrics undefined and cannot establish event detection. Do not select new cases to manufacture events.

## Metadata-only feasibility checked in this review

Read only sealed registrations, source receipts and published aggregate review reports; no individual outcome vectors, protected quality text or predictions were opened. The expansion registration supplies 232 baseline source identities plus 1,000 successful current-source additions, yielding 1,232 identities. Removing the 32 source-covered identities that belong to the 100-bill pilot leaves 1,200. **These are preliminary identity-only counts, before pilot-family exclusion and real-schema/preprocessing failures:**

| Evaluation period | Source-covered original core | Source-covered original calibration | Unified training | Source-covered evaluation |
|---|---:|---:|---:|---:|
| 115 | 433 | 111 | 544 | 300 |
| 116 | 676 | 172 | 848 | 300 |
| 117, not selected | 947 | 230 | 1,177 | 0 |

Sources: `data/research-runs/mechanism-training-expansion-20261108-v1/registration.json` and its source records; `data/research-runs/mechanism-training-coverage-20261108-v2/registration.json` pilot exclusions; `data/research-runs/exploratory-calendar-20261108-v1/registration.json` legacy memberships. These are ignored local artifacts, not public data releases. The later execution registration must verify every seal and actual source-file digest; this feasibility inspection did not certify those bindings. Counts must be recomputed after whole-family exclusion rather than copied as final memberships.

## Measurement and interpretation

Report, for each arm/reference and each period: evaluated bills, positives/negatives and distinct provisional families; expected events; Brier loss (mean squared probability error); log loss (mean binary negative log likelihood with a fixed documented numerical boundary); positive- and negative-class Brier with their own denominators; fixed-bin reliability with counts, and source-coverage/exclusion counts. Undefined bins/classes remain explicitly undefined.

Primary comparison is the paired text-minus-anchor difference in equal-period mean raw Brier; also report per-period differences and raw log loss. Relative reduction is one minus text loss divided by anchor loss, whereas rate skill is one minus model loss divided by rate loss. Neither is accuracy or a percentage-point gain. A fixed family-paired bootstrap may describe uncertainty if registered before scores, with cross-period shared-family multiplicities retained and invalid draws reported; it does not repair selection, temporal provenance, provisional-family errors, or previous exposure. No statistical-significance or lead-selection rule is needed for this diagnostic.

The original 200/100 reviewed-positive-family floors remain unmet/unresolved. This limited diagnostic does not redefine them or sum overlapping fold appearances to pass them. Actual class/family counts and uncertainty must be disclosed. A small event count makes estimates unstable regardless of whether both classes exist. No sample-size adequacy or powered effect claim is possible from the metadata counts above; do not invent a replacement numeric floor simply to pass the available data.

## Critical limitations and learning discipline

1. **Source-time uncertainty:** current introduced renditions may contain later rendering/transcription/revision changes. Their introduced-version designation and printed dates do not prove their exact bytes were available at the checkpoint. Chronological row splits do not solve this.
2. **Acquisition-conditioned sample:** sources were selected for an earlier training-coverage exercise. They are not a representative census of all evaluation bills, even though that selection was outcome-blind. Loss comparisons apply only to the frozen covered subset; missingness and exclusion can change its distribution.
3. **Prior exposure:** these periods and some structured results have already informed development. A fresh file name or split does not produce independent validation.
4. **Provisional labels/families:** machine checks and independent agent replay do not certify complete negative evidence, family genealogy, legal source interpretation or human qualifications.
5. **Controlled learning:** the optimizer learns weights from recorded training labels. Future improvement should use new versioned data, frozen candidate specifications and later evaluation, not automatic self-generated labels, test-driven feature changes or automatic promotion.

Working backward from bills with matured outcomes is normal supervised learning. The defensible order is to define the historical prediction question, reconstruct permissible inputs independently of the outcome, freeze the split, and only then train and evaluate. This diagnostic deliberately measures a narrower current-rendition association while reconstruction continues.

## Review disposition

No fatal design contradiction was identified for this explicitly limited four-fit diagnostic, provided the execution registration enforces the rules above. This is a pre-execution AI methods review, not a result, numerical replay, source certification, human signoff or permission to unlock the original E3 study. No model was fitted by this reviewer. Code, exact final memberships, final class counts, and execution outputs remain to be checked independently.

## Independent verification of alternate-dataset acquisition

Independently checked the [historical dataset options report](20261108-historical-dataset-options.md) against retained direct-response evidence, without any new request, bill-row parsing, protected-outcome access or model fitting. Recomputed all **18** file hashes in its result manifest; checked that each of the three plans predates its corresponding request timestamps and observed request counts stay within their declared bounds. Confirmed **10 direct requests**, six HTTP 200 and four HTTP 206, totaling **148,573 saved response-body bytes**, with no recorded HTTP/transport/parse failure. Discovery web browsing is outside this count and was not independently re-fetched.

Reparsed the retained ZIP central directory and reproduced all **26 member names, compressed/uncompressed lengths and declared CRC values**, including the text member's 1,436,764,626 compressed and 6,591,284,872 uncompressed bytes. Verified the archive's advertised 1,936,532,215-byte length, matching HEAD/tail ETag and April 15, 2025 Last-Modified header. Independently reconstructed each of the three prefix offsets, verified its local ZIP member name, saved hash, byte count, returned range and ETag, and reproduced the exact bills/texts/actions column arrays from header-only decompression. No data row was parsed or inspected. The saved author declaration has **22 files**, confirming the discrepancy with the actual 26-member archive.

No material factual error was found in these directly retained acquisition claims. The public report correctly leaves corpus row counts, actual Congress coverage, text-body-versus-URL semantics, introduced-version completeness, full archive checksum and member CRC verification unresolved. Declared CRC values were compared, not validated against full members. A current archive timestamp cannot establish historical availability of any bill rendition. The retained MIT license covers the repository software; this review did not establish a separate archive-wide license for derivative/enrichment data and does not recommend redistribution on that basis.

One initial independent-verifier attempt stopped while reading the upstream dataset declaration because the verifier expected an ordinary Python assignment and the upstream file uses an annotated assignment. Correcting this verifier-only assumption allowed replay to complete; no source evidence was modified and no request was repeated. This was a reviewer tooling error, not an acquisition failure. The one-off probes use assertions and overwrite-capable output paths, so the recorded normal-Python execution is not a reusable fail-closed collector or an optimized-Python validation claim.

- Verified original [result manifest](../../../data/research-runs/historical-dataset-options-20261108/result.json), SHA-256 `df62938ef9d725ad489a990d41586ac4019fb8ee02f228535be2a7b91cf2d4e2`.
- New independent [verification record](../../../data/research-runs/historical-dataset-options-20261108/independent-review.json), SHA-256 `93ba19ee803f8c03f577e0f50806b387ae855a6974febd4bb8084937c8c36c61`.

These checks substantiate a concrete alternative acquisition route. They do not certify a prediction-ready corpus, resolve the original eight cases, or evaluate model performance.
