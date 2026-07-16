from __future__ import annotations
import shutil
import tempfile
from pathlib import Path
from functools import cache

import tomlkit
from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QPlainTextEdit, QDialogButtonBox, QDialog, QVBoxLayout, QMessageBox, )
from importlib import resources

from platformdirs import PlatformDirs

from importlib.abc import Traversable
from typing import Any

TomlReadable = Path | Traversable

TomlWritable = Path #types
# Persistent user config directory
_platform_data_dirs = PlatformDirs(appname="ReapySet")

_cfg_dir = Path(_platform_data_dirs.user_config_dir)

_cfg_dir.mkdir(parents=True, exist_ok=True)

CONFIG_PATH = _cfg_dir / "config.toml"
SRC_PATH: Traversable = resources.files("ReapySet.common") / "_rpsproj.toml"

BACKUP_CONFIG_PATH: Traversable = resources.files("ReapySet.common") / "_config_backup.toml"
# ---------------------------------------------------------------------#
# Bundled resources
# These are Traversable objects, NOT guaranteed real pathlib.Path objects.
# ---------------------------------------------------------------------#

SRC_RESOURCE: Traversable = resources.files("ReapySet.common") / "_rpsproj.toml"

BACKUP_CONFIG_RESOURCE: Traversable = resources.files("ReapySet.common") / "_config_backup.toml"

GREETINGS_PATH: Traversable = (
    resources.files("ReapySet.common.long_tomls_folder") / "greetings.toml"
)
class TomlHandler:
    _temp_dir: Path | None = None
    DEST_PATH: Path | None = None

    @staticmethod
    def _dest_path() -> Path:

        if TomlHandler.DEST_PATH is None:
            raise RuntimeError("Project TOML sandbox has not been initialised.")
        return TomlHandler.DEST_PATH

    @staticmethod
    @cache
    def _toml_load(p_doc_path: TomlReadable | None = None) -> tomlkit.TOMLDocument:
        """
        Loads a TOML document.
        - If p_doc_path is None, reads the current temporary project TOML.
        - If p_doc_path is Path, reads a real filesystem file.
        - If p_doc_path is Traversable, reads a bundled importlib resource.
        """
        doc = p_doc_path or TomlHandler._dest_path()
        with doc.open("r", encoding="utf-8") as f:
            return tomlkit.load(f)

    @staticmethod
    def initialise_sandbox() -> None:
        """
        Creates a real editable TOML file from the bundled _rpsproj.toml template.
        SRC_PATH is bundled inside the package / Nuitka executable and must stay
        read-only. The GUI must only edit DEST_PATH, which is a real file inside
        a manually managed temporary directory.
        """
        TomlHandler.clear_sandbox()

        temp_dir = Path(tempfile.mkdtemp(prefix="reapyset_"))
        dest_path = temp_dir / "_rpsproj.toml"
        TomlHandler._temp_dir = temp_dir # Keep the temp directory path for manual cleanup.
        TomlHandler.DEST_PATH = dest_path #Editable copy used by the GUI.

        with resources.as_file(SRC_PATH) as src:
            shutil.copy(src, dest_path)
        TomlHandler._toml_load.cache_clear()

    @staticmethod
    def clear_sandbox() -> None:

        TomlHandler._toml_load.cache_clear()
        if TomlHandler._temp_dir is not None:

            shutil.rmtree(TomlHandler._temp_dir, ignore_errors=False)

        TomlHandler._temp_dir = None
        TomlHandler.DEST_PATH = None

    @staticmethod
    def _toml_read(p_doc_path: TomlReadable | None = None) -> tomlkit.TOMLDocument:
        return TomlHandler._toml_load(p_doc_path)

    @staticmethod
    def _toml_write(
        data: tomlkit.TOMLDocument,
        p_doc_path: TomlWritable | None = None,
    ) -> None:

        path = p_doc_path or TomlHandler._dest_path()
        with path.open("w", encoding="utf-8") as f_:
            tomlkit.dump(data, f_)
        TomlHandler._toml_load.cache_clear()

    @staticmethod #edits the toml in a specific line in order to allow the file to be easily parsed
    def toml_edit(section: str, key: str, value: Any, subsection: str | None = None, p_doc_path: TomlWritable | None = None) -> None:
        path = p_doc_path or TomlHandler._dest_path()


        """print(f"toml_edit called: {section}.{key} = {value}")"""
        data = TomlHandler._toml_read(path)
        if subsection:
            data[section][subsection][key] = value
        else:
            data[section][key] = value
        TomlHandler._toml_write(data, path)


    @staticmethod
    def toml_get(p_file: TomlReadable,
                 section: str,
                 key: str,
                 subsection: str | None = None
                 ) -> Any | None:
        """
       reads a specific value from a TOML.
        """
        try:
                data = TomlHandler._toml_load(p_file)
                return data[section][subsection][key] if subsection else data[section][key]

        except (FileNotFoundError, KeyError) as e:
            print(f"Error reading file or key: {e}")
            return None

    @staticmethod
    def set_enabled_1lang(p_lang: str) -> None:
        toml_line = TomlHandler._toml_read()
        for lang in toml_line["languages"]:
            toml_line["languages"][lang]["enabled"] = (lang == p_lang)
        TomlHandler._toml_write(toml_line)

    @staticmethod
    def set_disabled_all_langs() -> None:
        toml_line = TomlHandler._toml_read()
        for lang in toml_line["languages"]:
            toml_line["languages"][lang]["enabled"] = False
        TomlHandler._toml_write(toml_line)


    @staticmethod
    def reset_config() -> None:
        """
        Restores the persistent user config from the bundled backup config.
        """
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with resources.as_file(BACKUP_CONFIG_PATH) as src:
            shutil.copy(src, CONFIG_PATH)

        TomlHandler._toml_load.cache_clear()

    @staticmethod
    def ensure_config_exists() -> None:
        """
        Creates or restores the persistent config.toml if it does not exist
        or if it exists but is empty.
        """
        if not CONFIG_PATH.exists() or CONFIG_PATH.stat().st_size == 0:
            TomlHandler.reset_config()








