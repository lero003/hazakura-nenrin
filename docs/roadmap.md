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
- When real work exposes small roadmap or documentation drift, update the relevant doc in the same slice instead of leaving the guidance only in chat.
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

## v0.1 - Pruning Ledger Reference Beta

Goal: present a low-friction pruning-ledger model as a usable reference implementation.

Status: `v0.1.0-beta.1` is published as an immutable prerelease. Current `main`
uses the development version `0.2.0.dev0` while the next low-friction operation
cycle is exercised.

Current scope:

- `nenrin init`
- `nenrin change`
- `nenrin observe`
- `nenrin review`
- `nenrin metrics`
- `nenrin debt`
- `nenrin brief`
- `nenrin diff`
- Markdown records with small YAML-like frontmatter
- `changes/`, `observations/`, `reviews/`, templates, config, README

The `v0.1.0-beta.1` release should prove the shape, not completeness as a large application. Nenrin should be understandable as a standalone CLI and as a reference implementation for harnesses that want lightweight recall, review, and pruning.

Success means:

- users understand that Nenrin is not a task manager, full activity log, or AI agent framework
- no-op pruning is accepted as a healthy outcome
- a fresh checkout can run the basic workflow
- harness authors can see where Nenrin fits without making it responsible for execution
- the ledger does not encourage recording everything
- review, debt, and pruning flows feel natural without much process

## v0.2 - Low-Friction Operation

Goal: make the ledger easy for humans and coding agents to use without over-recording.

This is an operation release, not a feature-count release. The central question
is whether teams can record less, observe later, and prune with confidence. A
growing count of `observing` / `unknown` change records with few observations is
an acceptable early signal, but it should be treated as v0.2 risk evidence
rather than a reason to add more commands.

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

Release `v0.2.0` only when real use shows that:

- no-op after `diff`, `debt`, or `review` feels normal
- agents can skip records for small wording or implementation-only changes
- observations are created after related work without becoming task logs
- at least one review decision has been applied or consciously kept observing
- `metrics` and `debt` remain quiet unless there is actionable signal
- `effective` is used only with behavior evidence
- Nenrin-related docs changes can happen without creating unnecessary records

For v0.2, prefer polishing these release gates over adding JSON output,
dashboards, broader integrations, or AI-assisted judgment.

## v0.2.x - Foundation Hardening ~~(done)~~

Goal: remove hidden correctness gaps before review, briefing, and diff automation depend on them.

Focus:

- ~~Parse `config.yaml` and use `review_defaults` for `nenrin change`.~~
- ~~Treat `tracked_files` as the runtime contract for `nenrin diff`.~~
- ~~Fix frontmatter parser edge cases or adopt a small maintained YAML parser if the dependency cost stays low.~~
- ~~Add cross-record validation so `nenrin observe --change <id>` does not silently create orphan observations.~~
- ~~Broaden tests around frontmatter edge cases, `cmd_review --create`, `cleanup_candidates()`, `unique_record_path()`, and `slugify()`.~~
- ~~Keep generated outputs distinct: `index.md` for navigation, `metrics.md` for aggregate state, and future `brief` output for next-session context.~~

Success means generated config is not misleading, record references are checked, parser behavior is covered by tests, and later automation has a reliable base.

## v0.3 - Review and Pruning

Goal: connect observations to keep, remove, merge, narrow, and move decisions.

Focus:

- Make review records useful in real operation.
- Turn long-lived `observing` and `unknown` records into an explicit review queue instead of treating them as success.
- ~~Clarify `final_judgment` values: `keep`, `remove`, `merge`, `narrow`, `move_to_skill`, `move_to_handoff`, `move_to_checklist`, `keep_observing`.~~
- ~~Add a path from review decisions back to change `status` and `impact`.~~ (`nenrin review --apply`)
- Improve `debt` cleanup candidates without making them noisy; use `impact` and review evidence to avoid generic all-option advice.
- Prefer reviewing a small number of lived records over adding more fields or states.

Success means at least some improvements are pruned, narrowed, merged, or moved instead of only being added.

Automation in this phase should act as a pruning pass, not a work generator. It should prioritize overdue review, recurring failure verification, active-record hygiene, evidence quality, and no-op when nothing needs to close.

## v0.4 - Briefing ~~(done)~~

Goal: summarize the active observation context for the next agent session.

Command:

```bash
nenrin brief
```

Output shape (active changes with Watch/Risk signals extracted from record body):

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

Command:

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
- Does the ledger drift toward change-record accumulation without enough later observation or review?
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
