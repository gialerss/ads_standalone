from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path

import pyads_standalone.bootstrap as bootstrap


def _reset_bootstrap_state() -> None:
    bootstrap._DLL_DIR_HANDLE = None
    bootstrap._HOOK_INSTALLED = False
    sys.meta_path[:] = [finder for finder in sys.meta_path if finder.__class__.__name__ != "_PyadsFinder"]


def test_bootstrap_is_noop_off_windows(monkeypatch) -> None:
    _reset_bootstrap_state()
    monkeypatch.setattr(bootstrap, "_is_windows", lambda: False)
    monkeypatch.setattr(bootstrap, "_has_twincat", lambda: False)

    assert bootstrap.bootstrap() is False


def test_enable_bundled_dll_uses_add_dll_directory(monkeypatch, tmp_path: Path) -> None:
    _reset_bootstrap_state()
    monkeypatch.setattr(bootstrap, "_is_windows", lambda: True)
    monkeypatch.setattr(bootstrap, "_has_twincat", lambda: False)
    monkeypatch.setattr(bootstrap, "_bundled_dll_dir", lambda: tmp_path)

    recorded = {}

    def fake_add_dll_directory(path: str):
        recorded["path"] = path
        return object()

    monkeypatch.setattr(os, "add_dll_directory", fake_add_dll_directory, raising=False)

    assert bootstrap.enable_bundled_dll() is True
    assert recorded["path"] == str(tmp_path)


def test_enable_bundled_dll_uses_path_fallback(monkeypatch, tmp_path: Path) -> None:
    _reset_bootstrap_state()
    monkeypatch.setattr(bootstrap, "_is_windows", lambda: True)
    monkeypatch.setattr(bootstrap, "_has_twincat", lambda: False)
    monkeypatch.setattr(bootstrap, "_bundled_dll_dir", lambda: tmp_path)
    monkeypatch.setattr(bootstrap.sys, "version_info", (3, 7, 9))
    monkeypatch.delattr(os, "add_dll_directory", raising=False)
    monkeypatch.setenv("PATH", "C:\\Windows")

    assert bootstrap.enable_bundled_dll() is True
    assert os.environ["PATH"].split(os.pathsep)[0] == str(tmp_path)


def test_install_import_hook_is_idempotent() -> None:
    _reset_bootstrap_state()
    original_len = len(sys.meta_path)

    bootstrap.install_import_hook()
    bootstrap.install_import_hook()

    assert len(sys.meta_path) == original_len + 1

