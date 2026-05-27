import atexit
import os
import sys
import time

# Start the timer immediately at the script entry point
start_time = time.perf_counter()

import qdarktheme
from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QApplication
from logic_mainwindow import LogicMainWindow
from config import MwConfig as Mwc
from ReapySet.common.toml_handler import TomlHandler

def main():
    TomlHandler.initialise_sandbox()
    app: QApplication = QApplication(sys.argv)
    app.setStyle("Fusion" if os.name == "nt" else "")
    app.styleHints().setColorScheme(Qt.ColorScheme.Dark) # ENFORCES MANDATORY DARK MODE
    app.setPalette(
    qdarktheme.load_palette(
        theme="dark",
        custom_colors={
            "primary": "#FCE3F0", # pink-ish
            "background": "#202124",
            "foreground": "#E8EAED",

        }
    )
)
    m_window: LogicMainWindow = LogicMainWindow()
    #qdarktheme.setup_theme()
    m_window.create_language_buttons(m_window.button_labels_dict,
                                     Mwc.LangBtnWidget.max_btn_x_row,
                                     m_window.main_layout)


    icon: QIcon = QIcon(str(Mwc.Images().icon_path))

    app.setWindowIcon(icon)
    m_window.setWindowIcon(icon)


    m_window.show()
    if sys.platform == "darwin":
        try:
            import objc
            from AppKit import NSApplication
            ns_app = NSApplication.sharedApplication()
            ns_window = ns_app.windows()[0]
            ns_window.setCollectionBehavior_(1 << 2)  # NSWindowCollectionBehaviorMoveToActiveSpace
        except Exception:#type: ignore
            pass

    m_window.original_geometry = m_window.geometry()

    # Calculate and print total startup time before entering the event loop
    end_time = time.perf_counter()
    print(f"ReadySet started in: {end_time - start_time:.4f} seconds")

    atexit.register(TomlHandler.clear_sandbox)
    sys.exit(app.exec())




if __name__ == "__main__":

    main()
