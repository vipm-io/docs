"""Tests for generated CLI markdown snippets."""

from __future__ import annotations

import generate_cli_snippets


def test_render_exit_codes_snippet_includes_name_column() -> None:
    snippet = generate_cli_snippets.render_exit_codes_snippet(
        [
            {
                "code": 0,
                "name": "SUCCESS",
                "description": "Operation completed successfully",
            },
            {
                "code": 2,
                "name": "COMMAND_SYNTAX_ERROR",
                "description": "Invalid arguments | failed input validation\nretry",
            },
        ]
    )

    assert '<div class="cli-options cli-exit-codes" markdown>' in snippet
    assert "| Exit Code | Meaning |" in snippet
    assert "| `0` `SUCCESS` | Operation completed successfully |" in snippet
    assert (
        "| `2` `COMMAND_SYNTAX_ERROR` | Invalid arguments \\| "
        "failed input validation retry |"
    ) in snippet
