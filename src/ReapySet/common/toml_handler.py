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
I18N_FILE_PATH: Traversable = resources.files("ReapySet.common") / "long_tomls_folder" / "i18n.toml"
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
    #@cache
    # Nuitka doesnt support @cache feel free to decomment if you dont plan to use Nuitka
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
        TomlHandler._temp_dir = temp_dir # Keep the temp directory path for manual clean-up.
        TomlHandler.DEST_PATH = dest_path #Editable copy used by the GUI.

        with resources.as_file(SRC_PATH) as src:
            shutil.copy(src, dest_path)
        # TomlHandler._toml_load.cache_clear()

    @staticmethod
    def clear_sandbox() -> None:

        # TomlHandler._toml_load.cache_clear()
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
        # TomlHandler._toml_load.cache_clear()

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

        # TomlHandler._toml_load.cache_clear()

    @staticmethod
    def ensure_config_exists() -> None:
        """
        Creates or restores the persistent config.toml if it does not exist
        or if it exists but is empty.
        """
        if not CONFIG_PATH.exists() or CONFIG_PATH.stat().st_size == 0:
            TomlHandler.reset_config()
