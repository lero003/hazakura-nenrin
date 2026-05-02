from __future__ import annotations

from datetime import date
from typing import Any

from .frontmatter import dump_frontmatter


DEFAULT_CONFIG = """project_name: hazakura-nenrin
nenrin_version: 0.1

tracked_files:
  - AGENTS.md
  - CLAUDE.md
  - README.md
  - docs/**/*.md
  - skills/**/SKILL.md
  - handoff/**/*.md
  - roadmap*.md
  - release*.md
  - qa*.md

review_defaults:
  tasks: 3
  days: 7

impact_values:
  - unknown
  - effective
  - partially_effective
  - ineffective
  - harmful

status_values:
  - draft
  - observing
  - ready_for_review
  - reviewed
  - archived
"""


def change_record(
    *,
    record_id: str,
    title: str,
    today: date,
    changed: str = "TBD",
    reason: str = "TBD",
    expected_behavior: str = "TBD",
    review_days: int = 7,
    review_tasks: int = 3,
    related_files: list[str] | None = None,
) -> str:
    metadata: dict[str, Any] = {
        "type": "nenrin_change",
        "id": record_id,
        "date": today.isoformat(),
        "status": "observing",
        "impact": "unknown",
        "related_files": related_files or [],
        "review_after": {
            "tasks": review_tasks,
            "days": review_days,
        },
    }
    body = f"""# Change: {title}

## Changed

- {changed}

## Reason

{reason}

## Expected Behavior

- {expected_behavior}

## Review After

- {review_tasks} related task(s)
- {review_days} day(s)

## Success Signals

- TBD

## Failure Signals

- TBD

## Result

Unjudged.
"""
    return dump_frontmatter(metadata, body)


def observation_record(
    *,
    record_id: str,
    title: str,
    today: date,
    related_changes: list[str],
    impact: str,
) -> str:
    metadata: dict[str, Any] = {
        "type": "nenrin_observation",
        "id": record_id,
        "date": today.isoformat(),
        "related_changes": related_changes,
        "impact_judgment": impact,
    }
    body = f"""# Observation: {title}

## Task

TBD

## Observed Behavior

- TBD

## Success Signals Observed

- TBD

## Failure Signals Observed

- TBD

## Impact Judgment

{impact}

## Next Action

- TBD
"""
    return dump_frontmatter(metadata, body)


def review_record(*, record_id: str, title: str, today: date, related_change: str) -> str:
    metadata: dict[str, Any] = {
        "type": "nenrin_review",
        "id": record_id,
        "date": today.isoformat(),
        "related_change": related_change,
        "final_judgment": "keep_observing",
    }
    body = f"""# Review: {title}

## Summary

TBD

## Evidence

- TBD

## Decision

- keep_observing

## Cleanup

- TBD
"""
    return dump_frontmatter(metadata, body)


def project_readme() -> str:
    return """# Nenrin Ledger

This directory tracks whether changes to the AI agent working environment actually improved later agent behavior.

Use this ledger for changes to agent-facing artifacts such as rules, skills, handoffs, roadmaps, release checklists, and QA gates.

## Workflow

1. Create a change record when an agent-facing artifact changes.
2. Create observation records after related work.
3. Review whether the improvement should be kept, removed, merged, narrowed, moved to a skill, moved to a handoff, or kept observing.

## What Nenrin Is Not

- Not prompt eval.
- Not production observability.
- Not a benchmark suite.
- Not an agent runtime.

It is a lightweight improvement observation ledger.
"""


def index_markdown(summary: str = "No records yet.") -> str:
    return f"""# Nenrin Index

{summary}
"""


def metrics_markdown(summary: str = "Run `nenrin metrics` after adding records.") -> str:
    return f"""# Nenrin Metrics

{summary}
"""
