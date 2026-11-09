# Legislative prediction: primary-source review and next experiment

Reviewed November 8, 2026. This is a targeted methods review, not a systematic review or a new predictive experiment. No model was fitted, no existing gate was changed, and no published score below is directly comparable to Momentum's 60% relative Brier-loss-reduction target.

## Decision

Use mature historical outcomes, including unsuccessful bills, while separating labels from the information available at prediction time. The user’s proposal to work backward is appropriate for assembling supervised-learning examples. It does not authorize using final text, final cosponsor totals or later procedural actions as earlier predictors. Preserve bill language alongside context; begin with the already implemented structured-versus-structured-plus-text comparison, rather than expanding architectures or regex rules.

If exact historical rendition eligibility remains unresolved, a **separately registered retrospective association diagnostic** can measure whether currently retrieved introduced-version text adds signal on later-Congress held-out rows. Its result would remain conditional on reconstructed inputs, unresolved source timing and existing development exposure. It cannot certify forecasts, release E3 gates, meet the publication target or promote a model. Keep the original forecasting protocol immutable. This is a proposed distinct study, not an exception silently applied to E3.

## Studies and what they establish

### Nay (2017): federal enactment probabilities

[Primary paper, methods §§2–3 and Table 1](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0176999).

The study evaluates 68,863 bills, including 2,513 enactments, across seven test Congresses, 107–113 (2001–2015), each trained on earlier Congresses. It separates introduction-time inputs from newest text/metadata. Text models score sentences through word vectors; contextual ensembles combine regularized logistic regression, random forests and boosting, with out-of-fold stacking. The null uses earlier chamber-specific enactment rates. Metrics are Brier loss, log loss and ROC AUC. Combined text/context performs best; the newest-input setting improves substantially. Introduction-time context alone beats text alone. The paper reports infinite log loss for the title-only model. Mean predicted probability near the event rate is not a full calibration assessment. The accessed main methods describe stacking rather than a dedicated later-period calibration set. Exact numerical Table 1 cells were not recovered reliably in this review, so no numerical improvement claim is transcribed. Data pointers are GovTrack and MIT committee records; the article is CC BY. A reusable model-code release/license was not verified. Our interpretation: newest-input results are not benchmarks for introduction-time forecasts; temporal splitting alone does not establish exact source custody or family independence.

### Yano, Smith and Wilkerson (2012): committee survival

