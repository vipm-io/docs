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
# VIPM Pro activation credentials
VIPM_SERIAL_NUMBER=your-serial-number-here
VIPM_FULL_NAME=Your Full Name
VIPM_EMAIL=your.email@example.com

# Non-interactive mode: auto-confirm prompts and error on missing params
# (recommended for Docker/CI — prevents commands from hanging)
VIPM_NONINTERACTIVE=1

# Disable colored output for cleaner CI logs
NO_COLOR=1
```

See [Environment Variables](environment-variables.md) for the full list and [GitHub Actions and CI/CD](github-actions.md) for workflow examples.

### Running the Container

Build and run your container:

```bash
docker compose run --rm vipm-labview
```

## Display and LabVIEW Setup (Linux Containers)

!!! important "Display setup required before VIPM commands (Linux only)"
    On Linux containers, VIPM commands that interact with LabVIEW need a running display server. Create a `setup-display.sh` script and source it before running `vipm` commands:

        #!/bin/bash
        TARGET_DISPLAY=:99
        export DISPLAY="$TARGET_DISPLAY"
        if ! pgrep -x Xvfb > /dev/null; then
            Xvfb "$TARGET_DISPLAY" -screen 0 1280x720x24 -ac +extension GLX +render -noreset \
                > /tmp/xvfb.log 2>&1 &
        fi
        # Without this marker file the LabVIEW Runtime Engine may not start properly.
        mkdir -p /tmp/natinst && echo "1" > /tmp/natinst/LVContainer.txt
        echo "$(pgrep -x Xvfb > /dev/null && echo "Xvfb running (DISPLAY=$TARGET_DISPLAY)" || echo "WARNING: Xvfb is required by vipm, but failed to start; DISPLAY=$DISPLAY may not work. Check /tmp/xvfb.log for details.")"

!!! important "Launch LabVIEW in headless mode before install/build commands (Linux only)"
    Commands that install or build packages need LabVIEW running in the background. Launch it non-blocking with the `--headless` flag:

        /usr/local/natinst/LabVIEW-${LABVIEW_VERSION_YEAR}-64/labview --headless &

    The trailing `&` runs it in the background so the shell continues to the `vipm` command.

!!! tip "Headless LabVIEW"
    The `--headless` flag prevents LabVIEW from opening a GUI and works on both Windows and Linux. It should be used in any CI/CD or containerized workflow. See [Headless LabVIEW](https://github.com/ni/labview-for-containers/blob/main/docs/headless-labview.md) for details.

!!! note "LabVIEW containers are new"
    The official NI LabVIEW container images and the tooling around them are still maturing. JKI and NI are actively polishing the rough edges — expect these setup steps to simplify over time.

## VIPM CLI Commands in Containers

Once inside a running container, use the same CLI commands described in the [CLI Command Reference](command-reference.md). The examples below highlight container-specific considerations:

- **Activate VIPM Pro** (required today). Use environment variables from your `.env` file:

  ```bash
  vipm activate --serial-number "$VIPM_SERIAL_NUMBER" --name "$VIPM_FULL_NAME" --email "$VIPM_EMAIL"
  ```

- **Refresh package sources** before every install to avoid stale caches when containers are rebuilt frequently:

  ```bash
  vipm refresh
  ```

- **Install packages or `.vipc` files`** just like on desktop. If you have multiple LabVIEW versions in the container image, pair your command with `--labview-version` (and `--labview-bitness` when needed).

  ```bash
  vipm install -y oglib_boolean
  vipm install -y project.vipc
  ```

- **List/verify installations** to confirm the container state before running builds or tests:

  ```bash
  vipm list --installed
  ls -al /usr/local/natinst/LabVIEW-2025-64/user.lib/_OpenG.lib
  ```

> 💡 Because containers are often ephemeral, script these commands in your Docker entrypoint or CI workflow so every run activates, refreshes, installs, and verifies automatically.

!!! tip "No extra configuration needed in CI"
    When running inside a CI system (GitHub Actions, GitLab CI, etc.), VIPM auto-detects the environment and enables non-interactive mode. For standalone Docker usage outside CI, set `VIPM_NONINTERACTIVE=1` in your `.env` file to prevent commands from hanging on missing input. See [Environment Variables](environment-variables.md) for details.

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
