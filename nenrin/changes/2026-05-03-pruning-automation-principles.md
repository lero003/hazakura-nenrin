---
type: nenrin_change
id: pruning-automation-principles
date: 2026-05-03
status: observing
impact: unknown
related_files:
  - README.md
  - docs/agent-usage.md
  - docs/philosophy.md
  - docs/roadmap.md
review_after:
  tasks: 3
  days: 7
---

# Change: pruning-automation-principles

## Changed

- Clarified that Nenrin is a pruning tool, not a log or work generator.
- Added no-op as a valid automation outcome when there is no actionable signal.
- Clarified that `effective` must be backed by behavior evidence, not record creation.
- Clarified that confidence belongs in review evidence, not extra status values.

## Reason

Habitat self-use and follow-up review showed that Nenrin becomes useful when observations are closed, narrowed, moved, or removed. The next automation prompt should protect that direction by prioritizing overdue review, recurring failure verification, active-record hygiene, evidence quality, and no-op.

## Expected Behavior

- Future automation does not create arbitrary work just to produce a commit.
- Future agents keep impact/status values small and write evidence in record bodies.
- Weak evidence remains `unknown` or `partially_effective` instead of being upgraded because a record exists.
- No-action runs are reported as successful pruning passes when metrics, debt, and review show nothing actionable.

## Review After

- 3 related task(s)
- 7 day(s)

## Success Signals

- A later automation run reports no-op without changing files when there is no overdue review, recurring failure, or active-record hygiene issue.
- A later review cites concrete behavior evidence instead of adding `validated` or `proven` states.
- Automation closes or narrows mature records before adding new durable guidance.

## Failure Signals

- Automation keeps creating docs or records when there is no actionable signal.
- Agents treat no-failure placeholders as proof of success.
- New status or impact values are added instead of writing clearer evidence.

## Result

Unjudged.
