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

See `docs/roadmap.md` for the current direction. The roadmap is intentionally evidence-led: Nenrin should evolve through observed use, not through a large feature checklist.

See `docs/philosophy.md` for the early product stance behind Nenrin.

## 改善観察台帳

Nenrin is best understood as an 改善観察台帳: it records why an agent-environment improvement was added, what behavior was expected, what happened later, and whether the improvement should be kept, removed, merged, narrowed, or moved.

It intentionally avoids turning every improvement into a numeric score. The first job is to keep the retrospective loop visible.

AI usability is a constraint from the beginning, not a future feature. Records should stay easy for coding agents to read, update, and summarize without needing a dashboard or external service.

Nenrin is intentionally on the defensive side of AI-first development. Faster generation, broader automation, and more powerful agent execution will keep improving elsewhere; Nenrin focuses on keeping the agent working environment understandable, reviewable, and pruneable as that speed increases.

## Core Workflow

1. When you change an agent-facing artifact, run `nenrin change <name>`.
2. Fill in the generated Markdown record with the change, reason, expected behavior, and review timing.
3. After a related task, run `nenrin observe <name> --change <change-id>`.
4. Use `nenrin metrics` and `nenrin debt` to find stale observing changes, overdue reviews, recurring failures, and cleanup candidates.

Create records for durable changes to agent-facing behavior: instructions, skills, handoffs, roadmaps, release rules, QA gates, and recurring workflow guidance. Skip Nenrin records for tiny wording fixes, formatting-only edits, one-off task notes, or changes that do not affect future agent behavior.

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

Review records include `final_judgment`. A later CLI version should use review judgments to prompt updates to the related change's `status` and `impact`.

## Tests

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```
