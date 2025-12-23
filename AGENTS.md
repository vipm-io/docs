# Project Agent Guide

## Purpose

This file captures key practices and project context so future agents can ramp up quickly when working on the VIPM documentation repo.

## Current Focus Areas

- **CLI docs modernization** lives in `dev-docs/cli-docs-improvement-proposal.md`. Treat that document as the source of truth for plan, decisions, and progress logs. Update it whenever you touch `docs/cli/`.
- The CLI content currently spans `docs/cli/index.md`, `docs/cli/docker.md`, and `docs/cli/github-actions.md`. We are incrementally restructuring toward the proposal’s multi-phase plan.

## Working Expectations

1. **Plan before editing**
   - Update the tracker tables in the proposal doc to reflect in-progress work.
   - Use the `manage_todo_list` tool to track multi-step tasks during a session.
2. **Editing conventions**
   - Default to ASCII; add concise comments only when the intent isn’t obvious.
   - Reuse the established “Expected output” format when documenting CLI commands.
   - Add cross-links between related docs to improve navigation.
3. **Verification**
   - Run `uv run mkdocs build` after meaningful documentation changes. Fix warnings immediately (e.g., relative links).
4. **Communication**
   - Summarize changes clearly, referencing file paths (e.g., `docs/cli/index.md`).
   - Call out next logical steps (tests to run, docs to draft) so the user can steer the work.

## Useful References

- **Build command**: `uv run mkdocs build`
- **Active plan**: `dev-docs/cli-docs-improvement-proposal.md`
- **Key folders**: `docs/cli/`, `docs/index.md`, `dev-docs/`
- **VIPM CLI help**: Run `vipm help` for the global summary and `vipm <command> --help` to grab authoritative syntax/options for each command

## Lessons Learned

- Small navigational improvements (cross-links, consistent headings) already deliver value—iterate incrementally.
- MkDocs warnings often point to broken relative links; they’re quick wins worth fixing immediately.
- Keep the proposal’s progress log up to date so future contributors know what’s done and what’s next.
