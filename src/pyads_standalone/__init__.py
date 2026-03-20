"""Runtime helpers for the pyads standalone Windows companion package."""

__all__ = ["__version__", "enable"]

__version__ = "0.1.0"


def enable() -> bool:
    """Enable the bundled DLL/import hook explicitly before importing pyads."""

    from .bootstrap import bootstrap

    return bootstrap()
