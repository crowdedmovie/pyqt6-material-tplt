# pyqt6-material-tplt

![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![PyQt6](https://img.shields.io/badge/GUI-PyQt6-41CD52.svg)
![License: GPLv3](https://img.shields.io/badge/license-GPLv3-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey.svg)

This template is a reusable baseline for Python desktop apps. It is based on the work of <https://github.com/beatreichenbach/>, using <https://github.com/beatreichenbach/qt-themes> for themes and <https://github.com/beatreichenbach/qt-material-icons> for icons.

![Theme and Icon Switching GIF Placeholder](docs/screenshots/theme-and-icons-switching-placeholder.gif)

It includes:

- PyQt6 UI
- runtime Qt Designer `.ui` loading
- full theme support via `qt-themes`
- Material icons support via `qt-material-icons`
- Windows and Linux (`.deb` & `.rpm`) packaging scripts


## Quick Start

Create and activate a virtual environment first, then install and run:

```bash
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
python -m pip install -e .
pyqt6-app-template
```

Or run locally with:

```bash
python src/app.py
```

## How The Template Works

1. `app.py` creates the `QApplication` and shows `MainWindow`.
2. `main_window.py` loads `ui/main_window.ui` at runtime with `qtpy.uic.loadUi`.
3. `theme_service.py` reads all available themes from `qt_themes.get_themes()`.
4. `icon_service.py` maps widget object names to Material icon names.
5. Startup theme defaults to `nord` (fallback to first available theme).
6. Changing the combo box reapplies the selected theme and recreates icons.

## Editing The UI With Qt Designer

1. Open `src/gui_template/ui/main_window.ui` in Qt Designer.
2. Edit layout/widgets and save.
3. Keep required object name `themeCombo` (used to bind theme switching).
4. Run the app again. No `.py` UI generation step is needed.

## Themes

- Theme support is provided by the `qt-themes` project from beatreichenbach.
- All `.json` themes shipped in `qt-themes` are available automatically.

## Icons

- Icon support is provided by the `qt-material-icons` project from beatreichenbach.
- Icon names are sourced from <https://fonts.google.com/icons>.
- Widget-to-icon mapping is defined in `src/gui_template/icon_service.py`.
- Icons are recreated on theme changes so colors follow the active palette.

## Packaging

Build standalone binaries with PyInstaller so end users do not need to install dependencies.

### Windows Build Instructions

1. Open PowerShell in the project root.
2. Create and activate a virtual environment.
3. Run the build script:

```powershell
.\scripts\build_windows.ps1
```

4. When the build completes, find the executable at `dist/pyqt6-app-template.exe`.
5. Run the exe directly to verify that the packaged app starts correctly.

Notes:

- The script installs the build dependencies before packaging.
- It bundles the `qt-themes` package, the `qt-material-icons` package, and the app icon from `src/gui_template/assets/`.
- The script stops any running copy of the app before rebuilding so Windows file locks do not block the output folder.
- The script builds a single-file executable (`--onefile`).

### Linux Build and Packaging

1. Open WSL in the project root.
2. Create and activate a Python virtual environment.
3. Install packaging dependencies:

```bash
sudo apt update
sudo apt install -y ruby ruby-dev build-essential rpm python3-venv
```

4. Install `fpm`:

```bash
sudo gem install --no-document fpm
```

5. Build the PyInstaller bundle:

```bash
./scripts/build_linux.sh
```

6. Package the bundle:

```bash
./scripts/package_linux.sh all
```

7. Or build one package at a time:

```bash
./scripts/package_linux.sh deb
./scripts/package_linux.sh rpm
```

Notes:

- `build_linux.sh` creates the frozen app under `dist/pyqt6-app-template`.
- `package_linux.sh` writes distributable files to `dist/packages`.
- `.deb` and `.rpm` are produced from the same frozen bundle.
- `ruby`, `ruby-dev`, and `build-essential` are required to install `fpm` from gems.
- `rpm` provides `rpmbuild` for `.rpm` package creation.
- `python3-venv` is useful if you want isolated build environments.

## Template Reuse Flow

For a new project based on this template:

1. Rename package/module and app command in `pyproject.toml`.
2. Update project constants in `src/gui_template/main_window.py`.
3. Replace sample widgets and text in `src/gui_template/ui/main_window.ui`.
4. Keep `themeCombo` object name if you want built-in theme switching.
5. Adjust icon mappings in `src/gui_template/icon_service.py`.

## License

This template is distributed under GPLv3.
