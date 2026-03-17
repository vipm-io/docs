---
title: SBOM Overview
---

# Software Bill of Materials (SBOM)

--8<-- "sbom-preview.md"

A Software Bill of Materials (SBOM) is a machine-readable inventory of every software component in your product — including package names, versions, suppliers, licenses, and cryptographic hashes. SBOMs give you and your customers visibility into exactly what ships in your software.

## Why SBOMs matter

Regulations such as the [EU Cyber Resilience Act (CRA)](https://jki.net/cra/) and [US Executive Order 14028](https://www.nist.gov/itl/executive-order-14028-improving-nations-cybersecurity) are making SBOMs a requirement for software products in regulated markets. Beyond compliance, SBOMs support practical goals like license auditing, vulnerability tracking, and supply chain transparency.

## What VIPM generates

The VIPM CLI generates [CycloneDX](https://cyclonedx.org/) 1.5 SBOMs in JSON format. A single command scans your LabVIEW project and produces an SBOM that includes:

- **VIPM packages** — packages installed via VI Package Manager
- **NI packages (NIPM)** — packages installed via NI Package Manager
- **Enriched metadata** — display names, descriptions, vendors, license identifiers, and download URLs
- **Cryptographic hashes** — SHA-256 and MD5 checksums for each component
- **Product metadata** — your application's name, version, and component type

## Supported inputs

| Input type | Description | LabVIEW required? |
|------------|-------------|-------------------|
| `vipm.toml` | Project manifest with declared dependencies | No |
| `.lvproj` | LabVIEW project file — scans installed packages directly | Yes |
| `.dragon` | Dragon configuration file | No |
| `.vipc` | VIPM configuration file | No |

Choose the input that matches your workflow. If your project already uses `vipm.toml`, that's the simplest path — no LabVIEW installation is needed. For existing LabVIEW projects, point directly at your `.lvproj` file. See [Workflows](workflows.md) for guidance on each approach.

## Prerequisites

- **VIPM 2026 Q3 Preview** or later — [download here](../preview.md)
- **LabVIEW** — required only when generating SBOMs from `.lvproj` files
- **NI Package Manager** — required only when including NI packages in the SBOM

Verify your CLI is available:

```bash
vipm --version
```

## Next steps

- **[Getting Started](getting-started.md)** — generate your first SBOM in a few minutes
- **[Workflows](workflows.md)** — choose the right approach for your project and environment
- **[CLI Command Reference](../cli/command-reference.md#vipm-sbom)** — full parameter reference for `vipm sbom`

--8<-- "need-help.md"
