# Scheduled research and three-round audit workflow

Requested November 5, 2026. Local-only, every two hours throughout the day. The Codex heartbeat is the scheduler; this file does not itself execute jobs.

Each run reads this file, INTELLIGENCE_ROADMAP.md, prior run receipts and lessons.md. Inspect repository changes and live agents first; do not run competing writers or duplicate an active research job. Resume the saved checkpoint.

## Round 1: evidence and design
Assign an evidence auditor and a methods auditor. Check source availability, dataset separation, dates, outcomes, family overlap, sample denominators, previous outcome exposure and registered comparison. Each review includes evidence paths, concrete findings and unresolved questions. Agent judgments remain agent audits; they cannot complete designated human audit receipts. Identify one bounded research advancement with measurable acceptance criteria.

## Research execution
Acquire/cache missing official evidence in resumable, rate-limited batches. Prepare human review packets when necessary. Implement scoped workflow fixes with focused regression checks. Freeze new designs before inspecting new evaluation results, run eligible comparisons, preserve failed/negative outcomes and baseline scores. Never retune against protected evaluation data or count reruns as independent learning. If evidence blocks scoring, progress acquisition, provenance or review tooling instead of repeatedly rerunning the blocked experiment.

## Round 2: independent implementation and result review
Use reviewers other than the implementation author to inspect code changes, numerical outputs, temporal leakage, reproducibility and user-facing claims. Include runtime/API health and affected desktop/mobile workflows when browser policy permits. Record failed checks and fix actionable defects. Do not claim all modules were audited when only a subset was inspected; maintain rotating coverage of ingestion, storage, modeling, learning, scheduling, API/chat, UI and exports.

## Round 3: verification and release decision
An independent verifier checks the fixes against original findings, reproduces eligible results offline, checks relevant tests and confirms that evidence gates and frozen studies remain intact. Record unresolved findings. Failed verification blocks model promotion and unsupported success claims; save a next-run repair checkpoint. Do not silently call a skipped round passed.

## Run receipt and continuity
Save docs/operations/runs/<UTC timestamp>.md: scope, source/code/input hashes where applicable, assigned agents, three round verdicts and evidence, changes, commands/test outcomes, new evidence versus reused evidence, metrics versus baselines, limitations, blockers and next action. Maintain docs/operations/status.md as the current checkpoint. Update lessons.md only with substantiated mistakes, root causes, fixes and prevention checks. Read those checks before future related edits; this is procedural memory, not model-weight training.

Keep existing frozen research modules/results unchanged. New research uses versioned modules/protocols. No fabricated human approvals, public deployment, credential disclosure, external messages or unbounded paid model calls. Existing explicit budgets remain in force. Keep runs bounded and resumable; do not start a second expensive batch while one is active. End idle runs without cosmetic churn.

## Autonomous learning mandate — November 5, 2026

The user authorizes routine local evidence acquisition, eligible training, testing, audit, and logging without repeated input. Continue through reversible implementation choices autonomously. Preserve designated human audit fields: an agent must never impersonate a human reviewer. When a frozen protocol needs human adjudication, record the precise blocker once and pursue independent evidence/provenance work or a separately registered agent-audited development track with honest limitations. Never weaken a frozen study to obtain a number.

On each two-hour cycle, inspect `GET /api/learning`, `/api/autoresearch`, monitoring and active import/research jobs. Resume the checkpoint; skip unchanged inputs and avoid overlapping writers. Start the existing local server if absent using the documented launcher. Keep the current worker budgets (three experiments per cycle, twelve per UTC day) and source-refresh settings; these are maxima, not targets. Bound new acquisition to at most 100 official bill records per audit cycle, process sequentially with retry/backoff and retained source hashes, and stop at a resumable checkpoint on persistent source failure. Do not introduce new paid provider usage.

Prioritize the missing historical snapshots, outcome labels and family evidence needed for valid training. For newly eligible evidence, freeze a new development session and train the local forecasting model through the existing session workflow. Record weights, scaling, feature/version identifiers, training membership, cutoff, label availability and source/code hashes. Preserve prior artifacts and all negative results. Never change a hosted chat model's weights or imply that prompt memory is weight training.

Independent auditors must check temporal leakage, train/validation/test separation, class counts, family overlap, exclusions, same-case baseline comparisons, Brier and log loss, calibration, reproducibility and data drift where measurable. Report unavailable metrics honestly. Repeatedly inspected evaluation data is development evidence. Reserve a separately registered later evaluation set before selecting candidate models; uncertainty and practical effect size must be reported before claiming improvement. Live forecasts remain on their existing implementation until a separately specified release gate is implemented and independently passed; audit success by itself does not promote a model.

Every executed cycle writes a durable receipt, even if blocked, failed or unchanged. Include acquisition attempts and failures, evidence hashes, model artifacts or exact no-training reason, actual independent auditor identities/verdicts, tests, scores and baseline, release decision, resource usage when available, and next checkpoint. Use timestamped files under `docs/operations/runs/`; update `docs/operations/status.md`. Do not copy credentials, full environments or private chat contents into logs. Quiet cycles still log locally. Notify only on material progress, a measured result/regression, a new failure, or a decision that cannot be resolved within the authorized scope.

### Shared run lease

Before research mutations, run `python3 -m engine.research_lease acquire <unique-run-owner>` and proceed only when `granted` is true. Use a unique chat/run identifier, never a shared constant. The default lease expires after 30 minutes; renew at least every 10 minutes and before mutations with `python3 -m engine.research_lease renew <unique-run-owner>`. If renewal fails, stop writing and defer. Release in cleanup with `python3 -m engine.research_lease release <unique-run-owner>`. SQLite transactions exclude other cooperating scheduled agents across processes; expiration permits crash recovery. This cooperative lease does not lock the application's own workers, so separately inspect active import/research jobs and avoid overlapping datasets or code changes while they run. If work remains active beyond lease expiry, do not blindly take over; verify no prior writer is still working.
