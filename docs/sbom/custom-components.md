---
title: Custom Components
---

# Adding Custom Components to Your SBOM

## Background

`vipm sbom` automatically discovers VIPM and NIPM packages in your project, but LabVIEW applications
can depend on components that neither package manager tracks — DLLs called through Call Library
Function nodes, firmware images, hardware drivers, vendor SDKs, and other third-party artifacts.
Compliance frameworks expect the SBOM to account for **all** third-party components, not only the
package-manager-tracked subset.

Declare these components once in your `vipm.toml`, and every SBOM you generate from that manifest
includes them — deduplicated against discovered packages, deterministically ordered, and marked with
their origin.

!!! tip "Never edit generated SBOM files"

    A generated SBOM is a pure output: it is rebuilt from your manifest, lock file, and project
    sources every time, so hand-edits are destroyed on the next run and break the document's
    verifiability. Add or change components in `vipm.toml` and regenerate instead.

## Declaring components

Add one `[[sbom.component]]` block per component to your `vipm.toml`:

```toml
[[sbom.component]]
name = "libusb"
version = "1.0.27"
type = "library"
purl = "pkg:github/libusb/libusb@1.0.27"
license = "LGPL-2.1-or-later"
supplier = "libusb contributors"
description = "Cross-platform USB access library"
homepage = "https://libusb.info"

[[sbom.component]]
name = "motor-controller-firmware"
version = "3.2.0"
type = "firmware"
supplier = "Acme Motion Inc."
depends-on = ["libusb@1.0.27"]
```

Then generate as usual:

```bash
vipm sbom vipm.toml --format cyclonedx --output build/bom.json
```

Declared components apply to manifest-backed generation — `vipm sbom` with a `vipm.toml` input.
Generating directly from a `.lvproj` file scans the project itself and does not read any manifest,
so declarations do not apply there.

### Field reference

| Field | Required | Description |
|-------|----------|-------------|
| `name` | yes | Component name as it should appear in the SBOM. |
| `version` | no | Component version. When absent, the component is emitted without a version field. |
| `type` | no | CycloneDX component type: `application`, `container`, `data`, `device`, `device-driver`, `file`, `firmware`, `framework`, `library` (default), `machine-learning-model`, `operating-system`, or `platform`. |
| `purl` | no | [Package URL](https://github.com/package-url/purl-spec) identifying the component. Validated when the manifest is loaded and emitted in canonical form. If it carries a version segment, it must agree with `version`. |
| `cpe` | no | CPE identifier for vulnerability correlation. |
| `license` | no | SPDX license identifier (emitted as a license `id`) or a free-form license name (emitted as a license `name`). |
| `supplier` | no | Supplier as `Name <email>` or a bare organization name. |
| `description` | no | Human-readable description. |
| `homepage` | no | Project or vendor URL, emitted as a `website` external reference. |
| `depends-on` | no | Dependency references to other components in the SBOM — see below. |

Declarations are validated when the manifest is loaded: a missing `name`, an unknown `type`, an
invalid `purl`, a duplicate declaration, or a blank field fails the command with a message naming
every problem, so a bad declaration can never produce a silently wrong SBOM.

### Declaring dependencies between components

The `depends-on` field records that a component depends on other components in the SBOM — either
discovered packages or other declared components — by name, or by `name@version` when several
versions are present:

```toml
[[sbom.component]]
name = "motor-controller-firmware"
version = "3.2.0"
type = "firmware"
depends-on = ["libusb@1.0.27", "oglib_error"]
```

These references become edges in the SBOM's dependency graph (CycloneDX `dependencies`). A reference
that matches nothing in the generated SBOM — or that ambiguously matches several components — fails
generation with a message naming the component and the reference, so the graph never silently drops
or misdirects a declared relationship.

### Deduplication against discovered packages

If a declaration matches a package that `vipm sbom` discovered on its own — the same purl, or the
same name and version — the discovered package wins (it carries verified installed-state metadata),
the redundant declaration is dropped with a warning, and any `depends-on` edges from the declaration
carry over to the surviving component. This also means a declaration whose identity matches a
discovered package is the supported way to attach dependency edges to that package.

### Knowing where each component came from

Every component in CycloneDX output carries a `vipm:component:source` property naming how it entered
the SBOM:

| Value | Meaning |
|-------|---------|
| `declared` | A `[[sbom.component]]` declaration in `vipm.toml` |
| `manifest` | A direct dependency from the manifest's dependency tables |
| `transitive` | Resolved from the lock file as a dependency of another package |
| `project-scan` | Discovered by scanning a LabVIEW project |

Tools consuming the SBOM can use this to tell user-declared entries from discovered ones — for
example, to know which components are editable in the manifest.

## Alternative: merging supplemental SBOMs

For component metadata that goes beyond the declaration fields above (file hashes, nested component
trees, output from other scanners such as `syft` or `cdxgen`), you can maintain a separate CycloneDX
file and merge it with the `vipm sbom` output using standard CycloneDX merge tooling:

```bash
vipm sbom vipm.toml --format cyclonedx --output build/labview-bom.json

cyclonedx-cli merge \
  --input-files build/labview-bom.json custom-components.json \
  --output-file build/final-bom.json
```

Keep the supplemental file in version control alongside your project so the merged result stays
reproducible.

| Tool | Description |
|------|-------------|
| [CycloneDX CLI](https://github.com/CycloneDX/cyclonedx-cli) | Official CycloneDX tool. Supports flat and hierarchical merge. |
| [sbomasm](https://github.com/interlynk-io/sbomasm) | Supports CycloneDX and SPDX with multiple merge strategies. |
| [sbom-combiner](https://github.com/CycloneDX/sbom-combiner) | Java-based combiner under the CycloneDX organization. |

--8<-- "need-help.md"
