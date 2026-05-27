
from PySide6.QtWidgets import QFileDialog, QMessageBox, QWidget
from pathlib import Path
from common.toml_handler import TomlHandler
PATH_SAMPLE_DEFAULT: Path = Path("rps_samples")

def pick_folder(parent: QWidget = None) -> str:
    """
    Opens a dialogue, validates the selection.
    Returns the chosen path as string, or "" if cancelled/invalid.
    """
    folder = QFileDialog.getExistingDirectory(
        parent, "Select folder", str(PATH_SAMPLE_DEFAULT)
    )

    if not folder:
        return ""

    chosen_path = Path(folder)

    if not chosen_path.name.startswith("rps_") or folder == str(PATH_SAMPLE_DEFAULT):
        QMessageBox.warning(
            parent,
            "Invalid folder!",
            f"The folder must start with 'rps_' and cannot be {PATH_SAMPLE_DEFAULT},\n I'm afraid. :(\n\t please choose another folder.",
        )
        return ""

    TomlHandler.toml_edit("global", "boilerplate_project_path", f"{folder}")
    return folder