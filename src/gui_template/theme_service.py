"""Theme discovery and application helpers for the template app."""

from __future__ import annotations

import importlib
import os
from typing import Iterable

os.environ.setdefault("QT_API", "pyqt6")

from qtpy import QtWidgets

DEFAULT_THEME = "nord"


def available_theme_names() -> list[str]:
    """Return all discoverable qt-themes names sorted alphabetically."""

    qt_themes = importlib.import_module("qt_themes")
    themes = qt_themes.get_themes()
    return sorted(themes.keys())


def pick_startup_theme(theme_names: Iterable[str]) -> str | None:
    """Pick the startup theme with a safe fallback."""

    names = list(theme_names)
    if not names:
        return None
    if DEFAULT_THEME in names:
        return DEFAULT_THEME
    return names[0]


def apply_theme(theme_name: str | None) -> None:
    """Apply a theme to the current QApplication instance."""

    qt_themes = importlib.import_module("qt_themes")
    if theme_name:
        qt_themes.set_theme(theme_name)
    else:
        qt_themes.set_theme(None)


def ensure_app() -> QtWidgets.QApplication:
    """Return the current QApplication or create one."""

    app = QtWidgets.QApplication.instance()
    if isinstance(app, QtWidgets.QApplication):
        return app
    return QtWidgets.QApplication([])
