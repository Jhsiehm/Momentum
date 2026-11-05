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
