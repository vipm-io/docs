# Using VIPM in GitHub Actions and CI/CD

VIPM's command-line interface enables seamless integration with CI/CD platforms like GitHub Actions, enabling automated package management, building, and testing of LabVIEW projects.

## Overview

Using VIPM in CI/CD pipelines allows you to:

- Automatically install package dependencies before running tests
- Build VI packages as part of your release process
- Validate package installations in different LabVIEW versions
- Ensure reproducible builds with consistent package versions

## GitHub Actions Integration

### Prerequisites

To use VIPM in GitHub Actions, you'll need:

1. A GitHub repository with your LabVIEW project
2. VIPM Pro serial number (store as GitHub secret)
3. A workflow configuration file (`.github/workflows/`)

### Setting Up GitHub Secrets

Store your VIPM Pro credentials as GitHub repository secrets:

1. Go to your repository → Settings → Secrets and variables → Actions
2. Add the following secrets:
   - `VIPM_SERIAL_NUMBER`: Your VIPM Pro serial number
   - `VIPM_FULL_NAME`: Your full name (as registered)
   - `VIPM_EMAIL`: Your email address (as registered)

You can find your VIPM Pro serial number on the [VIPM account page](https://www.vipm.io/account/).

### Basic Workflow Example

Create a file at `.github/workflows/vipm-ci.yml`:

```yaml
name: VIPM CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  install-packages:
    runs-on: ubuntu-latest
    
    container:
      image: nationalinstruments/labview:latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Install VIPM
        run: |
          wget -O /tmp/vipm.deb https://packages.jki.net/vipm/preview/vipm_latest_preview_amd64.deb
          sudo dpkg -i /tmp/vipm.deb
          rm /tmp/vipm.deb
      
      - name: Activate VIPM
        run: |
          vipm vipm-activate \
            --serial-number "${{ secrets.VIPM_SERIAL_NUMBER }}" \
            --name "${{ secrets.VIPM_FULL_NAME }}" \
            --email "${{ secrets.VIPM_EMAIL }}"
      
      - name: Refresh package list
        run: vipm package-list-refresh
      
      - name: Install project dependencies
        run: vipm install project.vipc
      
      - name: List installed packages
        run: vipm list --installed
```

### Installing Specific Packages

To install specific packages instead of using a `.vipc` file:

```yaml
- name: Install required packages
  run: |
    vipm install oglib_boolean
    vipm install oglib_numeric
    vipm install jki_lib_state_machine
```

### Building VI Packages

To build VI packages as part of your CI pipeline:

```yaml
- name: Build VI Package
  run: vipm build source/MyPackage.vipb

- name: Upload built package
  uses: actions/upload-artifact@v4
  with:
    name: vi-package
    path: builds/*.vip
```

## Common Workflow Patterns

### Complete Build and Test Workflow

```yaml
name: Build and Test

on: [push, pull_request]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    container:
      image: nationalinstruments/labview:latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Install VIPM
        run: |
          wget -O /tmp/vipm.deb https://packages.jki.net/vipm/preview/vipm_latest_preview_amd64.deb
          sudo dpkg -i /tmp/vipm.deb
          rm /tmp/vipm.deb
      
      - name: Activate VIPM
        run: |
          vipm vipm-activate \
            --serial-number "${{ secrets.VIPM_SERIAL_NUMBER }}" \
            --name "${{ secrets.VIPM_FULL_NAME }}" \
            --email "${{ secrets.VIPM_EMAIL }}"
      
      - name: Refresh package list
        run: vipm package-list-refresh
      
      - name: Install dependencies
        run: vipm install project.vipc
      
      - name: Build project
        run: |
          # Add your LabVIEW build commands here
          echo "Building LabVIEW project..."
      
      - name: Run tests
        run: |
          # Add your test commands here
          echo "Running tests..."
      
      - name: List installed packages
        if: always()
        run: vipm list --installed
```

### Release Workflow

```yaml
name: Release

on:
  release:
    types: [created]

jobs:
  build-package:
    runs-on: ubuntu-latest
    container:
      image: nationalinstruments/labview:latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Install VIPM
        run: |
          wget -O /tmp/vipm.deb https://packages.jki.net/vipm/preview/vipm_latest_preview_amd64.deb
          sudo dpkg -i /tmp/vipm.deb
          rm /tmp/vipm.deb
      
      - name: Activate VIPM
        run: |
          vipm vipm-activate \
            --serial-number "${{ secrets.VIPM_SERIAL_NUMBER }}" \
            --name "${{ secrets.VIPM_FULL_NAME }}" \
            --email "${{ secrets.VIPM_EMAIL }}"
      
      - name: Build VI Package
        run: vipm build source/MyPackage.vipb
      
      - name: Upload to Release
        run: gh release upload ${{ github.event.release.tag_name }} builds/*.vip
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Troubleshooting

### VIPM Activation Issues

If activation fails in CI:
- Verify secrets are correctly set in repository settings
- Ensure the serial number is valid and not expired
- Check that the name and email match your VIPM account

### Package Installation Failures

If package installation fails:
- Run `vipm package-list-refresh` before installing packages
- Check that package names are correct (case-sensitive)
- Verify LabVIEW version compatibility

### Container Issues

If the container doesn't start or VIPM is not found:
- Ensure you're using the correct container image
- Verify the container has VIPM installed
- Check container logs for errors

## Examples Repository

For complete working examples, visit:

- [VIPM Docker Examples](https://github.com/vipm-io/examples-vipm-docker) - Contains Docker and CI/CD configuration examples

## Additional Resources

- [Docker and Containers Guide](docker.md)
- [VIPM CLI Reference](index.md)
- [NI LabVIEW for Containers](https://github.com/ni/labview-for-containers)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
