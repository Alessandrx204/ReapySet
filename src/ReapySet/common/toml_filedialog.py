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
from pathlib import Path

import tomlkit
from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QShortcut, QKeySequence, QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QPlainTextEdit, QVBoxLayout, QMessageBox
from ReapySet.config import MwConfig as Mwc

class TomlEditorDialog(QDialog):
    def __init__(self, config_path: Path, parent=None):
        super().__init__(parent)
        self.save_shortcut = QShortcut(QKeySequence.StandardKey.Save, self)
        self.save_shortcut.activated.connect(self._save)
        self.close_shortcut = QShortcut(QKeySequence.StandardKey.Close, self)
        self.close_shortcut.activated.connect(self.reject)

        self.path = config_path# qt is a
        self.setWindowTitle(Mwc.toml_settings_window_title)
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
        ).setText(Mwc.toml_settings_window_save_button)

        buttons.button(
            QDialogButtonBox.StandardButton.Cancel
        ).setText(Mwc.toml_settings_window_close_button)

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
                Mwc.toml_error_txt_title,
                f"{Mwc.toml_error_txt}:\n\n{e}"
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