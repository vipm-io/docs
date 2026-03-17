---
title: NI Packages (NIPM)
---

# Managing NI Packages with vipm.toml

VIPM supports managing NI Package Manager (NIPM) dependencies alongside VIPM packages in a single `vipm.toml` manifest. This gives you a unified view of all your project's dependencies — both community packages from vipm.io and NI packages from NI feeds.

## vipm.toml format

NIPM dependencies use three dedicated sections in `vipm.toml`:

```toml
[nipm.feeds]
ni = "https://download.ni.com/support/nipkg/products/ni-d/ni-daqmx/24.5/released/"

[nipm.dependencies]
ni-daqmx = "24.5.0"

[nipm.dev-dependencies]
ni-teststand = "2023.1.0"
```

### `[nipm.feeds]`

Maps human-readable aliases to NI package feed URLs. Feed aliases are referenced by dependencies to specify where to download the package.

```toml
[nipm.feeds]
ni-daqmx-feed = "https://download.ni.com/support/nipkg/products/ni-d/ni-daqmx/24.5/released/"
ni-visa-feed = "https://download.ni.com/support/nipkg/products/ni-v/ni-visa/2024Q1/released/"
```

### `[nipm.dependencies]` and `[nipm.dev-dependencies]`

Declare NIPM packages your project depends on. Two formats are supported:

**Simple format** — version string only:

```toml
[nipm.dependencies]
ni-daqmx = "24.5.0"
```

**Detailed format** — with feed alias:

```toml
[nipm.dependencies]
ni-daqmx = { version = "24.5.0", feed = "ni-daqmx-feed" }
```

Use `[nipm.dev-dependencies]` for packages only needed during development or testing.

!!! note
    NIPM dependencies require explicit version numbers. Unlike VIPM packages, version auto-resolution is not available for NIPM packages.

## Workflow

### Adding NIPM dependencies

Use `vipm add --nipm` to add NI packages to your manifest:

```bash
# Add with explicit version (required)
vipm add --nipm ni-daqmx@24.5.0

# Add with a feed alias
vipm add --nipm ni-daqmx@24.5.0 --feed ni-daqmx-feed

# Register a new feed and add the package
vipm add --nipm ni-daqmx@24.5.0 --feed ni-daqmx-feed --feed-url "https://download.ni.com/..."

# Add as a dev dependency
vipm add --nipm ni-teststand@2023.1.0 --dev
```

On Windows with NI Package Manager installed, VIPM can auto-detect the installed version if you omit the version number, and can discover which feed provides the package.

### Removing NIPM dependencies

```bash
vipm remove --nipm ni-daqmx
vipm remove --nipm ni-teststand --dev
```

### Locking

`vipm lock` includes NIPM dependencies in the lock file alongside VIPM packages:

```bash
vipm lock
```

The lock file records each NIPM package's name, version, feed URL, and checksum (when available).

### Installing

When you run `vipm install` on a project with NIPM dependencies, VIPM installs both VIPM and NIPM packages:

```bash
vipm install
```

!!! note "Windows only"
    NIPM package installation requires Windows with NI Package Manager installed. On other platforms, VIPM manages the manifest entries but cannot install NI packages. VIPM will display a warning if NIPM is not available.

!!! info "Planned: selective installation"
    `vipm install` does not yet support `--no-nipm` or `--no-vipm` flags to install only one type of package. Currently it installs both VIPM and NIPM dependencies together.

### Listing

`vipm list` shows NIPM dependencies alongside VIPM packages when listing from a `vipm.toml`:

```bash
vipm list vipm.toml
```

!!! info "Planned: selective listing"
    `vipm list` does not yet support `--no-nipm` or `--no-vipm` flags to filter by package type. Currently it shows all dependencies together.

### Inspecting NI packages

Use `vipm info --nipm` to view metadata for an installed NI package:

```bash
vipm info --nipm ni-daqmx
```

To see which files a package installed:

```bash
vipm info --nipm ni-daqmx --installed-files
```

`vipm info --nipm` requires Windows with NI Package Manager installed.

## Filtering by package type

Several commands include both VIPM and NIPM packages by default. Use `--no-nipm` or `--no-vipm` to filter:

| Command | `--nipm` | `--no-nipm` | `--no-vipm` |
|---------|----------|-------------|-------------|
| `vipm add` | Select NIPM mode | — | — |
| `vipm remove` | Select NIPM mode | — | — |
| `vipm info` | Query NIPM package | — | — |
| `vipm install` | — | Planned | Planned |
| `vipm list` | — | Planned | Planned |
| `vipm sbom` | — | Exclude NIPM | Exclude VIPM |
| `vipm sync` | — | Exclude NIPM | Exclude VIPM |

Examples:

```bash
# Generate SBOM with only VIPM packages
vipm sbom vipm.toml --format cyclonedx --schema-version 1.5 --no-nipm --output bom.json

# Generate SBOM with only NI packages
vipm sbom vipm.toml --format cyclonedx --schema-version 1.5 --no-vipm --output bom.json

# Sync vipm.toml from project, excluding NI packages
vipm sync --from MyProject.lvproj --no-nipm
```

## Complete example

```toml
[project]
name = "instrument-control"
version = "1.0.0"
labview-version = "2024"
labview-bitness = 64

[dependencies]
oglib_array = "6.0.1.20"
jki_lib_state_machine = "2.0.0.50"

[dev-dependencies]
caraya = "1.4.5.165"

[nipm.feeds]
ni-daq = "https://download.ni.com/support/nipkg/products/ni-d/ni-daqmx/24.5/released/"

[nipm.dependencies]
ni-daqmx = { version = "24.5.0", feed = "ni-daq" }

[nipm.dev-dependencies]
ni-teststand = "2023.1.0"
```

```bash
# Add all dependencies
vipm add oglib_array jki_lib_state_machine
vipm add --dev caraya
vipm add --nipm ni-daqmx@24.5.0 --feed ni-daq

# Lock and install
vipm lock
vipm install

# Generate SBOM including both VIPM and NI packages
vipm sbom vipm.toml \
  --format cyclonedx \
  --schema-version 1.5 \
  --product-name "Instrument Control" \
  --product-version 1.0.0 \
  --output build/bom.json
```

--8<-- "need-help.md"
