#from PySide6.QtGui import QPalette, QColor, QFontDatabase
import os
import sys
from pathlib import Path

from PySide6.QtCore import QPoint, QSize, Qt, QRectF
from PySide6.QtGui import QIcon, QFontMetrics, QPainterPath, QRegion, QCursor
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QGridLayout, QDialogButtonBox, \
    QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout, QLineEdit, QComboBox

import logic_mainwindow
import widgets.widget1.sample_picker as sample_picker
from ReapySet.widgets.the_label_widget0 import the_label_txt, get_label_stylesheet
from common.toml_handler import TomlHandler
from config import MwConfig as Mwc, LogicVariables
from widgets.MwFuctions import MwFuncs as Mwf


#mainwindow
class RsMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._language_buttons = None
        self.setWindowTitle(Mwc.mw_title)


        #-----------------SIZE-AND-POS---------------------------
        self.resize(Mwc.mw_width, Mwc.mw_height)

        self.setMaximumSize(Mwc.mw_width, Mwc.mw_height)  # MAX SIZE
        self.status = self.statusBar()  # adds a status bar

        frame = self.frameGeometry()
        screen = QApplication.screenAt(QCursor.pos())  # schermo dove c'è il cursore
        if screen is None:
            screen = QApplication.primaryScreen()  # fallback
        print(f"Screen: {screen.name()}, geometry: {screen.availableGeometry()}")
        print(f"Cursor pos: {QCursor.pos()}")
        centre = screen.availableGeometry().center()
        frame.moveCenter(centre)

        top_left: QPoint = frame.topLeft()
        top_left.setY(top_left.y() + Mwc.mw_y_offset)  #offsets 150 px to Y - is up + is down

        self.move(top_left)
        # ----------------- PALETTE --------------------------#
        """Disabled due inability to work on os theme changes"""

        #std_palette: QPalette = self.palette()
        #std_palette.setColor(QPalette.ColorRole.Window, QColor(248, 248, 245))
        #std_palette.setColor(QPalette.ColorRole.Button, QColor(241, 241, 239))
        #self.setPalette(std_palette)

        #self.setAutoFillBackground(True)
        # ----------------- END-PALETTE --------------------------#


        #----------------------------------------------------------------#
        #self._button_labels_list: list[str] = Mwc.LangBtnWidget.button_list
        self.button_labels_dict: dict[str, list] = Mwc.LangBtnWidget().button_dict
        self._enabled_buttons = Mwc.LangBtnWidget().enabled_btns  #enabled buttons list
        self.widget0 = QWidget()  # <-- top Widget containts stuffs like "hello" news titles etc...
        self.widget1 = QWidget()  #<--- stuff like GitHub and path
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
        self.w1_github_input.setEnabled(False) #GitHub enabled y/n?
        self.widget1Layout.addWidget(Mwf.labeled_field(Mwc.Widget1.github_box_top_label, self.w1_github_input))
        self.w1_github_input.setPlaceholderText(Mwc.Widget1.github_box_placeholder_txt)
        self.w1_github_input.setStyleSheet(Mwc.Widget1.QlineEditQSS)
        self.w1_path_input = QLineEdit()
        self.widget1Layout.addWidget(Mwf.labeled_field(f"{Mwc.Widget1.path_box_top_label}", self.w1_path_input))
        self.w1_path_input.setPlaceholderText(Mwc.Widget1.path_box_placeholder_txt)
        self.w1_path_input.setStyleSheet(f"{Mwc.Widget1.QlineEditQSS}")

        text_ = str(Path.home() / "Projects/")

        metrics = QFontMetrics(self.w1_path_input.font())
        elided = metrics.elidedText(text_, Qt.TextElideMode.ElideLeft, self.w1_path_input.width())

        self.w1_path_input.setText(
            elided + "/" if not sys.platform.startswith("win") else elided + "\\")  #text that scorlls on the left
        TomlHandler.toml_edit("global", "project_path", self.w1_path_input.text())
        self.w1_path_input.setTextMargins(0, 0, 50, 0)  # adds a white space

        self.w1_boilerplates_box = QLineEdit()
        self.w1_boilerplates_box.setEnabled(False)  # boilerplates enabled y/n?
        self.w1_boilerplates_box.setPlaceholderText(Mwc.Widget1.boilerplates_box_placeholder_txt)

        self.widget1Layout.addWidget(Mwf.labeled_field(Mwc.Widget1.sample_box_top_label, self.w1_boilerplates_box))

        self.w1_boilerplates_box.setStyleSheet(Mwc.Widget1.QlineEditQSS)

        self.w1_browse_bplates_button = QPushButton(Mwc.Widget1.browse_button_text)
        self.w1_browse_bplates_button.setEnabled(False)
        self.widget1Layout.addWidget(Mwf.labeled_field("", self.w1_browse_bplates_button))  #moves down a bit the button by gioving it a null text in a QVBox
        self.w1_browse_bplates_button.clicked.connect(
            lambda: self._on_folder_selected(sample_picker.pick_folder(self))
        )

        self.w1_boilerplates_box.textChanged.connect(self._on_sample_input_changed)

        self.w1_select_editor: QComboBox = QComboBox()
        self.widget1Layout.addWidget(Mwf.labeled_field("", self.w1_select_editor))
        # deprecated: self.w1_select_editor.addItems(Mwc.Widget1.select_editor_Combobox_entry)
        self.w1_select_editor.addItems(LogicVariables.EditorCmd.get_all_editors())
        TomlHandler.toml_edit(
            "global", "fav_editor",
            f"{self.w1_select_editor.currentText().lower()}"
                             )# saves current editor_page on boot
        self.w1_select_editor.currentTextChanged.connect(
            #saves in the toml common/toml_playground/toml_playground_cc.toml in the fav editor_page section .lower() for easy parsing
            lambda p_text: TomlHandler.toml_edit("global", "fav_editor", f"{p_text.lower()}")
        )

        self.widget1.setLayout(self.widget1Layout)
        self.widget1.setEnabled(True)
        outer_layout.addWidget(self.central_widget2, 0)
        outer_layout.addWidget(self.widget3_stacked, 1)
        self.widget3_stacked.setStyleSheet(Mwc.Widget3.widget3_qss)
        self.widget3_stacked.setEnabled(True)
        self.setCentralWidget(wrapper)

        # ------------------------ END TOP WIDGET --------------------------#
        # ------------------- TOOLBAR / STATUSBAR BUTTONS ------------------#
        self.statusBar().setContentsMargins(8, 0, 8, 0) # padding
        # noinspection PyTypeChecker
        self.button_box: QDialogButtonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            #| QDialogButtonBox.StandardButton.Cancel
        )

        # 2. gets reference to internal buttons to configure them
        self.confirm_button: QPushButton = self.button_box.button(QDialogButtonBox.StandardButton.Ok)
        self.confirm_button.setText("Confirm")
        self.confirm_button.clicked.connect(

            self.handle_confirm_clicked

        )
        #self.cancel_button: QPushButton = self.button_box.button(QDialogButtonBox.StandardButton.Cancel)

        self.back_button: QPushButton = QPushButton("Back")
        self.back_button.setEnabled(False)

        self.confirm_button.setEnabled(False)
        #self.cancel_button.setEnabled(False)
        # noinspection PyStatementEffect
        self.back_button.clicked.connect(
            lambda: (
                logic_mainwindow.LogicMainWindow.handle_back_button(self), #type: ignore (since pyright
                                                                        # doesnt catch up on inheritance)
                TomlHandler.set_disabled_all_langs(),  # noqa linter complains it doesnt return anything
                                                                            # but that's the whole point,
                                                                        # no need to return anything there
            )
        )

        #self.button_box.accepted.connect(lambda : ConfirmButtonLogic().on_confirm_clicked())
        #self.confirm_button.clicked.connect(self.handle_confirm_clicked)
        #self.button_box.rejected.connect(lambda: print("Cancel pressed"))
        #self.button_box.rejected.connect(lambda: (logic_mainwindow.LogicMainWindow.handle_back_button(self), # type ignore
                                                  #TomlHandler.set_disabled_all_langs())) # noqa back button clone (for now)

        # adds to status bar
        #self.back_button.setStyleSheet("margin-left: 2px;")
        self.statusBar().addWidget(self.back_button)
        self.statusBar().addPermanentWidget(self.button_box)  # on the right ( for whatever reason)
        # ------------------- END TOOLBAR / STATUSBAR BUTTONS ------------------#
        Mwf.connect_qlineedit(self.w1_path_input, "global", "project_path")


        #TODO: decide if this is worth keeping or not (most likely not)
        self.w1_path_input.textChanged.connect(
            lambda text: TomlHandler.toml_edit("global",
                                               "folder_name",
                                               os.path.basename(os.path.normpath(text)))
        )

        Mwf.connect_qlineedit(self.w1_boilerplates_box, "global", "boilerplate_project_path")
        Mwf.connect_qlineedit(self.w1_github_input, "global", "github_repo_link")
        self.setMinimumSize(Mwc.mw_width, Mwc.mw_height)


    #---------------- INIT END ---------------------#


    def _on_sample_input_changed(self, text: str):
        if text:
            self.w1_boilerplates_box.setTextMargins(0, 0, 50, 0)
        else:
            self.w1_boilerplates_box.setTextMargins(0, 0, 0, 0)  # dynamic padding
        # ------------------- END BUTTONS -------------------

        #self.setCentralWidget(self.central_widget2)  # <-- not just setLayout() directly

    def resizeEvent(self, event):  #resizeEvent is a special method of Qt:
        # it gets called automatically every time the window size changes.
        super().resizeEvent(event)
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.widget3_stacked.rect()), 10.0, 10.0)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.widget3_stacked.setMask(region)



    def create_language_buttons(self,
                                p_button_labels_dict: dict[str, list],
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
            button.setProperty("lang_id", abbrev)
            button.setProperty("selected", False)
            button.setStyleSheet(Mwc.LangBtnWidget.lang_btns_qss)#?
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

    def _on_folder_selected(self, folder: str):
        if folder:
            self.usr_selected_folder = folder
            self.w1_boilerplates_box.setText(folder)

    #_connect_qlineedit replaced with Mwf.connect_qlineedit



#-----------------------------------------------------END-MAIN-WINDOW--CLASS-------------------------------------------#
