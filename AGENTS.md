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
