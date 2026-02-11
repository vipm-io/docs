# This file contains useful commands for development tasks.

list:
    @just --list

# build and serve locally, with live reload (auto-finds open port starting at 8000)
dev:
    #!/usr/bin/env bash
    port=8000
    while ss -tlnp | grep -q ":$port "; do
        port=$((port + 1))
    done
    echo "Serving on http://localhost:$port"
    uv run mkdocs serve --livereload --dev-addr "localhost:$port"

# build the documentation site
build:
    uv run mkdocs build