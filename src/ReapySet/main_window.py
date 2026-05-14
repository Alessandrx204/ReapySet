#from PySide6.QtGui import QPalette, QColor, QFontDatabase
import sys
from pathlib import Path

from PySide6.QtCore import QPoint, QSize, Qt
from PySide6.QtGui import QIcon, QFontMetrics
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QGridLayout, QDialogButtonBox, \
    QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout, QLineEdit, QComboBox

import logic_mainwindow
from ReapySet.widgets.the_label_widget0 import the_label_txt, get_label_stylesheet
from config import MwConfig as Mwc


# import qdarktheme


#mainwindow
class RsMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._language_buttons = None
        self.setWindowTitle(Mwc.mw_title)

        #-----------------SIZE-AND-POS---------------------------
        self.resize(Mwc.mw_width, Mwc.mw_height)

        self.setMaximumSize(Mwc.mw_width, Mwc.mw_height) # MAX SIZE
        self.status = self.statusBar() # adds a status bar

        frame = self.frameGeometry()
        centre = QApplication.primaryScreen().availableGeometry().center()
        frame.moveCenter(centre)

        top_left: QPoint = frame.topLeft()
        top_left.setY(top_left.y() +Mwc.mw_y_offset) #offsets 150 px to Y - is up + is down

        self.move(top_left)
        # ----------------- PALETTE --------------------------#
        """Disabled due inability to work on os theme changes"""
        #std_palette: QPalette = self.palette()
        #std_palette.setColor(QPalette.ColorRole.Window, QColor(248, 248, 245))
        #std_palette.setColor(QPalette.ColorRole.Button, QColor(241, 241, 239))
        #self.setPalette(std_palette)

        #self.setAutoFillBackground(True)
        # ----------------- END-PALETTE --------------------------#


        #-----------------END-SIZE-AND-POS-BLOCK--------------------------#
        #self._button_labels_list: list[str] = Mwc.LangBtnWidget.button_list
        self.button_labels_dict: dict[str, list] = Mwc.LangBtnWidget().button_dict
        self._enabled_buttons = Mwc.LangBtnWidget().enabled_btns #enabled buttons list
        self.widget0 = QWidget()  # <-- top Widget containts stuffs like "hello" news titles etc...
        self.widget1 = QWidget()  #<--- stuff like github and path
        self.central_widget2 = QWidget()  # <-- QMainWindow needs a central window
        self.widget3_stacked = QStackedWidget()  # <-- Widget for the lower part of the Window
        self.main_layout = QGridLayout(self.central_widget2)
        # ------------------- TOOLBAR / STATUSBAR BUTTONS ------------------#
        self.central_widget2.setFixedHeight(Mwc.LangBtnWidget.cw_height)
        #self.widget1.setFixedHeight(Mwc.Widget1.w1_height)
        # ------------------------ WIDGET SET --------------------------#
        wrapper = QWidget()
        outer_layout: QVBoxLayout = QVBoxLayout(wrapper)
        big_label = QLabel(the_label_txt)

        big_label.setStyleSheet(get_label_stylesheet())  #src/the_label_widget0.py


        outer_layout.addWidget(big_label)
        outer_layout.addWidget(self.widget1)


        self.widget1Layout = QHBoxLayout()


        self.w1_github_input = QLineEdit()
        self.widget1Layout.addWidget(self.w1_github_input)
        self.w1_github_input.setPlaceholderText("github repository URL...")
        self.w1_github_input.setStyleSheet(Mwc.Widget1.QlineEditQSS)
        self.w1_path_input = QLineEdit()
        self.widget1Layout.addWidget(self.w1_path_input)
        self.w1_path_input.setPlaceholderText("Project Path...")
        self.w1_path_input.setStyleSheet(f"{Mwc.Widget1.QlineEditQSS}")
        #self.w1_path_input.setText(str(Path.home() / "Projects/"))

        text_ = str(Path.home() / "Projects/")

        metrics = QFontMetrics(self.w1_path_input.font())
        elided = metrics.elidedText(text_, Qt.TextElideMode.ElideLeft, self.w1_path_input.width())

        self.w1_path_input.setText(elided + "/" if not sys.platform.startswith("win") else elided+"\\" ) #text that scorlls on the left
        self.w1_path_input.setTextMargins(0, 0, 50, 0) # adds a white space

        self.w1_sample_input = QLineEdit()
        self.w1_sample_input.setPlaceholderText("Sample project?...")
        self.widget1Layout.addWidget(self.w1_sample_input)
        self.w1_sample_input.setStyleSheet(Mwc.Widget1.QlineEditQSS)

        self.w1_browse_samples_button = QPushButton("Browse...")
        self.widget1Layout.addWidget(self.w1_browse_samples_button)

        self.w1_select_editor = QComboBox()
        self.widget1Layout.addWidget(self.w1_select_editor)
        self.w1_select_editor.addItems(["VSCode", "Pycharm", "Godot", "Intellij IDEA ", "Zed", "Sublime Text", "Notepad++","nVim"])



        self.widget1.setLayout(self.widget1Layout)
        self.widget1.setEnabled(True)
        outer_layout.addWidget(self.central_widget2, 0)
        outer_layout.addWidget(self.widget3_stacked, 1)
        self.widget3_stacked.setStyleSheet("background-color:"
                                           " rgb(255, 255, 255);"
                                           " border-radius: 10px; ") # border: 5px solid rgb(x, y, z);
        self.widget3_stacked.setEnabled(False)
        self.setCentralWidget(wrapper)

        # ------------------------ END TOP WIDGET --------------------------#
        # ------------------- TOOLBAR / STATUSBAR BUTTONS ------------------#

        # noinspection PyTypeChecker
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )


        # 2. gets reference to internal buttons to configure them
        self.confirm_button = self.button_box.button(QDialogButtonBox.StandardButton.Ok)
        self.confirm_button.setText("Confirm")
        #self.confirm_button.setIcon(QIcon(pythonlogo))

        self.cancel_button = self.button_box.button(QDialogButtonBox.StandardButton.Cancel)


        self.back_button = QPushButton("Back")
        self.back_button.setEnabled(False)



        self.confirm_button.setEnabled(False)
        self.cancel_button.setEnabled(False)


        self.back_button.clicked.connect(
            lambda: logic_mainwindow.LogicMainWindow.handle_back_button(self)  # type: ignore
        )

        self.button_box.accepted.connect(lambda: print("Confirm pressed"))
        self.button_box.rejected.connect(lambda: print("Cancel pressed"))

        # adds to status bar
        #self.back_button.setStyleSheet("margin-left: 2px;")
        self.statusBar().addWidget(self.back_button)
        self.statusBar().addPermanentWidget(self.button_box)  # on the right ( for whatever reason)

        # ------------------- END BUTTONS -------------------





        #self.setCentralWidget(self.central_widget2)  # <-- not just setLayout() directly

    def resizeEvent(self, event): #resizeEvent is a special method of Qt:
        # it gets called automatically every time the window size changes.
        super().resizeEvent(event)
        ...

    def create_language_buttons(self,
                                p_button_labels_dict: dict[str, list],  # ← tipo aggiornato
                                p_max_btn_per_row: int,
                                p_window_layout: QGridLayout) -> list[QPushButton]:
        """Creates and places language buttons in a brick-like structure."""
        buttons: list[QPushButton] = []

        for i, (name, btn_data) in enumerate(p_button_labels_dict.items()):
            abbrev = btn_data[0]  # ← get abbrev from 1st element
            logo_path = btn_data[1]  #logo is at the index 2 of the list

            btn_in_row = i // p_max_btn_per_row
            index_column = i % p_max_btn_per_row

            row_offset = 1 if (btn_in_row % 2 == 1) else 0
            col = index_column * 2 + row_offset

            button = QPushButton(name)
            if logo_path is not None:
                button.setIcon(QIcon(str(logo_path)))
                button.setIconSize(QSize(25, 15))
            button.setEnabled(i in self._enabled_buttons)

            button.clicked.connect(
                lambda checked, val=abbrev: self.handle_event(val)  # type: ignore[attr-defined]
            )

            p_window_layout.addWidget(button, btn_in_row, col, 1, 2)
            buttons.append(button)

        self._language_buttons = buttons
        return buttons
#-----------------------------------------------------END-MAIN-WINDOW--CLASS-------------------------------------------#

