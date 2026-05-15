title: Command Reference

# VIPM CLI Command Reference

Use this page to look up syntax, options, and common workflows for the most frequently used VIPM CLI commands. For additional details, remember that `vipm help` lists every command and `vipm <command> --help` prints the authoritative help text for a single command.

!!! info "vipm.toml Commands (Preview)"
    Looking for `vipm init`, `vipm add`, `vipm remove`, `vipm lock`, or `vipm clean`? These commands work with the new `vipm.toml` project configuration format. See the [vipm.toml Getting Started guide](../vipm-toml/getting-started.md) for details. For managing NI packages (NIPM) in vipm.toml, see [NI Packages (NIPM)](../vipm-toml/nipm.md).

## Global Options

These options are available on every command unless noted otherwise. Every command also accepts `-h` / `--help`, which prints the authoritative help text for that command.

--8<-- "_generated/global-options.md"

## Exit Codes

Every command returns exit code `0` on success and a non-zero value on failure. The codes are stable — once assigned, a value never changes meaning, so automation scripts can branch on them safely. A given command emits only the subset relevant to its operation; consult the per-command "Common Issues" notes for command-specific guidance.

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | Unexpected or unclassified error |
| `2` | Invalid arguments or failed input validation. Also covers `vipm.lock` being stale or incomplete during dependency-state verification (run `vipm lock`, or pass `--allow-package-drift`). |
| `4` | Requested LabVIEW version is not installed |
| `6` | Insufficient edition, license, or activation |
| `8` | File system or IO failure |
| `11` | LabVIEW build operation failed (compilation error, App Builder failure, etc.) — `vipm build` only |
| `12` | Named build target not found in the project |
| `13` | Input file is not a supported type |
| `14` | Input file exists but is malformed |
| `15` | A required file does not exist |
| `17` | Installed packages disagree with the project's declared state in `vipm.toml` or `vipm.lock`. Use `--allow-package-drift` to override. Applies to `vipm build` and `vipm sbom`. |
| `18` | One or more files referenced by the scanned project could not be found on disk. Use `--allow-missing-files` to override. `vipm sbom` only. |

Commands may additionally emit codes not listed here (e.g., authentication, network, or interruption failures). `vipm <command> --help` is the authoritative source for each command. On failure, stderr always contains a human-readable error message.

## Command Quick Look

