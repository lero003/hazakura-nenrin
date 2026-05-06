from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Parse the small YAML subset Nenrin writes in Markdown records."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text

    end_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_index = index
            break

    if end_index is None:
        return {}, text

    metadata = _parse_mapping(lines[1:end_index])
    body = "\n".join(lines[end_index + 1 :]).lstrip("\n")
    if body and text.endswith("\n"):
        body += "\n"
    return metadata, body


def dump_frontmatter(metadata: Mapping[str, Any], body: str) -> str:
    frontmatter = "\n".join(_dump_mapping(metadata))
    normalized_body = body.strip() + "\n"
    return f"---\n{frontmatter}\n---\n\n{normalized_body}"


def _parse_mapping(lines: list[str]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    index = 0

    while index < len(lines):
        line = lines[index]
        if not line.strip() or line.lstrip().startswith("#"):
            index += 1
            continue

        if line.startswith(" ") or ":" not in line:
            index += 1
            continue

        key, raw_value = line.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()

        if raw_value:
            result[key] = _parse_scalar(raw_value)
            index += 1
            continue

        nested: list[str] = []
        index += 1
        while index < len(lines) and lines[index].startswith("  "):
            nested.append(lines[index][2:])
            index += 1

        if nested and all(item.strip().startswith("- ") for item in nested if item.strip()):
            result[key] = [
                _parse_scalar(item.strip()[2:].strip())
                for item in nested
                if item.strip().startswith("- ")
            ]
        else:
            result[key] = _parse_mapping(nested)

    return result


def _parse_scalar(value: str) -> Any:
    if value == "[]":
        return []
    if value == "{}":
        return {}
    if value == "":
        return None
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if value.lower() in {"null", "none"}:
        return None
    if value.startswith('"') and value.endswith('"'):
        return _unescape_double_quoted(value[1:-1])
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    try:
        return int(value)
    except ValueError:
        return value


def _dump_mapping(metadata: Mapping[str, Any], indent: int = 0) -> list[str]:
    lines: list[str] = []
    prefix = " " * indent

    for key, value in metadata.items():
        if isinstance(value, Mapping):
            lines.append(f"{prefix}{key}:")
            lines.extend(_dump_mapping(value, indent + 2))
        elif isinstance(value, list):
            if value:
                lines.append(f"{prefix}{key}:")
                for item in value:
                    lines.append(f"{prefix}  - {_format_scalar(item)}")
            else:
                lines.append(f"{prefix}{key}: []")
        else:
            lines.append(f"{prefix}{key}: {_format_scalar(value)}")

    return lines


def _format_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    text = str(value)
    if not text:
        return '""'
    if any(char in text for char in [":", "#", "[", "]", "{", "}", ","]):
        return '"' + text.replace('"', '\\"') + '"'
    return text


def _unescape_double_quoted(value: str) -> str:
    result: list[str] = []
    index = 0
    while index < len(value):
        char = value[index]
        if char == "\\" and index + 1 < len(value):
            next_char = value[index + 1]
            if next_char in {'"', "\\"}:
                result.append(next_char)
                index += 2
                continue
        result.append(char)
        index += 1
    return "".join(result)


def load_config(path: Path) -> dict[str, Any]:
    """Parse a YAML-like config file without frontmatter delimiters."""
    if not path.exists():
        return {}
    lines = path.read_text(encoding="utf-8").splitlines()
    return _parse_mapping(lines)
