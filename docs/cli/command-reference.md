title: Command Reference

# VIPM CLI Command Reference

Use this page to look up syntax, options, and common workflows for the most frequently used VIPM CLI commands. For additional details, remember that `vipm help` lists every command and `vipm <command> --help` prints the authoritative help text for a single command.

!!! info "vipm.toml Commands (Preview)"
    Looking for `vipm init`, `vipm add`, `vipm remove`, `vipm lock`, or `vipm clean`? These commands work with the new `vipm.toml` project configuration format. See the [vipm.toml Getting Started guide](../vipm-toml/getting-started.md) for details. For managing NI packages (NIPM) in vipm.toml, see [NI Packages (NIPM)](../vipm-toml/nipm.md).

## Global Options

These flags are available on every command unless noted otherwise:

| Option | Description |
|--------|-------------|
| `--refresh` | Forces a package-list refresh before the command runs. Helpful when automation needs the latest repository metadata. |
| `--labview-version <YYYY>` | Targets a specific LabVIEW year (e.g., `2025`). Combine with `--labview-bitness` when multiple bitnesses exist. |
| `--labview-bitness <32|64>` | Specifies 32-bit or 64-bit LabVIEW when both are installed for the same year. Only meaningful with `--labview-version`. |
| `--color-mode <auto|always|never>` | Controls CLI color output (defaults to `auto`). |
| `--timeout <seconds>` | How long to wait for the operation to finish. Use `-1` for no timeout. |
| `--show-progress` | Display a progress indicator during long-running operations. |
| `--verbose`, `-v` | Enable verbose output for additional diagnostic detail. |
| `-h`, `--help` | Shows help for the current command. |

Unless a command states otherwise, it returns exit code `0` on success and a non-zero value on failure (check your automation scripts for non-zero exits).

## Command Quick Look

