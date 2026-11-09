# Historical object evidence request v1

Date: 2026-11-08. **Local draft for review; not sent.** Intended recipient role: the GovInfo preservation or repository custodian able to identify historical BILLS objects. No external contact has been made through this document. This request does not change any Momentum eligibility gate.

## Purpose and bounded evidence gap

Momentum needs to determine which exact introduced-bill XML rendition was publicly available before each historical forecast cutoff. We are requesting preservation evidence for the eight packages and sixteen older XML object identifiers below—not the latest XML download alone.

The initial sealed audit found that all eight downloaded XML files match their named current PREMIS objects, but the associated access renditions were created in January 2023, after these cutoffs. The older XML object descriptions omit digest values. This does not establish that legislative meaning changed.

A separately registered follow-up completed sixteen requests: one current public PREMIS refresh and one public ZIP for each package. All returned HTTP 200 and parsed; all eight ZIP XML members matched the already retained current XML. No digest values were recovered for the sixteen older identifiers, so none of the eight historical identities became eligible. The two registered public routes are exhausted for this fixed study; this is not a claim that every possible recovery route has been exhausted or that historical objects do not exist.

## Exact cases to resolve

Cutoffs are copied verbatim from the sealed prior audit. They are UTC forecast boundaries, not alleged release dates. The two identifiers per package are preserved in source order; neither is assumed to be the historical public-access rendition.

| Bill | Package / legislative version | Historical cutoff (UTC) | Older XML object A | Older XML object B |
|---|---|---|---|---|
| 113-hr3884 | `BILLS-113hr3884ih` | 2014-07-14T23:59:59Z | `D09002ee186e098b4` | `D09002ee186e0b015` |
| 113-hr4267 | `BILLS-113hr4267ih` | 2014-09-10T23:59:59Z | `D09002ee187ff44ba` | `D09002ee188028f4f` |
| 114-hr2776 | `BILLS-114hr2776ih` | 2015-12-12T23:59:59Z | `D09002ee18cb21906` | `D09002ee18cb2247d` |
| 114-hr2447 | `BILLS-114hr2447ih` | 2015-11-15T23:59:59Z | `D09002ee18c7db45c` | `D09002ee18c7dd2e7` |
| 115-hr4997 | `BILLS-115hr4997ih` | 2018-08-12T23:59:59Z | `D09002ee1987f3892` | `D09002ee1987f47e3` |
| 115-s2712 | `BILLS-115s2712is` | 2018-10-16T23:59:59Z | `D09002ee19a242cd1` | `D09002ee19a244023` |
| 116-s2862 | `BILLS-116s2862is` | 2020-05-12T23:59:59Z | `D09002ee1a3cbb1d5` | `D09002ee1a3cbb595` |
| 116-s843 | `BILLS-116s843is` | 2019-09-10T23:59:59Z | `D09002ee1a03cf96e` | `D09002ee1a03d0a0f` |

## Four questions for the custodian

1. **Can the original bytes and recorded fixity be supplied for each listed object?** Please provide the checksum algorithm and stored digest value, byte length, format/encoding, originating package and rendition identifiers, and the dated creation/submission and fixity-event records. Preserve original bytes without reserialization. If bytes cannot be exported, please distinguish unavailable, deleted, access-restricted and not located, and provide the original digest/event evidence if possible.
2. **Which object and rendition were publicly accessible before the listed cutoff?** Please identify the public URL and access rendition, the earliest supported public-release timestamp with timezone, any embargo or withdrawal interval, and the record supporting that timing. Please distinguish archival ingestion from public release. If neither older object was publicly served, identify the actual served object and its relationship to these objects.
3. **How is that historical rendition related to the currently served XML?** Please provide the source and destination object/rendition identifiers and digests for any reprocessing or transformation, event timestamps, software/transformation version or stylesheet when retained, and a statement of which bytes or content changed. A general statement that a package was reprocessed cannot establish byte identity. If unchanged legislative content is asserted despite differing bytes, please specify the supported scope of that assertion and the evidence or reproducible transformation.
4. **What is the authoritative way to verify or retrieve this evidence again?** Please provide a public retrieval route if one exists, an archival export manifest or durable record identifier otherwise, the custodian's scope of authority, and any restrictions or unresolved uncertainty. A partial response is useful; please state explicitly which objects, dates or links remain unsupported.

A useful response is one row per object, with associated files or record references: package; object ID; rendition ID; original filename; byte length; algorithm; digest; creation time; first supported public-release time; public URL; supporting event/record IDs; transformation parent; export timestamp; unresolved limitations. Please keep historical event timestamps separate from the time this evidence is exported.

## Verification after a response

Retain the response and its actual receipt time in ignored runtime storage. Hash original response attachments and historical bytes, verify stated fixity, and check every object-to-rendition-to-publication link against the cutoff. Compare bytes with current XML separately. Do not replace a failed byte-identity check with an undeclared normalization or semantic-equivalence claim. Register any rendering-equivalence test separately with frozen transformations and explicit limitations. Independent review must precede any eligibility decision; this request itself certifies zero cases. Evidence for these eight cannot certify the remaining corpus.

## Alternative: prospective capture without backdating

If historical recovery remains unresolved, a prospective branch can begin with a separately registered acquisition and evaluation policy. Preserve each actually retrieved official rendition as immutable raw bytes with retrieval time in UTC, requested and final URL, HTTP status and relevant headers, bill/package/version identity, byte length, SHA-256, parser version and any accompanying metadata. Preserve subsequent revisions as new records; never overwrite the first capture. Record failed requests and scheduled polling intervals, because the earliest observed successful retrieval bounds what was known to this system; it does not establish the first public release instant.

Only make a forecast from evidence captured before its frozen prediction time, with an explicit outcome horizon and at-risk check. Seal input-manifest hashes, model/preprocessing versions, training-label cutoff and forecast probabilities before later outcomes are observed. Score only matured outcomes under the registered policy. Use only training-partition data to fit preprocessing and model parameters; freeze calibration and promotion rules before evaluation. Record labels and corrections as new versions. This route produces new prospective evidence as time elapses; it neither repairs old cutoffs nor licenses historical backtests using newly retrieved bytes.

## Local evidence and reproducibility

- [Initial source audit](reviews/20261108-historical-text-eligibility-audit.md).
- [Documented public retrieval routes](reviews/20261108-historical-source-routes.md).
- Sealed prior audit: `data/research-runs/historical-text-eligibility-20261108-v1/audit.json`, body hash `4f8db6a2506056554f9220a641e9ffc2264d01565335d3bf4022fb4dd4d0a178`.
- Follow-up registration: `data/research-runs/historical-source-feasibility-v1-20261108/registration.json`, hash `6092a2a78fa2be4b33de987b0ca62479dff8dd038087ebbfff5b115d1fa32f81`.
- Follow-up result: `data/research-runs/historical-source-feasibility-v1-20261108/result.json`, body hash `3f8c28344464b49319aa01d915caccca569a15b4e0404aed8a766ac08ea59076`.

The case table was generated from the verified sealed prior audit and checked against all eight follow-up result records, including exact cutoff strings and both object IDs per case. No model fitting or predictive evaluation was performed by this request preparation.
