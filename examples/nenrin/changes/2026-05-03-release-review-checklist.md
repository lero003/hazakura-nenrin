---
type: nenrin_change
id: release-review-checklist
date: 2026-05-03
status: observing
impact: unknown
related_files:
  - AGENTS.md
  - docs/release-checklist.md
review_after:
  tasks: 3
  days: 7
---

# Change: release-review-checklist

## Changed

- Added a release review checklist for changelog, docs, tests, and stale handoff checks.

## Reason

Release readiness checks were scattered across multiple project notes.

## Expected Behavior

- The agent checks changelog, docs, and tests before recommending a release.
- The agent does not rely on stale handoff context without verification.

## Review After

- 3 related task(s)
- 7 day(s)

## Success Signals

- Changelog consistency is mentioned during release review.
- Release risks are separated into blockers and non-blockers.

## Failure Signals

- Changelog consistency is missed.
- Release readiness is judged without checking docs or tests.

## Result

Unjudged.
