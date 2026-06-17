#!/usr/bin/env python3
"""Validate prebuild outputs before `zensical build` runs.

Runs after `scripts/generate_release_notes_table.py` in CI workflows
(`.github/workflows/ci.yml`, `preview.yml`) to catch regressions the
generator's internal checks don't surface:

  1. Generated snippet files exist where `pymdownx.snippets` expects
     them (stronger than `check_paths: true`'s file-exists test, since
     we also verify content shape).
  2. Each generated snippet has the expected shape - for the release-
     notes table, at least one data row; for the CLI exit-codes table,
     named exit-code rows. Catches output-format drift if a generator
     is refactored.

All checks run; every failure is reported in one CI log so authors see
the full picture. Extend ``CHECKS`` when new prebuild artifacts land.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

RELEASE_NOTES_TABLE = REPO_ROOT / "docs" / ".snippets" / "release-notes-table.md"
RELEASE_NOTES_ROW_RE = re.compile(r"^\| <a href", re.MULTILINE)
EXIT_CODES_TABLE = REPO_ROOT / "docs" / ".snippets" / "_generated" / "exit-codes.md"
EXIT_CODES_HEADER_RE = re.compile(r"^\| Exit Code \| Meaning \|$", re.MULTILINE)
EXIT_CODE_NAME_ROW_RE = re.compile(r"^\| `\d+` `[A-Z0-9_]+` \|", re.MULTILINE)


def _check_release_notes_table() -> str | None:
    rel = RELEASE_NOTES_TABLE.relative_to(REPO_ROOT)
    if not RELEASE_NOTES_TABLE.is_file():
        return (
            f"missing: {rel} — run `scripts/generate_release_notes_table.py` "
            f"(or `just prebuild`) before building."
        )
    content = RELEASE_NOTES_TABLE.read_text()
    if not RELEASE_NOTES_ROW_RE.search(content):
        return (
            f"empty: {rel} has no data rows (no lines matching `^| <a href`). "
            f"The generator may have found no `docs/release-notes/*.md` files, "
            f"or the output format has drifted."
        )
    return None


def _check_exit_codes_table() -> str | None:
    rel = EXIT_CODES_TABLE.relative_to(REPO_ROOT)
    if not EXIT_CODES_TABLE.is_file():
        return (
            f"missing: {rel} - run `scripts/generate_cli_snippets.py` "
            f"(or `just prebuild`) before building."
        )
    content = EXIT_CODES_TABLE.read_text()
    if not EXIT_CODES_HEADER_RE.search(content):
        return f"malformed: {rel} is missing the `Exit Code | Meaning` header."
    if not EXIT_CODE_NAME_ROW_RE.search(content):
        return (
            f"empty: {rel} has no named exit-code rows. The CLI JSON may be "
            f"missing `exit_codes[].name`, or the output format has drifted."
        )
    return None


CHECKS = [_check_release_notes_table, _check_exit_codes_table]


def main() -> int:
    errors = [msg for check in CHECKS if (msg := check()) is not None]
    for msg in errors:
        print(f"error: {msg}", file=sys.stderr)
    if errors:
        return 1
    print(f"ok: validated {len(CHECKS)} check(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
