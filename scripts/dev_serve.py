#!/usr/bin/env python3
"""Serve the docs locally on the first open port at or above 8000.

Backs `just dev`. The port scan lives here, in Python, rather than in a
shell recipe so it runs identically on Windows, macOS, and Linux. The
previous shell implementation relied on `ss` (Linux-only) inside a
`#!/usr/bin/env bash` shebang recipe, which also required `cygpath` on
Windows — neither is present in a stock Git-for-Windows shell.

Finds an unused TCP port by attempting to bind it, then hands off to
`zensical serve --dev-addr <host>:<port>`.
"""

from __future__ import annotations

import socket
import subprocess
import sys

DEFAULT_HOST = "localhost"
DEFAULT_START_PORT = 8000


def find_open_port(host: str = DEFAULT_HOST, start: int = DEFAULT_START_PORT) -> int:
    """Return the first port >= ``start`` on ``host`` that accepts a bind.

    Raises ``OSError`` if no port up to 65535 is free.
    """
    for port in range(start, 65536):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind((host, port))
            except OSError:
                continue
            return port
    raise OSError(f"no open port available at or above {start} on {host}")


def main() -> int:
    host = DEFAULT_HOST
    port = find_open_port(host)
    print(f"Serving on http://{host}:{port}", file=sys.stderr)
    return subprocess.run(
        ["zensical", "serve", "--dev-addr", f"{host}:{port}"]
    ).returncode


if __name__ == "__main__":
    raise SystemExit(main())
