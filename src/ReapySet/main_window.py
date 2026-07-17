#from PySide6.QtGui import QPalette, QColor, QFontDatabase
import os
import platform
import subprocess

from pathlib import Path
from typing import Any

from PySide6.QtCore import QPoint, QSize, QRectF, QUrl, Qt
from PySide6.QtGui import (
    QAction,
    QCursor,
    QDesktopServices,
    QIcon,
    QKeySequence,
    QPainterPath,
    QRegion,
    QShortcut,
    QShowEvent,
)
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialogButtonBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenuBar,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ReapySet.common.toml_handler import TomlHandler, CONFIG_PATH, TomlEditorDialog


from ReapySet.widgets.the_label_widget0 import (
    the_label_txt,
    get_label_stylesheet,
)
from config import MwConfig as Mwc, LogicVariables
from widgets.MwFunctions import MwFuncs as Mwf


#mainwindow
class RpsMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._language_buttons: list[QPushButton] = []
        self.setWindowTitle(Mwc.mw_title)
        self.initial_centre_pos = None


        #-----------------SIZE-AND-POS---------------------------
        self.resize(Mwc.mw_width, Mwc.mw_height())

        self.setMaximumSize(Mwc.mw_width, Mwc.mw_height())  # MAX SIZE
        self.status = self.statusBar()  # adds a status bar

        screen = QApplication.screenAt(QCursor.pos()) # screen where the cursor is at
        if screen is None:
            screen = QApplication.primaryScreen()  # fallback
        print(f"Screen: {screen.name()}, geometry: {screen.availableGeometry()}")
        print(f"Cursor pos: {QCursor.pos()}")
        # ----------------- PALETTE --------------------------#
        """Disabled due inability to work on os theme changes"""

        #std_palette: QPalette = self.palette()
        #std_palette.setColor(QPalette.ColorRole.Window, QColor(248, 248, 245))
        #std_palette.setColor(QPalette.ColorRole.Button, QColor(241, 241, 239))
        #self.setPalette(std_palette)

        #self.setAutoFillBackground(True)
        # -------------------- END-PALETTE -----------------------------#
        # ---------------------- MENUBAR -------------------------------#
        mw_menubar: QMenuBar = self.menuBar()
        isnative_menubar: bool = TomlHandler.toml_get(CONFIG_PATH, "advanced", "nativeMenubar") # noqa
        mw_menubar.setNativeMenuBar(isnative_menubar)
        # Main menus
        app_menu = mw_menubar.addMenu("&ReapySet")

        file_menu = mw_menubar.addMenu("&File")

        view_menu = mw_menubar.addMenu("&View")
        help_menu = mw_menubar.addMenu("&Help")

        # ---------------------- APP / SETTINGS ------------------------#

        open_settings_action = QAction("&Settings...", self)
        open_settings_action.setShortcut(QKeySequence.StandardKey.Preferences)
        open_settings_action.setMenuRole(QAction.MenuRole.PreferencesRole)
        open_settings_action.triggered.connect(lambda: (
                TomlHandler.ensure_config_exists(),
                TomlEditorDialog(CONFIG_PATH, self).exec()
            ))

        quit_action = QAction("&Quit ReapySet", self)
        quit_action.setShortcut(QKeySequence.StandardKey.Quit)
        quit_action.triggered.connect(self.close)
        quit_action.setMenuRole(QAction.MenuRole.QuitRole)

        app_menu.addAction(open_settings_action)
        app_menu.addSeparator()
        app_menu.addAction(quit_action)

        # ---------------------- EDIT ----------------------------------#
        """file_menu.addAction(QAction("Cu&t", self))
        edit_menu.addAction(QAction("&Copy", self))
        edit_menu.addAction(QAction("&Paste", self))
        edit_menu.addSeparator()
        edit_menu.addAction(QAction("Select &All", self))"""
        file_menu.addSeparator()
        locate_config_action = QAction("&Locate config.toml file", self)
        locate_config_action.triggered.connect(
            lambda: self.reveal_in_file_manager(CONFIG_PATH)
        )
        file_menu.addAction(locate_config_action)
        find_socket_action = QAction("&Locate socket file", self)
        find_socket_action.triggered.connect(
            lambda: self.reveal_in_file_manager(TomlHandler._temp_dir)
        )
        file_menu.addAction(find_socket_action)



        # ---------------------- VIEW ----------------------------------#
        reset_window_pos_action = QAction("&Reset Window Position", self)
        reset_window_pos_action.triggered.connect(self.centre_mwindow)

        view_menu.addAction(reset_window_pos_action) # todo bug puts i too hig if reposed when expaned

        # ----------------- HELP & LEGAL STUFFS ------------------------#
        github_action = QAction("&GitHub Repository", self)
        github_action.triggered.connect(
            lambda: QDesktopServices.openUrl(
                QUrl("https://github.com/Alessandrx204/ReapySet")
            )
        )

        license_action = QAction("&ReapySet License", self)
        license_action.triggered.connect(
            lambda: QDesktopServices.openUrl(
                QUrl("https://github.com/Alessandrx204/ReapySet/blob/Master/LICENSE")
            )
        )

        third_party_licenses_action = QAction("&Open Source Licenses", self)
        third_party_licenses_action.triggered.connect(
            lambda: QDesktopServices.openUrl(
                QUrl("https://github.com/Alessandrx204/ReapySet/blob/Master/LICENSE-3RD-PARTY.md")
            )
        )

        about_action = QAction("&About ReapySet", self)
        about_action.setMenuRole(QAction.MenuRole.AboutRole)
        about_action.triggered.connect(self.show_about_dialog)

        help_menu.addAction(github_action)
        help_menu.addSeparator()
        help_menu.addAction(license_action)
        help_menu.addAction(third_party_licenses_action)
        help_menu.addSeparator()
        help_menu.addAction(about_action)
        # -------------------- END-MENUBAR ------------------------------#
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

        # ---------------- GitHub ----------------
        self.w1_github_input = QLineEdit()
        self.w1_github_input.setEnabled(False)
        self.w1_github_input.setPlaceholderText(
            Mwc.Widget1.github_box_placeholder_txt
        )

        self.w1_github_input.setStyleSheet(Mwc.Widget1.QlineEditQSS)
        github_field = Mwf.labeled_field(
            Mwc.Widget1.github_box_top_label,
            self.w1_github_input,
        )

        self.widget1Layout.addWidget(github_field)

        # ---------------- Project path ----------------

        self.w1_path_input = QLineEdit()

        self.w1_path_input.setPlaceholderText(

            Mwc.Widget1.path_box_placeholder_txt

        )

        self.w1_path_input.setStyleSheet(Mwc.Widget1.QlineEditQSS)

        path_field = Mwf.labeled_field(

            Mwc.Widget1.path_box_top_label,

            self.w1_path_input,

        )

        self.widget1Layout.addWidget(path_field)
        self.w1_path_input.setPlaceholderText(Mwc.Widget1.path_box_placeholder_txt)
        self.w1_path_input.setStyleSheet(f"{Mwc.Widget1.QlineEditQSS}")

        raw_default_path: Any | None = TomlHandler.toml_get(
            CONFIG_PATH,
            "general",
            "default_project_path",
        )
        projects_folder_name: str | None = TomlHandler.toml_get(
            CONFIG_PATH,
            "general",
            "default_projects_folder"
        )

        if isinstance(raw_default_path, str) and raw_default_path.strip():

            project_path = Path(raw_default_path).expanduser() # converts ~ to the user's home directory .

        else:

            project_path = Path.home() / (projects_folder_name if projects_folder_name else "")
        project_path_txt: str = str(project_path) + os.sep
        # if you see a double call dont worry its normal

        self.w1_path_input.setText(project_path_txt)
        self.w1_path_input.setTextMargins(0, 0, 50, 0)  # adds a white space on the right
        self.w1_path_input.setCursorPosition(len(project_path_txt))
        self.w1_path_input.setToolTip(project_path_txt)
        TomlHandler.toml_edit("global", "project_path", project_path_txt)



        # -------------------------------- Cookiecutter template ------------------------------------#

        self.w1_cookiecutter_boilerplates_box = QLineEdit()
        self.w1_cookiecutter_boilerplates_box.setEnabled(True)
        self.w1_cookiecutter_boilerplates_box.setPlaceholderText(
            Mwc.Widget1.boilerplates_box_placeholder_txt
        )
        self.w1_cookiecutter_boilerplates_box.setStyleSheet(
            Mwc.Widget1.QlineEditQSS
        )
        cc_path_field = Mwf.labeled_field(
            Mwc.Widget1.sample_box_top_label,
            self.w1_cookiecutter_boilerplates_box,
        )
        self.widget1Layout.addWidget(cc_path_field)



        #--- doubleclick actions ------#
        self.w1_path_input.mouseDoubleClickEvent = (
            lambda event: Mwf.choose_project_path_qldialogue(self, self.w1_path_input)
        )

        path_field.mouseDoubleClickEvent = (
            lambda event: Mwf.choose_project_path_qldialogue(self, self.w1_path_input)
        )

        self.w1_cookiecutter_boilerplates_box.mouseDoubleClickEvent = (
            lambda event: Mwf.choose_project_path_qldialogue(self, self.w1_cookiecutter_boilerplates_box, p_caption="Choose a Valid Coockiecutter template folder")
        )

        cc_path_field.mouseDoubleClickEvent = (
            lambda event: Mwf.choose_project_path_qldialogue(self, self.w1_cookiecutter_boilerplates_box,  p_caption="Choose a Valid Coockiecutter template folder")
        )
        #------------ end doubleclick actions -----------------#


        self.w1_cookiecutter_boilerplates_box.textChanged.connect(self._on_sample_input_changed)

        self.w1_select_editor: QComboBox = QComboBox()
        self.widget1Layout.addWidget(Mwf.labeled_field("", self.w1_select_editor))
        # deprecated: self.w1_select_editor.addItems(Mwc.Widget1.select_editor_Combobox_entry)
        self.w1_select_editor.addItems(LogicVariables.EditorCmd.get_all_editors())
        TomlHandler.toml_edit(
            "global", "fav_editor",
            f"{self.w1_select_editor.currentText().lower()}"
                             )# saves current editor_page on boot
        self.w1_select_editor.currentTextChanged.connect(
            #saves in the toml common/toml_playground/toml_playground_cc.toml in the fav editor_page section for easy parsing
            lambda p_text: TomlHandler.toml_edit("global", "fav_editor", f"{p_text}")
        )

        self.widget1.setLayout(self.widget1Layout)
        self.widget1.setEnabled(True)
        outer_layout.addWidget(self.central_widget2, 0)
        outer_layout.addWidget(self.widget3_stacked, 1)
        self.widget3_stacked.setStyleSheet(Mwc.Widget3.widget3_qss)
        self.widget3_stacked.setVisible(True)
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

            self.handle_confirm_clicked # it will be called in confirm_button_logic.py

        )

        self.confirm_shortcut: QShortcut = QShortcut(QKeySequence("Ctrl+Return"), self)
        self.confirm_shortcut.setContext(Qt.ShortcutContext.ApplicationShortcut)
        self.confirm_shortcut.activated.connect(self.handle_confirm_clicked) # noqa
        self.confirm_shortcut_numpad: QShortcut = QShortcut(QKeySequence("Ctrl+Enter"), self)
        self.confirm_shortcut_numpad.setContext(Qt.ShortcutContext.ApplicationShortcut)
        self.confirm_shortcut_numpad.activated.connect(self.handle_confirm_clicked) # noqa


        # it may be useful someday
        #self.cancel_button: QPushButton = self.button_box.button(QDialogButtonBox.StandardButton.Cancel)

        self.back_button: QPushButton = QPushButton("Back")
        self.back_button.setEnabled(False)

        self.confirm_button.setEnabled(False)
        self.confirm_button.setToolTip(self.confirm_shortcut
                                       .key().toString(QKeySequence.SequenceFormat.NativeText)+"\n(if enabled)"
                                       ) #displays the right shortcut
        #self.cancel_button.setEnable d(False)
        # noinspection PyStatementEffect


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

        # TODO: decide if this is worth keeping or not (most likely not)
        self.w1_path_input.textChanged.connect(
            lambda text: TomlHandler.toml_edit("global",
                                               "folder_name",
                                               os.path.basename(os.path.normpath(text)))
        )

        Mwf.connect_qlineedit(self.w1_cookiecutter_boilerplates_box, "cookiecutter", "template_path")
        Mwf.connect_qlineedit(self.w1_github_input, "global", "github_repo_link")
        self.setMinimumSize(Mwc.mw_width, Mwc.mw_height())



    #---------------- INIT END ---------------------#
    def centre_mwindow(self) -> None:
        screen = QApplication.screenAt(QCursor.pos())
        # Tries the application's primary screen as a fallback.
        if screen is None:
            screen = QApplication.primaryScreen()

        # If no screen is available even after the fallback, return.
        if screen is None:
            return

        if self.initial_centre_pos is None:
            frame = self.frameGeometry()

            frame.moveCenter(screen.availableGeometry().center())

            self.initial_centre_pos = frame.topLeft()

        current_pos: QPoint = QPoint(self.initial_centre_pos)
        current_pos.setY(current_pos.y() + Mwc.mw_y_offset)  #offsets 150 px to Y - is up + is down

        self.move(current_pos)

    def reveal_in_file_manager(self, target_path):
        path = Path(target_path).resolve()

        if not path.exists():
            msg = QMessageBox(self)

            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("File not found")
            msg.setText("Impossible to find the file or directory.")
            msg.setInformativeText(f"the path:\n{path}\n  doesnt seem to exist")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)

            msg.exec()
            return

        sys_ = platform.system()

        if sys_ == "Windows":
            subprocess.run(["explorer", "/select,", str(path)])
        elif sys_ == "Darwin":  # macOS
            subprocess.run(["open", "-R", str(path)])
        else:  # Linux
            subprocess.run(["xdg-open", str(path.parent)])

        #------------------ END MENU BAR UTILS ---------------------------#


    def _on_sample_input_changed(self, p_text: str):
        if p_text:
            self.w1_cookiecutter_boilerplates_box.setTextMargins(0, 0, 50, 0)

        else:
            self.w1_cookiecutter_boilerplates_box.setTextMargins(0, 0, 0, 0)  # dynamic padding
        # ------------------- END BUTTONS -------------------


    def resizeEvent(self, event):  #resizeEvent is a special method of Qt:
        # it gets called automatically every time the window size changes.
        super().resizeEvent(event)
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.widget3_stacked.rect()), 10.0, 10.0) # staked widget corners
        region = QRegion(path.toFillPolygon().toPolygon())
        self.widget3_stacked.setMask(region)

    def showEvent(self, event: QShowEvent):
        """ gets the centre before is expaned so it can always refer to the OG centre
        instead of the actual centre which shift when the window is expanded."""
        super().showEvent(event)
        if self.initial_centre_pos is None:
            self.centre_mwindow()



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
            self.w1_cookiecutter_boilerplates_box.setText(folder)

    #_connect_qlineedit replaced with Mwf.connect_qlineedit

    def show_about_dialog(self) -> None:
        QMessageBox.about(
            self,
            "About ReapySet",
            (
                "<h3>ReapySet</h3>"
                "<p>Version: beta 5.0</p>"
                "<p>Project setup and environment launcher.</p>"
                "<p>Powered by Open source software</p>"
                "<p>Copyright © Alessandra 2026</p>"
            )
        )



#-----------------------------------------------------END-MAIN-WINDOW--CLASS-------------------------------------------#
