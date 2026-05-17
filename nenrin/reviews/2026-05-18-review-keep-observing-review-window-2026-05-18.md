---
type: nenrin_review
id: review-keep-observing-review-window-2026-05-18
date: 2026-05-18
related_change: keep-observing-review-window
final_judgment: keep
---

# Review: keep-observing-review-window

## Summary

Keep, with one follow-up fix landed in this slice. The review window reset
worked, and this pass exposed and fixed the adjacent `review --create` bug that
prevented a new review after an old keep-observing review became due again.

## Evidence

- Existing tests already covered keep-observing resetting overdue pressure and
  later observations making a change due again.
- Real use showed date-based overdue pressure after older keep-observing
  reviews.
- `review --create` initially skipped due changes because any prior review for
  the change existed; it now skips only same-day review templates.
- A regression test covers creating a new review after an old keep-observing
  review.

## Still Unknown

- Whether future review passes choose `keep_observing` only when the review
  body names concrete remaining evidence.

## Observe Next

- Watch the next pruning pass for bounded `keep_observing` reviews rather than
  mechanical deferral.

## Out of Scope

- Do not add owners, priority states, or task breakdowns to review due items.

## Decision

- keep

## Cleanup

- Mark the change reviewed/effective through `nenrin review --apply`; the
  adjacent create behavior is now covered by code and tests.
