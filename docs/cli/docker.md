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

Once inside a running container, use the same CLI commands described in the [CLI Command Reference](command-reference.md). The examples below highlight container-specific considerations:

- **Activate VIPM Pro** (required today). Use environment variables from your `.env` file:

  ```bash
  vipm activate --serial-number "$VIPM_SERIAL_NUMBER" --name "$VIPM_FULL_NAME" --email "$VIPM_EMAIL"
  ```

- **Refresh metadata** before every install to avoid stale caches when containers are rebuilt frequently:

  ```bash
  vipm package-list-refresh
  ```

- **Install packages or `.vipc` files`** just like on desktop. If you have multiple LabVIEW versions in the container image, pair your command with `--labview-version` (and `--labview-bitness` when needed).

  ```bash
  vipm install oglib_boolean
  vipm install project.vipc
  ```

- **List/verify installations** to confirm the container state before running builds or tests:

  ```bash
  vipm list --installed
  ls -al /usr/local/natinst/LabVIEW-2025-64/user.lib/_OpenG.lib
  ```

> 💡 Because containers are often ephemeral, script these commands in your Docker entrypoint or CI workflow so every run activates, refreshes, installs, and verifies automatically.

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
- [CLI Command Reference](command-reference.md)
