from pathlib import Path
import shutil
import tomlkit

_BASE = Path(__file__).resolve().parent
SRC_PATH  = _BASE / "_rpsproj.toml"
DEST_PATH = _BASE / "toml_playground" / "toml_project_cc.toml"

class TomlHandler:
    @staticmethod
    def initialise_sandbox():
        DEST_PATH.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SRC_PATH, DEST_PATH)

    @staticmethod
    def clear_sandbox():
        DEST_PATH.unlink(missing_ok=True)

    @staticmethod
    def _toml_read() -> tomlkit.TOMLDocument:
        with open(DEST_PATH, "r") as file_:
            return tomlkit.load(file_)

    @staticmethod
    def _toml_write(data: tomlkit.TOMLDocument) -> None:
        with open(DEST_PATH, "w") as f:
            tomlkit.dump(data, f)

    @staticmethod #edits the toml in a specific line in order to allow the file to be easily parsed
    def toml_edit(section: str, key: str, value, subsection: str = None) -> None:
        data = TomlHandler._toml_read()
        if subsection:
            data[section][subsection][key] = value
        else:
            data[section][key] = value
        TomlHandler._toml_write(data)

    @staticmethod
    def set_enabled_lang(p_lang: str) -> None:
        toml_line = TomlHandler._toml_read()
        for lang in toml_line["languages"]:
            toml_line["languages"][lang]["enabled"] = (lang == p_lang)
        TomlHandler._toml_write(toml_line)