# VIPM Linux Crash on Package Installation - Permission Fix

!!! info "🚀 New: VIPM 2026 Q1 Preview Available"

    We recommend trying the new **[VIPM 2026 Q1 Preview](../preview.md)** which includes the VIPM CLI plus native Linux installers in both RPM and DEB package formats. The new release provides improved Linux support and may resolve many installation issues.

## Problem

VIPM crashes with segmentation fault when installing packages on Linux:

```
LabVIEW caught fatal signal
23.3.7f7 - Received SIGSEGV
Reason: invalid permissions for mapped object
Segmentation fault
```

**Symptoms:**
- VIPM launches successfully
- Crashes only when installing/downloading packages
- Standard tmp folder fix doesn't resolve the issue

## Root Cause

VIPM requires write access to LabVIEW installation directories to install packages. When LabVIEW directories are owned by root, VIPM cannot write files and crashes.

## Solution

Change ownership of LabVIEW directories to your user account:

```bash
# Set ownership of LabVIEW installation
sudo chown $USER -R /usr/local/natinst/LabVIEW*

# Set ownership of VIPM directories
sudo chown $USER -R /usr/local/JKI/VIPM
sudo chown $USER -R /etc/JKI
```

## Verification

1. **Check ownership changed:**
   ```bash
   ls -la /usr/local/natinst/ | grep LabVIEW
   ```
   Should show your username, not "root"

2. **Launch VIPM as regular user (NOT with sudo):**
   ```bash
   vipm
   ```

3. **Test package installation** - should complete without crashes

## Important Notes

- **Always run VIPM as regular user** after fixing permissions (don't use `sudo vipm`)
- This matches Windows behavior where users have write access to LabVIEW
- For multi-user systems, consult your system administrator about group-based permissions

## Complete Setup Script

For fresh installations or persistent issues:

```bash
#!/bin/bash

if [ "$EUID" -ne 0 ]; then
  echo "Run with: sudo $0"
  exit 1
fi

echo "Configuring VIPM permissions for: $SUDO_USER"

# Fix file handle limits
if ! test -f /etc/sysctl.d/vipm-files.conf; then
  echo "fs.file-max = 2000000" > /etc/sysctl.d/vipm-files.conf
fi

# Set ownership
chown $SUDO_USER -R /usr/local/natinst/LabVIEW*
chown $SUDO_USER -R /usr/local/JKI/VIPM 2>/dev/null || true
chown $SUDO_USER -R /etc/JKI 2>/dev/null || true

# Fix tmp permissions
chmod 777 /tmp

echo "Complete! Run 'vipm' as regular user (not sudo)"
```

Save as `fix-vipm-permissions.sh`, then run:
```bash
chmod +x fix-vipm-permissions.sh
sudo ./fix-vipm-permissions.sh
```

## Additional Troubleshooting

If issues persist, check:
- File handle limits: `cat /etc/sysctl.d/vipm-files.conf`
- System logs: `journalctl -xe | grep -i vipm`
- See **VIPM Linux Installation Guide** for comprehensive setup

## References

- Jim Kring's [Forum Post](https://forums.vipm.io/topic/6643-file-and-permissions-issues-on-ubuntu-linux/)

---

**Quick Fix**: Run the permission commands above, then launch VIPM as regular user (not sudo).
