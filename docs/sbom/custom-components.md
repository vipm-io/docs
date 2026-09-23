---
title: Custom Components
---

# Adding Custom Components to Your SBOM

## Background

`vipm sbom` automatically discovers VIPM and NIPM packages in your project, but LabVIEW applications can depend on components that neither package manager tracks — DLLs, firmware, hardware modules, and other third-party artifacts.

These components appear in your SBOM only because someone records them. The [JKI Security Suite SBOM Helper](helper.md) is the most direct way to do that: it opens the SBOM `vipm sbom` generated, lets you add and describe the components the scan cannot see, and saves a file ready to ship with your product.

## Add components with the SBOM Helper

The SBOM Helper is a Windows desktop application. See [SBOM Helper Desktop App](helper.md) to download and install it, and for what it can record.

**Step 1** — Generate your LabVIEW SBOM as usual:

```bash
vipm sbom MyProject.lvproj \
  --format cyclonedx \
  --schema-version 1.5 \
  --product-name "My Application" \
  --product-version 1.0.0 \
  --output build/labview-bom.json
```

**Step 2** — Open `build/labview-bom.json` in the SBOM Helper.

**Step 3** — Add a component for each artifact the scan could not find. Point the Helper at the file on disk and it fills in what the file itself declares, or type the details yourself. For each component you can record:

- a **name** — the component's canonical identifier — and a **display name** for the name people recognise
- a **version** and a **component type** — library, application, device driver, and the other CycloneDX types
- a **supplier** and a **license**
- **cryptographic hashes**, read from the file you picked or typed in
- a **Package URL (purl)** — or none, when no package ecosystem describes the component

**Step 4** — Save. The result is one CycloneDX file holding both the discovered packages and the components you added.

Because the Helper edits the generated SBOM in place, there is no second file to keep in step and no merge step to run.

## Maintaining a supplemental SBOM by hand

Editing the generated SBOM suits a person working through a release. A build with nobody at the keyboard needs its components to come from a file under version control instead, so the supplemental-file approach below remains the right answer for automated pipelines — and for anything the Helper does not cover.

**Step 1** — Generate your LabVIEW SBOM as shown above.

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
