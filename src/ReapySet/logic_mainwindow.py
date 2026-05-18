from PySide6.QtCore import QRect, QPropertyAnimation, QTimer

from main_window import RsMainWindow

from config import MwConfig as Mwc








def switch_stacked_widget():
    ...

class LogicMainWindow(RsMainWindow):
    def __init__(self):
        super().__init__()
        self.anim = QPropertyAnimation(self, b"geometry") #type: ignore
        self.original_geometry = self.geometry()

    def expand_window(self):
        for btn in self._language_buttons:
            btn.setEnabled(False)
        self.setMaximumSize(Mwc.mw_width, Mwc.mw_expanded_height)  # MAX SIZE

        current: QRect = self.geometry()
        expanded: QRect = QRect(current.x(), current.y(), current.width(), current.height() + Mwc.mw_height_expansion)

        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(Mwc.mw_expansion_time)
        self.anim.setStartValue(current)
        self.anim.setEndValue(expanded)
        self.anim.setEasingCurve(Mwc.mw_expand_curve)  # <----- ANIMATION STYLE
        self.anim.start()
        QTimer.singleShot(Mwc.mw_widget_enable_delay, lambda: self.widget3_stacked.setEnabled(True))

        QTimer.singleShot(Mwc.mw_expansion_time, lambda: self.setMinimumSize(Mwc.mw_width, Mwc.mw_expanded_height))




    #------------------------------------------------------------------------------------------------------------------#


    def collapse_window(self):

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

        self.expand_window()

        self.back_button.setEnabled(True)
        print(button_label_txt)


        ...

    #------------------------------------------------------------------------------------------------------------------#


    def handle_back_button(self):
        self.back_button.setEnabled(False)
        self.collapse_window()


    def handle_github_button_on_enter_pressed(self):
        print("downloading repo")


