# Release Checklist

This checklist is for the current release flow. `v0.1.0-beta.1` remains the
immutable pruning-ledger reference beta; `v0.2.0` is the low-friction operation
release.

The beta is not meant to prove that Nenrin is a complete project management tool or AI agent framework. It should show whether the pruning-ledger model is understandable and useful when used directly or embedded in a development harness.

## v0.2 Readiness Addendum

Before cutting `v0.2.0`, verify the low-friction operation gates from the
roadmap instead of relying on the old beta smoke alone:

- [x] A first-time reader can tell from `README.md` when not to create a
  record, before reading the command list.
- [x] The smoke path uses `nenrin metrics --no-write` for inspection so the
  first run does not imply generated-output churn is mandatory.
- [x] `nenrin review --apply` leaves reviewed or archived change records with
  matching frontmatter and `## Result` text.
- [x] `nenrin debt` warns when a `keep_observing` review leaves `Observe Next`
  empty or at its placeholder.
- [x] Release notes keep JSON output, dashboards, AI judgment, task ownership,
  priority states, and broad integrations out of scope.

## Release Positioning

- [x] README opens with Nenrin as a pruning ledger for development judgment.
- [x] README explains what Nenrin is not.
- [x] Harness integration docs explain that the harness owns execution and Nenrin owns the lightweight judgment ledger.
- [x] Roadmap names `v0.2` as the low-friction operation release.
- [x] Release notes focus on use, boundaries, and no-op pruning before feature lists.
- [x] License is chosen before public distribution: MIT.

## Beta Success Criteria

The release is successful if:

- users understand that Nenrin is not a task manager
- users understand that no-op is a valid outcome
- users can run the basic workflow in a fresh checkout
- harness authors can see where Nenrin fits into their loop
- the ledger does not encourage recording everything
- review, debt, and pruning flows feel natural without adding much process

The goal is not to maximize usage. The goal is to keep the pruning-ledger model understandable, useful, and light under real use.

## Fresh Checkout Smoke

Run from a fresh Git checkout or temporary Git repository:

```bash
python3 -m pip install -e .
nenrin --version
nenrin init
nenrin change release-review-checklist
nenrin observe v0-2-smoke --change release-review-checklist
nenrin metrics --no-write
nenrin brief
nenrin debt
nenrin review
nenrin diff
```

Expected result:

- commands complete without crashes
- `nenrin --version` reports `nenrin 0.2.0`
- generated Markdown records are readable
- `brief`, `debt`, `review`, and `diff` are useful without requiring a dashboard
- no-op is easy to report when there is no actionable review, debt, or diff signal
- `nenrin diff` is run inside a Git repository; outside Git, it reports that it cannot inspect changes

## Local Verification

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
git diff --check
python3 -m build
PYTHONPATH=src python3 -m nenrin --root nenrin brief
PYTHONPATH=src python3 -m nenrin --root nenrin debt
PYTHONPATH=src python3 -m nenrin --root nenrin review
PYTHONPATH=src python3 -m nenrin --root nenrin diff
```

If the local Python does not have `build`, install it in a temporary virtual environment and build from there.

## Public Safety Check

Before making the repository public:

- run a secret-pattern search over tracked and new files
- confirm `.env`, private key, certificate, and local virtualenv files are not tracked
- confirm generated build outputs are ignored or removed
- confirm README and release notes do not claim enforcement, sandboxing, security protection, or agent-framework behavior that Nenrin does not implement

## Release Note Draft

```md
# Nenrin v0.2.0 — Low-Friction Operation

Nenrin is a small pruning ledger for development judgment.

This release is not a feature-count release. It asks whether a pruning ledger
can stay lightweight under real use.

Since `v0.1.0-beta.1`:

- the README starts with the smallest useful adoption path and when not to record
- `brief`, `debt`, `review`, and `diff` all treat quiet output as a healthy no-op
- `review --apply` keeps change frontmatter and `## Result` text in agreement
- generated config uses `config_schema: 1` instead of a confusing package-version-like field
- real self-use reviewed 10 changes, archived 6, recorded 12 observations, and left no review debt

This release intentionally does not add JSON output, dashboards, AI-generated
judgments, task ownership, priority management, broad integrations, or automatic
record creation from diffs.
```
