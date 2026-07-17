


from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QPixmap, Qt
from PySide6.QtWidgets import (
    QWidget, QGridLayout, QRadioButton, QButtonGroup, QComboBox, QSizePolicy, QLabel, QLineEdit
)

from widgets.MwFunctions import MwFuncs as Mwf
#from pathlib import Path

from widgets.widgets3.widget31_python.python_interpreter_find import populate_interpreter_combobox
from config import MwConfig as Mwc
from ReapySet.common.toml_handler import TomlHandler, CONFIG_PATH
# --- Data: (key, button txt, icon path) ---
widget3_instance = Mwc.Widget3()
PMS_ENTRIES = widget3_instance.py_PM_RBTNS_ENTRIES
FMK_ENTRIES = widget3_instance.py_FMK_RBTNS_ENTRIES

MAX_PER_ROW = 4  # p_max_entry_x_row


QSS = Mwc.Widget3.py_radiobutton_qss


class PythonGenWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pms_group = QButtonGroup(self)
        self.frameworks_group = QButtonGroup(self)

        self.select_interpreter = QComboBox()

        self.main_layout: QGridLayout = QGridLayout(self)
        self.main_layout.setSpacing(Mwc.Widget3.py_pkg_manager_rbtns_spacing)

        self.python_label = QLabel(Mwc.Widget3.py_qlabel_txt)
        self.py_frameworks_sep_label = QLabel(Mwc.Widget3.py_frameworks_sep_label_txt)

        self.python_label.setStyleSheet(Mwc.Widget3.py_qlabel_qss)
        self.py_frameworks_sep_label.setStyleSheet(Mwc.Widget3.py_qlabel_qss)


        self.bg_image_path = str(Mwc.Images().python_wallpaper)
        self.bg_pixmap = QPixmap(self.bg_image_path)
        self.bg_label = QLabel(self)
        self.bg_label.lower()

        self.main_layout.addWidget(self.python_label, Mwc.Widget3.py_python_qlabel_coords[0],
                                   Mwc.Widget3.py_python_qlabel_coords[1])

        self.main_layout.addWidget(self.py_frameworks_sep_label, Mwc.Widget3.py_frameworks_sep_label_coords[0],
                                   Mwc.Widget3.py_frameworks_sep_label_coords[1])

        self.setup_interpreter_selector(Mwc.Widget3.py_interpreter_qcombobox_coords[0],
                                        Mwc.Widget3.py_interpreter_qcombobox_coords[1])
        self.setup_py_pms_selector(PMS_ENTRIES, self.pms_group, max_per_row=MAX_PER_ROW)
        self.setup_py_fmk_selector(FMK_ENTRIES, self.frameworks_group, max_per_row=MAX_PER_ROW)

        self.unb_interp_qlinedit = QLineEdit(self)
        self.unb_interp_qlinedit.setStyleSheet(Mwc.Widget3.QlineEditQSS)
        self.unb_interp_qlinedit.setMaximumWidth(60)
        self.unb_interp_qlinedit.setSizePolicy(
                            QSizePolicy.Policy.Fixed,
                            QSizePolicy.Policy.Fixed
                                              )
        self.main_layout.addWidget(
            Mwf.labeled_field(Mwc.Widget3.py_unb_interp_qlinedit_top_txt, self.unb_interp_qlinedit, w1qss="", gqss="""QLabel { 
                                                                                                                                font-family: Arial;
                                                                                                                                font-weight: bold; 
                                                                                                                                font-size: 9px;
                                                                                                                                color: #efebf0; /* grey */
                                                                                                                                                }"""
                                                                                                                                                ),
            Mwc.Widget3.py_unb_interpreter_box_coords[0],
            Mwc.Widget3.py_unb_interpreter_box_coords[1],

            alignment=Qt.AlignmentFlag.AlignVCenter)
        self.unb_interp_qlinedit.setPlaceholderText(Mwc.Widget3.py_unb_interp_qlinedit_inner_txt)

    def setup_interpreter_selector(self, p_row: int, p_col: int) -> None:
        populate_interpreter_combobox(self.select_interpreter)

        self.main_layout.addWidget(
            Mwf.labeled_field(Mwc.Widget3.py_interp_qcbox_top_txt, self.select_interpreter, w1qss="", gqss="""QLabel { 
                                                                                                                                font-family: Arial;
                                                                                                                                font-weight: bold; 
                                                                                                                                font-size: 10px;
                                                                                                                                color: #efebf0; /* grey */
                                                                                                                                                }"""
                                                                                                                                                ),
            p_row,
            p_col,
            alignment=Qt.AlignmentFlag.AlignVCenter
        )

        self.select_interpreter.currentIndexChanged.connect(
            lambda: self.on_interpreter_changed(
                self.select_interpreter
            )
        )

        self.on_interpreter_changed(
            self.select_interpreter
        )

    def setup_py_pms_selector(self,
                            entries,
                              btn_group: QButtonGroup,
                            max_per_row=Mwc.Widget3.py_MAX_RBTNS_PER_ROW,
                            row_offset=Mwc.Widget3.py_pkg_manager_rbtns_coords[0],
                            col_offset=Mwc.Widget3.py_pkg_manager_rbtns_coords[1],
                                       ) -> None:

        self.setStyleSheet(QSS)

        pm_widget: QWidget = QWidget()
        pm_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        pm_layout = QGridLayout(pm_widget)
        pm_layout.setSpacing(Mwc.Widget3.py_pkg_manager_rbtns_spacing)
        pm_layout.setContentsMargins(0, 0, 0, 0)
        pm_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        project_pm = TomlHandler.toml_get(
            p_file=TomlHandler._dest_path(),
            section="languages",
            subsection="python",
            key="package_manager"
        )

        default_pm = TomlHandler.toml_get(
            p_file=CONFIG_PATH,
            section="python",
            key="default_pm"
        )

        checked_pm = project_pm or default_pm or "PY:VENV"

        if not project_pm: # "" in toml is not none but empty string
            TomlHandler.toml_edit(
                "languages",
                "package_manager",
                checked_pm,
                subsection="python"
            )

        for i, (key, label, icon_path) in enumerate(entries):
            row, col = divmod(i, max_per_row)
            btn_label: str = label
            if key == default_pm:
                btn_label += " (default)" # adds default label to the default pm
            btn = QRadioButton(btn_label)
            btn.setProperty("key", key)
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(20, 20))
            btn_group.addButton(btn, i)
            pm_layout.addWidget(btn, row, col)
            if key == checked_pm:
                btn.setChecked(True)
                # Selects the package manager currently stored in the project TOML.
                # If missing, it was initialised from the global default.
            if i == len(entries) - 1:
                btn.setEnabled(False) #disables mojo

        btn_group.buttonClicked.connect(self.on_package_manager_changed)



        self.main_layout.addWidget(pm_widget, row_offset, col_offset)
    def setup_py_fmk_selector(self,
                            entries,
                              btn_group: QButtonGroup,
                            max_per_row=Mwc.Widget3.py_MAX_RBTNS_PER_ROW,
                            row_offset=Mwc.Widget3.py_fmk_rbtns_coords[0],
                            col_offset=Mwc.Widget3.py_fmk_rbtns_coords[1],
                                       ) -> None:

        self.setStyleSheet(QSS)

        fmk_widget: QWidget = QWidget()
        fmk_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        fmk_layout = QGridLayout(fmk_widget)
        fmk_layout.setSpacing(Mwc.Widget3.py_pkg_manager_rbtns_spacing)
        fmk_layout.setContentsMargins(0, 0, 0, 0)
        fmk_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        project_fmk = TomlHandler.toml_get(
            p_file=TomlHandler._dest_path(),
            section="languages",
            subsection="python",
            key="selected_framework"
        )






        for i, (key, label, icon_path) in enumerate(entries):
            row, col = divmod(i, max_per_row)
            btn_label: str = label

            btn = QRadioButton(btn_label)
            btn.setProperty("key", key)
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(20, 20))
            btn_group.addButton(btn, i)
            fmk_layout.addWidget(btn, row, col)

                # Selects the package manager currently stored in the project TOML.
                # If missing, it was initialised from the global default.
            if i != len(entries) :# a way to disable them
                btn.setEnabled(False) #disables all except the last

        btn_group.buttonClicked.connect(self.on_framework_changed)



        self.main_layout.addWidget(fmk_widget, row_offset, col_offset)

    @staticmethod
    def on_package_manager_changed(button: QRadioButton) -> None:
        key = button.property("key")
        TomlHandler.toml_edit(
            "languages",
            "package_manager",
            str(key),
            subsection="python"
        )

    @staticmethod
    def on_framework_changed(button: QRadioButton) -> None:
        key = button.property("key")
        TomlHandler.toml_edit(
            "languages",
            "selected_framework",
            str(key),
            subsection="python"
        )

    def resizeEvent(self, event) -> None:
        self.bg_label.setPixmap(
            self.bg_pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )
        self.bg_label.setGeometry(self.rect())
        super().resizeEvent(event)

    @staticmethod
    def on_interpreter_changed(combobox: QComboBox) -> None:
        label = combobox.currentText()
        path = combobox.currentData()
        print(f"{label} interpreter was selected, path: {path}")
        TomlHandler.toml_edit("languages", "interpreter_version", label, subsection="python")
        TomlHandler.toml_edit("languages", "interpreter_path", path, subsection="python")






