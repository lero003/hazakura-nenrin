---
type: nenrin_change
id: record-shape-debt-warnings
date: 2026-05-09
status: reviewed
impact: effective
related_files:
  - src/nenrin/records.py
  - src/nenrin/cli.py
  - tests/test_nenrin.py
  - docs/roadmap.md
  - docs/agent-usage.md
review_after:
  tasks: 3
  days: 7
---

# Change: record-shape-debt-warnings

## Changed

- Warn when ledger files under changes/observations/reviews have nonstandard or incomplete frontmatter.

## Reason

hazakura-ai-mobile showed a model decision note under nenrin/changes with frontmatter but no nenrin record type, so metrics silently ignored it while the ledger looked active.

## Expected Behavior

- Future pruning passes can use nenrin debt to catch record-shape drift before the ledger becomes a mixed decision-note and change-record store.

## Review After

- 3 related task(s)
- 7 day(s)

## Success Signals

- `nenrin debt` flags nonstandard frontmatter files in ledger record directories.
- Agents can decide whether a model decision note belongs in project docs or should become a standard Nenrin change/review record.
- `metrics` remains quiet about intentionally ignored files while `debt` still gives a cleanup path.

## Failure Signals

- Ordinary README, index, metrics, or template files are reported as record-shape warnings.
- Debt output becomes noisy for harmless notes outside record directories.
- Agents keep adding decision notes to `changes/` without converting or moving them.

## Result

Reviewed via `review-record-shape-debt-warnings-2026-05-16`. Judgment: `keep`.
