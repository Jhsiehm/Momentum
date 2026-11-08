# Independent bill-context source audit — November 8, 2026

Reviewer: `context_source_audit`, an AI agent. Scope: the existing `data/research-runs/bill-context-20261108-v1` preparation run. This is machine verification and design-case inspection, not qualified human certification, an adjudicated measurement study, or independent predictive validation. No source acquisition, fitting, scoring, frozen-artifact changes, quality XML parsing, or outcome-label inspection was performed. Quality bytes were read only to calculate hashes/lengths. All runtime artifacts remained read-only.

## Verdict

The retained pilot is internally consistent for evidence preparation. All 100 introduced-text downloads match their receipts and hashes; 326 retained source references resolve with matching hashes and lengths. The recorded 50 design and 50 quality cases have 10 of each partition per Congress 113–117 and 100 distinct recorded families. These are provisional family IDs, not verified genealogies. All 100 new text retrievals occurred after their historical prediction checkpoints. Thus no historical feature eligibility is certified by this audit.

The 50 design records reproduce their saved extraction exactly, retain 213 sections and 1,105 lexical candidate spans, and appear verbatim in their review pages. Raw XML remains intact. All mechanism values remain unknown, all annotation queue assignments and labels remain null, and historical eligibility is false. Quality records contain no design extraction, and no quality review pages were exported. These observations demonstrate a software firewall, not independent access custody or proof that nobody previously saw these public bills.

## Actionable findings

1. **Word boundaries are not preserved in the parsed reading/feature view (medium).** `parse_design` uses `''.join(tree.itertext())`, which preserves the sequence of text-node characters but removes element boundaries. Across design sources there are 992 adjacent text-node pairs ending and starting with alphanumeric characters; some are legitimate inline joins, but others visibly merge separate headings/body blocks. For example, 113-hr4401 contains `Short titleThis Act may be cited as the ` and `In generalSection 205(j)(1)`. The current replay test verifies the same concatenation and cannot detect this semantic rendering defect. Keep the existing immutable extraction as evidence, but create a separately versioned boundary-aware reading/tokenization view with markup-aware block separators and source-offset mapping. Do not blindly insert spaces at every inline boundary. Freeze that view on design cases before quality extraction or text-feature use. This does not establish lost raw source information: the XML remains authoritative.
2. **Congress identity validation uses a prefix instead of an exact parsed number (medium).** The condition `congress.startswith(c)` accepts a synthetic document declaring `1130th CONGRESS` for requested `113-hr1`. A local synthetic reproduction confirmed acceptance. Parse the integer and require exact equality, retaining strict chamber/number checks. Add wrong-Congress and malformed-form fixtures. Current design records reproduced successfully, but the defective guard provides weaker future protection than claimed. Quality XML identities are deliberately not certified here because their content was not parsed.
3. **Lexical hits are not legal-mechanism labels (known limitation, correctly marked).** Design 114-hr668 includes “do not authorize the designation, appointment, or employment”; 114-hr5053 includes “the Secretary may not require the name, address, or other identifying information”. Affirmative keyword flags would invert meaning here. The existing implementation appropriately leaves mechanism labels null and warns that negation/cross-references require review. Maintain that separation in any agent-generated interpretations; agreement among agents is not an independent reference standard.
4. **Existing generic verifier is not suitable for a strictly label-blind source reviewer.** `verify_bill_context_execution.verify()` calls `load_rows()`, which loads the underlying population containing outcomes, even though its reported work is largely software checking. This audit instead used a custom sealed-record/source-only path. Future review tooling should declare exactly which files/content it reads and provide a source-only entry point. This is an access-scope limitation, not evidence that outcomes influenced this audit.

## Code reviewed and verification scope

Read `AGENTS.md`, the controlling experiment plan and annotation guide; `scripts/bill_context_execution.py`, `scripts/bill_context_review_handoff.py`, `scripts/verify_bill_context_execution.py`, `scripts/paper_review_packet.py`, `engine/bill_context.py`; the `Sources` cache implementation in `engine/cohort.py`; and execution unit tests. The acquisition runner and handoff are fail-closed about human approval and model execution. Source URL selection requires a unique introduced `ih`/`is` XML rendition linked by retained MODS. The audit checked that link for all 100 records without parsing quality bill XML.

