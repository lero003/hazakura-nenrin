from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from .frontmatter import parse_frontmatter


VALID_IMPACTS = {"unknown", "effective", "partially_effective", "ineffective", "harmful"}
VALID_STATUSES = {"draft", "observing", "ready_for_review", "reviewed", "archived"}

_PLACEHOLDER_FAILURE_SIGNALS = {
    "none",
    "none observed",
    "none observed in this slice",
    "none in this run",
    "none in this task",
    "no failure signals observed",
    "no failure signals observed yet",
    "tbd",
}


@dataclass(frozen=True)
class Record:
    path: Path
    metadata: dict[str, Any]
    body: str

    @property
    def id(self) -> str:
        return str(self.metadata.get("id", self.path.stem))

    @property
    def type(self) -> str:
        return str(self.metadata.get("type", ""))


@dataclass(frozen=True)
class OverdueChange:
    change: Record
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class RecordShapeWarning:
    path: Path
    message: str


def load_records(root: Path) -> list[Record]:
    records: list[Record] = []
    if not root.exists():
        return records

    for path in sorted(root.glob("**/*.md")):
        if _should_skip_record_path(root, path):
            continue
        text = path.read_text(encoding="utf-8")
        metadata, body = parse_frontmatter(text)
        if metadata.get("type"):
            records.append(Record(path=path, metadata=metadata, body=body))

    return records


def record_shape_warnings(root: Path) -> list[RecordShapeWarning]:
    warnings: list[RecordShapeWarning] = []
    if not root.exists():
        return warnings

    for path in sorted(root.glob("**/*.md")):
        if _should_skip_record_path(root, path):
            continue

        metadata, _body = parse_frontmatter(path.read_text(encoding="utf-8"))
        if not metadata:
            continue

        relative_parts = path.relative_to(root).parts
        if not relative_parts:
            continue

        collection = relative_parts[0]
        record_type = str(metadata.get("type", "")).strip()
        if collection in {"changes", "observations", "reviews"} and not record_type:
            warnings.append(
                RecordShapeWarning(
                    path=path,
                    message="frontmatter is missing `type`, so Nenrin ignores this file",
                )
            )
            continue

        if collection == "changes" and record_type == "nenrin_change":
            missing = [
                key
                for key in ("status", "impact", "review_after")
                if key not in metadata or metadata.get(key) in (None, "")
            ]
            if missing:
                warnings.append(
                    RecordShapeWarning(
                        path=path,
                        message=f"nenrin_change is missing {', '.join(missing)}",
                    )
                )

            status = str(metadata.get("status", "")).strip()
            if status and status not in VALID_STATUSES:
                warnings.append(
                    RecordShapeWarning(
                        path=path,
                        message=f"nenrin_change has nonstandard status `{status}`",
                    )
                )

            impact = str(metadata.get("impact", "")).strip()
            if impact and impact not in VALID_IMPACTS:
                warnings.append(
                    RecordShapeWarning(
                        path=path,
                        message=f"nenrin_change has nonstandard impact `{impact}`",
                    )
                )

        if collection == "observations" and record_type == "nenrin_observation":
            judgment = str(metadata.get("impact_judgment", "")).strip()
            if judgment and judgment not in VALID_IMPACTS:
                warnings.append(
                    RecordShapeWarning(
                        path=path,
                        message=f"nenrin_observation has nonstandard impact_judgment `{judgment}`",
                    )
                )

        if collection == "reviews" and record_type == "nenrin_review":
            judgment = str(metadata.get("final_judgment", "")).strip()
            if judgment == "keep_observing" and not _has_substantive_section_content(_body, "Observe Next"):
                warnings.append(
                    RecordShapeWarning(
                        path=path,
                        message="review uses final_judgment: keep_observing but Observe Next appears empty",
                    )
                )

    return warnings


def _has_substantive_section_content(body: str, heading: str) -> bool:
    section_lines = _markdown_section_lines(body, heading)
    if not section_lines:
        return False

    placeholders = {"-", "tbd", "- tbd", "todo", "- todo"}
    for line in section_lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.lower() in placeholders:
            continue
        return True
    return False


def _markdown_section_lines(body: str, heading: str) -> list[str]:
    target = f"## {heading}".lower()
    in_section = False
    lines: list[str] = []

    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            if in_section:
                break
            if stripped.lower() == target:
                in_section = True
            continue
        if in_section:
            lines.append(line)

    return lines


def changes(records: list[Record]) -> list[Record]:
    return [record for record in records if record.type == "nenrin_change"]


def observations(records: list[Record]) -> list[Record]:
    return [record for record in records if record.type == "nenrin_observation"]


def status_counts(records: list[Record]) -> Counter[str]:
    return Counter(str(record.metadata.get("status", "unknown")) for record in changes(records))


