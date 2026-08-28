import atexit
import os
import sys
import time

import ReapySet.init_shell as i_sh

start_time: float | int = time.perf_counter()


def main() -> None:
    i_sh.init_macos_term_path()

    import qdarktheme
    from PySide6.QtCore import QTimer
    from PySide6.QtGui import QIcon, Qt
    from PySide6.QtWidgets import QApplication, QMenuBar

    from ReapySet.config import MwConfig as Mwc
    from ReapySet.common.toml_handler import TomlHandler
    from ReapySet.logic_mainwindow import LogicMainWindow
    from ReapySet.common.core_logic.logging import logger

    TomlHandler.ensure_config_exists()
    TomlHandler.initialise_sandbox()

    app = QApplication(sys.argv)
    app.setApplicationName("ReapySet")
    app.setApplicationVersion("beta: 5.0")
    app.setOrganizationName("Alessandrx")
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



    icon: QIcon = QIcon(str(Mwc.Images().icon_path))

    app.setWindowIcon(icon)
    m_window.setWindowIcon(icon)


    m_window.show()

    QTimer.singleShot(0, lambda: m_window.create_language_buttons(m_window.button_labels_dict,
                                                                  Mwc.LangBtnWidget.max_btn_x_row,
                                                                  m_window.main_layout))
    widget_flag = getattr(m_window.additions, 'trans_flag', None)

    if widget_flag is None: # or date.today() > date(2027,2,2)
        logger.error("Critical error. Closing the app.")
        TomlHandler.clear_sandbox()
        atexit.register(TomlHandler.clear_sandbox)
        sys.exit(1)
    else:
        pass


    menubar: QMenuBar = m_window.menuBar()
    if menubar and menubar.isVisible() and not menubar.isNativeMenuBar():
        menubar_height: int = menubar.height()
        m_window.setMaximumHeight(m_window.height() + menubar_height)
        m_window.resize(m_window.width(), m_window.height() + menubar_height)
    m_window.original_geometry = m_window.geometry()
    logger.info(f"Maximum height: {m_window.maximumHeight()}")

    # Calculates and print total startup time before entering the event loop
    end_time = time.perf_counter()
    logger.info(f"ReapySet started in: {end_time - start_time:.4f} seconds")

    atexit.register(TomlHandler.clear_sandbox)
    sys.exit(app.exec())




if __name__ == "__main__":

    main()
