# Official context diagnostic v1: source acquisition and extraction registration

This separate current-rendition retrospective diagnostic does not modify E3 or certify historical forecasts. No historical source custody, negative-label certification, human certification, family completeness, promotion or 60% improvement is established. Sponsor party and text modeling are excluded. A distinct fit registration and independently reviewed runner must precede labels/fits. This acquisition script never invokes its separate outcome function.

## Fixed source population and bounded acquisition

Use the previously independently accepted twelve official BILLSTATUS directory indexes, pin their bytes and result, and validate exact observed XML hrefs. Canonical IDs have form hr1-113. Before hashing, exclude the protected 100-case pilot and its known families plus all 595 previously scored evaluation identities and their known families across the entire sampling pool. Use only frozen pilot registration, prior prediction identity/family fields, and existing source-record family assignments. Do not load historical quality labels or recompute a graph by loading outcomes. Report this limited known-family coverage; later current related-bill edges can reveal additional exclusions.

For each Congress 113–118, select the first 2,000 remaining identities by SHA-256 of `official-context-diagnostic-v1`, newline and canonical ID. Freeze all 12,000 cases before network. Four concurrent workers schedule round-robin across Congresses, preserving fixed order within each. No retries or replacements, including later semantic or label failures. Every case receives an attempted/failure/not-attempted disposition.

Each current XML response has a 2,000,000-byte cap plus one retained sentinel. Reserve that maximum for each in-flight request; total retained response bodies may not exceed 500,000,000 bytes. Stop new scheduling after 1,800 seconds. This is explicitly a scheduling ceiling: existing requests may run to their 20-second socket timeout, and offline feature processing is not inside the scheduling deadline. These limits are not measured duration/cost promises. Save request intent, raw source, response metadata and hashes. Retain HTTP/transport/schema failures; do not interpret missing files as negatives. No linked text downloads or retries. Source files are newly retrieved; no silently mixed old renditions.

## Frozen feature mapping

Parse exact validated official identity; introduction must fall inside the calendar Congress. Checkpoint is introduction plus 180 days and must be strictly before next January 3 Congress start. All date-only events enter features only when D is strictly before checkpoint date; same-day events are withheld. Current edition dates are **retrospective publication-date assertions**, not historical availability dates.

A has the six unchanged formula definitions: maximum eligible publication stage/4; capped bill age/730; eligible version count capped30/30; days since last edition capped730/730; Senate indicator; editions in preceding30days capped10/10. Eligible recognized codes are IH/IS stage0, RH/RS stage1, own-chamber EH/ES stage2 (opposite chamber0), ENR stage3. Require a unique introduced package whose asserted edition date is on/after introduction and strictly before cutoff; delayed printing is retained, pre-introduction or cutoff-and-later assertions are rejected. Match exact GovInfo HTTPS source host, own package ID, code/type and rendition filename; conflicting dates/types fail. Deduplicate by package. Count only asserted editions from introduction through strictly before cutoff. Other codes do not enter the legacy anchor. Unknown or invalid anchor excludes both arms before labels.

B adds three fields: log1p(active cosponsors); log1p(distinct top-level referred committees); days since last qualifying action divided180 and bounded[0,1]. It also adds three missing indicators, for twelve total columns. Fit-stage imputation is median of observed training values only; scaling uses training population standard deviation floor0.1. If any context field is entirely missing in training, stop the entire comparison; do not drop the field or choose a different subset after labels.

Cosponsors require a Bioguide identity and valid join date. Deduplicate identical identity/history; conflicting histories become unknown. Join must be before cutoff, and a dated withdrawal before cutoff removes that cosponsor. Join or withdrawal exactly on cutoff makes the aggregate unknown; a join/withdrawal on the same earlier day is inactive. Absent withdrawal means no withdrawal asserted by this current record, not certified completeness. Absent/unsupported cosponsor container is missing, not zero; an explicitly empty supported container is zero.

Referral breadth uses only top-level committee system codes and dated activity items whose name is exactly `Referred to`. Deduplicate committee codes; subcommittees are not counted as new committees. Missing committee/activity history or unsupported layout is unknown. An explicitly empty supported container is zero. No guessed action-code-to-referral mapping is used.

Action recency uses all valid top-level action dates with recognized source system0,1,2,9 before cutoff; code is optional (ordinary sources0/1 legitimately omit it). Deduplicate source/date/code for recency; no action prose becomes a predictor. Invalid required dates/identity/history make affected context fields missing. Labels, laws, unrestricted current counts, later actions, titles and summaries are not predictors.

## Separate outcome-only resolver, never run during acquisition

After source/feature/family populations are frozen independently, classify own-bill public-law enactment strictly after cutoff and before Congress end. Positive requires a concordant public-law number in own-bill laws and exact anchored `Became Public Law No` terminal action text plus date. Supported terminal pairings are LOC action36000/source9, or E40000/source2 or9. Multiple conflicting laws/dates, mismatched identity, unsupported source, incomplete history, signing-only or other uncorroborated enactment assertions remain unknown. Private/unsupported law types remain unknown. Already enacted by cutoff or on boundary dates are exclusions, not negatives.

A zero is only an expressly **uncertified current-official-record negative proxy**: complete parse with matched identity/introduction, nonempty valid dated action history from known sources, updateDate strictly after Congress end, and no public-law/signing/enactment assertions in laws, actions, latest/last action or public-law edition metadata. Missing or conflicting coverage stays unknown. This makes a bounded retrospective calculation possible; it does not certify true negative follow-up. Positive maturity is enactment date; negative target horizon matures at Congress end, while current source update is retained separately. These target-horizon dates never certify historical availability of this current record.

Source methods are supported by pinned official GPO XML guidance, Library of Congress action-code discussion and official API endpoint documentation in `data/research-runs/official-context-primary-docs-20261109/`. The code/receipt hashes are frozen with acquisition. Code/source pairing restrictions are conservative; no secondary inferred tables are used.

## Later comparison and stopping

Train on Congresses113–116; evaluate117 and118 with the same two fixed fitted artifacts, no calibration/tuning. References are training-only Beta(1,1) rate and stage-smoothed rate. Before labels, union available current related-bill links and frozen known-family assignments conservatively, removing protected/previously scored known families. Give later evaluation priority over earlier evaluation and training when families cross roles; retain one deterministic representative per family. Incomplete genealogy and adaptive exposure remain explicit. The fit runner must independently register exact memberships, feature matrices, labels, solver, two-fit limit and metrics before training. Acquisition is not permission to bypass that review.

Report all12,000 source-only dispositions, missingness, accepted populations, unknown labels and class/family counts before any fits. No desired score or event count permits extending or replacing the sample. Preserve negative results and all failures. Tests are software checks, not predictive evidence.

```sh
python3 -m unittest tests.test_official_context_v1 tests.test_official_context_independent
python3 -m scripts.official_context_acquisition_v1 --output data/research-runs/official-context-acquisition-v1-NEW
```
