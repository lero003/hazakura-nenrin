# Hazakura Nenrin Development Loop

Status: Operational
Scope: Recurring Nenrin self-development and pruning automation
Authority: High
Last reviewed: 2026-05-16

This document is the repo-side runbook for Nenrin development automation. The
saved Codex automation prompts should point here for durable behavior, while
the prompts provide scheduling and environment details.

Nenrin automation must stay small, evidence-led, and willing to end as no-op.
The goal is not to keep the repository busy. The goal is to preserve a useful
pruning ledger while `v0.2.0` proves low-friction operation.

## Active Automations

- `hazakura-nenrin-1`: low-frequency small improvement pass.
- `hazakura-nenrin-daily-reflection`: weekly pruning review pass.

Schedules live in the Codex app automation settings. This document owns the
behavioral contract, not the exact RRULE.

## Standard Preflight

Start each Nenrin automation run with:

1. `git status --short --branch`
2. `README.md`
3. `docs/roadmap.md`
4. `docs/agent-usage.md`
5. `docs/development_loop.md`
6. `nenrin/index.md`
7. `PYTHONPATH=src python3 -m nenrin --root nenrin brief`
8. `PYTHONPATH=src python3 -m nenrin --root nenrin review`
9. `PYTHONPATH=src python3 -m nenrin --root nenrin debt`
10. `PYTHONPATH=src python3 -m nenrin --root nenrin diff`

Use `brief` as a narrowing surface. Do not read every active record unless the
preflight output or the selected slice genuinely needs that context.

## Decision Order

Choose at most one small, verifiable slice in this order:

1. Overdue review or review-apply work.
2. Recurring failure verification.
3. Active-record hygiene or evidence quality.
4. External-use carry-back from Habitat or `hazakura-ai-mobile`.
5. Small roadmap or documentation drift discovered during the run.
6. A narrow CLI, parser, template, or test fix with clear operational value.
7. No-op when none of the above is actionable.

Do not create a feature, record, or docs edit only to avoid an empty run. A
clean no-op is successful when the checked signals are quiet.

## External Use Intake

Habitat and `hazakura-ai-mobile` are read-only evidence sources for Nenrin
development automation. They are not secondary work targets.

For external repos, inspect only enough to decide whether a Nenrin-side change
is warranted:

- repo status
- relevant automation memory
- current status or development automation docs
- existing Nenrin ledger, if present
- recent commits
- Habitat report freshness and command-decision guidance

Run a fresh Habitat scan into a temporary output path only when the existing
report is stale, weak, missing, or contradicted by current repo facts. Do not
update the observed project's `habitat-report/` directory from a Nenrin run.

Carry back at most one Nenrin-side change: a review decision, observation,
docs clarification, prompt adjustment, or CLI hygiene fix. If the signal is
weak or project-specific, report the bounded evidence and leave Nenrin
unchanged.

## No-Op Gate

Prefer no-op when:

- `review`, `debt`, and `diff` are quiet.
- External-use checks do not change the next Nenrin decision.
- A docs concern is only wording churn with no durable behavior change.
- Verification would require bypassing another project's environment blocker.
- The only possible change would add record pressure without a review question.

When ending no-op, report the checked commands and the reason no repository
change was made.

## Prompt And Docs Sync

If a saved automation prompt changes durable behavior, update this document in
the same slice. If this document changes the automation flow, update the saved
automation prompt in the same slice.

Keep detailed operating rules here instead of letting prompts grow into the
only source of truth. Prompts may repeat the short preflight and final report
shape, but the durable decision rules should remain readable in the repository.

## Verification

- Docs-only changes: run `git diff --check`.
- Nenrin record or generated-output changes: run
  `PYTHONPATH=src python3 -m nenrin --root nenrin metrics` and
  `PYTHONPATH=src python3 -m nenrin --root nenrin debt`.
- Code changes: run `PYTHONPATH=src python3 -m unittest discover -s tests`.

Before commit, inspect the diff and stage only the coherent slice.

## Final Report Shape

Automation reports should include:

- selected change or no-op reason
- external-use judgment, if checked
- changed files
- verification results
- commit hash
- push result
- remaining risk
- next signal to watch
