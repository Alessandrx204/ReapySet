from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMainWindow, QMessageBox, QMenu

from app.config import APP_NAME, APP_WINDOW_MINIMUM_SIZE
from app.widgets.home_widget import HomeWidget


class MainWindow(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        # Basic mainwindow configuration
        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(*APP_WINDOW_MINIMUM_SIZE)

        # Initialises central widget
        self.home_widget: HomeWidget = HomeWidget(self)
        self.setCentralWidget(self.home_widget)

        # Builds application interface and signal connections
        self._create_actions()
        self._create_menus()
        self._connect_signals()

        self.statusBar().showMessage("ready!")

    def _create_actions(self) -> None:
        """Define application-wide actions and shortcuts."""
        self.exit_action = QAction("Exit", self)
        self.exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        self.exit_action.triggered.connect(self.close)

        self.about_action = QAction("About", self)
        self.about_action.triggered.connect(self._show_about_dialog)

    def _create_menus(self) -> None:
        """Construct the top menu bar structure."""
        file_menu: QMenu = self.menuBar().addMenu("File")
        file_menu.addAction(self.exit_action)

        help_menu: QMenu = self.menuBar().addMenu("Help")
        help_menu.addAction(self.about_action)

    def _connect_signals(self) -> None:
        # Route custom widget signals to window slots
        self.home_widget.message_submitted.connect(self._on_message_submitted)

    @Slot(str)
    def _on_message_submitted(self, message: str) -> None:
        # Display submitted message in status bar for 4 seconds
        self.statusBar().showMessage(f"Message received: {message}", 4000)

    @Slot()
    def _show_about_dialog(self) -> None:
        """Display basic application information dialoggue."""
        QMessageBox.about(
            self,
            f"About {APP_NAME}",
            f"<b>{APP_NAME}</b><br><br>PySide6 template written in Python.",
        )
