#from PySide6.QtGui import QPalette, QColor, QFontDatabase
from typing import cast
from config import MwConfig as Mwc

from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QGridLayout, QDialogButtonBox, \
    QVBoxLayout, QLabel, QStackedWidget
import logic_mainwindow
from the_label_widget0 import the_label_txt, get_label_stylesheet


# import qdarktheme


#mainwindow
class RsMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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
        self._button_labels_list: list[str] = Mwc.LangBtnWidget.button_list
        self._enabled_buttons = Mwc.LangBtnWidget.enabled_btns #enabled buttons list
        self.widget0 = QWidget()  # <-- top Widget containts stuffs like "hello" news titles etc...
        self.widget1 = QWidget()  #<--- stuff like github and path
        self.central_widget2 = QWidget()  # <-- QMainWindow needs a central window
        self.widget3_stacked = QStackedWidget()  # <-- Widget for the lower part of the Window
        self.main_layout = QGridLayout(self.central_widget2)
        # ------------------- TOOLBAR / STATUSBAR BUTTONS ------------------#
        self.central_widget2.setFixedHeight(Mwc.LangBtnWidget.cw_height)
        self.widget1.setFixedHeight(Mwc.Widget1.w1_height)
        # ------------------------ WIDGET SET --------------------------#
        wrapper = QWidget()
        outer_layout: QVBoxLayout = QVBoxLayout(wrapper)
        big_label = QLabel(the_label_txt)

        big_label.setStyleSheet(get_label_stylesheet())  #src/the_label_widget0.py

        outer_layout.addWidget(big_label)
        outer_layout.addWidget(self.widget1)
        outer_layout.addWidget(self.central_widget2, 0)
        outer_layout.addWidget(self.widget3_stacked, 1)
        self.widget3_stacked.setStyleSheet("background-color:"
                                           " rgb(255, 255, 255);"
                                           " border-radius: 10px; ") # border: 5px solid rgb(x, y, z);
        self.widget3_stacked.setEnabled(False)
        self.setCentralWidget(wrapper)
        # ------------------------ END TOP WIDGET --------------------------#
        # ------------------- TOOLBAR / STATUSBAR BUTTONS ------------------#


        self.button_box = (
            QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )) #ignore


        # 2. gets reference to internal buttons to configure them
        self.confirm_button = self.button_box.button(QDialogButtonBox.StandardButton.Ok)
        self.confirm_button.setText("Confirm")
        self.cancel_button = self.button_box.button(QDialogButtonBox.StandardButton.Cancel)


        self.back_button = QPushButton("Back")
        self.back_button.setEnabled(False)



        self.confirm_button.setEnabled(False)
        self.cancel_button.setEnabled(False)


        #self.back_button.clicked.connect(lambda: print("Back pressed"))
        self.back_button.clicked.connect(
            lambda : logic_mainwindow.LogicMainWindow.handle_back_button(
                cast(logic_mainwindow.LogicMainWindow, self)
            )
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
            p_button_labels_list: list[str],
            p_max_btn_per_row: int,
            p_window_layout: QGridLayout) -> list[QPushButton]:
        """Creates and places language buttons in a brick-like structure."""
        buttons: list[QPushButton] = []

        for i, btn_label in enumerate(p_button_labels_list):
            btn_in_row = i // p_max_btn_per_row
            index_column = i % p_max_btn_per_row

            # Offset of 1 column for odd rows like (0, 1, 2...)
            row_offset = 1 if (btn_in_row % 2 == 1) else 0
            col = index_column * 2 + row_offset

            button = QPushButton(btn_label)
            button.setEnabled(True) if i in self._enabled_buttons else button.setEnabled(False)

            # self is RsMainWindow, but LogicMainWindow inherits from it, so at runtime
            # self is also a valid LogicMainWindow. cast() just tells VSCode that so it
            # stops raising a type warning — it has zero effect on actual execution.
            button.clicked.connect(
                lambda checked, txt=btn_label: logic_mainwindow.LogicMainWindow.handle_event(
                    cast(logic_mainwindow.LogicMainWindow, self), txt
                )
            )


            p_window_layout.addWidget(button, btn_in_row, col, 1, 2) #setter
            buttons.append(button)

        self._language_buttons = buttons
        return buttons

    @property
    def button_labels_list(self):
        return self._button_labels_list

#-----------------------------------------------------END-MAIN-WINDOW--CLASS-------------------------------------------#

