"""Main window for the GUI template."""

from __future__ import annotations

import importlib.resources

from qtpy import QtCore, QtGui, QtWidgets, uic

from .icon_service import apply_widget_icons
from .theme_service import apply_theme, available_theme_names, pick_startup_theme

PROJECT_NAME = "pyqt6-app-template"
REPO_URL = "https://github.com/crowdedmovie/pyqt6-app-template"
LICENSE_TEXT = "GPLv3"
LICENSE_URL = "https://www.gnu.org/licenses/quick-guide-gplv3.en.html"
WINDOW_ICON_REL_PATH = ("assets", "icon.png")


class MainWindow(QtWidgets.QMainWindow):
    """Simple baseline window for future GUI projects."""

    def __init__(self) -> None:
        super().__init__()
        self._theme_names = available_theme_names()
        self._theme_combo: QtWidgets.QComboBox | None = None
        self._theme_menu: QtWidgets.QMenu | None = None
        self._theme_actions: dict[str, QtGui.QAction] = {}
        self._load_ui()
        self._wire_ui()
        self._apply_startup_theme()

    def _load_ui(self) -> None:
        ui_resource = importlib.resources.files("gui_template").joinpath("ui", "main_window.ui")
        with importlib.resources.as_file(ui_resource) as ui_file:
            uic.loadUi(str(ui_file), self)

        icon_resource = importlib.resources.files("gui_template").joinpath(*WINDOW_ICON_REL_PATH)
        with importlib.resources.as_file(icon_resource) as icon_file:
            icon = QtGui.QIcon(str(icon_file))
        self.setWindowIcon(icon)
        QtWidgets.QApplication.setWindowIcon(icon)

    def _wire_ui(self) -> None:
        theme_combo = self.findChild(QtWidgets.QComboBox, "themeCombo")
        if theme_combo is not None:
            theme_combo.clear()
            theme_combo.addItems(self._theme_names)
            theme_combo.currentTextChanged.connect(self._on_theme_changed)
            self._theme_combo = theme_combo

        self._wire_menu_actions()
        self._rebuild_theme_menu()

    def _wire_menu_actions(self) -> None:
        action_exit = self.findChild(QtGui.QAction, "actionExit")
        if action_exit is not None:
            action_exit.triggered.connect(self.close)

        action_license = self.findChild(QtGui.QAction, "actionViewLicense")
        if action_license is not None:
            action_license.triggered.connect(self._show_license)

        action_source = self.findChild(QtGui.QAction, "actionSource")
        if action_source is not None:
            action_source.triggered.connect(self._show_source)

        self._theme_menu = self.findChild(QtWidgets.QMenu, "menuThemes")

    def _rebuild_theme_menu(self) -> None:
        if self._theme_menu is None:
            return

        self._theme_menu.clear()
        self._theme_actions.clear()
        for theme_name in self._theme_names:
            action = self._theme_menu.addAction(theme_name)
            action.setCheckable(True)
            action.triggered.connect(
                lambda checked, name=theme_name: self._set_theme_from_menu(name, checked)
            )
            self._theme_actions[theme_name] = action

    def _set_theme_from_menu(self, theme_name: str, checked: bool) -> None:
        if not checked:
            return

        if self._theme_combo is not None:
            self._theme_combo.setCurrentText(theme_name)
            return
        self._on_theme_changed(theme_name)

    def _sync_theme_menu(self, active_theme: str) -> None:
        for theme_name, action in self._theme_actions.items():
            blocker = QtCore.QSignalBlocker(action)
            action.setChecked(theme_name == active_theme)
            del blocker

    def _show_license(self) -> None:
        self._show_link_dialog(
            title="License",
            html=(
                f"This template is distributed under {LICENSE_TEXT}.<br><br>"
                f"See <a href=\"{LICENSE_URL}\">{LICENSE_TEXT}</a> for details."
            ),
        )

    def _show_source(self) -> None:
        self._show_link_dialog(
            title="Source",
            html=(
                f"Project: {PROJECT_NAME}<br>"
                f"Repository: <a href=\"{REPO_URL}\">{REPO_URL}</a>"
            ),
        )

    def _show_link_dialog(self, title: str, html: str) -> None:
        dialog = QtWidgets.QMessageBox(self)
        dialog.setWindowTitle(title)
        dialog.setTextFormat(QtCore.Qt.TextFormat.RichText)
        dialog.setText(html)
        dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)

        label = dialog.findChild(QtWidgets.QLabel, "qt_msgbox_label")
        if label is not None:
            label.setOpenExternalLinks(True)

        dialog.exec()

    def _apply_startup_theme(self) -> None:
        startup_theme = pick_startup_theme(self._theme_names)
        if not startup_theme:
            apply_widget_icons(self)
            self.statusBar().showMessage("No qt-themes were discovered.")
            return

        if self._theme_combo:
            self._theme_combo.blockSignals(True)
            self._theme_combo.setCurrentText(startup_theme)
            self._theme_combo.blockSignals(False)
        self._on_theme_changed(startup_theme)

    def _on_theme_changed(self, theme_name: str) -> None:
        apply_theme(theme_name)
        apply_widget_icons(self)
        self._sync_theme_menu(theme_name)
        self.statusBar().showMessage(f"Active theme: {theme_name}")
