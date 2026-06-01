---
title: LabVIEW Compatibility
---

# LabVIEW Compatibility for VIPM CLI

Several `vipm` commands scan or build LabVIEW projects by launching LabVIEW directly. This page covers which LabVIEW versions those operations support, how the CLI picks a version when several are installed, and how compatibility failures are reported.

## Operations that require LabVIEW

The CLI launches LabVIEW when a command operates on a LabVIEW project file or runs a LabVIEW Application Builder build:

- [`vipm sbom <project>.lvproj`](command-reference.md#vipm-sbom) — project scan for SBOM generation
- [`vipm sync --from <project>.lvproj`](command-reference.md#vipm-sync) — project scan to update `vipm.toml`
- [`vipm build <project>.lvproj`](command-reference.md#vipm-build) — LabVIEW Application Builder build from a `.lvproj`
- [`vipm build`](command-reference.md#vipm-build) on a `vipm.toml` LabVIEW build target — LabVIEW Application Builder build from a manifest

Inputs that do **not** launch LabVIEW:

- `vipm sbom` on `vipm.toml`, `.dragon`, or `.vipc` — parsed directly
- `vipm build` on a `.vipb` file — handled without the LabVIEW Application Builder

## Supported LabVIEW version range

VIPM CLI's LabVIEW interop is bounded on both sides:

| Bound | Constraint | Exit code on failure |
|---|---|---|
| Minimum | LabVIEW 2024 (or newer) | [`20`](command-reference.md#exit-codes) (`LABVIEW_VERSION_TOO_OLD`) |
| Maximum | The CLI's own version year — e.g., VIPM CLI 2026 supports LabVIEW up to 2026 | [`19`](command-reference.md#exit-codes) (`COMPONENT_INCOMPATIBLE`) |

If your installed LabVIEW falls outside this window, install a supported LabVIEW year or upgrade VIPM CLI to a year that matches or exceeds your LabVIEW.

### Below the minimum (exit code `20`)

--8<-- "cli-labview-interop-min-version.md"

### Above the maximum (exit code `19`)

If the resolved LabVIEW year is newer than this VIPM CLI year, the command fails with exit code `19` (`COMPONENT_INCOMPATIBLE`) and asks you to upgrade VIPM CLI to a year that matches or exceeds the LabVIEW year. The same upper-bound check also applies to VIPM Desktop and NI Package Manager — see [Exit Codes](command-reference.md#exit-codes).

## Selecting which LabVIEW VIPM uses

When multiple LabVIEW versions are installed, VIPM picks a target from these sources:

- **Command line.** `--labview-version YYYY` and `--labview-bitness 32|64` on any command that resolves a LabVIEW target.
- **Project manifest.** `[project] labview-version` and `labview-bitness` in `vipm.toml`.
- **Workspace-local override.** A `.vipm/config.toml` next to your project's `vipm.toml` overrides the selection for your local checkout only. See [Workspace-Local Configuration](../vipm-toml/workspace-local-config.md).
- **Project file.** `.lvproj` files carry an `LVVersion` attribute that pins the target version.

When a LabVIEW-needing command fails because the resolved version doesn't work (codes `4`, `19`, or `20`), the error reports the resolved LabVIEW version, the source it was picked from, and the other installed LabVIEW versions you could switch to.

## Exit codes from LabVIEW interop

| Code | Constant | Fires when |
|---|---|---|
| `4` | `LABVIEW_VERSION_NOT_FOUND` | The requested LabVIEW version is not installed |
| `19` | `COMPONENT_INCOMPATIBLE` | The resolved LabVIEW year is newer than this VIPM CLI (upper bound) |
| `20` | `LABVIEW_VERSION_TOO_OLD` | The resolved LabVIEW year is older than 2024 (lower bound) |

See the [Exit Codes](command-reference.md#exit-codes) table for the canonical reference across all codes.

## Related

- [CLI Command Reference](command-reference.md) — per-command options including `--labview-version` and `--labview-bitness`
- [Workspace-Local Configuration](../vipm-toml/workspace-local-config.md) — `.vipm/config.toml` LabVIEW override
- [SBOM Overview](../sbom/index.md) — when LabVIEW is needed for SBOM generation
