def test_basic():
    assert True


from PySide6.QtWidgets import QApplication, QStyleFactory
import sys

app = QApplication(sys.argv)
print(QStyleFactory.keys())
print(app.style().name())



from pathlib import Path
from PySide6.QtGui import QIcon

icon_path = Path("src/ReadySet/resources/icon.png").resolve()
print(icon_path)
print(icon_path.exists())

icon = QIcon(str(icon_path))
print(icon.isNull())