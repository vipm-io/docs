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

# build the documentation site
build: prebuild
    uv run zensical build
