from typing import Callable

from PySide6.QtCore import QRegularExpression, QTimer
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QLineEdit

from common.toml_handler import TomlHandler
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