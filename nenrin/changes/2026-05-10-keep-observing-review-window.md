---
type: nenrin_change
id: keep-observing-review-window
date: 2026-05-10
status: observing
impact: unknown
related_files:
  - src/nenrin/records.py
  - tests/test_nenrin.py
  - docs/agent-usage.md
  - docs/roadmap.md
  - pyproject.toml
  - src/nenrin/__init__.py
  - README.md
review_after:
  tasks: 3
  days: 7
---

# Change: keep-observing-review-window

## Changed

- Treat `final_judgment: keep_observing` review records as a real review point for overdue calculations.
- Bump current `main` development version to `0.2.0.dev2`.

## Reason

The v0.2 release gate allows a review decision to be applied or consciously kept observing, but `nenrin review` still treated a keep-observing review as immediately overdue because the old change date and old observations remained the only review triggers.

## Expected Behavior

- Creating a keep-observing review keeps the change active but resets the review window.
- Observations after that review, or enough time after that review, can make the change due again.
- v0.2 release review can close real overdue pressure without pretending every record is already effective.

## Review After

- 3 related task(s)
- 7 day(s)

## Success Signals

- A review with `final_judgment: keep_observing` removes old overdue pressure without archiving or upgrading the change.
- Later observations after the review still trigger a new review when `review_after.tasks` is reached.
- v0.2 release prep can distinguish "not ready" from "reviewed and intentionally still observing".

## Failure Signals

- Keep-observing reviews hide records that should have been removed, narrowed, or marked ineffective.
- Agents create keep-observing reviews mechanically instead of writing evidence.
- Review debt becomes invisible even when new post-review observations accumulate.

## Result

Unjudged.
