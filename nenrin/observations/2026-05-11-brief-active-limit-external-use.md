---
type: nenrin_observation
id: brief-active-limit-external-use
date: 2026-05-11
related_changes:
  - brief-active-observation-limit
impact_judgment: partially_effective
success_tags:
  - review_due_visible_before_active_context
failure_tags: []
---

# Observation: brief-active-limit-external-use

## Task

Daily Nenrin improvement run checked Nenrin itself plus Habitat and ai-mobile
as read-only external use cases before deciding whether Nenrin needed a small
change.

## Observed Behavior

- Nenrin's own ledger was quiet: no overdue reviews, recurring failures,
  cleanup candidates, record-shape warnings, or tracked diffs.
- Habitat's larger ledger had 11 overdue reviews and 120 active observing
  changes. The default `brief` showed Review Due first, then omitted the
  remaining long active-observation list with an explicit `--active-limit 0`
  hint.
- ai-mobile had no Nenrin review/debt/diff signal. Its current friction was an
  Android verification environment blocker, not a Nenrin record-shape issue.

## Success Signals Observed

- The bounded Habitat brief made the actionable review queue visible without
  requiring a full active-record scan.
- No external project needed mutation for this observation.

## Failure Signals Observed

- None observed in this slice.

## Impact Judgment

partially_effective

## Next Action

- Keep watching whether agents routinely need `brief --active-limit 0`; if not,
  the bounded default remains sufficient.
