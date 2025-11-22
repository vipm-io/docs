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

- [Docker and Containers](docker.md) - Learn how to use VIPM in Docker containers with LabVIEW
- [GitHub Actions and CI/CD](github-actions.md) - Integrate VIPM into your CI/CD workflows

## Example Commands

Here are some common VIPM CLI commands:

```bash
# Activate VIPM Pro
vipm vipm-activate --serial-number "YOUR-SERIAL" --name "Your Name" --email "your@email.com"

# Refresh package list
vipm package-list-refresh

# Install a package
vipm install oglib_boolean

# Install multiple packages
vipm install oglib_boolean oglib_numeric

# Install from a VI Package Configuration file
vipm install path/to/project.vipc

# List installed packages
vipm list --installed

# Uninstall a package
vipm uninstall oglib_boolean

# Build a VI package
vipm build path/to/package.vipb
```

## Getting Started

To start using VIPM CLI, ensure you have VIPM installed on your system. The CLI is included with all editions of VIPM.

For detailed examples and use cases, check out the topic pages listed above.
