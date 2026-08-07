import sys
from pathlib import Path
from loguru import logger
from platformdirs import user_log_dir

APP_NAME = "ReapySet"

# Sets the appropriate log folder
log_dir = Path(user_log_dir(APP_NAME))
log_dir.mkdir(parents=True, exist_ok=True)
log_file_path: Path = log_dir / "ReapySet.log"

logger.remove()

# 1. Output to screen (visible if you launch the app from the terminal or during development)
logger.add(sys.stderr, level="INFO", colorize=True)

# 2. Output to File (saves ALL logs, including DEBUG)
logger.add(
    log_file_path,
    level="DEBUG",
    rotation="5 MB",
    retention="90 days",
    encoding="utf-8",
    enqueue=True  # IMPORTANT for GUIs: makes writing thread-safe and avoids interface crashes
)
