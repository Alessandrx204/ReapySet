import sys


from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QPixmap, Qt
from PySide6.QtWidgets import (
    QApplication, QWidget, QGridLayout, QRadioButton, QButtonGroup, QComboBox, QSizePolicy, QLabel, QLineEdit
)
#from pathlib import Path

from widgets.widgets3.widget31_python.python_interpreter_utils import populate_interpreter_combobox
from config import MwConfig as Mwc
from common.toml_handler import TomlHandler
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


QSS = Mwc.Widget3.py_radiobutton_qss


class PythonGenWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.group = QButtonGroup(self)
        self.select_interpreter = QComboBox()

        self.main_layout = QGridLayout(self)
        self.main_layout.setSpacing(Mwc.Widget3.py_pkg_manager_rbtns_spacing)

        self.python_label = QLabel(Mwc.Widget3.py_qlabel_txt)
        self.python_label.setStyleSheet(Mwc.Widget3.py_qlabel_qss)


        self.bg_image_path = str(Mwc.Images().python_wallpaper)
        self.bg_label = QLabel(self)
        self.bg_label.lower()

        self.main_layout.addWidget(self.python_label, Mwc.Widget3.py_python_qlabel_coords[0],
                                   Mwc.Widget3.py_python_qlabel_coords[1])
        self.setup_interpreter_selector(Mwc.Widget3.py_interpreter_qcombobox_coords[0],
                                        Mwc.Widget3.py_interpreter_qcombobox_coords[1])
        self.setup_package_manager_selector(ENTRIES, max_per_row=MAX_PER_ROW)

        self.unb_interp_qlinedit = QLineEdit(self)
        self.unb_interp_qlinedit.setStyleSheet(Mwc.Widget3.QlineEditQSS)
        self.unb_interp_qlinedit.setMaximumWidth(60)
        self.unb_interp_qlinedit.setSizePolicy(
                            QSizePolicy.Policy.Fixed,
                            QSizePolicy.Policy.Fixed
                                              )
        self.main_layout.addWidget(self.unb_interp_qlinedit,
                                   4,
                                   4,)

    def setup_interpreter_selector(self, row: int, col: int) -> None:
        populate_interpreter_combobox(self.select_interpreter)
        self.main_layout.addWidget(self.select_interpreter, row, col)
        self.select_interpreter.currentIndexChanged.connect(
            lambda: self.on_interpreter_changed(self.select_interpreter)
        )
        self.on_interpreter_changed(self.select_interpreter)  # ← chiamata iniziale

    def setup_package_manager_selector(self, entries, max_per_row=Mwc.Widget3.py_MAX_RBTNS_PER_ROW,
                                       row_offset=Mwc.Widget3.py_pkg_manager_rbtns_coords[0],
                                       col_offset=Mwc.Widget3.py_pkg_manager_rbtns_coords[1]
                                       ) -> None:
        self.setStyleSheet(QSS)

        pm_widget = QWidget()
        pm_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        pm_layout = QGridLayout(pm_widget)
        pm_layout.setSpacing(Mwc.Widget3.py_pkg_manager_rbtns_spacing)
        pm_layout.setContentsMargins(0, 0, 0, 0)

        for i, (key, label, icon_path) in enumerate(entries):
            row, col = divmod(i, max_per_row)
            btn = QRadioButton(label)
            btn.setProperty("key", key)
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(20, 20))
            self.group.addButton(btn, i)
            pm_layout.addWidget(btn, row, col)
            if i == 1:
                btn.setChecked(True)
                TomlHandler.toml_edit("languages", "package_manager", "venv", subsection="python")
                #note: ensures the default type alwaays
                # overrides the previously selected package managaer to avoind mixing them up



        self.group.buttonClicked.connect(
            lambda b: TomlHandler.toml_edit("languages", "package_manager", f"{b.property('key')}", subsection="python"))



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
    def on_interpreter_changed(combobox: QComboBox) -> None:
        label = combobox.currentText()
        path = combobox.currentData()
        print(f"{label} interpreter was selected, path: {path}")
        TomlHandler.toml_edit("languages", "interpreter_version", label, subsection="python")
        TomlHandler.toml_edit("languages", "interpreter_path", path, subsection="python")






if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = PythonGenWidget()
    w.show()
    sys.exit(app.exec())