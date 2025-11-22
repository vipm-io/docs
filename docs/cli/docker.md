title: Docker Containers

# Using VIPM in Docker Containers

VIPM can be used in Docker containers to manage LabVIEW packages in containerized environments. This is particularly useful for CI/CD pipelines, automated testing, and reproducible builds.

## Overview

VIPM works with NI's official LabVIEW container images, allowing you to:

- Install and manage VI packages in containerized LabVIEW environments
- Automate package installation in CI/CD pipelines
- Create reproducible build environments
- Build VI packages in containers

### Related Topics

- [VIPM CLI Overview](index.md) — feature summary and example commands
- [GitHub Actions and CI/CD](github-actions.md) — integrate container workflows into automation

## Docker Examples Repository

For complete working examples, see the [examples-vipm-docker](https://github.com/vipm-io/examples-vipm-docker) repository, which contains:

- Docker configuration files
- Environment setup examples
- Step-by-step guides for common scenarios

## Using NI's Official LabVIEW Container

NI provides official LabVIEW container images that work with VIPM:

- [LabVIEW on Docker Hub](https://hub.docker.com/r/nationalinstruments/labview)
- [LabVIEW for Containers on GitHub](https://github.com/ni/labview-for-containers)

### Basic Setup

A typical Docker setup for VIPM includes:

1. **Dockerfile** - Defines your container configuration based on NI's LabVIEW image
2. **docker-compose.yml** - Orchestrates container setup and configuration
3. **.env file** - Stores environment variables (VIPM serial number, etc.)

Example `.env` file:

```bash
VIPM_SERIAL_NUMBER=your-serial-number-here
VIPM_FULL_NAME=Your Full Name
VIPM_EMAIL=your.email@example.com
```

### Running the Container

Build and run your container:

```bash
docker compose run --rm vipm-labview
```

## VIPM CLI Commands in Containers

Once inside a running container, you can use VIPM CLI commands to manage packages.

### Activate VIPM

Currently, using VIPM inside containers requires activating VIPM Pro. Support for VIPM Community Edition and VIPM Free Edition is being worked on.

```bash
vipm vipm-activate --serial-number "$VIPM_SERIAL_NUMBER" --name "$VIPM_FULL_NAME" --email "$VIPM_EMAIL"
```

Expected output:
```
✓ Activation succeeded!
```

### Refresh Package List

Refresh VIPM's package metadata from the vipm.io community repository:

```bash
vipm package-list-refresh
```

Expected output:
```
✓ Package list refreshed successfully
```

### List Installed Packages

Check which packages are installed in LabVIEW:

```bash
vipm list --installed
```

Expected output:
```
Listing installed packages
Auto-detected LabVIEW 2025 (64-bit)
Found 0 packages:
```

**Note**: If you have multiple LabVIEW versions installed, specify the version using `--labview-version`.

### Install a Package

Install a single package:

```bash
vipm install oglib_boolean
```

Expected output:
```
Installing 1 package
Auto-detected LabVIEW 2025 (64-bit)
install: 100 (1/1; 100%) - Installation complete
✓ Installed 1 package from LabVIEW 2025 (64-bit) in 23.5s
Successfully installed 1 package:
  OpenG Boolean Library (oglib_boolean v6.0.0.9)
```

### Install Multiple Packages

Install multiple packages in one command:

```bash
vipm install oglib_boolean oglib_numeric
```

Expected output:
```
Installing 2 packages
Auto-detected LabVIEW 2025 (64-bit)
install: 100 (1/1; 100%) - Installation complete
✓ Installed 2 packages from LabVIEW 2025 (64-bit) in 28.5s
Successfully installed 2 packages:
  OpenG Boolean Library (oglib_boolean v6.0.0.9)
  OpenG Numeric Library (oglib_numeric v6.0.0.9)
```

### Install from VI Package Configuration File

Use a `.vipc` file to install all project dependencies:

```bash
vipm install path/to/project.vipc
```

Expected output:
```
Installing packages from configuration file project.vipc
✓ Installed N packages ...
```

### Uninstall a Package

Remove an installed package:

```bash
vipm uninstall oglib_boolean
```

Expected output:
```
Uninstalling 1 package
Auto-detected LabVIEW 2025 (64-bit)
validate: 100 (1/1; 100%) - Validation complete
Uninstalling oglib_boolean v6.0.0.9...
uninstall: 100 (1/1; 100%) - Uninstall complete
✓ Uninstalled 1 package from LabVIEW 2025 (64-bit) in 10.3s
Successfully uninstalled 1 package:
  OpenG Boolean Library (oglib_boolean v6.0.0.9)
```

### Verify Installation

You can verify package installation by checking the LabVIEW directory. For example, OpenG packages are installed in:

```bash
ls -al /usr/local/natinst/LabVIEW-2025-64/user.lib/_OpenG.lib
```

Expected output:
```
total 16
drwxr-xr-x 4 root root 4096 Nov 11 21:19 .
drwxr-xr-x 1 root root 4096 Nov 11 21:19 ..
drwxr-xr-x 3 root root 4096 Nov 11 21:19 boolean
drwxr-xr-x 3 root root 4096 Nov 11 21:19 numeric
```

## Building VI Packages in Containers

You can build VI packages from `.vipb` build specifications:

```bash
vipm build path/to/your_package.vipb
```

Expected output:
```
Building VI Package from path/to/your_package.vipb
✓ Build completed: builds/your_package.vip
```

**Note**: Package building on Linux is currently under development and may have some limitations. Check the [VIPM 2026 Q1 Preview](https://docs.vipm.io/preview/) for the latest updates.

## Use Cases for Containers

Using VIPM in containers is ideal for:

- **CI/CD Pipelines**: Automate package installation and testing in GitHub Actions, GitLab CI, etc.
- **Reproducible Builds**: Ensure consistent package versions across development environments
- **Automated Testing**: Run LabVIEW tests with specific package dependencies
- **Development Environments**: Share consistent development environments across teams

## Additional Resources

- [VIPM Docker Examples Repository](https://github.com/vipm-io/examples-vipm-docker)
- [NI LabVIEW Docker Hub](https://hub.docker.com/r/nationalinstruments/labview)
- [LabVIEW for Containers GitHub](https://github.com/ni/labview-for-containers)
- [GitHub Actions and CI/CD Guide](github-actions.md)
