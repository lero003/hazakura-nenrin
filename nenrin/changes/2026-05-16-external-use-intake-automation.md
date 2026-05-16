---
type: nenrin_change
id: external-use-intake-automation
date: 2026-05-16
status: observing
impact: unknown
related_files:
  - docs/agent-usage.md
  - docs/development_loop.md
  - docs/roadmap.md
review_after:
  tasks: 3
  days: 7
---

# Change: external-use-intake-automation

## Changed

- Added External Use Intake guidance and updated Nenrin development automations to inspect ai-mobile read-only for Nenrin-side lessons.

## Reason

Nenrin automation already checked ai-mobile in the daily loop, but the pruning/review guidance did not clearly say how external project use should become a bounded carry-back signal instead of a second workstream.

## Expected Behavior

- Future Nenrin automation checks ai-mobile usage for record pressure, stale guidance, command-decision drift, and blocker patterns, then carries back at most one Nenrin-side docs, prompt, review, observation, or CLI improvement; weak or project-specific signals end as no-op.

## Review After

- 3 related task(s)
- 7 day(s)

## Success Signals

- Automation reports ai-mobile-derived signals as bounded evidence and either
  no-ops cleanly or makes one small Nenrin-side adjustment.
- Future agents do not edit ai-mobile from Nenrin development runs.
- External use checks reduce broad context gathering by pointing to the
  specific blocker, boundary, freshness, or record-pressure signal that matters.

## Failure Signals

- Nenrin automation starts treating ai-mobile backlog items as Nenrin work.
- External checks add raw logs or broad summaries without changing the next
  Nenrin decision.
- Agents create new records after every external read even when no future
  review question exists.

## Result

Unjudged.
