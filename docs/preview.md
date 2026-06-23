# VIPM Preview

VIPM previews give you early access to upcoming features before they're included in a stable release.

!!! tip "Latest Preview Release"
    [VIPM 2026 Q3 f1 Preview](release-notes/2026.3.1.md) is the latest preview release — see its release notes for what's new.

## Installation

### Windows

- [Download the Windows installer](https://packages.jki.net/vipm/preview/vipm-setup-latest-preview.exe)
- Or install via command line:

    **Silent install — PowerShell:**

    ``` { .powershell .copy }
    $ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri "https://packages.jki.net/vipm/preview/vipm-setup-latest-preview.exe" -OutFile "$env:TEMP\vipm-setup.exe"; Start-Process -Wait -FilePath "$env:TEMP\vipm-setup.exe" -ArgumentList "/exenoui /qn"; Remove-Item "$env:TEMP\vipm-setup.exe" -Force
    ```

    **Silent install — cmd.exe:**

    ``` { .shell .copy }
    curl.exe -L https://packages.jki.net/vipm/preview/vipm-setup-latest-preview.exe -o %TEMP%\vipm-setup.exe && start /wait %TEMP%\vipm-setup.exe /quiet /norestart && del %TEMP%\vipm-setup.exe
    ```

    **Interactive install — PowerShell:**

    ``` { .powershell .copy }
    $ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri "https://packages.jki.net/vipm/preview/vipm-setup-latest-preview.exe" -OutFile "$env:TEMP\vipm-setup.exe"; Start-Process -Wait -FilePath "$env:TEMP\vipm-setup.exe"; Remove-Item "$env:TEMP\vipm-setup.exe" -Force
    ```

    **Interactive install — cmd.exe:**

    ``` { .shell .copy }
    curl.exe -L https://packages.jki.net/vipm/preview/vipm-setup-latest-preview.exe -o %TEMP%\vipm-setup.exe && start /wait %TEMP%\vipm-setup.exe && del %TEMP%\vipm-setup.exe
    ```

### Linux

#### Debian-based (Ubuntu, Debian, Linux Mint, and derivatives)

- [Download .deb package](https://packages.jki.net/vipm/preview/vipm_latest_preview_amd64.deb)
- Or install via command line:

    ``` { .shell .copy }
    wget -O /tmp/vipm.deb https://packages.jki.net/vipm/preview/vipm_latest_preview_amd64.deb && sudo dpkg -i /tmp/vipm.deb && rm /tmp/vipm.deb
    ```

#### Red Hat-based (RHEL, Fedora, CentOS, Rocky Linux, and derivatives)

- [Download .rpm package](https://packages.jki.net/vipm/preview/vipm_latest_preview_amd64.rpm)
- Or install via command line:

    **RHEL 8+ / Fedora / Rocky Linux / AlmaLinux (dnf):**

    ``` { .shell .copy }
    wget -O /tmp/vipm.rpm https://packages.jki.net/vipm/preview/vipm_latest_preview_amd64.rpm && sudo dnf install -y --nogpgcheck /tmp/vipm.rpm && rm /tmp/vipm.rpm
    ```

    **RHEL 7 / CentOS 7 (yum):**

    ``` { .shell .copy }
    wget -O /tmp/vipm.rpm https://packages.jki.net/vipm/preview/vipm_latest_preview_amd64.rpm && sudo yum install -y --nogpgcheck /tmp/vipm.rpm && rm /tmp/vipm.rpm
    ```

    **openSUSE (zypper):**

    ``` { .shell .copy }
    wget -O /tmp/vipm.rpm https://packages.jki.net/vipm/preview/vipm_latest_preview_amd64.rpm && sudo zypper --non-interactive install --no-recommends --allow-unsigned-rpm /tmp/vipm.rpm && rm /tmp/vipm.rpm
    ```

## Feedback

Report issues on [GitHub](https://github.com/vipm-io/vipm-desktop-issues/issues) or join us on [Discord](https://discord.gg/GCB7QQyzsP).
