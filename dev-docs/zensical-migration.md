# Zensical Migration

Documents decisions made during the Material for MkDocs → Zensical migration (issue #76).

## Why

Material for MkDocs entered maintenance mode on 2025-11-06; its maintainers shifted focus to Zensical, a purpose-built successor from the same team. Staying on Material indefinitely left us downstream of a feature-frozen toolchain and exposed to MkDocs 2.0 (explicitly incompatible with Material). Zensical reads `mkdocs.yml` and the same content/extensions with minimal changes, so it is the forward path rather than a fork like ProperDocs.

## What changed

- `pyproject.toml` — replaced `mkdocs-material`, `mkdocs-redirects`, and `mike` with `zensical`.
- `justfile` — `mkdocs build`/`serve` → `python zensical_hooks.py build`/`serve` (see shim note below).
- `.github/workflows/ci.yml` — dropped `--strict` (Zensical 0.0.33 lists it as unsupported); replaced the `mike deploy` pipeline with `peaceiris/actions-gh-pages` using `keep_files: true`.
- `mkdocs.yml` — removed the `plugins.redirects` block, the `extra.version` (mike) block, and the top-level `hooks:` reference. The `copyright:` line is no longer set here; the shim sets it with the current year on every build.
- `hooks.py` → `zensical_hooks.py` — Zensical has no native hook API yet (module system is on the roadmap but unshipped). The new file monkey-patches `zensical.config.parse_config` and `zensical.markdown.render` before delegating to the Zensical CLI, restoring the two hooks we rely on (dynamic copyright year, release-notes table generation). Pattern adapted from a community gist; not endorsed by the Zensical team. Build commands invoke `python zensical_hooks.py build` instead of `zensical build`.
- `docs/report-a-problem.md` — replaces the `mkdocs-redirects` redirect mapping with a meta-refresh page pointing at `support/`.

## Accepted regressions

1. **No per-release versioning.** `mike` was dropped; `docs.vipm.io` now ships a single "latest" version at root. Legacy `/latest/`, `/preview/`, `/2026.3/`, … subdirectories remain served from `gh-pages` (via `keep_files: true`) but are no longer updated, and there is no version selector UI. Revisit if Zensical grows a versioning plugin.
2. **No `--strict` guard in CI.** Zensical 0.0.33 flags `--strict` as "currently unsupported". CI builds no longer fail on warnings. Revisit when upstream adds support.
3. **`/report-a-problem` is a redirect page, not a plugin-generated redirect.** Bookmarks to `/report-a-problem/` still land on Support, via meta-refresh rather than server-side.
4. **`zensical_hooks.py` relies on Zensical internals.** Each Zensical upgrade may break the shim (monkey-patches `parse_config` and `render`). When it does, re-adapt against the new entry points, or fall back to hand-maintaining the affected surfaces (release-notes table, copyright line).

## Follow-ups

- Remove the `keep_files: true` deploy option and prune stale `gh-pages` subdirectories after confirming no inbound traffic to legacy version paths.
- Replace the shim with Zensical's module system once it ships (https://zensical.org/about/roadmap/#module-system).
- Track Zensical releases for `--strict` support and a versioning story.
