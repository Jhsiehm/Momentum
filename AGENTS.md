# Repository workflow

## Standing user instruction

All new Momentum implementation and progress belongs in this repository:
https://github.com/Jhsiehm/Momentum.git

- Commit completed, meaningful changes and push them to this repository as part of finishing authorized work. This is the user's standing authorization; do not ask again for routine commits or pushes.
- Review the diff and run checks appropriate to the change before committing. Do not claim checks passed unless they ran successfully.
- Update `docs/DEVELOPMENT_LOG.md` for each meaningful work batch, recording the date, changes, validation, and any outstanding issue. Update `CHANGELOG.md` for user-visible milestones.
- Keep `README.md` public-facing and accurate. Put detailed implementation and local-workspace history in `WORKSPACE_GUIDE.md` or `docs/`.
- Preserve research protocols, immutable evidence and forecasts, and existing audit gates. Report blocked or negative results honestly.
- Never commit secrets, `.env`, local databases, downloaded runtime data, caches, or private chat history. Commit reproducible code and suitable research summaries; keep runtime artifacts in ignored `data/`.
- Do not force-push or overwrite remote history. If pushing is blocked, preserve the local commit and report the blocker.
- When creating a branch, use the `codex/` prefix unless the user requests otherwise.

Existing research-operation receipts live in `docs/operations/`; keep those alongside the development log.

## Experiment reporting — standing user preference

For every experiment, present detailed results in the user-facing response, not only a short completion summary or a link. Lead with the outcome, then provide the exact question/hypothesis, experiment type, versions and baseline, dataset identity and size, selection/exclusions, configuration and rule/feature changes, metrics with definitions and denominators, before/after and per-category results, review sampling and all shortfalls, observed failures, uncertainty and leakage/design-exposure limitations, actual validation and independent-review results, and what the findings do and do not establish.

Keep a complete, readable execution receipt in docs/operations/runs/. Include per-bill/per-case results and all reviewed error cases when applicable. Link the exact registration, full results, review/evidence records, code, reproduction commands and immutable artifact hashes so the user can inspect every recorded detail. Do not substitute unit-test success or locator coverage for semantic/predictive accuracy. Explicitly state when no model fitting or predictive test occurred. Do not claim unmeasured details (including timing/cost) were recorded.

Preserve raw runtime artifacts in ignored data/; do not publish private data or secrets to satisfy reporting detail. Record known failures and negative results without post-result tuning or silent replacement. Honor requests for a shorter response on an individual turn without weakening the complete saved receipt.
