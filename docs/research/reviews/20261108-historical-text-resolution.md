# Historical text resolution: bounded official-source investigation

Date: 2026-11-08. Reviewer: agent_a.

This investigation did not recover older XML bytes or the missing historical checksum values for any of the eight audited bills. It found documented public retrieval of package content and metadata, but no historical internal-object-ID or as-of retrieval route in the inspected documentation. That is a bounded search result, not proof that GPO cannot provide the evidence. All eight cases remain unresolved and ineligible for historical-feature certification.

## Starting evidence and request boundary

The [retained PREMIS audit](20261108-historical-text-eligibility-audit.md) establishes eight matching current XML checksums and eight current-rendition creation events in January 2023, after historical cutoffs. It also identifies sixteen older XML objects whose retained object descriptions lack checksum values. Prior sealed audit hash: `4f8db6a2506056554f9220a641e9ffc2264d01565335d3bf4022fb4dd4d0a178`.

Eight page requests were made through the web tool, covering six distinct official URLs. Two were continuation opens of pages whose initial excerpts did not expose their substantive text. The requests returned extracted page content; the tool did not supply original HTML bytes or HTTP response headers/status codes. The preserved receipts are tool responses, not raw HTTP captures. No API request or archived-text retrieval was attempted, and no failed endpoint or 404 is claimed.

## Exact attempted URLs and results

| Request | Exact URL | Observed result |
|---|---|---|
| 1 | [https://www.govinfo.gov/developers](https://www.govinfo.gov/developers) | Developer hub returned; API, bulk XML, RSS and sitemap routes documented. |
| 2 | [https://www.govinfo.gov/help/bills](https://www.govinfo.gov/help/bills) | Bill help returned; legislative versions and bulk XML documented. |
| 3 | [https://www.govinfo.gov/about/authentication](https://www.govinfo.gov/about/authentication) | Authentication documentation returned; PDF signatures and reprocessing discussed. |
| 4 | [https://github.com/usgpo/api](https://github.com/usgpo/api) | Official GPO API README returned; package/granule retrieval and date-filter semantics documented. |
| 5 | [https://www.govinfo.gov/about/digital-preservation](https://www.govinfo.gov/about/digital-preservation) | Preservation page returned; initial excerpt insufficient for detailed assessment. |
| 6 | [https://www.govinfo.gov/developers/system-design](https://www.govinfo.gov/developers/system-design) | System-design index returned; initial excerpt insufficient for detailed assessment. |
| 7 | [https://www.govinfo.gov/about/digital-preservation](https://www.govinfo.gov/about/digital-preservation) | Continuation at line40 returned preservation/fixity policy details. |
| 8 | [https://www.govinfo.gov/developers/system-design](https://www.govinfo.gov/developers/system-design) | Continuation at line40 returned architecture/requirements document index. |

## What the documentation resolves

The [Developer Hub](https://www.govinfo.gov/developers) identifies package APIs and bulk congressional bill XML. It also says notifications may be suppressed during large reprocessing operations. Consequently, an absent RSS update would not establish unchanged bytes. The [bill help page](https://www.govinfo.gov/help/bills) describes published legislative versions. An introduced-versus-enrolled version distinction does not establish preservation versions of the same introduced XML.

The [official GPO API README](https://github.com/usgpo/api) documents package and granule retrieval. Package summaries provide available format links, including XML, MODS, PREMIS and ZIP. Its collection date filter tracks the package's add/update time; the published service filters issuance dates. Neither documented filter returns an as-of snapshot. “Versioning” concerns the API interface. I found no documented input for the internal `D…` file or `R…` rendition IDs in this README. This does not rule out an undocumented or separately documented export. The API supports a public `DEMO_KEY`; no private credential was sought or used. A package-summary call would be a next retrieval test, not historical proof by itself.

The [preservation page](https://www.govinfo.gov/about/digital-preservation) documents multiple archival copies, preservation metadata and file fixity checks. This supports pursuing an archival export, but supplies none of the missing object-level checksums. The [system-design index](https://www.govinfo.gov/developers/system-design) links a July 2023 architecture PDF and a preservation white paper. Those linked documents were not fetched within this request cap; the index warns its design materials are informational and can change.

The [authentication page](https://www.govinfo.gov/about/authentication) explains PDF signature verification and warns that extracted text does not retain the signature. It also anticipates reprocessing PDFs with newer signatures. A current authenticated PDF therefore cannot automatically establish the historical XML bytes; a historical signed PDF could be separate evidence only after checking its dated signature and the relevant text relationship. No PDF was acquired or signature validated here.

## Concrete unresolved object requests

These are identifiers from the retained PREMIS, not guessed network endpoints. No claim is made that the second identifier in each row was a publicly available rendition: that mapping must itself be established.

| Bill | Older XML object 1 | Older XML object 2 |
|---|---|---|
| 113-hr3884 | `D09002ee186e098b4` | `D09002ee186e0b015` |
| 113-hr4267 | `D09002ee187ff44ba` | `D09002ee188028f4f` |
| 114-hr2776 | `D09002ee18cb21906` | `D09002ee18cb2247d` |
| 114-hr2447 | `D09002ee18c7db45c` | `D09002ee18c7dd2e7` |
| 115-hr4997 | `D09002ee1987f3892` | `D09002ee1987f47e3` |
| 115-s2712 | `D09002ee19a242cd1` | `D09002ee19a244023` |
| 116-s2862 | `D09002ee1a3cbb1d5` | `D09002ee1a3cbb595` |
| 116-s843 | `D09002ee1a03cf96e` | `D09002ee1a03d0a0f` |

To resolve a case, obtain the historical object bytes and stored digest, an authoritative mapping to the introduced public rendition before its cutoff, and enough version/transform history to compare with the current file. An equal digest would support byte identity; a different digest requires preserving both objects and a separate declared text-comparison procedure. Preservation lineage alone does not supply equality.

## Next bounded action

A further authorized request batch should first inspect the already-linked architecture/preservation documents for an export procedure and test one audited-package API summary with the documented public demo key. Only an explicit historical route or archival export should trigger old-object retrieval. If this requires nonpublic credentials or communication with GPO, stop and ask the coordinating agent before proceeding. No message, signup, credential lookup or fee occurred in this investigation.

The request cap has been reached; no additional access was attempted. The absence of a confirmed route in six pages is insufficient to declare the evidence irretrievable. None of the sixteen historical checksum values, eight pre-cutoff public-access mappings or eight historical XML comparisons was resolved.

## Preserved receipt

`data/research-runs/historical-text-resolution-20261108-v1/web-tool-responses.json` preserves the three tool batches. `resolution.json` binds their SHA-256, request ledger, prior audit, eight case identities and unresolved requirements. Its sealed body hash is `8ee0b731440a4a72bc133ab3839a58b945c926b4d7e8a4ad4d8e0024cf6f3da3`.

No original source, model, annotation, eligibility gate or acquisition code was changed. Historical identities established: **0/8**. Human certification and historical-feature eligibility remain false.
