# Independent structural-input v1 review — 2026-11-08

Decision: the registered structural-input design run passed the independent checks described below. This is a parser-visible structure and offset review, not semantic or predictive validation.

## Before registration

The independent reviewer authored `tests/test_bill_structural_input_independent.py` without inspecting the forty real design sources. All nine methods passed under normal Python and `python3 -O`. Cases cover nested table ownership without duplicate inner cells; empty cells and uninterpreted malformed/merged-span attributes; orphan rows/cells; mixed-number, land-description and MathML fraction contexts without normalization; namespace-qualified attribute collisions; incorrect source/view/bill bindings; canonical tampering rejection; deterministic nonmutating construction; and an external DOCTYPE with network sockets blocked. No substantive failures were observed in these tests. The builder and execution runner were also read for scope, input authentication, pre-execution registration, fixed-population handling, and failure preservation. Registered source and tests were not edited afterward.

## Independent registered-run verification

Registration: `eb98b86390cfafde53c3806f9d47511b54848ee5ecdaded3e2226cb1f653b815`.
Result: `f3505ea7c8618d686c0401790130ad619c0c73a0812fca21e05a0559706c3bb0`.

A separate verifier read all forty original XML sources and rebuilt topology and reading-view offsets directly with ElementTree, using an explicit traversal and a locally transcribed frozen renderer block list. It never called the structural builder or coverage auditor. It checked:

- All 83 registered input-file hashes, 23 code/test-file hashes, forty sealed sidecar hashes, and source/view bindings.
- All 8,331 XML nodes in order: qualified names, parents, ordered children, 3,726 parsed attributes and exact start/end offsets.
- All 9,299 XML text/tail segments, inserted separators, full reconstructed reading text and rendered-text hashes.
- The one actual table, its ten rows and twenty cells, source-order membership, literal cell attributes/text/offsets, orphan lists, and absence of inferred grid/span interpretation.
- All three fraction nodes: exact literals, offsets, children, attributes and 32-code-point context bounds. The two `1/2` fractions next to a preceding `4` remain unchanged; the `1/4` land-description fraction remains unchanged.

All forty passed. Normal and optimized executions produced byte-identical sealed review JSON. No discrepancy or post-result correction occurred.

Runtime evidence (ignored, retained locally):

- `data/research-runs/structural-input-v1-20261108/independent_verifier.py`, SHA-256 `55b3d6e6abb612b0c25861a39ff89e6876561105e0806dcf3aa2ee188da92ad5`.
- `data/research-runs/structural-input-v1-20261108/independent-review.json`, sealed body hash `fe80b9071803af6428b3810c5ada68e11cdb3a2b7f92e5d016dcea4bb0127913`. Includes per-bill counts and the complete checked table/fraction records.

Reproduce from repository root:

```sh
python3 -m unittest tests.test_bill_structural_input_independent -v
python3 -O -m unittest tests.test_bill_structural_input_independent -v
python3 data/research-runs/structural-input-v1-20261108/independent_verifier.py
python3 -O data/research-runs/structural-input-v1-20261108/independent_verifier.py
```

## Limits

The verifier uses the same standard-library XML parser family as the implementation; it is an independent traversal, not an independent parser implementation. Parser normalization, omitted XML comments/processing instructions, namespace-prefix spellings and declaration positions, raw attribute lexical form/order, external DTD defaults, and raw XML byte offsets are not certified. Exact offsets refer to decoded Unicode code points in the unchanged frozen reading view. Table source order does not establish a visual grid, and no numeric or legal meaning is inferred from fraction syntax. All forty bills are repeatedly exposed design cases; no protected-quality sources, human certification, historical-availability proof, model fitting or predictive testing were involved.