A custom Python source-only replay completed with exit code 0: it unsealed registration, source packet, every selected record and annotation queue; checked selection/record identities and partitions, distinct recorded families, source URL/MODS linkage, all referenced raw and receipt hashes, all 100 new raw hashes/lengths/receipt equality, pending eligibility/annotations, full design parser equality and handoff text, and quality export absence. Results were 326 source references/326 distinct retained source paths, 100 downloads, 100 post-cutoff retrievals, 213 sections, 1,105 lexical hits, and no quality parsing/outcome inspection. No whole-repository test pass is claimed by this audit.

The following smaller reproduction independently covers the two actionable parser findings and design-source integrity without opening quality content or labels:

```sh
python3 - <<'PY'
import hashlib, json
import xml.etree.ElementTree as ET
from pathlib import Path
from engine.paper_evaluation import unseal
from scripts.bill_context_execution import parse_design
p = Path('data/research-runs/bill-context-20261108-v1')
spec = unseal(json.loads((p/'registration.json').read_text()))
fusions = cases = 0
for entry in spec['selection']:
    if entry['partition'] != 'design':
        continue
    r = unseal(json.loads((p/'records'/(entry['bill_id']+'.json')).read_text()))
    key = hashlib.sha256(r['source']['url'].encode()).hexdigest()
    raw = (p/'sources'/(key+'.raw')).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == r['source']['sha256']
    assert parse_design(raw, entry['bill_id']) == r['design_extraction']
    parts = list(ET.fromstring(raw).itertext())
    fusions += sum(bool(a and b and a[-1].isalnum() and b[0].isalnum())
                   for a,b in zip(parts, parts[1:]))
    cases += 1
print('design_cases', cases, 'alphanumeric_boundaries', fusions)
fixture = b'<bill><form><congress>1130th CONGRESS</congress><legis-num>H.R.1</legis-num></form><section><text>Text.</text></section></bill>'
try:
    parse_design(fixture, '113-hr1')
    print('DEFECT: prefix Congress 1130 accepted as 113')
except ValueError:
    print('Congress mismatch rejected')
PY
```

Observed before any repair: `design_cases 50 alphanumeric_boundaries 992` and `DEFECT: prefix Congress 1130 accepted as 113`. The 992 count is a diagnostic of potential joins, not a count of independently adjudicated semantic errors. A subsequent parser repair must retain the original registration/code identity and use a new version rather than mutate the sealed run.

## Limits and recommendation

Official hosting and valid hashes establish retained bytes and source linkage, not their historical byte identity or first-public-availability timestamp. This audit cannot certify quality identities, mechanism precision/recall, complete family genealogy, outcomes, positive-family floors, or prospective validity. Agent cross-audits can identify errors and improve packets; they must be recorded as agent reviews, not backfilled as human signatures. Continue design-only fixes and independent machine review with the quality firewall intact. Preserve the existing run and all negative/blocked findings.

## Cross-audit of the methods agent

Reviewed [the methods report](20261108-context-methods-audit.md) against the controlling plan and inspected implementation on November 8, 2026. Its source counts, partition counts, section count and noncertification conclusion agree with this audit's separate source-only checks. I did not rerun its population-label checks or independently certify its reported positive counts; those belong to the methods audit's explicitly disclosed label-aware scope. Reading its aggregate count table is not an independent verification of underlying labels.

The E6 comparability finding is substantiated: the plan simultaneously forbids comparing differently restricted populations and proposes ranking more than four blocks by matched relative gain, without requiring identical populations at that screening step. A later common-population E6 run does not repair the earlier score-based selection rule. A score-independent fixed block priority is the least invasive bounded solution and must be versioned before scores.

