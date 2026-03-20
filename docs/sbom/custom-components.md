---
title: Custom Components
---

# Adding Custom Components to Your SBOM

--8<-- "sbom-preview.md"

## Background

`vipm sbom` automatically discovers VIPM and NIPM packages in your project, but LabVIEW applications can depend on components that neither package manager tracks — DLLs, firmware, hardware modules, and other third-party artifacts.

The recommended approach is to maintain a separate CycloneDX file for these components and merge it with the `vipm sbom` output using standard CycloneDX merge tooling.

## Merge the `vipm sbom` output with a supplemental SBOM

One practical approach is to maintain a hand-crafted CycloneDX JSON file containing your custom components and merge it with the output of `vipm sbom`.

**Step 1** — Generate your LabVIEW SBOM as usual:

```bash
vipm sbom MyProject.lvproj \
  --format cyclonedx \
  --schema-version 1.5 \
  --product-name "My Application" \
  --product-version 1.0.0 \
  --output build/labview-bom.json
```

**Step 2** — Create a supplemental SBOM file (`custom-components.json`) with your additional components:

```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.5",
  "version": 1,
  "components": [
    {
      "type": "library",
      "name": "libusb",
      "version": "1.0.27",
      "purl": "pkg:github/libusb/libusb@v1.0.27",
      "licenses": [
        { "license": { "id": "LGPL-2.1-or-later" } }
      ]
    }
  ]
}
```

**Step 3** — Merge the two files using the [CycloneDX CLI](https://github.com/CycloneDX/cyclonedx-cli):

```bash
cyclonedx-cli merge \
  --input-files build/labview-bom.json custom-components.json \
  --output-file build/final-bom.json
```

### Other merge tools

Several tools can merge CycloneDX SBOMs:

| Tool | Description |
|------|-------------|
| [CycloneDX CLI](https://github.com/CycloneDX/cyclonedx-cli) | Official CycloneDX tool. Supports flat and hierarchical merge. |
| [sbomasm](https://github.com/interlynk-io/sbomasm) | Supports CycloneDX and SPDX with multiple merge strategies. |
| [sbom-combiner](https://github.com/CycloneDX/sbom-combiner) | Java-based combiner under the CycloneDX organization. |

--8<-- "need-help.md"
