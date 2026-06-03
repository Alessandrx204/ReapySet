from pathlib import Path
import shutil
import tomlkit

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
    def _toml_read() -> tomlkit.TOMLDocument:
        with open(DEST_PATH, "r", encoding="utf-8") as f_:
            return tomlkit.load(f_)

    @staticmethod
    def _toml_write(data: tomlkit.TOMLDocument) -> None:
        with open(DEST_PATH, "w") as f:
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