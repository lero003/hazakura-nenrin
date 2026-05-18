---
type: nenrin_observation
id: placeholder-run-wording-filter
date: 2026-05-18
related_changes:
  - ignore-placeholder-failure-signals
impact_judgment: partially_effective
success_tags:
  - placeholder_failure_signal_filtered
failure_tags: []
---

# Observation: placeholder-run-wording-filter

## Context

Daily external-use intake against Habitat showed `nenrin metrics --no-write`
counting repeated `None in this run.` bullets as a recurring failure.

## Evidence

- Habitat's ledger had two observations with `None in this run.` under failure
  signals.
- Nenrin already intended no-failure placeholders to stay out of recurring
  debt, but the older filter only covered nearby wording such as `None in this
  task.` and `None observed in this slice.`

## Effect

- The recurring-failure placeholder filter now includes `None in this run.`
- The existing regression test covers that wording so future `debt` and
  `metrics` output stays focused on real repeated failures.

## Failure Signals

- None observed in this slice.
