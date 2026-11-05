# Autonomous learning checkpoint

Updated November 5, 2026 after a completed full research cycle.

## Completed

- Three independent audit rounds completed: evidence/methods, results review with correction, offline verification. Receipt: `docs/operations/runs/20261105-full-learning-cycle.md`.
- New official evidence: five GovInfo source documents. Final 114th House calendar enumerates all 329 originating laws and matches the retained NARA census. Calendar available March 24, 2017; sampled positive law date proof available May 19, 2016. Both predate July 16, 2019 inner validation. This unlocks a separately registered publication-based adaptive diagnostic, not existing human/action-history gates.
- Real historical diagnostic: 23 training/1 enacted, 30 validation/1 enacted, 33 evaluation/0 enacted. Selected context hashing/L2=.01 on prior validation only. Adaptive Brier .00455711; fixed .00605899; baseline .00297521. Adaptive improved fixed but loses to baseline. Both bootstrap difference intervals include zero. No promotion.
- Synthetic chronological check: 15 targets/6 enacted, 240→300 resolved training cases. Before Brier .22643566→after .22688385 (worse). Adaptive .26081357 also worse than fixed and baseline. Machinery works; no improvement claim.
- All six inner candidate weight artifacts retained in supplementary audit; independent reviewer verified correction. Official/demo/supplement reproduce exactly. 26 relevant tests pass. Frozen studies unchanged.
- Artifacts and full scripts: `data/research-runs/full-cycle-20261105/`. Saved local platform chat/report: “Full learning cycle · November 5 · audited results”. Demo session visible in Model learning.

## Next cycle

Freeze a broader outcome-blind temporal cohort with sufficient naturally occurring enactments and a separately protected later evaluation before fitting/selection. Reuse the new 114th proof only in a new protocol; preserve all old studies. Do not optimize again on the exposed 33-case all-negative diagnostic. Acquire missing historical/family evidence; agent review must not impersonate designated human approval. Keep comparative baselines and negative learning results.

## Scheduling

One existing Codex heartbeat every two hours; local worker hourly, at most 3 experiments/cycle and 12/day; source refresh hourly. Acquire unique shared research lease, inspect active jobs and preserve budgets. Local server required. Live forecasts unchanged; no hosted language-model fine-tuning or paid provider calls were used.
