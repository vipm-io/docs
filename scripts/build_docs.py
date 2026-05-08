#!/usr/bin/env python3
"""Orchestrate the Zensical docs build with pre- and post-build validation.

Single entrypoint for `just build` and CI. Runs five stages in sequence:

  1. ``scripts/generate_release_notes_table.py`` — regenerate the
     gitignored release-notes table snippet.
  2. ``scripts/generate_cli_snippets.py`` — regenerate the gitignored
     per-command and global-options snippets from
     ``data/vipm-public-cli.json``.
  3. ``scripts/validate_docs_build.py`` — check that the generator's
     outputs are present and shaped as expected.
  4. ``zensical build`` — render the site to ``site/``.
  5. Post-build checks against rendered HTML — guard against regressions
     introduced by the MkDocs→Zensical migration (see
     ``dev-docs/zensical-migration.md``): the release-notes index page
     actually contains the generated table, and the `/report-a-problem/`
     page still emits the meta-refresh redirect that the removed
     `mkdocs-redirects` plugin used to provide.

Any stage failing exits non-zero so the CI log points at the regression
source. The mike-deploy workflow in ``.github/workflows/ci.yml`` does
NOT call this script; mike invokes `zensical build` itself as a
subprocess, so that workflow keeps its discrete generate + validate-pre
steps.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
SITE_DIR = REPO_ROOT / "site"

RELEASE_NOTES_INDEX = SITE_DIR / "release-notes" / "index.html"
REPORT_A_PROBLEM_INDEX = SITE_DIR / "report-a-problem" / "index.html"


def _post_release_notes_table_rendered() -> str | None:
    if not RELEASE_NOTES_INDEX.is_file():
        return f"missing rendered page: {RELEASE_NOTES_INDEX.relative_to(REPO_ROOT)}"
    html = RELEASE_NOTES_INDEX.read_text()
    if "<table>" not in html:
        return (
            f"{RELEASE_NOTES_INDEX.relative_to(REPO_ROOT)} has no <table> — "
            f"the release-notes snippet did not render. Check the "
            f"pymdownx.snippets include in docs/release-notes/index.md."
        )
    # Confirm at least one row links back into a release subpage in the
    # expected `../release-notes/<slug>/` form. This specific pattern
    # resolves to `/release-notes/<slug>/` from the un-versioned index
    # page and to `/<version>/release-notes/<slug>/` from a mike-versioned
    # one. A bare `<slug>/` href (what the generator emits literally) gets
    # rewritten by Zensical to `../<slug>/`, which routes to `/<slug>/`
    # (top-level, 404), so we reject any non-`../release-notes/` form.
    if not re.search(r'<a href="\.\./release-notes/[^/"]+/"', html):
        return (
            f"{RELEASE_NOTES_INDEX.relative_to(REPO_ROOT)} table has no row "
            f"links in the expected `../release-notes/<slug>/` form — the "
            f"generated snippet may be header-only, or Zensical's URL "
            f"rewriting changed and the links now 404."
        )
    return None


def _post_report_a_problem_redirect() -> str | None:
    if not REPORT_A_PROBLEM_INDEX.is_file():
        return f"missing rendered page: {REPORT_A_PROBLEM_INDEX.relative_to(REPO_ROOT)}"
    html = REPORT_A_PROBLEM_INDEX.read_text()
    # Require the full `url=../support/` form. A bare `url=support/`
    # resolves from `/report-a-problem/` to `/report-a-problem/support/`
    # (404); raw HTML meta tags aren't URL-rewritten by Zensical the way
    # markdown links are, so the source has to spell the correct relative
    # path explicitly. See P2 in the PR review history.
    if 'http-equiv="refresh"' not in html or "url=../support/" not in html:
        return (
            f"{REPORT_A_PROBLEM_INDEX.relative_to(REPO_ROOT)} is missing the "
            f"meta-refresh redirect to `../support/`. This was previously "
            f"provided by the removed mkdocs-redirects plugin; it is now "
            f"inline in docs/report-a-problem.md."
        )
    return None


POST_BUILD_CHECKS = [
    _post_release_notes_table_rendered,
    _post_report_a_problem_redirect,
]


def _run(argv: list[str]) -> None:
    print(f"→ {' '.join(argv)}", file=sys.stderr)
    subprocess.run(argv, check=True)


def _run_zensical_build() -> int | None:
    # Zensical 0.0.x exits 0 even when individual pages hit render errors
    # (e.g., a SnippetMissingError skips the page but the CLI succeeds).
    # Capture output and fail explicitly on any `Error:` line. Replace
    # this wrapper with `zensical build --strict` once upstream ships it.
    argv = ["zensical", "build"]
    print(f"→ {' '.join(argv)}", file=sys.stderr)
    result = subprocess.run(argv, capture_output=True, text=True)
    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)
    if result.returncode != 0:
        return result.returncode
    if re.search(r"^Error:", result.stdout + result.stderr, re.MULTILINE):
        print(
            "error: zensical logged page render errors. Zensical 0.0.x exits 0 "
            "on per-page errors; see output above for the specific failure.",
            file=sys.stderr,
        )
        return 1
    return None


def main() -> int:
    _run([sys.executable, str(SCRIPTS_DIR / "generate_release_notes_table.py")])
    _run([sys.executable, str(SCRIPTS_DIR / "generate_cli_snippets.py")])
    _run([sys.executable, str(SCRIPTS_DIR / "validate_docs_build.py")])

    rc = _run_zensical_build()
    if rc is not None:
        return rc

    errors = [msg for check in POST_BUILD_CHECKS if (msg := check()) is not None]
    for msg in errors:
        print(f"error: {msg}", file=sys.stderr)
    if errors:
        return 1
    print(f"ok: built and validated ({len(POST_BUILD_CHECKS)} post-build check(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
