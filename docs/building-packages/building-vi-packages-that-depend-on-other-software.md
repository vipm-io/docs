# Building VI Packages that Depend on other Software

When the package you are building depends on other software to be installed on the system (e.g. MSVC Runtime, Python, NI TestStand, etc.) there are different ways of handling this.

## A) Inform Users and Let Them Manage it

- In your VI Package's documentation/description, you can list the additional software as a dependency and include a link for how to install and uninstall it.
- You can have your LabVIEW Toolkit VIs check and output an error message that this additional software is required (maybe inside `Create.vi` / `Init.vi`).
- If your LabVIEW Toolkit is interactive (has a UI), you can ask the user if they want to download and install it. You can then download and install it as part of your toolkit's user experience.

## B) Include the Additional Installer in your VI Package (and install it with a post-install custom action)

This approach bundles the additional installer into your VI Package and runs it as part of the installation/uninstallation process.

- Include the additional installer MSI/EXE as an installed file of your package.
- Use a post-install custom action that calls system-exec to run the installer.
- Optionally, use a pre-uninstall custom action that uninstalls the additional installer.

An example of this is the fantastic [G-CLI VI Package Source Code](https://github.com/JamesMc86/G-CLI/tree/v2.4.0/LabVIEW%20Source).

Here's how the G-CLI VI Package does it.

- It includes both a 32-bit and 64-bit MSI installer in the [Installation Support folder](https://github.com/JamesMc86/G-CLI/tree/v2.4.0/LabVIEW%20Source/Installation%20Support). These files get installed right alongside the toolkit VIs.
- Its `Post-Install Custom Action.vi` runs the installer after the VIs and MSIs are installed into LabVIEW.
- Its `Pre-Uninstall Custom Action.vi` runs the uninstaller before the VIs and MSIs are uninstalled from LabVIEW.

If you take this approach, you'll probably want to add some smarts inside your post-install and pre-uninstall custom actions. For example:

- In the post-install action, check whether the additional installer is already installed on the system. If it's installed already, then there's no need to install it.
- In the pre-uninstall action, check whether your VI Package is installed on other LabVIEW versions. You won't want to uninstall the additional software if your package is installed on other LabVIEW versions and it's still needed.

### B.i) Include the Additional Installer in your VI Package as a System Sub-Package

If your VI Package includes the MSIs and puts them in a Destination that installs to a location on the system that is **not underneath LabVIEW** (e.g. `C:\ProgramData\YOUR_PACKAGE_NAME\additional_installers\*.msi`) then the built VI Package will bundle a VIPM "System Package" inside your VI Package as a sub-package.  

This will allow your VI Package to be installed into multiple LabVIEW versions without installing the MSIs into each LabVIEW version and means you won't have to put special smarts into your post-install and pre-uninstall custom actions.
