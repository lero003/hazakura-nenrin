---
type: nenrin_observation
id: diff-untracked-status-config
date: 2026-05-06
related_changes:
  - diff-command-tracked-files
impact_judgment: partially_effective
success_tags:
  - untracked_agent_file_detected
failure_tags: []
---

# Observation: diff-untracked-status-config

## Task

Tightened `nenrin diff` so new untracked agent-facing files are reported even when a repository config hides untracked files from ordinary `git status`.

## Observed Behavior

- The active `diff-command-tracked-files` record narrowed this run to a concrete omission risk in v0.5 diff awareness.
- `git_changed_paths` now calls `git status --porcelain=v1 --untracked-files=all`, making diff detection independent of `status.showUntrackedFiles`.
- Added a regression test that configures `status.showUntrackedFiles=no`, creates an untracked `docs/new-guidance.md`, and verifies `nenrin diff` still reports it.

## Success Signals Observed

- `nenrin diff` can now catch newly added tracked-pattern docs before they are staged.
- The command remains read-only and still only suggests record creation when the change is durable.

## Failure Signals Observed

- None observed in this slice.

## Impact Judgment

partially_effective

## Next Action

- Keep observing whether `nenrin diff` reduces missed durable agent-facing changes without making agents record tiny one-off files.
