---
title: Overview
---

# vipm.toml Project Configuration

!!! warning "Preview Feature"
    `vipm.toml` support requires **VIPM Desktop 2026 Q1 Preview** or later.
    This feature is not available in stable releases. See the [Preview page](../preview.md) for installation instructions.

!!! note "Community and Professional Edition Features"
    Most `vipm.toml` commands require **VIPM Community Edition (with public repositories) or VIPM Professional**. Use `vipm help` or `vipm <command> --help` for more details about the commands for which this applies.

`vipm.toml` is a modern, human-readable configuration file for managing your LabVIEW project's dependencies and builds.

Ready to dive in? Jump to the **[vipm.toml Getting Started guide →](vipm-toml/getting-started.md)**

## First look at `vipm.toml`

A typical workflow with `vipm.toml`:

```bash
vipm init                          # Create vipm.toml
vipm add oglib_array oglib_error   # Add dependencies
```

This creates a `vipm.toml` file like:

```toml
[project]
name = "my-labview-project"
version = "1.0.0"
labview-version = "2024"

[dependencies]
oglib_array = "6.0.1.20"
oglib_error = "5.0.0.27"
```

Install your packages:

```bash
vipm install                       # Install packages to LabVIEW
```

Add a build spec:

```toml
[build.my_library]
type = "ppl"
top-level-library = "src/MyLibrary.lvlib"
```

Do a build:

```bash
vipm build                         # Build your project (see `my_library` below)
```

Use your build output:

```bash
builds/my_library/MyLibrary.lvlib
```

## Why vipm.toml?

| Feature | |
|---------|---|
| ✅ **Human-readable** | TOML format, easy to edit and review |
| ✅ **Version control** | Git-friendly diffs and merges |
| ✅ **Lock files** | Reproducible builds with `vipm.lock` |
| ✅ **Build system** | Define PPL, EXE, and package builds in one file |
| ✅ **CI/CD ready** | `vipm lock --check` for validation |

## Next Steps

- Read through **[the Getting Started guide](getting-started.md)** and follow the step-by-step instructions for using `vipm.toml` for your labview project dependencies, builds, and CI/CD workflow automations.

--8<-- "need-help.md"
