# Independent agents and reciprocal bill-context audit

November 8, 2026. User explicitly requested agents independently review the work and audit each other. Three agents independently inspected the pilot, then challenged peers' findings and reviewed fixes. Their reports are machine audits, not human certification or independent predictive validation.

## Roles and reciprocal checks

| Agent | Initial independent work | Cross-audit / repair verification |
| --- | --- | --- |
| `context_source_audit` | Source-only audit: 100 XML downloads, 326 retained source references, design text/spans and quality firewall | Challenged methods interpretation; independently replayed v2 renderer on all 50 design bills; challenged exporter provenance and verified final repair |
| `context_methods_audit` | Pilot selection, all 28,433 calendar rows, exact original inputs, chronology, family partitions and protocol adequacy | Challenged code report; independently reproduced rejected split/eligibility mutations after repair; found unchecked section identifiers |
| `context_code_audit` | Verifier, runner, review exporter and negative mutation probes | Cross-audited source report; implemented verifier repairs after initial audit; methods agent independently reviewed those repairs |

Reports: [sources](../../research/reviews/20261108-context-source-audit.md), [methods](../../research/reviews/20261108-context-methods-audit.md), [software](../../research/reviews/20261108-context-code-audit.md). Implementation ownership after audit is disclosed: the code agent did not independently certify its own repair. Reports distinguish independently reproduced claims from peer-reported results.

## Findings and disposition

1. **Verifier bypasses confirmed on disposable copies.** Rehashed incorrect identities, swapped core/calibration IDs and false release claims were accepted by the original verifier; optimized Python removed its assertions. Fixed with explicit exceptions and authoritative record/source/legacy membership/control-vector/annotation/stage bindings. Independent methods replay rejected the repaired split and release mutations. A further section-index/XML-ID gap found by that reviewer was fixed and regression-tested.
2. **Reading-view boundaries and identity guard.** Original text-node concatenation can fuse headings with body text, and original prefix matching accepts synthetic Congress 1130 for 113. Original raw XML is intact. Added a separately versioned renderer with exact Congress identity, block separators, preserved inline text/tails and per-element view offsets. Replayed all 50 design sources; nonwhitespace content preserved. Original registered runner and its outputs remain unchanged for reproducibility. It remains a legacy v1 implementation; use the reviewed renderer and strict verifier for subsequent preparation, with new registrations required before modeling.
3. **Review-export provenance.** Added source-only checks of identity, original text, exact introduced rendition, raw bytes and metadata receipt hashes, including discovery evidence. Export manifests now hash every page, renderer, exporter and guide. Source peer review caught omitted pinned receipts in the first revision; final revision includes them. Wrong-identity and altered-receipt probes reject. The final export has50 design pages plus index,51 verified hashes, zero quality pages and zero approvals. Intermediate exports remain preserved separately.
4. **Methods limitations remain real.** E6 ranking across different restricted samples is not comparable. A [separate methods clarification](../../research/BILL_CONTEXT_METHODS_CLARIFICATION_V1.md) blocks selection until a common-population comparison and allocation are registered, without changing the hashed plan or adding fits. Raw positive counts would fail multiple per-fold 200/100 gates; applicable population scope and actual reviewed counts remain unresolved. Agents cannot infer an exception.

## Artifacts and validation

New ignored audit directory: `data/research-runs/context-peer-audit-20261108/`. Original pilot: `data/research-runs/bill-context-20261108-v1/`.

- Before/after hashes confirm **all 359 original pilot files unchanged**, plus the frozen model/training/prior-result audit unchanged. Preservation receipt digest: `6255cd1f1aa1aa45d864b4c4f2e12d6657a0954b00626a690712522eebfd1df4`.
- Separate design-view manifest digest: `2c8c890dadc07f9790998838682c10ae7a183c8523aa7a8292953321d795d60f`.
- Final readable export: `data/research-runs/context-peer-audit-20261108/review-design-v3/START_HERE.md`. Its manifest records exact output and implementation hashes; previous pilot pages remain untouched.
- Full regression suite: **318 tests passed in 77.310 seconds** (`python3 -m unittest discover -s tests -q`). Diff whitespace checks passed.
- Three deterministic renderer tests passed. Eight real-corpus verifier integration cases exercise positive replay and corruption/optimized-mode rejection. The integration cases explicitly skip when the ignored corpus is absent from a clean checkout; this is not public reproduction of the corpus from Git alone.
- Source auditor independently checked all final export hashes and two negative handoff probes. Methods auditor independently replayed the real verifier and two negative mutation probes.

The shared research lease was acquired and renewed for this audit, then released at completion. No new downloads, predictive fits, scores, forecasts, paid services, promotion or scheduler changes. Quality bill XML was hashed for integrity but not parsed for extraction. Methods/code auditors read existing outcome-bearing development records; source audit and source-only handoff did not load the outcome population. This is explicitly not a fully label-blind team.

## Result

Machine review and reciprocal challenges completed; confirmed implementation defects were addressed and tested. E0 remains a preparation/measurement study awaiting certified annotations; E1–E9 are not released by agent agreement. No 60% improvement claim follows. Independent human roles and prospective custody remain requirements of the unchanged protocol; any proposed alternative must be a separately named, explicitly revised study, not retroactive approval of these records.
