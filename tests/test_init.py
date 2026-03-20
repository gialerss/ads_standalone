from __future__ import annotations

import pyads_standalone
import pyads_standalone.bootstrap as bootstrap_module


def test_enable_delegates_to_bootstrap(monkeypatch) -> None:
    called = []

    def fake_bootstrap() -> bool:
        called.append(True)
        return True

    monkeypatch.setattr(bootstrap_module, "bootstrap", fake_bootstrap)

    assert pyads_standalone.enable() is True
    assert called == [True]
