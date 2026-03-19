from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import textwrap
import venv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SMOKE_VENV_DIR = ROOT / ".smoke-venv"


def _python_in_venv() -> Path:
    if sys.platform == "win32":
        return SMOKE_VENV_DIR / "Scripts" / "python.exe"
    return SMOKE_VENV_DIR / "bin" / "python"


def _run(cmd: list[str], cwd: Path | None = None) -> None:
    subprocess.run(cmd, cwd=cwd or ROOT, check=True)


def _find_wheel(explicit_path: str | None) -> Path:
    if explicit_path:
        wheel = Path(explicit_path).resolve()
        if not wheel.exists():
            raise FileNotFoundError(f"Wheel non trovato: {wheel}")
        return wheel

    wheels = sorted((ROOT / "dist").glob("*.whl"))
    if not wheels:
        raise FileNotFoundError("Nessun wheel trovato in dist/. Esegui prima la build.")
    return wheels[-1]


def _recreate_smoke_venv() -> Path:
    if SMOKE_VENV_DIR.exists():
        shutil.rmtree(SMOKE_VENV_DIR)

    venv.EnvBuilder(with_pip=True).create(SMOKE_VENV_DIR)
    return _python_in_venv()


def _smoke_code() -> str:
    return textwrap.dedent(
        """
        import time

        import pyads
        from pyads import Connection
        from pyads.testserver import AdsTestServer


        server = AdsTestServer(logging=False)
        server.start()
        try:
            time.sleep(1)
            pyads.open_port()
            pyads.set_local_address("127.0.0.1.1.1")
            pyads.add_route("127.0.0.1.1.1", "127.0.0.1")

            plc = Connection("127.0.0.1.1.1", pyads.PORT_TC3PLC1, "127.0.0.1")
            plc.open()
            plc.close()
            pyads.close_port()
        finally:
            server.close()
            server.join(timeout=5)
        """
    )


def main() -> int:
    if sys.platform != "win32":
        raise RuntimeError("Lo smoke test del wheel e supportato solo su Windows.")

    parser = argparse.ArgumentParser(
        description="Installa il wheel Windows appena creato in una venv pulita e prova l'import/runtime."
    )
    parser.add_argument(
        "--wheel",
        help="Percorso esplicito del wheel da installare. Se omesso, usa l'ultimo wheel in dist/.",
    )
    args = parser.parse_args()

    wheel = _find_wheel(args.wheel)
    python = _recreate_smoke_venv()

    print(f"Uso il wheel: {wheel}")
    _run([str(python), "-m", "pip", "install", "--upgrade", "pip"])
    _run([str(python), "-m", "pip", "install", "--force-reinstall", str(wheel)])
    _run([str(python), "-c", _smoke_code()])

    print("\nSmoke test completato.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
