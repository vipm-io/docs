title: Overview

# Using VIPM via Command-Line Interface (CLI)

VIPM includes a powerful command-line interface (CLI) that enables automation, integration with CI/CD pipelines, and usage in containerized environments.

## CLI Features

The VIPM CLI provides commands for:

- **Package Management**: Install, uninstall, and list VI packages
- **Package Building**: Build VI packages from `.vipb` build specifications
- **Activation**: Activate VIPM Pro licenses
- **Repository Management**: Refresh package lists from repositories

## Use Cases

The VIPM CLI is particularly useful for:

- **Continuous Integration/Continuous Deployment (CI/CD)**: Automate package installation and builds in GitHub Actions, GitLab CI, or other CI/CD platforms
- **Docker Containers**: Use VIPM in containerized LabVIEW environments
- **Automation Scripts**: Create scripts to manage LabVIEW dependencies and build processes
- **Headless Environments**: Work with VIPM on systems without a graphical interface

## Topics

Explore the following topics to learn more about using VIPM CLI:

- [Getting Started](getting-started.md) - Step-by-step guide for your first commands
- [Docker and Containers](docker.md) - Learn how to use VIPM in Docker containers with LabVIEW
- [GitHub Actions and CI/CD](github-actions.md) - Integrate VIPM into your CI/CD workflows

## Example Commands

Use these quick snippets to verify your environment. For full syntax, options, exit codes, and troubleshooting tips, see the upcoming command reference (Phase 2).

### Activate VIPM Pro

```bash
vipm vipm-activate \
	--serial-number "YOUR-SERIAL" \
	--name "Your Name" \
	--email "your@email.com"
```

Expected output:

```
✓ Activation succeeded!
```

### Refresh Package List

```bash
vipm package-list-refresh
```

Expected output:

```
✓ Package list refreshed successfully
```

### Install a Single Package

```bash
vipm install oglib_boolean
```

Expected output:

```
Installing 1 package
✓ Installed 1 package ...
```

### Install Multiple Packages

```bash
vipm install oglib_boolean oglib_numeric
```

Expected output:

```
Installing 2 packages
✓ Installed 2 packages ...
```

### Install from a VI Package Configuration File

```bash
vipm install path/to/project.vipc
```

Typical outcome: VIPM installs every dependency specified in the configuration file and reports any missing packages before exiting.

### List Installed Packages

```bash
vipm list --installed
```

Expected output:

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

To start using VIPM CLI, ensure you have VIPM installed on your system. The CLI is included with all editions of VIPM.

For detailed examples and use cases, check out the topic pages listed above.

## Next Steps

- First time using the CLI? Follow the [Getting Started guide](getting-started.md).
- Ready for containers? Head to [Docker and Containers](docker.md) for environment setup tips.
- Automating builds? Explore [GitHub Actions and CI/CD](github-actions.md) for workflow samples.
