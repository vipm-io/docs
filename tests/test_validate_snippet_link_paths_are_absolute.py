"""Enforce that hand-authored snippets use absolute paths for cross-page links.

Snippets in ``docs/.snippets/`` are included from pages at various depths.
A relative path like ``../foo.md`` only resolves correctly from one specific
depth and silently breaks when the same snippet is included from elsewhere.
Absolute paths from docs root (leading ``/``) work universally.

This test acts as the enforcement mechanism for the convention: if a snippet
introduces a relative cross-page link, ``just check`` (and CI) will fail.

Excluded from the check:
  - ``_generated/`` subdir — those snippets are written by ``generate_cli_snippets.py``
    from the consuming page's perspective and are intentionally relative.
  - External links (``http://``, ``https://``, ``mailto:``, ``tel:``).
  - Pure anchor links (``#fragment``).
  - Non-Markdown destinations (images, CSS, etc.).
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SNIPPETS_DIR = REPO_ROOT / "docs" / ".snippets"
MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def _is_cross_page_md_link(href: str) -> bool:
    """Return True if ``href`` targets another Markdown page in this site."""
    if not href:
        return False
    if href.startswith(("http://", "https://", "mailto:", "tel:", "#")):
        return False
    base = href.split("#", 1)[0]
    return base.endswith(".md")


def _collect_violations(snippets_dir: Path) -> list[str]:
    """Return a list of `path: link` strings for any relative cross-page link
    found in hand-authored snippets at the top level of ``snippets_dir``.

    Top-level glob only; subdirs (notably ``_generated/``) are skipped.
    """
    violations: list[str] = []
    for snippet in sorted(snippets_dir.glob("*.md")):
        text = snippet.read_text(encoding="utf-8")
        for match in MD_LINK_RE.finditer(text):
            href = match.group(1).split(None, 1)[0]
            if not _is_cross_page_md_link(href):
                continue
            if not href.startswith("/"):
                try:
                    location = snippet.relative_to(REPO_ROOT)
                except ValueError:
                    location = snippet
                violations.append(f"{location}: `{href}`")
    return violations


# --- enforcement against the actual repo --------------------------------


def test_real_snippets_use_absolute_paths() -> None:
    violations = _collect_violations(SNIPPETS_DIR)
    assert not violations, (
        "Cross-page links in hand-authored snippets must use absolute paths "
        "from docs root (leading `/`) so they work from any include depth:\n  "
        + "\n  ".join(violations)
    )


# --- self-tests for the check logic -------------------------------------


def test_collect_violations_passes_on_absolute_paths(tmp_path: Path) -> None:
    (tmp_path / "a.md").write_text(
        "See [Compatibility](/cli/labview-interop.md) for details.\n"
        "Also [Support](/support.md#contact).\n"
    )
    assert _collect_violations(tmp_path) == []


def test_collect_violations_catches_relative_paths(tmp_path: Path) -> None:
    (tmp_path / "a.md").write_text("See [Compatibility](../cli/labview-interop.md).\n")
    violations = _collect_violations(tmp_path)
    assert len(violations) == 1
    assert "a.md" in violations[0]
    assert "../cli/labview-interop.md" in violations[0]


def test_collect_violations_exempts_external_links(tmp_path: Path) -> None:
    (tmp_path / "a.md").write_text(
        "Visit [GitHub](https://github.com/vipm-io/docs/issues).\n"
        "Mail [us](mailto:support@vipm.io).\n"
    )
    assert _collect_violations(tmp_path) == []


def test_collect_violations_exempts_anchors(tmp_path: Path) -> None:
    (tmp_path / "a.md").write_text("Jump to [the section](#install-or-select).\n")
    assert _collect_violations(tmp_path) == []


def test_collect_violations_exempts_non_md_targets(tmp_path: Path) -> None:
    (tmp_path / "a.md").write_text("![logo](../assets/logo.png)\n")
    assert _collect_violations(tmp_path) == []


def test_collect_violations_does_not_descend_into_subdirs(tmp_path: Path) -> None:
    nested = tmp_path / "_generated"
    nested.mkdir()
    (nested / "info.md").write_text("See [other](../some-page.md).\n")
    assert _collect_violations(tmp_path) == []


def test_collect_violations_reports_each_relative_link(tmp_path: Path) -> None:
    (tmp_path / "a.md").write_text("See [A](../a.md) and [B](b.md) and [C](/ok.md).\n")
    violations = _collect_violations(tmp_path)
    assert len(violations) == 2
    joined = "\n".join(violations)
    assert "../a.md" in joined
    assert "b.md" in joined
    assert "/ok.md" not in joined
