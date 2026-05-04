# Agent Usage Guidance

Use this guidance when adding Nenrin to `AGENTS.md`, `CLAUDE.md`, project instructions, or a skill.

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

## First Files To Read

For an existing ledger, read:

1. `nenrin/index.md`
2. active records in `nenrin/changes/`
3. Run `nenrin brief` to get active observation context in one screen
4. Run `nenrin metrics` and `nenrin debt` when deciding what to review

Keep observations short and evidence-oriented. Do not turn the ledger into a transcript archive.

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
- `nenrin review --apply` reads completed reviews and updates the related change's `status` and `impact` based on `final_judgment` (e.g., `keep` → `reviewed`/`effective`, `remove` → `archived`/`ineffective`).
