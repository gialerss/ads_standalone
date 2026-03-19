from __future__ import annotations

import os
import struct
import subprocess
import sys
from pathlib import Path

import build_wheel


ROOT = Path(__file__).resolve().parents[1]


def _run(cmd: list[str], env: dict[str, str] | None = None) -> None:
    subprocess.run(cmd, cwd=ROOT, env=env, check=True)


def _validate_runtime() -> None:
    if sys.platform != "win32":
        raise RuntimeError("Questo script e pensato per la validazione completa su Windows.")
    if struct.calcsize("P") != 8:
        raise RuntimeError("La validazione completa richiede Python Windows a 64 bit.")


def main() -> int:
    _validate_runtime()

    python = build_wheel.ensure_venv()
    print(f"Uso l'ambiente di build: {python}")

    _run([str(python), "-m", "pip", "install", "--upgrade", "pip", "build", "pytest"])

    test_env = os.environ.copy()
    test_env["PYADS_STANDALONE_SKIP_NATIVE"] = "1"

    print("\n[1/3] Eseguo i test Python...")
    _run([str(python), "-m", "pytest"], env=test_env)

    print("\n[2/3] Costruisco il wheel Windows...")
    _run([str(python), str(ROOT / "scripts" / "build_wheel.py")])

    print("\n[3/3] Eseguo lo smoke test sul wheel appena creato...")
    _run([str(python), str(ROOT / "scripts" / "smoke_test_wheel.py")])

    print("\nValidazione Windows completata.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
