# Hazakura Nenrin

Hazakura Nenrin is a lightweight improvement observation ledger for AI-first development. If you prefer agile language, you can think of it as a small retrospective ledger for agent-environment changes.

It helps you record changes to agent-facing artifacts such as `AGENTS.md`, `SKILL.md`, handoffs, checklists, roadmaps, and QA gates, then observe whether those changes actually improved later agent behavior.

Nenrin is not prompt eval, production observability, or an agent runtime. It is closer to a small retrospective ledger for your AI working environment: why you added a rule, what behavior you expected, what happened later, and whether to keep, remove, merge, narrow, or move that improvement.

## Quick Start

```bash
python3 -m pip install -e .
nenrin init
nenrin change release-review-checklist
nenrin observe v0-3-release-review --change release-review-checklist
nenrin metrics
nenrin debt
```

All records are Markdown files under `nenrin/` with YAML-like frontmatter that humans and coding agents can both read.

See `examples/nenrin/` for a tiny sample ledger.

## Core Workflow

1. When you change an agent-facing artifact, run `nenrin change <name>`.
2. Fill in the generated Markdown record with the change, reason, expected behavior, and review timing.
3. After a related task, run `nenrin observe <name> --change <change-id>`.
4. Use `nenrin metrics` and `nenrin debt` to find stale observing changes, overdue reviews, recurring failures, and cleanup candidates.

## Commands

```bash
nenrin init
nenrin change <name>
nenrin observe <name> --change <change-id>
nenrin review
nenrin metrics
nenrin debt
```

`nenrin change` and `nenrin observe` intentionally create editable Markdown templates instead of forcing a heavy questionnaire. The first version optimizes for Codex, Claude Code, Cursor, Windsurf, and similar tools that can fill in records directly.

## Tests

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```
