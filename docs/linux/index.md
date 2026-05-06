title: Overview

# VIPM on Linux

VIPM is available as a native Linux package, with both DEB and RPM installers, full Package Manager UI, and a powerful command-line interface (CLI) for automation and CI/CD.

## Install

### Debian-based distributions (Ubuntu, Debian, Linux Mint, and derivatives)

Download: [`vipm_26.1.1-3772_amd64.deb`](https://traffic.libsyn.com/secure/jkinc/vipm_26.1.1-3772_amd64.deb)

Or via a one-command install:

```
wget -O /tmp/vipm.deb https://traffic.libsyn.com/secure/jkinc/vipm_26.1.1-3772_amd64.deb && sudo dpkg -i /tmp/vipm.deb && rm /tmp/vipm.deb
```

### Red Hat-based distributions (RHEL, Fedora, CentOS, Rocky Linux, and derivatives)

Download: [`vipm-26.1.1-3772.x86_64.rpm`](https://traffic.libsyn.com/secure/jkinc/vipm-26.1.1-3772.x86_64.rpm)

Or via a one-command install:

- **RHEL 8+ / Fedora / Rocky Linux / AlmaLinux (`dnf`):**
  ```
  wget -O /tmp/vipm.rpm https://traffic.libsyn.com/secure/jkinc/vipm-26.1.1-3772.x86_64.rpm && sudo dnf install -y --nogpgcheck /tmp/vipm.rpm && rm /tmp/vipm.rpm
  ```
- **RHEL 7 / CentOS 7 (`yum`):**
  ```
  wget -O /tmp/vipm.rpm https://traffic.libsyn.com/secure/jkinc/vipm-26.1.1-3772.x86_64.rpm && sudo yum install -y --nogpgcheck /tmp/vipm.rpm && rm /tmp/vipm.rpm
  ```
- **openSUSE (`zypper`):**
  ```
  wget -O /tmp/vipm.rpm https://traffic.libsyn.com/secure/jkinc/vipm-26.1.1-3772.x86_64.rpm && sudo zypper --non-interactive install --no-recommends --allow-unsigned-rpm /tmp/vipm.rpm && rm /tmp/vipm.rpm
  ```

## What's included

- **Native Linux installers** — DEB and RPM, supporting Debian/Ubuntu/Mint and RHEL/Fedora/CentOS/Rocky/openSUSE
- **VIPM Desktop UI** — full graphical Package Manager, including search, install, build, and configure flows
- **VIPM CLI** — command-line interface for scripting and CI/CD integration
- **VI Package building** — build `.vip` packages natively on Linux; `.vipb` build files work across Windows and Linux

See [Release Notes for VIPM 2026 Q1](../release-notes/2026.1.md) for the full feature list, and the [VIPM 2026.1f1 release notes](../release-notes/2026.1.1.md) for the latest fixes.

## Documentation

- [Installing VIPM 2022 on Ubuntu](ubuntu.md) — Legacy installation guide for VIPM 2022
- [Permission Fix for Package Installation Issues](VIPM%20Linux%20Crash%20on%20Package%20Installation%20-%20Permission%20Fix.md) — Troubleshooting guide for installation crashes

--8<-- "need-help.md"
