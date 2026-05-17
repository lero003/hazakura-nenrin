---
type: nenrin_change
id: roadmap-ai-usable-from-start
date: 2026-05-03
status: reviewed
impact: effective
related_files:
  - README.md
  - docs/roadmap.md
  - docs/agent-usage.md
review_after:
  tasks: 3
  days: 7
---

# Change: roadmap-ai-usable-from-start

## Changed

- Added an evidence-led roadmap.
- Added minimal agent usage guidance for `AGENTS.md`, `CLAUDE.md`, project instructions, or skills.
- Clarified in README that AI usability is an initial constraint and that records should not be created for tiny or non-agent-facing changes.

## Reason

AI usability needs to be an initial constraint, not a late AI-assistance feature. The roadmap should emphasize observation, review, pruning, and briefings before diff detection or AI judgment.

## Expected Behavior

- Future agents treat Nenrin as a lightweight improvement observation ledger.
- Future agents avoid over-recording tiny or non-agent-facing changes.
- Future planning prioritizes review, pruning, and briefings before diff detection or AI judgment.
- Nenrin's own development uses Nenrin records when changing durable agent-facing project guidance.

## Review After

- 3 related task(s)
- 7 day(s)

## Success Signals

- A future task reads `docs/roadmap.md` before proposing broad features.
- Agents can decide when not to create a Nenrin record.
- `brief`, review, and pruning work are prioritized before heavy metrics or AI judgment.

## Failure Signals

- New roadmap or README changes add feature promises without observed use.
- Agents create records for every tiny edit.
- Nenrin positioning drifts toward prompt eval, dashboards, or automatic AI judgment.

## Result

Reviewed via `review-roadmap-ai-usable-from-start-2026-05-18`. Judgment: `keep`.
