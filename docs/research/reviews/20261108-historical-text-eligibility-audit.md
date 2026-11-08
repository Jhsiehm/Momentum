# Historical text eligibility: retained preservation metadata audit

Date: 2026-11-08. Reviewer: agent_a. No historical certification or eligibility gate change.

The eight audited current XML files match the SHA-256, byte size and exact public-access URL recorded in retained PREMIS. However, every matching XML rendition has a January 2023 creation event, after its historical cutoff. Earlier XML objects have dated checksum-calculation and successful fixity events, but their object descriptions omit the digest values. The retained evidence therefore verifies current rendition identity and historical package activity; it does not establish that current XML bytes were available at the historical cutoff. It also does not prove that the legislative text changed.

## Fixed scope and verification

The subset is the first two entries per Congress 113–116 in saved selection order from `mechanism-training-coverage-20261108-v2/registration.json`, registration hash `801dd51ca5cb3aad862e7b308fa3e91cf7192f2f9a605e29699b8a695bfd9af1`. Selection preceded metadata inspection. This is eight of the existing 200 cases, not a prevalence estimate for the corpus.

All 16 retained MODS/PREMIS files were parsed, and their receipt hashes and byte lengths verified. All eight existing current XML files were hashed without inspecting bill text; their hashes, sizes and URLs matched the named PREMIS XML objects. Metadata receipts date to November 5, 2026; current XML receipts date to November 8, 2026. No new source acquisition, quality text access, outcome inspection, fitting or gate modification occurred.

| Bill | MODS issued | Computed package availability | Historical cutoff | Matching XML rendition creation | XML bytes |
|---|---|---|---|---|---|
| 113-hr3884 | 2014-01-15 | 2014-01-19 | 2014-07-14 | 2023-01-07 | 9871 |
| 113-hr4267 | 2014-03-14 | 2014-03-22 | 2014-09-10 | 2023-01-06 | 2827 |
| 114-hr2776 | 2015-06-15 | 2015-06-20 | 2015-12-12 | 2023-01-06 | 3145 |
| 114-hr2447 | 2015-05-19 | 2015-05-29 | 2015-11-15 | 2023-01-06 | 8762 |
| 115-hr4997 | 2018-02-13 | 2018-02-18 | 2018-08-12 | 2023-01-03 | 177618 |
| 115-s2712 | 2018-04-19 | 2018-04-28 | 2018-10-16 | 2023-01-03 | 17261 |
| 116-s2862 | 2019-11-14 | 2019-11-23 | 2020-05-12 | 2023-01-01 | 7902 |
| 116-s843 | 2019-03-14 | 2019-04-04 | 2019-09-10 | 2023-01-02 | 7859 |

Availability is the existing conservative package-date calculation, not a rendition release timestamp. Creation dates above preserve the calendar date in PREMIS's explicit timezone; complete timestamps and event IDs are in the sealed audit.

## What the retained records actually contain

Each PREMIS file describes three `text/xml` file objects. The named current public-access object has SHA-256, size, filename, URL and a structural “is part of” link to a rendition identifier. The other two XML objects have identifiers and formats but no checksum value, size, public-access URL or structural mapping in their object descriptions. Successful older checksum/fixity event messages refer to those older identifiers and state that stored values matched, but do not reveal the values. Thus an old object's successful fixity check cannot be compared with the current downloaded hash.

For every current XML object, the structural rendition ID is explicitly linked to a successful `Rendition Creation` event in January 2023. Each event says a new rendition was created from an older rendition. Current object digest-calculation and format-identification events occur at the same time. All eight package histories also contain `Reprocessed for Access` events describing deletion and regeneration of derived renditions and reparsing. The only object-level relationship subtype present in these retained documents is `is part of`; no equality assertion binds the old XML bytes to the current XML bytes. A derivation event is useful lineage evidence, but cannot establish byte identity by itself.

For example, `113-hr3884` current XML object `D09002ee1ba618d5c` matches SHA-256 `952b132b4ba4f80a05a6332074d272ddfb1a39a3f9f2a2ee64372ac4b95fd8fd` and 9,871 bytes. It belongs to rendition `R0b002ee1ba618d4c`, created on `2023-01-07T00:57:39-05:00` in event `3c65a56c-1a4f-4722-ba7d-ad24f3d2e20b`. The older XML identifiers `D09002ee186e098b4` and `D09002ee186e0b015` have 2014 checksum events and subsequent fixity checks, but no digest values in their retained object descriptions. This is an observable break in the available byte-binding evidence, rather than a hypothetical concern about a current URL.

## Code interpretation

`engine/cohort.py:92` (`provenance`) verifies MODS package identity, issuance/ingestion dates and the earliest successful Ingestion, ACP Creation and Parsing events. It adds a one-day margin to the latest relevant calendar date. It does not follow object identifiers, inspect digest values or require the current rendition creation to precede the cutoff. Its returned basis explicitly disclaims byte-identical archived proof.

`scripts/mechanism_training_coverage.py` (`introduced_evidence`) replays the preserved metadata and checks package/chamber, dates, byte hashes of metadata and current XML URL identity. This correctly supports its stated metadata-dated-current-XML status. Passing those checks must not be interpreted as historical rendition certification. The code's false eligibility flag remains appropriate for all eight inspected cases.

## Concrete next requirements

1. Request or locate the historical XML/AIP or ACP object bytes and their recorded checksum values using the exact older object identifiers retained for each case in the audit. Establish which object was the publicly accessible introduced rendition before cutoff, with a dated public-access link. An early ingestion or archived object alone does not prove public availability.
2. Verify the archived bytes against the recovered checksum, then compare them with the current XML hash. If hashes differ, preserve both versions and separately test whether the rendered legislative text is unchanged under a declared, frozen transformation. Do not silently replace byte identity with semantic equivalence.
3. If only the derived January 2023 rendition is obtainable, obtain official version/transformation evidence that binds its input to the historical object, including the actual historical digest and transformation details. The present event descriptions and structural membership links are insufficient for that binding.
4. Before proposing any eligibility change, implement a separate evidence check for the full object/representation/date/fixity chain, record unresolved cases explicitly and independently review the proposed standard. Repeat it per case across the corpus; eight examples cannot certify the remaining cases.

No historical identity was established in this audit: 0/8. This count expresses the available evidence, not a finding of changed legislative meaning. No source or existing immutable artifact was modified.

## Reproducible evidence receipt

Runtime artifact: `data/research-runs/historical-text-eligibility-20261108-v1/audit.json`.

Sealed body hash: `4f8db6a2506056554f9220a641e9ffc2264d01565335d3bf4022fb4dd4d0a178`.

The artifact retains each metadata path, source URL, retrieval time, SHA-256 and size; exact current-object and rendition-creation XML snippets with character offsets; all XML-linked event records, reprocessing events and event-type counts; full source-byte checksums; code hashes; selection rule; and explicit false certification/eligibility flags. The metadata supplies the official source URLs directly. The report can be checked without inspecting bill text or outcomes.
