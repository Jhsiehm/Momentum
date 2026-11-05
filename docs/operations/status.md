# Latest controlled three-model comparison

November5,2026. Receipt: `docs/operations/runs/20261105-three-model.md`.

Completed1,000 new source audits;696 eligible bills,10 enactments. Models and candidate identities frozen before acquisition. Original49-row survivor Brier0.01354544; calibration on149 separate earlier bills0.01365660 (+0.82% worse); retrained198-row model0.01408350 (+3.97% worse). Calibration paired95% interval includes zero; retraining interval favors original within this historical batch. Neither update improves the retained survivor.

36 tests, exact offline replay, separate2,088-probability/score/bootstrap verification and3,320 source checks passed. Saved five reports and ten collections in platform chat “Controlled comparison · survivor, calibration, retraining”; all1,000 imports retain actual observation times. Preserve original; no promotion or schedule changes. These are exploratory same-Congress development results, not prospective validation or proof of self-improvement. Next learning research needs stronger representative training evidence and a separately registered time-period evaluation.

# Latest high-volume experiment

November5,2026. Receipt: `docs/operations/runs/20261105-survivor1000.md`.

Completed1,000 new-candidate source audits with zero failures;736 eligible cases,16 enactments,264 exclusions. Exact49-row original-data survivor weights unchanged. Brier0.01995385 vs rate0.02157197 (7.50% lower); paired conditional95% difference interval[-0.00264608,-0.00072374]. This supports a within-batch advantage over baseline, not automatic learning or cross-Congress validation.

Calibration lead:13 higher-probability cases averaged11.73% but6 enacted (46.15%);723 low-probability cases averaged2.41% with10 enactments (1.38%). Do not tune and rescore this now-exposed batch as fresh validation. Next study should preregister calibration and independent evaluation. Existing historical-action/family/human gates remain.

Six new tests, exact offline replay, direct736-case arithmetic,3,298 source checks and repeated bootstrap passed. Saved ten collections and two reports; all1,000 current imports retain actual observation times. Scheduled settings unchanged; no promotion. Runtime bundle: `data/research-runs/survivor1000-20261105/`.

# Latest requested experiment: original-data survivor on20 bills

November5,2026. Receipt: `docs/operations/runs/20261105-survivor20.md`.

Scored20 eligible bills from a preregistered40-candidate screen using the exact49-row trained L2 .2 survivor, with no updated prediction weights. Eight late checkpoints and two prior-family overlaps excluded; ten eligible surplus cases unscored. Brier0.00054515 versus rate baseline0.00153787. All20 outcomes negative; no enacted-case discrimination or general improvement established.

Offline replay and independent arithmetic passed;130 source documents verified. Two reports and a20-bill collection saved in the platform. All40 screened cases are now exposed; preserve original artifacts. No production promotion or schedule change. Day180 enactment remains distinct from the blocked day30 passage workflow below.

# Latest outcome audit: negatives

November 5, 2026. Receipt: `docs/operations/runs/20261105-negative-passage-audit.md`.

Audited738 unresolved outcomes plus64 positive controls using five final calendars and full retained BILLSTATUS action lists. Source-reviewed12 exact pending-calendar cases into negative labels;10 have day30 publication proxies. All positives remained outside the negative set. Remaining726 unresolved outcomes and18 prior source failures retained. Labels are available only at the current audit time, not retroactively; zero independent human certifications.

23 focused tests and exact offline replays passed. Original JSON key-order replay failure corrected in a canonical revision with unchanged evidence and preserved initial artifacts. Three platform reports saved and API-verified. No scoring, production or schedule changes. Historical action features, early-Congress coverage, representative negatives and family/human gates remain outstanding.

# Latest evidence acquisition

November 5, 2026. Receipt: `docs/operations/runs/20261105-passage-evidence.md`.

Audited802/820 fixed bills;18 HTTP404 source failures. Produced64 machine-corroborated passage positives and584 day30 publication-proxy records;32 bills have both. Verified2,664 retained sources and reconstructed802 successful rows offline. Fourteen focused tests passed; three platform reports saved and checked.

These are preservation-bound publication proxies, not complete historical actions or human-certified labels. No certified negative labels. No day30 proxy rows in110/111, seven in112. Sequential scoring remains blocked pending complete negatives, sufficient early-Congress evidence, family/human review and action-history provenance. Do not backdate official records or use exposed samples as fresh validation.

# Latest execution: updated sequential practices

November 5, 2026. Receipt: `docs/operations/runs/20261105-sequential-practices-execution.md`.

The active day-30 originating-chamber passage workflow was executed. Official snapshot: 11,092 bills; no audited passage labels; no historical day-30 checkpoint metadata in available evaluation Congresses. All six113–118 folds blocked; no official scores or model fitted. Nineteen119th-Congress checkpoints exist outside this benchmark. Earlier110–112 training coverage is absent.

Separate synthetic check: 1,080 simulated bills, six folds, four comparison methods, exact replay passed. Eight tests and independent checks of24 synthetic Brier scores passed; three reports saved and API-verified. This does not establish real forecasting improvement. No promotion or schedule changes.

Next prerequisite: source-audited passage labels and historical checkpoint evidence, plus early-Congress coverage and the documented research gates. Do not substitute prior enactment labels or backdate modern source imports. Prior expanded experiment findings remain below as historical context, not the active target.

# Autonomous learning checkpoint

Updated November 5, 2026 after the expanded700-bill/10-candidate batch.

## Latest completed batch

Receipt: `docs/operations/runs/20261105-expanded-experiments.md`; runtime: `data/research-runs/expanded-experiments-20261105/`.

- All700 new bills audited without source failures;2,334 source documents retained. Seeded200 training candidates plus250 development/250 confirmation; no replacements.
- After eligibility/family separation: training198/6 positives, development194/1, confirmation181/2 across180 families. Original-only comparator49/1;149 new training rows added.
- Ten predefined variants fitted; X2 structured L2 .05 selected on development and saved before confirmation. Confirmation Brier: selected .01040158, expanded survivor .01096349, original-only survivor .01034320, historical rate .01150124.
- Selected vs expanded survivor improves5.13% descriptively, but95% paired interval crosses zero, as does selected vs rate. Added training worsens survivor Brier6.00%; conditional worsening interval narrowly excludes zero. No automatic accuracy-improvement claim or promotion.
- Independent design, implementation and numerical verification passed. Full isolated offline replay reproduced frozen results exactly. Full dependency bytes retained during unrelated concurrent workspace changes.
- All700 source XMLs imported at actual observation times; seven collections and12 clickable reports saved in local chat “Expanded experiments · 700 bills · 10 models · audited results”. All12 report endpoints verified.

## Next cycle

All500 new evaluation candidates are now exposed evidence. Do not reuse them as fresh validation. Register a later independent Congress, investigate calibration/base-rate shift, and use enough natural positive outcomes. X2 is a candidate hypothesis only. Preserve human/action-history gates and historical provenance limits. More observations or fitted weights do not guarantee better accuracy; this batch demonstrated negative transfer from added training.

## Schedule and budgets

Existing hourly workers and two-hour heartbeat unchanged. User authorized this manual700-bill/10-candidate batch only; scheduled3/cycle and12/day limits unchanged. No paid calls or live promotion. Shared lease acquired/renewed and released after completion.

## Previous studies

Earlier receipts remain in `docs/operations/runs/20261105-five-experiments.md` and `20261105-full-learning-cycle.md`. Their evaluation samples remain exposed development evidence.
