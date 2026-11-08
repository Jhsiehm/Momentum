# Bill-context pilot: annotation guide and record dictionary v1

Status: preparation only, November 8, 2026. The [experiment plan](BILL_CONTEXT_EXPERIMENT_PLAN_V1.md) controls acceptance and modeling. This document does not certify fields or assign human reviewers.

## Registered pilot

The executable runner is `python3 -m scripts.bill_context_execution --output data/research-runs/<new-run> --acquire`. Output directories must be new; the runner will not overwrite a prior execution. It acquires the shared research lease, seals selection/code/input hashes before fetching, checks retained evidence bytes, and releases the lease on completion or error. The initial acquisition is sequential and limited to one introduced XML URL per selected bill (100 bills). Network retries follow the existing official-source fetch policy. No paid services are used.

Population: existing nonexcluded development records from Congresses 113–117. Within Congress, sort by canonical JSON SHA-256 of bill ID and then ID. Process Congresses ascending and reject any family already selected anywhere in this pilot. Select 20 per Congress; first 10 are design, last 10 quality. The global family graph is an automated screen, pending human certification. Ineligible and unselected candidates remain in a disposition ledger. This feasibility sample does not estimate population prevalence. Existing 12-case review work stays separate; any overlap is disclosed, not treated as newly independent evidence.

## Versioned record dictionary

Version 1 records are sealed envelopes with a canonical body digest. Original downloaded XML bytes and retrieval receipts are preserved separately under ignored runtime storage. Text is never substituted for its source bytes.

| Field | Meaning / constraint |
| --- | --- |
| `bill_id`, `congress`, `family_id` | Stable joins; family remains provisional until adjudicated. Never use IDs as predictors. |
| `partition` | `design` or `quality`, fixed before source acquisition. |
| `cutoff` | Original day-180 checkpoint, preserving timezone precision. |
| `package` | Introduced `ih`/`is` package identified in retained MODS, not a final amended version. |
| `source` | Official URL, SHA-256, byte count and actual retrieval timestamp. |
| `original_availability` | `unverified` until a subject-bound review establishes what rendition was public at the checkpoint. A 2026 download is not an earlier observation. |
| `historical_feature_eligible` | False throughout this preparation run. Neither parsing nor official hosting certifies historical eligibility. |
| `parser_sha256` | Hash of the exact implementation used. Registration also hashes dependencies and the controlling plan. |
| `attributes` | Twelve mechanism entries with `value: null`, `status: unknown` until reviewed. Null never means absent. |
| `design_extraction.text` | Complete XML text-node concatenation, including negation and cross-references; raw XML remains authoritative for markup and whitespace. |
| `design_extraction.sections` | Each section's index, XML ID if available, text and text hash. Nested sections may overlap and must not be counted as separate independent evidence. |
| `design_extraction.lexical_candidates` | Character offsets and exact quotes in the stored concatenation; pointers for interpretation, not mechanism labels. |
| `quality_content` | Records that quality bytes are retained but quality extraction/annotations have not been opened. |
| `human_review` | Pending. The runner cannot write human approval. |
| `blocked_reason` | A retained missing-source/parser error; no replacement bill is chosen. |

The first twelve mechanisms are create programme, authorize, appropriate, tax, prohibit, require, amend, repeal, rename/designate, reporting, deadline and sunset. They are overlapping labels. A lexical match does not establish any of them: “not authorized” must not become an affirmative authorization, and a citation to a reporting law does not necessarily create a reporting duty.

A completed annotation must retain: mechanism/policy/other field name; value and status (`observed`, `derived`, `unknown`, `disputed`, `not_applicable`); package and source hash; section/XML path and exact quote; affected entity, action, statutory object, conditions, exceptions, amounts/units and effective dates when relevant; effective time, public-availability evidence, actual retrieval time; extraction version; and real reviewer identity/date. Unsupported or ambiguous interpretations remain unknown/disputed. Provision meaning stays alongside the full text. Broader policy/support/procedure/schedule/relationship records are not claimed as implemented or available in this pilot.

## Annotation procedure and quality firewall

1. Assign two qualified independent reviewers and a separate adjudicator; record qualifications and conflicts. Agents may assemble packets but cannot occupy these human certification roles.
2. Review only the 50 design cases initially. Check bill identity, section boundaries, historical rendition provenance and interpretation of the twelve mechanisms. Refine rules on these cases and record every change.
3. Freeze the extractor, vocabulary, annotation instructions and hashes before opening the 50 quality annotations or running quality extraction. The present candidate lexicon is a design implementation, not an accepted extractor. If the freeze has not occurred, the quality evaluation remains blocked.
4. Have the two reviewers annotate quality cases independently, without seeing each other's decisions or outcome labels. The annotation queue deliberately leaves all decisions and names null. Raw bills may themselves reveal political context; this is not a guarantee of perfect blinding.
5. Resolve disagreements through the adjudicator, retaining both original annotations, the resolution, source spans and rationale. Source availability and global-family reviews are additional requirements; mechanism agreement alone does not satisfy them.
6. Report per-field precision/recall, agreement, abstentions, per-period coverage, exact date/unit agreement and evidence resolution. Count at least 20 positive quality annotations before assessing that field against 95% precision / 90% recall. Zero unresolved identity/future-availability errors and 100% resolvable retained references are required. Sparse fields stay uncertified. These are engineering thresholds, not statistical power guarantees.
7. Preserve failed quality results. Do not tune on the quality set and report its rescore as independent. A revised extractor needs a newly registered quality sample.

## Source/feature readiness matrix

| Block | Current evidence | Required next evidence |
| --- | --- | --- |
| E1 calendar | Existing checkpoint, Congress end and stage; exact legacy memberships retained | Subject-bound introduction, family, label and population reviews; approved modeling registration |
| E2 mechanisms/policy | Introduced XML collection and design-only candidate spans | Qualified annotations, quality certification and dated policy labels |
| E3 text | Current introduced XML bytes, without historical rendition certification | Historical availability review, matched population, audited sparse objective and dependency pinning |
| E4 support/procedure | Legacy publication-stage metadata only | Point-in-time affiliations/roles/cosponsors and complete dated action evidence |
| E5 schedules/relations | No certified feature matrix | Announcements as known at cutoff, coverage evidence, typed dated links |
| E6–E8 | No new qualifying modeling results | Accepted prerequisite blocks and registered matched comparisons |
| E9 | Existing V1 remains frozen | Qualified successor, joint protocol/custody, timely genuine forecasts and matured future outcomes |

The E1 input file is explicitly **unapproved**: storing mechanically derived calendar features does not approve model fitting. The runner provides evidence preparation and stage dispositions, not implementations of the nine gated model experiments. A subsequent execution must verify the complete source/review manifests before fitting. No automatic promotion or recurring schedule is changed.
