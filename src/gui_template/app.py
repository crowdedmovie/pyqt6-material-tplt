"""Application entrypoint."""

from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("QT_API", "pyqt6")

if __package__ in (None, ""):
    # Support direct execution: python src/gui_template/app.py
    package_parent = Path(__file__).resolve().parents[1]
    if str(package_parent) not in sys.path:
        sys.path.insert(0, str(package_parent))
    from gui_template.main_window import MainWindow
    from gui_template.theme_service import ensure_app
else:
    from .main_window import MainWindow
    from .theme_service import ensure_app


def main() -> int:
    app = ensure_app()
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
