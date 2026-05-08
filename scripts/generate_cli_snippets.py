#!/usr/bin/env python3
"""Generate per-command Markdown snippets from data/vipm-public-cli.json.

Writes one snippet per command to docs/.snippets/_generated/commands/.
Snippets are designed to be included via pymdownx.snippets; pages
control heading level by placing the include under their own heading.

Iterative-experiment v1 shape per snippet:

  - Tier badge include (nested snippet: tier-{tier}.md)
  - Description as a paragraph
  - Usage line
  - Options table (if any)

`always_allowed` commands receive no tier badge. Subcommands are
not yet handled.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE = REPO_ROOT / "data" / "vipm-public-cli.json"
OUTDIR = REPO_ROOT / "docs" / ".snippets" / "_generated" / "commands"

# Per-tier badge inclusion. "Free" and "always_allowed" mean "available
# in all editions" — readers can infer that from the absence of a badge,
# so we don't emit one (this matches the "flag exceptions, not norms"
# convention applied elsewhere in the docs).
#
# A "community" tier item is available in BOTH Community and Pro, so we
# show both badges to make the eligibility explicit. A "professional"
# item is Pro-only, so it gets just the Pro badge.
TIER_BADGES_BY_TIER = {
    "free": [],
    "always_allowed": [],
    "community": ["tier-community.md", "tier-pro.md"],
    "professional": ["tier-pro.md"],
}


def render_tier_badge(access: dict) -> str:
    badges = TIER_BADGES_BY_TIER.get(access.get("tier"), [])
    if not badges:
        return ""
    return "".join(f'--8<-- "{b}"\n' for b in badges) + "\n"


def render_usage(cmd: dict) -> str:
    parts = [f"`vipm {cmd['name']}"]
    if cmd.get("options"):
        parts.append("[OPTIONS]")
    for arg in cmd.get("arguments", []):
        token = arg["value_name"]
        if arg.get("multiple"):
            token = f"[{token}]..."
        elif not arg.get("required"):
            token = f"[{token}]"
        else:
            token = f"<{token}>"
        parts.append(token)
    return "**Usage:** " + " ".join(parts) + "`"


PRO_OPTION_BADGE = (
    "[VIPM Pro](../vipm-editions-comparison.md#available-editions)"
    "{ .md-button .vipm-tier-pill-small .vipm-tier-pro }"
)


def render_value_signature(opt: dict) -> str:
    """Format the value signature attached to an option flag.

    - Boolean toggles (true/false) → no signature.
    - Short enums (≤3 values) → ``<a|b|c>``.
    - Otherwise → ``<VALUE_NAME>``.
    """
    possible = opt.get("possible_values") or []
    if possible == ["true", "false"]:
        return ""
    if 0 < len(possible) <= 3:
        return f" <{'|'.join(possible)}>"
    value_name = opt.get("value_name")
    if value_name:
        return f" <{value_name}>"
    return ""


def render_default_suffix(opt: dict) -> str:
    """Append a default-value suffix to an option description, if any."""
    defaults = opt.get("defaults") or []
    if not defaults:
        return ""
    formatted = ", ".join(f"`{d}`" for d in defaults)
    return f" (default: {formatted})"


def render_option_row(opt: dict) -> str:
    flags = []
    if opt.get("short"):
        flags.append(f"`-{opt['short']}`")
    if opt.get("long"):
        flags.append(f"`{opt['long']}`")
    flag_cell = ", ".join(flags) if flags else f"`{opt['name']}`"

    desc = opt.get("description", "").replace("|", "\\|").replace("\n", " ")
    access = opt.get("access") or {}
    if access.get("tier") == "professional":
        desc = f"{desc} {PRO_OPTION_BADGE}"

    return f"| {flag_cell} | {desc} |"


def render_options_table(cmd: dict) -> str:
    options = cmd.get("options") or []
    if not options:
        return ""
    # Wrap in a div so we can target the table with CSS. The `markdown`
    # attribute (md_in_html extension) keeps the wrapped content
    # parsed as Markdown rather than treated as raw HTML.
    lines = [
        "**Options:**",
        "",
        '<div class="cli-options" markdown>',
        "",
        "| Option | Description |",
        "|---|---|",
    ]
    lines.extend(render_option_row(opt) for opt in options)
    lines.append("")
    lines.append("</div>")
    return "\n".join(lines) + "\n"


def render_command_snippet(cmd: dict) -> str:
    chunks = [
        render_tier_badge(cmd.get("access", {})),
        cmd.get("description", "").rstrip(".") + ".\n",
        "\n" + render_usage(cmd) + "\n",
    ]
    options_table = render_options_table(cmd)
    if options_table:
        chunks.append("\n" + options_table)
    return "".join(chunks)


def render_global_option_row(opt: dict) -> str:
    """Render a Global Options row: signature attached to the long flag."""
    sig = render_value_signature(opt)
    flags = []
    if opt.get("short"):
        flags.append(f"-{opt['short']}")
    if opt.get("long"):
        flags.append(opt["long"])
    if sig and flags:
        # Attach value signature to the last flag so the whole "flag plus
        # value" form sits inside a single backticked code span — keeps
        # the visual unit obvious and side-steps markdown table escaping
        # of `|` characters that appear inside short enum signatures.
        flags[-1] = flags[-1] + sig
    flag_cell = ", ".join(f"`{f}`" for f in flags) if flags else f"`{opt['name']}`"

    desc = opt.get("description", "").replace("|", "\\|").replace("\n", " ")
    desc += render_default_suffix(opt)
    access = opt.get("access") or {}
    if access.get("tier") == "professional":
        desc = f"{desc} {PRO_OPTION_BADGE}"

    return f"| {flag_cell} | {desc} |"


def render_global_options_snippet(global_options: list) -> str:
    """Render the Global Options table snippet.

    The source JSON is already sanitized upstream (no private/hidden
    items), so this just iterates and renders each option.
    """
    rows = [render_global_option_row(opt) for opt in global_options]
    lines = [
        '<div class="cli-options" markdown>',
        "",
        "| Option | Description |",
        "|---|---|",
        *rows,
        "",
        "</div>",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    if not SOURCE.is_file():
        sys.exit(f"missing source: {SOURCE}")
    data = json.loads(SOURCE.read_text())
    OUTDIR.mkdir(parents=True, exist_ok=True)

    written = 0
    for cmd in data.get("commands", []):
        out = OUTDIR / f"{cmd['name']}.md"
        out.write_text(render_command_snippet(cmd))
        written += 1

    global_snippet_path = OUTDIR.parent / "global-options.md"
    global_snippet_path.write_text(
        render_global_options_snippet(data.get("global_options", []))
    )

    print(
        f"wrote {written} command snippet(s) to {OUTDIR.relative_to(REPO_ROOT)}, "
        f"plus {global_snippet_path.relative_to(REPO_ROOT)}"
    )


if __name__ == "__main__":
    main()
