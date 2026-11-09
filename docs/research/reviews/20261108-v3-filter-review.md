# Qualified amendment triage correction: filter v3

2026-11-08. Provisional agent engineering review of previously exposed design cases, not independent human certification or held-out semantic evaluation. This module is separate from the immutable v1/v2 filters.

## Question and scope

Can a bounded structural scope chain recover the two genuine struck-operand flags missed by v2 while preserving its protection against negated, narrative and insertion contexts? The known motivating cases are 115-S1657 authorize at 14274:14283 and reporting at 14744:14757. Both contain `in clause (...), as redesignated, by striking ... and inserting ...` beneath an affirmative Section 2705 amendment declaration. These cases are explicitly design-exposed.

`scripts/mechanism_context_filter_v3.py` composes v2 without monkeypatching. It reconsideres only legacy deletion flags that v2 declined because affirmative provenance was not established. The local prefix must match the entire bounded grammar for `in` a legislative subdivision or `in the matter preceding` a subdivision, with optional `as redesignated` and up to four comma-separated qualifications. Each represented intermediate direct-text lead-in must itself be such a scope qualifier; narrative, insertion and negation cues stop inheritance. A quoted-block ancestor stops inheritance. An affirmative ancestor declaration must match the entire v2 declaration grammar after terminal dash/colon normalization. Scope strings are capped at 512 characters and ancestry at twelve levels.

A successful correction restores the prior deletion reasons and preserves the exact proof chain as source evidence. `previous_status`, `previous_reasons` and `previous_evidence` preserve v2 decisions, while the original `legacy_*` fields preserve v1. No source hit is removed. No semantic mechanism label is accepted. Retain still means unflagged, not approved.

## Targeted source inspection before the bounded experiment

Only the already exposed 115-S1657 design view was inspected. A direct proof-helper check, not a full bill classification or forty-bill experiment, identified these exact chains:

| Case start | Local qualification | Intermediate qualifiers | Affirmative ancestor |
| --- | --- | --- | --- |
| 14274 | 14192:14225 `in clause (ii), as redesignated, ` | 13710:13730; 13028:13063; 11899:11917 | 11832:11889 |
| 14744 | 14657:14689 `in clause (v), as redesignated, ` | 13710:13730; 13028:13063; 11899:11917 | 11832:11889 |

The intermediate text is respectively `in subparagraph (B)—`, `in paragraph (4), as redesignated,—`, and `in subsection (a)—`. The ancestor is `Section 2705 of title 18, United States Code, is amended—`. These are source-bound syntax clues, not an adjudication of the legal mechanism or net statutory change.

## Synthetic validation

Eight owner tests initially passed normally. Thirteen owner-plus-v2 tests passed under optimized Python. Fixtures cover qualified chains and combined prefixes, absent/narrative/conditional/negated amendment declarations, narrative/insertion/negated intermediate scope, local-prefix punctuation and unsupported modifiers, quoted-block ancestry, replacement operand retention, unchanged inputs, exact source evidence, repeated determinism and preserved v2 affirmative/negated behavior.

Commands:

```
python3 -m unittest tests.test_mechanism_context_filter_v3
python3 -O -m unittest tests.test_mechanism_context_filter_v3 tests.test_mechanism_context_filter_v2
```

Independent review was requested before root freezes and runs the bounded experiment. No forty-bill run, predictive test, outcome access, network acquisition, model fitting or commits were performed by this owner.

## Remaining limitations

This is a finite syntax rule, not a general amendment parser. Unsupported subdivision qualifiers, deep ancestry, cross-referenced instructions, missing structural nodes, tables and ambiguous directives remain unflagged or inherit existing v2 behavior. Existing v2 positives are preserved rather than comprehensively revalidated. A supplied structure is not authenticated by this classifier; the runner must apply source-integrity guards and hash bindings. Overlap, hit counts and unit-test success cannot establish legal precision/recall, historical availability or predictive lift. Known-case recovery would be engineering regression repair on reused design material.

Independent reviewer follow-up: the separate `tests/test_mechanism_v5_independent.py` suite passed, including affirmative qualified chains contrasted with conditional, negated, narrative and insertion lead-ins, intermediate barriers and quoted-block boundaries. No blocking filter defect was found in those probes. This is another agent's synthetic review, not independent human or held-out semantic validation.
