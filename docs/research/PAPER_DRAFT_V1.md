# Learning legislative enactment probabilities across Congresses

Working paper draft, version 1, 2026-11-05. **Exploratory findings with prospective validation pending.** This is a substantive methods/results draft, not a claim of a completed confirmatory study. Numerical statements below refer to repository receipts. External literature and source semantics still require verified citations.

## Abstract

We investigate whether statistical models trained on historical U.S. congressional evidence improve probabilities of a bill's own public-law enactment by the end of its Congress. The prediction task is conditioned on a bill remaining unenacted 180 days after introduction. Momentum preserves official-source evidence, dated feature and label eligibility, frozen models, family-separation rules and failed experiments. A historical campaign audited 30,500 candidate bills and selected a calibrated model across four chronological development folds. On a subsequent identity-separated but historically exposed comparison of 2,315 eligible bills with 29 enactments, its Brier loss was effectively tied with a frozen 49-case survivor. Later development experiments found that weaker regularization improved period-specific controls across three exposed Congresses, and a separate candidate was frozen after training-convergence checks. These results do not establish independent predictive improvement. We specify a prospective paired evaluation with historical-rate and stage-aware baselines, explicit provenance gates and dependence-aware reporting. Independent source/family certification and prospective issuance infrastructure remain prerequisites.

## Introduction and motivation

Legislative forecasts must specify what success means and when information was available. A bill may advance procedurally without becoming law, or its provisions may appear in another vehicle. This study addresses only a bill's own public-law enactment before the end of its Congress. It does not estimate policy impact or provision-level success. The day-180 checkpoint defines a conditional population of bills still at risk; bills enacted earlier and introductions too late to reach the checkpoint are outside this estimand.

Probabilities are evaluated with proper scoring rules rather than a single classification-accuracy figure. Because enactment is rare in the audited samples, a model can appear accurate while assigning nearly every bill a small probability. Historical-rate and stage-aware comparators are therefore central: complex learning should improve on simple information available at forecast time. TODO: verify and cite primary methodological sources for proper scoring rules, rare-event evaluation and calibration; no citation is claimed here.

Momentum's research history also illustrates why larger training sets and more elaborate models cannot be equated with progress. Some expanded or updated models worsened Brier loss, and repeated within-period comparisons exposed the same outcome environment to model development. Our contribution at this stage is a reproducible account of these results and an explicit boundary between exploratory development and independent validation. TODO: literature review before claiming novelty of this contribution.

## Related-work questions requiring source verification

The following are research questions, not fabricated references:

- Which primary studies predict U.S. bill enactment, at what checkpoints, and with what outcome definitions? Distinguish introduction-time forecasts, rolling forecasts, passage and provision incorporation.
- Which studies use random splits versus chronological Congress splits, purge related/reintroduced bills, and preserve point-in-time source vintages?
- What role do procedural stage, text, sponsor characteristics and political context play relative to credible simple baselines? Are input timestamps and final-outcome contamination assessed?
- Which calibration and rare-event methods have been validated under temporal distribution shift? What are their assumptions and limits with few positives?
- Which uncertainty methods handle bill-family dependence and few period clusters? Distinguish conditional fitted-model comparisons from inference over future Congresses.
- What do the official GovInfo/BILLSTATUS specifications establish about retrospective updates, publication versions and preservation-event dates? Historical availability and byte identity are different claims.

TODO: for each included paper, verify the primary text, authors, year, DOI/URL, exact target, split, feature vintage, baseline and metric. Populate a comparison table only after verification. No external empirical claim in this draft relies on an unverified reference.

## Research hypotheses

The central question is whether a model learned from earlier congressional evidence improves later day-180 enactment probabilities. The proposed confirmatory study tests the frozen weaker-penalty candidate against the survivor and two prespecified baselines. Practical success requires at least a 2% Brier reduction against all three under the simultaneous conditional procedure in [the paper protocol](PAPER_PROTOCOL_V1.md), consistent per-period direction and no worse secondary log loss. The user's long-term 60% reduction ambition is not a stopping criterion or promised effect.

