# VIPM Preview

VIPM previews give you early access to upcoming features before they're included in a stable release.

!!! tip "Preview Documentation"
    Full documentation for preview features is available at [docs.vipm.io/preview](https://docs.vipm.io/preview/).

## Installation

### Windows

- [Download the Windows installer](https://packages.jki.net/vipm/preview/vipm-setup-latest-preview.exe)
- Or install via command line:

    ```shell
    curl.exe -L https://packages.jki.net/vipm/preview/vipm-setup-latest-preview.exe -o %TEMP%\vipm-setup.exe && start /wait %TEMP%\vipm-setup.exe /quiet /norestart && del %TEMP%\vipm-setup.exe
    ```

### Linux

#### Debian-based (Ubuntu, Debian, Linux Mint, and derivatives)

- [Download .deb package](https://packages.jki.net/vipm/preview/vipm_latest_preview_amd64.deb)
- Or install via command line:

    ```shell
    wget -O /tmp/vipm.deb https://packages.jki.net/vipm/preview/vipm_latest_preview_amd64.deb && sudo dpkg -i /tmp/vipm.deb && rm /tmp/vipm.deb
    ```

#### Red Hat-based (RHEL, Fedora, CentOS, Rocky Linux, and derivatives)

- [Download .rpm package](https://packages.jki.net/vipm/preview/vipm_latest_preview_amd64.rpm)
- Or install via command line:
    - **RHEL 8+ / Fedora / Rocky Linux / AlmaLinux (dnf):** `wget -O /tmp/vipm.rpm https://packages.jki.net/vipm/preview/vipm_latest_preview_amd64.rpm && sudo dnf install -y --nogpgcheck /tmp/vipm.rpm && rm /tmp/vipm.rpm`
    - **RHEL 7 / CentOS 7 (yum):** `wget -O /tmp/vipm.rpm https://packages.jki.net/vipm/preview/vipm_latest_preview_amd64.rpm && sudo yum install -y --nogpgcheck /tmp/vipm.rpm && rm /tmp/vipm.rpm`
    - **openSUSE (zypper):** `wget -O /tmp/vipm.rpm https://packages.jki.net/vipm/preview/vipm_latest_preview_amd64.rpm && sudo zypper --non-interactive install --no-recommends --allow-unsigned-rpm /tmp/vipm.rpm && rm /tmp/vipm.rpm`

## Feedback

Report issues on [GitHub](https://github.com/vipm-io/vipm-desktop-issues/issues) or join us on [Discord](https://discord.gg/GCB7QQyzsP).
