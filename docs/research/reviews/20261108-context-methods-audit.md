# Independent machine methods audit: bill-context preparation

Date: November 8, 2026 (America/New_York). Reviewer: independent methods agent. Baseline: `f2101ace0b5ebb0cb4a8633eaad7fa4ca9f6aead`. Scope: [experiment plan](../BILL_CONTEXT_EXPERIMENT_PLAN_V1.md), preparation runner, read-only verifier and ignored runtime `data/research-runs/bill-context-20261108-v1/`. This is an agent audit, not human certification, an external statistical review, or independent empirical validation. No models were fitted, no prediction losses calculated, no quality XML parsed, and no frozen artifacts changed.

## Verdict

The current preparation artifacts pass the mechanical checks performed below. E1–E9 remain blocked under the existing protocol. Multiple agents can independently inspect and challenge software and reasoning; their agreement cannot supply missing historical evidence, the designated human reviews or future outcomes. The current runner deliberately prepares inputs and reports dispositions; it does not implement the full modeling programme.

Two prospective design/verification issues should be resolved before any model registration: the scope of positive-family floors, and selection among feature blocks evaluated on different populations. Neither is evidence that current predictions are invalid, because this run produced none.

## Reproduced results

Called `scripts.verify_bill_context_execution.verify` directly, without its receipt-writing CLI. It returned: 326 retained metadata source references, 100 XML files, 1,505,008 XML bytes, 50 parsed design bills, 213 design sections, 28,433 calendar-row appearances, unchanged frozen artifacts, and no quality-text parsing. Source bytes were hashed for integrity; quality XML was not parsed or read for interpretation.

Independently reloaded the legacy population, reconstructed the global automated family graph and `make_split` memberships, compared the recorded E1 partitions, and checked datetime objects rather than relying only on string order. Checked each of the 28,433 stored control vectors and cutoffs for exact equality with its legacy row, and independently confirmed calibration/core/evaluation family separation. No new model probabilities or losses were computed.

| Evaluation Congress | Core / calibration / evaluation rows | Core / calibration / evaluation positives | Latest training label bound | Earliest evaluation checkpoint |
| --- | --- | --- | --- | --- |
| 115 | 3,569 / 893 / 2,717 | 86 / 30 / 75 | 2017-03-25 23:59:59Z | 2017-07-02 23:59:59Z |
| 116 | 5,272 / 1,319 / 2,792 | 130 / 28 / 48 | 2019-06-12 23:59:59Z | 2019-07-02 23:59:59Z |
| 117 | 7,049 / 1,763 / 3,059 | 181 / 46 / 59 | 2021-05-08 23:59:59Z | 2021-07-03 23:59:59Z |

Both classes occur in every core and calibration partition. Training Congresses precede evaluation Congresses. Each training and evaluation population contains one row per provisional family; core/calibration and train/evaluation family intersections are empty under the recorded graph. These results verify recorded chronology, not the truth of historical publication dates or completeness of the family graph.

The E0 selection contains exactly ten design and ten quality bills in each of Congresses 113–117, and 100 distinct provisional families globally. Selection uses ID digest and fixed eligibility/family exclusions, not outcome values. Eligibility and available records nevertheless define a restricted feasibility population; this is not representative sampling of all legislation. The full legacy population has zero subject-bound review objects.

The E1 formula is implemented correctly: `r = (Congress_end - cutoff).total_seconds() / 63072000`, and the interaction is `x[0] * r`, because the legacy first column is already `stage/4`. Each training row uses its own Congress boundary. The fixed Congress-end convention is January 3 at 17:00 UTC. The code rejects invalid legacy stage encodings and nonpositive/out-of-range remaining time.

## Findings requiring resolution before fitting

1. **Methods gate scope is not executable yet.** Plan section 3 requires 200 reviewed positive training families and 100 reviewed positive development families at the applicable registered study level, but leaves the precise population to methods signoff. The execution receipt correctly reports this as unestablished. Raw training positives are only 116, 158 and 227 per fold; evaluation positives are 75, 48 and 59. If these floors apply per fold, the earlier training folds and all development folds fail even before review. If they apply to distinct study-level populations, those populations and global deduplication must be named and counted before registration. Reused fold appearances cannot be summed. Do not resolve this after seeing scores or label all folds approved merely because aggregate counts are larger. No reviewer identities or qualifications were certified here.

2. **E6 ranking has a population-comparability ambiguity.** Section 3 forbids ranking different conditional subsets as interchangeable, but section 7 ranks more than four qualifying blocks by relative Brier gain from their respective matched subsets. Matching within each block does not make gains across different subsets comparable. Resolve this in a versioned pre-score amendment: either use a fixed score-independent block priority when subsets differ, or preregister genuinely common-population block comparisons and their additional fit allocation. Simply recomputing the eventual union on a common E6 population does not retroactively make earlier screening gains comparable. Preserve the original plan and hash-bound registration rather than silently editing the execution's referenced plan.

3. **The reusable verifier is narrower than its potential interpretation.** Its E1 loop checks partition disjointness and formula arithmetic, but does not independently reconstruct legacy fold memberships, assert control-vector equality, or repeat temporal/family separation. The runner performed some of these checks, and this audit independently reproduced all of them successfully for the current artifacts. Add these as reusable verifier checks for future executions. This is a coverage gap, not an observed corruption or numerical mismatch.

## Scientific blockers versus software status