| Command | Summary |
|---------|---------|
| [`vipm install`](#vipm-install) | Install packages, `.vipc`, `.vip`, `.ogp`, or `.dragon` files. |
| [`vipm uninstall`](#vipm-uninstall) | Remove packages from the selected LabVIEW installation. |
| [`vipm list`](#vipm-list) | List installed packages or inspect a `.vipc`/`.dragon` file. |
| [`vipm info`](#vipm-info) | Show metadata and installed files for a package. |
| [`vipm refresh`](#vipm-refresh) | Refresh all package sources (VIPM Desktop, CLI cache, NIPM feeds). |
| [`vipm activate`](#vipm-activate) | Activate VIPM Pro using a serial number, name, and email. |
| [`vipm build`](#vipm-build) | Build packages from `.vipb` specs or LabVIEW project build specs. |
| [`vipm sbom`](#vipm-sbom) | Generate a CycloneDX SBOM from a project or manifest. |
| [`vipm sync`](#vipm-sync) | Reconcile vipm.toml from a LabVIEW project scan. |
| [`vipm version`](#vipm-version) | Output the CLI and Desktop version numbers. |
| [`vipm about`](#vipm-about) | Print installation details (paths, versions). |

## `vipm install`

--8<-- "_generated/commands/install.md"

`--yes`/`-y` is also available as the `VIPM_ASSUME_YES=1` environment variable, or use `VIPM_NONINTERACTIVE=1` to disable all prompts. See [Environment Variables](environment-variables.md).

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

- **Package not found**: Run `vipm refresh` and verify the package ID at [vipm.io](https://www.vipm.io).
- **Wrong LabVIEW version**: Specify `--labview-version` and `--labview-bitness` to target the correct environment.

## `vipm uninstall`

--8<-- "_generated/commands/uninstall.md"

`--yes`/`-y` is also available as the `VIPM_ASSUME_YES=1` environment variable, or use `VIPM_NONINTERACTIVE=1` to disable all prompts. See [Environment Variables](environment-variables.md).

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

--8<-- "_generated/commands/list.md"

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

--8<-- "_generated/commands/info.md"

For managing NI packages in vipm.toml, see [NI Packages (NIPM)](../vipm-toml/nipm.md).

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

--8<-- "_generated/commands/search.md"

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
- Run `vipm refresh` first to ensure the latest catalog data before searching in CI.

## `vipm refresh`

--8<-- "_generated/commands/refresh.md"

Refreshes every package source the CLI consults: VIPM Desktop's repository list, the CLI's local cache (repo indexes, specs, database), and any configured NIPM feeds. Use `--no-cache` or `--no-nipm` to skip individual sources, and `--force` to re-download even when a cached copy looks current.

### Example

```bash
vipm refresh
```

### Common Issues

- **Corporate proxy**: Configure `http_proxy` / `https_proxy` environment variables before running.
- **Offline environments**: Mirror the repository internally and point VIPM to the local server.

## `vipm activate`

--8<-- "_generated/commands/activate.md"

Any argument omitted on interactive terminals will trigger a prompt.

### Example Output

```
✓ Activation succeeded!
```

### Common Issues

- Ensure the serial number is valid and not already in use elsewhere.
- The name and email must exactly match the VIPM account tied to the serial number.

## `vipm build`

--8<-- "_generated/commands/build.md"

For LabVIEW project builds:

```bash
vipm build \
  --lvproj-build-spec "My Build" \
  --lvproj-target "My Computer" \
  path/to/project.lvproj
```

### Example Output

```
Building VI Package from path/to/your_package.vipb
✓ Build completed: builds/your_package.vip
```

### Dependency-State Verification

When `vipm build` runs against a `vipm.toml` project, it verifies the build environment matches the project's declared dependency state *before* executing any build target:

1. If `vipm.lock` exists, the lock is checked for completeness and consistency with `vipm.toml`.
2. The installed packages on the host are compared against the lock (or, with no lock, against `vipm.toml`'s direct dependency specifiers).

If either check fails, `vipm build` exits without producing any artifact. The error message identifies the specific packages and tells you which command to run to reconcile:

- `vipm lock` — when the lock is out of sync with `vipm.toml`.
- `vipm install` — when an installed package version doesn't match what's declared.

Bare `.lvproj`/`.vipb` builds (no `vipm.toml`) skip this check; there's no manifest to verify against.

To bypass verification for a single invocation, pass `--allow-package-drift`. The check still runs but failures become stderr warnings instead of hard errors, and the warning lists each drifted package so you see what you're accepting. There is no manifest field for this — the bypass is CLI-only by design.

### Exit Codes

See [Exit Codes](#exit-codes) for the canonical reference. `vipm build` uses codes `0`–`8`, `11`–`15`, and `17`. Any non-zero exit means the build artifact was **not** produced.

### Common Issues

- **Linux build limitations**: Review the [VIPM Preview docs](../preview.md) for current platform support notes.
- **Missing dependencies**: Run `vipm install project.vipc` before invoking `vipm build` in CI.
- **Stale `vipm.lock`**: After editing `vipm.toml`, run `vipm lock` so the lock matches the manifest before building.

## `vipm sbom`

--8<-- "_generated/commands/sbom.md"

Generates a [CycloneDX](https://cyclonedx.org/) Software Bill of Materials. See the [SBOM documentation](../sbom/index.md) for a tutorial and workflow guidance.

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

Scope an SBOM to a specific build specification within a `.lvproj`:

```bash
vipm sbom MyProject.lvproj \
  --format cyclonedx \
  --schema-version 1.5 \
  --lvproj-build-spec "My EXE Build" \
  --lvproj-target "My Computer" \
  --output build/bom.json
```

The resulting SBOM reports only the packages whose code contributes to
that build spec's deliverable — its declared source roots plus whatever
the LabVIEW linker can reach from them. It's a strict subset of (or
equal to) the SBOM for `--lvproj-target "My Computer"` alone.

#### What's in the SBOM vs. what's in the build output

`--lvproj-build-spec` narrows the SBOM to code the build **delivers**,
not just files LabVIEW **copies** into the output directory. In
particular, the build-dialog optimization settings (`exclude-*` /
`remove-*` — inline SubVIs, typedefs, library items, dependent PPLs,
excluded directories, etc.) do **not** shrink the SBOM. Those settings
control file-copy behaviour at build time; the linked code from those
files is still part of the deliverable (e.g., an inline SubVI's block
diagram is expanded into every caller; a dependent PPL is runtime-linked
at load time). Reporting them in the SBOM is correct for supply-chain
disclosure.

If the build spec is an `Installer` or `Package` type, the command
errors with exit code `2`. Those types bundle other build specs'
outputs and declare NIPM dependencies through a different mechanism;
for now, use `--lvproj-target` to scope to the containing target.

Scope to a specific target without selecting a build spec (useful when running from source without building a binary):

```bash
vipm sbom MyProject.lvproj \
  --format cyclonedx \
  --schema-version 1.5 \
  --lvproj-target "My Computer" \
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

See [Exit Codes](#exit-codes) for the canonical reference. `vipm sbom` uses codes `0`–`8`, `12`–`15`, `17`, and `18`. Any non-zero exit means the SBOM was **not** produced — the `--output` file is only written on exit code `0`.

On failure, stderr contains a human-readable error message. Example:

```
error: No LabVIEW installation found for version '2024'.
help: Use 'vipm labview-list' to see available versions
```

### Common Issues

- **Missing `--output`**: The `--output` flag is always required. `--format` defaults to `cyclonedx` and `--schema-version` defaults to `1.5`, so they can be omitted.
- **Wrong LabVIEW version**: Use `--labview-version` and `--labview-bitness` to target the correct installation when scanning `.lvproj` files.
- **`--no-dev` on non-toml input**: The `--no-dev` flag is only valid with `vipm.toml` input.

## `vipm sync`

--8<-- "_generated/commands/sync.md"

`TARGET` is the `vipm.toml` to update — if omitted, the CLI searches upward from the current directory.

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

--8<-- "_generated/commands/version.md"

Useful for support tickets and automation logs. Sample output:

```
VIPM CLI version 2025.3.0
VIPM Desktop version 2025.3.0
```

## `vipm about`

--8<-- "_generated/commands/about.md"

Shows installation information such as install paths and license data. Use `vipm about --help` to review the latest options.

## Related Resources

- [Getting Started](getting-started.md)
- [Environment Variables](environment-variables.md)
- [SBOM Generation](../sbom/index.md)
- [Docker and Containers](docker.md)
- [GitHub Actions and CI/CD](github-actions.md)
