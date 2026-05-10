---
type: nenrin_change
id: brief-active-observation-limit
date: 2026-05-11
status: observing
impact: unknown
related_files:
  - src/nenrin/cli.py
  - README.md
  - docs/agent-usage.md
review_after:
  tasks: 3
  days: 7
---

# Change: brief-active-observation-limit

## Changed

- Bound nenrin brief active observation output by default while keeping Review Due and Recurring Failures visible.

## Reason

Habitat's ledger showed that a long active-observation list can crowd the operational signals agents need first.

## Expected Behavior

- Agents use the default brief for a bounded scan and request --active-limit 0 only when the full active list is genuinely needed.

## Review After

- 3 related task(s)
- 7 day(s)

## Success Signals

- Agents notice review-due or recurring-failure signals before scanning long active lists.
- Large ledgers use the default brief without treating omitted active observations as missing data.

## Failure Signals

- Agents need full active context often enough that `--active-limit 0` becomes routine.
- Important active records are hidden from the default brief when there is no review or debt signal.

## Result

Unjudged.
