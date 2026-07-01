import shutil
from pathlib import Path
from functools import cache

import tomlkit
from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PySide6.QtWidgets import (
    QPlainTextEdit, QDialogButtonBox, QDialog, QVBoxLayout, QMessageBox, )

_BASE: Path = Path(__file__).resolve().parent
SRC_PATH: Path  = _BASE / "_rpsproj.toml"
DEST_PATH: Path = _BASE / "toml_playground" / "toml_project_cc.toml"
CONFIG_PATH: Path = _BASE / "toml_playground" / "config.toml"
BACKUP_CONFIG_PATH: Path = _BASE / "_config_backup.toml"

GREETINGS_PATH: Path = _BASE / "long_tomls_folder" / "greetings.toml"
class TomlHandler:
    @staticmethod
    @cache
    def _toml_load(p_doc_path: Path = DEST_PATH) -> tomlkit.TOMLDocument:
        with open(p_doc_path, "r", encoding="utf-8") as f_:
            return tomlkit.load(f_)

        
    @staticmethod
    def initialise_sandbox():
        DEST_PATH.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SRC_PATH, DEST_PATH)
        TomlHandler._toml_load.cache_clear()

    @staticmethod
    def clear_sandbox():
        DEST_PATH.unlink(missing_ok=True)
        TomlHandler._toml_load.cache_clear()


    @staticmethod
    def _toml_read(p_doc_path: Path = DEST_PATH) -> tomlkit.TOMLDocument:
        return TomlHandler._toml_load(p_doc_path)

    @staticmethod
    def _toml_write( data: tomlkit.TOMLDocument,p_doc_path: Path = DEST_PATH) -> None:
        with open(p_doc_path, "w") as f:
            tomlkit.dump(data, f)
        TomlHandler._toml_load.cache_clear()

    @staticmethod #edits the toml in a specific line in order to allow the file to be easily parsed
    def toml_edit(section: str, key: str, value, subsection: str|None = None) -> None:
        print(f"toml_edit called: {section}.{key} = {value}")
        data = TomlHandler._toml_read()
        if subsection:
            data[section][subsection][key] = value
        else:
            data[section][key] = value
        TomlHandler._toml_write(data)


    @staticmethod
    def toml_get(p_file: Path, section: str, key: str, subsection: str | None = None):
        """
       reads a specific value from a TOML.
        """
        # uses 'rb' and decode to better manage encodings (recommended by the tomlkit doc)
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
        shutil.copy(BACKUP_CONFIG_PATH, CONFIG_PATH)







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

        self.path = config_path
        self.setWindowTitle("Settings TOML")
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