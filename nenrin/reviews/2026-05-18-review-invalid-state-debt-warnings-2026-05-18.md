---
type: nenrin_review
id: review-invalid-state-debt-warnings-2026-05-18
date: 2026-05-18
related_change: invalid-state-debt-warnings
final_judgment: keep
---

# Review: invalid-state-debt-warnings

## Summary

Keep. The warning stays quiet for valid current records while preserving the
small status/impact vocabulary that v0.2 depends on.

## Evidence

- `nenrin debt` reports no record-shape warnings for the current ledger.
- The v0.2 readiness work did not introduce new status values such as
  validated, proven, blocked, or active.
- Tests still cover nonstandard status and impact warnings.
- External review reinforced the need to avoid task states, priorities, and
  broader workflow status vocabulary.

## Still Unknown

- Whether cross-project ledgers with nonstandard states will appear again
  during later external-use intake.

## Observe Next

- In future external-use intake, watch whether nonstandard states are surfaced
  as cleanup rather than normalized into Nenrin's core vocabulary.

## Out of Scope

- Do not add confidence states or project-management states to solve wording
  uncertainty.

## Decision

- keep

## Cleanup

- Mark the change reviewed/effective through `nenrin review --apply`; future
  state vocabulary drift is covered by the existing debt warning.
