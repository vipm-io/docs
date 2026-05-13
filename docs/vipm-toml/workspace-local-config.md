---
title: Workspace-Local Config
---

# Workspace-Local Configuration (`.vipm/config.toml`)

!!! warning "Preview Feature"
    Workspace-local configuration requires **VIPM Desktop 2026 Q3 Preview** or later. This feature is not available in stable releases. See the [Preview page](../preview.md) for installation instructions.

`.vipm/config.toml` is a **per-developer, non-committed** companion to `vipm.toml`. It lets you override the LabVIEW version your local commands use — without editing the team's shared `vipm.toml` and without retyping `--labview-version` on every invocation.

The team's `vipm.toml` and your personal `.vipm/config.toml` are two different things:

- **`vipm.toml`** is the project's team contract — committed to the repo, shared across the team.
- **`.vipm/config.toml`** is your personal override — local to your checkout, never committed.

## When to use it

- **You haven't installed the team's pinned LabVIEW year yet.** The team's `vipm.toml` declares `labview-version = "2024"`, but you're still on LabVIEW 2023 locally. Point `.vipm/config.toml` at 2023 so `vipm install`, `vipm sbom`, etc. run against your installed year — without touching the shared file.
- **CI runner / dev-machine drift.** A CI runner has a different set of installed LabVIEW versions than the developer who authored `vipm.toml`. The runner's `.vipm/config.toml` selects what's actually there.
- **Compatibility review.** You're reviewing a PR and want to validate the project against a LabVIEW year other than the one the author declared.
- **Version-bump preparation.** You're about to bump the team's `labview-version` in `vipm.toml` and want to verify locally first.

## File location and shape

`.vipm/config.toml` lives in a `.vipm/` directory **next to your project's `vipm.toml`**:

```
my-project/
├── vipm.toml          # team-committed
├── .vipm/
│   └── config.toml    # per-developer; gitignored
└── ...
```

The file is a small TOML overlay of `vipm.toml`'s `[project]` section:

```toml
[project]
labview-version = "2023"
labview-bitness = 64
```

A `.vipm/` directory in any other location is ignored. The override is consulted only when colocated with the `vipm.toml` that VIPM discovered for your command.

## Allowed keys

Two keys, both optional:

| Key | Type | Purpose |
|-----|------|---------|
| `[project].labview-version` | string (year, e.g. `"2024"`) | Year to use for this workspace |
| `[project].labview-bitness` | integer (`32` or `64`) | Bitness to use for this workspace |

Any other key — a different `[project]` field, or any other table — is rejected. For example, this file:

```toml
[project]
name = "my-project"           # ← not allowed in .vipm/config.toml
```

produces an error and exits with code `2`. Only the LabVIEW year and bitness are configurable here; everything else belongs in `vipm.toml`.

## Precedence

When VIPM picks a LabVIEW version for a command, it consults sources in this order — the **first** source that yields a value wins:

1. `--labview-version` / `--labview-bitness` CLI flags
2. **`.vipm/config.toml`** (this file)
3. `vipm.toml` `[project].labview-version` / `labview-bitness`
4. Input-file metadata (`.lvproj` `LVVersion`, `.dragon` / `.vipc` target, etc.)
5. Auto-detect from installed LabVIEW

`labview-version` and `labview-bitness` are resolved **independently**. For example, with the override file above and a `vipm.toml` that declares `labview-version = "2024"`:

- `vipm install` → uses LabVIEW 2023 (64-bit). The override's year wins over `vipm.toml`'s.
- `vipm install --labview-version 2025` → uses LabVIEW 2025 (64-bit). The CLI flag's year wins over the override's. Bitness still comes from the override since the CLI did not provide one.

## Field independence

You can override only the year, only the bitness, or both.

**Override the year only:**

```toml
[project]
labview-version = "2023"
```

Bitness then comes from `vipm.toml` (or its default of 64).

**Override the bitness only:**

```toml
[project]
labview-bitness = 32
```

Year then comes from `vipm.toml` (or a lower layer).

**Override both:**

```toml
[project]
labview-version = "2023"
labview-bitness = 32
```

!!! tip
    When the target year/bitness combination on your machine differs from `vipm.toml` in **both** dimensions, set both keys explicitly. Bitness-only overrides work, but if the year resolved from a lower layer isn't installed in your chosen bitness, the resulting error is less specific than if you'd named the combination directly in `.vipm/config.toml`.

## Gitignore convention

`.vipm/` is per-developer state. Don't commit it. Add this to your repo's `.gitignore`:

```gitignore
.vipm/
```

Each developer's `.vipm/config.toml` then stays local to their checkout, and the team's `vipm.toml` remains the single committed source of project configuration.

## Errors

| Scenario | Exit code | Behavior |
|----------|-----------|----------|
| Override points at an uninstalled year/bitness | `4` | Fails fast. The error names `.vipm/config.toml` so you know where to fix it. |
| Unknown key in `.vipm/config.toml` | `2` | Rejected at parse time; error names the unknown key. |
| Malformed TOML | `2` | Rejected at parse time. |
| Override's year is older than the command's minimum LabVIEW year | `20` | Some commands have a minimum LabVIEW year (e.g., `vipm build` requires LabVIEW 2024+); the error reports the resolved version and the override path. |
| Override's year is newer than the CLI's supported window | `19` | Rare; surfaces only if you override to a year past the CLI's upper bound. |

See the [CLI command reference](../cli/command-reference.md) for the full exit-code taxonomy.

## Complete example

A typical project where the team is on LabVIEW 2024 64-bit, but you're temporarily running LabVIEW 2023 32-bit:

```
my-project/
├── vipm.toml          # team: labview-version = "2024", labview-bitness = 64
├── .vipm/
│   └── config.toml    # you:  labview-version = "2023", labview-bitness = 32
└── .gitignore         # contains: .vipm/
```

`my-project/.vipm/config.toml`:

```toml
[project]
labview-version = "2023"
labview-bitness = 32
```

Running `vipm install` from inside `my-project/`:

```
$ vipm install
Using LabVIEW 2023 (32-bit) from workspace override (./.vipm/config.toml)
... installs dependencies for LabVIEW 2023 (32-bit) ...
```

A teammate who has not created their own `.vipm/config.toml` continues to see LabVIEW 2024 (64-bit) per the team's `vipm.toml`. The shared file does not change.

--8<-- "need-help.md"
