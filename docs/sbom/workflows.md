---
title: Workflows
---

# SBOM Workflows

--8<-- "sbom-preview.md"

The VIPM CLI supports several input types for SBOM generation. This page helps you choose the right approach for your project and shows how to integrate SBOM generation into CI/CD pipelines.

## Manifest-based generation (vipm.toml)

If your project uses a `vipm.toml` file to declare dependencies, this is the simplest workflow. No LabVIEW installation is needed — the CLI reads the manifest directly.

```bash
vipm sbom vipm.toml \
  --format cyclonedx \
  --schema-version 1.5 \
  --product-name "My Application" \
  --product-version 1.0.0 \
  --output build/bom.json
```

If you omit the input path, the CLI searches upward from the current directory for a `vipm.toml` file.

### Excluding dev-dependencies

Use `--no-dev` to omit dependencies marked as dev-only in your `vipm.toml`:

```bash
vipm sbom vipm.toml \
  --format cyclonedx \
  --schema-version 1.5 \
  --no-dev \
  --output build/bom.json
```

`--no-dev` is only available with `vipm.toml` input.

### Keeping vipm.toml in sync with your project

Use `vipm sync` to reconcile your `vipm.toml` with the dependencies discovered in a LabVIEW project:

```bash
vipm sync --from MyProject.lvproj
```

This updates the `vipm.toml` in your project directory to reflect the packages found in the `.lvproj` file. You can then generate SBOMs from the manifest without needing LabVIEW on your build machine.

Preview changes without writing:

```bash
vipm sync --from MyProject.lvproj --dry-run
```

See the [CLI Command Reference](../cli/command-reference.md#vipm-sync) for full `vipm sync` options.

## Project-based generation (.lvproj)

For LabVIEW projects that don't yet use `vipm.toml`, point directly at the `.lvproj` file. The CLI scans the LabVIEW installation to discover installed packages.

```bash
vipm sbom MyProject.lvproj \
  --format cyclonedx \
  --schema-version 1.5 \
  --output build/bom.json
```

### Targeting a specific LabVIEW version

If multiple LabVIEW versions are installed, use the global options to select one:

```bash
vipm sbom MyProject.lvproj \
  --labview-version 2025 \
  --labview-bitness 64 \
  --format cyclonedx \
  --schema-version 1.5 \
  --output build/bom.json
```

### Following the VI linker

For deeper dependency discovery, use `--follow-linker` to trace subVI dependencies through the LabVIEW linker:

```bash
vipm sbom MyProject.lvproj \
  --format cyclonedx \
  --schema-version 1.5 \
  --follow-linker \
  --follow-depth 3 \
  --output build/bom.json
```

`--follow-depth` sets how many levels deep the linker traversal goes. It requires `--follow-linker` to be set.

## Legacy inputs (.dragon, .vipc)

The CLI also accepts `.dragon` and `.vipc` files as input. These are useful when migrating from older VIPM workflows:

```bash
vipm sbom project.dragon \
  --format cyclonedx \
  --schema-version 1.5 \
  --output build/bom.json
```

```bash
vipm sbom project.vipc \
  --format cyclonedx \
  --schema-version 1.5 \
  --output build/bom.json
```

## CI/CD integration

SBOM generation fits naturally into build pipelines. The CLI runs headless with no GUI, making it suitable for automated environments.

### Docker

If you already run VIPM in Docker (see [Docker and Containers](../cli/docker.md)), add the `vipm sbom` step after your build:

```bash
vipm sbom vipm.toml \
  --format cyclonedx \
  --schema-version 1.5 \
  --product-name "$PRODUCT_NAME" \
  --product-version "$VERSION" \
  --output /output/bom.json
```

### GitHub Actions

Add an SBOM generation step to your workflow (see [GitHub Actions and CI/CD](../cli/github-actions.md) for environment setup):

```yaml
- name: Generate SBOM
  run: |
    vipm sbom vipm.toml \
      --format cyclonedx \
      --schema-version 1.5 \
      --product-name "${{ github.event.repository.name }}" \
      --product-version "${{ github.ref_name }}" \
      --output build/bom.json

- name: Upload SBOM artifact
  uses: actions/upload-artifact@v4
  with:
    name: sbom
    path: build/bom.json
```

### Verifying success in automation

Check the exit code to determine success. Exit code `0` means the SBOM was written; any non-zero code means it was not produced. See the [exit codes table](../cli/command-reference.md#vipm-sbom) for the full list.

## Understanding the CycloneDX output

The generated JSON follows the [CycloneDX 1.5 specification](https://cyclonedx.org/docs/1.5/json/). Here's an overview of the key sections:

### `metadata`

Contains information about the SBOM itself:

- **`metadata.timestamp`** — when the SBOM was generated (ISO 8601)
- **`metadata.tools`** — identifies VIPM CLI as the generating tool
- **`metadata.component`** — your product: the name, version, and type set via `--product-name`, `--product-version`, and `--product-type`

### `components`

An array of dependencies found in your project. Each component includes:

| Field | Description |
|-------|-------------|
| `type` | Component type (e.g., `library`) |
| `name` | Package name |
| `version` | Package version |
| `purl` | Package URL — `pkg:vipm/name@version` or `pkg:nipkg/name@version` |
| `supplier` | Package vendor or publisher |
| `description` | Package description |
| `licenses` | SPDX license identifiers |
| `hashes` | SHA-256 and MD5 checksums |

### `serialNumber` and `version`

Each SBOM has a unique serial number (`urn:uuid:...`) and a document version (starting at 1). These support tracking multiple revisions of the same SBOM over time. You can set them explicitly with `--document-serial-number` and `--document-version`, or let the CLI auto-generate them.

--8<-- "need-help.md"
