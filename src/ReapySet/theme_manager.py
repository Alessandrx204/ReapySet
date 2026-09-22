from PySide6.QtCore import Qt, QObject, Signal
from PySide6.QtWidgets import QApplication

from ReapySet.common.toml_handler import TomlHandler, CONFIG_PATH
from ReapySet.common.core_logic.logging import logger


class ThemeManager(QObject):
    theme_changed = Signal(str)
    def __init__(self, app: QApplication) -> None:

        super().__init__()

        self._app = app
        self._style_hints = app.styleHints()
        self.current_theme: str = self._update_current_theme()

        print(
            "System theme on boot:",
            self._style_hints.colorScheme(),
        )
        self._style_hints.colorSchemeChanged.connect(

            self._on_system_theme_changed
        )

    def get_set_theme(self)-> str :
        return TomlHandler.toml_get(CONFIG_PATH, "personal", "application_theme") or "unknown"

    def _on_system_theme_changed(
        self,
        scheme: Qt.ColorScheme,
    ) -> None:

        fav_theme: str = self.get_set_theme()
        if fav_theme != "auto":
            return

        new_theme = self._update_current_theme()

        if new_theme == self.current_theme:

            return

        self.current_theme = new_theme
        self.theme_changed.emit(new_theme)



    def _update_current_theme(self) -> str:
        fav_theme: str = self.get_set_theme()
        if fav_theme == "auto":

            system_theme: Qt.ColorScheme = self._style_hints.colorScheme()

            match system_theme:
                case Qt.ColorScheme.Dark:
                    logger.info("THEME: CHANGED TO: DARK")
                    current_theme = "dark"

                case Qt.ColorScheme.Light:
                    logger.info("THEME: CHANGED TO: LIGHT")
                    current_theme = "light"

                case _:
                    logger.info("THEME: CHANGED TO: DARK (as fallback)")
                    current_theme = "dark"
        else:
            current_theme = fav_theme


        TomlHandler.toml_edit("global",
                              "current_theme",
                              current_theme)

        return current_theme






