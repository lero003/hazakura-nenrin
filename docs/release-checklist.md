# Release Checklist

This checklist is for `v0.1.0-beta.1`, the pruning-ledger reference beta.

Python packaging uses the PEP 440 version `0.1.0b1` for this beta.

The beta is not meant to prove that Nenrin is a complete project management tool or AI agent framework. It should show whether the pruning-ledger model is understandable and useful when used directly or embedded in a development harness.

## Release Positioning

- [x] README opens with Nenrin as a pruning ledger for development judgment.
- [x] README explains what Nenrin is not.
- [x] Harness integration docs explain that the harness owns execution and Nenrin owns the lightweight judgment ledger.
- [x] Roadmap names `v0.1` as the reference implementation beta for a low-friction pruning ledger.
- [x] Release notes focus on use, boundaries, and no-op pruning before feature lists.
- [x] License is chosen before public distribution: MIT.

## Beta Success Criteria

The beta is successful if:

- users understand that Nenrin is not a task manager
- users understand that no-op is a valid outcome
- users can run the basic workflow in a fresh checkout
- harness authors can see where Nenrin fits into their loop
- the ledger does not encourage recording everything
- review, debt, and pruning flows feel natural without adding much process

The goal of the beta is not to maximize usage. The goal is to see whether the pruning-ledger model is understandable and useful.

## Fresh Checkout Smoke

Run from a fresh Git checkout or temporary Git repository:

```bash
python3 -m pip install -e .
nenrin --version
nenrin init
nenrin change release-review-checklist
nenrin observe v0-1-beta-smoke --change release-review-checklist
nenrin brief
nenrin debt
nenrin review
nenrin diff
```

Expected result:

- commands complete without crashes
- `nenrin --version` reports `nenrin 0.1.0b1`
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
# Nenrin v0.1.0-beta.1

Nenrin is a small pruning ledger for development judgment.

This beta is not intended to present Nenrin as a complete project management tool or an AI agent framework. Instead, it introduces a lightweight model for remembering decisions, unresolved concerns, and hypotheses that may matter later, and for pruning them when they no longer do.

Nenrin can be used as a standalone CLI, but it is also intended as a reference implementation for harnesses that want to incorporate low-friction recall, review, and pruning into their development loop.

This release focuses on:

- recalling relevant context before work
- identifying unresolved debt and review items
- inspecting meaningful changes after work
- accepting no-op as a valid outcome
- keeping the ledger small enough to remain useful
```
