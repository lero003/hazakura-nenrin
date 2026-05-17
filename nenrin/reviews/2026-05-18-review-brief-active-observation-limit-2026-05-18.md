---
type: nenrin_review
id: review-brief-active-observation-limit-2026-05-18
date: 2026-05-18
related_change: brief-active-observation-limit
final_judgment: keep_observing
---

# Review: brief-active-observation-limit

## Summary

Keep observing. The default brief is still below the active limit in this
ledger, so the limit has not yet been tested against a genuinely omitted active
list. The ordering still helped by putting Review Due first.

## Evidence

- `nenrin brief` surfaced the six review-due items before active observations.
- The current active observation list remained under the default limit, so no
  omission behavior was exercised in this repo.
- Tests cover `--active-limit 0` and default limit behavior.

## Still Unknown

- Whether a larger real ledger can use the default brief without needing
  `--active-limit 0` routinely.

## Observe Next

- In the next ledger with more than 20 active records, watch whether omitted
  active observations are acceptable when Review Due and Recurring Failures
  stay visible.

## Out of Scope

- Do not add scores, priorities, or dashboard grouping to solve brief length.

## Decision

- keep_observing

## Cleanup

- Keep observing the real-ledger limit behavior; no code change is needed in
  this slice.
