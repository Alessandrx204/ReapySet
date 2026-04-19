from PySide6.QtCore import QPropertyAnimation, QRect, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QPushButton, QMessageBox

import mainWindow



class LangSetup(mainWindow.MainWindow):
    def __init__(self):
        super().__init__()
        self._anim = QPropertyAnimation(self, b"geometry")
        self._saved_geometry = None
        self._expanded_geometry = None
        #---------------BACK-BUTTON-LOGIC-----------------------
        self.back_button = QPushButton("Back", self) #back button to return to main window
        self.back_button.setFixedSize(90, 32)
        self.back_button.hide()
        self.back_button.clicked.connect(self.restore_window)
        # --------------END-BACK-BUTTON-LOGIC-----------------------

    def resizeEvent(self, event):
        super().resizeEvent(event)
        margin = 12
        x = margin
        y = self.height() - self.back_button.height() - margin
        self.back_button.move(x, y)

    @staticmethod
    def setup_all(p_choosed_lang):
        match p_choosed_lang:
            #btn_txt_element: list[str] = ["Python","Kotlin/Java","C/C++","C#","Ts/JavaScript","GDscript", "Rust","Ruby", "SOON™" ]

            case "Python":
                error_window()
            case "Java/Kotlin":
                ...
            case "C/C++":
                ...
            case "C#":
                ...
            case "Ts/JavaScript":
                ...
            case "Rust":
                ...
            case "Ruby":
                ...
            case "SOON":
                ...
    ...



    def common_window_update(self):
        if self._saved_geometry is None:
            self._saved_geometry = self.geometry()

        start_rect = self.geometry()
        end_rect = QRect(
            start_rect.x(),
            start_rect.y(),
            start_rect.width(),
            start_rect.height() + 180,
        )

        self._expanded_geometry = end_rect
        self.back_button.show()
        self.back_button.raise_()

        self._anim.stop()
        self._anim.setDuration(250)
        self._anim.setStartValue(start_rect)
        self._anim.setEndValue(end_rect)
        self._anim.start()



    def restore_window(self):
        if self._saved_geometry is None:
            return

        self._anim.stop()
        self._anim.setDuration(250)
        self._anim.setStartValue(self.geometry())
        self._anim.setEndValue(self._saved_geometry)
        try:
            self._anim.finished.disconnect()
        except RuntimeError:
            pass
        self._anim.finished.connect(self.back_button.hide)
        self._anim.start()
        self._expanded_geometry = None



#-----------------------------------------------------------------------

def error_window(p_title="Error", p_text="Something Went Wrong", p_url="about:blank"):
    msg = QMessageBox()
    msg.setWindowTitle(f"{p_title}")
    msg.setText(f"{p_text}")
    msg.setIcon(QMessageBox.Icon.Warning.Critical)
    learn_more = msg.addButton("Learn More", QMessageBox.ButtonRole.HelpRole)
    msg.exec_()
    if msg.clickedButton() == learn_more:
        QDesktopServices.openUrl(QUrl(f"{p_url}"))
