# Agent Usage Guidance

Use this guidance when adding Nenrin to `AGENTS.md`, `CLAUDE.md`, project instructions, or a skill.

Command examples below assume the `nenrin` CLI is already installed or available
on `PATH`. In a fresh checkout, use `uv run nenrin <command>` or install the
editable package first.

## Minimal Rule

```md
## Nenrin Usage

Use `nenrin/` as the improvement observation ledger for agent-facing workflow changes.

Create or update a Nenrin change record when you make a durable change to:

- agent instructions
- skills or `SKILL.md`
- handoff format
- roadmap or release checklist
- QA gates or review criteria
- recurring automation or workflow guidance

When implementation, verification, or real use shows that the roadmap or
related docs no longer match the best next direction, update the relevant doc
in the same small slice. Keep that update evidence-based and directly tied to
the work at hand.

After related work, create an observation record when an active change affected the task.

Prefer keep, remove, merge, narrow, move-to-skill, move-to-handoff, or move-to-checklist decisions over adding more permanent rules by default.

Nenrin is a pruning tool, not a work generator. Prioritize overdue review, recurring failure verification, active-record hygiene, and evidence quality. If there is no actionable signal, make no changes and report the no-op as a normal result.
```

## When Not To Record

Skip a Nenrin record for:

- typo or formatting fixes
- one-off task notes
- implementation-only changes that do not affect future agent behavior
- temporary instructions that belong in the current handoff only
- duplicate records where an existing active change already covers the behavior
- version history already captured clearly in `AGENTS.md`, changelogs, or roadmaps unless there is a specific future behavior to observe
- `nenrin diff` findings that are small wording churn or docs maintenance with no durable behavior change

## First Files To Read

For an existing ledger, read:

1. `nenrin/index.md`
2. active records in `nenrin/changes/`
3. Run `nenrin brief` to get active observation context in one screen
4. Run `nenrin metrics` and `nenrin debt` when deciding what to review

If `brief` is too long to act on, narrow from review due dates, recurring failures, recent related work, or `diff` relevance. Do not read every active record just to satisfy process.

Keep observations short and evidence-oriented. Do not turn the ledger into a transcript archive.

Treat record pressure as a signal. If a run creates another change record
without a clear future observation or review trigger, stop and ask whether the
correct outcome is no-op, a short observation on an existing record, or a
roadmap/docs clarification instead.

## Judgment Rules

Keep status and impact values small. Do not add new states such as `validated`, `proven`, or `invalid` just to express confidence. Put the evidence in the record body instead.

Use `effective` only when the evidence shows behavior changed, such as:

- the next command changed
- context gathering moved from broad discovery to targeted active-record review
- the cleanup choice narrowed from adding guidance to reviewing, pruning, or moving it
- a recurring failure became a concrete fix or review decision

Reading a record, creating a record, or noticing a possible issue is not enough by itself. If the signal is weak, leave the change impact as `unknown`, mark the observation `impact_judgment` as `unknown` or `partially_effective`, and say what must be watched next.

No-failure placeholders are not debt. They also are not proof of success. If there is no failure but no behavior evidence either, keep observing rather than upgrading the judgment.

## Review Commands

- `nenrin review` lists overdue changes.
- `nenrin review --create` generates review templates for each overdue change.
- `nenrin review --apply` reads completed reviews and updates the related change's `status` and `impact` based on `final_judgment` (e.g., `keep` → `reviewed`/`effective`, `remove` → `archived`/`ineffective`). Unsupported values warn and leave the change unchanged.
- A review with `final_judgment: keep_observing` keeps the change active but resets the overdue window; later observations or elapsed days can make it due again.
- `nenrin debt` also reports record-shape warnings for frontmatter files under `changes/`, `observations/`, or `reviews/` that Nenrin cannot treat as standard records, plus nonstandard `status` / `impact` values.
- `nenrin diff` checks changed `tracked_files` paths and reports whether they have related active change records; it does not create records automatically.
