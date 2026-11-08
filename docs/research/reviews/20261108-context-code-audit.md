# Independent bill-context software audit

Date: November 8, 2026. Agent role: `context_code_audit`. This is a machine review, not human source certification, legal interpretation, or scientific validation. Scope: execution runner, replay verifier, design handoff, focused tests and controlling experimental plan. No fitting, scoring, quality-text parsing or new acquisition was performed. Frozen runtime inputs were not modified; mutation probes used a disposable full copy in a temporary directory.

## Observed checks

- Read repository AGENTS.md, the controlling experiment plan and annotation guide.
- `python3 -m unittest tests.test_bill_context_execution -v`: **5 tests passed**.
- `python3 -m scripts.verify_bill_context_execution data/research-runs/bill-context-20261108-v1`: passed its implemented checks; reported 326 source references, 100 XML files, 1,505,008 bytes, 50 design cases, 213 sections and 28,433 calendar row appearances. It reported scientific validation false. CLI compares the pre-existing verification receipt without altering it.
- `python` is unavailable in this environment; use `python3`. Initial invocation with `python` failed and was repeated correctly.
- Runner creates a new output directory, seals inputs before acquisition, retains unknown/null labels, preserves explicit errors and hardcodes modeling stages blocked. No path from this runner to fitting or human certification was found. These are useful protections, but the verifier weaknesses below narrow the meaning of its passed result.

## Confirmed defects in the initial implementation

### P1: optimized Python removes the verifier's integrity gates

`scripts/verify_bill_context_execution.py` uses `assert` for almost every verification condition (initial lines 23–103). Python `-O` strips these conditions. Reproduction: copy the existing run, load result.json, set body.models_fitted=123 and reseal using `engine.paper_evaluation.seal`; then invoke `python3 -O -c 'from scripts.verify_bill_context_execution import verify; import sys; print(verify(sys.argv[1]))' COPY_DIRECTORY`. It exits zero and reports passed software/artifact checks. Hash sealing still runs, but sealing only establishes self-consistency and does not replace semantic validation.

Required correction: use explicit fail-closed exceptions for invariants; regression-test rejection under normal and optimized interpreters.

### P1: E1 membership verification does not reconstruct original splits

At initial lines 85–98, the verifier checks disjoint sets and internally consistent calendar arithmetic. It does not compare core/calibration/evaluation IDs or original control vectors to the registered legacy data. Reproduction: in a temporary copy, swap the first IDs between fold115 core_ids and calibration_ids, reseal e1-unapproved-inputs.json and call verify. It reports passed. This contradicts a broad interpretation of exact split replay; disjointness is insufficient. A changed control vector propagated into its time/interaction versions would likewise evade the internal arithmetic check (code inspection; not separately executed).

Required correction: independently reconstruct the expected fold memberships from original immutable manifests and source rows, verify model hashes, compare ordered IDs, verify unique complete row membership, and compare each cutoff/control vector to the original data before testing added time features.

### P1: record identity and result eligibility claims are not bound

At initial lines 59–83, filenames choose the expected record, but the body bill_id, family_id and congress are not checked against that identity or parsed XML identity. Reproduction: reseal records/113-hr4401.json after replacing its bill_id with 117-hr999999, family_id with wrong and congress with117. Verification still passes. Separately resealing result.json with release_eligible=true and independent_validation=true also passes, since these flags and stage dispositions are not validated.

Required correction: bind all record identities, cutoff, package, parser version and source URL to the expected registered bill/version; independently validate design XML identity. Check declared count/partition fields, failures, blocked stages and false eligibility flags against reconstructed facts. Verify annotation labels/status and required schema keys, not just reviewer-null fields.

### P2: parser Congress comparison accepts a longer numeric prefix

`scripts/bill_context_execution.py`, parse_design, checks `congress.startswith(c)`. Synthetic XML with `<congress>1130th CONGRESS</congress>` and bill number H.R.1 is accepted for113-hr1. This does not demonstrate a wrong real packet; it demonstrates that the intended exact identity gate is weaker than its name.

Required correction: parse the leading complete integer and compare equality. Preserve the original registered runner's provenance when correcting this: its exact code hash is in the immutable registration. Do not silently rewrite that registration or accept an arbitrary replacement parser hash.

### P2: design handoff does not bind page contents to the full execution provenance

