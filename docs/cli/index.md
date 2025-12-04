title: Overview

# Using VIPM via Command-Line Interface (CLI)

--8<-- "preview-available.md"

VIPM includes a powerful command-line interface (CLI) that enables automation, integration with CI/CD pipelines, and usage in containerized environments.

## Example Commands

Use these quick snippets to verify your environment, then jump to the [CLI Command Reference](command-reference.md) for full syntax, options, exit codes, and troubleshooting tips.

```bash
# Activate VIPM Pro (optional)


# Refresh package list so installs see the latest metadata
vipm package-list-refresh

# Install packages by name or from a .vipc file
vipm install oglib_boolean oglib_numeric
vipm install path/to/project.vipc

# Inspect installed packages or files
vipm list --installed
vipm list project.vipc

# Build a VI package (requires .vipb or .lvproj)
```
```
Listing installed packages
Found <n> packages:
	<Package Name> (<id> vX.Y.Z)
```

### Uninstall a Package

```bash
vipm uninstall oglib_boolean
```

Expected output:

```
Uninstalling 1 package
✓ Uninstalled 1 package ...
```

### Build a VI Package

```bash
vipm build path/to/package.vipb
```

Typical outcome: VIPM validates the build specification, produces a `.vip` artifact, and reports the output location.

## Getting Started

To start using VIPM CLI, ensure you have VIPM installed on your system. The CLI ships with every edition of VIPM Desktop.

Next, walk through the [Getting Started guide](getting-started.md) for first-run verification, then dive into [Docker](docker.md) or [GitHub Actions](github-actions.md) when you need environment-specific workflows.

## Next Steps

- First time using the CLI? Follow the [Getting Started guide](getting-started.md).
- Ready for containers? Head to [Docker and Containers](docker.md) for environment setup tips.
- Automating builds? Explore [GitHub Actions and CI/CD](github-actions.md) for workflow samples.

--8<-- "need-help.md"