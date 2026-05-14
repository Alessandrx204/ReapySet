import os

from PySide6.QtWidgets import (
    QWidget, QGridLayout, QLineEdit, QPushButton, QFileDialog, QMessageBox
)
from pathlib import Path


PATH_SAMPLE_DEFAULT: Path = Path("rps_samples" )



class FolderSelectorWidget(QWidget):
    """
    Grid-based widget with a text field (pre-filled) and a browse button.
    The user must pick a folder starting with 'rps_' that is not PATH_SAMPLE_DEFAULT.
    The chosen path is stored in self.usr_selected_folder.
    """

    def __init__(self, x: int, y: int, placeholder_txt: str, parent=None):
        super().__init__(parent)

        # Storing coordinates (for external use / positioning by the caller)
        self.x_pos, self.y_pos = x, y
        self.usr_selected_folder: str = ""

        # --- Layout setup ---
        layout = QGridLayout(self)

        # Text field pre-filled with the default path
        self.path_input = QLineEdit(str(PATH_SAMPLE_DEFAULT)+ os.sep) # os.sep is / on unix and \ on nt
        self.path_input.setPlaceholderText(placeholder_txt)
        layout.addWidget(self.path_input, 0, 0)

        # Browse button
        browse_btn = QPushButton("Browse…")
        browse_btn.clicked.connect(self._pick_folder)
        layout.addWidget(browse_btn, 0, 1)

    def _pick_folder(self):
        """Opens a dialogue, validates the selection, then updates the field and usr_selected_folder."""
        # Let's convert the default path into a string for the dialogue box
        default_path_str = str(PATH_SAMPLE_DEFAULT)

        folder = QFileDialog.getExistingDirectory(
            self, "Select folder", default_path_str
        )

        if not folder:
            return  # The user cancelled the action

        # We'll use pathlib to analyse the chosen path properly
        chosen_path = Path(folder)

        # Proper validation
        # 1. Checking if the folder name starts with the required prefix
        is_valid_name = chosen_path.name.startswith("rps_")

        # 2. Comparing strings (normalised) or Path objects
        is_not_default = folder != default_path_str

        if not is_valid_name or not is_not_default:
            QMessageBox.warning(
                self,
                "Invalid folder",
                f"The folder must start with 'rps_' and cannot be {default_path_str}, I'm afraid."
            )
            return

        self.usr_selected_folder = folder
        self.path_input.setText(folder)


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    widget = FolderSelectorWidget(x=100, y=100, placeholder_txt="Select a rps_ folder...")
    widget.setWindowTitle("FolderSelectorWidget Test")
    widget.show()
    sys.exit(app.exec())