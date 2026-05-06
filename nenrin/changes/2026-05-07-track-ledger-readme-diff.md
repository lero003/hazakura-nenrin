---
type: nenrin_change
id: track-ledger-readme-diff
date: 2026-05-07
status: observing
impact: unknown
related_files:
  - nenrin/config.yaml
  - src/nenrin/templates.py
  - tests/test_nenrin.py
review_after:
  tasks: 3
  days: 7
---

# Change: track-ledger-readme-diff

## Changed

- Added nenrin/README.md to the default and local tracked_files list.

## Reason

The ledger README is an agent-facing guidance file, but recent edits to it were invisible to nenrin diff.

## Expected Behavior

- Future ledger README edits appear in nenrin diff so agents can consciously decide whether a durable Nenrin record is warranted.

## Review After

- 3 related task(s)
- 7 day(s)

## Success Signals

- `nenrin diff` reports future `nenrin/README.md` edits as tracked agent-facing changes.
- Agents still skip records for tiny ledger README wording fixes when no durable behavior changed.

## Failure Signals

- Ledger README edits create pressure to record routine wording churn.
- Agents miss a durable ledger README guidance change because the tracked pattern does not match the project layout.

## Result

Unjudged.
