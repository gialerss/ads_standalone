from __future__ import annotations

import os
import subprocess
import sys
import venv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VENV_DIR = ROOT / ".build-venv"


def _python_in_venv() -> Path:
    if os.name == "nt":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def _run(cmd: list[str], cwd: Path | None = None) -> None:
    subprocess.run(cmd, cwd=cwd or ROOT, check=True)


def ensure_venv() -> Path:
    if not VENV_DIR.exists():
        venv.EnvBuilder(with_pip=True).create(VENV_DIR)
    return _python_in_venv()


def main() -> int:
    python = ensure_venv()

    _run([str(python), "-m", "pip", "install", "--upgrade", "pip", "build"])
    _run([str(python), "-m", "build", "--wheel"], cwd=ROOT)

    print("\nBuild completata.")
    print(f"Wheel disponibile in: {ROOT / 'dist'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

