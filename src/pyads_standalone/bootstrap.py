from __future__ import annotations

import importlib.abc
import importlib.machinery
import os
import sys
from pathlib import Path
from types import ModuleType

from ._patch import patch_loaded_pyads_modules


_DLL_DIR_HANDLE = None
_HOOK_INSTALLED = False
_TARGET_MODULES = {"pyads", "pyads.ads", "pyads.connection", "pyads.pyads_ex"}


def _is_windows() -> bool:
    return sys.platform == "win32"


def _has_twincat() -> bool:
    return bool(os.environ.get("TWINCAT3DIR"))


def _bundled_dll_dir() -> Path:
    return Path(__file__).resolve().parent / "bin"


def enable_bundled_dll() -> bool:
    global _DLL_DIR_HANDLE

    if not _is_windows() or _has_twincat():
        return False

    dll_dir = _bundled_dll_dir()
    if not dll_dir.is_dir():
        return False

    if sys.version_info >= (3, 8) and hasattr(os, "add_dll_directory"):
        if _DLL_DIR_HANDLE is None:
            _DLL_DIR_HANDLE = os.add_dll_directory(str(dll_dir))
    else:
        current = os.environ.get("PATH", "")
        dll_dir_str = str(dll_dir)
        if dll_dir_str not in current.split(os.pathsep):
            os.environ["PATH"] = dll_dir_str + os.pathsep + current if current else dll_dir_str

    return True


def patch_loaded_modules() -> bool:
    pyads_module = sys.modules.get("pyads")
    ads_module = sys.modules.get("pyads.ads")
    connection_module = sys.modules.get("pyads.connection")
    pyads_ex_module = sys.modules.get("pyads.pyads_ex")

    if not all((pyads_module, ads_module, connection_module, pyads_ex_module)):
        return False

    return patch_loaded_pyads_modules(
        pyads_module=pyads_module,
        ads_module=ads_module,
        connection_module=connection_module,
        pyads_ex_module=pyads_ex_module,
    )


class _LoaderWrapper(importlib.abc.Loader):
    def __init__(self, wrapped_loader: importlib.abc.Loader) -> None:
        self._wrapped_loader = wrapped_loader

    def create_module(self, spec):  # type: ignore[no-untyped-def]
        if hasattr(self._wrapped_loader, "create_module"):
            return self._wrapped_loader.create_module(spec)
        return None

    def exec_module(self, module: ModuleType) -> None:
        self._wrapped_loader.exec_module(module)
        patch_loaded_modules()


class _PyadsFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):  # type: ignore[no-untyped-def]
        if fullname not in _TARGET_MODULES:
            return None

        spec = importlib.machinery.PathFinder.find_spec(fullname, path)
        if spec is None or spec.loader is None or isinstance(spec.loader, _LoaderWrapper):
            return spec

        spec.loader = _LoaderWrapper(spec.loader)
        return spec


def install_import_hook() -> None:
    global _HOOK_INSTALLED

    if _HOOK_INSTALLED:
        return

    sys.meta_path.insert(0, _PyadsFinder())
    _HOOK_INSTALLED = True


def bootstrap() -> bool:
    enabled = enable_bundled_dll()
    if not enabled:
        return False

    patch_loaded_modules()
    install_import_hook()
    return True


bootstrap()

