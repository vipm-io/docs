# Installing VIPM 2022 on Ubuntu

!!! info "🚀 New: VIPM 2026 Q1 Preview Available"

    We recommend trying the new **[VIPM 2026 Q1 Preview](../preview.md)** which includes the VIPM CLI plus native Linux installers in both RPM and DEB package formats. This provides a much better installation experience than the legacy VIPM 2022 release documented below.

This document is for collecting information on how to successfully install VIPM 2022 on Ubuntu Linux.

Useful Links:

- [Download VIPM 2022 beta for Linux](https://forums.vipm.io/topic/6423-announcing-the-vipm-2022-for-mac-and-linux-public-beta/)
- [Community Support Forum for VIPM 2022 beta for Linux and Mac](https://forums.vipm.io/forum/89-vipm-2022-for-macos-and-linux-public-beta/)

## Install the LabVIEW 2019 for Linux Runtime Engine (or LabVIEW development environment)

Installing VIPM 2022 for Linux requires intalling the LabVIEW 2019 Runtime Engine.

This can be accomplished by deing either of the following:
- install the full LV2019 development environment (it includes the runtime engine as part of the installation)
- install the LV2019 Runtime Engine (separately without the development environment)


## Installing RPM (.rpm) packages on Ubuntu using `alien`

Either of the above steps will require use of the `alien` command-line tool which can handle rpm packages by converting them to .deb packages.

See: [https://wiki.ubuntu.com/LabVIEW](https://wiki.ubuntu.com/LabVIEW)