A fixed-artifact prospective comparison can support transfer of learned information. It cannot isolate the causal contribution of each added training example, nor establish that automatic updating will improve indefinitely. Existing chronological updating studies are analyzed separately as exploratory evidence on that narrower mechanism.

## Dataset construction and temporal safeguards

The source pipeline uses official bill identity records, introduced and later text publications, metadata and preservation records, final public-law calendars and law-specific evidence. The 113–118 inventories contain 75,605 H.R./S. identities in total. The campaign audited 500 feasibility candidates, 25,000 development/reserve candidates and 5,000 later comparison candidates. The 10,000 reserve was triggered by prespecified usable-positive counts before fitting, not by forecast performance. These are candidate audits, not 30,500 scored or independently sampled outcomes. [Campaign receipt](../operations/runs/20261105-cross-congress-campaign.md).

For each eligible record, the historical implementation constructs a checkpoint at introduction plus 180 days and uses only publication constituents with effective and bounded availability dates at or before it. Its six inputs summarize publication stage, fixed bill age, publication count, time since available publication, chamber and recent publication count. Complete law censuses support negative labels; individual positive laws require identity/date proofs. Missing evidence remains missing. Current BILLSTATUS imports retain their real retrieval times and are not backdated into historical snapshots.

The evidence has important limits. Preservation events do not establish that today's rendition bytes are identical to the historical version. Publication versions proxy procedural actions. Family linkage combines available related-bill records and title heuristics; it is not a certified genealogy of shared provisions. The final paper must distinguish automated integrity checks from human provenance certification. TODO: complete source/family review, release an auditable denominator flow and document the reproduction bundle's licensing/access conditions.

Training in chronological folds precedes the evaluation Congress and requires labels knowable before the earliest evaluated checkpoint. Known overlapping families are removed. Core and calibration subsets are disjoint under the available graph. This ordering prevents direct use of future labels for a given fit, but does not undo repeated development exposure. Congresses 113–118 have influenced the current research direction. Newly scored 118 identities are not an untouched temporal test. [Readiness audit](VALIDATION_READINESS.md).

## Statistical methods

The survivor is a structured logistic artifact trained on 49 retained original bills from 114/116, with one enactment, L2=0.2 and 300 gradient steps. Its lineage is an original-only refit in the expanded experiment, subsequently frozen. Earlier uses of “survivor configuration” must not be conflated with this exact artifact.

The campaign compared five fixed training strategies across chronological development folds and selected calibrated all-history by mean fold Brier skill relative to the training-rate reference. Calibration uses a monotone affine transformation of the logit, with disjoint calibration rows. The final campaign fit uses 11,871 family representatives with 281 enactments; 9,496 train the base and 2,375 calibrate it. [Campaign receipt](../operations/runs/20261105-cross-congress-campaign.md).

The later research candidate retains those final memberships and six features, changes L2 to 0.05, and uses a training-only penalized-gradient stopping rule. Both weaker and stronger controls reached a maximum absolute gradient of 1e-6 after at least 300 and at most 20,000 iterations. The final weaker base reached tolerance at 3,917 iterations. Calibration retains the existing fixed 2,000-step procedure; its convergence was not established by the base criterion. An initial vectorized arithmetic warning led to a preserved, explicitly documented einsum rerun with finite-value assertions; the accepted run's probabilities differed by at most 6.94e-16. [Convergence receipt](../operations/runs/20261105-convergence.md).

The planned independent comparison freezes both learned artifacts and adds two earlier-only references: Beta(1,1) historical rate and stage-specific rates shrunk with five pseudo-observations toward that rate. All four methods use identical evaluation cases. Brier loss is primary; Brier Skill Score reports relative loss reduction against each comparator. Log loss, fixed-bin reliability, event-specific error, expected events and coverage are secondary.

