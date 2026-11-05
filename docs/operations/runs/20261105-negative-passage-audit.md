# Negative passage outcome audit — November 5, 2026

## Result

Audited all738 unresolved outcomes from the prior passage-evidence bundle, alongside64 known-positive controls. Acquired five final second-session House calendars (Congresses110,111,112,116,118), including House and Senate bill-history sections:20 retained metadata/text documents,45,521,141 bytes. Cross-checked exact bill identities against retained full BILLSTATUS action lists, publication versions and law indicators.

Twelve bills have explicit terminal pending-calendar entries and matching final calendar-placement actions, without passage or contradictory subsequent evidence. All twelve entries and their complete retained action lists were reviewed case by case in this execution, then passed additional deterministic calendar-number, introduction, date and later-action checks. Ten have previously verified day30 publication proxies. The12 labels are AI/source-adjudicated negative outcomes, not independent human certification. The remaining726 outcomes stay unresolved;18 prior HTTP404 source failures remain outside the completed802-bill audit denominator.

Reviewed bills: 116-hr3356, 116-hr3723, 116-hr3851, 116-hr5119, 118-hr1166, 118-hr6538, 118-hr6997, 118-hr1115, 118-hr7251, 118-hr783, 118-hr8674, 118-hr8728.

## Source scope and limits

[GovInfo calendar documentation](https://www.govinfo.gov/help/ccal) describes histories of bills reported or considered by either chamber; this is not a census of every introduced bill. Therefore absence from these calendars never becomes a negative. Exact final entries explicitly leaving a bill pending are stronger evidence than absence. For each reviewed case, the terminal House/Union calendar number matches the corresponding official action, the list includes introduction, there is no later dated action, and no passage/engrossed/enrolled/law indicator contradicts the pending status.

The screening counts are:682 not listed;12 explicit pending candidates;35 entries without a qualifying terminal pending marker;7 entries with passage or ambiguous history;2 action histories requiring review. All64 positive controls were excluded from the negative set. Broad text screening deliberately leaves ambiguous cases unresolved; it is not a comprehensive parser for every form of parliamentary action. All12 negatives are House bills from116/118 and selected by available pending-history evidence, not a representative negative sample.

## Label timing and coverage assertion

Labels are stored in `data/research-runs/negative-passage-audit-20261105-v2/audited-negative-labels.jsonl`. Their effective time is Congress end; their availability time is the **current adjudication time**, `2026-11-05T19:09:11Z`. No historical training eligibility is claimed from modern verification. Each label carries the exact final-calendar entry, source hashes, matched placement action and complete retained action-list hash. The older final-calendar preservation bound is separately retained and is not substituted for the label audit time.

`complete_coverage: true` is an AI/source-adjudicated assertion for this narrow outcome through Congress end, based on the full retained status history corroborated by an explicit final pending entry. It does not assert that every historical event byte was preserved unchanged, that day30 action features are complete, or that a human has approved the record. Fields explicitly mark `human_reviewed: false`, `historical_training_eligible: false`, and `release_eligible: false`. No main-store observations were backdated or forecasts issued.

The initial screen's count of zero certified negatives is preserved as a stage-specific result. A separate appended adjudication artifact records12 source-reviewed negatives and zero human-certified negatives. It does not retroactively rewrite the screening record or equate machine review with the platform's human-review gates.

## Validation and reproducibility

23 focused tests passed (nine new negative-audit tests plus14 passage/sequential tests). Cases include missing-calendar abstention, companion references, duplicate IDs, passage contradictions, mismatched calendar numbers, later actions, positive controls and current-time label availability. The screen and adjudication each replayed exactly offline. Canonical report hashes verified; all new source receipts were rehashed by the offline source manager. Three reports saved and API-verified in local platform chat “Negative passage audit · 12 reviewed outcomes”.

Initial replay exposed differing JSON key insertion order between freshly fetched and cached metadata, despite equal semantic data. Revision2 canonicalizes serialization; original protocol, sources, screening and adjudication remain intact in `data/research-runs/negative-passage-audit-20261105/`. Revision2 evidence and decisions match revision1 exactly, excluding code/report hashes; the execution amendment documents the change. No outcomes or thresholds were changed to improve scores.

Current screening hash: `0abeebfb006598b3e362e4bbda2ca5415bdd77eda43795d268f3ac8e10fffb44`. Adjudication hash: `d3a988e4fb2d5f799a7190a92524291af268aa7453498e78c436477a74ea8e69`. Modules: `engine.negative_passage_audit` and `engine.negative_passage_adjudication`. Replay requires the retained protocol and source caches; run `python3 -m engine.negative_passage_audit --offline`, then `python3 -m engine.negative_passage_adjudication`. Runtime evidence stays outside Git.

## Remaining work

These12 negatives are useful outcome evidence but do not unblock the original historical learning curve: modern audit availability, sparse early-Congress coverage, incomplete historical action features, selection bias and family/human gates remain. Resolve the726 other outcomes with bill-specific official end-of-Congress evidence; do not convert calendar absence or unsuccessful retrieval into failure. No model fit, accuracy claim, promotion or schedule change was made.
