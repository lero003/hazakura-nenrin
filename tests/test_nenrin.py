from __future__ import annotations

import io
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import date
from pathlib import Path

from nenrin.cli import build_parser, main, render_diff, tracked_file_matches, git_changed_paths
from nenrin.frontmatter import dump_frontmatter, load_config, parse_frontmatter
from nenrin.records import (
    change_impact_counts,
    cleanup_candidates,
    load_records,
    observation_impact_counts,
    overdue_changes,
    record_shape_warnings,
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

    def test_quoted_value_with_escaped_quote_round_trip(self) -> None:
        metadata = {
            "type": "nenrin_change",
            "id": "test",
            "reason": 'agent note: keep "effective" evidence strict',
        }
        text = dump_frontmatter(metadata, "# Body\n")
        parsed, body = parse_frontmatter(text)
        self.assertEqual(parsed["reason"], 'agent note: keep "effective" evidence strict')

    def test_quoted_value_with_backslash_before_quote_round_trip(self) -> None:
        metadata = {
            "type": "nenrin_change",
            "id": "test",
            "reason": 'agent note: preserve \\\\"marker"',
        }
        text = dump_frontmatter(metadata, "# Body\n")
        parsed, body = parse_frontmatter(text)
        self.assertEqual(parsed["reason"], 'agent note: preserve \\\\"marker"')
        self.assertEqual(body, "# Body\n")

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

    def test_keep_observing_review_resets_overdue_window(self) -> None:
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
            write_record(
                root / "reviews" / "2026-05-03-review-release.md",
                {
                    "type": "nenrin_review",
                    "id": "review-release",
                    "date": "2026-05-03",
                    "related_change": "release",
                    "final_judgment": "keep_observing",
                },
                "# Review\n",
            )

            records = load_records(root)

            self.assertEqual(overdue_changes(records, today=date(2026, 5, 4)), [])

    def test_observations_after_keep_observing_review_can_make_change_overdue(self) -> None:
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
                    "review_after": {"days": 7, "tasks": 1},
                },
                "# Change\n",
            )
            write_record(
                root / "reviews" / "2026-05-03-review-release.md",
                {
                    "type": "nenrin_review",
                    "id": "review-release",
                    "date": "2026-05-03",
                    "related_change": "release",
                    "final_judgment": "keep_observing",
                },
                "# Review\n",
            )
            write_record(
                root / "observations" / "2026-05-04-release.md",
                {
                    "type": "nenrin_observation",
                    "id": "release-obs",
                    "date": "2026-05-04",
                    "related_changes": ["release"],
                    "impact_judgment": "unknown",
                },
                "# Observation\n",
            )

            overdue = overdue_changes(load_records(root), today=date(2026, 5, 4))

            self.assertEqual(len(overdue), 1)
            self.assertEqual(overdue[0].change.id, "release")
            self.assertEqual(overdue[0].reasons, ("1 observation(s), review_after.tasks=1",))

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
            for impact, status, record_id in [
                ("ineffective", "observing", "removal-target"),
                ("harmful", "observing", "harmful-target"),
                ("partially_effective", "observing", "narrow-target"),
                ("effective", "observing", "stay-target"),
                ("ineffective", "archived", "already-removed"),
                ("partially_effective", "reviewed", "already-narrowed"),
            ]:
                write_record(
                    root / "changes" / f"2026-05-01-{record_id}.md",
                    {
                        "type": "nenrin_change",
                        "id": record_id,
                        "date": "2026-05-01",
                        "status": status,
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
            self.assertFalse(any("already-removed" in c for c in candidates))
            self.assertFalse(any("already-narrowed" in c for c in candidates))

    def test_record_shape_warnings_for_nonstandard_change_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "nenrin"
            write_record(
                root / "changes" / "2026-05-09-model-decision.md",
                {
                    "id": "model-decision",
                    "kind": "decision",
                    "status": "active",
                },
                "# Decision\n",
            )

            warnings = record_shape_warnings(root)

            self.assertEqual(len(warnings), 1)
            self.assertIn("missing `type`", warnings[0].message)

    def test_record_shape_warnings_for_incomplete_change_records(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "nenrin"
            write_record(
                root / "changes" / "2026-05-09-incomplete.md",
                {
                    "type": "nenrin_change",
                    "id": "incomplete",
                    "date": "2026-05-09",
                    "status": "observing",
                },
                "# Change\n",
            )

            warnings = record_shape_warnings(root)

            self.assertEqual(len(warnings), 1)
            self.assertIn("impact", warnings[0].message)
            self.assertIn("review_after", warnings[0].message)

    def test_record_shape_warnings_for_nonstandard_change_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "nenrin"
            write_record(
                root / "changes" / "2026-05-10-active-model.md",
                {
                    "type": "nenrin_change",
                    "id": "active-model",
                    "date": "2026-05-10",
                    "status": "active",
                    "impact": "positive",
                    "review_after": {"tasks": 3, "days": 7},
                },
                "# Change\n",
            )

            messages = [warning.message for warning in record_shape_warnings(root)]

            self.assertIn("nenrin_change has nonstandard status `active`", messages)
            self.assertIn("nenrin_change has nonstandard impact `positive`", messages)

    def test_record_shape_warnings_for_nonstandard_observation_impact(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "nenrin"
            write_record(
                root / "observations" / "2026-05-10-obs.md",
                {
                    "type": "nenrin_observation",
                    "id": "obs",
                    "date": "2026-05-10",
                    "related_changes": ["active-model"],
                    "impact_judgment": "validated",
                },
                "# Observation\n",
            )

            warnings = record_shape_warnings(root)

            self.assertEqual(len(warnings), 1)
            self.assertIn("nonstandard impact_judgment `validated`", warnings[0].message)

    def test_debt_reports_record_shape_warnings(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "nenrin"
            self.assertEqual(main(["--root", str(root), "init"]), 0)
            write_record(
                root / "changes" / "2026-05-09-model-decision.md",
                {
                    "id": "model-decision",
                    "kind": "decision",
                    "status": "active",
                },
                "# Decision\n",
            )

            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(main(["--root", str(root), "debt"]), 0)

            text = output.getvalue()
            self.assertIn("## Record Shape Warnings", text)
            self.assertIn("changes/2026-05-09-model-decision.md", text)

    def test_tracked_file_matches_globstar_and_shallow_paths(self) -> None:
        patterns = ["AGENTS.md", "docs/**/*.md", "skills/**/SKILL.md"]

        self.assertTrue(tracked_file_matches("AGENTS.md", patterns))
        self.assertTrue(tracked_file_matches("docs/roadmap.md", patterns))
        self.assertTrue(tracked_file_matches("docs/release/checklist.md", patterns))
        self.assertTrue(tracked_file_matches("skills/release/SKILL.md", patterns))
        self.assertTrue(tracked_file_matches("skills/release/review/SKILL.md", patterns))
        self.assertFalse(tracked_file_matches("src/nenrin/cli.py", patterns))

    def test_tracked_file_matches_single_star_stays_in_one_directory(self) -> None:
        patterns = ["docs/*.md", "skills/*/SKILL.md"]

        self.assertTrue(tracked_file_matches("docs/roadmap.md", patterns))
        self.assertTrue(tracked_file_matches("skills/release/SKILL.md", patterns))
        self.assertFalse(tracked_file_matches("docs/release/checklist.md", patterns))
        self.assertFalse(tracked_file_matches("skills/release/review/SKILL.md", patterns))

    def test_render_diff_reports_related_active_changes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "nenrin"
            write_record(
                root / "changes" / "2026-05-05-docs-guidance.md",
                {
                    "type": "nenrin_change",
                    "id": "docs-guidance",
                    "date": "2026-05-05",
                    "status": "observing",
                    "impact": "unknown",
                    "related_files": ["docs/**/*.md"],
                },
                "# Change\n",
            )
            records = load_records(root)

            output = render_diff(
                ["docs/roadmap.md", "README.md", "src/nenrin/cli.py"],
                ["README.md", "docs/**/*.md"],
                records,
            )

            self.assertIn("docs/roadmap.md: related active change(s): docs-guidance", output)
            self.assertIn("README.md: no related active change found", output)
            self.assertNotIn("src/nenrin/cli.py", output)


class CliTests(unittest.TestCase):
    def test_review_help_mentions_apply_flow(self) -> None:
        help_text = build_parser().format_help()

        self.assertIn("Show, create, or apply review records.", help_text)

    def test_init_change_observe_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "nenrin"

            self.assertEqual(main(["--root", str(root), "init"]), 0)
            self.assertTrue((root / "README.md").exists())
            self.assertTrue((root / "config.yaml").exists())
            self.assertIn(
                "  - nenrin/README.md",
                (root / "config.yaml").read_text(encoding="utf-8"),
            )

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
            metrics_text = (root / "metrics.md").read_text(encoding="utf-8")
            self.assertIn("- Change records: 1", metrics_text)
            self.assertIn("- Observation records: 1", metrics_text)

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

    def test_cmd_review_create_skips_existing_review(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "nenrin"

            self.assertEqual(main(["--root", str(root), "init"]), 0)
            main(["--root", str(root), "change", "Old Change", "--review-days", "1", "--review-tasks", "1"])
            change_files = sorted((root / "changes").glob("*.md"))
            change_text = change_files[0].read_text(encoding="utf-8")
            change_id_start = change_text.index("id: ") + 4
            change_id_end = change_text.index("\n", change_id_start)
            change_id = change_text[change_id_start:change_id_end].strip()

            main(["--root", str(root), "observe", "Old Obs", "--change", change_id])
            self.assertEqual(main(["--root", str(root), "review", "--create"]), 0)

            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(main(["--root", str(root), "review", "--create"]), 0)

            self.assertIn("No overdue changes.", output.getvalue())
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

    def test_brief_runs_on_empty_ledger(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "nenrin"

            self.assertEqual(main(["--root", str(root), "init"]), 0)
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(main(["--root", str(root), "brief"]), 0)

            self.assertIn("# Nenrin Brief", output.getvalue())
            self.assertIn("## Active Observations", output.getvalue())

    def test_brief_shows_active_observations_and_review_due(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "nenrin"

            self.assertEqual(main(["--root", str(root), "init"]), 0)
            main(["--root", str(root), "change", "Brief Test", "--review-days", "1", "--review-tasks", "1"])
            change_files = sorted((root / "changes").glob("*.md"))
            change_text = change_files[0].read_text(encoding="utf-8")
            change_id_start = change_text.index("id: ") + 4
            change_id_end = change_text.index("\n", change_id_start)
            change_id = change_text[change_id_start:change_id_end].strip()

            main(["--root", str(root), "observe", "Brief Obs", "--change", change_id])

            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(main(["--root", str(root), "brief"]), 0)

            self.assertIn(change_id, output.getvalue())

    def test_brief_puts_review_due_before_active_observations(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "nenrin"

            self.assertEqual(main(["--root", str(root), "init"]), 0)
            main(["--root", str(root), "change", "Brief Order", "--review-days", "0"])

            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(main(["--root", str(root), "brief"]), 0)

            text = output.getvalue()
            self.assertLess(
                text.index("## Review Due"),
                text.index("## Active Observations"),
            )

    def test_review_apply_updates_change_status_and_impact(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "nenrin"

            self.assertEqual(main(["--root", str(root), "init"]), 0)
            main(["--root", str(root), "change", "ApplyTest", "--review-days", "1", "--review-tasks", "1"])
            change_files = sorted((root / "changes").glob("*.md"))
            change_text = change_files[0].read_text(encoding="utf-8")
            change_id_start = change_text.index("id: ") + 4
            change_id_end = change_text.index("\n", change_id_start)
            change_id = change_text[change_id_start:change_id_end].strip()

            main(["--root", str(root), "observe", "App Obs", "--change", change_id])

            # Create a review template
            main(["--root", str(root), "review", "--create"])

            # Fill in the review with a final judgment
            review_files = sorted((root / "reviews").glob("*.md"))
            self.assertEqual(len(review_files), 1)
            review_text = review_files[0].read_text(encoding="utf-8")
            review_text = review_text.replace("keep_observing", "keep")
            review_files[0].write_text(review_text, encoding="utf-8")

            # Apply
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(main(["--root", str(root), "review", "--apply"]), 0)

            self.assertIn("keep → applytest", output.getvalue())
            self.assertIn("status=reviewed", output.getvalue())
            self.assertIn("impact=effective", output.getvalue())

            # Verify the change record was updated
            updated_text = change_files[0].read_text(encoding="utf-8")
            self.assertIn("status: reviewed", updated_text)
            self.assertIn("impact: effective", updated_text)
            metrics_text = (root / "metrics.md").read_text(encoding="utf-8")
            self.assertIn("- reviewed: 1", metrics_text)
            self.assertIn("- effective: 1", metrics_text)

    def test_review_apply_warns_on_unsupported_final_judgment(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "nenrin"

            self.assertEqual(main(["--root", str(root), "init"]), 0)
            main(["--root", str(root), "change", "TypoTest", "--review-days", "1", "--review-tasks", "1"])
            change_files = sorted((root / "changes").glob("*.md"))
            change_text = change_files[0].read_text(encoding="utf-8")
            change_id_start = change_text.index("id: ") + 4
            change_id_end = change_text.index("\n", change_id_start)
            change_id = change_text[change_id_start:change_id_end].strip()

            main(["--root", str(root), "observe", "Typo Obs", "--change", change_id])
            main(["--root", str(root), "review", "--create"])

            review_files = sorted((root / "reviews").glob("*.md"))
            review_text = review_files[0].read_text(encoding="utf-8")
            review_text = review_text.replace("keep_observing", "keep_typo")
            review_files[0].write_text(review_text, encoding="utf-8")

            stderr = io.StringIO()
            with redirect_stderr(stderr):
                self.assertEqual(main(["--root", str(root), "review", "--apply"]), 0)

            self.assertIn("unsupported final_judgment 'keep_typo'", stderr.getvalue())
            unchanged_text = change_files[0].read_text(encoding="utf-8")
            self.assertIn("status: observing", unchanged_text)
            self.assertIn("impact: unknown", unchanged_text)

    def test_review_apply_skips_already_applied_judgment(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "nenrin"

            self.assertEqual(main(["--root", str(root), "init"]), 0)
            main(["--root", str(root), "change", "Already Applied", "--review-days", "1", "--review-tasks", "1"])
            change_files = sorted((root / "changes").glob("*.md"))
            change_text = change_files[0].read_text(encoding="utf-8")
            change_id_start = change_text.index("id: ") + 4
            change_id_end = change_text.index("\n", change_id_start)
            change_id = change_text[change_id_start:change_id_end].strip()

            main(["--root", str(root), "observe", "Already Applied Obs", "--change", change_id])
            main(["--root", str(root), "review", "--create"])

            review_files = sorted((root / "reviews").glob("*.md"))
            review_text = review_files[0].read_text(encoding="utf-8")
            review_files[0].write_text(review_text.replace("keep_observing", "keep"), encoding="utf-8")

            self.assertEqual(main(["--root", str(root), "review", "--apply"]), 0)

            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(main(["--root", str(root), "review", "--apply"]), 0)

            self.assertIn("No review judgments to apply.", output.getvalue())
            self.assertNotIn("keep \u2192 already-applied", output.getvalue())

    def test_diff_reports_no_tracked_changes_on_clean_temp_repo(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            root = project / "nenrin"

            self.assertEqual(main(["--root", str(root), "init"]), 0)
            subprocess_run(["git", "init"], cwd=project)
            subprocess_run(["git", "add", "."], cwd=project)
            subprocess_run(
                ["git", "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-m", "init"],
                cwd=project,
            )

            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(main(["--root", str(root), "diff"]), 0)

            self.assertIn("# Nenrin Diff", output.getvalue())
            self.assertIn("- None", output.getvalue())

    def test_diff_reports_dirty_tracked_docs_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            root = project / "nenrin"

            self.assertEqual(main(["--root", str(root), "init"]), 0)
            docs = project / "docs"
            docs.mkdir()
            roadmap = docs / "roadmap.md"
            roadmap.write_text("# Roadmap\n", encoding="utf-8")
            subprocess_run(["git", "init"], cwd=project)
            subprocess_run(["git", "add", "."], cwd=project)
            subprocess_run(
                ["git", "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-m", "init"],
                cwd=project,
            )
            roadmap.write_text("# Roadmap\n\nUpdated guidance.\n", encoding="utf-8")

            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(main(["--root", str(root), "diff"]), 0)

            self.assertIn("docs/roadmap.md: no related active change found", output.getvalue())
            self.assertIn("Create or update a Nenrin change only if", output.getvalue())

    def test_diff_reports_dirty_ledger_readme(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            root = project / "nenrin"

            self.assertEqual(main(["--root", str(root), "init"]), 0)
            subprocess_run(["git", "init"], cwd=project)
            subprocess_run(["git", "add", "."], cwd=project)
            subprocess_run(
                ["git", "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-m", "init"],
                cwd=project,
            )
            readme = root / "README.md"
            readme.write_text(readme.read_text(encoding="utf-8") + "\nAgent note.\n", encoding="utf-8")

            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(main(["--root", str(root), "diff"]), 0)

            self.assertIn("nenrin/README.md: no related active change found", output.getvalue())

    def test_diff_reports_untracked_docs_even_when_status_hides_untracked(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            root = project / "nenrin"

            self.assertEqual(main(["--root", str(root), "init"]), 0)
            subprocess_run(["git", "init"], cwd=project)
            subprocess_run(["git", "config", "status.showUntrackedFiles", "no"], cwd=project)
            subprocess_run(["git", "add", "."], cwd=project)
            subprocess_run(
                ["git", "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-m", "init"],
                cwd=project,
            )
            docs = project / "docs"
            docs.mkdir()
            (docs / "new-guidance.md").write_text("# Guidance\n", encoding="utf-8")

            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(main(["--root", str(root), "diff"]), 0)

            self.assertIn("docs/new-guidance.md: no related active change found", output.getvalue())

    def test_diff_keeps_untracked_paths_with_spaces_unquoted(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            root = project / "nenrin"

            self.assertEqual(main(["--root", str(root), "init"]), 0)
            subprocess_run(["git", "init"], cwd=project)
            subprocess_run(["git", "add", "."], cwd=project)
            subprocess_run(
                ["git", "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-m", "init"],
                cwd=project,
            )
            docs = project / "docs"
            docs.mkdir()
            (docs / "agent guidance.md").write_text("# Guidance\n", encoding="utf-8")

            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(main(["--root", str(root), "diff"]), 0)

            self.assertIn("docs/agent guidance.md: no related active change found", output.getvalue())
            self.assertNotIn('"docs/agent guidance.md"', output.getvalue())

    def test_diff_preserves_inner_spaces_in_porcelain_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            root = project / "nenrin"

            self.assertEqual(main(["--root", str(root), "init"]), 0)
            subprocess_run(["git", "init"], cwd=project)
            subprocess_run(["git", "add", "."], cwd=project)
            subprocess_run(
                ["git", "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-m", "init"],
                cwd=project,
            )
            docs = project / "docs"
            docs.mkdir()
            (docs / "agent guidance .md").write_text("# Guidance\n", encoding="utf-8")

            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(main(["--root", str(root), "diff"]), 0)

            self.assertIn("docs/agent guidance .md: no related active change found", output.getvalue())
            self.assertNotIn("docs/agent guidance.md: no related active change found", output.getvalue())

    def test_tracked_file_matching_preserves_path_boundary_spaces(self) -> None:
        self.assertTrue(tracked_file_matches("./docs/agent guidance.md", [" docs/**/*.md "]))
        self.assertFalse(tracked_file_matches("docs/agent guidance.md ", ["docs/**/*.md"]))
        self.assertFalse(tracked_file_matches(" docs/agent guidance.md", ["docs/**/*.md"]))

    def test_git_changed_paths_reports_rename_target_with_spaces(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            docs = project / "docs"
            docs.mkdir()
            old_path = docs / "old guidance.md"
            old_path.write_text("# Guidance\n", encoding="utf-8")
            subprocess_run(["git", "init"], cwd=project)
            subprocess_run(["git", "add", "."], cwd=project)
            subprocess_run(
                ["git", "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-m", "init"],
                cwd=project,
            )

            new_path = docs / "new guidance.md"
            old_path.rename(new_path)
            subprocess_run(["git", "add", "-A"], cwd=project)

            self.assertEqual(git_changed_paths(project), ["docs/new guidance.md"])


def write_record(path: Path, metadata: dict, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump_frontmatter(metadata, body), encoding="utf-8")


def subprocess_run(command: list[str], *, cwd: Path) -> None:
    import subprocess

    result = subprocess.run(
        command,
        cwd=cwd,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        raise AssertionError(result.stderr or result.stdout)


if __name__ == "__main__":
    unittest.main()
