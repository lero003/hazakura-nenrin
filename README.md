# Hazakura Nenrin

<p align="center">
  <img src="docs/assets/hazakura-nenrin-logo.png" alt="Hazakura Nenrin logo" width="720">
</p>

Hazakura Nenrin is a small pruning ledger for development judgment.

The latest published release is `v0.2.0`, the low-friction operation release.
The earlier `v0.1.0-beta.1` prerelease remains available as the pruning-ledger
reference beta.

It helps humans and agents:

- remember past decisions and unresolved concerns before work
- decide whether a change is worth recording after work
- periodically review stale hypotheses, debts, and pending reviews
- treat no-op pruning as a healthy outcome

Nenrin can be used as a standalone CLI, but it is also intended as a reference implementation for development harnesses that want low-friction recall, review, and pruning. The harness owns execution. Nenrin owns the lightweight judgment ledger.

For partial adoption in an existing repository, see
[AI Agent Adoption Guide](docs/adoption_guide.md). Nenrin can start as a small
agent-facing rule before a project adopts a full ledger or harness integration.

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

## Smallest Useful Path

Start lower than you think.

1. If the repository has no recurring agent-facing workflow changes, do not
   adopt Nenrin yet.
2. If a small rule would prevent future misunderstanding, paste the minimal
   rule from [AI Agent Adoption Guide](docs/adoption_guide.md) into
   `AGENTS.md`, `CLAUDE.md`, or a harness prompt.
3. Run `nenrin init` only when durable agent-facing guidance changes over time
   and later review would be useful.

Normal use should stay selective: run `nenrin brief` before work only when
prior decisions or unresolved concerns may affect the task, and run `nenrin
diff`, `nenrin debt`, or `nenrin review` after work only to decide whether
there is a durable behavior signal. Create no record for tiny wording changes,
implementation-only work, one-off notes, or quiet review/debt/diff output. A
clean no-op is a successful Nenrin outcome.

## Quick Start Smoke

```bash
python3 -m pip install -e .
nenrin init
nenrin change release-review-checklist
nenrin observe v0-3-release-review --change release-review-checklist
nenrin brief
nenrin metrics --no-write
nenrin debt
nenrin review
nenrin diff
```

The quick start installs the editable package first, so later examples use the
short `nenrin` command. When working from a fresh checkout without installing,
use `uv run nenrin <command>` instead. Minimal Python environments can also use
`PYTHONPATH=src python3 -m nenrin <command>`. `nenrin diff` inspects Git
working-tree changes, so run the smoke inside a Git checkout or temporary Git
repository.

All records are Markdown files under `nenrin/` with YAML-like frontmatter that humans and coding agents can both read.

See `examples/nenrin/` for a tiny sample ledger.

See `docs/roadmap.md` for the current direction. The roadmap is intentionally evidence-led: Nenrin should evolve through observed use, not through a large feature checklist.

See `docs/development_loop.md` for the recurring self-development and pruning
automation runbook used by this repository.

See `docs/integration.md` for guidance on calling Nenrin from a development harness.

See `docs/adoption_guide.md` for choosing the smallest useful adoption level.

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

Treat review due items as a judgment queue, not a task queue. A review should
move an old hypothesis toward keep, remove, merge, narrow, move, or bounded
observation. `keep_observing` must not be used as an indefinite holding area:
when a review keeps an entry observing, state what remains unknown and what to
observe next. Nenrin tracks bounded observation conditions, not tasks, owners,
priorities, or progress.

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

`nenrin review` lists overdue changes. `--create` generates review templates
for each overdue change. `--apply` propagates completed review judgments to
related change records and updates their `## Result` section.

`nenrin brief` prints review deadlines, recurring failures, and active observation context for the next agent session without requiring the agent to read every record. It shows up to 20 active observation records by default so large ledgers keep review and failure signals near the top; use `nenrin brief --active-limit 0` to show all active observations.

`nenrin diff` compares the current Git working tree with `tracked_files` in `config.yaml` and shows whether changed agent-facing files already have related active change records. It reports omissions but does not create records automatically.

`nenrin metrics --no-write` prints metrics without updating `nenrin/metrics.md` or `nenrin/index.md`.

## Configuration

`nenrin init` creates `nenrin/config.yaml` with defaults. The `config_schema`
value identifies the config shape, not the installed Nenrin package version.
The `review_defaults.tasks` and `review_defaults.days` values are used as
fallback defaults for `nenrin change` when `--review-tasks` and
`--review-days` are not specified on the command line.

`nenrin observe --change <id>` warns when a referenced change ID does not exist in the ledger, helping catch orphan observations before they accumulate.

`nenrin review --apply` reads completed review records and updates the related
change's `status`, `impact`, and `## Result` section based on the
`final_judgment`:

| Judgment | Change status | Change impact |
|----------|--------------|---------------|
| `keep` | `reviewed` | `effective` |
| `remove` | `archived` | `ineffective` |
| `merge` | `archived` | `partially_effective` |
| `narrow` | `reviewed` | `partially_effective` |
| `move_to_*` | `archived` | `effective` |
| `keep_observing` | *no change* | *no change* |

Unsupported non-default `final_judgment` values emit a warning and leave the
related change unchanged, so typoed review decisions do not silently prune a
record.

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

Review records include `final_judgment`. Use `nenrin review --apply` to
propagate completed review judgments back to the related change's `status`,
`impact`, and `## Result` section; unsupported values warn and leave the
change unchanged.

When `final_judgment` stays `keep_observing`, fill in `Still Unknown`,
`Observe Next`, and `Out of Scope` so the review records a bounded observation
condition instead of vague deferral. `nenrin debt` warns when a
`keep_observing` review leaves `Observe Next` empty or at its placeholder.

## Tests

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

## License

MIT License. See `LICENSE`.
