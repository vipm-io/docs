# VIPM 2026 Q3 Preview 1

## Installation & Feedback

### Windows
- Download the Windows Installer [here](https://packages.jki.net/vipm/preview/vipm-setup-latest-preview.exe)
- Or via a one command install `curl.exe -L https://packages.jki.net/vipm/preview/vipm-setup-latest-preview.exe -o %TEMP%\vipm-setup.exe && start /wait %TEMP%\vipm-setup.exe /quiet /norestart && del %TEMP%\vipm-setup.exe`

### Linux

#### Debian-based distributions (Ubuntu, Debian, Linux Mint, and derivatives)
- Download [here](https://packages.jki.net/vipm/preview/vipm_latest_preview_amd64.deb)
- Or via a one command install `wget -O /tmp/vipm.deb https://packages.jki.net/vipm/preview/vipm_latest_preview_amd64.deb && sudo dpkg -i /tmp/vipm.deb && rm /tmp/vipm.deb`

#### Red Hat-based distributions (RHEL, Fedora, CentOS, Rocky Linux, and derivatives)
- Download [here](https://packages.jki.net/vipm/preview/vipm_latest_preview_amd64.rpm)
- Or via one command install:
  - **RHEL 8+ / Fedora / Rocky Linux / AlmaLinux (dnf):** `wget -O /tmp/vipm.rpm https://packages.jki.net/vipm/preview/vipm_latest_preview_amd64.rpm && sudo dnf install -y --nogpgcheck /tmp/vipm.rpm && rm /tmp/vipm.rpm`
  - **RHEL 7 / CentOS 7 (yum):** `wget -O /tmp/vipm.rpm https://packages.jki.net/vipm/preview/vipm_latest_preview_amd64.rpm && sudo yum install -y --nogpgcheck /tmp/vipm.rpm && rm /tmp/vipm.rpm`
  - **openSUSE (zypper):** `wget -O /tmp/vipm.rpm https://packages.jki.net/vipm/preview/vipm_latest_preview_amd64.rpm && sudo zypper --non-interactive install --no-recommends --allow-unsigned-rpm /tmp/vipm.rpm && rm /tmp/vipm.rpm`

### Feedback
Report issues on [GitHub](https://github.com/vipm-io/vipm-desktop-issues/issues) or join us on [Discord](https://discord.gg/GCB7QQyzsP)

## What's New

### CycloneDX SBOM Generation

Generate a [CycloneDX](https://cyclonedx.org/) 1.5 Software Bill of Materials (SBOM) for your LabVIEW project with a single command. The SBOM includes VIPM packages, NI packages (NIPM), enriched metadata (licenses, descriptions, vendors), and cryptographic hashes (SHA-256, MD5).

SBOMs are increasingly required for regulatory compliance, including the [EU Cyber Resilience Act (CRA)](https://jki.net/cra/). See the [SBOM documentation](sbom/index.md) for details.

```bash
vipm sbom MyProject.lvproj \
  --format cyclonedx \
  --schema-version 1.5 \
  --product-name "My Instrument" \
  --product-version 2.1.0 \
  --output build/bom.json
```

**[Get started with SBOM generation →](sbom/getting-started.md)**

### Manifest Sync (vipm sync)

Keep your `vipm.toml` manifest in sync with the dependencies discovered in a LabVIEW project:

```bash
vipm sync --from MyProject.lvproj
```

Preview changes before writing with `--dry-run`. See the [CLI Command Reference](cli/command-reference.md#vipm-sync) for full options.

---

## Feedback

Thank you to everyone testing VIPM previews! Your feedback is invaluable in helping us improve the product.

Report issues on [GitHub](https://github.com/vipm-io/vipm-desktop-issues/issues) or join us on [Discord](https://discord.gg/GCB7QQyzsP)
