---
title: Getting Started
---

# Getting Started with SBOM Generation

--8<-- "sbom-preview.md"

This guide walks you through generating your first CycloneDX SBOM with the VIPM CLI.

## Step 1 — Verify the CLI is available

Open a terminal and confirm that VIPM is installed:

```shell
vipm --version
```

Expected output:

```text
VIPM CLI version 2026.3.x
```

If the command is not found, install the [VIPM 2026 Q3 Preview](../preview.md) first.

## Step 2 — Generate an SBOM

Run the `vipm sbom` command against your project. This example uses a `.lvproj` file:

```shell
vipm sbom "C:\MyProject\MyProject.lvproj" ^
  --format "cyclonedx" ^
  --schema-version "1.5" ^
  --output "C:\MyProject\build\bom.json"
```

On Linux or macOS, use backslash line continuations instead:

```bash
vipm sbom "/home/user/MyProject/MyProject.lvproj" \
  --format "cyclonedx" \
  --schema-version "1.5" \
  --output "/home/user/MyProject/build/bom.json"
```

Expected output:

```text
SBOM written to "C:\MyProject\build\bom.json"
```

The only required flag is `--output`. The `--format` and `--schema-version` flags default to `cyclonedx` and `1.5` respectively, but are shown explicitly here for clarity.

## Step 3 — Inspect the output

Open `bom.json` to see the generated CycloneDX document. Key sections include:

- **`metadata.component`** — your product (name, version, type)
- **`metadata.tools`** — records that VIPM CLI generated the SBOM
- **`components`** — the list of dependencies, each with a package URL (`purl`), license, vendor, description, and hashes

## Step 4 — Add product metadata

Set your product's name and version so they appear in the SBOM's root component:

```shell
vipm sbom MyProject.lvproj ^
  --format "cyclonedx" ^
  --schema-version "1.5" ^
  --product-name "My Instrument" ^
  --product-version "2.1.0" ^
  --output "build\bom.json"
```

If `--product-name` is omitted, it defaults to the input filename stem (e.g., `MyProject`). If `--product-version` is omitted, the version field is left out of the SBOM.

## Step 5 — Filter dependencies

You can exclude specific dependency sources:

```shell
# Exclude NI packages, only include VIPM packages
vipm sbom MyProject.lvproj ^
  --format "cyclonedx" ^
  --schema-version "1.5" ^
  --no-nipm ^
  --output "build\bom.json"
```

Available filters:

| Flag | Effect |
|------|--------|
| `--vipm` | Include only VIPM packages |
| `--nipm` | Include only NIPM packages |
| `--no-vipm` | Exclude VIPM packages from the SBOM |
| `--no-nipm` | Exclude NI packages (NIPM) from the SBOM |
| `--no-dev` | Exclude dev-dependencies (vipm.toml input only) |

## Next steps

- **[Workflows](workflows.md)** — learn about different input types, CI/CD integration, and understanding the CycloneDX output
- **[Output Reference](output-reference.md)** — detailed breakdown of every CycloneDX field, where the data comes from, and how enrichment works
- **[CLI Command Reference](../cli/command-reference.md#vipm-sbom)** — full parameter reference including exit codes

--8<-- "need-help.md"
