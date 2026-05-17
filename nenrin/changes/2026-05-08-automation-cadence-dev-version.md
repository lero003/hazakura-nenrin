---
type: nenrin_change
id: automation-cadence-dev-version
date: 2026-05-08
status: reviewed
impact: effective
related_files:
  - docs/roadmap.md
  - docs/release-checklist.md
  - README.md
  - pyproject.toml
  - src/nenrin/__init__.py
review_after:
  tasks: 3
  days: 7
---

# Change: automation-cadence-dev-version

## Changed

- Lower recurring automation cadence and move main development version past the published v0.1 beta.

## Reason

Recent runs produced many quiet or small follow-up passes, so hourly automation is too frequent; main also contains post-beta fixes and should not keep reporting the published beta version.

## Expected Behavior

- Automations run less often, and agents/users can distinguish the immutable v0.1.0-beta.1 release from current main development work.

## Review After

- 3 related task(s)
- 7 day(s)

## Success Signals

- Hourly-style development automations stop producing repeated quiet or tiny follow-up runs.
- `nenrin --version` on `main` no longer reports the already-published beta version.
- Release docs still preserve `v0.1.0-beta.1` as the immutable public prerelease.

## Failure Signals

- Lower cadence lets overdue reviews or recurring failure signals sit too long.
- Users mistake `0.2.0.dev0` for a published stable release.
- Automation prompt wording drifts back toward hourly work generation.

## Result

Reviewed via `review-automation-cadence-dev-version-2026-05-15`. Judgment: `keep`.
