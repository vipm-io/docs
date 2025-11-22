title: Getting Started

# Getting Started with the VIPM CLI

This guide walks you through verifying your VIPM installation, running your first CLI commands, and learning where to go next. It assumes you already have VIPM Desktop installed on Windows, macOS, or Linux. If you need installation help, start with the platform-specific instructions in the main VIPM docs.

## Prerequisites

- VIPM Desktop installed (Community, Free, or Pro) with CLI support
- LabVIEW installed, or container image that includes LabVIEW + VIPM
- Terminal or shell access (PowerShell, Command Prompt, bash, etc.)
- Optional: VIPM Pro serial number if you need to activate Pro-only features

## Step 1 — Verify VIPM CLI Access

Run `vipm --version` to confirm the CLI is available and on your `PATH`.

```bash
vipm --version
```

Expected output:

```
VIPM CLI version X.Y.Z
```

If you see "command not found," add the VIPM installation directory to your PATH or open the VIPM terminal shortcut installed with VIPM.

Tip: `vipm help` prints the global command list, and `vipm <command> --help` shows authoritative syntax, options, and examples for each command.

## Step 2 — (Optional) Activate VIPM Pro

If you need Pro features (building packages, scripting, etc.), activate once per machine:

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

Skip this step if you are using Community/Free features only.

## Step 3 — Refresh Package Metadata

Pull the latest package list so that installs succeed on the first try:

```bash
vipm package-list-refresh
```

Expected output:

```
✓ Package list refreshed successfully
```

Behind a proxy or on a restricted network? Configure proxy environment variables before running this command, or plan to sync from an internal VIPM repository.

## Step 4 — Install Your First Package

Install a well-known package (replace with your preferred package ID). Use `--labview-version` if you have multiple versions installed.

```bash
vipm install oglib_boolean
```

Expected output (truncated):

```
Installing 1 package
✓ Installed 1 package ...
```

To install everything defined in a `.vipc` configuration:

```bash
vipm install path/to/project.vipc
```

If a package cannot be found, rerun `vipm package-list-refresh` and verify the package name on [vipm.io](https://www.vipm.io) or in your `.vipc` file.

## Step 5 — List Installed Packages

Confirm what VIPM just installed:

```bash
vipm list --installed
```

Expected output:

```
Listing installed packages
Found <n> packages:
  OpenG Boolean Library (oglib_boolean v6.0.0.9)
```

Add `--labview-version` to focus on a specific LabVIEW release if you have more than one.

## Step 6 — Where to Go Next

- Need container guidance? Continue to [Docker and Containers](docker.md).
- Automating CI builds? Jump to [GitHub Actions and CI/CD](github-actions.md).
- Looking for command syntax, options, and exit codes? See the upcoming [CLI Command Reference](command-reference.md) once published.
- Troubleshooting installs? Refer to the (planned) `docs/cli/troubleshooting.md` page or the main [troubleshooting index](../troubleshooting/index.md).

## Quick Troubleshooting Tips

- **CLI not found**: Use the VIPM terminal shortcut installed with VIPM or add the install directory (for example, `C:/Program Files/JKI/VIPM` or `/usr/local/jki/vipm`) to your PATH.
- **Activation fails**: Confirm the serial number, name, and email match your VIPM account exactly; rerun `vipm vipm-activate` after updating secrets or environment variables.
- **Package install fails**: Refresh metadata (`vipm package-list-refresh`) and double-check the package ID; add `--labview-version` when multiple LabVIEW versions are installed.
- **Network issues**: Configure proxy variables (`http_proxy`, `https_proxy`) or use an internal repository mirror if the build machine cannot reach `vipm.io`.

## Notes for Contributors

This file currently serves as the quick-start outline. As the new command reference and troubleshooting docs come online, tighten each step to cross-reference those pages and keep duplication minimal.
