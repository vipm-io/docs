# System Software Dependencies

If the package you are building requires software to be installed on the system, there are ways of handling this with VIPM.

- include the additional installer MSI/EXE as an installed file of your package.
- use a post-build custom action that calls system-exec to run the installer.
- optionally, use a pre-uninstall custom action that uninstalls the additional installer.

For an example, see the G-CLI vi package source code and .vipm build spec:
https://github.com/JamesMc86/G-CLI/tree/v2.4.0/LabVIEW%20Source
