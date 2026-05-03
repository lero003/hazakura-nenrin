from __future__ import annotations

import io
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import date
from pathlib import Path

from nenrin.cli import main
from nenrin.frontmatter import dump_frontmatter, parse_frontmatter
from nenrin.records import (
    change_impact_counts,
    load_records,
    observation_impact_counts,
    overdue_changes,
    recurring_failure_signals,
    status_counts,
)


class FrontmatterTests(unittest.TestCase):
    def test_frontmatter_round_trip_small_yaml_subset(self) -> None:
        metadata = {
            "type": "nenrin_change",
            "id": "release-review",
            "status": "observing",
            "related_files": ["AGENTS.md", "docs/release.md"],
            "review_after": {"tasks": 3, "days": 7},
        }

        text = dump_frontmatter(metadata, "# Body\n")
        parsed, body = parse_frontmatter(text)

        self.assertEqual(parsed, metadata)
        self.assertEqual(body, "# Body\n")


class RecordTests(unittest.TestCase):
    def test_metrics_aggregation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "nenrin"
            write_record(
                root / "changes" / "2026-05-01-release.md",
                {
                    "type": "nenrin_change",
                    "id": "release",
                    "date": "2026-05-01",
                    "status": "observing",
                    "impact": "unknown",
                },
                "# Change\n",
            )
            write_record(
                root / "observations" / "2026-05-02-release.md",
                {
                    "type": "nenrin_observation",
                    "id": "release-obs",
                    "date": "2026-05-02",
                    "related_changes": ["release"],
                    "impact_judgment": "partially_effective",
                },
                "# Observation\n",
            )

            records = load_records(root)

            self.assertEqual(status_counts(records)["observing"], 1)
            self.assertEqual(change_impact_counts(records)["unknown"], 1)
            self.assertEqual(observation_impact_counts(records)["partially_effective"], 1)

    def test_templates_are_not_records(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "nenrin"
            write_record(
                root / "templates" / "change.md",
                {
                    "type": "nenrin_change",
                    "id": "template",
                    "date": "2026-05-01",
                    "status": "observing",
                },
                "# Template\n",
            )

            self.assertEqual(load_records(root), [])

    def test_overdue_review_detection_by_days_and_tasks(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "nenrin"
            write_record(
                root / "changes" / "2026-05-01-release.md",
                {
                    "type": "nenrin_change",
                    "id": "release",
                    "date": "2026-05-01",
                    "status": "observing",
                    "impact": "unknown",
                    "review_after": {"days": 2, "tasks": 1},
                },
                "# Change\n",
            )
            write_record(
                root / "observations" / "2026-05-02-release.md",
                {
                    "type": "nenrin_observation",
                    "id": "release-obs",
                    "date": "2026-05-02",
                    "related_changes": ["release"],
                    "impact_judgment": "unknown",
                },
                "# Observation\n",
            )

            records = load_records(root)
            overdue = overdue_changes(records, today=date(2026, 5, 3))

            self.assertEqual(len(overdue), 1)
            self.assertEqual(overdue[0].change.id, "release")
            self.assertEqual(len(overdue[0].reasons), 2)

    def test_recurring_failure_signals(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "nenrin"
            for index in range(2):
                write_record(
                    root / "observations" / f"2026-05-0{index + 1}-obs.md",
                    {
                        "type": "nenrin_observation",
                        "id": f"obs-{index}",
                        "date": f"2026-05-0{index + 1}",
                        "related_changes": ["release"],
                        "impact_judgment": "partially_effective",
                    },
                    """# Observation

## Failure Signals Observed

- changelog check missed
""",
                )

            records = load_records(root)

            self.assertEqual(recurring_failure_signals(records)["changelog check missed"], 2)

    def test_recurring_failure_signals_ignore_none_placeholders(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "nenrin"
            placeholders = [
                "None observed in this slice.",
                "None in this task.",
                "No failure signals observed yet.",
            ]
            for index, placeholder in enumerate(placeholders):
                write_record(
                    root / "observations" / f"2026-05-0{index + 1}-obs.md",
                    {
                        "type": "nenrin_observation",
                        "id": f"obs-{index}",
                        "date": f"2026-05-0{index + 1}",
                        "related_changes": ["release"],
                        "impact_judgment": "effective",
                    },
                    f"""# Observation

## Failure Signals Observed

- {placeholder}
""",
                )

            records = load_records(root)

            self.assertEqual(recurring_failure_signals(records), {})

    def test_recurring_failure_tags(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "nenrin"
            for index in range(2):
                write_record(
                    root / "observations" / f"2026-05-0{index + 1}-obs.md",
                    {
                        "type": "nenrin_observation",
                        "id": f"obs-{index}",
                        "date": f"2026-05-0{index + 1}",
                        "related_changes": ["release"],
                        "impact_judgment": "partially_effective",
                        "failure_tags": ["changelog_consistency_missed"],
                    },
                    "# Observation\n",
                )

            records = load_records(root)

            self.assertEqual(
                recurring_failure_signals(records)["tag:changelog_consistency_missed"],
                2,
            )


class CliTests(unittest.TestCase):
    def test_init_change_observe_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "nenrin"

            self.assertEqual(main(["--root", str(root), "init"]), 0)
            self.assertTrue((root / "README.md").exists())
            self.assertTrue((root / "config.yaml").exists())

            self.assertEqual(main(["--root", str(root), "change", "Release Review"]), 0)
            change_files = list((root / "changes").glob("*.md"))
            self.assertEqual(len(change_files), 1)
            self.assertIn("id: release-review", change_files[0].read_text(encoding="utf-8"))

            self.assertEqual(
                main(["--root", str(root), "observe", "Release Review Obs", "--change", "release-review"]),
                0,
            )
            observation_files = list((root / "observations").glob("*.md"))
            self.assertEqual(len(observation_files), 1)

            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(main(["--root", str(root), "metrics"]), 0)

            self.assertIn("# Nenrin Metrics", output.getvalue())
            self.assertTrue((root / "metrics.md").exists())
            index_text = (root / "index.md").read_text(encoding="utf-8")
            self.assertIn("## Active Changes", index_text)
            self.assertIn("- `release-review` - [changes/", index_text)

    def test_debt_runs_on_empty_ledger(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "nenrin"

            self.assertEqual(main(["--root", str(root), "init"]), 0)
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(main(["--root", str(root), "debt"]), 0)

            self.assertIn("# Improvement Debt", output.getvalue())


def write_record(path: Path, metadata: dict, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump_frontmatter(metadata, body), encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
