---
type: nenrin_change
id: diff-command-tracked-files
date: 2026-05-05
status: observing
impact: unknown
related_files:
  - README.md
  - docs/roadmap.md
  - docs/agent-usage.md
  - src/nenrin/cli.py
  - tests/test_nenrin.py
review_after:
  tasks: 2
  days: 7
---

# Change: diff-command-tracked-files

## Changed

- Added a read-only nenrin diff command that compares Git working tree changes with tracked_files and reports related active change coverage.

## Reason

v0.5 diff awareness needs a small manual omission check before any automated record creation exists.

## Expected Behavior

- Agents run nenrin diff after agent-facing file edits and create a record only when the change is durable.

## Review After

- 2 related task(s)
- 7 day(s)

## Success Signals

- `nenrin diff` helps an agent notice changed tracked files before deciding whether a record is warranted.
- The command stays read-only and does not turn every docs or instruction edit into a generated record.

## Failure Signals

- Agents treat the warning as a requirement to create records for tiny or temporary edits.
- The path matching misses common `tracked_files` patterns such as shallow `docs/*.md` files.

## Result

Unjudged.
