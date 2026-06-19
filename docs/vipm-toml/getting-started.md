---
title: Getting Started
---

# Getting Started with vipm.toml

!!! note "Community and Professional Edition Features"
    Most `vipm.toml` commands require **VIPM Community Edition (with public repositories) or VIPM Professional**. Use `vipm help` or `vipm <command> --help` for more details about the commands for which this applies.

This guide walks you through using `vipm.toml` to manage your LabVIEW project's dependencies and builds.

> **TL;DR** - Quick start for experienced users:
>
> ```bash
> vipm init                          # Create vipm.toml
> vipm add oglib_array oglib_error   # Add dependencies
> vipm install                       # Install packages to LabVIEW
> vipm build                         # Build your project
> ```

## Table of Contents

- [What is vipm.toml?](#what-is-vipmtoml)
- [What is vipm.lock?](#what-is-vipmlock)
- [Creating a New Project](#creating-a-new-project)
- [Managing Dependencies](#managing-dependencies)
- [Lock Files](#lock-files)
- [Building Your Project](#building-your-project)
- [Cleaning Build Outputs](#cleaning-build-outputs)
- [Complete Example](#complete-example)
- [CI/CD Workflows](#cicd-workflows)
- [Command Reference](#command-reference)

---

## What is vipm.toml?

`vipm.toml` is a configuration file that defines your LabVIEW project's metadata, dependencies, and build specifications in a human-readable format. It replaces or works alongside traditional `.vipc` and `.dragon` files.

Benefits:

- **Human-readable** - Easy to edit and review in version control
- **Declarative Dependencies** - Specify what packages your project needs
- **Easy-to-use Build System** - Define build specifications in one place
- **Reproducible Builds** - Automatically tracks ALL your project's dependencies (and transitive dependencies)
- **Git, Version Control Friendly** - Easy to diff/merge the file

## What is vipm.lock?

`vipm.lock` is a file that records the exact versions of every package your project resolves to (including transitive dependencies), so a build can be reproduced exactly. It is a human-readable (and git source control friendly) configuration file, but it should not be manually edited. Lock files are **opt-in**: you create one with `vipm lock`, and `vipm install` keeps it up to date from then on. We'll cover this in the [Lock Files](#lock-files) section below, and in full detail on the dedicated [Lock Files page](lock-files.md).

---

## Creating a New Project

### Initialize a vipm.toml File

Use `vipm init` to create a new `vipm.toml` file:

```bash
# Create vipm.toml in current directory
vipm init

# Create vipm.toml in a specific directory
vipm init path/to/project

# Create with a custom project name
vipm init --name my-labview-project
```

The `init` command will:

- Create a minimal `vipm.toml` with a `[project]` section
- Detect the LabVIEW version from existing `.lvproj` files (if present)
- Fail if `vipm.toml` already exists (use `--force` to overwrite)

Example output:

```bash
$ vipm init --name my-labview-project
Created vipm.toml
```

!!! tip
    Use `vipm init --force` to overwrite an existing `vipm.toml` file. This will replace the file without prompting.

### Example Generated File

```toml
[project]
name = "my-labview-project"
version = "0.1.0"
labview-version = "2024"
```

!!! tip "Per-developer LabVIEW version override"
    The `[project].labview-version` field is the team's pinned version, shared via git. If you need to run commands against a different LabVIEW year locally — without editing the shared file — create a personal `.vipm/config.toml`. See [Workspace-Local Configuration](workspace-local-config.md).

---

## Managing Dependencies

### Adding Dependencies

Use `vipm add` to add packages to your `vipm.toml`:

```bash
# Add a package (uses latest available version)
vipm add oglib_array

# Add a package with a specific version
vipm add oglib_array@6.0.1.20

# Add multiple packages at once
vipm add oglib_array oglib_error jki_lib_state_machine

# Add as a dev dependency (testing frameworks, etc.)
vipm add --dev caraya

# Add and immediately install (refreshes an existing vipm.lock)
vipm add --install oglib_array
```

After adding dependencies, your `vipm.toml` will look like:

```toml
[project]
name = "my-labview-project"
version = "0.1.0"
labview-version = "2024"

[dependencies]
oglib_array = "6.0.1.20"
oglib_error = "5.0.0.27"
jki_lib_state_machine = "2.0.0.50"

[dev-dependencies]
caraya = "1.4.5.165"
```

#### Notes on `vipm add`

- Requires an existing `vipm.toml` file (use `vipm init` first)
- Searches parent directories for `vipm.toml`, so you can run it from subdirectories
- Preserves comments and formatting in your existing file
- Does NOT create or modify `vipm.lock` — run `vipm lock` (or `vipm install`, which refreshes an existing lock) to update it
- Does NOT install packages by default—use `vipm install` after adding, or use `--install`

### Removing Dependencies

Use `vipm remove` to remove packages from your `vipm.toml`:

```bash
# Remove a package
vipm remove oglib_array

# Remove multiple packages
vipm remove oglib_array oglib_error

# Remove from dev dependencies
vipm remove --dev caraya
```

#### Notes on `vipm remove`

- Only removes the package from `vipm.toml`—does NOT uninstall it from LabVIEW
- Automatically updates `vipm.lock` if it exists (does not create it)
- Use `vipm uninstall <package>` if you also want to remove it from LabVIEW
- Returns an error if the package isn't found in the manifest

### Installing Dependencies

Use `vipm install` to install all dependencies declared in `vipm.toml`:

```bash
# Install from vipm.toml in current directory
vipm install

# Install from a specific vipm.toml file
vipm install ./path/to/vipm.toml

# Install including dev dependencies
vipm install --dev

# Explicitly skip dev dependencies
vipm install --no-dev

# Upgrade packages to latest version if already installed
vipm install --upgrade
```

When run without arguments, `vipm install` searches for manifest files in this order:

1. `vipm.toml` (highest priority)
2. `.dragon` file
3. `.vipc` file

The `labview-version` from `vipm.toml` is used automatically when installing. To override for your local checkout only — without editing the shared file — see [Workspace-Local Configuration](workspace-local-config.md).

---

## Lock Files

`vipm.lock` records the exact resolved version of every package your project depends on — including transitive dependencies — together with their sources and integrity checksums, so a build can be reproduced exactly. Lock files are **opt-in**: no `vipm.lock` exists until you create one with `vipm lock`, and `vipm install` keeps it up to date from then on. `vipm add` and `vipm remove` edit `vipm.toml` only and never touch the lock.

For the full lock-file workflow — what gets recorded, the on-disk format, the schema, and how the lock file is consumed by `vipm build` and `vipm sbom` — see the dedicated [Lock Files](lock-files.md) page.

A common use is verifying in CI that the committed lock file still matches `vipm.toml`:

```bash
# Verify vipm.lock is in sync with vipm.toml (writes nothing).
# Exit code 0 = in sync; exit code 2 = out of sync (or no lock file).
vipm lock --check
```

See [Checking lock file sync (in CI)](lock-files.md#checking-lock-file-sync-in-ci) for the full details.

---

## Building Your Project

The `vipm build` command can build artifacts defined in `vipm.toml`.

### Defining Builds

Add build specifications to your `vipm.toml`:

```toml
[project]
name = "my-labview-project"
version = "1.0.0"
labview-version = "2024"

# Packed library build
[build.my_library]
type = "ppl"
top-level-library = "src/MyLibrary.lvlib"

# Executable build
[build.my_app]
type = "exe"
startup-vi = "src/Main.vi"

# Build for a different LabVIEW version
[build.legacy_library]
type = "ppl"
top-level-library = "src/LegacyLib.lvlib"
labview-version = "2020"      # Override project default
labview-bitness = 32          # Override project default

# Wrap an existing .lvproj build spec
[build.legacy_build]
type = "lvproj"
path = "MyProject.lvproj"
spec = "Release Build"
target = "My Computer"

# Wrap an existing .vipb file
[build.my_package]
type = "vipb"
path = "Package.vipb"
```

!!! tip
    Individual builds can override `labview-version` and `labview-bitness` from `[project]`. This is useful when you need to build the same library for multiple LabVIEW versions.

### Running Builds

```bash
# Build all default targets
vipm build

# Build a specific target
vipm build my_library

# Build all targets (including non-default)
vipm build --all

# Build with a specific version number
vipm build my_app --version-number 2.1.0

# Build with a specific build number (4th component)
vipm build my_app --build-number 42
```

### Supported Build Types

| Type | Alias | Description | Required Fields |
|------|-------|-------------|-----------------|
| `packed-library` | `ppl` | Packed Project Library (.lvlibp) | `top-level-library` |
| `executable` | `exe` | Standalone application (.exe/.app) | `startup-vi` |
| `lvproj` | — | Build from existing .lvproj | `path`, `spec` |
| `vipb` | — | Build from existing .vipb | `path` |

### Build Output Directories

By default, builds output to `builds/{build_name}/`. You can customize this:

```toml
[project]
name = "my-project"
builds-dir = "dist"  # All builds go under dist/ instead of builds/

[build.my_library]
type = "ppl"
top-level-library = "src/MyLib.lvlib"
output-name = "MyLibrary"           # Custom output filename
# Output: dist/my_library/

[build.release]
type = "exe"
startup-vi = "src/Main.vi"
output-dir = "releases"              # Explicit override
# Output: releases/
```

### Variable Substitution

You can use variables in `output-dir` and `output-name` fields using `${VAR_NAME}` syntax. This reduces duplication and enables dynamic, portable build configurations.

#### Supported Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `${LABVIEW_VERSION}` | Target LabVIEW version year | `2024` |
| `${LABVIEW_BITNESS}` | Target bitness (32 or 64) | `64` |
| `${PROJECT_NAME}` | From `[project].name` | `my-project` |
| `${PROJECT_VERSION}` | From `[project].version` | `1.0.0` |
| `${BUILD_NAME}` | Current build target name | `my_library` |
| `${BUILDS_DIR}` | From `[project].builds-dir` | `builds` |
| `${OS_NAME}` | Operating system | `linux`, `windows`, `macos` |
| `${ARCH}` | CPU architecture | `x86_64`, `aarch64` |

#### Example

```toml
[project]
name = "my-library"
version = "1.0.0"
labview-version = "2024"

[build.ppl]
type = "packed-library"
top-level-library = "src/MyLib.lvlib"
output-name = "MyLib_${LABVIEW_VERSION}_${LABVIEW_BITNESS}bit.lvlibp"
```

With LabVIEW 2024 64-bit on Linux, this resolves to:

- output file: `builds/packed-library/MyLib_2024_64bit.lvlibp`

!!! tip
    Variable substitution is especially useful when building the same project for multiple LabVIEW versions/bitnesses and operating systems, as the output paths automatically reflect the target version.

### Build Dependencies

Use the `depends-on` field to specify that one build must complete before another. This is useful when:

- A VI package (`.vipb`) needs a packed library to be built first
- An executable depends on libraries built by other build specs
- You want to ensure a specific build order

```toml
[build.core_library]
type = "ppl"
top-level-library = "src/CoreLib.lvlib"

[build.ui_library]
type = "ppl"
top-level-library = "src/UILib.lvlib"
depends-on = ["core_library"]  # Build core_library first

[build.my_app]
type = "exe"
startup-vi = "src/Main.vi"
depends-on = ["core_library", "ui_library"]  # Build both libraries first

[build.my_package]
type = "vipb"
path = "Package.vipb"
depends-on = ["my_app"]  # Build the app before packaging
```

When you run `vipm build my_package`, vipm will automatically build the dependencies in the correct order: `core_library` → `ui_library` → `my_app` → `my_package`.

You can skip dependency builds with `--no-deps` or force rebuild them with `--rebuild-deps`.

---

## Cleaning Build Outputs

Use `vipm clean` to remove build output directories:

```bash
# Clean all build outputs
vipm clean

# Clean a specific build
vipm clean my_library

# Preview what would be deleted (dry run)
vipm clean --dry-run

# Explicitly clean all builds
vipm clean --all
```

---

## Complete Example

Here's a complete `vipm.toml` for a typical LabVIEW project:

```toml
[project]
name = "instrument-control-system"
version = "2.1.0"
labview-version = "2024"
labview-bitness = 64
description = "Automated instrument control and data acquisition system"
authors = ["Lab Team <lab@example.com>"]
license = "MIT"
repository = "https://github.com/example/instrument-control"

[dependencies]
oglib_array = "6.0.1.20"
oglib_error = "5.0.0.27"
jki_lib_state_machine = "2.0.0.50"

[dev-dependencies]
caraya = "1.4.5.165"
jki_vi_tester = "3.0.2.294"

[build.main_library]
type = "ppl"
top-level-library = "src/InstrumentControl.lvlib"

[build.main_app]
type = "exe"
startup-vi = "src/Main.vi"
default = false  # Not built by default

[build.package]
type = "vipb"
path = "InstrumentControl.vipb"
depends-on = ["main_library"]  # Build library first
```

### Typical Workflow

```bash
# 1. Initialize the project
vipm init --name instrument-control-system

# 2. Add dependencies
vipm add oglib_array oglib_error jki_lib_state_machine
vipm add --dev caraya jki_vi_tester

# 3. Install all dependencies
vipm install --dev

# 4. Generate lock file
vipm lock

# 5. Build the project
vipm build

# 6. Clean up build outputs when needed
vipm clean
```

---

## CI/CD Workflows

The `vipm.toml` and `vipm.lock` files make it easy to integrate LabVIEW builds into your CI/CD pipeline. For additional CI/CD examples and troubleshooting, see the [GitHub Actions guide](../cli/github-actions.md).

### GitHub Actions

```yaml
name: Build LabVIEW Project

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: [self-hosted, labview]  # Requires LabVIEW on runner
    steps:
      - uses: actions/checkout@v4

      - name: Verify lock file is in sync
        run: vipm lock --check

      - name: Install dependencies
        run: vipm install

      - name: Build project
        run: vipm build --all
```

### GitLab CI

```yaml
stages:
  - validate
  - build

check-lockfile:
  stage: validate
  script:
    - vipm lock --check
  tags:
    - labview

build-project:
  stage: build
  script:
    - vipm install
    - vipm build --all
  artifacts:
    paths:
      - builds/
  tags:
    - labview
```

### Jenkins Pipeline

```groovy
pipeline {
    agent { label 'labview' }
    stages {
        stage('Validate') {
            steps {
                sh 'vipm lock --check'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'vipm install'
            }
        }
        stage('Build') {
            steps {
                sh 'vipm build --all'
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'builds/**/*', fingerprint: true
        }
    }
}
```

### CI Best Practices

- **Always run `vipm lock --check`** first to catch out-of-sync lock files early
- **Commit `vipm.lock`** to your repository for reproducible builds
- **Use `--no-dev`** in production builds: `vipm install --no-dev`
- **Cache dependencies** if your CI system supports it (speeds up builds)
- **Fail fast** on lock file mismatches to enforce discipline

---

## Command Reference

For detailed documentation on all CLI commands, see the [CLI Command Reference](../cli/command-reference.md).

| Command | Description |
|---------|-------------|
| `vipm init [path]` | Create a new vipm.toml file (`--name`, `--force`) |
| `vipm add <packages>` | Add dependencies to vipm.toml (`--dev`, `--install`) |
| `vipm remove <packages>` | Remove dependencies from vipm.toml (`--dev`) |
| `vipm install` | Install dependencies from vipm.toml (`--dev`, `--no-dev`, `--upgrade`) |
| `vipm lock` | Generate/update vipm.lock (`--best-effort`) |
| `vipm lock --check` | Verify lock file is in sync (for CI) |
| `vipm build [name]` | Build targets defined in vipm.toml (`--all`, `--debug`, `--version-number`) |
| `vipm clean [name]` | Remove build output directories (`--all`, `--dry-run`) |
| `vipm list [file]` | List packages from vipm.toml or installed (`--installed`, `--dev`, `--no-dev`) |

--8<-- "need-help.md"
