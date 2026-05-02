from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

from . import __version__
from .records import (
    VALID_IMPACTS,
    cleanup_candidates,
    impact_counts,
    load_records,
    observations,
    observation_counts_by_change,
    overdue_changes,
    recurring_failure_signals,
    status_counts,
)
from .templates import (
    DEFAULT_CONFIG,
    change_record,
    index_markdown,
    metrics_markdown,
    observation_record,
    project_readme,
    review_record,
)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="nenrin",
        description="A lightweight improvement observation ledger for AI agent working environments.",
    )
    parser.add_argument("--version", action="version", version=f"nenrin {__version__}")
    parser.add_argument(
        "--root",
        default="nenrin",
        help="Nenrin ledger directory. Defaults to ./nenrin.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create a Nenrin ledger directory.")
    init_parser.set_defaults(func=cmd_init)

    change_parser = subparsers.add_parser("change", help="Create a change record.")
    change_parser.add_argument("name")
    change_parser.add_argument("--changed", default="TBD")
    change_parser.add_argument("--reason", default="TBD")
    change_parser.add_argument("--expected", default="TBD")
    change_parser.add_argument("--review-days", type=int, default=7)
    change_parser.add_argument("--review-tasks", type=int, default=3)
    change_parser.add_argument("--file", action="append", default=[], dest="related_files")
    change_parser.set_defaults(func=cmd_change)

    observe_parser = subparsers.add_parser("observe", help="Create an observation record.")
    observe_parser.add_argument("name")
    observe_parser.add_argument("--change", action="append", default=[], dest="related_changes")
    observe_parser.add_argument(
        "--impact",
        default="unknown",
        choices=sorted(VALID_IMPACTS),
    )
    observe_parser.set_defaults(func=cmd_observe)

    review_parser = subparsers.add_parser("review", help="Show overdue changes and create review templates.")
    review_parser.add_argument("--create", action="store_true", help="Create review templates for overdue changes.")
    review_parser.set_defaults(func=cmd_review)

    metrics_parser = subparsers.add_parser("metrics", help="Print metrics and update nenrin/metrics.md.")
    metrics_parser.add_argument("--no-write", action="store_true", help="Do not update metrics.md or index.md.")
    metrics_parser.set_defaults(func=cmd_metrics)

    debt_parser = subparsers.add_parser("debt", help="Print improvement debt candidates.")
    debt_parser.set_defaults(func=cmd_debt)

    return parser


def cmd_init(args: argparse.Namespace) -> int:
    root = Path(args.root)
    for directory in ["changes", "observations", "reviews", "templates"]:
        (root / directory).mkdir(parents=True, exist_ok=True)

    _write_once(root / "README.md", project_readme())
    _write_once(root / "config.yaml", DEFAULT_CONFIG)
    _write_once(root / "index.md", index_markdown())
    _write_once(root / "metrics.md", metrics_markdown())
    _write_once(
        root / "templates" / "change.md",
        change_record(record_id="example-change", title="example-change", today=date.today()),
    )
    _write_once(
        root / "templates" / "observation.md",
        observation_record(
            record_id="example-observation",
            title="example-observation",
            today=date.today(),
            related_changes=["example-change"],
            impact="unknown",
        ),
    )
    _write_once(
        root / "templates" / "review.md",
        review_record(
            record_id="review-example-change",
            title="example-change",
            today=date.today(),
            related_change="example-change",
        ),
    )

    print(f"Initialized Nenrin ledger at {root}")
    return 0


def cmd_change(args: argparse.Namespace) -> int:
    root = Path(args.root)
    ensure_initialized(root)
    today = date.today()
    record_id = slugify(args.name)
    path = unique_record_path(root / "changes", today, record_id)
    path.write_text(
        change_record(
            record_id=record_id,
            title=args.name,
            today=today,
            changed=args.changed,
            reason=args.reason,
            expected_behavior=args.expected,
            review_days=args.review_days,
            review_tasks=args.review_tasks,
            related_files=args.related_files,
        ),
        encoding="utf-8",
    )
    update_index(root)
    print(path)
    return 0


def cmd_observe(args: argparse.Namespace) -> int:
    root = Path(args.root)
    ensure_initialized(root)
    today = date.today()
    record_id = slugify(args.name)
    path = unique_record_path(root / "observations", today, record_id)
    path.write_text(
        observation_record(
            record_id=record_id,
            title=args.name,
            today=today,
            related_changes=args.related_changes,
            impact=args.impact,
        ),
        encoding="utf-8",
    )
    update_index(root)
    print(path)
    return 0