The planned analysis weights Congresses equally and resamples paired global family clusters, retaining all bill/period memberships. Simultaneous intervals address the three prespecified practical-effect comparisons. This conditions on the models and observed periods. With only two future Congresses, a reliable population-level Congress-cluster confidence claim is unavailable; the paper will show each period and disclose that limitation rather than substitute bill-level independence. Positive-event minima are readiness rules, not statistical power guarantees. Full methods, including negative and inconclusive decisions, are fixed in the protocol and await a verified clustered implementation.

## Existing exploratory findings

| Comparison | Evaluated cases / enactments | Finding |
| --- | --- | --- |
| Fixed survivor versus its rate reference | 736 / 16 in 118 | Brier 0.019953854 vs 0.021571971; 7.50% lower within this historical batch |
| Calibration and retraining versus survivor | 696 / 10 in 118 | Calibration Brier 0.82% worse; retraining 3.97% worse |
| Campaign selected challenger versus survivor | 2,315 / 29 in 118 | Brier 0.012143970715225 vs 0.012144114714759; essentially tied |
| Chronological updates | 8,568 / 182 across 115–117 | Every tested update improved two periods and worsened one |
| Converged L2=0.05 versus period-specific L2=0.2 | Same exposed 115–117 rows | Mean period-relative Brier improvement 8.3911%; all three directions favorable |

Sources: [survivor batch](../operations/runs/20261105-survivor1000.md), [three-model comparison](../operations/runs/20261105-three-model.md), [campaign](../operations/runs/20261105-cross-congress-campaign.md), [chronological updates](../operations/runs/20261105-chronological-weight-updates.md), [convergence](../operations/runs/20261105-convergence.md). These rows reuse data and are not independent replications.

The campaign's paired conditional 95% difference interval, [−0.000179614233499, +0.000214936935199], includes zero. The descriptive Brier reduction is only 0.001186%, below its 2% threshold, and 29 enactments fall below its 50-positive gate. A 1.98% log-loss reduction does not change the primary conclusion. The survivor was retained.

Subsequent stage audits found overprediction among introduced-document groups and underprediction among passage-document groups in three periods. Weaker regularization improved those development comparisons, but this is not proof of a causal mechanism or superiority over the survivor. The 8.3911% value is a mean of relative gains against period-specific controls, not an accuracy percentage-point increase, a pooled independent effect, or a survivor comparison. The challenger remains a hypothesis to test.

The earlier expanded experiment also preserved a negative result: expanded survivor training worsened confirmation Brier by 6.00% relative to the original-only refit; the selected weaker-L2 model did not beat that original-only comparator. This cautions against describing additional data acquisition as automatic self-improvement. [Expanded experiment](../operations/runs/20261105-expanded-experiments.md).

## Limitations and planned validation

The largest limitation is exposure: no audited historical period remains established as an independent forward test of the selected candidate. Rare positive outcomes, repeated model comparisons, incomplete family graphs and conditional uncertainty compound this issue. Point-in-time publication provenance remains bounded rather than fully certified. Missing and excluded records can alter the target population, and the constant day-180 age feature carries no within-fold discrimination. Model convergence addresses numerical optimization only.

We therefore propose prospective shadow forecasts across Congresses 120 and 121, with the protocol and models frozen before 120 opens, actual dated paired issuance, independent outcome custody and no interim adaptation. The study must preserve late/missing forecasts and wait for closed-horizon labels. No such forecast has been generated by the present preparation, and the existing arbitrary-age live capture cannot be relabeled as this experiment.

TODO before submission: external preregistration; independent source/family review; custodian and timestamping arrangements; verified prospective adapter and clustered analysis; acquisition and exclusion flow; independently executable numerical verifier; reproducibility bundle; verified literature citations; and completed prospective results. If those results are negative or inconclusive, report them without changing the objective or extending the sample until a favorable result appears. The current defensible conclusion is a reproducible development lead with independent efficacy unestablished.
