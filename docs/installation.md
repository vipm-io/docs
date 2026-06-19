---
title: Installing VIPM
description: Download and install the latest VIPM release on Windows and Linux.
---

# Installing VIPM

## Download (recommended)

Download VIPM from **[vipm.io/download](https://www.vipm.io/download/)** and run the installer. This is the recommended way to install VIPM on Windows and Linux.

## Command-line install (advanced)

!!! note "Interim approach"
    The commands below download the installer for the **current release** directly from our CDN. A simpler scripted installer is planned — a single `curl … | sh` / PowerShell one-liner that always fetches the latest version — and these commands will be replaced by it.

### Windows

**Silent install — PowerShell:**

```powershell
$ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri "https://traffic.libsyn.com/secure/jkinc/vipm-26.3.3954-windows-setup.exe" -OutFile "$env:TEMP\vipm-setup.exe"; Start-Process -Wait -FilePath "$env:TEMP\vipm-setup.exe" -ArgumentList "/exenoui /qn"; Remove-Item "$env:TEMP\vipm-setup.exe" -Force
```

**Silent install — cmd.exe:**

```shell
curl.exe -L https://traffic.libsyn.com/secure/jkinc/vipm-26.3.3954-windows-setup.exe -o %TEMP%\vipm-setup.exe && start /wait %TEMP%\vipm-setup.exe /quiet /norestart && del %TEMP%\vipm-setup.exe
```

**Interactive install — PowerShell:**

```powershell
$ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri "https://traffic.libsyn.com/secure/jkinc/vipm-26.3.3954-windows-setup.exe" -OutFile "$env:TEMP\vipm-setup.exe"; Start-Process -Wait -FilePath "$env:TEMP\vipm-setup.exe"; Remove-Item "$env:TEMP\vipm-setup.exe" -Force
```

**Interactive install — cmd.exe:**

```shell
curl.exe -L https://traffic.libsyn.com/secure/jkinc/vipm-26.3.3954-windows-setup.exe -o %TEMP%\vipm-setup.exe && start /wait %TEMP%\vipm-setup.exe && del %TEMP%\vipm-setup.exe
```

### Linux

**Debian-based (Ubuntu, Debian, Linux Mint, and derivatives):**

```shell
wget -O /tmp/vipm.deb https://traffic.libsyn.com/secure/jkinc/vipm_26.3.0-3954_amd64.deb && sudo dpkg -i /tmp/vipm.deb && rm /tmp/vipm.deb
```

**Red Hat-based (RHEL, Fedora, CentOS, Rocky Linux, and derivatives):**

- **dnf (RHEL 8+ / Fedora / Rocky Linux / AlmaLinux):** `wget -O /tmp/vipm.rpm https://traffic.libsyn.com/secure/jkinc/vipm-26.3.0-3954.x86_64.rpm && sudo dnf install -y --nogpgcheck /tmp/vipm.rpm && rm /tmp/vipm.rpm`
- **yum (RHEL 7 / CentOS 7):** `wget -O /tmp/vipm.rpm https://traffic.libsyn.com/secure/jkinc/vipm-26.3.0-3954.x86_64.rpm && sudo yum install -y --nogpgcheck /tmp/vipm.rpm && rm /tmp/vipm.rpm`
- **zypper (openSUSE):** `wget -O /tmp/vipm.rpm https://traffic.libsyn.com/secure/jkinc/vipm-26.3.0-3954.x86_64.rpm && sudo zypper --non-interactive install --no-recommends --allow-unsigned-rpm /tmp/vipm.rpm && rm /tmp/vipm.rpm`

For more on running VIPM on Linux, see [VIPM on Linux](linux/index.md).

--8<-- "need-help.md"
