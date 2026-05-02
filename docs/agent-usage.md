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
```

## When Not To Record

Skip a Nenrin record for:

- typo or formatting fixes
- one-off task notes
- implementation-only changes that do not affect future agent behavior
- temporary instructions that belong in the current handoff only
- duplicate records where an existing active change already covers the behavior

## First Files To Read

For an existing ledger, read:

1. `nenrin/index.md`
2. active records in `nenrin/changes/`
3. `nenrin/metrics.md` or `nenrin debt` when deciding what to review

Keep observations short and evidence-oriented. Do not turn the ledger into a transcript archive.