# macOS + Qt/PySide6 note:
# When using text widgets (QLineEdit/QPlainTextEdit) together with IME
# input methods (Japanese, Chinese, etc.), macOS may print console warnings
# such as:
#
#   TSMSendMessageToUIServer: CFMessagePortSendRequest FAILED(-1)
#   error messaging the mach port for IMKCFRunLoopWakeUpReliable
#
# These are macOS InputMethodKit/Text Services Manager warnings and are
# generally harmless if text input and IME composition work correctly.
# No action required unless the app shows real input/focus issues.

class TomlEditorDialog(QDialog):
    def __init__(self, config_path: Path, parent=None):
        super().__init__(parent)
        self.save_shortcut = QShortcut(QKeySequence.StandardKey.Save, self)
        self.save_shortcut.activated.connect(self._save)
        self.close_shortcut = QShortcut(QKeySequence.StandardKey.Close, self)
        self.close_shortcut.activated.connect(self.reject)

        self.path = config_path# qt is a  
        self.setWindowTitle("Settings")
        self.resize(700, 600)

        self.editor_page = QPlainTextEdit()
        self.editor_page.setPlainText(self.path.read_text(encoding="utf-8"))

        self.highlighter = TomlHighlighter(self.editor_page.document())

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save |
            QDialogButtonBox.StandardButton.Cancel # noqa
        )

        buttons.button(
            QDialogButtonBox.StandardButton.Save
        ).setText("&Save && Exit")

        buttons.button(
            QDialogButtonBox.StandardButton.Cancel
        ).setText("Close without saving")

        buttons.accepted.connect(self._save)
        buttons.rejected.connect(self.reject)
        buttons.setStyleSheet("/* BASE STYLE (Pink) */\n"
                              "QPushButton {\n"
                              "    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #96788f, stop:1 #80637a);\n"
                              "    color: #f3eaf0;\n"
                              "    border: 1px solid #736473;\n"
                              "    border-radius: 7px;\n"
                              "    padding: 3px 18px;\n"
                              "}\n"
                              "\n"
                              "/* HOVER (Brighter Pink) */\n"
                              "QPushButton:hover {\n"
                              "    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #a889a1, stop:1 #8e7188);\n"
                              "    color: #ffffff;\n"
                              "    border-color: #8d627d;\n"
                              "}\n"
                              "\n"
                              "/* ON PRESSED (Dark gray) */\n"
                              "QPushButton:pressed {\n"
                              "    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #5f6063, stop:1 #4f5052);\n"
                              "    color: #d1c9cf;\n"
                              "    border-color: #433841;\n"
                              "}\n"
                              "\n"
                              "/* CHECKED (Gray) */\n"
                              "QPushButton:checked {\n"
                              "    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #66676b, stop:1 #57585a);\n"
                              "    color: #e3dae0;\n"
                              "    border-color: #4d424b;\n"
                              "}") #QSS

        layout = QVBoxLayout(self)
        layout.addWidget(self.editor_page)

        layout.addWidget(buttons)



    def _save(self):
        # validates TOML before saving
        text = self.editor_page.toPlainText()

        try:
            tomlkit.parse(text)
        except Exception as e:
            QMessageBox.critical(
                self,
                "Invalid Config TOML",
                f"The Config TOML file contains an error:\n\n{e}"
            )
            return

        self.path.write_text(text, encoding="utf-8")
        self.accept()





class TomlHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent)

        self.section_format = QTextCharFormat()
        self.section_format.setForeground(QColor("#ff9acb"))
        self.section_format.setFontWeight(QFont.Weight.Bold)

        self.key_format = QTextCharFormat()
        self.key_format.setForeground(QColor("#9cdcfe"))

        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor("#ce9178"))

        self.number_format = QTextCharFormat()
        self.number_format.setForeground(QColor("#b5cea8"))

        self.bool_format = QTextCharFormat()
        self.bool_format.setForeground(QColor("#569cd6"))
        self.bool_format.setFontWeight(QFont.Weight.Bold)

        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor("#6a9955"))
        self.comment_format.setFontItalic(True)

        self.rules = [
            (QRegularExpression(r"^\s*\[.*\]"), self.section_format),
            (QRegularExpression(r"^\s*[A-Za-z0-9_\-]+(?=\s*=)"), self.key_format),
            (QRegularExpression(r'"[^"]*"'), self.string_format),
            (QRegularExpression(r"\b\d+(\.\d+)?\b"), self.number_format),
            (QRegularExpression(r"\b(true|false)\b"), self.bool_format),
            (QRegularExpression(r"#.*$"), self.comment_format),
        ]

    def highlightBlock(self, text: str) -> None:
        for pattern, fmt in self.rules:
            match_iterator = pattern.globalMatch(text)

            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(
                    match.capturedStart(),
                    match.capturedLength(),
                    fmt
                )