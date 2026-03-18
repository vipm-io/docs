"""MkDocs hooks for dynamic configuration."""
import os
import re
from datetime import datetime

import yaml


def on_config(config, **kwargs):
    """Update copyright year dynamically at build time."""
    current_year = datetime.now().year
    config['copyright'] = f'Copyright &copy; {current_year} VIPM Community Contributors'
    return config


def _parse_frontmatter(filepath):
    """Extract frontmatter fields from a Markdown file."""
    with open(filepath) as f:
        content = f.read()
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if match:
        return yaml.safe_load(match.group(1)) or {}
    return {}


def _version_sort_key(filename):
    """Extract numeric parts from a filename for sorting (e.g. '2025.3.1.md' -> (2025, 3, 1))."""
    stem = filename.replace(".md", "")
    parts = []
    for part in stem.split("."):
        try:
            parts.append(int(part))
        except ValueError:
            parts.append(0)
    return tuple(parts)


def on_page_markdown(markdown, page, config, files, **kwargs):
    """Replace <!-- release-notes-table --> with a generated table of release notes."""
    if page.file.src_path != "release-notes/index.md":
        return markdown

    if "<!-- release-notes-table -->" not in markdown:
        return markdown

    docs_dir = config["docs_dir"]
    rn_dir = os.path.join(docs_dir, "release-notes")

    rn_files = [
        f for f in os.listdir(rn_dir)
        if f.endswith(".md") and f != "index.md"
    ]
    rn_files.sort(key=_version_sort_key, reverse=True)

    rows = []
    for fname in rn_files:
        meta = _parse_frontmatter(os.path.join(rn_dir, fname))
        title = meta.get("title", fname.replace(".md", ""))
        description = meta.get("description", "")
        slug = fname.replace(".md", "")
        link = f'<a href="{slug}/" style="white-space: nowrap">{title}</a>'
        rows.append(f"| {link} | {description} |")

    table = "| Release | Summary |\n| --- | --- |\n" + "\n".join(rows)
    return markdown.replace("<!-- release-notes-table -->", table)
