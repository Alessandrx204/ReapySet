from typing import cast

from PySide6.QtCore import Qt, QSize, QRectF
from PySide6.QtGui import QColor
from PySide6.QtGui import QIcon
from PySide6.QtGui import QPainterPath
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QLabel, QPushButton, QApplication

from ReapySet.common.toml_handler import CONFIG_PATH, TomlEditorDialog, TomlHandler


class TransFlagWidget(QLabel):
    """Discreet trans flag with tooltip"""

    def __init__(self, parent=None, size=22):
        super().__init__(parent)

        self.size = size

        self._set_trans_flag()

        self.setToolTip("We despise how political propaganda on all sides uses LGBTQ+ people.\n Our rights should not be bundled with partisan agendas,\n nor should they be targeted by reactionary hostility.\n Basic respect shouldn't belong to any political wing.")
        #self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.setFixedSize(size, size)

    def _set_trans_flag(self):
        base = QPixmap(self.size, self.size)
        base.fill(Qt.GlobalColor.transparent)

        painter = QPainter(base)

        light_blue = QColor(91, 206, 250)
        pink = QColor(255, 153, 198)
        white = QColor(255, 255, 255)

        stripe_h = self.size // 5

        painter.fillRect(0, 0, self.size, stripe_h, light_blue)
        painter.fillRect(0, stripe_h, self.size, stripe_h, pink)
        painter.fillRect(0, stripe_h * 2, self.size, stripe_h, white)
        painter.fillRect(0, stripe_h * 3, self.size, stripe_h, pink)
        painter.fillRect(0, stripe_h * 4, self.size, stripe_h, light_blue)

        painter.end()

        rounded = QPixmap(self.size, self.size)
        rounded.fill(Qt.GlobalColor.transparent)

        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        path = QPainterPath()
        margin = 1

        rect = rounded.rect().adjusted(
            margin,
            margin,
            -margin,
            -margin
        )

        radius = 5

        path.addRoundedRect(rect, radius, radius)

        painter.setClipPath(path)
        painter.drawPixmap(0, 0, base)

        painter.setPen(QColor(255, 255, 255, 40))
        painter.drawRoundedRect(rect, radius, radius)

        self.setPixmap(rounded)


# SVG come stringa



SETTINGS_SVG = b'''<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M12.0122 2.25C12.7462 2.25846 13.4773 2.34326 14.1937 2.50304C14.5064 2.57279 14.7403 2.83351 14.7758 3.15196L14.946 4.67881C15.0231 5.37986 15.615 5.91084 16.3206 5.91158C16.5103 5.91188 16.6979 5.87238 16.8732 5.79483L18.2738 5.17956C18.5651 5.05159 18.9055 5.12136 19.1229 5.35362C20.1351 6.43464 20.8889 7.73115 21.3277 9.14558C21.4223 9.45058 21.3134 9.78203 21.0564 9.9715L19.8149 10.8866C19.4607 11.1468 19.2516 11.56 19.2516 11.9995C19.2516 12.4389 19.4607 12.8521 19.8157 13.1129L21.0582 14.0283C21.3153 14.2177 21.4243 14.5492 21.3297 14.8543C20.8911 16.2685 20.1377 17.5649 19.1261 18.6461C18.9089 18.8783 18.5688 18.9483 18.2775 18.8206L16.8712 18.2045C16.4688 18.0284 16.0068 18.0542 15.6265 18.274C15.2463 18.4937 14.9933 18.8812 14.945 19.3177L14.7759 20.8444C14.741 21.1592 14.5122 21.4182 14.204 21.4915C12.7556 21.8361 11.2465 21.8361 9.79803 21.4915C9.48991 21.4182 9.26105 21.1592 9.22618 20.8444L9.05736 19.32C9.00777 18.8843 8.75434 18.498 8.37442 18.279C7.99451 18.06 7.5332 18.0343 7.1322 18.2094L5.72557 18.8256C5.43422 18.9533 5.09403 18.8833 4.87678 18.6509C3.86462 17.5685 3.11119 16.2705 2.6732 14.8548C2.57886 14.5499 2.68786 14.2186 2.94485 14.0293L4.18818 13.1133C4.54232 12.8531 4.75147 12.4399 4.75147 12.0005C4.75147 11.561 4.54232 11.1478 4.18771 10.8873L2.94516 9.97285C2.6878 9.78345 2.5787 9.45178 2.67337 9.14658C3.11212 7.73215 3.86594 6.43564 4.87813 5.35462C5.09559 5.12236 5.43594 5.05259 5.72724 5.18056L7.12762 5.79572C7.53056 5.97256 7.9938 5.94585 8.37577 5.72269C8.75609 5.50209 9.00929 5.11422 9.05817 4.67764L9.22824 3.15196C9.26376 2.83335 9.49786 2.57254 9.8108 2.50294C10.5281 2.34342 11.26 2.25865 12.0122 2.25ZM11.9997 8.99995C10.3428 8.99995 8.9997 10.3431 8.9997 12C8.9997 13.6568 10.3428 15 11.9997 15C13.6565 15 14.9997 13.6568 14.9997 12C14.9997 10.3431 13.6565 8.99995 11.9997 8.99995Z" fill="#FFFFFF"/>
</svg>'''



