---
type: nenrin_change
id: ignore-placeholder-failure-signals
date: 2026-05-03
status: reviewed
impact: effective
related_files:
  - src/nenrin/records.py
  - tests/test_nenrin.py
review_after:
  tasks: 3
  days: 7
---

# Change: ignore-placeholder-failure-signals

## Changed

- Recurring failure detection now ignores placeholder bullets such as `None observed in this slice.` and `None in this task.`.
- Added a regression test covering common no-failure placeholder wording.

## Reason

Habitat's ledger accumulated enough observations for review, but `nenrin debt` treated repeated no-failure bullets as recurring failures. That made healthy observations look like cleanup debt and obscured real signals.

## Expected Behavior

- `nenrin metrics` and `nenrin debt` report recurring failures only when the failure section names a real signal.
- Observation records can keep a readable no-failure bullet without polluting debt output.
- Future template wording or parser changes keep no-failure placeholders out of recurring failure counts.

## Review After

- 3 related task(s)
- 7 day(s)

## Success Signals

- Habitat metrics no longer reports `None observed...` or `None in this task` as recurring failure signals.
- Real repeated failure bullets and `failure_tags` are still counted.

## Failure Signals

- Real repeated failure wording is filtered out by overly broad placeholder matching.
- Agents respond to no-failure placeholders as if cleanup is needed.

## Result

Reviewed effective on 2026-05-10.
