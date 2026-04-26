#!/usr/bin/env bash
set -euo pipefail

export QT_API=pyqt6

python3 -m pip install '.[build]'
python3 -m PyInstaller --noconfirm --windowed --clean --name pyqt6-app-template --collect-all qt_themes --collect-data gui_template --collect-all qt_material_icons --add-data "./src/gui_template/assets/icon.png:gui_template/assets" --collect-submodules qtpy --exclude-module PyQt5 --exclude-module PySide6 ./src/gui_template/app.py

echo "Build complete. Output folder: dist/pyqt6-app-template"
