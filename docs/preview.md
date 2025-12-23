# VIPM 2026Q1 Preview 3

Watch our [overview video](https://www.youtube.com/watch?v=2vHFfQF0agc) to see the new features and improvements in this preview release.

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

### Updates in Preview 3
This release focuses on polish and bug fixes based on community feedback:

**VIPM Desktop Improvements:**

- **Fixed "Search Online" button alignment**: Corrected alignment of the "Search Online" button in the window that appears when no packages are available for search results
- **Fixed destination deletion text issue**: Resolved issue where deleting a custom VI Package Builder destination would leave previously selected text white
- **Improved installer window behavior**: The Updates Installer window now stays visible instead of hiding to the System Tray, making installation progress clearly visible

**VIPM CLI Improvements:**

- **Fixed `vipm about` initialization error**: The `vipm about` command now prints all fields and outputs a warning when VIPM Desktop is not fully initialized (such as on first startup)
- **Added Global Options to command help**: Running `--help` for individual commands (e.g., `vipm build --help`) now displays Global Options in addition to command-specific options
- **Fixed LabVIEW version reporting**: The `vipm build LVPROJ_FILE` command now correctly reports the LabVIEW version being used
- **Fixed output line formatting**: Resolved issue where `vipm build LVPROJ_FILE` output would sometimes garble multiple lines together into a single line

### Updates in Preview 2

- **VI Package building officially supported on Linux**: Build .vip packages natively on Linux systems
- **Multi-platform .vipb files**: Package build files (.vipb) now work seamlessly across Windows and Linux
- **Improved Linux support for RHEL**: Native RPM packages for Red Hat Enterprise Linux and derivatives
- **Fixed .dragon and .vip installation**: Resolved issues with VIPM CLI when installing .dragon and .vip files
- **Case-insensitive library name handling**: VIPM now handles internal library name changes in a case-insensitive manner
- **LabVIEW Class default menu support**: Re-added support for LabVIEW Class default menu items

### LabVIEW 2026 Support
This preview release has been tested with LabVIEW 2026 Beta and includes full LabVIEW 2026 support. You can access the LabVIEW 2026 Beta at the [LabVIEW Beta forum](https://forums.ni.com/t5/LabVIEW-Beta/ct-p/7035).

### Improved Support for Installing VIPM on Linux

VIPM is now available as native Linux packages for seamless installation and updates:

- **DEB Packages** - Native support for Debian-based distributions (Ubuntu, Debian, Linux Mint, and derivatives)

- **RPM Packages** - Native support for Red Hat-based distributions (RHEL, Fedora, CentOS, Rocky Linux, and derivatives)

### VIPM Command Line Interface (CLI)

The new VIPM CLI brings powerful automation capabilities to your package management workflows. Install, update, and remove packages from the command line, integrate VIPM operations into build scripts and CI/CD pipelines, and automate package management tasks across multiple systems.

Once installed, try out VIPM CLI by opening a terminal and typing `vipm`.

### vipm.toml Project Configuration (Preview Feature)

Manage your LabVIEW project's dependencies and builds with a modern, human-readable `vipm.toml` configuration file. Features include declarative dependency management, reproducible builds via lock files, and seamless CI/CD integration.

**[Read the vipm.toml Quick Start Guide →](vipm-toml/index.md)**

### Faster Downloads and Improved Stability (Preview Feature)

VIPM now uses a modernized HTTP client for improved package repository communication and download performance. This preview feature lays the groundwork for enhanced reliability and future capabilities.

### Bug Fixes and Usability Improvements
Various bug and usability fixes including:

* LabVIEW Libraries (lvlib) that contain support files now correctly point to the correct location. Thank you to GitHub users @NatanBiesmans and @AlexanderElbert for reporting this issue.
* Improved Linux workflows. Thank you to GitHub users @pesmith8a and @JamesMc86 for reporting this issue.
* Fixed issue where similar VIPB destination names become linked. Thank you to GitHub user @qalldredge for reporting this issue.
* "Place folder contents in destination" now works for support files. Thank you to GitHub user @Sdusing7 for reporting this issue.

  > This is a preview feature. Enable this through Options > Preview Features and select "[Bug Fix] Place Folder Contents for Non-LabVIEW Files".

--8<-- "need-help.md"    

---

## Thank You to Our Community

Thank you to everyone who has been testing the VIPM 2026Q1 Preview! Your feedback and testing efforts are invaluable in helping us improve the product.

Please continue to report any issues you encounter:

**Feedback**
Report issues on [GitHub](https://github.com/vipm-io/vipm-desktop-issues/issues) or join us on [Discord](https://discord.gg/GCB7QQyzsP)

We appreciate your ongoing support and contributions to making VIPM better for the entire LabVIEW community!

---

**Page last edited:** November 19, 2025

---
