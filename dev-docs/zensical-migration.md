# Zensical Migration

Documents decisions made during the Material for MkDocs → Zensical migration (issue #76).

## Why

Material for MkDocs entered maintenance mode on 2025-11-06; its maintainers shifted focus to Zensical, a purpose-built successor from the same team. Staying on Material indefinitely left us downstream of a feature-frozen toolchain and exposed to MkDocs 2.0 (explicitly incompatible with Material). Zensical reads `mkdocs.yml` and the same content/extensions with minimal changes, so it is the forward path rather than a fork like ProperDocs.

## What changed

- `pyproject.toml` — replaced `mkdocs-material` and `mkdocs-redirects` with `zensical`. `mike` is retained but now pulled from the Zensical-compatible fork at `git+https://github.com/squidfunk/mike.git` (the fork's maintainers chose not to publish to PyPI; see <https://zensical.org/docs/setup/versioning/>).
- `justfile` / GitHub workflows — `mkdocs build`/`serve` → `zensical build`/`serve`, preceded by a prebuild step that regenerates the release-notes table snippet (see below).
- `.github/workflows/ci.yml` — retained the pre-migration mike-based deploy pipeline verbatim; only the build commands change. `--strict` was dropped from the build step because Zensical 0.0.x lists it as unsupported.
- `mkdocs.yml` — removed the `plugins.redirects` block and the top-level `hooks:` reference. The `extra.version` (mike) block stays. The `copyright:` line is now static (bump the year annually).
- `hooks.py` removed. Zensical has no native hook API yet, and its mike fork invokes `zensical build` as a subprocess (see `mike/utils.py`), so a Python-level runtime shim around `zensical.markdown.render` would not fire during `mike deploy`.
- `scripts/generate_release_notes_table.py` — the release-notes table is now generated at the source level by a prebuild script that writes `docs/.snippets/release-notes-table.md`. `docs/release-notes/index.md` pulls the snippet in via the existing pymdownx.snippets extension. This mirrors the output of the previous `hooks.py:on_page_markdown` and works with both direct `zensical build` and `mike deploy`.
- `scripts/validate_docs_build.py` + `scripts/build_docs.py` — pre-build validation (snippet exists, shape correct) and an end-to-end build orchestrator (generate → validate-pre → `zensical build` → validate-post) used by `just build`, `ci.yml`'s build job, and `preview.yml`. Post-build checks guard rendered-output markers the migration is sensitive to (release-notes `<table>` present, `/report-a-problem/` meta-refresh intact). The mike-deploy job keeps its discrete pre-build steps because mike invokes `zensical build` itself as a subprocess.
- `docs/.snippets/release-notes-table.md` — gitignored; produced by the prebuild.
- `docs/report-a-problem.md` — replaces the `mkdocs-redirects` redirect mapping with a meta-refresh page pointing at `../support/`. The `../` prefix is required because Zensical does not rewrite relative URLs inside raw HTML (only inside markdown links); a bare `url=support/` from `/report-a-problem/` would resolve to `/report-a-problem/support/` and 404.

## Accepted regressions

1. **No `--strict` guard in CI.** Zensical 0.0.x flags `--strict` as "currently unsupported" and exits 0 even when individual pages hit render errors (e.g., a `SnippetMissingError` skips the page but the CLI reports success). `scripts/build_docs.py` mitigates this by capturing zensical's output and failing the build if any `Error:` line is logged. Replace the wrapper with `zensical build --strict` once upstream ships it.
2. **`/report-a-problem` is a redirect page, not a plugin-generated redirect.** Bookmarks to `/report-a-problem/` still land on Support, via meta-refresh rather than server-side.
3. **Static `copyright:` year.** The old `hooks.py:on_config` auto-bumped the year; now we set it once in `mkdocs.yml` and bump manually each January. Low effort, very visible if missed.
4. **`mike` is a git dependency on a 3rd-party fork**. Lock captures a specific commit; refresh with `uv lock --upgrade-package mike`. This is a bridge until Zensical ships native versioning (tracked on the Zensical roadmap).

## Follow-ups

- Replace the prebuild script with Zensical-native extension hooks once its module system ships (<https://zensical.org/about/roadmap/>).
- Track Zensical releases for `--strict` support; re-enable the guard when available.
- Drop the mike git dependency in favor of Zensical-native versioning once it ships.
