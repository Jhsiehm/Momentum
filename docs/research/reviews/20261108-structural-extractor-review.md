# Independent structural extractor v1 review — 2026-11-08

Outcome: no mapping or arithmetic discrepancies found. The registered experiment produced **no changed decisions**: all 2,722 baseline locators pass the cell-boundary screen, 2,403 remain after combining the frozen context filter, and quotation overlap stays 449/501. This is a null diagnostic result, not measured semantic or predictive improvement.

## Independence and scope

A separate review agent wrote seven adversarial synthetic tests before registration without opening the real 40-case corpus. All seven passed under normal and optimized Python. Tests cover nested-cell masking, exact half-open boundary touches, zero-width/orphan cells, Unicode fraction ambiguity, full-context/raw-output preservation, binding corruption, and metric overlap losses and cross-mechanism nonmatches. No failing test or implementation correction was required by this independent suite.

After registration, a separate verifier reconstructed all 2,722 decisions directly from sidecar node intervals, checked containing/intersecting/enclosing-node mappings and fraction contexts, checked every original candidate identity and unchanged raw output/full text, verified all 40 per-bill and 12-category metrics against all 501 reference effects, and verified all 257 registered code/input byte hashes. Its normal and optimized executions produced the same sealed review. This verifier does not invoke the new extractor or runner metrics function. It trusts previously authenticated sidecar node positions; it does not supply a second XML parser. The preceding structural-input independent audit supplies the separate raw-node reconstruction.

All 17 predeclared associated hits were inspected in context: 14 table-cell hits in 114-hr3803 and three fraction-near hits in 113-hr128. No hit crosses a cell boundary. The three near-fraction hits do not themselves overlap the fractions. The third source fraction, the land-description `1/4` in 117-hr1597, has no hit within its fixed context window and therefore no per-hit fraction annotation; it remains intact in the structural input and full text. There were zero boundary-flagged cases to adjudicate. This close contextual inspection is not a semantic census of all 2,722 hits.

## Every associated case

All rows below are retained by the boundary rule. Offsets are half-open Unicode reading-view positions, not raw XML byte coordinates.

| Bill | Mechanism | Offsets | Locator | Exact containing cell or fraction context | Structural rationale |
|---|---|---|---|---|---|
| 113-hr128 | prohibit | 3770:3790 | `no broadcaster shall` | ster shall allot more ⏎     than 41/2 hours per week of free broadcas | Near fraction; exact fraction/context preserved, no numeric inference. |
| 113-hr128 | require | 3785:3790 | `shall` | ster shall allot more ⏎     than 41/2 hours per week of free broadcas | Near fraction; exact fraction/context preserved, no numeric inference. |
| 113-hr128 | require | 3991:3999 | `required` |    this paragraph would exceed 41/2 hours, the time required ⏎     to | Near fraction; exact fraction/context preserved, no numeric inference. |
| 114-hr3803 | authorize | 2232:2235 | `May` | May 15 | Entire locator inside one cell; no interior cell edge. |
| 114-hr3803 | authorize | 2258:2261 | `may` | Appropriation bills may be considered in the House of Representatives. | Entire locator inside one cell; no interior cell edge. |
| 114-hr3803 | appropriate | 2330:2344 | `Appropriations` | House Appropriations Committee reports last appropriation bill. | Entire locator inside one cell; no interior cell edge. |
| 114-hr3803 | appropriate | 2368:2381 | `appropriation` | House Appropriations Committee reports last appropriation bill. | Entire locator inside one cell; no interior cell edge. |
| 114-hr3803 | appropriate | 2429:2442 | `appropriation` | House completes action on appropriation bills. | Entire locator inside one cell; no interior cell edge. |
| 114-hr3803 | reporting | 1845:1852 | `submits` | President submits budget recommendations. | Entire locator inside one cell; no interior cell edge. |
| 114-hr3803 | reporting | 1924:1931 | `submits` | Congressional Budget Office submits report to Budget Committees. | Entire locator inside one cell; no interior cell edge. |
| 114-hr3803 | reporting | 1932:1938 | `report` | Congressional Budget Office submits report to Budget Committees. | Entire locator inside one cell; no interior cell edge. |
| 114-hr3803 | reporting | 2026:2032 | `submit` | Committees submit views and estimates to Budget Committees. | Entire locator inside one cell; no interior cell edge. |
| 114-hr3803 | reporting | 2108:2114 | `report` | Budget Committees report joint resolution on the budget. | Entire locator inside one cell; no interior cell edge. |
| 114-hr3803 | reporting | 2355:2362 | `reports` | House Appropriations Committee reports last appropriation bill. | Entire locator inside one cell; no interior cell edge. |
| 114-hr3803 | deadline | 1772:1778 | `before` | On or before: | Entire locator inside one cell; no interior cell edge. |
| 114-hr3803 | deadline | 1969:1983 | `Not later than` | Not later than 6 weeks after budget submission | Entire locator inside one cell; no interior cell edge. |
| 114-hr3803 | deadline | 1992:1997 | `after` | Not later than 6 weeks after budget submission | Entire locator inside one cell; no interior cell edge. |

