---
type: nenrin_change
id: ai-agent-adoption-guide
date: 2026-05-15
status: observing
impact: unknown
related_files:
  - README.md
  - docs/adoption_guide.md
  - docs/agent-usage.md
  - docs/integration.md
  - examples/nenrin/README.md
review_after:
  tasks: 3
  days: 7
---

# Change: ai-agent-adoption-guide

## Changed

- Added an AI agent adoption guide with partial Nenrin adoption levels.
- Linked the guide from README, agent-usage, integration, and example-ledger docs.
- Clarified that adoption can start as a minimal agent rule before a project needs a ledger or harness integration.

## Reason

Nenrin's target reader is often the next AI agent or harness deciding whether a durable pruning ledger is worth using. The docs needed a direct adoption surface so agents can avoid over-recording, keep no-op normal, and choose the smallest useful level.

## Expected Behavior

- Future agents can decide whether no adoption, a minimal rule, a small ledger, a work loop, a pruning loop, or harness integration is appropriate.
- Agents skip raw transcripts, implementation logs, tiny wording fixes, and unapproved speculation.
- Harness authors keep execution and task choice outside Nenrin.
- `effective` remains a behavior-evidence claim, not proof that a record was created.

## Review After

- 3 related task(s)
- 7 day(s)

## Success Signals

- Future integrations paste the minimal rule or adopt a small ledger before jumping to harness integration.
- Agents report no-op as a normal result when there is no actionable recall, review, pruning, or record-pressure signal.
- README and external framing describe Nenrin as a pruning ledger/reference implementation rather than a task manager or agent framework.

## Failure Signals

- Agents create records for ordinary logs or tiny wording churn because the adoption guide feels mandatory.
- Harness docs make Nenrin responsible for execution or task choice.
- Future docs accumulate more philosophy without clarifying record boundaries.

## Result

Unjudged.
