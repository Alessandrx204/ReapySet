import sys
from pathlib import Path

#import qdarktheme

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QGridLayout
#from chooselang import LangSetup

def _create_language_buttons(
    p_window: QWidget,
    p_button_labels_list: list[str],
    p_max_btn_per_row: int,
    p_window_layout: QGridLayout
    ) -> list[QPushButton]:
    """Creates and places language buttons in a brick-like structure."""



    buttons: list = []

    for i, btn_label in enumerate(p_button_labels_list):
        btn_in_row: int = i // p_max_btn_per_row
        index_column: int = i % p_max_btn_per_row
        row_offset = 1 if (btn_in_row % 2 == 1) else 0
        col: int = index_column * 2 + row_offset

        button = QPushButton(btn_label)
        button.clicked.connect(
            lambda checked=True, btn_txt=btn_label: _handle_language_click(p_window.window(), btn_txt, p_buttons=buttons)
        )

        p_window_layout.addWidget(button, btn_in_row, col, 1, 2)
        buttons.append(button)

    return buttons


def init_main_window(
    p_window: QWidget,
    p_btn_txt_element: list[str],
    p_max_btn_per_row: int = 5) -> list[QPushButton]:

    """Initialises the main window layout and its widgets."""
    window_layout = QGridLayout()
    window_layout.setVerticalSpacing(25)
    window_layout.setAlignment(
        Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
    )

    buttons = _create_language_buttons(p_window, p_btn_txt_element, p_max_btn_per_row, window_layout)

    p_window.setLayout(window_layout)
    return buttons







def _handle_language_click(p_window, p_btn_txt: str, p_buttons: list[QPushButton]):
    from window_reshaping_logic import LangSetup #avoidance of cross import
    LangSetup.setup_buttons(p_window, p_btn_txt, p_buttons)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ReadySet")
        #-----------------SIZE-AND-POS---------------------------
        self.resize(400, 200)

        frame = self.frameGeometry()
        center = QApplication.primaryScreen().availableGeometry().center()
        frame.moveCenter(center)

        top_left = frame.topLeft()
        top_left.setY(top_left.y() -150)

        self.move(top_left)
        #-----------------END-SIZE-AND-POS-BLOCK--------------------------
        self._button_labels_list: list[str] = ["Python", "Kotlin/Java", "C/C++", "C#/F#", "Ts/JavaScript", "GDscript", "Rust", "GO", "Lua"]

        central_widget = QWidget()  # <-- QMainWindow needs a central window


        init_main_window(central_widget,
                         self._button_labels_list)  # Important: this inserts the button text and generates the buttons



        self.setCentralWidget(central_widget)  # <-- not just setLayout() directly

    def resizeEvent(self, event): #resizeEvent is a special method of Qt:
        # it gets called automatically every time the window size changes.
        super().resizeEvent(event)

        if hasattr(self, "back_button"):
            margin = 12
            self.back_button.move(
                margin,
                self.height() - self.back_button.height() - margin
            )

def main():

    app: QApplication = QApplication(sys.argv)
    window: MainWindow = MainWindow()
    base_dir : Path = Path(__file__).resolve().parent
    icon_path : Path = base_dir / "resources" / "icon.png" #sets icon

    icon : QIcon = QIcon(str(icon_path))

    app.setWindowIcon(icon)
    window.setWindowIcon(icon)

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":

    main()