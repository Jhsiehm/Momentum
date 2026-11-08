# Historical text resolution: architecture and public-package follow-up

Date: 2026-11-08. Reviewer: rubric_v2_methods. Scope: the same eight cases as the [first investigation](20261108-historical-text-resolution.md); no quality-case texts.

**Historical identities established remain 0/8.** Six official-source HTTP requests returned 200. The follow-up recovered architecture documentation and a public package ZIP, but no older XML bytes or missing historical checksums. Historical-feature eligibility and human certification remain false. This bounded result does not establish that GPO cannot supply an archival export.

## Actual HTTP evidence

Unlike the prior page-excerpt investigation, these requests used HTTP retrieval and retained the complete response bytes, response headers/status, retrieval timestamps and SHA-256 hashes. The cap was eight; six requests were used, with no undocumented endpoint guesses or additional requests. PDF text extraction was local using pypdf 6.14.2; extracted text is an aid to reading, not authenticated historical bill evidence.

| Request | Official URL | Observed response |
| --- | --- | --- |
| 1 | [System design](https://www.govinfo.gov/developers/system-design) | 200 HTML; links to architecture and preservation PDFs |
| 2 | [Digital preservation](https://www.govinfo.gov/about/digital-preservation) | 200 HTML; preservation-document links |
| 3 | [113-hr3884 introduced package summary](https://api.govinfo.gov/packages/BILLS-113hr3884ih/summary?api_key=DEMO_KEY) | 200 JSON, 3,993 bytes; current format links |
| 4 | [Architecture v7](https://www.govinfo.gov/media/GovInfo_Architecture_v7.pdf) | 200 PDF, 2,595,865 bytes, 101 PDF pages |
| 5 | [Preservation white paper](https://www.govinfo.gov/media/preservation-white-paper_20080709.pdf) | 200 PDF, 91,113 bytes, 11 PDF pages |
| 6 | [113-hr3884 package ZIP](https://api.govinfo.gov/packages/BILLS-113hr3884ih/zip?api_key=DEMO_KEY) | 200 ZIP, 235,301 bytes; six entries |

Only the documented public `DEMO_KEY` was used. No private credential, signup, message, contact or fee was involved. These are new source-investigation requests, not corpus expansion or model evaluation.

## What the documents establish

The July 2023 architecture, section 7.2, describes assigning unique digital-object identifiers and calculating checksums during ingest. Section 7.5 distinguishes CMS Export for authorized users from public delivery through access packages. Sections 7.2–7.3 describe a public cache containing access renditions rather than routine public retrieval from archival storage. Section 8.5 explains that access packages can replace rendition files, record events in preservation metadata, and maintain archival and access rendition updates independently. These architectural descriptions explain why a lineage relation does not establish equal bytes. They do not provide a tested public lookup for the known historical D/R identifiers.

The July 2008 preservation white paper, printed pages 6–8, describes archival packages retaining normalized preservation and original submitted renditions, separate public access packages, and possible archival-package replication to partner repositories. These are preservation design descriptions, not evidence that a particular historical object is available now or that its bytes equal the current XML. No partner endpoint or archival export was discovered or tested.

## Actual package findings

The 113-hr3884 API summary identifies introduced version `ih`, issuance date `2014-01-15`, and `lastModified` `2025-03-07T14:09:12Z`. The issuance date dates the publication; it does not certify the downloaded bytes. The summary exposes package-level XML, HTML, PDF, MODS, PREMIS and ZIP links, without an historical-object/as-of retrieval parameter in this response.

The ZIP contains `dip.xml`, one bill XML, HTML, PDF, `premis.xml` and `mods.xml`. The bill XML is 9,871 bytes, SHA-256 `952b132b4ba4f80a05a6332074d272ddfb1a39a3f9f2a2ee64372ac4b95fd8fd`. No older bill XML files are included. The DIP manifest is dated `2026-10-15T05:56:58Z`; its format links point to the public package. This is a current dissemination package, not a recovered pre-cutoff snapshot.

The ZIP's PREMIS still describes `D09002ee186e098b4` as an FDsys ACP XML object and `D09002ee186e0b015` as an FDsys AIP XML object, but neither object description supplies fixity. Their presence in metadata does not recover their contents or certify historical public availability. No historical XML digest or byte comparison was established for this case; the other seven cases were not fetched again and remain unresolved under their prior evidence.

## Receipt and next evidence requirement

Ignored runtime directory: `data/research-runs/historical-text-resolution-20261108-v2/`. `http-ledger.json` records the six responses; `response-1.bin` through `response-6.bin` preserve their bytes; the PDF text extracts and `zip-inventory.json` provide reproducible inspection aids. `resolution.json` binds these files, request ledger, all eight case identities and the prior investigation. Sealed body hash: `6f0a45f3cdafe6ca70202aa6790539ffd2dc796f432a717a7cbe6d2c26509976`.

The remaining requirement is unchanged: actual older object bytes and stored fixity, authoritative mapping to a public introduced rendition before cutoff, and transformation/version evidence sufficient for comparison. A documented public archival export or authorized custodian-supplied evidence could resolve this. Access-controlled CMS Export was described, not attempted. Existing gates, sources and frozen acquisition code were preserved; no model fitting, prediction scoring or certification occurred.
