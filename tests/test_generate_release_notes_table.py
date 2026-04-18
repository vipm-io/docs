"""Tests for scripts/generate_release_notes_table.py.

Guards the invariants surfaced in the PR #77 review:
  - sort order deterministic even with non-conforming filenames
  - missing frontmatter warns loudly rather than silently emitting a
    slug-as-title row
  - empty release-notes dir hard-fails rather than writing a header-
    only table and exiting 0
  - generated link format is the `../release-notes/<slug>/` form that
    renders to working URLs after Zensical's snippet-include rewriting
    (a bare `{slug}/` or `../{slug}/` form would 404)
"""

from __future__ import annotations

from pathlib import Path

import generate_release_notes_table as gen


# --- pure helpers ---------------------------------------------------------


def test_version_sort_key_numeric():
    assert gen._version_sort_key("2026.3.md") == ((2026, 3), "2026.3")
    assert gen._version_sort_key("2025.3.1.md") == ((2025, 3, 1), "2025.3.1")


def test_version_sort_key_non_numeric_warns_and_tiebreaks(capsys):
    key = gen._version_sort_key("draft.md")
    captured = capsys.readouterr()
    assert "non-numeric version part" in captured.err
    assert key == ((0,), "draft")


def test_version_sort_is_stable_and_numeric_wins(capsys):
    files = ["draft.md", "other-weird.md", "2026.3.md", "2025.3.1.md"]
    ordered_a = sorted(files, key=gen._version_sort_key, reverse=True)
    ordered_b = sorted(files, key=gen._version_sort_key, reverse=True)
    assert ordered_a == ordered_b
    assert ordered_a[0] == "2026.3.md"
    assert ordered_a[1] == "2025.3.1.md"


def test_parse_frontmatter_present(tmp_path: Path):
    p = tmp_path / "x.md"
    p.write_text("---\ntitle: T\ndescription: D\n---\ncontent")
    assert gen._parse_frontmatter(p) == {"title": "T", "description": "D"}


def test_parse_frontmatter_absent_returns_empty(tmp_path: Path):
    p = tmp_path / "x.md"
    p.write_text("no frontmatter block at all")
    assert gen._parse_frontmatter(p) == {}


def test_parse_frontmatter_empty_block_returns_empty(tmp_path: Path):
    p = tmp_path / "x.md"
    p.write_text("---\n---\ncontent")
    assert gen._parse_frontmatter(p) == {}


# --- main() integration ---------------------------------------------------


def _setup_fixture(tmp_path: Path, files: dict[str, str]) -> tuple[Path, Path]:
    rn_dir = tmp_path / "docs" / "release-notes"
    rn_dir.mkdir(parents=True)
    (rn_dir / "index.md").write_text("# Overview")
    for name, body in files.items():
        (rn_dir / name).write_text(body)
    output = tmp_path / "docs" / ".snippets" / "release-notes-table.md"
    return rn_dir, output


def _point_at(monkeypatch, tmp_path: Path, rn_dir: Path, output: Path) -> None:
    monkeypatch.setattr(gen, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(gen, "RELEASE_NOTES_DIR", rn_dir)
    monkeypatch.setattr(gen, "OUTPUT", output)


def test_main_empty_dir_hard_fails(tmp_path, monkeypatch, capsys):
    rn_dir, output = _setup_fixture(tmp_path, {})
    _point_at(monkeypatch, tmp_path, rn_dir, output)

    rc = gen.main()

    assert rc == 1
    assert "no release-notes files found" in capsys.readouterr().err
    assert not output.exists(), "snippet must NOT be written on failure"


def test_main_generates_expected_href_format(tmp_path, monkeypatch):
    # Regression guard for PR #77 P1: the link must be the full
    # `../release-notes/<slug>/` form. A bare `<slug>/` or `../<slug>/`
    # renders to `/{slug}/` after Zensical's snippet-include rewriting
    # (top-level, 404).
    rn_dir, output = _setup_fixture(
        tmp_path,
        {
            "2026.3.md": "---\ntitle: VIPM 2026 Q3\ndescription: Latest\n---\n",
            "2025.3.md": "---\ntitle: VIPM 2025 Q3\ndescription: Older\n---\n",
        },
    )
    _point_at(monkeypatch, tmp_path, rn_dir, output)

    rc = gen.main()

    assert rc == 0
    content = output.read_text()
    assert '<a href="../release-notes/2026.3/"' in content
    assert '<a href="../release-notes/2025.3/"' in content
    # Explicitly assert the broken forms are NOT emitted.
    assert '<a href="../2026.3/"' not in content
    assert '<a href="2026.3/"' not in content


def test_main_warns_on_missing_frontmatter(tmp_path, monkeypatch, capsys):
    rn_dir, output = _setup_fixture(
        tmp_path,
        {
            "2026.3.md": "no frontmatter at all",
            "2025.3.md": "---\ntitle: OK\ndescription: OK\n---\n",
        },
    )
    _point_at(monkeypatch, tmp_path, rn_dir, output)

    rc = gen.main()

    assert rc == 0  # warn-only, not fail
    err = capsys.readouterr().err
    assert "2026.3.md is missing frontmatter" in err
    assert "title" in err and "description" in err


def test_main_warns_on_non_numeric_filename_but_keeps_numeric_first(
    tmp_path, monkeypatch, capsys
):
    rn_dir, output = _setup_fixture(
        tmp_path,
        {
            "draft.md": "---\ntitle: D\ndescription: d\n---\n",
            "2026.3.md": "---\ntitle: T\ndescription: t\n---\n",
        },
    )
    _point_at(monkeypatch, tmp_path, rn_dir, output)

    rc = gen.main()

    assert rc == 0
    err = capsys.readouterr().err
    assert "non-numeric version part" in err
    content = output.read_text()
    # Numeric version sorts above non-numeric (reverse=True, (2026,3) > (0,)).
    assert content.index("2026.3") < content.index("draft")


def test_main_output_header_shape(tmp_path, monkeypatch):
    rn_dir, output = _setup_fixture(
        tmp_path,
        {"2026.3.md": "---\ntitle: T\ndescription: d\n---\n"},
    )
    _point_at(monkeypatch, tmp_path, rn_dir, output)

    assert gen.main() == 0
    content = output.read_text()
    assert content.startswith("<!-- Auto-generated")
    assert "| Release | Summary |" in content
    assert "| --- | --- |" in content
