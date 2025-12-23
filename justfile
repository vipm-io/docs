# This file contains useful commands for development tasks.

list:
    @just --list

# build and server locally, with live reload
dev:
    uv run mkdocs serve --livereload

# build the documentation site
build:
    uv run mkdocs build