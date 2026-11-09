# Historical source recovery: documented routes

Date: 2026-11-08. Scope: primary-source documentation review before the fixed eight-bill feasibility requests. No bill-specific content was fetched for this review. No model was fitted or tested. This review does not certify historical eligibility.

## Finding

The documented public services support a bounded comparison of current package metadata, ZIP members and bulk XML. I found no documented public endpoint that retrieves an older internal AIP/ACP object by its preservation identifier. This is a search result and limitation, not proof that recovery is impossible.

The decisive distinction is between a legislative version (for example, introduced versus enrolled) and an earlier digital rendition of that same legislative version. GovInfo's bill help documents published legislative versions and version-bearing package IDs; that does not establish unchanged XML bytes since publication. Its definitions also distinguish publication from ingestion. [Congressional Bills help](https://www.govinfo.gov/help/bills).

## Routes suitable for preregistration

| Route | Documented basis | Interpretation |
|---|---|---|
| `https://www.govinfo.gov/content/pkg/{packageId}.zip` | GPO's transition guide explicitly gives `https://www.govinfo.gov/content/pkg/BILLS-115s3021enr.zip` and directs developers to construct package links. | Public package ZIP; no documented historical object selector. |
| `https://api.govinfo.gov/packages/{packageId}/summary`, then its `premisLink`, `xmlLink` or `zipLink` | GPO API package documentation lists these downloads. | Alternate discovery/retrieval route; requires an API key. |
| Existing official bulk XML URL, or links obtained from the documented bulk JSON/XML listing | GPO documents bulk bill XML and listing endpoints. | Another present-day rendition to compare; not automatically a historical snapshot. |

The public ZIP pattern is directly supported by the [official GPO transition guide](https://github.com/usgpo/api/wiki/Transition-Guide), under “govinfo BILLS Sitemaps.” The guide concerns current added/updated material. The [API documentation](https://github.com/usgpo/api) describes a possible ZIP-generation HTTP 503 with `Retry-After`; register any retry budget in advance. Bulk listings accept `/json` or `/xml` after `/bulkdata`; JSON callers should set an appropriate Accept header. [GPO bulk-data documentation](https://github.com/usgpo/bulk-data).

GovInfo's [API introduction](https://www.govinfo.gov/features/api) describes ZIP contents as content renditions plus DIP/METS, MODS and PREMIS. PREMIS includes preservation-event and fixity information. Therefore ZIP member inspection is a documented route to a manifest and checksums, although any particular bill's available members must be measured, not assumed.

## Why preservation records alone are insufficient

The [GovInfo architecture, July 2023](https://www.govinfo.gov/media/GovInfo_Architecture_v7.pdf), section 7.2, describes creation of an AIP with hashes and timestamps, a separate ACP for access processing, and a public cache containing a subset of ACP objects. It states that ACP storage is accessible only to authorized users. Some access additions may not enter the AIP. This supports keeping archive identity, public rendition identity and public availability as separate checks; it provides no public historical-object download syntax.

As a collection-specific caution, [Statute Compilations help](https://www.govinfo.gov/help/comps) explicitly distinguishes the latest downloadable compilation from earlier versions retained in preservation. Do not generalize that collection's access policy to BILLS. It illustrates why retention is not equivalent to public retrieval.

## Recommended fixed study and stopping rule

Reuse the same eight already audited package IDs. Refresh their already-known official PREMIS URLs, download each documented public ZIP, and compare the existing bulk XML or a preregistered current bulk refresh. Count every attempt, redirect and retry under the root registration's budget. Inspect ZIP members without executing or extracting arbitrary paths.

For every content member, record package/version identity, byte size, SHA-256 and any algorithm needed to compare declared fixity. Preserve the specific PREMIS object/event association and timestamp. A hash equality supports byte identity with that object; it does not by itself establish that the object was publicly available before the forecast cutoff. A package-level old event cannot date every later rendition.

If no member matches a dated, relevant historical object with adequate availability evidence, report unresolved eligibility for that case. Do not widen the sample, invent archival URLs, silently relax the gate, or infer historical eligibility from a current URL, HTTP Last-Modified, filename, publication date or successful download. Stop the acquisition branch and record the evidence gap before considering a separately approved retrieval approach.
