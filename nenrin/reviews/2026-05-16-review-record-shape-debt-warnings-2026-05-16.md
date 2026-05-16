---
type: nenrin_review
id: review-record-shape-debt-warnings-2026-05-16
date: 2026-05-16
related_change: record-shape-debt-warnings
final_judgment: keep
---

# Review: record-shape-debt-warnings

## Summary

Keep. The warning is earning its place: it stayed quiet for Nenrin's own
ledger, and it exposed a real Habitat ledger file that has frontmatter but is
not a typed Nenrin record.

## Evidence

- `PYTHONPATH=src python3 -m nenrin --root nenrin debt` reported no record
  shape warnings for this repository, so ordinary generated files and templates
  were not noisy.
- Running the same debt check against Habitat's embedded ledger reported
  `changes/2026-05-15-narrow-depth-platform-boundary.md` as missing `type`.
- Inspecting that Habitat file confirmed it is a decision/change note under
  `nenrin/changes/` with frontmatter but without `type: nenrin_change`, so
  Nenrin ignores it in metrics.
- That warning changed the pruning pass from broad overdue-review scanning to a
  concrete cleanup target for the Habitat checkout. This pass keeps the slice
  to the Nenrin review and leaves the Habitat cleanup for the next bounded
  Habitat-side run.

## Decision

- keep

## Cleanup

- Keep the warning focused on record directories only. The next Habitat-capable
  run should either convert the narrow-depth platform boundary note into a
  standard Nenrin record or move it out of `nenrin/changes/` if it is only
  historical context.
