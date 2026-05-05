---
type: nenrin_observation
id: diff-glob-segment-matching
date: 2026-05-05
related_changes:
  - diff-command-tracked-files
impact_judgment: partially_effective
success_tags: []
failure_tags: []
---

# Observation: diff-glob-segment-matching

## Task

Tightened `nenrin diff` tracked-file glob matching after the active diff-command record highlighted path matching as a failure risk.

## Observed Behavior

- The existing `diff-command-tracked-files` record narrowed this run from broad new feature work to one concrete v0.5 correctness fix.
- `tracked_file_matches` now treats `*` as a single path segment and `**` as zero or more path segments, so shallow patterns stay shallow while `docs/**/*.md` still covers docs root files.

## Success Signals Observed

- A recorded failure signal became a small CLI behavior fix with direct unit coverage.
- The diff command remains read-only and does not create records automatically.

## Failure Signals Observed

- None observed in this slice.

## Impact Judgment

partially_effective

## Next Action

- Keep observing whether `nenrin diff` reduces missed durable records without making agents record tiny or temporary edits.