The positive-family-floor ambiguity is also accurately stated, and the report does not exploit aggregate counts to bypass it. Defining the applicable population before registration is necessary; agent review cannot grant a post-hoc exception. Its reusable-verifier finding is corroborated by code inspection: formula/disjoint-ID checks alone do not independently prove original row-vector equality, chronology or global-family separation. The report honestly distinguishes its additional replay checks from the narrower existing verifier.

No unsupported claim of scientific success or human approval was found in the methods report. Its permission to create provisional machine annotations should continue to preserve the design/quality firewall and distinguish machine disagreement resolution from the protocol's qualified human adjudication. Cross-audit agreement is corroboration of specific inspected claims, not an independent quality reference standard or permission to fit blocked experiments.

## Review of the separately versioned design renderer

After the initial findings, the root agent added `scripts/bill_context_design_text_v2.py` and its focused tests, leaving the registered v1 runner and records intact. I independently inspected both files and exercised `render()` on all 50 design XMLs only. The new identity guard parses and exactly compares the Congress number. Newline insertion at named structural boundaries repairs the demonstrated heading/body fusion; inline text and tails remain continuous. Every design rendering preserved the exact original sequence of non-whitespace characters. This is a useful losslessness invariant, not a legal-meaning certification.

I examined every design `<text>` parent: paragraph 739, subparagraph 449, subsection 295, clause 226, section 114, subclause 74, item 21, and quoted-block 1. No design `<text>` appeared within an inline emphasis/span element, so I found no observed context-sensitive word split caused by treating this tag as a boundary in these 50 cases. Unknown markup and future schemas remain a limitation; this result does not authorize quality extraction or guarantee all legislative XML behaves alike. The separate view accurately declares that its offsets differ from both raw XML byte offsets and v1 concatenation offsets.

Ran `python3 -m unittest tests.test_bill_context_design_text_v2 -v`: all 3 tests passed, covering exact identity rejection, inline continuity/negation/Unicode, nested section ranges, and forbidden entities. The 50-case local replay also completed successfully. No additional code edits were needed from this reviewer, and no quality files were parsed. The new renderer is a design aid, not a frozen accepted extractor or a historical-eligibility approval.

## Final handoff exporter re-review

Reviewed the revised `scripts/bill_context_review_handoff.py` source-only verification and manifest implementation. An initial re-review identified missing discovery-source validation and missing pinned metadata-receipt hashes. Root repaired both before the final export. The exporter now validates design record identity/status, retained discovery/version metadata, each pinned metadata receipt, selected rendition identity, downloaded XML hash/length/receipt, and original text equality; it renders only design text through v2. It binds the renderer, guide and exporter hashes and all generated Markdown page hashes in a sealed manifest. This does not certify historical availability.

Executed the exporter first to the new `context-peer-audit-20261108/review-design-v2` directory, retaining that intermediate export, then after the receipt-chain repair to the separate final directory:

```sh
python3 -m scripts.bill_context_review_handoff \
  data/research-runs/bill-context-20261108-v1 \
  --export-directory data/research-runs/context-peer-audit-20261108/review-design-v3
```

Both executions returned successfully. Independent manifest checks verified exactly 50 design bill pages plus `START_HERE.md`, all 51 page SHA-256 values, exactly the registered design IDs, no quality pages, zero approvals, and no unexpected export files. The final manifest's `quality_content_exported` is false. The intermediate export also directly verified current exporter/renderer/guide hashes and the repaired `Short title`/body boundary in 113-hr4401.

A before/after SHA-256 map of **all 359 original pilot files** was identical around each export. Quality bytes were included only in preservation hashing/copying, never parsed or interpreted. Temporary-copy negative probes then separately altered a sealed design record's bill identity and altered a pinned discovery receipt by appending a newline while retaining its original expected hash. Both exports rejected the mutations, respectively with `Review record identity/status mismatch` and `Pinned metadata receipt changed`. The temporary probes were cleaned up; original records and sources were unchanged. No code modifications were made by this reviewer. These are reproducible software checks, not human certification or model-performance evidence.
