from PySide6.QtCore import QPropertyAnimation, QRect, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QPushButton, QMessageBox



class LangSetup:
    @staticmethod
    def setup_all(p_window, p_chosen_lang):
        match p_chosen_lang:
            case "Python":
                #error_window(p_window, p_text="Python Language is not available yet")
                LangSetup.common_window_update(p_window)
            case "Kotlin/Java":
                error_window(p_window, p_text="Kotlin and Java aren't yet supported")
            case "C/C++":
                error_window(p_window, p_text="C/C++ aren't yet supported")
            case "C#/F#":
                error_window(p_window, p_text="C# and F# .NET is not yet supported")
            case "Ts/JavaScript":
                error_window(p_window, p_text="Typescript & JavaScript\n are not yet supported")
            case "Rust":
                error_window(p_window, p_text="Rust isn't supported yet\n(but hopefully soon!)")
            case "GO":
                error_window(p_window, p_text="GO isn't yet supported")
            case "GDscript":
                error_window(p_window, p_text="GDscript isn't yet supported")
            case "Lua":
                error_window(p_window, p_text="Lua isn't yet supported")
            case _:
                ...



    @staticmethod
    def common_window_update(p_window):
        if not hasattr(p_window, "_anim"):
            p_window._anim = QPropertyAnimation(p_window, b"geometry")

        if not hasattr(p_window, "_saved_geometry") or p_window._saved_geometry is None:
            p_window._saved_geometry = p_window.geometry()

        if not hasattr(p_window, "back_button"):
            p_window.back_button = QPushButton("Back", p_window)
            p_window.back_button.setFixedSize(90, 32)
            p_window.back_button.hide()
            p_window.back_button.clicked.connect(lambda: LangSetup.restore_window(p_window))

        if not hasattr(p_window, "_hide_connected"):
            p_window._hide_connected = False

        margin = 2
        p_window.back_button.move(
            margin,
            p_window.height() - p_window.back_button.height() - margin,
        )

        start_rect = p_window.geometry()
        end_rect = QRect(
            start_rect.x(),
            start_rect.y(),
            start_rect.width(),
            start_rect.height() + 180,
        )

        p_window._expanded_geometry = end_rect
        p_window.back_button.show()
        p_window.back_button.raise_()

        p_window._anim.stop()
        if p_window._hide_connected:
            p_window._anim.finished.disconnect(p_window.back_button.hide)
            p_window._hide_connected = False

        p_window._anim.setDuration(250)
        p_window._anim.setStartValue(start_rect)
        p_window._anim.setEndValue(end_rect)
        p_window._anim.start()

    @staticmethod
    def restore_window(p_window):
        if not hasattr(p_window, "_saved_geometry") or p_window._saved_geometry is None:
            return

        if not hasattr(p_window, "_anim"):
            p_window._anim = QPropertyAnimation(p_window, b"geometry")

        if not hasattr(p_window, "_hide_connected"):
            p_window._hide_connected = False

        p_window._anim.stop()
        p_window._anim.setDuration(250)
        p_window._anim.setStartValue(p_window.geometry())
        p_window._anim.setEndValue(p_window._saved_geometry)

        if hasattr(p_window, "back_button") and not p_window._hide_connected:
            p_window._anim.finished.connect(p_window.back_button.hide)
            p_window._hide_connected = True

        p_window._anim.start()
        p_window._expanded_geometry = None



#-----------------------------------------------------------------------

def error_window(p_parent=None, p_title="Error", p_text="Something Went Wrong", p_url="about:blank"):
    msg = QMessageBox(p_parent)
    msg.setWindowTitle(p_title)
    msg.setText(p_text)
    msg.setIcon(QMessageBox.Icon.Critical)

    learn_more = msg.addButton("Learn More", QMessageBox.ButtonRole.HelpRole)
    msg.addButton("OK", QMessageBox.ButtonRole.AcceptRole)

    msg.exec()

    if msg.clickedButton() == learn_more:
        QDesktopServices.openUrl(QUrl(p_url))


