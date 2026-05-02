# Hazakura Nenrin Roadmap

This roadmap is a hypothesis, not a promise.

Nenrin should evolve through observed use. Do not add automation before the manual ledger proves useful. Do not add heavy metrics before the observation habit is stable. Do not add AI judgment before review decisions are clear. Do not let Nenrin itself become improvement debt.

## Product Principles

- AI usability is a starting constraint, not a later feature.
- Markdown records should remain readable by humans and coding agents.
- Frontmatter should stay simple enough for lightweight local parsing.
- Observation and review matter more than numeric scoring.
- Cleanup decisions matter as much as adding new guidance.
- Habitat is a strong proving ground, but Nenrin should not depend on Habitat.

For the broader product stance, see [Product Philosophy](philosophy.md).

## v0.1 - Minimal Ledger

Goal: create change and observation records.

Current scope:

- `nenrin init`
- `nenrin change`
- `nenrin observe`
- `nenrin review`
- `nenrin metrics`
- `nenrin debt`
- Markdown records with small YAML-like frontmatter
- `changes/`, `observations/`, `reviews/`, templates, config, README

Success means an agent-facing change can be recorded, a later task can add an observation, and overdue or stale improvements are visible enough to review.

## v0.2 - Low-Friction Operation

Goal: make the ledger easy for humans and coding agents to use without over-recording.

Focus:

- Keep change and observation templates short enough to fill naturally.
- Clarify when to create a record and when not to.
- Keep `metrics` useful as an observation summary, not a scoring system.
- Keep `debt` quiet enough that it points to reviewable cleanup.
- Support optional `success_tags` and `failure_tags` for recurring signals.
- Provide a minimal rule that can be pasted into `AGENTS.md` or similar agent instructions.

Success means the ledger is used during real work without becoming a chore or a stale checklist.

## v0.3 - Review and Pruning

Goal: connect observations to keep, remove, merge, narrow, and move decisions.

Focus:

- Make review records useful in real operation.
- Clarify `final_judgment` values:
  - `keep`
  - `remove`
  - `merge`
  - `narrow`
  - `move_to_skill`
  - `move_to_handoff`
  - `move_to_checklist`
  - `keep_observing`
- Add a path from review decisions back to change `status` and `impact`.
- Improve `debt` cleanup candidates without making them noisy.

Success means at least some improvements are pruned, narrowed, merged, or moved instead of only being added.

## v0.4 - Briefing

Goal: summarize the active observation context for the next agent session.

Possible command:

```bash
nenrin brief
```

Expected shape:

```md
# Nenrin Brief

## Active Observations

- release-review-checklist
  - Watch: changelog consistency
  - Risk: checklist may be too shallow

## Review Due

- handoff-format-update

## Recurring Failures

- changelog consistency missed
```

Success means an agent can understand what to watch without reading every record.

## v0.5 - Diff Awareness

Goal: detect important agent-facing changes without automatically turning every diff into a record.

Possible command:

```bash
nenrin diff
```

Focus:

- Use `tracked_files` from `config.yaml`.
- Detect changed `AGENTS.md`, `SKILL.md`, handoff, roadmap, release, docs, or QA files.
- Warn when no related Nenrin change appears to exist.
- Suggest record creation without creating records automatically.

Success means record omissions decrease without forcing tiny edits into the ledger.

## v0.6 - Assisted Reflection

Goal: let AI suggest signals, judgments, and cleanup actions while keeping decisions reviewable.

Possible assistance:

- Draft expected behavior.
- Draft success and failure signals.
- Suggest impact judgment from observations.
- Suggest review decisions.
- Summarize stale rule or duplicate guidance candidates.
- Group recurring failures despite wording drift.

Boundary:

> AI suggests; the human or project owner decides.

Success means AI help reduces reflection effort without turning judgment into unreviewed automation.

## v1.0 - Proven in Real Use

Goal: show that Nenrin helped at least one real AI-first development workflow avoid improvement debt.

Release readiness should be based on use, not feature count:

- Real projects have accumulated change and observation records.
- Some improvements were removed, merged, narrowed, or moved.
- Recurring failures became visible.
- It is possible to explain why a rule exists or why it was retired.
- Nenrin itself remains lightweight.
- Coding agents can use it naturally.

## Watch Nenrin Itself

Early self-observation should focus on:

- Are change records created naturally?
- Are observations forgotten?
- Does `review_after` produce useful review timing?
- Do `metrics` and `debt` change behavior?
- Are records growing too quickly?
- Do agents leave `TBD` content behind?
- Do old changes stay `observing` forever?
- Do remove, merge, and narrow decisions actually happen?

If the answer is no, improve the workflow before adding more features.

## Not Now

- GUI
- Web app
- GitHub integration
- LangSmith or Braintrust integration
- Large dashboards
- Complex scoring
- Automatic AI judgment
- Habitat-only coupling
- Prompt-eval positioning
- Broad convenience features
