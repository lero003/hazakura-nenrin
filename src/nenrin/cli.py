from __future__ import annotations

import argparse
import fnmatch
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

from . import __version__
from .frontmatter import dump_frontmatter, load_config, parse_frontmatter
from .records import (
    VALID_IMPACTS,
    changes,
    change_impact_counts,
    cleanup_candidates,
    load_records,
    observation_impact_counts,
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
    change_parser.add_argument("--review-days", type=int, default=None)
    change_parser.add_argument("--review-tasks", type=int, default=None)
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
    review_parser.add_argument("--apply", action="store_true", help="Apply completed review judgments to related change records.")
    review_parser.set_defaults(func=cmd_review)

    metrics_parser = subparsers.add_parser("metrics", help="Print metrics and update nenrin/metrics.md.")
    metrics_parser.add_argument("--no-write", action="store_true", help="Do not update metrics.md or index.md.")
    metrics_parser.set_defaults(func=cmd_metrics)

    debt_parser = subparsers.add_parser("debt", help="Print improvement debt candidates.")
    debt_parser.set_defaults(func=cmd_debt)

    brief_parser = subparsers.add_parser("brief", help="Print active observation context for the next agent session.")
    brief_parser.set_defaults(func=cmd_brief)

    diff_parser = subparsers.add_parser("diff", help="Show tracked agent-facing working tree changes.")
    diff_parser.set_defaults(func=cmd_diff)

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
    config = load_config(root / "config.yaml")
    review_defaults = config.get("review_defaults", {})
    review_days = args.review_days if args.review_days is not None else review_defaults.get("days", 7)
    review_tasks = args.review_tasks if args.review_tasks is not None else review_defaults.get("tasks", 3)
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
            review_days=review_days,
            review_tasks=review_tasks,
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

    existing_ids = {record.id for record in load_records(root) if record.type == "nenrin_change"}
    for change_id in args.related_changes:
        if change_id not in existing_ids:
            print(f"Warning: change '{change_id}' not found in ledger; observation may be orphaned.", file=sys.stderr)

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

    if args.apply:
        return _apply_reviews(root)

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
    change_impacts = change_impact_counts(records)
    observation_impacts = observation_impact_counts(records)
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
    lines.extend(_counter_section("Change Impact", change_impacts))
    lines.extend(_counter_section("Observation Impact Judgment", observation_impacts))

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


_REVIEW_JUDGMENT_MAP = {
    "keep": {"status": "reviewed", "impact": "effective"},
    "remove": {"status": "archived", "impact": "ineffective"},
    "merge": {"status": "archived", "impact": "partially_effective"},
    "narrow": {"status": "reviewed", "impact": "partially_effective"},
    "move_to_skill": {"status": "archived", "impact": "effective"},
    "move_to_handoff": {"status": "archived", "impact": "effective"},
    "move_to_checklist": {"status": "archived", "impact": "effective"},
}


def _apply_reviews(root: Path) -> int:
    records = load_records(root)
    applied = 0

    for review in records:
        if review.type != "nenrin_review":
            continue
        judgment = str(review.metadata.get("final_judgment", ""))
        if judgment == "keep_observing" or judgment not in _REVIEW_JUDGMENT_MAP:
            continue

        mapping = _REVIEW_JUDGMENT_MAP[judgment]
        related_change_id = str(review.metadata.get("related_change", ""))
        change_matches = [r for r in records if r.type == "nenrin_change" and r.id == related_change_id]

        if not change_matches:
            print(f"Warning: change '{related_change_id}' not found for review '{review.id}'.", file=sys.stderr)
            continue

        change = change_matches[0]
        text = change.path.read_text(encoding="utf-8")
        metadata, body = parse_frontmatter(text)
        metadata["status"] = mapping["status"]
        metadata["impact"] = mapping["impact"]
        change.path.write_text(dump_frontmatter(metadata, body), encoding="utf-8")
        print(f"{judgment} → {related_change_id} (status={mapping['status']}, impact={mapping['impact']})")
        applied += 1

    if applied:
        update_index(root)
    else:
        print("No review judgments to apply.")
    return 0


def cmd_brief(args: argparse.Namespace) -> int:
    root = Path(args.root)
    ensure_initialized(root)
    records = load_records(root)
    lines = render_brief(root, records)
    print(lines.rstrip())
    return 0


def render_brief(root: Path, records: list) -> str:
    active_changes = [
        r for r in changes(records)
        if r.metadata.get("status") in {"observing", "ready_for_review"}
    ]
    overdue = overdue_changes(records)
    recurring = recurring_failure_signals(records)

    lines = ["# Nenrin Brief", ""]
    lines.append("## Active Observations")
    lines.append("")
    if active_changes:
        for change in active_changes:
            lines.append(f"- {change.id}")
            watch = _extract_body_item(change.body, "Expected Behavior")
            if watch:
                lines.append(f"  - Watch: {watch}")
            risk = _extract_body_item(change.body, "Failure Signals")
            if risk:
                lines.append(f"  - Risk: {risk}")
    else:
        lines.append("- None")
    lines.append("")

    lines.append("## Review Due")
    lines.append("")
    if overdue:
        for item in overdue:
            lines.append(f"- {item.change.id}")
    else:
        lines.append("- None")
    lines.append("")

    lines.append("## Recurring Failures")
    lines.append("")
    if recurring:
        for signal, count in recurring.most_common():
            lines.append(f"- {signal} ({count}x)")
    else:
        lines.append("- None")
    lines.append("")

    return "\n".join(lines)


def cmd_diff(args: argparse.Namespace) -> int:
    root = Path(args.root)
    ensure_initialized(root)
    config = load_config(root / "config.yaml")
    tracked_patterns = [str(item) for item in _as_list(config.get("tracked_files", []))]
    project_root = root.resolve().parent

    try:
        changed_paths = git_changed_paths(project_root)
    except RuntimeError as error:
        print(f"Unable to inspect git changes: {error}", file=sys.stderr)
        return 1

    records = load_records(root)
    print(render_diff(changed_paths, tracked_patterns, records).rstrip())
    return 0


def render_diff(changed_paths: list[str], tracked_patterns: list[str], records: list) -> str:
    tracked_changes = [
        path for path in sorted(changed_paths)
        if tracked_file_matches(path, tracked_patterns)
    ]
    active_changes = [
        record
        for record in changes(records)
        if record.metadata.get("status") in {"observing", "ready_for_review"}
    ]

    lines = ["# Nenrin Diff", "", "## Tracked Changes", ""]
    if not tracked_changes:
        lines.append("- None")
        lines.append("")
        return "\n".join(lines)

    for path in tracked_changes:
        related = [
            record.id for record in active_changes
            if tracked_file_matches(path, _as_str_list(record.metadata.get("related_files", [])))
        ]
        if related:
            lines.append(f"- {path}: related active change(s): {', '.join(related)}")
        else:
            lines.append(f"- {path}: no related active change found")

    lines.append("")
    lines.append("## Suggested Action")
    lines.append("")
    lines.append("- Create or update a Nenrin change only if this is a durable agent-facing workflow change.")
    lines.append("")
    return "\n".join(lines)


def git_changed_paths(project_root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(project_root), "status", "--porcelain"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        message = result.stderr.strip() or "git status failed"
        raise RuntimeError(message)

    paths: list[str] = []
    for line in result.stdout.splitlines():
        parsed = _parse_porcelain_path(line)
        if parsed:
            paths.append(parsed)
    return paths


def tracked_file_matches(path: str, patterns: list[str]) -> bool:
    normalized = path.strip().lstrip("./")
    for pattern in patterns:
        normalized_pattern = pattern.strip().lstrip("./")
        if not normalized_pattern:
            continue
        if fnmatch.fnmatchcase(normalized, normalized_pattern):
            return True
        if "/**/" in normalized_pattern:
            shallow_pattern = normalized_pattern.replace("/**/", "/")
            if fnmatch.fnmatchcase(normalized, shallow_pattern):
                return True
    return False


def _extract_body_item(body: str, section_name: str) -> str:
    in_section = False
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            in_section = section_name.lower() in stripped.lower()
            continue
        if in_section and stripped.startswith("- "):
            item = stripped[2:].strip()
            if item.lower() not in {"tbd", ""}:
                return item
    return ""


def _parse_porcelain_path(line: str) -> str:
    if len(line) < 4:
        return ""
    path = line[3:].strip()
    if " -> " in path:
        path = path.rsplit(" -> ", 1)[1]
    return path.strip('"')


def _as_str_list(value) -> list[str]:
    return [str(item) for item in _as_list(value)]


def _as_list(value) -> list:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def update_index(root: Path) -> None:
    records = load_records(root)
    statuses = status_counts(records)
    overdue = overdue_changes(records)
    active_changes = [
        record
        for record in changes(records)
        if record.metadata.get("status") in {"observing", "ready_for_review"}
    ]

    lines = ["# Nenrin Index", "", "## Active Summary", ""]
    if statuses:
        for status, count in sorted(statuses.items()):
            lines.append(f"- {status}: {count}")
    else:
        lines.append("- No change records yet.")
    lines.append("")
    if active_changes:
        lines.append("## Active Changes")
        lines.append("")
        for record in active_changes:
            path = record.path.relative_to(root).as_posix()
            lines.append(f"- `{record.id}` - [{path}]({path})")
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
