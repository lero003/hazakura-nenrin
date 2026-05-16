---
type: nenrin_observation
id: llm-manager-external-use-intake
date: 2026-05-16
related_changes:
  - external-use-intake-automation
impact_judgment: partially_effective
success_tags: []
failure_tags:
  - external_source_not_git_repo
---

# Observation: llm-manager-external-use-intake

## Task

Added `hazakura-llm-manager` as another read-only external-use source for
Nenrin development automation.

## Observed Behavior

- `hazakura-llm-manager` has `AGENTS.md` guidance for Habitat and Nenrin usage,
  plus README/product brief scope boundaries for a macOS local LLM server
  manager.
- From this workspace it does not currently appear to be a Git repository, so
  Nenrin automation should not assume `git status` or recent commits are always
  available for that observed project.
- The useful carry-back signal is command and scope discipline: SwiftPM
  verification, restricted-environment flags, local endpoint/runtime command
  boundaries, and explicit non-goals such as no chat UI, no model download, and
  no proxy layer.

## Success Signals Observed

- External-use intake can be generalized without turning the manager app into a
  Nenrin mutation target.
- The runbook now says to use repo status only when the observed project is a
  Git repository.

## Failure Signals Observed

- If future automation treats missing Git metadata as a manager-side problem to
  fix, the external-use boundary is too broad.

## Impact Judgment

partially_effective

## Next Action

- Watch whether future Nenrin runs can reference manager-side command/scope
  lessons while still ending no-op when no Nenrin-side decision changes.
