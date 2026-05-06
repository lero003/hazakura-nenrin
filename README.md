# Hazakura Nenrin

Hazakura Nenrin is a small pruning ledger for development judgment.

It helps humans and agents:

- remember past decisions and unresolved concerns before work
- decide whether a change is worth recording after work
- periodically review stale hypotheses, debts, and pending reviews
- treat no-op pruning as a healthy outcome

Nenrin can be used as a standalone CLI, but it is also intended as a reference implementation for development harnesses that want low-friction recall, review, and pruning. The harness owns execution. Nenrin owns the lightweight judgment ledger.

## What Nenrin Is Not

Nenrin is not:

- a task manager
- a full activity log
- a memory dump
- a project management system
- an AI agent framework
- a scoring or ranking system
- prompt eval or production observability

Its value comes from recording less, not more: decisions, concerns, and hypotheses that may matter later, plus the evidence needed to keep, remove, merge, narrow, or move them.

## Quick Start

```bash
python3 -m pip install -e .
nenrin init
nenrin change release-review-checklist
nenrin observe v0-3-release-review --change release-review-checklist
nenrin brief
nenrin metrics
nenrin debt
nenrin review
nenrin diff
```

The quick start installs the editable package first, so later examples use the
short `nenrin` command. When working from a fresh checkout without installing,
use `uv run nenrin <command>` instead. Minimal Python environments can also use
`PYTHONPATH=src python3 -m nenrin <command>`.

All records are Markdown files under `nenrin/` with YAML-like frontmatter that humans and coding agents can both read.

See `examples/nenrin/` for a tiny sample ledger.

See `docs/roadmap.md` for the current direction. The roadmap is intentionally evidence-led: Nenrin should evolve through observed use, not through a large feature checklist.

See `docs/integration.md` for guidance on calling Nenrin from a development harness.

See `docs/philosophy.md` for the early product stance behind Nenrin.

## 改善観察台帳

Nenrin is best understood as an 改善観察台帳: it records why an agent-environment improvement was added, what behavior was expected, what happened later, and whether the improvement should be kept, removed, merged, narrowed, or moved.

It intentionally avoids turning every improvement into a numeric score. The first job is to keep the retrospective loop visible.

AI usability is a constraint from the beginning, not a future feature. Records should stay easy for coding agents to read, update, and summarize without needing a dashboard or external service.

Nenrin is intentionally on the defensive side of AI-first development. Faster generation, broader automation, and more powerful agent execution will keep improving elsewhere; Nenrin focuses on keeping the agent working environment understandable, reviewable, and pruneable as that speed increases.

Nenrin is a pruning tool, not a log generator. A healthy ledger is not the one with the most records; it is the one where improvements can be reviewed, closed, narrowed, moved, or removed when evidence is weak. No actionable signal is also a valid outcome: do not create work just to prove the ledger is active.

## Core Workflow

1. When you change an agent-facing artifact, run `nenrin change <name>`.
2. Fill in the generated Markdown record with the change, reason, expected behavior, and review timing.
3. After a related task, run `nenrin observe <name> --change <change-id>`.
4. Use `nenrin metrics` and `nenrin debt` to find stale observing changes, overdue reviews, recurring failures, and cleanup candidates.

Create records for durable changes to agent-facing behavior: instructions, skills, handoffs, roadmaps, release rules, QA gates, and recurring workflow guidance. Skip Nenrin records for tiny wording fixes, formatting-only edits, one-off task notes, or changes that do not affect future agent behavior.

Treat `effective` as a behavior claim, not a feeling of progress. Use it when evidence shows a changed next command, a narrower cleanup choice, a safer review path, or a concrete reduction in recurring friction. If the evidence only says a record was read or written, keep the impact unknown or partially effective and write the uncertainty in the review note.

## Commands

Command examples in this README prefer `nenrin` after installation. Agent quick
references may use the same short form when the CLI is already on `PATH`; setup
and fresh-checkout instructions should show the install step or use
`uv run nenrin`.

```bash
nenrin init
nenrin change <name> [--changed <text>] [--reason <text>] [--expected <text>]
                     [--review-days <n>] [--review-tasks <n>] [--file <path> ...]
nenrin observe <name> --change <change-id> [--impact <value>]
nenrin review [--create] [--apply]
nenrin brief
nenrin metrics [--no-write]
nenrin debt
nenrin diff
```

All commands accept `--root <path>` to point to a non-default ledger directory (default: `./nenrin`).

`nenrin change` and `nenrin observe` intentionally create editable Markdown templates instead of forcing a heavy questionnaire. The first version optimizes for Codex, Claude Code, Cursor, Windsurf, and similar tools that can fill in records directly.

`nenrin review` lists overdue changes. `--create` generates review templates for each overdue change. `--apply` propagates completed review judgments to related change records.

`nenrin brief` prints the active observation context for the next agent session (Watch/Risk signals, review deadlines, recurring failures) without requiring the agent to read every record.

`nenrin diff` compares the current Git working tree with `tracked_files` in `config.yaml` and shows whether changed agent-facing files already have related active change records. It reports omissions but does not create records automatically.

`nenrin metrics --no-write` prints metrics without updating `nenrin/metrics.md` or `nenrin/index.md`.

## Configuration

`nenrin init` creates `nenrin/config.yaml` with defaults. The `review_defaults.tasks` and `review_defaults.days` values are used as fallback defaults for `nenrin change` when `--review-tasks` and `--review-days` are not specified on the command line.

`nenrin observe --change <id>` warns when a referenced change ID does not exist in the ledger, helping catch orphan observations before they accumulate.

`nenrin review --apply` reads completed review records and updates the related change's `status` and `impact` based on the `final_judgment`:

| Judgment | Change status | Change impact |
|----------|--------------|---------------|
| `keep` | `reviewed` | `effective` |
| `remove` | `archived` | `ineffective` |
| `merge` | `archived` | `partially_effective` |
| `narrow` | `reviewed` | `partially_effective` |
| `move_to_*` | `archived` | `effective` |
| `keep_observing` | *no change* | *no change* |

The `tracked_files` list in `config.yaml` defines the file patterns that `nenrin diff` watches for agent-facing changes.

## Frontmatter

Nenrin frontmatter supports a small YAML-like subset, not full YAML. It supports scalar values, nested mappings, and simple lists.

Observation records may include optional `success_tags` and `failure_tags` to reduce wording drift in recurring signals:

```md
---
type: nenrin_observation
id: release-review
failure_tags:
  - changelog_consistency_missed
success_tags:
  - release_risk_classified
---
```

Review records include `final_judgment`. Use `nenrin review --apply` to propagate completed review judgments back to the related change's `status` and `impact`.

## Tests

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

## License

MIT License. See `LICENSE`.