[Primary paper, §§3–5 and Tables 3/5](https://aclanthology.org/N12-1097.pdf).

The corpus covers 51,762 House bills in Congresses 103–111 (1993–2010), with 6,828 committee-survival positives. Main training: 45,191 bills, Congresses 103–110; test: 6,571 bills, Congress 111. Inputs use introduced text and sponsor/committee metadata; regularized logistic models add lexical indicators, categories or proxy votes. Test error is 12.6% for majority class, 11.8% metadata, 9.8% metadata plus lexical features, and 9.6% full model. These are classification errors, not Brier losses. Earlier-Congress replication also trains only on preceding Congresses. No separate probability-calibration procedure is established here. The paper documents reserved speaker bill numbers incorrectly treated as failed bills: a concrete label-quality warning. Committee survival is not enactment, and a roll-call-only sample would omit most introduced bills. Our inference: simple lexical features deserve testing before elaborate taxonomies; family/copy separation and precise source-time certification still require independent work.

[Author-hosted corpus](https://www.cs.cmu.edu/~ark/bills/) advertises a 211 MB archive. Its [README](https://www.cs.cmu.edu/~ark/bills/README.txt) identifies per-Congress labels/features and raw downloaded text. The [dataset license](https://www.cs.cmu.edu/~ark/bills/LICENSE.txt) is CC BY-SA 3.0, requiring attribution and share-alike for covered derivatives. It is a candidate for a separately defined historical stage benchmark, not an enactment-label replacement. Download: [Congressional Bill Corpus](https://www.cs.cmu.edu/~ark/bills/Congressional_Bill_Corpus.v1.00.tgz). The archive itself was not downloaded or audited in this review; no preserved-byte timing guarantee is inferred from its publication date alone.

### Eidelman, Kornilova and Argyle (2018): state floor action

[Primary paper, §§3–5, Table 3 and calibration appendix](https://aclanthology.org/C18-1013.pdf).

About one million bills across states, averaging ten sessions per state, include approximately 360,000 floor-action positives; coverage periods vary. The study uses ten-fold cross-validation, not demonstrated chronological future-session testing. Context includes sponsors, committees and bill attributes; text is title/description TF-IDF n-grams, not full bill language. Logistic, NBSVM and boosted models feed an ensemble; NBSVM probabilities use Platt scaling. Averaged across states, metadata-only versus combined accuracy is .846 versus .859, log loss .32 versus .31, and AUROC .82 versus .85. Majority baseline accuracy is .68. Thus the incremental text gain is 1.3 percentage points, distinct from the abstract’s broader baseline comparison. Features are described as introduction-available, but committee referral/effectiveness aggregates and companion status would need cutoff-specific reconstruction in Momentum. No author-released corpus/code license was verified here; the article is CC BY 4.0. Our inference: this supports complementarity, but neither the target nor split supports importing its accuracy as enactment-forecast performance.

### Pal (2022), DeepParliament: Indian bill-status classification

[Primary paper, §§3–8 and Tables 1/4/5](https://aclanthology.org/2022.umios-1.8.pdf).

The English corpus contains 5,329 documents (4,223 train, 1,106 test), sourced from 1986 onward; targets are binary passed/failed and five status classes. Models range from recurrent/convolutional networks to general/legal pretrained transformers. Five seeded runs are averaged. Full-token binary macro-F1 reaches 93.1 for Legal-RoBERTa; multiclass macro-F1 reaches 61.4 for Legal-BERT. These are not probability calibration or Brier-skill measures. The reviewed paper does not establish a chronological split, exact pre-outcome source versions, family-disjoint validation or a dedicated calibration set. It discusses truncation/input-region effects. Our inference: impressive status-classification scores are not evidence of accurate prospective U.S. enactment probabilities. Pretraining contamination would also require investigation before historical forecasting claims.

The [author repository](https://github.com/monk1337/DeepParliament) provides code and data pointers, but no explicit repository license was visible in the inspected root listing/README; reuse permission is therefore unresolved, not assumed. The article’s availability does not license all code/data automatically. No code or dataset from it was imported.

## Available collection routes

[GovInfo's official developer hub](https://www.govinfo.gov/developers) documents bulk congressional text from Congress 113 onward and bill status from Congress 108 onward. These are suitable acquisition starting points. Current availability is not proof of historical availability of current bytes. Preserve document version codes, source URLs, response bytes, retrieval times, hashes and event/effective dates separately. A new observation today can support future custody, not manufacture a past timestamp.

[unitedstates/congress](https://github.com/unitedstates/congress) supplies community-maintained collectors and converters for official bill status, text and votes under a declared CC0-1.0 license. Collector reuse does not establish data provenance automatically. Existing Momentum ingestion should be preferred where it already supplies the same capability.

The legacy CMU archive hostname failed in this review, but the corrected official CMU path above worked. GovTrack’s data page returned an access error to the browser tool. The CMU archive link returned an unsupported binary-content response in that tool; this is not evidence that the archive is absent. No private account, paid dataset or outbound contact was used.

## Smallest informative historical study

This recommendation is analytical judgment based on the literature and Momentum's frozen comparison, not a new execution registration.

1. Freeze one precise question: does introduced-version language add predictive association beyond the same six structured features? Use the existing sparse objective/preprocessing and two arms. Freeze input hashes, memberships, exclusions and fit budget before scores. Do not add categories, embeddings or model searches in response to results.
2. Use completed historical Congresses for mature positive/negative outcomes. Include both classes through a reproducible population rule; do not collect only successful bills or only bills that reached a vote. Distinguish never-introduced placeholders, unresolved outcomes, missing text and genuinely negative labels. Keep census-like class prevalence; outcome-balanced sampling would require its own weighting/calibration design.
3. Split by time and enforce the existing family rules. Identical/reintroduced/companion text can otherwise place the same policy in training and evaluation. Count unique families rather than repeated fold memberships. Learn vocabulary/scaling exclusively from core training rows; do not train on evaluations or model-generated labels.
4. Record every eligible/excluded bill and every unresolved timing issue. With current reconstructed text, label the study retrospective association. Missing historical custody is a limitation of the estimand, not a feature to set to zero. The actual training/evaluation populations and positive counts must come from a frozen manifest, not extrapolation from eight audited cases.
5. Report each fold’s raw Brier/log loss against matched historical-rate and structured controls, positive/negative losses, class counts, expected events and reliability with bin counts. Calibration requires its own adequate earlier sample under the governing study design; do not hide five or fewer positives behind a smooth calibration curve. A diagnostic can omit calibration only through an explicit separate registration, not reinterpret the original protocol.
6. Stop after the fixed comparison, even if negative. The next investment is determined by the measured failure: missing/unstable data, text’s incremental signal, calibration uncertainty or drift. Confirmatory forecasting requires a new untouched population and source/review gates. Sixty-percent relative Brier reduction remains an unproven target.

## Stage, horizon and learning roadmap

The reviewed committee and floor-action papers show why target definitions matter. Momentum should eventually maintain separate registered questions for advancement by a fixed horizon, enactment by session end and conditional advancement from a known stage. Do not pool these as one success label. At a prediction cutoff, unresolved bills are at risk; after a defined observation horizon, outcomes must be matured or explicitly censored. Multiple snapshots of one bill remain dependent observations. Stage counts and time remaining can be useful only when known at the cutoff; the existing exploratory calendar result does not establish text performance.

A defensible self-learning loop means collecting immutable dated snapshots, waiting for verified outcomes, retraining on matured earlier cohorts, testing a challenger on later untouched cohorts and promoting only through a fixed decision rule. It does not mean feeding the model its own forecasts as truth, silently replacing history, or repeatedly optimizing against the same exposed test folds. Larger neural models can be considered later if the inexpensive comparison establishes a robust incremental signal and adequate data. No architecture removes missing provenance or rare-event uncertainty.

## Review limits

Four primary studies were read for targeted decisions, with official/author distribution pages inspected where available. This is not an exhaustive search or replication; no independently recomputed paper results, author correspondence, archive-content audit, exhaustive license audit or new Momentum scores are claimed. Cross-paper numbers differ in target, era, geography, prevalence, splits and metric. Literature does not certify Momentum's source, family, outcome or qualified-human-review requirements.
