# VIPM 2026Q1 Preview 1

Watch our [overview video](https://www.youtube.com/watch?v=2vHFfQF0agc) to see the new features and improvements in this preview release.

## Installation & Feedback

### Windows
Download the Windows Installer [here](https://packages.jki.net/vipm/preview/vipm-setup-latest-preview.exe)

### Linux

#### Debian-based distributions (Ubuntu, Debian, Linux Mint, and derivatives)
- Download [here](https://packages.jki.net/vipm/preview/vipm_latest_preview_amd64.deb)
- Or via a one command install `wget -O /tmp/vipm.deb https://packages.jki.net/vipm/preview/vipm_latest_preview_amd64.deb && sudo dpkg -i /tmp/vipm.deb && rm /tmp/vipm.deb`

#### Red Hat-based distributions (RHEL, Fedora, CentOS, Rocky Linux, and derivatives)
- Download [here](https://packages.jki.net/vipm/preview/vipm_latest_preview_amd64.rpm)
- Or via a one command install `wget -O /tmp/vipm.rpm https://packages.jki.net/vipm/preview/vipm_latest_preview_amd64.rpm && sudo dpkg -i /tmp/vipm.rpm && rm /tmp/vipm.rpm`

### Feedback
Report issues on [GitHub](https://github.com/vipm-io/vipm-desktop-issues/issues) or join us on [Discord](https://discord.gg/GCB7QQyzsP)

## What's New

### LabVIEW 2026 Support
This preview release has been tested with LabVIEW 2026 Beta and includes full LabVIEW 2026 support. You can access the LabVIEW 2026 Beta at the [LabVIEW Beta forum](https://forums.ni.com/t5/LabVIEW-Beta/ct-p/7035).

### Improved Support for Installing VIPM on Linux

VIPM is now available as native Linux packages for seamless installation and updates:

- **DEB Packages** - Native support for Debian-based distributions (Ubuntu, Debian, Linux Mint, and derivatives)

- **RPM Packages** - Native support for Red Hat-based distributions (RHEL, Fedora, CentOS, Rocky Linux, and derivatives)

### VIPM Command Line Interface (CLI)

The new VIPM CLI brings powerful automation capabilities to your package management workflows. Install, update, and remove packages from the command line, integrate VIPM operations into build scripts and CI/CD pipelines, and automate package management tasks across multiple systems.

Once installed, try out VIPM CLI by opening a terminal and typing `vipm`.

### Faster Downloads and Improved Stability (Preview Feature)

VIPM now uses a modernized HTTP client for improved package repository communication and download performance. This preview feature lays the groundwork for enhanced reliability and future capabilities.

### Bug Fixes and Usability Improvements
Various bug and usability fixes including:

* LabVIEW Libraries (lvlib) that contain support files now correctly point to the correct location. Thank you to GitHub users @NatanBiesmans and @AlexanderElbert for reporting this issue.
* Improved Linux workflows. Thank you to GitHub users @pesmith8a and @JamesMc86 for reporting this issue.
* Fixed issue where similar VIPB destination names become linked. Thank you to GitHub user @qalldredge for reporting this issue.
* "Place folder contents in destination" now works for support files. Thank you to GitHub user @Sdusing7 for reporting this issue.

  > This is a preview feature. Enable this through Options > Preview Features and select "[Bug Fix] Place Folder Contents for Non-LabVIEW Files".
    
## Known Issues

| Issue | Status |
|-------|--------|
| Default menu files removed from libraries during build | Fix in review |

---

## Thank You to Our Community

Thank you to everyone who has been testing the VIPM 2026Q1 Preview! Your feedback and testing efforts are invaluable in helping us improve the product.

Please continue to report any issues you encounter:

**Feedback**
Report issues on [GitHub](https://github.com/vipm-io/vipm-desktop-issues/issues) or join us on [Discord](https://discord.gg/GCB7QQyzsP)

We appreciate your ongoing support and contributions to making VIPM better for the entire LabVIEW community!

---

**Page last edited:** November 05, 2025

---
