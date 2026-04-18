"""Tests for pre- and post-build validators.

Covers the failure modes surfaced by PR #77 review, ensuring each
validator rejects the broken pattern and accepts the correct one with
synthetic HTML inputs — independent of what the live generator happens
to produce today.
"""

from __future__ import annotations

from pathlib import Path

import build_docs
import validate_docs_build


# --- validate_docs_build._check_release_notes_table ---------------------


def test_pre_build_missing_snippet(tmp_path, monkeypatch):
    monkeypatch.setattr(validate_docs_build, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(
        validate_docs_build, "RELEASE_NOTES_TABLE", tmp_path / "absent.md"
    )

    result = validate_docs_build._check_release_notes_table()

    assert result is not None
    assert "missing:" in result
    assert "absent.md" in result


def test_pre_build_empty_snippet(tmp_path, monkeypatch):
    snippet = tmp_path / "release-notes-table.md"
    snippet.write_text("| Release | Summary |\n| --- | --- |\n")
    monkeypatch.setattr(validate_docs_build, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(validate_docs_build, "RELEASE_NOTES_TABLE", snippet)

    result = validate_docs_build._check_release_notes_table()

    assert result is not None
    assert "empty:" in result


def test_pre_build_snippet_with_rows_ok(tmp_path, monkeypatch):
    snippet = tmp_path / "release-notes-table.md"
    snippet.write_text(
        "| Release | Summary |\n| --- | --- |\n"
        '| <a href="../release-notes/2026.3/">x</a> | bar |\n'
    )
    monkeypatch.setattr(validate_docs_build, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(validate_docs_build, "RELEASE_NOTES_TABLE", snippet)

    assert validate_docs_build._check_release_notes_table() is None


# --- build_docs._post_release_notes_table_rendered ----------------------


def _write_html(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body)


def _point_release_notes_at(monkeypatch, tmp_path: Path, html_path: Path) -> None:
    monkeypatch.setattr(build_docs, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(build_docs, "SITE_DIR", tmp_path / "site")
    monkeypatch.setattr(build_docs, "RELEASE_NOTES_INDEX", html_path)


def test_post_release_notes_missing_file(tmp_path, monkeypatch):
    html_path = tmp_path / "site" / "release-notes" / "index.html"
    _point_release_notes_at(monkeypatch, tmp_path, html_path)

    result = build_docs._post_release_notes_table_rendered()

    assert result is not None
    assert "missing rendered page" in result


def test_post_release_notes_no_table_tag(tmp_path, monkeypatch):
    html_path = tmp_path / "site" / "release-notes" / "index.html"
    _write_html(html_path, "<html><body><h1>Release Notes</h1></body></html>")
    _point_release_notes_at(monkeypatch, tmp_path, html_path)

    result = build_docs._post_release_notes_table_rendered()

    assert result is not None
    assert "no <table>" in result


def test_post_release_notes_wrong_href_form_fails(tmp_path, monkeypatch):
    # Regression guard for PR #77 P1: a stray `../<slug>/` (no
    # `release-notes/` segment) would render broken links.
    html_path = tmp_path / "site" / "release-notes" / "index.html"
    _write_html(
        html_path,
        '<table><tr><td><a href="../2026.3/">x</a></td></tr></table>',
    )
    _point_release_notes_at(monkeypatch, tmp_path, html_path)

    result = build_docs._post_release_notes_table_rendered()

    assert result is not None
    assert "expected `../release-notes/<slug>/` form" in result


def test_post_release_notes_correct_form_ok(tmp_path, monkeypatch):
    html_path = tmp_path / "site" / "release-notes" / "index.html"
    _write_html(
        html_path,
        '<table><tr><td><a href="../release-notes/2026.3/">x</a></td></tr></table>',
    )
    _point_release_notes_at(monkeypatch, tmp_path, html_path)

    assert build_docs._post_release_notes_table_rendered() is None


# --- build_docs._post_report_a_problem_redirect -------------------------


def _point_report_at(monkeypatch, tmp_path: Path, html_path: Path) -> None:
    monkeypatch.setattr(build_docs, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(build_docs, "REPORT_A_PROBLEM_INDEX", html_path)


def test_post_report_a_problem_missing_file(tmp_path, monkeypatch):
    html_path = tmp_path / "site" / "report-a-problem" / "index.html"
    _point_report_at(monkeypatch, tmp_path, html_path)

    result = build_docs._post_report_a_problem_redirect()

    assert result is not None
    assert "missing rendered page" in result


def test_post_report_a_problem_wrong_url_fails(tmp_path, monkeypatch):
    # Regression guard for PR #77 P2: bare `url=support/` would
    # resolve from `/report-a-problem/` to `/report-a-problem/support/`.
    html_path = tmp_path / "site" / "report-a-problem" / "index.html"
    _write_html(
        html_path, '<meta http-equiv="refresh" content="0; url=support/">'
    )
    _point_report_at(monkeypatch, tmp_path, html_path)

    result = build_docs._post_report_a_problem_redirect()

    assert result is not None
    assert "`../support/`" in result


def test_post_report_a_problem_correct_form_ok(tmp_path, monkeypatch):
    html_path = tmp_path / "site" / "report-a-problem" / "index.html"
    _write_html(
        html_path, '<meta http-equiv="refresh" content="0; url=../support/">'
    )
    _point_report_at(monkeypatch, tmp_path, html_path)

    assert build_docs._post_report_a_problem_redirect() is None


def test_post_report_a_problem_missing_refresh_fails(tmp_path, monkeypatch):
    html_path = tmp_path / "site" / "report-a-problem" / "index.html"
    _write_html(html_path, "<html><body>no redirect</body></html>")
    _point_report_at(monkeypatch, tmp_path, html_path)

    result = build_docs._post_report_a_problem_redirect()

    assert result is not None
