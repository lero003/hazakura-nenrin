---
type: nenrin_change
id: roadmap-drift-doc-sync
date: 2026-05-07
status: observing
impact: unknown
related_files:
  - docs/agent-usage.md
  - docs/roadmap.md
review_after:
  tasks: 3
  days: 7
---

# Change: roadmap-drift-doc-sync

## Changed

- Document that agents may update roadmap/docs during a work slice when implementation or verification reveals small drift.

## Reason

Recent work showed roadmap alignment should not remain only in chat guidance when it affects future agent decisions.

## Expected Behavior

- Future agents update the relevant docs in the same small slice instead of leaving roadmap drift for a later vague cleanup.

## Review After

- 3 related task(s)
- 7 day(s)

## Success Signals

- Agents update roadmap or agent-usage guidance when a completed slice reveals a small mismatch with current direction.
- Documentation updates remain narrow and evidence-based instead of becoming broad planning work.

## Failure Signals

- Agents edit roadmap language for speculative ideas that did not arise from real work.
- Documentation drift remains only in chat even when it affects future command or scope decisions.

## Result

Unjudged.