class SettingsButtonWidget(QPushButton):
    def __init__(self, parent=None, size=22):
        super().__init__(parent)
        self.setFixedSize(size, size)
        self.setFlat(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip("Settings")
        self._set_icon(size)
        #self.clicked.connect(lambda : print("clicked"))
        self.clicked.connect(
            lambda: (
                TomlHandler.ensure_config_exists(),
                TomlEditorDialog(CONFIG_PATH, self).exec()
            )
        )
        self.setStyleSheet("QPushButton { border: none; background: transparent; outline: none; }")

    def _set_icon(self, size: int) -> None:
        """
        Render the settings SVG icon at high resolution for HiDPI/Retina displays.

        The SVG is rasterised into a DPR-aware QPixmap to ensure the icon remains
        sharp on high-density screens (e.g. macOS Retina). Rendering is performed
        in logical coordinates so Qt correctly maps the image to the device pixel
        ratio without visual offsets or scaling artefacts.

        Args:
            size: Desired icon size in logical pixels.
        """

        # Retrieve the current QApplication instance.
        app = cast(QApplication, QApplication.instance())

        # Get the primary screen in order to determine the device pixel ratio (DPR).
        # DPR > 1.0 is common on Retina/HiDPI displays.
        screen = app.primaryScreen()

        # Fallback to standard DPI if no screen is available.
        dpr = screen.devicePixelRatio() if screen else 1.0

        # Convert the logical size into physical pixels.
        # Example: 20 px icon on a Retina display (DPR 2.0) -> 40 px backing image.
        physical_size = int(size * dpr)

        # Create a transparent high-resolution pixmap.
        pixmap = QPixmap(physical_size, physical_size)
        pixmap.setDevicePixelRatio(dpr)
        pixmap.fill(Qt.GlobalColor.transparent)

        # Load the SVG renderer.
        renderer = QSvgRenderer(SETTINGS_SVG)

        # Paint the SVG onto the pixmap.
        painter = QPainter(pixmap)

        # Enable antialiasing for smoother vector rendering.
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Render using LOGICAL coordinates (size x size), not physical pixels.
        # Qt will automatically map this to the correct DPR-aware resolution.
        renderer.render(painter, QRectF(0, 0, size, size))

        # Properly release painter resources.
        painter.end()

        # Apply the rendered icon to the widget.
        self.setIcon(QIcon(pixmap))

        # Ensure Qt uses the intended logical icon size.
        self.setIconSize(QSize(size, size))

class MwAdditions:
    def __init__(self, window):
        self.window = window
        self.trans_flag = None
        self.settings_btn = None

    def add_trans_flag(self, size=22):
        self.trans_flag = TransFlagWidget(
            parent=self.window.centralWidget(),
            size=size
        )
        self.trans_flag.raise_()
        self.trans_flag.show()
        self.position_trans_flag()

    def add_settings_button(self, size=22):
        self.settings_btn = SettingsButtonWidget(
            parent=self.window.centralWidget(),
            size=size
        )
        self.settings_btn.raise_()
        self.settings_btn.show()
        self.position_settings_btn()


    def position_widget(
            self,
            widget,
            anchor: str = "top_right",
            offset_x: int = 0,
            offset_y: int = 0
    ) -> None:
        if widget is None:
            return

        cw = self.window.centralWidget()
        cw_w = cw.width()
        cw_h = cw.height()

        w = widget.width()
        h = widget.height()

        match anchor:
            case "top_right":
                x = cw_w - w
                y = 0

            case "top_left":
                x = 0
                y = 0

            case "bottom_right":
                x = cw_w - w
                y = cw_h - h

            case "bottom_left":
                x = 0
                y = cw_h - h

            case "center":
                x = (cw_w - w) // 2
                y = (cw_h - h) // 2

            case _:
                raise ValueError(f"Unknown anchor: {anchor}")

        widget.move(x + offset_x, y + offset_y)

    def position_trans_flag(self):
        self.position_widget(
            self.trans_flag,
            anchor="top_left",
            offset_x=10,
            offset_y=10
        )

    def position_settings_btn(self):
        self.position_widget(
            self.settings_btn,
            anchor="top_right",
            offset_x=-10,
            offset_y=10
        )

    def reposition_all(self):
        self.position_trans_flag()
        self.position_settings_btn()