`scripts/bill_context_review_handoff.py` unseals registration and individual records but does not replay their registration/body identity bindings, source bytes or result disposition before exporting pages. It also writes pages without recording their content hashes in the handoff receipt. Together with the identity weakness above, a self-consistently resealed substituted record can produce a misleading page under an expected bill title. This is a code-inspection finding; no original handoff or approval was changed.

Required correction: require an appropriately scoped corrected provenance verification before export; bind selected identity and source hash, and retain an export manifest hashing generated pages and annotation guide version. Keep human-review states pending and quality pages absent. The user's reviewer volunteering is context, not evidence approval or qualification.

## Coverage and interpretation

The focused tests cover deterministic selection, family shortfall/duplicate rows, calendar boundaries, basic XML identity/negation/Unicode, and blocked status. They do not currently cover full replay tampering, optimized execution, exact fold replay, or handoff provenance. Add targeted negative tests for the confirmed defects; no need to rerun fitting or expose quality annotations.

The actual run passed the checks that existed. Mutation acceptance shows the verifier could falsely validate altered data, not that the original run was altered. The execution receipt's zero fitted models and all-blocked scientific gates remain consistent with the observed unmodified run. E0 human annotation and other human/custody gates remain unresolved; agent cross-review cannot certify them under the controlling protocol.

## Cross-audit and remediation status

Findings supplied to root for repairs. This report records the original audit evidence; independent re-review of the corrected implementation and peer reports will be appended separately once available.

## Repair and independent cross-audit follow-up

Root assigned this auditor ownership of the verifier and new mutation tests after the initial independent findings were delivered. Consequently the following implementation is **my repair**, not my independent certification of that repair. The methods agent independently reviewed it and is replaying it separately.

Replaced verifier assertions with explicit `require` exceptions, preserving gates under optimized Python. Added reconstruction of the complete disposition/source packet; identity/cutoff/version/source/parser bindings; strict design XML Congress/chamber/number checks; complete mechanism/lexical schema; exact legacy core/calibration/evaluation memberships and original vectors/cutoffs; full annotation queue; result counts, failures, eligibility and stage dispositions. The methods agent then identified missing section-coordinate binding during cross-audit; added full XML section index/ID/text/hash equality and a regression case. No registered runner, original plan or runtime record was changed. The original parser's prefix defect remains in the immutable v1 implementation; the corrected verifier and separately versioned renderer check exact identity.

New `tests/test_verify_bill_context_execution.py` exercises a temporary copy of the retained corpus. Its initial seven cases passed in 18.621 seconds: original replay, record identity substitution, core/calibration swap, internally consistent altered control vectors, false release eligibility, non-null annotation label and optimized-Python false fit count. An eighth section-coordinate mutation case was subsequently added in response to cross-audit. These are explicit local-corpus integration tests: they skip with a stated reason when the ignored runtime corpus is unavailable in a clean checkout. They do not imply that corpus evidence is publicly reproducible from Git alone.

## Cross-audit of source review

Read [the source agent's report](20261108-context-source-audit.md), comparing its claims with the audited code, actual verifier output and design-only record 113-hr4401. The exact heading/body joins `Short titleThis Act may be cited as the ` and `In generalSection 205(j)(1)` are present in the preserved extraction; the report correctly distinguishes fused presentation/tokenization from loss of raw XML bytes. The Congress-prefix reproduction was independently reproduced by this auditor. Source counts, section counts and null/unapproved states agree with the independent software replay. I did not independently repeat its 992-boundary or 1,105-lexical-span census, and do not certify those counts on its behalf.

Its warning that generic replay loads outcome-bearing population records is accurate: this software audit uses `load_rows()` and is not a label-blind source audit. No predictive fit, score or selection was performed. Its recommendation for separately versioned markup-aware rendering is justified, and its distinction between AI review and qualified human certification matches the controlling plan. The source report does not claim historical byte identity from a 2026 download, legal-mechanism accuracy from keywords, or scientific success from hashing. No unsupported gate-clearing claim was found in the peer report.

The additional section-coordinate mutation and original positive replay both passed (2 tests, 4.816 seconds). This rechecked the positive run after the cross-audit fix.

### Root integration disposition

After this report's initial handoff finding, root implemented source-only identity/byte/pinned-receipt checks and export page/code/guide hashes. The source agent independently challenged the first revision and verified the final repair and two rejection probes; see its final handoff re-review. Root's full regression run passed all 318 tests in 77.310 seconds, including all eight verifier integration cases. These integration statements do not retroactively attribute the source agent's tests to the software auditor.
