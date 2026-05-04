---
type: nenrin_change
id: roadmap-tool-role-boundaries
date: 2026-05-04
status: observing
impact: unknown
related_files:
  - docs/roadmap.md
  - docs/philosophy.md
  - ../hazakura_Habitat/README.md
  - ../hazakura_Habitat/docs/roadmap.md
  - ../hazakura_Habitat/docs/product_direction.md
  - ../hazakura_Habitat/docs/current_status.md
  - ../hazakura_Habitat/docs/development_loop.md
  - ../hazakura_Habitat/docs/self_use.md
review_after:
  tasks: 3
  days: 7
---

# Change: roadmap-tool-role-boundaries

## Changed

- Clarified that `AGENTS.md`, roadmap, and development docs remain the immediate operational source of truth.
- Clarified that Habitat should surface current repository facts and instruction drift instead of repeating project instructions.
- Clarified that Nenrin should be judged by later review and pruning decisions, not by record creation alone.
- Shifted Habitat `v0.5` language from generic evidence normalization toward evidence and instruction alignment.

## Reason

DeepSeek and Chika feedback both showed that Habitat and Nenrin are weak if judged as immediate substitutes for `AGENTS.md`. Habitat needs a sharper preflight-audit role, and Nenrin needs its review loop to prove whether recorded changes actually help.

## Expected Behavior

- Future roadmap work treats `AGENTS.md` as the main immediate-work guide.
- Habitat planning prioritizes command-changing repository facts, mismatches, and instruction drift.
- Nenrin planning prioritizes review of `observing` and `unknown` records before adding broader automation.
- Agents do not claim Habitat or Nenrin are valuable merely because they produced output.

## Review After

- 3 related task(s)
- 7 day(s)

## Success Signals

- Habitat self-use reports facts that would not be known from `AGENTS.md` alone.
- Nenrin reviews convert at least one `observing` or `unknown` record into keep, remove, merge, narrow, or move guidance.
- Future agents describe the three-tool split without treating Habitat or Nenrin as required for every tiny task.

## Failure Signals

- Habitat output remains mostly a duplicate of written project instructions.
- Nenrin records accumulate without later review decisions.
- Roadmap work adds new automation before evidence shows the review loop or instruction-drift check helps.

## Result

Unjudged.
