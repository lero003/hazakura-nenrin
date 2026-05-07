# Harness Integration

Nenrin can be used directly as a CLI, but it is also designed to be called from a development harness.

The examples below use `nenrin` for the installed command. A harness running
from an uninstalled checkout should call `uv run nenrin <command>` or run the
module with `PYTHONPATH=src python3 -m nenrin <command>`.

A harness may call:

- `nenrin brief` before work, to recall relevant context without reading every record
- `nenrin diff` after work, to inspect meaningful agent-facing changes
- `nenrin debt` to surface unresolved concerns and recurring failure signals
- `nenrin review` to identify entries that should be revisited
- `nenrin review --create` and `nenrin review --apply` when a review pass should close, narrow, move, or keep observing a change

The harness owns execution. Nenrin owns the lightweight judgment ledger.

This boundary matters. Nenrin should not decide what command to run next, manage the task queue, control a conversation, or become a full agent framework. It should help the surrounding workflow remember what may matter later and prune what no longer earns its place.

Machine-readable output may be added later for harness integration, but v0.2
prioritizes human-readable, low-friction operation. Add structured output only
when it reduces record pressure or review friction without turning Nenrin into
the harness.

## Suggested Loop

1. Before work, run `nenrin brief` only when prior decisions or unresolved concerns may affect the task.
2. During work, prefer the repository, tests, and current harness signals over the ledger.
3. After work, run `nenrin diff` to see whether changed agent-facing files already have related active records.
4. Create or update a record only when the change affects future judgment or agent behavior.
5. If `nenrin debt` and `nenrin review` are quiet, report no-op as a healthy result.

## Integration Principles

- Keep Nenrin optional in the hot path.
- Do not mirror every implementation log into the ledger.
- Treat `effective` as a behavior claim, not a feeling.
- Prefer pruning, narrowing, merging, or moving old guidance over adding permanent rules.
- Let no-op remain visible and acceptable.

## Minimal Agent Rule

Use this when embedding Nenrin into `AGENTS.md`, `CLAUDE.md`, a skill, or a harness prompt:

```md
Use `nenrin/` as the pruning ledger for durable changes to agent-facing judgment.

Before work, read `nenrin brief` only when past decisions or unresolved concerns may change the task.
After work, use `nenrin diff`, `nenrin debt`, or `nenrin review` to decide whether there is anything worth recording or pruning.

Create or update records for durable changes to instructions, skills, handoffs, roadmaps, release rules, QA gates, or recurring workflow guidance.
Skip records for ordinary implementation logs, tiny wording fixes, and changes that do not affect future behavior.

If there is no actionable signal, make no Nenrin change and report the no-op as a normal result.
```
