# Product Philosophy

This document captures the early stance behind Hazakura Nenrin. It is deliberately provisional. Nenrin is still young, and the right shape should change as real self-use shows what helps and what becomes friction.

## Defensive Infrastructure

Many AI-first development tools optimize for the offensive side of the loop:

- generate more code
- automate larger tasks
- integrate more tools
- delegate more work to agents
- make the development cycle faster

That direction is valuable, and many people will pursue it well. Nenrin intentionally focuses on the defensive side:

- What should the agent read before acting?
- Which workflow rules actually improved later behavior?
- Which skills, handoffs, roadmaps, or QA checks became stale?
- Which instructions are duplicated, too broad, or no longer useful?
- Did an improvement change the next agent action, or only make the docs longer?
- Can the team explain why a rule still exists?

The bet is that faster agent work makes defensive infrastructure more important, not less.

## The Loop With Habitat

Hazakura Habitat and Hazakura Nenrin are separate products, but they fit together naturally.

Habitat is a preflight tool. It gives an AI coding agent short, advisory context before work starts, especially around safer command choices.

Nenrin is a retrospective ledger. It records changes to the agent-facing working environment and asks later whether those changes helped, should be kept, should be narrowed, or should be removed.

In shorthand:

- Habitat: before work, make the next command safer.
- Nenrin: after changes, make the working environment less likely to accumulate improvement debt.

This pairing may become a useful base layer for an autonomous improvement loop: preflight context, real work, observation, pruning, then better preflight context next time.

## Beyond Skills Alone

Skills are an important part of the agent environment, but Nenrin should not become only a skill manager.

The working environment also includes:

- `AGENTS.md` and other instructions
- `SKILL.md`
- handoff formats
- release checklists
- QA gates
- roadmaps
- decision logs
- automation prompts
- project-specific operating rules

The problem is not only whether a skill exists. The problem is whether the whole agent-facing environment is still coherent.

## Balance Against Over-Measurement

Nenrin should avoid drifting into heavy measurement too early.

Prompt eval, production observability, benchmark suites, and experiment trackers are useful, but Nenrin is trying to stay lighter:

- record the reason for an improvement
- record the expected behavior
- record later observations
- review whether to keep, remove, merge, narrow, or move the improvement

Numbers can help, but the core value is the retrospective habit. `metrics` should remain an observation summary, not a pressure to create a dashboard or score every rule.

## Pruning Is A Feature

Nenrin should make it normal to remove or narrow improvements.

Agent environments often grow by accretion:

- a mistake happens
- a rule is added
- another mistake happens
- another rule is added
- the agent now has more to read and more ways to be confused

Nenrin exists to ask whether those additions actually earned their place.

Useful outcomes include:

- keep a rule because it worked
- remove a rule because it did not
- merge duplicated guidance
- narrow a broad instruction
- move details into a skill
- move one-off context into a handoff
- move recurring release checks into a checklist

## Loose Until Proven

The project should stay loose for now.

Do not rush toward:

- GUI
- web app
- heavy dashboards
- automatic AI judgment
- broad external integrations
- Habitat-only coupling

The better near-term goal is to use Nenrin in real projects, especially Habitat, and notice what actually changes behavior. Public release should wait until there are a few lived examples: a rule kept, a rule removed, a skill moved, a checklist narrowed, or a recurring failure made visible.

The guiding question is:

> Can an AI coding agent help improve its own working environment without turning that environment into a pile of permanent, unreviewed instructions?

Nenrin is a small attempt to make that answer yes.
