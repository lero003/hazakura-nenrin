---
type: nenrin_change
id: release-beta-reference-positioning
date: 2026-05-06
status: observing
impact: unknown
related_files:
  - LICENSE
  - pyproject.toml
  - src/nenrin/__init__.py
  - README.md
  - docs/roadmap.md
  - docs/integration.md
  - docs/release-checklist.md
review_after:
  tasks: 3
  days: 7
---

# Change: release-beta-reference-positioning

## Changed

- Position v0.1.0-beta.1 as a pruning-ledger reference implementation release, not a task manager or full AI platform.

## Reason

External user feedback showed Nenrin's value is easiest to understand as low-friction recall, review, and pruning that can be embedded in a harness.

## Expected Behavior

- Future release work explains the beta by its fit and boundaries, accepts no-op as healthy, and avoids promising a full project-management or agent-framework surface.

## Review After

- 3 related task(s)
- 7 day(s)

## Success Signals

- README frames Nenrin as a pruning ledger and reference implementation before listing commands.
- Release preparation docs make no-op and "not a task manager" explicit.
- Harness integration docs keep execution outside Nenrin.

## Failure Signals

- Release notes or README make Nenrin look like a full project management system or agent framework.
- Future agents create records for ordinary implementation logs because the boundary is unclear.
- The beta is judged by feature count instead of whether the pruning-ledger model is understandable.

## Result

Unjudged.