| Command | Summary |
|---------|---------|
| [`vipm install`](#vipm-install) | Install packages, `.vipc`, `.vip`, `.ogp`, or `.dragon` files. |
| [`vipm uninstall`](#vipm-uninstall) | Remove packages from the selected LabVIEW installation. |
| [`vipm list`](#vipm-list) | List installed packages or inspect a `.vipc`/`.dragon` file. |
| [`vipm info`](#vipm-info) | Show metadata and installed files for a package. |
| [`vipm package-list-refresh`](#vipm-package-list-refresh) | Refresh repository metadata (legacy command, still supported). |
| [`vipm activate`](#vipm-activate) | Activate VIPM Pro using a serial number, name, and email. |
| [`vipm build`](#vipm-build) | Build packages from `.vipb` specs or LabVIEW project build specs. |
| [`vipm sbom`](#vipm-sbom) | Generate a CycloneDX SBOM from a project or manifest. |
| [`vipm sync`](#vipm-sync) | Reconcile vipm.toml from a LabVIEW project scan. |
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
| `--dev` | Install dev-dependencies from `vipm.toml`. |
| `--no-dev` | Exclude dev-dependencies when installing from `vipm.toml`. |
| `--yes`, `-y` | Skip confirmation prompts and proceed automatically. Also available as `VIPM_ASSUME_YES=1` env var, or use `VIPM_NONINTERACTIVE=1` to disable all prompts. See [Environment Variables](environment-variables.md). |

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
vipm uninstall [OPTIONS] <package|package@version>...
```

### Options

| Option | Description |
|--------|-------------|
| `--allow-version-mismatch`, `-F`, `--force` | Proceed even if the installed version does not match the requested version. |
| `--yes`, `-y` | Skip confirmation prompts and proceed automatically. Also available as `VIPM_ASSUME_YES=1` env var, or use `VIPM_NONINTERACTIVE=1` to disable all prompts. See [Environment Variables](environment-variables.md). |

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
| `--dev` | Include dev-dependencies when listing from `vipm.toml`. |
| `--no-dev` | Exclude dev-dependencies when listing from `vipm.toml`. |

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

## `vipm info`

Shows metadata for a package, including name, version, description, vendor, and license. Can also list installed files. For managing NI packages in vipm.toml, see [NI Packages (NIPM)](../vipm-toml/nipm.md).

### Syntax

```bash
vipm info [OPTIONS] <package>
```

### Options

| Option | Description |
|--------|-------------|
| `--nipm` | Look up an NI package (NIPM) instead of a VIPM package. |
| `--installed-files` | List all files installed by the package (Professional edition). |

### Examples

Show metadata for a VIPM package:

```bash
vipm info oglib_boolean
```

Show metadata for an NI package:

```bash
vipm info --nipm ni-labview-2025-core --labview-version 2025
```

List installed files for a package:

```bash
vipm info oglib_boolean --installed-files
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

Activates VIPM Pro. Legacy scripts may use `vipm activate`; both map to the same functionality.

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
| `--all` | Build all build specs found in the project. |
| `--version-number <VERSION>` | Override the version number for the build. |
| `--build-number <N>` | Override the build number for the build. |
| `--debug` | Build in debug mode. |
| `--no-deps` | Skip installing dependencies before building. |
| `--rebuild-deps` | Reinstall dependencies before building, even if already installed. |

### Example Output

```
Building VI Package from path/to/your_package.vipb
✓ Build completed: builds/your_package.vip
```

### Common Issues

- **Linux build limitations**: Review the [VIPM Preview docs](../preview.md) for current platform support notes.
- **Missing dependencies**: Run `vipm install project.vipc` before invoking `vipm build` in CI.

## `vipm sbom`

--8<-- "sbom-preview.md"

Generates a [CycloneDX](https://cyclonedx.org/) Software Bill of Materials (SBOM) from a project file or manifest. See the [SBOM documentation](../sbom/index.md) for a tutorial and workflow guidance.

### Syntax

```bash
vipm sbom [INPUT] --format cyclonedx --schema-version 1.5 --output <PATH> [OPTIONS]
```

`INPUT` is a `vipm.toml`, `.lvproj`, `.dragon`, or `.vipc` file. If omitted, the CLI searches upward for a `vipm.toml`.

### Options

| Option | Description |
|--------|-------------|
| `--format cyclonedx` | Output format (default: `cyclonedx`). |
| `--schema-version 1.5` | CycloneDX spec version for the output document (default: `1.5`). |
| `--output <PATH>` | **Required.** File path for the generated SBOM (relative or absolute). |
| `--product-name <NAME>` | Sets `metadata.component.name` in the SBOM. Defaults to the input filename stem. |
| `--product-version <VERSION>` | Sets `metadata.component.version`. Omitted from the SBOM if not provided. |
| `--product-type <TYPE>` | Sets `metadata.component.type`. One of: `application` (default), `library`, `framework`, `container`, `firmware`, `device`, `file`. |
| `--document-version <N>` | BOM revision number (default: `1`). |
| `--document-serial-number <URN>` | Unique BOM identifier (`urn:uuid:...`). Auto-generated if omitted. |
| `--no-vipm` | Exclude VIPM packages from the SBOM. |
| `--no-nipm` | Exclude NI packages (NIPM) from the SBOM. |
| `--no-dev` | Exclude dev-dependencies (`vipm.toml` input only). |
| `--follow-linker` | Follow the VI linker to discover subVI dependencies (`.lvproj` input only). |
| `--follow-depth <N>` | Linker traversal depth limit. Requires `--follow-linker`. |

### Examples

Generate an SBOM from a LabVIEW project:

```bash
vipm sbom MyProject.lvproj \
  --format cyclonedx \
  --schema-version 1.5 \
  --product-name "My Instrument" \
  --product-version 2.1.0 \
  --output build/bom.json
```

Generate from a vipm.toml, excluding dev-dependencies:

```bash
vipm sbom vipm.toml \
  --format cyclonedx \
  --schema-version 1.5 \
  --no-dev \
  --output build/bom.json
```

Expected output on success:

```
SBOM written to build/bom.json
```

### Exit Codes

| Code | Meaning |
|------|---------|
| `0` | SBOM generated successfully |
| `1` | Unexpected or unclassified error |
| `2` | Invalid arguments or failed input validation |
| `4` | Requested LabVIEW version is not installed |
| `6` | Insufficient edition, license, or activation |
| `8` | File system or IO failure (e.g., cannot write to `--output` path) |
| `13` | Input file is not a supported type |
| `14` | Input file exists but is malformed |
| `15` | A required file does not exist |

Any non-zero exit code means the SBOM was **not** produced. The `--output` file is only written on exit code `0`.

On failure, stderr contains a human-readable error message. Example:

```
error: No LabVIEW installation found for version '2024'.
help: Use 'vipm labview-list' to see available versions
```

### Common Issues

- **Missing required flags**: `--format`, `--schema-version`, and `--output` are always required — there are no defaults.
- **Wrong LabVIEW version**: Use `--labview-version` and `--labview-bitness` to target the correct installation when scanning `.lvproj` files.
- **`--no-dev` on non-toml input**: The `--no-dev` flag is only valid with `vipm.toml` input.

## `vipm sync`

--8<-- "sbom-preview.md"

Reconciles a `vipm.toml` manifest from the dependencies discovered in a LabVIEW project scan.

### Syntax

```bash
vipm sync [TARGET] --from <SOURCE> [OPTIONS]
```

`TARGET` is the `vipm.toml` to update. If omitted, the CLI searches upward from the current directory. `SOURCE` is the file to scan (e.g., a `.lvproj`).

### Options

| Option | Description |
|--------|-------------|
| `--from <SOURCE>` | **Required.** The source file to scan for dependencies. |
| `--dry-run` | Preview changes without writing to the manifest. |
| `--no-vipm` | Exclude VIPM packages from the sync. |
| `--no-nipm` | Exclude NI packages (NIPM) from the sync. |
| `--follow-linker` | Follow the VI linker to discover subVI dependencies. |
| `--follow-depth <N>` | Linker traversal depth limit. Requires `--follow-linker`. |

### Examples

Sync vipm.toml from a LabVIEW project:

```bash
vipm sync --from MyProject.lvproj
```

Preview changes without writing:

```bash
vipm sync --from MyProject.lvproj --dry-run
```

### Common Issues

- **No vipm.toml found**: Either specify the target path explicitly or run the command from a directory that contains (or is a child of a directory that contains) a `vipm.toml`.

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
- [Environment Variables](environment-variables.md)
- [SBOM Generation](../sbom/index.md)
- [Docker and Containers](docker.md)
- [GitHub Actions and CI/CD](github-actions.md)
- Project plan: `dev-docs/cli-docs-improvement-proposal.md`
