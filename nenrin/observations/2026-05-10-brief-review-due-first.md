---
type: nenrin_observation
id: brief-review-due-first
date: 2026-05-10
related_changes:
  - v0-2-release-gate-record-pressure
impact_judgment: partially_effective
success_tags: []
failure_tags: []
---

# Observation: brief-review-due-first

## Task

Daily Nenrin improvement run checked Habitat and ai-mobile as external
read-only use cases before deciding whether Nenrin itself needed a small
change.

## Observed Behavior

- Habitat's ledger had four overdue review candidates, but `nenrin brief`
  printed a long Active Observations section before the Review Due section.
- This made the output less aligned with the pruning automation priority:
  review due first, recurring failures next, broad active context only after
  actionable signals are visible.
- Nenrin now renders `brief` with Review Due and Recurring Failures before
  Active Observations.

## Success Signals Observed

- The small change was covered by a focused unit test for section order.
- Running `brief` on the local ledger now shows Review Due before the active
  observation list.

## Failure Signals Observed

- None observed in this slice.

## Impact Judgment

partially_effective

## Next Action

- Watch whether large real ledgers still need a bounded or filtered `brief`
  mode after this ordering change.
