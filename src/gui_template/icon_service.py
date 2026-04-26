"""Widget icon mappings for qt-material-icons integration."""

from __future__ import annotations

import importlib

from qtpy import QtCore, QtWidgets

_ICON_MAP: dict[str, tuple[str, int]] = {
    "primaryActionButton": ("search", 20),
    "secondaryActionButton": ("settings", 20),
    "experimentalCheck": ("steppers", 24),
}


def apply_widget_icons(window: QtWidgets.QMainWindow) -> None:
    """Recreate and assign icons for mapped widgets using the active palette."""

    try:
        qt_material_icons = importlib.import_module("qt_material_icons")
    except ImportError:
        return

    material_icon = qt_material_icons.MaterialIcon
    style = material_icon.Style.OUTLINED
    loaded_sizes: set[int] = set()

    for widget_name, (icon_name, size) in _ICON_MAP.items():
        widget = window.findChild(QtWidgets.QAbstractButton, widget_name)
        if widget is None:
            continue

        if size not in loaded_sizes:
            material_icon.import_resource(style, size)
            loaded_sizes.add(size)

        if not material_icon.resource_exists(icon_name, style, False, size):
            continue

        icon = material_icon(icon_name, style=style, fill=False, size=size)
        widget.setIcon(icon)
        widget.setIconSize(QtCore.QSize(size, size))
