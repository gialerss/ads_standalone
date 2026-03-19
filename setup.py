from __future__ import annotations

import os
import shutil
import struct
import subprocess
import sys
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py
from setuptools.command.sdist import sdist
from wheel.bdist_wheel import bdist_wheel


ROOT = Path(__file__).resolve().parent
PACKAGE_NAME = "pyads_standalone"
TARGET_DLL = "TcAdsDll.dll"
NATIVE_SOURCE_DIR = ROOT
NATIVE_BUILD_DIR = ROOT / "build" / "native"


def _is_64bit_interpreter() -> bool:
    return struct.calcsize("P") == 8


def _should_build_native() -> bool:
    return sys.platform == "win32" and os.environ.get("PYADS_STANDALONE_SKIP_NATIVE") != "1"


def _run(cmd: list[str], cwd: Path | None = None) -> None:
    subprocess.run(cmd, cwd=cwd, check=True)


def build_tcadsdll() -> Path:
    if not _is_64bit_interpreter():
        raise RuntimeError("pyads-standalone only supports 64-bit Windows builds.")

    if shutil.which("meson") is None:
        raise RuntimeError("Meson is required to build the bundled TcAdsDll.dll.")

    if NATIVE_BUILD_DIR.exists():
        setup_cmd = ["meson", "setup", "--reconfigure", str(NATIVE_BUILD_DIR), str(NATIVE_SOURCE_DIR)]
    else:
        setup_cmd = ["meson", "setup", "--vsenv", str(NATIVE_BUILD_DIR), str(NATIVE_SOURCE_DIR)]

    _run(setup_cmd)
    _run(["meson", "compile", "-C", str(NATIVE_BUILD_DIR)])

    dll_path = NATIVE_BUILD_DIR / TARGET_DLL
    if not dll_path.exists():
        raise RuntimeError(f"Expected native build output at {dll_path}, but it was not produced.")

    return dll_path


class CustomBuildPy(build_py):
    def run(self) -> None:
        super().run()

        if not _should_build_native():
            return

        dll_path = build_tcadsdll()
        destination_dir = Path(self.build_lib) / PACKAGE_NAME / "bin"
        self.mkpath(str(destination_dir))
        self.copy_file(str(dll_path), str(destination_dir / TARGET_DLL))


class CustomSDist(sdist):
    def run(self) -> None:
        raise RuntimeError("sdist is intentionally disabled in v1; publish Windows wheels only.")


class CustomBDistWheel(bdist_wheel):
    def finalize_options(self) -> None:
        super().finalize_options()
        self.root_is_pure = False

    def get_tag(self) -> tuple[str, str, str]:
        if not _should_build_native():
            return super().get_tag()

        if not _is_64bit_interpreter():
            raise RuntimeError("pyads-standalone wheels are only produced for win_amd64.")

        return "py3", "none", "win_amd64"


setup(
    data_files=[("", ["pyads_standalone.pth"])],
    zip_safe=False,
    cmdclass={
        "build_py": CustomBuildPy,
        "sdist": CustomSDist,
        "bdist_wheel": CustomBDistWheel,
    },
)