def cmd_review(args: argparse.Namespace) -> int:
    root = Path(args.root)
    ensure_initialized(root)
    records = load_records(root)
    overdue = overdue_changes(records)

    if not overdue:
        print("No overdue changes.")
        return 0

    print("# Review Due")
    for item in overdue:
        print(f"- {item.change.id}: {'; '.join(item.reasons)}")

    if args.create:
        today = date.today()
        for item in overdue:
            record_id = f"review-{item.change.id}-{today.isoformat()}"
            path = unique_record_path(root / "reviews", today, record_id)
            path.write_text(
                review_record(
                    record_id=record_id,
                    title=item.change.id,
                    today=today,
                    related_change=item.change.id,
                ),
                encoding="utf-8",
            )
            print(f"created {path}")
        update_index(root)

    return 0


def cmd_metrics(args: argparse.Namespace) -> int:
    root = Path(args.root)
    ensure_initialized(root)
    records = load_records(root)
    markdown = render_metrics(root, records)
    print(markdown.rstrip())
    if not args.no_write:
        (root / "metrics.md").write_text(markdown, encoding="utf-8")
        update_index(root)
    return 0


def cmd_debt(args: argparse.Namespace) -> int:
    root = Path(args.root)
    ensure_initialized(root)
    records = load_records(root)
    lines = render_debt(records)
    print(lines.rstrip())
    return 0


def render_metrics(root: Path, records: list) -> str:
    statuses = status_counts(records)
    impacts = impact_counts(records)
    overdue = overdue_changes(records)
    observed = observation_counts_by_change(records)
    recurring = recurring_failure_signals(records)
    candidates = cleanup_candidates(records)

    lines = ["# Nenrin Metrics", "", "## Summary", ""]
    lines.append(f"- Change records: {sum(statuses.values())}")
    lines.append(f"- Observation records: {len(observations(records))}")
    lines.append(f"- Review overdue: {len(overdue)}")
    lines.append("")

    lines.extend(_counter_section("Status", statuses))
    lines.extend(_counter_section("Impact", impacts))

    lines.append("## Review Overdue")
    lines.append("")
    if overdue:
        for item in overdue:
            relative_path = item.change.path.relative_to(root)
            lines.append(f"- {item.change.id} ({relative_path}): {'; '.join(item.reasons)}")
    else:
        lines.append("- None")
    lines.append("")

    lines.extend(_counter_section("Recurring Failure Signals", recurring))

    lines.append("## Suggested Actions")
    lines.append("")
    if candidates:
        for candidate in candidates:
            lines.append(f"- {candidate}")
    else:
        lines.append("- None")
    lines.append("")
    return "\n".join(lines)


def render_debt(records: list) -> str:
    overdue = overdue_changes(records)
    recurring = recurring_failure_signals(records)
    candidates = cleanup_candidates(records)

    lines = ["# Improvement Debt", ""]
    lines.append("## Review Overdue")
    lines.append("")
    if overdue:
        for item in overdue:
            lines.append(f"- {item.change.id}: {'; '.join(item.reasons)}")
    else:
        lines.append("- None")
    lines.append("")

    lines.append("## Recurring Failure Signals")
    lines.append("")
    if recurring:
        for signal, count in recurring.most_common():
            lines.append(f"- {signal}: {count}")
    else:
        lines.append("- None")
    lines.append("")

    lines.append("## Cleanup Candidates")
    lines.append("")
    if candidates:
        for candidate in candidates:
            lines.append(f"- {candidate}")
    else:
        lines.append("- None")
    lines.append("")
    return "\n".join(lines)


def update_index(root: Path) -> None:
    records = load_records(root)
    statuses = status_counts(records)
    overdue = overdue_changes(records)

    lines = ["# Nenrin Index", "", "## Active Summary", ""]
    if statuses:
        for status, count in sorted(statuses.items()):
            lines.append(f"- {status}: {count}")
    else:
        lines.append("- No change records yet.")
    lines.append("")
    lines.append("## Review Due")
    lines.append("")
    if overdue:
        for item in overdue:
            lines.append(f"- {item.change.id}: {'; '.join(item.reasons)}")
    else:
        lines.append("- None")
    lines.append("")
    (root / "index.md").write_text("\n".join(lines), encoding="utf-8")


def ensure_initialized(root: Path) -> None:
    if not root.exists():
        raise SystemExit(f"Nenrin ledger not found at {root}. Run `nenrin init` first.")
    for directory in ["changes", "observations", "reviews"]:
        (root / directory).mkdir(parents=True, exist_ok=True)


def unique_record_path(directory: Path, today: date, record_id: str) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    base = directory / f"{today.isoformat()}-{record_id}.md"
    if not base.exists():
        return base

    counter = 2
    while True:
        candidate = directory / f"{today.isoformat()}-{record_id}-{counter}.md"
        if not candidate.exists():
            return candidate
        counter += 1


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "change"


def _write_once(path: Path, content: str) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _counter_section(title: str, counter) -> list[str]:
    lines = [f"## {title}", ""]
    if counter:
        for key, count in sorted(counter.items()):
            lines.append(f"- {key}: {count}")
    else:
        lines.append("- None")
    lines.append("")
    return lines


if __name__ == "__main__":
    sys.exit(main())
