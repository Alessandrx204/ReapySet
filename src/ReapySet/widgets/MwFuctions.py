from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton
from config import MwConfig as Mwc

class MwFucs:

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