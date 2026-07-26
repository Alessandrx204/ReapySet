from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget


class HomeWidget(QWidget):
    # Custom signal emitted when a valid message is submitted
    message_submitted = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        # UI elements setup
        self.title_label = QLabel("PySide6 template (ReapySet)")
        self.title_label.setObjectName("titleLabel")

        self.description_label = QLabel(
            "This is a simple PySide6 template application.\n You can type a message below and press 'Invia' or hit Enter to submit it."
        )
        self.description_label.setWordWrap(True)

        self.message_edit = QLineEdit()
        self.message_edit.setPlaceholderText("Type something here")
        self.message_edit.setClearButtonEnabled(True)

        self.submit_button = QPushButton("submit")
        self.submit_button.setDefault(True)

        # Main layout configuration
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(16)
        layout.addWidget(self.title_label)
        layout.addWidget(self.description_label)
        layout.addWidget(self.message_edit)
        layout.addWidget(self.submit_button)
        layout.addStretch()

        # Connect user actions to submission handler
        self.submit_button.clicked.connect(self._submit_message)
        self.message_edit.returnPressed.connect(self._submit_message)

    @Slot()
    def _submit_message(self) -> None:
        """Validate input and emit the message signal."""
        message = self.message_edit.text().strip()

        # Ignore empty submissions and retain input focus
        if not message:
            self.message_edit.setFocus()
            return

        self.message_submitted.emit(message)
        self.message_edit.clear()
        self.message_edit.setFocus()
