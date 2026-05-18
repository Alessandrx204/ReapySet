import sys

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QPixmap, Qt
from PySide6.QtWidgets import (
    QApplication, QWidget, QGridLayout, QRadioButton, QButtonGroup, QComboBox, QSizePolicy, QLabel
)
from pathlib import Path

from widgets.python_interpreter_utils import populate_interpreter_combobox

# --- Data: (key, button txt, icon path) ---
ENTRIES = [
    ("PY:UV",            "uv",                       "uv_logo.png"),
    ("PY:VENV",          "Venv(default)",        "python_logo.png"),
    ("PY:POETRY",        "poetry",               "poetry_logo.png"),
    ("PY:HATCH",         "Hatch",                   "pip_logo.png"),
    ("PY:GENERIC_CONDA", "conda*",                "conda_logo.png"),
    ("PY:PIXI",           "Pixi",                  "pixi_logo.png"),
    ("PY:MAMBA",          "Mamba",                "mamba_logo.png"),
    ("PY:PIPENV",         "PipEnv",              "pipenv_logo.png"),
    ("PY:VIRTUALENV",      "VirtualEnv",     "virtualenv_logo.png"),
    ("PY:PDM",             "PDM",                   "pdm_logo.png"),
]

MAX_PER_ROW = 4  # p_max_entry_x_row

QSS = """QRadioButton {
    spacing: -1px;
    padding: 4px 14px;
    border: 2px solid rgba(0, 0, 0, 0.3);
    border-radius: 7px;
    background: qlineargradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:0 rgba(50, 50, 50, 180),
        stop:1 rgba(30, 30, 30, 200)
    );
    color: rgba(235, 235, 235, 220);
    font-size: 13px;
    min-width: 90px;
}

QRadioButton:hover {
    border: 1px solid rgba(255, 255, 255, 0.18);
    background: qlineargradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:0 rgba(70, 70, 70, 200),
        stop:1 rgba(40, 40, 40, 220)
    );
}


QRadioButton:checked {
  
    border: 2px solid rgba(0, 0, 0, 0.3);
    
    /* Reversed gradient (darker at the top) to create an internal shadow effect */


    /* A touch of very muted pink, just to highlight the selection */
    color: rgba(230, 190, 255, 0.90); 
    font-weight: 500; 
}"""


class PackageSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.group = QButtonGroup(self)
        self.select_interpreter = QComboBox()

        self.main_layout = QGridLayout(self)
        self.main_layout.setSpacing(4)

        self.python_label = QLabel("Please Setup Your Python Workspace! (^-^)/")
        self.python_label.setStyleSheet("""QLabel { 
            font-family: "Times New Roman" ;
            letter-spacing: 1.5px; 
            font-style: bold; 
            font-weight: 200;
            font-size: 25pt;
            padding: 20px;
            qproperty-alignment: AlignCenter; 
        }""")

        BASE_DIR = Path(__file__).parent.parent
        self.bg_image_path = str(BASE_DIR / "resources" / "python_free_wallpaper.png")
        self.bg_label = QLabel(self)
        self.bg_label.lower()

        self.main_layout.addWidget(self.python_label, 0, 0)
        self.setup_interpreter_selector(0, 4)
        self.setup_package_manager_selector(ENTRIES, max_per_row=MAX_PER_ROW)

    def setup_interpreter_selector(self, row: int, col: int) -> None:
        populate_interpreter_combobox(self.select_interpreter)
        self.main_layout.addWidget(self.select_interpreter, row, col)
        self.select_interpreter.currentTextChanged.connect(self.on_interpreter_changed)
        self.on_interpreter_changed(self.select_interpreter.currentText())

    def setup_package_manager_selector(self, entries, max_per_row=4, row_offset=2, col_offset=0) -> None:
        self.setStyleSheet(QSS)

        pm_widget = QWidget()
        pm_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        pm_layout = QGridLayout(pm_widget)
        pm_layout.setSpacing(4)
        pm_layout.setContentsMargins(0, 0, 0, 0)

        for i, (key, label, icon_path) in enumerate(entries):
            row, col = divmod(i, max_per_row)
            btn = QRadioButton(label)
            btn.setProperty("key", key)
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(20, 20))
            self.group.addButton(btn, i)
            pm_layout.addWidget(btn, row, col)

        self.group.buttonClicked.connect(
            lambda b: print(f"Selected: key={b.property('key')}  text={b.text()}")
        )

        self.main_layout.addWidget(pm_widget, row_offset, col_offset)

    def resizeEvent(self, event) -> None:
        pixmap = QPixmap(self.bg_image_path)
        self.bg_label.setPixmap(pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ))
        self.bg_label.setGeometry(self.rect())
        super().resizeEvent(event)

    @staticmethod
    def on_interpreter_changed(text: str) -> None:
        print(f" {text} interpreter was selected")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = PackageSelector()
    w.show()
    sys.exit(app.exec())



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = PackageSelector()
    w.show()
    sys.exit(app.exec())