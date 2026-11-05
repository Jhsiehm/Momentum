# Controlled three-model historical comparison — November 5, 2026

## Registered question and model isolation

Test whether simple calibration or additional training data improves the existing original-data survivor under identical evaluation conditions. The target remains own-bill public-law enactment before Congress end, using publication-based evidence at day180. This is separate from the day30 originating-chamber passage benchmark.

All models, training rows, candidate identities, code dependencies and selection rules were frozen before new evaluation source acquisition:

1. Original structured L2 .2 survivor:49 training bills from Congress114/116, one enactment; artifact must exactly match the earlier survivor.
2. Original survivor plus monotone affine-logit calibration:149 other Congress116 training bills, five enactments, no original-training family overlap. Formula `sigmoid(a + b*logit(p))`; initialize `(a,b)=(0,1)`,2,000 full-batch gradient steps, learning rate .1, identity-anchored ridge .01, nonnegative slope. No parameter search. Fitted intercept .05556415334242551; slope .9501182101874305.
3. Retrained structured L2 .2 model:all198 available training bills, six enactments; same features and fitting procedure as survivor.

The calibration sample is previously exposed development data but was not used to train the original survivor. It does not use the preceding736-case118th-Congress evaluation: using those later outcomes to fit historical predictions would break the temporal boundary. Training labels' audited latest availability is2021-05-08, before evaluation cutoffs.

Fixed sample:1,000 IDs drawn without replacement from14,413 remaining118th-Congress candidates, seed202611053000. Exclude all locally imported, previously acquired and registered candidate identities before sampling. Score every source-eligible case, excluding known training/prior-exposed family overlaps and duplicate selected families in frozen order. All three models use precisely the same rows. No replacement, outcome enrichment, early stopping or tuning. Any required source failure blocks all scoring. A newly discovered link between original and calibration families also blocks scoring without refitting.

Primary comparisons are paired Brier differences, calibrated minus original and retrained minus original. Each uses2,000 family bootstrap replicates, seed20261024. Intervals are conditional on fitted models and this Congress. These are two exploratory comparisons without multiplicity-adjusted confirmatory claims. Log loss, reliability and outcome-specific scores are secondary. The original49-row smoothed rate2/51 is a shared reference.

Protocol hash: `7e944396419205c002b41c9669416201ae4cf4a197da9dbd0fbff0653943dd33`.

## Reproduction and scope

Runtime bundle: `data/research-runs/three-model-20261105/` (ignored). `python3 -m engine.three_model_experiment --offline` reconstructs acquisition/selection/scoring against frozen artifacts and dependency hashes. `python3 -m scripts.verify_three_model` separately recomputes all prediction arithmetic, Brier/log loss and paired intervals, checks source bytes/hashes, and verifies training-label availability. Frozen dependency source copies are retained in the local bundle.

This is a historical development follow-up, not untouched final or prospective validation. Earlier broad calendar exposure, repeated same-Congress experiments, rare training positives, incomplete family linkage and publication-proxy limitations remain. Machine verification is not independent human certification. No production promotion, paid calls or schedule changes are authorized by a favorable result alone.

## Results

All1,000 source audits succeeded.696 unique eligible families scored, including10 enactments and686 negatives.304 exclusions:163 checkpoints at/after Congress end,115 known prior/training family overlaps,16 duplicate selected families,6 missing introduced publications,4 already enacted at checkpoint. Acquired3,320 source documents totaling127,314,322 bytes.

| Model | Brier (lower better) | Log loss | Brier change versus original |
| --- | ---: | ---: | ---: |
| Original survivor | 0.0135454378 | 0.0701926240 | reference |
| Calibrated survivor | 0.0136565951 | 0.0738036506 | +0.82% (worse) |
| Retrained198 | 0.0140835036 | 0.0769764455 | +3.97% (worse) |
| Original training-rate reference | 0.0147787986 | 0.0859632817 | — |

Calibrated-minus-original Brier difference +0.0001111573; conditional95% interval[-0.0000881515,+0.0002778303]. No calibration improvement established; uncertainty includes zero. Retrained-minus-original difference +0.0005380658; interval[+0.0001956504,+0.0009958723], favoring the original within this batch. Original beats the rate reference by8.35% Brier, descriptively. Both challengers also have worse log loss.

The frozen adjustment raised probabilities: among687 original low-bin cases, original mean2.39%, calibrated3.02%, observed7/687=1.02%; among9 higher-bin cases, original11.91%, calibrated13.64%, observed3/9=33.33%. It moves the higher group toward its observed frequency but worsens the large low group. This is a post-evaluation explanation, not a newly tested calibration rule. Nine higher-bin cases remain too few for a robust general conclusion. Retrained probabilities all fall below .1.

## Verification and delivery

36 focused tests passed. Full offline replay exactly reproduced frozen acquisition, selection and result. Separate verifier reproduced all2,088 model probabilities, Brier/log loss and both2,000-replicate paired intervals; verified all3,320 source SHA-256/lengths, original-model identity and earlier-label availability. This is reproducibility and machine verification, not independent human certification.

Result hash: `acfc368b255ba8ce9cdd2c95e907367e1a56b740b3013fec3bf09244b482c1ac`.

The original survivor remains the retained research model. Neither challenger is promoted. This experiment tests two frozen updates and finds no improvement; it does not demonstrate automatic learning. Preserve all696 scored cases as exposed development evidence. A next learning experiment needs stronger representative training evidence and a separately registered time-period evaluation; further reuse of this Congress cannot become untouched validation.

Platform delivery completed: all1,000 current BILLSTATUS XMLs imported at actual observation time; ten100-bill collections, full comparison report, three component reports and verification report saved. All five report API endpoints verified. Platform chat: “Controlled comparison · survivor, calibration, retraining”. No paid calls, schedule changes or model promotion.
