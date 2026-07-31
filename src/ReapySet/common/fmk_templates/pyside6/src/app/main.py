import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent)) 
from PySide6.QtWidgets import QApplication


from app.config import APP_NAME, STYLESHEET_PATH
from app.main_window import MainWindow

def main() -> int:
    # Initialises application instance
    app: QApplication = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    # Applies the global stylesheet if any
    if STYLESHEET_PATH.exists():
        app.setStyleSheet(STYLESHEET_PATH.read_text(encoding="utf-8"))

    window = MainWindow()
    window.show()
    # Starts the event loop
    return app.exec()

if __name__ == "__main__":
    raise SystemExit(main())
