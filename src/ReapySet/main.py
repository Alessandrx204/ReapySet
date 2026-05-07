import sys
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from logic_mainwindow import LogicMainWindow
from config import MwConfig as Mwc
#os.environ["QT_MAC_WANTS_LAYER"] = "1"

def main():
    app: QApplication = QApplication(sys.argv)
    #m_window: RsMainWindow = RsMainWindow()
    m_window = LogicMainWindow()
    m_window.create_language_buttons(m_window.button_labels_list, Mwc.LangBtnWidget.max_btn_x_row, m_window.main_layout)
    base_dir : Path = Path(__file__).resolve().parent
    icon_path : Path = base_dir / "resources" / "icon.png" #sets icon

    icon: QIcon = QIcon(str(icon_path))
    app.setWindowIcon(icon)
    m_window.setWindowIcon(icon)


    m_window.show()
    m_window.original_geometry = m_window.geometry()
    sys.exit(app.exec())



if __name__ == "__main__":

    main()
