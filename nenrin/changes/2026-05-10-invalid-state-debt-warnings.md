---
type: nenrin_change
id: invalid-state-debt-warnings
date: 2026-05-10
status: observing
impact: unknown
related_files:
  - src/nenrin/records.py
  - tests/test_nenrin.py
  - docs/roadmap.md
  - docs/agent-usage.md
  - pyproject.toml
  - src/nenrin/__init__.py
  - README.md
review_after:
  tasks: 3
  days: 7
---

# Change: invalid-state-debt-warnings

## Changed

- Warn when Nenrin records use nonstandard status or impact values, and bump main to 0.2.0.dev1.

## Reason

hazakura-ai-mobile now exposes a typed change record with status active; metrics counts it, but the state is outside Nenrin's small status vocabulary.

## Expected Behavior

- Future ledgers surface nonstandard state values as debt so agents can normalize them or move decision notes out of change records before pruning becomes confusing.

## Review After

- 3 related task(s)
- 7 day(s)

## Success Signals

- `nenrin debt` flags `status: active`, `impact: positive`, or similar nonstandard states before they become normal ledger vocabulary.
- Cross-project ledgers can keep product decision notes in docs or convert them into standard Nenrin records intentionally.
- `0.2.0.dev1` clearly marks this as post-beta development behavior, not a stable release.

## Failure Signals

- Projects add new state names instead of keeping evidence in record bodies.
- Record-shape warnings become noisy for valid reviewed or archived records.
- Version wording suggests `v0.2.0` has been released instead of remaining a development version.

## Result

Unjudged.
