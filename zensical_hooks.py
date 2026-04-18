"""Zensical + MkDocs-style hooks shim.

Zensical does not yet expose a native hook API — its module system (see
https://zensical.org/about/roadmap/#module-system) is under active design.
Until that ships, this file monkey-patches two internal entry points
(`zensical.config.parse_config` and `zensical.markdown.render`) to restore
behavior that previously lived in `hooks.py` under MkDocs:

  1. Dynamic copyright year in the site footer.
  2. Auto-generated release-notes table on `release-notes/index.md`.

Pattern adapted from
https://gist.github.com/kamilkrzyskow/72c6ec3093e48132ead9469558e144c2 —
not endorsed by the Zensical team. Each Zensical upgrade may break the
shim; when that happens, either re-adapt or fall back to hand-maintaining
the affected surfaces. See `dev-docs/zensical-migration.md`.

Invoke instead of the `zensical` CLI:

    uv run python zensical_hooks.py build
    uv run python zensical_hooks.py serve
"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

import yaml
import zensical.config as config_module
import zensical.main as main_module
import zensical.markdown as markdown_module

_ORIG_PARSE_CONFIG = config_module.parse_config
_ORIG_RENDER = markdown_module.render

# Captured from on_config so on_page_markdown can resolve `path` (which is
# delivered relative to docs_dir) back to an absolute filesystem path.
_DOCS_DIR: Path | None = None


def _wrap_config(func):
    def wrapper(path: str):
        config = func(path)
        current_year = datetime.now().year
        config["copyright"] = (
            f"Copyright &copy; {current_year} VIPM Community Contributors"
        )
        global _DOCS_DIR
        docs_dir = config.get("docs_dir") or "docs"
        _DOCS_DIR = (Path(path).parent / docs_dir).resolve()
        return config

    return wrapper


def _parse_frontmatter(filepath: Path) -> dict:
    content = filepath.read_text()
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if match:
        return yaml.safe_load(match.group(1)) or {}
    return {}


def _version_sort_key(filename: str) -> tuple:
    stem = filename.removesuffix(".md")
    parts = []
    for part in stem.split("."):
        try:
            parts.append(int(part))
        except ValueError:
            parts.append(0)
    return tuple(parts)


def _release_notes_table(rn_dir: Path) -> str:
    rn_files = [
        f.name for f in rn_dir.iterdir() if f.suffix == ".md" and f.name != "index.md"
    ]
    rn_files.sort(key=_version_sort_key, reverse=True)
    rows = []
    for fname in rn_files:
        meta = _parse_frontmatter(rn_dir / fname)
        slug = fname.removesuffix(".md")
        title = meta.get("title", slug)
        description = meta.get("description", "")
        link = f'<a href="{slug}/" style="white-space: nowrap">{title}</a>'
        rows.append(f"| {link} | {description} |")
    return "| Release | Summary |\n| --- | --- |\n" + "\n".join(rows)


def _wrap_markdown(func):
    def wrapper(content: str, path: str, url: str):
        if (
            path.endswith("release-notes/index.md")
            and "<!-- release-notes-table -->" in content
            and _DOCS_DIR is not None
        ):
            rn_dir = _DOCS_DIR / "release-notes"
            if rn_dir.is_dir():
                content = content.replace(
                    "<!-- release-notes-table -->",
                    _release_notes_table(rn_dir),
                )
        return func(content, path, url)

    return wrapper


def main() -> None:
    config_module.parse_config = _wrap_config(_ORIG_PARSE_CONFIG)
    markdown_module.render = _wrap_markdown(_ORIG_RENDER)
    main_module.cli()


if __name__ == "__main__":
    main()
