# Bill-mechanism design pilot: independent machine annotations

November 8, 2026. Following the calendar experiment's mixed result, moved to semantic representation design under the user's instruction to take the next step. This is a bounded design exercise before E2 modeling, not another predictive experiment or quality-set evaluation.

[Study definition](../../research/MECHANISM_DESIGN_STUDY_V1.md). Runtime: `data/research-runs/mechanism-design-20261108-v1/` (ignored).

## Completed independent annotation

- Selected the first two already registered design bills per Congress 113–117, preserving original order: ten bills and 50,827 text characters. No outcome or length-based selection. Remaining 40 design cases and all 50 quality cases were not semantically annotated in this batch.
- Two agents independently read all ten complete supplied texts before seeing peer output. Each produced ten meaning summaries and 120 mechanism labels, with present/absent/uncertain status and rationale. Present classifications require exact source quotations. Both sealed submissions are preserved separately.
- Deterministic validation checked registered identities/order, all twelve fields, status/rationale schema, certification flags and every supplied quotation. Quotes resolve to original supplied text; this does not prove that a label follows from the quoted language.
- Paired comparison: **111 agreements / 120 assessments (92.5%)**, with **nine disagreements**. Agreements comprise 74 absent/absent, 33 present/present and four uncertain/uncertain pairs. This is descriptive agent agreement, not accuracy or an independently adjudicated quality score.

Registration digest: `efa0eaf8608f8631a3a59d7d4fbd12a21d2163ea14f739e092d47c35dc3720bf`.
Reviewer A digest: `e8aa34ce6a035d2a3357f344fbde1394c84c2b10608261352413f542d95daa57`.
Reviewer B digest: `2da0ebc8505a6e5b53a21699f67d04525377f0433dc0535923b970b16fbf42d9`.

| Mechanism | Agreements / ten cases |
| --- | ---: |
| Create programme | 10 |
| Authorize | 8 |
| Appropriate | 10 |
| Tax | 10 |
| Prohibit | 9 |
| Require | 9 |
| Amend | 10 |
| Repeal | 8 |
| Rename/designate | 8 |
| Reporting | 10 |
| Deadline | 10 |
| Sunset | 9 |

## Why this matters for the representation

A category alone can hide the direction of a legal change. A proposal may impose a deadline, waive it, amend eligibility under it, or merely cite it. A negative authorization clause must not become an affirmative authorization feature. Deleting words or redesignating numbered clauses is not automatically equivalent to repealing a substantive rule or renaming a public entity.

These boundaries need explicit annotation rules before scaling. The categories should retain operative action, target/entity, direction of change, conditions/exceptions and evidence spans alongside the full text. Any proposed additional fields are design conclusions to register next, not new predictors fitted after observing outcomes.

The third agent read sources first and then challenged all paired labels, including agreements; its separately saved adjudication and [public review](../../research/reviews/20261108-mechanism-design-adjudication.md) retain uncertainty and original disagreements. Machine adjudication is not an independent human reference standard.

## Validation and limits

Seven focused tests passed for annotation integrity/replay and boundary-aware text rendering. Tested unsupported quotations, wrong identities, missing mechanisms, false certification flags, disagreement counting and immutable replay. No full regression rerun is claimed for this isolated design utility.

All 359 original pilot files and frozen model audit remained unchanged. No quality text parsing, new downloads, model fits, new outcome scoring, paid services, promotion or scheduler changes. Shared research lease acquired/renewed during the batch and released at completion. Existing human-review records remain pending.

This small, selected design sample cannot establish precision/recall or generalization. Modern-agent interpretations may reflect pretrained knowledge; they are not automatically historically valid predictive inputs. The next prerequisite is a fixed rubric and further separated measurement work, followed by a separately registered matched predictive comparison. The calendar experiment's unchanged control remains the model reference.

## Adjudication and reciprocal check

All 120 paired labels were challenged, including 111 agreements. The final provisional statuses are **32 present, 74 absent, 14 uncertain**. All nine disagreements remained uncertain; four original shared uncertainties remained; one shared present label (113-hr4401/prohibit) was challenged to uncertain because missing referenced language and an unresolved applicability/prohibition distinction prevent a confident classification. This is an interpretive challenge, not proof that the first two agents were wrong.

Adjudication digest: `3e64c643868f9f9ed052de03c0c6cdafee5f3f740e7d7aa17e3822dc2a9bc635`. The integrity verifier resolved 35 quotes, checked every challenge against both original submissions, preserved all nine disagreements and validated the separate decision bindings. Command: `python3 -m scripts.mechanism_design_audit data/research-runs/mechanism-design-20261108-v1 --adjudication`. Replaying the paired comparison is byte-identical.

Reviewer B then independently [challenged the adjudication](../../research/reviews/20261108-mechanism-peer-review.md), confirmed all 120 challenge records and quote/hash fidelity, and found no definite source-contradicting final decision. It retained methodological disagreements and all 14 uncertainties. Review participation is disclosed: this is a counter-audit by one original reviewer, not a fourth independent annotator. Source matching and agent consensus remain distinct from semantic truth.
