from PySide6.QtCore import QRect, QPropertyAnimation, QTimer

from main_window import RsMainWindow

from config import MwConfig as Mwc
import widgets.widgets3.widget31_python.stacked_widget3 as SW3 #noqa
from common.toml_handler import TomlHandler






def switch_stacked_widget():
    ...

class LogicMainWindow(RsMainWindow):
    def __init__(self):
        super().__init__()
        self.anim = QPropertyAnimation(self, b"geometry") #type: ignore
        self.original_geometry = self.geometry()
        self.python_gen_widget = SW3.PythonGenWidget(self)
        self.python_gen_widget.hide()
        self.lang_btn_cfg = Mwc.LangBtnWidget()
        self._lang_widget = None

    def expand_window(self, language: str):
        lang_id = language  # "PY" it's already the id

        match lang_id:
            case "PY":
                TomlHandler.set_enabled_lang("python")
                self._lang_widget = SW3.PythonGenWidget(self)
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
            case "TSJS":
                print("testing tsjs")
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

        for btn in self._language_buttons:
            btn.setEnabled(False)
        self.setMaximumSize(Mwc.mw_width, Mwc.mw_expanded_height)

        current: QRect = self.geometry()
        expanded: QRect = QRect(current.x(), current.y(), current.width(), current.height() + Mwc.mw_height_expansion)

        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(Mwc.mw_expansion_time)
        self.anim.setStartValue(current)
        self.anim.setEndValue(expanded)
        self.anim.setEasingCurve(Mwc.mw_expand_curve)
        self.anim.start()

        QTimer.singleShot(Mwc.mw_widget_enable_delay, lambda: self.widget3_stacked.setEnabled(True))
        QTimer.singleShot(Mwc.mw_widget_enable_delay, lambda: (
            self.widget3_stacked.insertWidget(1, self._lang_widget),  # ← use _lang_widget
            self.widget3_stacked.updateGeometry()
        ))

        QTimer.singleShot(Mwc.mw_expansion_time, lambda: self.setMinimumSize(Mwc.mw_width, Mwc.mw_expanded_height))





    #------------------------------------------------------------------------------------------------------------------#


    def collapse_window(self):
        if self._lang_widget:
            self.widget3_stacked.removeWidget(self._lang_widget)
            self._lang_widget.deleteLater()
            self._lang_widget = None


        self.setMinimumSize(Mwc.mw_width, Mwc.mw_height)
        self.setMaximumSize(Mwc.mw_width, Mwc.mw_expanded_height)  # lascia libertà di scendere

        QTimer.singleShot(Mwc.mw_widget_enable_delay, lambda: self.widget3_stacked.setEnabled(False))
        self.anim.setDuration(Mwc.mw_collapse_time)
        self.anim.setStartValue(self.geometry())
        self.anim.setEndValue(self.original_geometry)
        self.anim.setEasingCurve(Mwc.mw_collapse_curve)  # <----- ANIMATION STYLE
        self.anim.start()

        QTimer.singleShot(Mwc.mw_fix_size_delay, lambda: self.setFixedSize(Mwc.mw_width, Mwc.mw_height))
        # Enable only buttons whose index appears in _enabled_buttons
        for i, btn in enumerate(self._language_buttons):
            btn.setEnabled(i in self._enabled_buttons)

    def handle_event(self, button_label_txt):
        self.expand_window(button_label_txt)  # ← passa il label
        self.back_button.setEnabled(True)
        print(button_label_txt)


        ...

    #------------------------------------------------------------------------------------------------------------------#


    def handle_back_button(self):
        self.back_button.setEnabled(False)
        self.collapse_window()


    def handle_github_button_on_enter_pressed(self):
        print("downloading repo...")


