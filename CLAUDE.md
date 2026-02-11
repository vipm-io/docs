# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Documentation site for [docs.vipm.io](https://docs.vipm.io), built with **MkDocs Material** and managed with **uv** (Python package manager).

## Commands

- `just dev` — Local dev server with live reload (auto-finds open port starting at 8000)
- `just build` — Build the site (alias for `uv run mkdocs build`)
- `uv run mkdocs build --strict` — Build with strict mode (used in CI, fails on warnings)

Always run `uv run mkdocs build` after documentation changes and fix any warnings immediately.

## Architecture

- `mkdocs.yml` — Site configuration: nav structure, theme, plugins, markdown extensions, social links
- `docs/` — All documentation content (Markdown files, assets)
- `docs/.snippets/` — Reusable Markdown snippets included via `pymdownx.snippets` extension
- `overrides/` — MkDocs Material theme overrides (custom icons in `.icons/custom/`)
- `hooks.py` — MkDocs build hooks (currently sets dynamic copyright year)
- `dev-docs/` — Internal planning documents, not published to the site

## Key Conventions

- Navigation is explicitly defined in `mkdocs.yml` under `nav:` — new pages must be added there to appear on the site
- Snippets use `--8<--` syntax and resolve from `docs/.snippets/`
- The header logo links to `vipm.io` (not the docs root) via `extra.homepage`
- CI builds with `--strict` flag, so warnings that pass locally will fail in CI
- The site auto-deploys to GitHub Pages on push to `main` via `mkdocs gh-deploy`

## Commit and PR Rules

Never include mentions of Claude, AI, or "generated with" in commit messages, PR titles, PR descriptions, or any other git metadata. No co-authored-by lines referencing Claude. No "🤖 Generated with Claude Code" footers. Commits and PRs should read as if written by a human developer.

## CLI Docs Modernization

Active improvement effort tracked in `dev-docs/cli-docs-improvement-proposal.md`. That document is the source of truth for CLI documentation plans, decisions, and progress. Update it when modifying `docs/cli/` content.
