import os
from pathlib import Path
from typing import Callable

from PySide6.QtCore import QRegularExpression, QTimer
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QLineEdit, QFileDialog

from ReapySet.common.toml_handler import TomlHandler
from config import MwConfig as Mwc


class MwFuncs:

    @staticmethod
    def labeled_field(
            label_txt: str,
            widget: QWidget,
            w1qss: str = Mwc.Widget1.QlineTopTextQSS,
            gqss: str = ""
    ) -> QWidget:
        """Wraps a widget with a label above it."""

        container = QWidget()

        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        label = QLabel(label_txt)
        label.setStyleSheet(gqss)

        layout.addWidget(label)
        layout.addWidget(widget)

        if not isinstance(widget, (QPushButton, QComboBox)):
            container.setStyleSheet(str(w1qss))

        return container
    @staticmethod
    def connect_qlineedit( #connects qlinedit to a toml
            p_widget: QLineEdit,
            p_section: str,
            p_key: str,
            p_subsection: str | None = None,
            p_regex_validation: str | None = None,
            p_callback: Callable | None = None
    ) -> None:

        if p_regex_validation:
            _value = QRegularExpressionValidator(
                QRegularExpression(p_regex_validation)
            )
            p_widget.setValidator(_value)

        _timer = QTimer(p_widget)
        _timer.setSingleShot(True)
        _timer.setInterval(500)
        p_widget.textChanged.connect(lambda: _timer.start())

        def _on_timeout():
            TomlHandler.toml_edit(p_section, p_key, p_widget.text(), p_subsection)
            if p_callback:
                p_callback()

        _timer.timeout.connect(_on_timeout)
    @staticmethod
    def choose_project_path_qldialogue(parent: QWidget, path_input: QLineEdit) -> None:
        # Uses the currently displayed path as the starting folder for the picker.
        current_path: str = path_input.text().strip() or str(Path.home())

        selected_dir = QFileDialog.getExistingDirectory(

            parent,

            "Choose default project folder",

            current_path,

        )

        if not selected_dir:
            return
        # Stores path with native OS separator \ or /

        project_path_txt = str(Path(selected_dir)) + os.sep

        path_input.setText(project_path_txt)

        path_input.setCursorPosition(len(project_path_txt))

        path_input.setToolTip(project_path_txt)
        # Updates DEST_PATH
        TomlHandler.toml_edit("global", "project_path", project_path_txt)

