import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QGridLayout
#from chooselang import LangSetup

def init_main_window(p_window: QWidget, p_btn_txt_element: list[str], p_per_row: int = 5):
    window_layout:QGridLayout = QGridLayout()
    window_layout.setVerticalSpacing(25)
    window_layout.setAlignment(
        Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
    ) #aligns to the widgets
    # each button takes 2 cloumns, offset od odd rows is +1 column

    """organises the buttons in a brick like stricksutre by leaving empy columns"""

    for i, program_lang in enumerate(p_btn_txt_element):
        btn_in_row = i // p_per_row #integer division
        index_column: int = i % p_per_row
        row_offset = 1 if (btn_in_row % 2 == 1) else 0
        col: int = index_column * 2 + row_offset
        button = QPushButton(program_lang)
        button.clicked.connect(
            lambda checked=False, btn_txt=program_lang: _handle_language_click(p_window.window(), btn_txt)
        )

        window_layout.addWidget(button, btn_in_row, col, 1, 2)

    p_window.setLayout(window_layout)

def _handle_language_click(p_window, p_btn_txt: str):
    from chooselang import LangSetup
    LangSetup.setup_all(p_window, p_btn_txt)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ReadySet")
        #-----------------SIZE-AND-POS---------------------------
        self.resize(400, 300)

        frame = self.frameGeometry()
        center = QApplication.primaryScreen().availableGeometry().center()
        frame.moveCenter(center)

        top_left = frame.topLeft()
        top_left.setY(top_left.y() -150)

        self.move(top_left)
        #-----------------END-SIZE-AND-POS-BLOCK--------------------------
        self._button_labels_txt: list[str] = ["Python", "Kotlin/Java", "C/C++", "C#/F#", "Ts/JavaScript", "GDscript", "Rust", "GO", "Lua"]

        central_widget = QWidget()  # <-- QMainWindow needs a central window
        init_main_window(central_widget, self._button_labels_txt)
        self.setCentralWidget(central_widget)  # <-- not just setLayout() directly

def main():

    app: QApplication = QApplication(sys.argv)
    window: MainWindow = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":

    main()