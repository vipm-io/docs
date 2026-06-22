# This file contains useful commands for development tasks.

# run recipe lines in bash on every platform
set shell := ["bash", "-cu"]

list:
    @just --list

# regenerate generated source snippets
prebuild:
    uv run python scripts/generate_release_notes_table.py
    uv run python scripts/generate_cli_snippets.py

# build and serve locally (auto-finds open port starting at 8000)
dev: prebuild
    uv run python scripts/dev_serve.py

# format Python code with ruff
format:
    uv run ruff format

# lint Python code with ruff (reports only; does not modify files)
lint:
    uv run ruff check

# verify pyproject.toml and uv.lock are in sync
lock:
    uv lock --check

# run static type checks
typecheck:
    uv run pyrefly check .

# lint and audit GitHub Actions workflows
workflow-check:
    uv run actionlint
    uv run zizmor --offline .github/workflows

# no-fix check used before pushing: lockfile, format, lint, types, workflow checks, tests
check:
    uv lock --check
    uv run ruff format --check
    uv run ruff check
    uv run pyrefly check .
    uv run actionlint
    uv run zizmor --offline .github/workflows
    uv run pytest

# run unit tests for scripts and validators
test:
    uv run pytest

# build the documentation site with pre- and post-build validation
build:
    uv run python scripts/build_docs.py
