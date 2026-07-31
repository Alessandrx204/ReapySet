from pathlib import Path

APP_NAME: str = "PySide6 Template (ReapySet)"
APP_WINDOW_MINIMUM_SIZE: tuple[int, int] = (720, 480)

PACKAGE_DIR: Path = Path(__file__).resolve().parent
RESOURCES_DIR: Path = PACKAGE_DIR / "resources"
STYLESHEET_PATH: Path = RESOURCES_DIR / "styles.qss"
