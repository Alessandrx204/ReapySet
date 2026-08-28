from PySide6.QtCore import QRect, QPropertyAnimation, QTimer
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import QMenuBar
from tomlkit import TOMLDocument

import ReapySet.widgets.widgets3.widget31_python.stacked_widget3 as SW3  # noqa
from ReapySet.common.core_logic.confirm_button_logic import ConfirmButtonLogic
from ReapySet.common.toml_handler import TomlHandler
from ReapySet.config import MwConfig as Mwc
from ReapySet.main_window import RpsMainWindow
from ReapySet.common.core_logic.MwFunctions import MwFuncs as Mwf
from ReapySet.widgets.floating_widgets import MwAdditions
from ReapySet.common.core_logic.logging import logger


def switch_stacked_widget():
    ...

class LogicMainWindow(RpsMainWindow):
    def __init__(self):
        super().__init__()
        self.anim = QPropertyAnimation(self, b"geometry") #type: ignore
        self.original_geometry = self.geometry()
        self.og_height = self.height()
        self.og_width = self.width()

        #self.python_gen_widget = SW3.PythonGenWidget(self)
        #self.python_gen_widget.hide()
        self.lang_btn_cfg = Mwc.LangBtnWidget()
        self._lang_widget = None
        self.confirm_logic = ConfirmButtonLogic()
        self.confirm_busy: bool = False
        self.back_button.clicked.connect(self.handle_back_button)
        #----Widgets on top -----#
        self.additions = MwAdditions(self)
        self.additions.add_trans_flag(size=20)
        self.additions.add_settings_button(size=22)

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        self.additions.reposition_all()
        # ----Widgets on top -----#
    def expand_window(self, p_language: str) -> None:

        if self._lang_widget is not None:# if exists
            return

        lang_id: str = p_language  # "PY" it's already the id

        specific_h_expansion: int = Mwc.mw_height_expansion

        match lang_id:
            case "PY":
                TomlHandler.set_enabled_1lang("python")
                self._lang_widget = SW3.PythonGenWidget(self)
                Mwf.connect_qlineedit(
                    self._lang_widget.unb_interp_qlinedit,
                    "languages",
                    "unb_interpreter_version",
                    "python",
                    p_regex_validation= r"^\d+\.\d+(\.\d+)?$" ## Prevents unsupported characters from being saved as a Python version. allowing only 1234567890 and "." basically

                )
                specific_h_expansion+=100

            case "RUST":
                print("testing rust")
                return
            case "DOTNET":
                print("testing dotnet")
                return
            case "KT":
                print("testing kotlin/java")
                return
            case "CPP":
                print("testing cpp")
                return
            case "JS":
                print("testing js")
                return
            case "GO":
                print("testing go")
                return
            case "LUA":
                print("testing lua")
                return
            case "GDSCRIPT":
                print("testing gdscript")
                return
            case _:
                print("unknown language")
                return
        expanded_height = Mwc.mw_height() + specific_h_expansion
        for btn in self._language_buttons:
            btn.setEnabled(False)
        self.setMaximumSize(Mwc.mw_width, expanded_height)

        current: QRect = self.geometry()
        expanded: QRect = QRect(current.x(), current.y(), current.width(), current.height() + specific_h_expansion)

        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(Mwc.mw_expansion_time)
        self.anim.setStartValue(current)
        self.anim.setEndValue(expanded)
        self.anim.setEasingCurve(Mwc.mw_expand_curve)
        self.anim.start()

        QTimer.singleShot(Mwc.mw_widget_enable_delay, self.show_lang_widget)

        QTimer.singleShot(Mwc.mw_expansion_time,lambda: self.setMinimumSize(Mwc.mw_width, expanded_height))
        QTimer.singleShot(Mwc.mw_expansion_time + 500, lambda: self._update_confirm_button())





    #------------------------------------------------------------------------------------------------------------------#
    def show_lang_widget(self):
        """Manages the insertion and updating of the language widget when the delay expires."""
        if self._lang_widget is None:
            return
        self.widget3_stacked.insertWidget(1, self._lang_widget)
        self.widget3_stacked.setCurrentWidget(self._lang_widget)
        self.widget3_stacked.updateGeometry()
        self.widget3_stacked.setEnabled(True)

    def collapse_window(self):
        if self._lang_widget:
            self.widget3_stacked.removeWidget(self._lang_widget)
            self._lang_widget.deleteLater()
            self._lang_widget = None
            self.confirm_button.setEnabled(False)

        menu_bar: QMenuBar = self.menuBar()

        mb_extra_h: int = menu_bar.height() if (
                    menu_bar and menu_bar.isVisible() and not menu_bar.isNativeMenuBar()) else 0

        self.setMinimumSize(Mwc.mw_width, Mwc.mw_height() + mb_extra_h)

        QTimer.singleShot(Mwc.mw_widget_enable_delay, lambda: self.widget3_stacked.setEnabled(False))

        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(Mwc.mw_collapse_time)
        self.anim.setStartValue(self.geometry())


        # Compensate for the native window frame offset.
        # QWidget.geometry() refers to the client area, while frameGeometry()
        # includes the platform window decorations, such as the title bar.
        # Without this correction, repeated geometry animations may cause a small
        # vertical drift on some window managers, especially on macOS.
        frame_offset_y: int = self.geometry().y() - self.frameGeometry().y()
        end_geometry: QRect = QRect(
            self.x(),
            self.y() + frame_offset_y,
            self.width(),
            self.og_height
        )
        self.anim.setEndValue(end_geometry)

        self.anim.setEasingCurve(Mwc.mw_collapse_curve)
        self.anim.start()


        QTimer.singleShot(
            Mwc.mw_collapse_time,
            lambda: self.setFixedSize(Mwc.mw_width, Mwc.mw_height() + mb_extra_h)
        )
        # Enable only buttons whose index appears in _enabled_buttons
        for i, btn in enumerate(self._language_buttons):
            btn.setEnabled(i in self._enabled_buttons)

    def handle_event(self, button_label_txt: str) -> None:
        for btn in self._language_buttons:
            btn.setProperty("selected", btn.property("lang_id") == button_label_txt)

            btn.style().unpolish(btn)
            btn.style().polish(btn) # forces a refresh
        self.expand_window(button_label_txt)
        self.back_button.setEnabled(True)
        logger.info(button_label_txt)



    #------------------------------------------------------------------------------------------------------------------#

    def handle_back_button(self) -> None:
        self.back_button.setEnabled(False)
        TomlHandler.set_disabled_all_langs()
        self.collapse_window()

    @staticmethod
    def handle_github_button_on_enter_pressed():
        print("downloading repo...")

    def _update_confirm_button(self) -> None:
        data: TOMLDocument = TomlHandler._toml_read()

        path_ok: bool = bool(data["global"]["project_path"].strip())
        lang_ok: bool = any(lang.get("enabled", False) for lang in data["languages"].values())

        self.confirm_button.setEnabled(path_ok and lang_ok) # path not null and a lang is enabled

    def handle_confirm_clicked(self) -> None:
        self.confirm_button.setEnabled(False)
        self.confirm_shortcut.setEnabled(False)


        if self.confirm_busy: #if is busy lets it finish
            return
        self.confirm_busy = True
        #self.confirm_button.setEnabled(False)
        #self.confirm_shortcut.setEnabled(False)
        self.confirm_shortcut_numpad.setEnabled(False)
        self.setEnabled(False)

        try:
            self.confirm_logic.on_confirm_clicked()

        finally: # awaits confirm logic to finish
            QTimer.singleShot(
                8000,
                self._unlock_confirm_btn # no () since its a reference
            )
        self.setEnabled(True) # re enables the window after confirm logic finishes



    def _unlock_confirm_btn(self) -> None:
        self.confirm_busy = False # re enables the button no longer busy
        self.confirm_shortcut.setEnabled(True)
        self.confirm_shortcut_numpad.setEnabled(True) # re enables the shortcut
        self._update_confirm_button()
