"""Tests for the cross-platform dev-server port scan.

Guards `just dev`'s replacement for the old `ss`/bash port loop: it must
return the start port when free, skip a port that is already bound, and
fail loudly when nothing is available.
"""

from __future__ import annotations

import socket

import dev_serve


def test_find_open_port_returns_start_when_free():
    # Bind an ephemeral port, release it, then ask the finder to start
    # there — it should hand the now-free port straight back.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.bind(("localhost", 0))
        free_port = probe.getsockname()[1]

    assert dev_serve.find_open_port("localhost", free_port) == free_port


def test_find_open_port_skips_bound_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as held:
        held.bind(("localhost", 0))
        taken = held.getsockname()[1]

        result = dev_serve.find_open_port("localhost", taken)

    assert result > taken


def test_find_open_port_raises_when_none_free(monkeypatch):
    # Force every bind to fail so the scan exhausts its range.
    class _AlwaysBusy:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def bind(self, _addr):
            raise OSError("busy")

    monkeypatch.setattr(dev_serve.socket, "socket", lambda *a, **k: _AlwaysBusy())

    try:
        dev_serve.find_open_port("localhost", 65535)
    except OSError as exc:
        assert "no open port" in str(exc)
    else:
        raise AssertionError("expected OSError when no port is free")
