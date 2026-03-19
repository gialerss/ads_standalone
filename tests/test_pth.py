from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_pth_is_noop_when_package_is_not_importable() -> None:
    pth_line = (ROOT / "pyads_standalone.pth").read_text(encoding="utf-8").strip()

    # During installation the .pth file can be processed before purelib is on sys.path.
    exec(pth_line, {}, {})
