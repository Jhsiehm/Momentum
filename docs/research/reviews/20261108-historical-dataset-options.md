# Historical dataset options and bounded acquisition — November 8, 2026

## Decision and scope

A usable public historical-data route exists: BICAM distributes a joined congressional corpus with bill, text, action and law tables. We verified the actual archive directory and three column headers, rather than treating a website description as data validation. This makes a **separately registered retrospective corpus audit** practical. It does **not** resolve the eight original historical-rendition cases or certify any as-of forecast feature. No model fitting, calibration, predictive scoring, protected local outcome reading, or per-bill content review occurred.

Historical learning is appropriate: outcomes of completed Congresses can label examples while features are restricted to the earlier prediction point. Having final outcomes is not leakage by itself; including final status, later text, final cosponsor counts or post-cutoff annotations among predictors is. A retrospective current-rendition study must remain clearly distinguished from an independently validated historical forecast.

## Sources and alternatives

| Route | Established evidence | Decision / limitation |
|---|---|---|
| [BICAM author repository](https://github.com/bicam-data/bicam), [bill archive page](https://bicam.net/category/bills/) | Author describes Congress.gov/GovInfo provenance. Current ZIP has 26 CSV members; actual bill/text/action headers verified below. | Best new alternate corpus for bounded inventory/schema audit; actual Congress coverage, counts, missingness, text-body availability and introduced-version semantics still need measurement. |
| [Official GPO Bill Status](https://github.com/usgpo/bill-status), [official BILLS bulk](https://www.govinfo.gov/bulkdata/BILLS) | GPO documents Bill Status starting with Congress 108; the current BILLS listing exposes Congresses 113–119. | Prefer official inventory for cohort enumeration and reconciliation. Presently downloaded introduced renditions are not automatically dated historical bytes. |
| [Nay 2017](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0176999) | Published study used nearly 70,000 bills, 2,513 enactments; temporal training/testing, introduced-versus-latest data, and text/context comparisons. Data statement points to GovTrack and MIT committee data. | Methodological precedent, not a newly verified immutable downloadable study corpus or proof of our source eligibility. |
| [BillSum authors' collection documentation](https://github.com/FiscalNote/BillSum/blob/master/BillSum_Data_Documentation.md) | Authors explicitly paired summaries with **final text versions**, because earlier summaries and version alignment were difficult. | Reject as an introduced-text forecast cohort. Useful summarization corpus cannot substitute for passage prediction data. |
| [Comparative Agendas U.S. datasets](https://comparativeagendas.net/project/us/datasets) / Congressional Bills Project | Primary project page advertises policy-coded bills and links to textual sources. | Legacy Congressional Bills download address redirected to unrelated gambling content during this review. No download or content execution from that destination; do not trust the old domain as a functioning scholarly data source. |
| [United States Congress collector](https://github.com/unitedstates/congress), [bill schema](https://github.com/unitedstates/congress/wiki/bills) | Public-domain/CC0 collection code and documented histories. Schema distinguishes bill identity, introduction, final status and actions. | Repository history versions collection code, not a complete bill-corpus snapshot. Documentation says update timestamps describe scraper saves; subjects/summaries may be added later. Old Statutes-only route selects enacted bills and cannot supply a representative negative class. |

BICAM's repository license is MIT for the software. We did not establish a separately stated archive-wide data license from the inspected files; official-source provenance alone does not establish rights for every derivative/enrichment table. Do not redistribute the archive or auxiliary lobbying data based solely on the software license.

## Preregistered bounded metadata checks

Discovery browsing preceded registration and is exploratory. Three separate local plans were sealed before their respective direct requests. Later plans are adaptive follow-ups, not retrospectively presented as an original single design. Each used zero retries, zero redirects and 20-second socket timeouts; these are not measured whole-run duration bounds.

1. Documentation plan allowed 12 metadata GETs, 2,000,000 bytes per response; executed five: author repository tree, pinned dataset documentation, pinned dataset declarations, pinned license, and bill webpage. All five HTTP 200.
2. Archive-directory plan allowed exactly a HEAD and a 65,536-byte suffix range request. Responses HTTP 200 and 206. No entire archive download.
3. Header plan allowed three 8,192-byte ranges, selected in advance for bills, texts and actions. Each response HTTP 206 with the same archive ETag; decompression capped at 65,536 bytes per member, only the first CSV header parsed. Raw compressed prefixes may include incidental bill bytes; no bill data rows were parsed or inspected.

Total direct requests: **10**; HTTP 200: **6**; HTTP 206: **4**; observed HTTP/transport/parsing failures: **0**. Saved response-body bytes: **148,573**. Discovery web requests are additional and are not included in these counts. Documentation browsing encountered one GitHub tree fetch restriction; direct author-tree metadata retrieval subsequently succeeded within the first plan.

### Actual archive evidence

- Public archive: `https://downloads.bicam.net/bills/bicam_bills.zip`.
- Advertised HTTP length: **1,936,532,215 bytes**; last modified April 15, 2025. This dates the current archive, not original bill availability.
- **26 entries** in central directory; 26 names below. No row count is established.
- Text member: **1,436,764,626 compressed / 6,591,284,872 uncompressed bytes** according to directory metadata. No full decompression or CRC verification.
- Website says approximately 2 GB and broad coverage from the sixth Congress; pinned package code says 1,847 MB and Congresses 93–118. Its documentation advertises different filenames and sizes. These inconsistencies mean actual coverage must be measured rather than assumed.
- Pinned author repository tree: `dbf37a8582a2f5453220727d2b37ac176c60c89e`. The code declares 22 files, while the downloaded directory actually has 26. A package-maintainer checksum exists but cannot be validated against our partial download.

Actual members: bills.csv; bills_actions.csv; bills_actions_committees.csv; bills_actions_recorded_votes.csv; bills_cbocostestimates.csv; bills_cosponsors.csv; bills_laws.csv; bills_lobbied.csv; bills_metadata.csv; bills_notes.csv; bills_notes_links.csv; bills_reference_codes.csv; bills_reference_codes_sections.csv; bills_reference_laws.csv; bills_reference_statutes.csv; bills_reference_statutes_pages.csv; bills_related_bills.csv; bills_sponsors.csv; bills_subjects.csv; bills_summaries.csv; bills_texts.csv; bills_titles.csv; ref_bill_summary_version_codes.csv; ref_bill_version_codes.csv; ref_title_type_codes.csv; crosswalk_bills_voteview.csv.

### Verified column headers

| Member | Columns |
|---|---|
| bills.csv | bill_id, bill_type, bill_number, congress, title, origin_chamber, current_chamber, version_code, introduced_at, constitutional_authority_statement, is_law, is_appropriation, is_private, policy_area, pages, actions_count, amendments_count, committees_count, cosponsors_count, summaries_count, subjects_count, titles_count, texts_count, updated_at |
| bills_texts.csv | bill_id, date, type, raw_text, formatted_text, pdf, xml |
| bills_actions.csv | action_id, bill_id, action_code, action_date, text, action_type, source_system, source_system_code, calendar, calendar_number |

The headers support a candidate bill-ID join and version/date selection, but do not establish whether `raw_text` holds bodies or URLs, or whether every bill has an introduced version. `is_law` belongs in an outcome-only partition. Current chamber, current version, final counts and unrestricted action histories cannot be assumed available at introduction/day 180.

## Concrete next acquisition and acceptance decisions

Use a separate retrospective audit registration, not a change to the frozen matched forecast experiment. Download only the bill identity table and version-code reference first (archive range retrieval can avoid the 1.4 GB compressed text member); obtain a frozen complete enumeration for selected **completed** Congresses and H.R./S. bills. Then a bounded deterministic sample, chosen by ID hash before reading labels, can establish text-body/URL semantics, introduced-version identity, duplicate/missing records and join multiplicity. Counts and exclusions must be measured before choosing a fitting population; do not select by enactment or only existing acquired texts.

If actual introduced text can be joined but as-of bytes remain unresolved, that enables an explicitly retrospective association diagnostic under a new protocol only. It cannot unlock, rewrite, or support promotion under the existing historically dated comparison. If introduced versions cannot be identified, reject this corpus for that task. Preserve the existing eight unresolved cases rather than replace them with easier examples.

Do not train on a handpicked balanced sample and present its accuracy as population performance. Use completed outcomes, earlier training and later testing, retain natural prevalence for scoring, isolate final outcomes, group related/reintroduced bills, and estimate uncertainty. No source option in this review independently establishes a 60% Brier-loss reduction.

## Runtime evidence and reproduction

Ignored runtime directory: `data/research-runs/historical-dataset-options-20261108/`. Files include the three plans, direct-request receipts, raw responses, partial compressed archive data, scripts, and result manifest. No private chat, credentials or downloaded corpus is committed.

- Documentation plan SHA-256: `6f73a5f4b777678c6aa22c713139dd838116e3249163c27f584a300387ceed25`.
- Archive-directory plan SHA-256: `fead53d4d50791e267f4c34daed0a0348facb1ac9b9a5392ed4ec5ec468efcb6`.
- Header plan SHA-256: `522322f0a428c35ae35bc04e34d514ea38b02bcc241c1d6ae5e4b761a6094593`.
- ZIP tail SHA-256: `8fa40bc106615a3243e505e6d44d8bd4a02119c957412880175ff71166d68a49`.

The result manifest hashes every request receipt, script and saved response. Inspection scripts are single-run research probes in ignored runtime, not an installed general collector. Reproduction should use a fresh output directory and new plans; do not overwrite evidence or rerun the current scripts against their existing receipt files. No unit tests were added for these one-off read-only probes, and no predictive metric or confidence interval was computed. Independent review is pending at this document's initial handoff.

[Result manifest](../../../data/research-runs/historical-dataset-options-20261108/result.json) SHA-256: `df62938ef9d725ad489a990d41586ac4019fb8ee02f228535be2a7b91cf2d4e2`. Exact URLs, headers, timestamps and all per-request hashes appear in [documentation requests](../../../data/research-runs/historical-dataset-options-20261108/requests.json), [archive result](../../../data/research-runs/historical-dataset-options-20261108/zip-result.json), and [header result](../../../data/research-runs/historical-dataset-options-20261108/headers-result.json). These links require retained local runtime evidence.
