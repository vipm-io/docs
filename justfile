# This file contains useful commands for development tasks.

list:
    @just --list

# regenerate generated source snippets (release-notes table)
prebuild:
    uv run python scripts/generate_release_notes_table.py

# build and serve locally (auto-finds open port starting at 8000)
dev: prebuild
    #!/usr/bin/env bash
    port=8000
    while ss -tlnp | grep -q ":$port "; do
        port=$((port + 1))
    done
    echo "Serving on http://localhost:$port"
    uv run zensical serve --dev-addr "localhost:$port"

# format Python code with ruff
format:
    uv run ruff format

# lint Python code with ruff (reports only; does not modify files)
lint:
    uv run ruff check

# no-fix check used before pushing: format check + lint + tests
check:
    uv run ruff format --check
    uv run ruff check
    uv run pytest

# run unit tests for scripts and validators
test:
    uv run pytest

# build the documentation site with pre- and post-build validation
build:
    uv run python scripts/build_docs.py
