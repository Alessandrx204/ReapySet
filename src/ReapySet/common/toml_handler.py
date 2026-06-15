import shutil
from pathlib import Path
import tomlkit
from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PySide6.QtWidgets import (
    QPlainTextEdit, QDialogButtonBox, QDialog, QVBoxLayout, QMessageBox,
)

_BASE: Path = Path(__file__).resolve().parent
SRC_PATH: Path  = _BASE / "_rpsproj.toml"
DEST_PATH: Path = _BASE / "toml_playground" / "toml_project_cc.toml"
CONFIG_PATH: Path = _BASE / "toml_playground" / "config.toml"
class TomlHandler:
    @staticmethod
    def initialise_sandbox():
        DEST_PATH.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SRC_PATH, DEST_PATH)

    @staticmethod
    def clear_sandbox():
        DEST_PATH.unlink(missing_ok=True)

    @staticmethod
    def _toml_read(p_doc_path: Path = DEST_PATH) -> tomlkit.TOMLDocument:
        with open(p_doc_path, "r", encoding="utf-8") as f_:
            return tomlkit.load(f_)

    @staticmethod
    def _toml_write( data: tomlkit.TOMLDocument,p_doc_path: Path = DEST_PATH) -> None:
        with open(p_doc_path, "w") as f:
            tomlkit.dump(data, f)

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
            with open(p_file, "r", encoding="utf-8") as f_:
                data = tomlkit.load(f_)

            if subsection:
                val = data[section][subsection][key]
            else:
                val = data[section][key]


            return val

        except (KeyError, FileNotFoundError) as e:
            print(f"Error reading file or a key: {e}")
            return None

    @staticmethod
    def set_enabled_1lang(p_lang: str) -> None:
        toml_line = TomlHandler._toml_read()
        for lang in toml_line["languages"]:
            toml_line["languages"][lang]["enabled"] = (lang == p_lang)
        TomlHandler._toml_write(toml_line)

    @staticmethod
    def set_disabled_all_langs() -> None:  # no need for p_lang
        toml_line = TomlHandler._toml_read()
        for lang in toml_line["languages"]:
            toml_line["languages"][lang]["enabled"] = False
        TomlHandler._toml_write(toml_line)






class TomlEditorDialog(QDialog):
    def __init__(self, config_path: Path, parent=None):
        super().__init__(parent)

        self.path = config_path
        self.setWindowTitle("Settings TOML")
        self.resize(700, 600)

        self.editor = QPlainTextEdit()
        self.editor.setPlainText(self.path.read_text(encoding="utf-8"))

        self.highlighter = TomlHighlighter(self.editor.document())

        buttons = QDialogButtonBox()
        buttons.setStandardButtons(
            QDialogButtonBox.StandardButton.Save |
            QDialogButtonBox.StandardButton.Cancel # noqa
        )

        buttons.accepted.connect(self._save)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addWidget(self.editor)
        layout.addWidget(buttons)

    def _save(self):
        # validates TOML before saving
        text = self.editor.toPlainText()

        try:
            tomlkit.parse(text)
        except Exception as e:
            QMessageBox.critical(
                self,
                "Invalid TOML",
                f"The TOML file contains an error:\n\n{e}"
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