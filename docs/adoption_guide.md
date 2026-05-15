# AI Agent Adoption Guide

Status: operational
Scope: Partial adoption of Hazakura Nenrin by AI agents, harnesses, and repositories
Authority: medium
Last reviewed: 2026-05-15

Hazakura Nenrin is meant to be useful when an AI coding agent or development
harness needs a small, reviewable memory of durable judgment changes.

This guide is for agents, harness authors, and maintainers deciding how much
Nenrin to adopt. It is not a task system, activity log, transcript archive, or
replacement for `README.md`, `AGENTS.md`, changelogs, roadmaps, or project docs.

## Adoption Levels

| Level | Use when | Minimum action |
| --- | --- | --- |
| 0. No adoption | The repository has no recurring agent-facing guidance changes to review. | Do nothing. |
| 1. Minimal rule | A project only needs a shared boundary for what should be recorded. | Paste the minimal Nenrin rule into `AGENTS.md`, `CLAUDE.md`, a skill, or a harness prompt. |
| 2. Small ledger | Agent-facing instructions, skills, handoffs, roadmaps, release rules, QA gates, or recurring workflow guidance change over time. | Run `nenrin init` and create records only for durable future-behavior changes. |
| 3. Work loop | Agents need lightweight recall before work and a record-pressure check after work. | Use `nenrin brief` before relevant work and `nenrin diff` / `nenrin debt` / `nenrin review` after agent-facing changes. |
| 4. Pruning loop | Older records are accumulating or review decisions matter. | Use `nenrin review --create` and `nenrin review --apply` to keep, remove, merge, narrow, move, or keep observing records. |
| 5. Harness integration | A development harness coordinates repeated AI work. | Let the harness call Nenrin commands, but keep execution, task choice, and final judgment outside Nenrin. |

Start at the lowest level that reduces future misunderstanding. More records do
not mean better adoption.

## Agent Instructions To Copy

Use this when adding Nenrin to `AGENTS.md`, `CLAUDE.md`, a skill, or a harness
prompt:

```md
Use `nenrin/` as a pruning ledger for durable changes to agent-facing judgment.

Before work, read `nenrin brief` only when prior decisions or unresolved
concerns may change the task.
After work, use `nenrin diff`, `nenrin debt`, or `nenrin review` to decide
whether there is anything worth recording or pruning.

Create or update records for durable changes to instructions, skills, handoffs,
roadmaps, release rules, QA gates, or recurring workflow guidance.
Skip records for implementation logs, tiny wording fixes, raw transcripts,
unapproved speculation, and changes that do not affect future agent behavior.

If there is no actionable signal, make no Nenrin change and report the no-op as
a normal result.
```

## Do Not

- Do not record raw chat logs, private reasoning, secrets, or unresolved
  speculation as durable context.
- Do not create records for ordinary implementation logs, typo fixes, or
  one-off task notes.
- Do not treat Nenrin as a task manager, project manager, agent runtime, eval
  system, or dashboard.
- Do not duplicate version history that already belongs in `README.md`,
  changelogs, roadmaps, or release notes unless there is a specific future
  behavior to observe.
- Do not upgrade a record to `effective` just because it was read, created, or
  mentioned. `effective` requires behavior evidence.
- Do not keep adding rules when a review should remove, merge, narrow, move, or
  keep observing an old record instead.

## Expected Benefit

Adoption is useful when it helps an AI agent or harness:

- remember prior durable judgments without reading a full work log
- decide when no record is the right outcome
- review whether old guidance still earns its place
- keep `README.md`, roadmap, release rules, and agent instructions from
  accumulating unreviewed improvement debt
- preserve enough evidence to keep, remove, merge, narrow, move, or keep
  observing a guidance change

If Nenrin does not change recall, review, pruning, or record-pressure decisions,
keep the adoption level lower.
