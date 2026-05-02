from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from .frontmatter import parse_frontmatter


VALID_IMPACTS = {"unknown", "effective", "partially_effective", "ineffective", "harmful"}


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


def load_records(root: Path) -> list[Record]:
    records: list[Record] = []
    if not root.exists():
        return records

    for path in sorted(root.glob("**/*.md")):
        if "templates" in path.relative_to(root).parts:
            continue
        if path.name in {"README.md", "index.md", "metrics.md"}:
            continue
        text = path.read_text(encoding="utf-8")
        metadata, body = parse_frontmatter(text)
        if metadata.get("type"):
            records.append(Record(path=path, metadata=metadata, body=body))

    return records


def changes(records: list[Record]) -> list[Record]:
    return [record for record in records if record.type == "nenrin_change"]


def observations(records: list[Record]) -> list[Record]:
    return [record for record in records if record.type == "nenrin_observation"]


def status_counts(records: list[Record]) -> Counter[str]:
    return Counter(str(record.metadata.get("status", "unknown")) for record in changes(records))


def impact_counts(records: list[Record]) -> Counter[str]:
    counter: Counter[str] = Counter()
    for record in changes(records):
        counter[str(record.metadata.get("impact", "unknown"))] += 1
    for record in observations(records):
        counter[str(record.metadata.get("impact_judgment", "unknown"))] += 1
    return counter


def observation_counts_by_change(records: list[Record]) -> Counter[str]:
    counter: Counter[str] = Counter()
    for record in observations(records):
        related = record.metadata.get("related_changes", [])
        if isinstance(related, str):
            related = [related]
        for change_id in related:
            counter[str(change_id)] += 1
    return counter


def overdue_changes(records: list[Record], today: date | None = None) -> list[OverdueChange]:
    today = today or date.today()
    observed_counts = observation_counts_by_change(records)
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

        if due_days is not None and change_date is not None:
            age_days = (today - change_date).days
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
        in_failure_section = False
        for raw_line in record.body.splitlines():
            line = raw_line.strip()
            if line.startswith("## "):
                in_failure_section = "failure" in line.lower()
                continue
            if in_failure_section and line.startswith("- "):
                signal = line[2:].strip()
                if signal and signal.upper() != "TBD":
                    counter[signal] += 1
    return Counter({key: value for key, value in counter.items() if value > 1})


def cleanup_candidates(records: list[Record]) -> list[str]:
    candidates: list[str] = []
    for record in changes(records):
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
