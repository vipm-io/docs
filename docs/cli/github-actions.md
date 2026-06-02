# GitHub Actions and CI/CD

VIPM's command-line interface enables seamless integration with CI/CD platforms like GitHub Actions, enabling automated package management, building, and testing of LabVIEW projects.

## Overview

Using VIPM in CI/CD pipelines allows you to:

- Automatically install package dependencies before running tests
- Build VI packages as part of your release process
- Validate package installations in different LabVIEW versions
- Ensure reproducible builds with consistent package versions

Need full command syntax while building workflows? Refer to the [CLI Command Reference](command-reference.md).

### Related Topics

- [VIPM CLI Overview](index.md) — general CLI concepts and sample commands
- [Docker and Containers Guide](docker.md) — containerized LabVIEW environments for CI runners

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

!!! tip "Prompts are auto-disabled in CI"
    VIPM automatically detects CI environments like GitHub Actions and enables non-interactive mode — confirmation prompts are auto-accepted and missing parameters cause immediate errors instead of hanging. No extra configuration is needed. You can also use the `-y` flag or `VIPM_ASSUME_YES=1` for explicit control. See [Environment Variables](environment-variables.md) for details.

!!! note "LabVIEW containers are new"
    The official NI LabVIEW container images and the tooling around them are still maturing. JKI and NI are actively polishing the rough edges — expect the setup steps (Xvfb, display configuration, runtime markers) to simplify over time.

!!! important "Display setup required for every step (Linux containers)"
    VIPM commands that interact with LabVIEW need a running display server on Linux. In GitHub Actions containers, processes don't survive between steps, so the display must be re-established at the top of every step that uses `vipm`. The workflow examples below include a step that writes `setup-display.sh` at the top of the job, then each subsequent step sources it.

!!! important "Launch LabVIEW in headless mode before install/build steps (Linux containers)"
    Steps that install or build packages need LabVIEW running in the background. Launch it non-blocking with the `--headless` flag before any `vipm` command that interacts with LabVIEW:

        /usr/local/natinst/LabVIEW-${LABVIEW_VERSION_YEAR}-64/labview --headless &

    The trailing `&` runs it in the background so the step continues to the `vipm` command.