- Official hosting and present-day retrieval do not establish historically available rendition bytes. All new XML remains marked historically ineligible.
- The family graph joins source-listed related bills and normalized equal titles. This can both miss true families and overjoin unrelated legislation; its disjointness is conditional on those provisional edges. Later-discovered edges can be used conservatively to exclude leakage, but cannot become historical predictors without availability evidence.
- The quality partition is unopened for extraction and annotation. Independent agents reviewing the design partition do not establish the quality-set precision/recall thresholds, human adjudication or field acceptance. The existing protocol explicitly reserves those certification roles for qualified humans.
- Congresses 115–117 are exposed development periods. Additional independent agent teams do not make those outcomes unexposed. Congress 118 is excluded from new ranking. No historical survivor backtest before its label availability is authorized.
- The 75-fit ceiling is a maximum, not a required quota or exemption from evidence gates. E2–E8 also lack registered feature matrices/implementations or upstream selections. E9 needs a separately frozen successor, protected custody and genuinely future observations. Agent consensus cannot shorten this timetable.

## Work that can proceed now

Independent agents may review the 50 design cases as explicitly provisional machine annotations, challenge each other's evidence and retain disagreements; audit parser and verifier defects; prepare source-availability and family-investigation queues; implement deterministic feature/solver fixtures without fitting research cases; and draft sealed-registration tooling. They may not write human approval, certify quality fields, reopen quality content before design freeze, fit the blocked historical experiments, or replace the frozen candidate under the existing protocol. A differently governed machine-only exploratory study would need a separately named, explicitly amended protocol and appropriately weaker claims; it would not satisfy the current paper gates.

## Reproduction

Run from the repository root, using retained ignored artifacts. The first call is read-only and avoids the CLI's receipt writer:

```python
from pathlib import Path
from scripts.verify_bill_context_execution import verify
print(verify(Path("data/research-runs/bill-context-20261108-v1")))
```

For the additional split checks used in this audit:

```python
import json
from datetime import datetime
from pathlib import Path
from engine.cohort import family_groups
from engine.paper_evaluation import unseal
from scripts.cross_congress_evaluate import load_rows, make_split
rows = load_rows()
groups = family_groups(rows)
by_id = {r["bill_id"]: r for r in rows}
inputs = unseal(json.loads(Path(
    "data/research-runs/bill-context-20261108-v1/e1-unapproved-inputs.json"
).read_text()))
def dt(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))
for c in (115, 116, 117):
    train, test = make_split(rows, c, groups)
    f = inputs[str(c)]
    assert f["evaluation_ids"] == [r["bill_id"] for r in test]
    assert set(f["core_ids"] + f["calibration_ids"]) == {r["bill_id"] for r in train}
    core = [by_id[i] for i in f["core_ids"]]
    cal = [by_id[i] for i in f["calibration_ids"]]
    fam = lambda rs: {groups[r["bill_id"]] for r in rs}
    assert not (fam(core) & fam(cal))
    assert not (fam(train) & fam(test))
    assert len(fam(train)) == len(train) and len(fam(test)) == len(test)
    assert max(r["congress"] for r in train) < c
    assert max(dt(r["label_available_at"]) for r in train) < min(dt(r["cutoff"]) for r in test)
    assert {r["y"] for r in core} == {0, 1} == {r["y"] for r in cal}
    for r in f["rows"]:
        assert r["features"]["control"] == by_id[r["bill_id"]]["x"]
        assert r["cutoff"] == by_id[r["bill_id"]]["cutoff"]
    print(c, [len(rs) for rs in (core, cal, test)],
          [sum(r["y"] for r in rs) for rs in (core, cal, test)])
```

No full regression suite was rerun by this methods agent; the checks above ran successfully. Peer-agent cross-audit observations are recorded below; this report does not certify another agent's untested conclusions.

## Peer cross-audit: software report

Read the separate [software audit](20261108-context-code-audit.md). Independently confirmed its Congress-prefix defect by passing synthetic `<congress>1130th CONGRESS</congress>` XML to the unchanged registered parser for `113-hr1`; the parser accepted it. The independent exact-membership replay above also confirms that the software report correctly distinguishes a verifier coverage weakness from any observed alteration of the actual run. Python assertion removal under optimization is consistent with the inspected implementation; this methods agent did not independently repeat the software agent's disposable-copy optimized mutation probe. No claims of independent reproduction are made for probes not run here. Corrected-verifier review remains pending while implementation changes are in progress.

### Corrected verifier cross-audit

After the software agent implemented explicit `require` gates and authoritative bindings, independently read the corrected implementation and reran `verify()` against the original run: passed with the same counts and no scientific certification. On a disposable copy, resealed a swap of the first fold115 core/calibration IDs: rejected with `E1 authoritative fold/feature mismatch`. Restored the copy, resealed `release_eligible=true`: rejected with `Invalid validation/eligibility claims`. The original runtime artifacts were never modified. The earlier verifier-membership finding is therefore addressed for the tested cases; complete family/temporal truths remain conditional on source evidence and the provisional graph.

A remaining section-coordinate coverage detail was supplied to the implementer: section `index` and `xml_id` should be rebound to XML alongside text/hash. The original parser's Congress-prefix weakness remains documented because the registered runner is intentionally unchanged; corrected replay independently enforces exact Congress identity before accepting design extraction. This is a fail-closed replay safeguard, not a retroactive rewrite of the original parser or its registration.

The software agent subsequently added exact section `index`/`xml_id`/text/hash equality and a targeted corruption test. This methods agent inspected the added comparison and stricter full-match Congress syntax; the software agent owns the corresponding test result. No additional unresolved current-data mismatch was found in this cross-audit.