## Observed shortfalls and interpretation

- `114-hr3803`, authorize, 2232:2235: **“May” is a month in “May 15”**, not modal permission. The boundary-only screen correctly leaves the existing locator unchanged but does not resolve this clear lexical ambiguity. This is a qualitative error example, not a certified precision estimate.
- `114-hr3803`, appropriate, 2330:2344: **“Appropriations” is part of “House Appropriations Committee”**. That word alone does not establish that the provision appropriates money. The other “appropriation” locators at 2368:2381 and 2429:2442 also describe appropriation bills in a timetable; they are candidates requiring semantic review, not established appropriation effects.
- `114-hr3803`, deadline, 1772:1778: “before” is in the table header “On or before:”; interpreting an actual deadline requires its row relationships. Preserving those relationships does not itself interpret them.
- The table is proposed statutory budget-timetable text, not observed historical legislative-calendar data. It cannot be inserted directly as an actual schedule feature.
- Fraction context preserves ambiguous flat text “41/2”; the wrapper intentionally does not decide mixed-number meaning. Full bill context remains available.
- The design corpus has one explicit table and three explicit fractions, and has been repeatedly exposed. Synthetic successes demonstrate only the declared guard behavior. There is no support for an accuracy, generalization, or 60% predictive-improvement claim.

No post-result rule changes, reference corrections, extra design substitutions, quality-text access, model fitting, or predictive testing occurred in this review. Human, source-availability, time and family-separation gates remain unmet where previously recorded.

## Evidence and reproduction

- Registration: `data/research-runs/structural-extractor-v1-20261108/registration.json`; envelope hash `59f6003bd437cfc88b3aa3c4d1b8031d4826b997f3086bad2c8706fde2d1dcc0`.
- Result: `data/research-runs/structural-extractor-v1-20261108/result.json`; envelope hash `7e65d21b79de0c1bf1a01c2b6192e3aa0c1641fdf877f7e7d88fa5f286c7c2af`.
- Review: `data/research-runs/structural-extractor-v1-20261108/independent-review.json`; envelope hash `4649080a66b0037791175700f602991d910e8d69c1fb4daf704bd1036fca0e34`.
- Verifier: `data/research-runs/structural-extractor-v1-20261108/independent_verify.py`; file SHA-256 `dad6c146fc455cf27b75e47e9627fccfa0a521dfe714816c8d54ad62a91f9df4`. Runtime artifacts remain ignored.
- Independent tests: `tests/test_mechanism_structural_independent.py`.

```sh
python3 -m unittest tests.test_mechanism_structural_independent -v
python3 -O -m unittest tests.test_mechanism_structural_independent -v
python3 -m data.research-runs.structural-extractor-v1-20261108.independent_verify
python3 -O -m data.research-runs.structural-extractor-v1-20261108.independent_verify
```