!!! tip "Headless LabVIEW"
    The `--headless` flag prevents LabVIEW from opening a GUI and works on both Windows and Linux. It should be used in any CI/CD or containerized workflow. See [Headless LabVIEW](https://github.com/ni/labview-for-containers/blob/main/docs/headless-labview.md) for details.

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
      image: nationalinstruments/labview:2026q1patch2-linux
    
    env:
      LABVIEW_VERSION_YEAR: "2026"
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Create display setup script
        run: |
          cat > setup-display.sh << 'EOF'
          TARGET_DISPLAY=:99
          export DISPLAY="$TARGET_DISPLAY"
          if ! pgrep -x Xvfb > /dev/null; then
              Xvfb "$TARGET_DISPLAY" -screen 0 1280x720x24 -ac +extension GLX +render -noreset \
                  > /tmp/xvfb.log 2>&1 &
          fi
          # Without this marker file the LabVIEW Runtime Engine may not start properly.
          mkdir -p /tmp/natinst && echo "1" > /tmp/natinst/LVContainer.txt
          echo "$(pgrep -x Xvfb > /dev/null && echo "Xvfb running (DISPLAY=$TARGET_DISPLAY)" || echo "WARNING: Xvfb is required by vipm, but failed to start; DISPLAY=$DISPLAY may not work. Check /tmp/xvfb.log for details.")"
          EOF
      
      - name: Install VIPM
        run: |
          wget -O /tmp/vipm.deb https://packages.jki.net/vipm/preview/vipm_latest_preview_amd64.deb
          sudo dpkg -i /tmp/vipm.deb
          rm /tmp/vipm.deb
      
      - name: Activate VIPM
        run: |
          source setup-display.sh
          vipm activate \
            --serial-number "${{ secrets.VIPM_SERIAL_NUMBER }}" \
            --name "${{ secrets.VIPM_FULL_NAME }}" \
            --email "${{ secrets.VIPM_EMAIL }}"
      
      - name: Refresh package sources
        run: |
          source setup-display.sh
          vipm refresh
      
      - name: Install project dependencies
        run: |
          source setup-display.sh
          /usr/local/natinst/LabVIEW-${LABVIEW_VERSION_YEAR}-64/labview --headless &
          vipm install -y project.vipc
      
      - name: List installed packages
        run: |
          source setup-display.sh
          vipm list --installed
```

### Installing Specific Packages

To install specific packages instead of using a `.vipc` file:

```yaml
- name: Install required packages
  run: |
    vipm install -y \
      oglib_boolean \
      oglib_numeric \
      jki_lib_state_machine
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

### Caching VIPM Package Downloads

To speed up builds, cache VIPM's package downloads:

```yaml
- name: Cache VIPM packages
  uses: actions/cache@v4
  with:
    path: |
      /usr/local/natinst/LabVIEW*/
      /usr/local/jki/vipm/cache/
      /usr/local/jki/vipm/db/
    key: ${{ runner.os }}-vipm-${{ hashFiles('project.vipc') }}
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
      image: nationalinstruments/labview:2026q1patch2-linux
    
    env:
      LABVIEW_VERSION_YEAR: "2026"
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Create display setup script
        run: |
          cat > setup-display.sh << 'EOF'
          TARGET_DISPLAY=:99
          export DISPLAY="$TARGET_DISPLAY"
          if ! pgrep -x Xvfb > /dev/null; then
              Xvfb "$TARGET_DISPLAY" -screen 0 1280x720x24 -ac +extension GLX +render -noreset \
                  > /tmp/xvfb.log 2>&1 &
          fi
          mkdir -p /tmp/natinst && echo "1" > /tmp/natinst/LVContainer.txt
          echo "$(pgrep -x Xvfb > /dev/null && echo "Xvfb running (DISPLAY=$TARGET_DISPLAY)" || echo "WARNING: Xvfb is required by vipm, but failed to start; DISPLAY=$DISPLAY may not work. Check /tmp/xvfb.log for details.")"
          EOF
      
      - name: Install VIPM
        run: |
          wget -O /tmp/vipm.deb https://packages.jki.net/vipm/preview/vipm_latest_preview_amd64.deb
          sudo dpkg -i /tmp/vipm.deb
          rm /tmp/vipm.deb
      
      - name: Activate VIPM
        run: |
          source setup-display.sh
          vipm activate \
            --serial-number "${{ secrets.VIPM_SERIAL_NUMBER }}" \
            --name "${{ secrets.VIPM_FULL_NAME }}" \
            --email "${{ secrets.VIPM_EMAIL }}"
      
      - name: Refresh package sources
        run: |
          source setup-display.sh
          vipm refresh
      
      - name: Install dependencies
        run: |
          source setup-display.sh
          /usr/local/natinst/LabVIEW-${LABVIEW_VERSION_YEAR}-64/labview --headless &
          vipm install -y project.vipc
      
      - name: Build project
        run: |
          source setup-display.sh
          /usr/local/natinst/LabVIEW-${LABVIEW_VERSION_YEAR}-64/labview --headless &
          # Add your LabVIEW build commands here
          echo "Building LabVIEW project..."
      
      - name: Run tests
        run: |
          source setup-display.sh
          /usr/local/natinst/LabVIEW-${LABVIEW_VERSION_YEAR}-64/labview --headless &
          # Add your test commands here
          echo "Running tests..."
      
      - name: List installed packages
        if: always()
        run: |
          source setup-display.sh
          vipm list --installed
```

## Troubleshooting

### VIPM Activation Issues

If activation fails in CI:
- Verify secrets are correctly set in repository settings
- Ensure the serial number is valid and not expired
- Check that the name and email match your VIPM account

### Package Installation Failures

If package installation fails:
- Run `vipm refresh` before installing packages
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
- [CLI Command Reference](command-reference.md)
- [NI LabVIEW for Containers](https://github.com/ni/labview-for-containers)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
