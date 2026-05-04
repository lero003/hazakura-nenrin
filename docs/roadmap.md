# Hazakura Nenrin Roadmap

This roadmap is a hypothesis, not a promise.

Nenrin should evolve through observed use. Do not add automation before the manual ledger proves useful. Do not add heavy metrics before the observation habit is stable. Do not add AI judgment before review decisions are clear. Do not let Nenrin itself become improvement debt.

## Product Principles

- AI usability is a starting constraint, not a later feature.
- Markdown records should remain readable by humans and coding agents.
- Frontmatter should stay simple enough for lightweight local parsing.
- Generated config should either affect runtime behavior or be clearly documented as advisory.
- Observation and review matter more than numeric scoring.
- Cleanup decisions matter as much as adding new guidance.
- Nenrin should close, narrow, move, or remove improvements more readily than it creates new permanent guidance.
- No-op is a valid automation outcome when there is no actionable signal.
- Keep states small and put confidence in review evidence, not in more status values.
- `AGENTS.md`, roadmap, and development docs remain the operational source of truth for current work; Nenrin should test whether changes to those sources earned their place.
- Habitat is a strong proving ground, but Nenrin should not depend on Habitat.

For the broader product stance, see [Product Philosophy](philosophy.md).

## Tool Roles

Current self-use suggests this working split:

| Tool | Primary role | Near-term test |
| --- | --- | --- |
| `AGENTS.md` and project docs | Current rules, direction, and concrete workflow | Does the next agent know what to do now? |
| Habitat | Pre-work repository reality check | Did it surface current project facts or instruction drift that changed the next command? |
| Nenrin | Retrospective pruning ledger | Did prior records make a later keep, remove, merge, narrow, or move decision easier? |

Nenrin should not try to beat `AGENTS.md` at immediate instruction or become a second version history. Its value should be judged after several tasks, when `observing` and `unknown` records can be reviewed against behavior evidence and pruned if `AGENTS.md` already carries the durable context well enough.

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
- Avoid duplicating version history that already belongs in `AGENTS.md`, changelogs, or roadmaps; record the expected future behavior and review trigger instead.
- Keep `metrics` useful as an observation summary, not a scoring system.
- Keep `debt` quiet enough that it points to reviewable cleanup.
- Keep optional `success_tags` and `failure_tags` useful for recurring signals.
- Provide a minimal rule that can be pasted into `AGENTS.md` or similar agent instructions.
- Keep no-failure placeholders out of recurring debt while preserving weak evidence as `unknown` or `partially_effective`.

Success means the ledger is used during real work without becoming a chore or a stale checklist.

## v0.2.x - Foundation Hardening

Goal: remove hidden correctness gaps before review, briefing, and diff automation depend on them.

Focus:

- Parse `config.yaml` and use `review_defaults` for `nenrin change`.
- Treat `tracked_files` as the future contract for `nenrin diff`, even before diff awareness ships.
- Fix frontmatter parser edge cases or adopt a small maintained YAML parser if the dependency cost stays low.
- Add cross-record validation so `nenrin observe --change <id>` does not silently create orphan observations.
- Broaden tests around frontmatter edge cases, `cmd_review --create`, `cleanup_candidates()`, `unique_record_path()`, and `slugify()`.
- Keep generated outputs distinct: `index.md` for navigation, `metrics.md` for aggregate state, and future `brief` output for next-session context.

Success means generated config is not misleading, record references are checked, parser behavior is covered by tests, and later automation has a reliable base.

## v0.3 - Review and Pruning

Goal: connect observations to keep, remove, merge, narrow, and move decisions.

Focus:

- Make review records useful in real operation.
- Turn long-lived `observing` and `unknown` records into an explicit review queue instead of treating them as success.
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
- Improve `debt` cleanup candidates without making them noisy; use `impact` and review evidence to avoid generic all-option advice.
- Prefer reviewing a small number of lived records over adding more fields or states.

Success means at least some improvements are pruned, narrowed, merged, or moved instead of only being added.

Automation in this phase should act as a pruning pass, not a work generator. It should prioritize overdue review, recurring failure verification, active-record hygiene, evidence quality, and no-op when nothing needs to close.

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

Before adding `brief`, keep its responsibility separate from generated `index.md` and `metrics.md`: the brief should orient a new agent session, not become another metrics report.

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
- Treat Habitat findings as useful input when they show a mismatch between written instructions and repository reality.

Success means record omissions decrease without forcing tiny edits into the ledger.

This phase depends on the v0.2.x config-loading work. If `config.yaml` is still only generated and not read, do not start diff awareness.

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
- Do `unknown` impacts become review decisions after enough related work?
- Do remove, merge, and narrow decisions actually happen?
- Do automations leave the ledger unchanged when there is no actionable review, failure, or hygiene signal?
- Are `effective` judgments backed by behavior evidence rather than by the fact that a record was created?
- Do generated config values actually match CLI behavior?
- Are early recurring failures visible enough, or does the threshold hide useful weak signals?

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
