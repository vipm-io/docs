title: Command Reference

# VIPM CLI Command Reference

Use this page to look up syntax, options, and common workflows for the most frequently used VIPM CLI commands. For additional details, remember that `vipm help` lists every command and `vipm <command> --help` prints the authoritative help text for a single command.

## Global Options

These flags are available on every command unless noted otherwise:

| Option | Description |
|--------|-------------|
| `--refresh` | Forces a package-list refresh before the command runs. Helpful when automation needs the latest repository metadata. |
| `--labview-version <YYYY>` | Targets a specific LabVIEW year (e.g., `2025`). Combine with `--labview-bitness` when multiple bitnesses exist. |
| `--labview-bitness <32|64>` | Specifies 32-bit or 64-bit LabVIEW when both are installed for the same year. Only meaningful with `--labview-version`. |
| `--color-mode <auto|always|never>` | Controls CLI color output (defaults to `auto`). |
| `-h`, `--help` | Shows help for the current command. |

Unless a command states otherwise, it returns exit code `0` on success and a non-zero value on failure (check your automation scripts for non-zero exits).

## Command Quick Look

| Command | Summary |
|---------|---------|
| [`vipm install`](#vipm-install) | Install packages, `.vipc`, `.vip`, `.ogp`, or `.dragon` files. |
| [`vipm uninstall`](#vipm-uninstall) | Remove packages from the selected LabVIEW installation. |
| [`vipm list`](#vipm-list) | List installed packages or inspect a `.vipc`/`.dragon` file. |
| [`vipm package-list-refresh`](#vipm-package-list-refresh) | Refresh repository metadata (legacy command, still supported). |
| [`vipm activate`](#vipm-activate) | Activate VIPM Pro using a serial number, name, and email. |
| [`vipm build`](#vipm-build) | Build packages from `.vipb` specs or LabVIEW project build specs. |
| [`vipm version`](#vipm-version) | Output the CLI and Desktop version numbers. |
| [`vipm about`](#vipm-about) | Print installation details (paths, versions). |

## `vipm install`

Installs one or more packages by name, name@version, or file path.

### Syntax

```bash
vipm install [OPTIONS] <package|path>...
```

### Options

| Option | Description |
|--------|-------------|
| `--upgrade` | If the package is already installed, upgrade it to the latest available version. |

### Examples

Install a single package:

```bash
vipm install oglib_boolean
```

Install multiple packages and upgrade existing ones:

```bash
vipm install --upgrade oglib_boolean oglib_numeric
```

Apply a configuration file:

```bash
vipm install project.vipc
```

Expected output includes progress such as:

```
Installing 2 packages
✓ Installed 2 packages from LabVIEW 2025 (64-bit) in 28.5s
```

### Common Issues

- **Package not found**: Run `vipm package-list-refresh` and verify the package ID at [vipm.io](https://www.vipm.io).
- **Wrong LabVIEW version**: Specify `--labview-version` and `--labview-bitness` to target the correct environment.

## `vipm uninstall`

Removes packages from the selected LabVIEW installation.

### Syntax

```bash
vipm uninstall <package|package@version>...
```

### Examples

```bash
vipm uninstall oglib_boolean
```

Expected output:

```
Uninstalling 1 package
✓ Uninstalled 1 package from LabVIEW 2025 (64-bit)
```

### Common Issues

- **Package in use**: Close LabVIEW or stop any process locking the files before uninstalling.
- **Multiple LabVIEW versions**: Provide `--labview-version` if the package exists in more than one installation.

## `vipm list`

Lists packages from the installed LabVIEW environment or from a `.vipc` / `.dragon` file.

### Syntax

```bash
vipm list [OPTIONS] [path/to/project.vipc]
```

### Options

| Option | Description |
|--------|-------------|
| `--installed` | Show every package installed in the active LabVIEW version. |

### Examples

List installed packages:

```bash
vipm list --installed
```

Inspect a configuration file:

```bash
vipm list project.vipc
```

Expected output:

```
Listing installed packages
Found 4 packages:
  OpenG Boolean Library (oglib_boolean v6.0.0.9)
```

## `vipm search`

Searches the VIPM repositories for packages by name or description.

### Syntax

```bash
vipm search [OPTIONS] <search terms>
```

### Options

| Option | Description |
|--------|-------------|
| `--limit <N>` | Limits the number of search results (defaults to 10). |

### Examples

Search for OpenG packages:

```bash
vipm search openg --limit 5
```

Sample output:

```
Showing 5 packages matching "openg":
  OpenG Array Library (oglib_array v6.0.0.9)
  ...
```

### Tips

- Combine multiple terms (e.g., `vipm search serial communication`) to narrow results.
- Append `--refresh` to ensure the latest catalog data before searching in CI.

## `vipm package-list-refresh`

Legacy command that refreshes VIPM's cached repository metadata. Still widely used in scripts.

### Syntax

```bash
vipm package-list-refresh [OPTIONS]
```

### Options

| Option | Description |
|--------|-------------|
| `--timeout <seconds>` | Set how long VIPM waits for the refresh to finish (`-1` waits indefinitely). |
| `--lv-version <YY.0>` | Old-style LabVIEW version selector (prefer `--labview-version`). |
| `--show-progress` | Display a progress bar. |

### Example

```bash
vipm package-list-refresh
```

Expected output:

```
✓ Package list refreshed successfully
```

### Common Issues

- **Corporate proxy**: Configure `http_proxy` / `https_proxy` environment variables before running.
- **Offline environments**: Mirror the repository internally and point VIPM to the local server.

## `vipm activate`

Activates VIPM Pro. Legacy scripts may use `vipm vipm-activate`; both map to the same functionality.

### Syntax

```bash
vipm activate \
  --serial-number "SERIAL" \
  --name "Full Name" \
  --email "you@example.com"
```

Any argument omitted on interactive terminals will trigger a prompt.

### Example Output

```
✓ Activation succeeded!
```

### Common Issues

- Ensure the serial number is valid and not already in use elsewhere.
- The name and email must exactly match the VIPM account tied to the serial number.

## `vipm build`

Builds packages or other project artifacts from `.vipb` or `.lvproj` build specifications.

### Syntax

```bash
vipm build [OPTIONS] path/to/spec.vipb
```

For LabVIEW project builds:

```bash
vipm build \
  --lvproj-spec "My Build" \
  --lvproj-target "My Computer" \
  path/to/project.lvproj
```

### Options

| Option | Description |
|--------|-------------|
| `--lvproj-spec <name>` | Name of the LabVIEW project build spec to run when using `.lvproj`. |
| `--lvproj-target <name>` | LabVIEW project target (defaults to `My Computer`). |

### Example Output

```
Building VI Package from path/to/your_package.vipb
✓ Build completed: builds/your_package.vip
```

### Common Issues

- **Linux build limitations**: Review the [VIPM Preview docs](../preview.md) for current platform support notes.
- **Missing dependencies**: Run `vipm install project.vipc` before invoking `vipm build` in CI.

## `vipm version`

Prints the VIPM CLI and Desktop versions. Useful for support tickets and automation logs.

```bash
vipm version
```

Sample output:

```
VIPM CLI version 2025.3.0
VIPM Desktop version 2025.3.0
```

## `vipm about`

Shows installation information such as install paths and license data.

```bash
vipm about
```

Use `vipm about --help` to review the latest options.

## Related Resources

- [Getting Started](getting-started.md)
- [Docker and Containers](docker.md)
- [GitHub Actions and CI/CD](github-actions.md)
- Project plan: `dev-docs/cli-docs-improvement-proposal.md`
