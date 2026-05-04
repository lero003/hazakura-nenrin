from __future__ import annotations

import io
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import date
from pathlib import Path

from nenrin.cli import main
from nenrin.frontmatter import dump_frontmatter, load_config, parse_frontmatter
from nenrin.records import (
    change_impact_counts,
    cleanup_candidates,
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

    def test_empty_list_and_dict_round_trip(self) -> None:
        metadata = {"type": "nenrin_change", "id": "test", "items": [], "mapping": {}}
        text = dump_frontmatter(metadata, "# Body\n")
        parsed, body = parse_frontmatter(text)
        self.assertEqual(parsed["items"], [])
        self.assertEqual(parsed["mapping"], {})
        self.assertEqual(body, "# Body\n")

    def test_quoted_value_with_colon_round_trip(self) -> None:
        metadata = {
            "type": "nenrin_change",
            "id": "test",
            "reason": "check: the colon should survive",
        }
        text = dump_frontmatter(metadata, "# Body\n")
        parsed, body = parse_frontmatter(text)
        self.assertEqual(parsed["reason"], "check: the colon should survive")

    def test_special_chars_in_value_round_trip(self) -> None:
        metadata = {
            "type": "nenrin_change",
            "id": "test",
            "note": "value with # hash and [brackets]",
            "empty_list": [],
            "empty_dict": {},
        }
        text = dump_frontmatter(metadata, "# Body\n")
        parsed, body = parse_frontmatter(text)
        self.assertEqual(parsed["note"], "value with # hash and [brackets]")
        self.assertEqual(parsed["empty_list"], [])
        self.assertEqual(parsed["empty_dict"], {})


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

    def test_config_loading(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "nenrin"
            (root).mkdir()
            (root / "config.yaml").write_text(
                "review_defaults:\n  tasks: 5\n  days: 14\n",
                encoding="utf-8",
            )
            config = load_config(root / "config.yaml")
            self.assertEqual(config["review_defaults"]["tasks"], 5)
            self.assertEqual(config["review_defaults"]["days"], 14)

    def test_config_loading_missing_file_returns_empty_dict(self) -> None:
        config = load_config(Path("/nonexistent/config.yaml"))
        self.assertEqual(config, {})

    def test_cleanup_candidates_by_impact(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "nenrin"
            for impact, record_id in [
                ("ineffective", "removal-target"),
                ("harmful", "harmful-target"),
                ("partially_effective", "narrow-target"),
                ("effective", "stay-target"),
            ]:
                write_record(
                    root / "changes" / f"2026-05-01-{record_id}.md",
                    {
                        "type": "nenrin_change",
                        "id": record_id,
                        "date": "2026-05-01",
                        "status": "observing",
                        "impact": impact,
                    },
                    "# Change\n",
                )

            records = load_records(root)
            candidates = cleanup_candidates(records)

            self.assertTrue(any("removal-target" in c for c in candidates))
            self.assertTrue(any("harmful-target" in c for c in candidates))
            self.assertTrue(any("narrow-target" in c for c in candidates))
            self.assertFalse(any("stay-target" in c for c in candidates))


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

    def test_cmd_review_creates_templates(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "nenrin"

            self.assertEqual(main(["--root", str(root), "init"]), 0)
            # Create an overdue change
            main(["--root", str(root), "change", "Old Change", "--review-days", "1", "--review-tasks", "1"])
            # This observation pushes it over the task threshold
            change_files = sorted((root / "changes").glob("*.md"))
            change_text = change_files[0].read_text(encoding="utf-8")
            change_id_start = change_text.index("id: ") + 4
            change_id_end = change_text.index("\n", change_id_start)
            change_id = change_text[change_id_start:change_id_end].strip()

            main(["--root", str(root), "observe", "Old Obs", "--change", change_id])

            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(main(["--root", str(root), "review", "--create"]), 0)

            self.assertIn("created", output.getvalue())
            review_files = list((root / "reviews").glob("*.md"))
            self.assertEqual(len(review_files), 1)

    def test_observe_warns_orphan_change(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "nenrin"

            self.assertEqual(main(["--root", str(root), "init"]), 0)
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                self.assertEqual(
                    main(["--root", str(root), "observe", "Orphan Obs", "--change", "nonexistent-id"]),
                    0,
                )
            self.assertIn("Warning: change 'nonexistent-id' not found", stderr.getvalue())

    def test_unique_record_path_collision(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "nenrin"

            self.assertEqual(main(["--root", str(root), "init"]), 0)
            self.assertEqual(main(["--root", str(root), "change", "Duplicate"]), 0)
            self.assertEqual(main(["--root", str(root), "change", "Duplicate"]), 0)
            change_files = sorted((root / "changes").glob("*.md"))
            self.assertEqual(len(change_files), 2)
            self.assertIn("-duplicate-2.md", change_files[0].name)

    def test_slugify_handles_special_chars(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "nenrin"

            self.assertEqual(main(["--root", str(root), "init"]), 0)
            self.assertEqual(main(["--root", str(root), "change", "Feature: X!@#$%^&*()"]), 0)
            change_files = list((root / "changes").glob("*.md"))
            self.assertEqual(len(change_files), 1)
            self.assertIn("feature-x", change_files[0].name)

    def test_change_uses_config_review_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "nenrin"

            self.assertEqual(main(["--root", str(root), "init"]), 0)
            # Override config defaults
            (root / "config.yaml").write_text(
                "review_defaults:\n  tasks: 10\n  days: 30\n",
                encoding="utf-8",
            )
            self.assertEqual(main(["--root", str(root), "change", "ConfigTest"]), 0)
            change_files = list((root / "changes").glob("*.md"))
            content = change_files[0].read_text(encoding="utf-8")
            self.assertIn("tasks: 10", content)
            self.assertIn("days: 30", content)


def write_record(path: Path, metadata: dict, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump_frontmatter(metadata, body), encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
