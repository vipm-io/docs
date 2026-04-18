# This file contains useful commands for development tasks.

list:
    @just --list

# build and serve locally (auto-finds open port starting at 8000)
dev:
    #!/usr/bin/env bash
    port=8000
    while ss -tlnp | grep -q ":$port "; do
        port=$((port + 1))
    done
    echo "Serving on http://localhost:$port"
    uv run python zensical_hooks.py serve --dev-addr "localhost:$port"

# build the documentation site
build:
    uv run python zensical_hooks.py build