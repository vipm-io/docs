---
title: SBOM Overview
---

# Software Bill of Materials (SBOM)

A Software Bill of Materials (SBOM) is a machine-readable inventory of every software component in your product — including package names, versions, suppliers, licenses, and cryptographic hashes. SBOMs give you and your customers visibility into exactly what ships in your software.

[Get the JKI Security Suite SBOM Helper desktop app](helper.md){ .md-button .md-button--primary }

## Why SBOMs matter

Regulations such as the [EU Cyber Resilience Act (CRA)](https://jki.net/cra/) and [US Executive Order 14028](https://www.nist.gov/itl/executive-order-14028-improving-nations-cybersecurity) are making SBOMs a requirement for software products in regulated markets. Beyond compliance, SBOMs support practical goals like license auditing, vulnerability tracking, and supply chain transparency.

--8<-- "cra-compliance-help.md"

## What VIPM generates

The VIPM CLI generates [CycloneDX](https://cyclonedx.org/) 1.5 SBOMs in JSON format. A single command scans your LabVIEW project and produces an SBOM that includes:

- **VIPM packages** — packages installed via VI Package Manager
- **NI packages (NIPM)** — packages installed via NI Package Manager
- **Enriched metadata** — descriptions, vendors, and license identifiers
- **Cryptographic hashes** — checksums for each component
- **Product metadata** — your application's name, version, and component type

## Generating from LabVIEW

The LabVIEW Application Builder can generate an SBOM for a build specification, and it does so by calling `vipm sbom` under the hood. The CLI and the Application Builder option are the same generator reached two ways, so an SBOM built from a build specification contains what this section describes, and the reference pages here apply to both.

This path requires **LabVIEW 2026 Q3 or later**. See [Generate an SBOM from LabVIEW](https://www.ni.com/docs/en-US/bundle/labview/page/generate-sbom.html) in the LabVIEW help for the build specification settings.

To run the same generation yourself — from a script, a CI job, or to narrow the SBOM to one build specification — see [Workflows](workflows.md). Running `vipm sbom` directly has different LabVIEW requirements, described under [Supported inputs](#supported-inputs) below.

## Editing an SBOM

Some components no scan can find: DLLs, firmware, hardware modules, and other artifacts that no package manager tracks. The [SBOM Helper Desktop App](helper.md) opens a generated SBOM, lets you add and describe those components, and saves a file ready to ship with your product.

See [Custom Components](custom-components.md) for the full workflow, including the file-based alternative suited to automated builds.

## Supported inputs

| Input type | Description | LabVIEW required? |
|------------|-------------|-------------------|
| `vipm.toml` | Project manifest with declared dependencies | No |
| `.lvproj` | LabVIEW project file — scans installed packages directly | Yes (LabVIEW 2024 or newer) |
| `.dragon` | Dragon configuration file | No |
| `.vipc` | VIPM configuration file | No |

Choose the input that matches your workflow. If your project already uses `vipm.toml`, that's the simplest path — no LabVIEW installation is needed. For existing LabVIEW projects, point directly at your `.lvproj` file. See [Workflows](workflows.md) for guidance on each approach.

!!! note "LabVIEW 2024 or newer is required for `.lvproj` scans"
    Generating an SBOM from a `.lvproj` file requires LabVIEW 2024 or newer; if an older target is resolved, the command exits with code `20` and no SBOM is written. Generate the SBOM from a `vipm.toml`, `.dragon`, or `.vipc` input to avoid the LabVIEW requirement.

    --8<-- "labview-interop-link-reference.md"

## Prerequisites

- **VIPM 2026 Q3** or later — [download here](../preview.md)
- **LabVIEW 2024 or newer** — required only when generating SBOMs from `.lvproj` files
- **NI Package Manager** — required only when including NI packages in the SBOM

Verify your CLI is available:

```bash
vipm --version
```

## Next steps

- **[Getting Started](getting-started.md)** — generate your first SBOM in a few minutes
- **[Workflows](workflows.md)** — choose the right approach for your project and environment
- **[Custom Components](custom-components.md)** — record the components no scan can discover
- **[Output Reference](output-reference.md)** — understand the CycloneDX fields, data sources, and enrichment in your SBOM
- **[CLI Command Reference](../cli/command-reference.md#vipm-sbom)** — full parameter reference for `vipm sbom`

--8<-- "need-help.md"
