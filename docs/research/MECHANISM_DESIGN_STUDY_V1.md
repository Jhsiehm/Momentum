# Machine-reviewed bill-mechanism design study v1

November 8, 2026. Following the mixed calendar experiment, the next step is representation design: determine what each bill does rather than adding another calendar/model variant. This is a bounded machine-only design exercise, not E2 predictive evaluation, a quality-set test, human certification or evidence of improved forecasting.

## Selection and separation

Use the first two already-registered design cases from each Congress 113–117, in their original frozen order: 113-hr4401, 113-s1772, 114-s2836, 114-hr668, 115-hr4885, 115-hr4920, 116-s724, 116-s4142, 117-hr6116, 117-hr1352. Selection uses no outcomes or text-length filtering. These ten cases contain 50,827 characters in their separate v2 reading views. The other 40 design cases and all 50 quality cases are outside this initial semantic pass. No outcome or quality-text files are provided to reviewers.

Registration sealed before annotations: `efa0eaf8608f8631a3a59d7d4fbd12a21d2163ea14f739e092d47c35dc3720bf`. Runtime directory: `data/research-runs/mechanism-design-20261108-v1/`. The manifest binds selection, input text hashes, mechanism names, allowed statuses, reviewer roles and scope. Original pilot/renderer records remain immutable.

## Independent reviews and challenge

Two agents separately read all supplied text and each write a plain-language summary and twelve overlapping mechanism assessments: create programme, authorize, appropriate, tax, prohibit, require, amend, repeal, rename/designate, reporting, deadline, sunset. They may not read the other submission before completing their own. Each value is present, absent or uncertain; present requires an exact source quotation. Every label includes rationale. Unknown is not zero. Keywords alone are not evidence of operative legal effect. Existing-law cross-references and unavailable deleted text may require abstention.

Both reviewers receive the same scope guidance: distinguish authorization from appropriation and prohibition from affirmative duty; create_programme refers to a new programme/entity framework, not any new definition; reporting means an operative report/disclosure obligation; deadline means an operative time limit; sunset means actual expiry. Broader boundary ambiguity is recorded rather than hidden. These instructions are design guidance, not a certified annotation standard.

A deterministic validator checks all IDs, twelve labels, status values, rationales, null certification flags and exact quotation resolution. It computes descriptive agreement and per-mechanism confusion counts across 120 paired assessments. Agreement is not precision, recall or accuracy, and agents from the same model family are not statistically independent reference judges. Both can share an error.

After submissions are sealed, a third agent reads the supplied text and both reviews, challenges disagreements and also audits agreements. Its decisions are separately versioned, with evidence and unresolved cases retained. Neither original submission is overwritten. Interpretation fixes become proposed rubric changes for later design work; do not revise the held-back quality sample or claim this exercise validated labels.

## Exit and future experiment

Deliverables: two immutable provisional annotation sets, quote-integrity checks, disagreement list, separate machine adjudication, failure examples and proposed rubric clarifications. No model fits, scores, forecasts, label-accuracy estimate, human approval or historical feature eligibility are created.

Before E2 fitting, a later registered study must settle the category definitions, validate extraction on appropriately separated data, build enough dated training/evaluation coverage and specify handling of uncertain attributes. Modern-agent interpretations of historical text may carry pretrained knowledge of later events; therefore these design annotations are not automatically eligible historical predictors. The existing text-only TF-IDF experiment remains a separate possible comparison, not something this small pilot can validate.
