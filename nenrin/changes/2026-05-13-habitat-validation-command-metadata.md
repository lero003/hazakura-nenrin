---
type: nenrin_change
id: habitat-validation-command-metadata
date: 2026-05-13
status: observing
impact: unknown
related_files:
  - pyproject.toml
  - nenrin/config.yaml
  - docs/agent-usage.md
  - docs/roadmap.md
review_after:
  tasks: 3
  days: 7
---

# Change: habitat-validation-command-metadata

## Changed

- Treat command-shaping project metadata as agent-facing guidance, track
  `pyproject.toml` in `nenrin diff`, and remove stale pytest configuration from
  `pyproject.toml`.

## Reason

A Habitat v0.6 stdout scan of Nenrin preferred pytest even though the
repository docs and working verification use unittest. The first suspected
cause was stale pytest metadata in `pyproject.toml`; after removing it, the
scan still preferred pytest, which makes this a bounded Habitat-side command
selection gap rather than only a Nenrin metadata issue.

## Expected Behavior

- Future agents treat package or validation metadata changes as record-worthy
  when they alter command selection.
- If Habitat output conflicts with documented or verified repository validation,
  agents should prefer the working repo command and record the mismatch as
  carry-back evidence instead of blindly following the generated preferred
  command.

## Review After

- 3 related task(s)
- 7 day(s)

## Success Signals

- `nenrin diff` surfaces future `pyproject.toml` changes for record-conscious
  review.
- Future Habitat/Nenrin use treats the pytest/unittest mismatch as bounded
  command-selection evidence, not as a reason to install pytest or rewrite the
  test suite.

## Failure Signals

- Agents run or install pytest for Nenrin solely because Habitat preferred it.
- Metadata cleanup becomes a broad Python workflow expansion instead of a
  narrow command-decision correction.

## Result

Initial correction made on 2026-05-13. Removing stale pytest config did not
change Habitat's preferred command, so the durable learning is the review
boundary: generated Habitat guidance must be checked against repo-local
validation truth before it changes commands.