def change_impact_counts(records: list[Record]) -> Counter[str]:
    return Counter(str(record.metadata.get("impact", "unknown")) for record in changes(records))


def observation_impact_counts(records: list[Record]) -> Counter[str]:
    return Counter(
        str(record.metadata.get("impact_judgment", "unknown")) for record in observations(records)
    )


def observation_counts_by_change(
    records: list[Record],
    after_dates: dict[str, date] | None = None,
) -> Counter[str]:
    after_dates = after_dates or {}
    counter: Counter[str] = Counter()
    for record in observations(records):
        related = record.metadata.get("related_changes", [])
        if isinstance(related, str):
            related = [related]
        for change_id in related:
            change_id = str(change_id)
            cutoff = after_dates.get(change_id)
            if cutoff is not None:
                observation_date = _parse_date(str(record.metadata.get("date", "")))
                if observation_date is None or observation_date <= cutoff:
                    continue
            counter[change_id] += 1
    return counter


def keep_observing_review_dates(records: list[Record]) -> dict[str, date]:
    latest: dict[str, date] = {}
    for record in records:
        if record.type != "nenrin_review":
            continue
        if str(record.metadata.get("final_judgment", "")).strip() != "keep_observing":
            continue

        related_change = str(record.metadata.get("related_change", "")).strip()
        review_date = _parse_date(str(record.metadata.get("date", "")))
        if not related_change or review_date is None:
            continue

        previous = latest.get(related_change)
        if previous is None or review_date > previous:
            latest[related_change] = review_date
    return latest


def overdue_changes(records: list[Record], today: date | None = None) -> list[OverdueChange]:
    today = today or date.today()
    latest_reviews = keep_observing_review_dates(records)
    observed_counts = observation_counts_by_change(records, after_dates=latest_reviews)
    overdue: list[OverdueChange] = []

    for change in changes(records):
        if change.metadata.get("status") not in {"observing", "ready_for_review"}:
            continue

        reasons: list[str] = []
        review_after = change.metadata.get("review_after", {})
        if not isinstance(review_after, dict):
            review_after = {}

        due_days = _int_or_none(review_after.get("days"))
        due_tasks = _int_or_none(review_after.get("tasks"))
        change_date = _parse_date(str(change.metadata.get("date", "")))
        baseline_date = latest_reviews.get(change.id, change_date)

        if due_days is not None and baseline_date is not None:
            age_days = (today - baseline_date).days
            if age_days >= due_days:
                reasons.append(f"{age_days} day(s) old, review_after.days={due_days}")

        if due_tasks is not None and observed_counts[change.id] >= due_tasks:
            reasons.append(
                f"{observed_counts[change.id]} observation(s), review_after.tasks={due_tasks}"
            )

        if reasons:
            overdue.append(OverdueChange(change=change, reasons=tuple(reasons)))

    return overdue


def recurring_failure_signals(records: list[Record]) -> Counter[str]:
    counter: Counter[str] = Counter()
    for record in observations(records):
        for tag in _as_list(record.metadata.get("failure_tags", [])):
            counter[f"tag:{tag}"] += 1

        in_failure_section = False
        for raw_line in record.body.splitlines():
            line = raw_line.strip()
            if line.startswith("## "):
                in_failure_section = "failure" in line.lower()
                continue
            if in_failure_section and line.startswith("- "):
                signal = line[2:].strip()
                if signal and not _is_placeholder_signal(signal):
                    counter[signal] += 1
    return Counter({key: value for key, value in counter.items() if value > 1})


def cleanup_candidates(records: list[Record]) -> list[str]:
    candidates: list[str] = []
    for record in changes(records):
        if record.metadata.get("status") not in {"observing", "ready_for_review"}:
            continue
        impact = str(record.metadata.get("impact", "unknown"))
        if impact == "ineffective":
            candidates.append(f"{record.id}: consider remove, merge, narrow, or move")
        elif impact == "harmful":
            candidates.append(f"{record.id}: consider removal or immediate narrowing")
        elif impact == "partially_effective":
            candidates.append(f"{record.id}: consider narrowing or moving details to a skill/checklist")

    for signal, count in recurring_failure_signals(records).items():
        candidates.append(f"Recurring failure ({count}x): {signal}")

    return candidates


def _parse_date(value: str) -> date | None:
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _int_or_none(value: Any) -> int | None:
    if isinstance(value, int):
        return value
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _is_placeholder_signal(value: str) -> bool:
    normalized = value.strip().lower().rstrip(".。")
    return normalized in _PLACEHOLDER_FAILURE_SIGNALS


def _should_skip_record_path(root: Path, path: Path) -> bool:
    relative_parts = path.relative_to(root).parts
    if "templates" in relative_parts:
        return True
    return path.name in {"README.md", "index.md", "metrics.md"}
