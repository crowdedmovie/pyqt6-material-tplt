Param(
    [string]$PythonCommand = "python"
)

$ErrorActionPreference = "Stop"

$env:QT_API = "pyqt6"

Get-Process -Name pyqt6-app-template -ErrorAction SilentlyContinue | Stop-Process -Force

& $PythonCommand -m pip install .[build]
& $PythonCommand -m PyInstaller --noconfirm --onefile --windowed --clean --name pyqt6-app-template --collect-all qt_themes --collect-data gui_template --collect-all qt_material_icons --add-data ".\src\gui_template\assets\icon.png;gui_template\assets" --collect-submodules qtpy --exclude-module PyQt5 --exclude-module PySide6 .\src\gui_template\app.py

Write-Host "Build complete. Output file: dist\\pyqt6-app-template.exe"
