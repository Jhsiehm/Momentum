# Machine adjudication of bill-mechanism design labels

Date: November 8, 2026. Scope: ten registered design bills, twelve mechanisms per bill. This is a provisional machine review of introduced text, not a predictive experiment, human reference standard or quality-set evaluation.

## Method and evidence separation

The adjudicator read all ten complete introduced-text reading views before seeing the paired submissions. After both reviewers had sealed their work, it read both summaries and all 120 paired assessments and challenged each against the supplied text. No outcome or held-back quality-text files were accessed. It reviewed agreements as well as disagreements; an agreement was not accepted merely because two agents produced it.

The original independent submissions and comparison remain unchanged. The separate sealed runtime artifact `data/research-runs/mechanism-design-20261108-v1/adjudication.json` contains all 120 final provisional assessments, summaries, evidence quotations, all 120 challenge records with both original labels/rationales, and the nine original disagreement records. `human_certified` and `historical_feature_eligible` are both false. Interpretations remain machine judgments; agent separation does not eliminate common-model errors or pretraining contamination.

## Findings

The first pair agreed on 111 of 120 statuses (92.5% descriptive agreement). This is **not accuracy**, sensitivity, specificity, extraction validation or a forecast improvement. The adjudicator assigned 32 present, 74 absent and 14 uncertain statuses. All 32 present decisions have exact source quotations; 35 quoted assessments in total resolve to source text, including three uncertain decisions. These counts describe this small selected design sample only.

A challenge changed one original agreement: both reviewers marked **113-hr4401 / prohibit** present, relying on an exclusion of a referenced subparagraph and the no-deferral heading. The adjudicator retained **uncertain** because the full referenced subparagraph is unavailable and the rubric does not settle removal of applicability versus a separately coded prohibition. This is a documented interpretive challenge, not proof that both original reviewers were wrong.

The nine original disagreements remain traceable and are all retained as uncertain rather than settled by majority vote:

| Bill | Mechanism | Agent A | Agent B | Adjudication rationale |
|---|---|---|---|---|
| 113-hr4401 | authorize | present | uncertain | The Commissioner must choose replacement payment arrangements and may select direct payment if beneficial. The rubric does not determine when an option inside an existing mandatory process is a separate authorization, and displaced law is absent. |
| 113-hr4401 | rename_designate | absent | uncertain | Technical clause redesignation alone is insufficient, but appointing a substitute payee is an administrative designation. The category has not settled whether that effect qualifies. |
| 113-s1772 | authorize | uncertain | absent | The income exclusion expands tax-favored transactions. There is no explicit standalone power grant, but the rubric has not resolved tax permission versus authorization; do not silently equate absence of a programme with absence of authorization. |
| 113-s1772 | prohibit | present | absent | The deduction-denial clause expressly excludes amounts from a calculation. The text is clear, but the category boundary between tax treatment and a separately counted prohibition remains unspecified. |
| 113-s1772 | repeal | absent | uncertain | Replacing a whole paragraph may eliminate limits, but displaced wording is unavailable and the rubric does not define whether replacement itself is repeal. |
| 115-hr4920 | rename_designate | absent | uncertain | Authorization for an honor is not the award itself, but the broad designation category has no explicit rule for named honorary recipients. Preserve that boundary rather than impose an unstated exclusion. |
| 117-hr6116 | require | absent | uncertain | The sanction clause makes violators subject to alternative penalties. Whether exposure to a penalty is a separate affirmative duty is not fixed by the design rubric. |
| 117-hr1352 | repeal | absent | uncertain | Existing acquisition restrictions and temporal limitations are removed or replaced. Whether those removals count as repeal in addition to amendment is not specified. |
| 117-hr1352 | sunset | absent | uncertain | Funding-year ranges are extended while the domestic-material temporal limit is removed. The supplied text does not unambiguously show expiry of a programme; whether finite authorization periods themselves qualify needs an explicit rule. |

The other four uncertain statuses were already uncertain in both reviews: 113-hr4401 / repeal, 114-s2836 / sunset, 116-s4142 / repeal, and 117-hr1352 / rename_designate. They concern missing displaced wording, conditional duration, judicial-doctrine abrogation and naming/category boundaries.

Clear contrasts survived adversarial review: the HHS hiree bill denies rather than grants specified authority; the Medicaid waiver bill preserves permission despite the word “prohibiting”; the medal bill waives a deadline rather than imposing one; and the opioid bill's seven-day supply is a quantity/duration cap rather than a completion deadline. The water bill separately supplies new programme creation, a direct appropriation, expanded permissible spending uses, tax change, prohibitions, duties, reporting and deadlines. A single topic label would lose these distinctions.

## Validator audit

The validator checks reviewer/registration binding, exact bill identity/order, complete mechanism keys, allowed statuses, nonempty summaries/rationales, false certification flags and exact quote substring resolution. The comparison verifies sealed inputs and each sealed submission. Those are integrity checks, not semantic guarantees.

An in-memory adversarial probe supplied the text “This does not authorize spending.” with a deliberately incorrect **present / authorize** label and the exact quote “not authorize”. Structure validation passed, demonstrating that a resolving quotation does not entail the claimed legal effect. This probe did not alter the registered study artifacts.

Additional limits: the validator does not establish that a quote comes from operative rather than title, findings, negated or deleted text; it cannot establish completeness or the truth of absence assertions; it cannot certify reviewer independence, qualification, historical availability or freedom from pretrained knowledge. It uses the first matching quote occurrence, so repeated text can need an explicitly chosen source span. A future semantic audit should preserve clause context and distinguish source integrity from interpretation.

## Proposed rubric work before a new study

These are proposals arising from design work, not retroactive changes to the sealed registration:

- Define whether a discretionary choice nested within a mandatory process or tax eligibility change is a separately coded authorization.
- Separate explicit conduct/power prohibitions, exclusions from calculations, and exceptions to existing applicability; retain the affected actor and exception scope.
- Define repeal at statutory provision, removed limitation and judicial-doctrine levels. Fetch displaced text only under a separately specified, dated source procedure.
- Distinguish administrative designation, named honorary recipients, naming new entities, heading changes and technical renumbering.
- Distinguish affirmative duties from liability to alternative sanctions; define conditional certification/disclosure as distinct from narrative reports.
- Separate action deadlines, effective dates, eligibility dates, quantity-duration limits, waived deadlines and actual expiry. Specify whether contingent waiver expiry and finite spending authorizations are sunsets.

Resolve these definitions on design material, then freeze the extraction procedure before any held-back evaluation. Do not convert uncertain to absent. Do not use the 92.5% agreement as permission to train on these labels or claim that the original human-review protocol has been met. No models were fitted, and no prediction scores or promotion decisions were generated by this adjudication.

## Artifact validation

The existing `validate` helper accepted all ten ordered records and twelve statuses per record and resolved all 35 quotations. A separate completeness assertion checked 120 challenge entries and preservation of all nine original disagreements. Original seals were verified by `unseal` before use. The adjudication was saved with exclusive creation, preserving original submissions.

Adjudication seal: `3e64c643868f9f9ed052de03c0c6cdafee5f3f740e7d7aa17e3822dc2a9bc635`.

Registration seal: `efa0eaf8608f8631a3a59d7d4fbd12a21d2163ea14f739e092d47c35dc3720bf`.

Source review seals: agent A `e8aa34ce6a035d2a3357f344fbde1394c84c2b10608261352413f542d95daa57`; agent B `2da0ebc8505a6e5b53a21699f67d04525377f0433dc0535923b970b16fbf42d9`.
