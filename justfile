# This file contains useful commands for development tasks.

# build and server locally, with live reload
dev:
    uv run mkdocs serve --livereload

build:
    uv run mkdocs build