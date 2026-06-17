import os
import shutil
import sys
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path

import tomlkit
from PySide6.QtCore import QEasingCurve
from common.toml_handler import TomlHandler, CONFIG_PATH


def _get_root() -> Path:
    if hasattr(sys, "frozen"):
        return Path(os.path.dirname(sys.executable))
    return Path(__file__).resolve().parent


@dataclass
class MwConfig:
    """Main Window configs"""
    mw_title: str = "ReapySet"

    mw_width: int = 770
    mw_height: int = 370

    mw_height_expansion: int = 280
    mw_expanded_height: int = mw_height + mw_height_expansion  # 580

    mw_expansion_time: int = 600
    mw_collapse_time: int = 450
    mw_expand_curve: QEasingCurve.Type = QEasingCurve.Type.OutExpo
    mw_collapse_curve: QEasingCurve.Type = QEasingCurve.Type.OutCubic

    mw_widget_enable_delay: int = 45
    mw_fix_size_delay: int = mw_collapse_time + 10

    mw_y_offset: int = -150

    # ── nested classes ──────────────────────────────────

    @dataclass
    class Images:
        root: Path = field(default_factory=_get_root)

        @cached_property          # computed once, then cached on the instance
        def res(self) -> Path:
            return self.root / "resources"

        @property
        def icon_path(self)       -> Path: return self.res / "icon.png"
        @property
        def python_logo(self)     -> Path: return self.res / "python_logo.svg"
        @property
        def rust_logo(self)       -> Path: return self.res / "rust_logo2.svg"
        @property
        def dotnet_logo(self)     -> Path: return self.res / "dotnet_logo.svg"
        @property
        def kotlin_logo(self)     -> Path: return self.res / "kotlin_java_logo.png"
        @property
        def javascript_logo(self) -> Path: return self.res / "js_logo.png"
        @property
        def go_logo(self)         -> Path: return self.res / "go_logo.svg"
        @property
        def lua_logo(self)        -> Path: return self.res / "lua_logo.svg"
        @property
        def godot_logo(self)      -> Path: return self.res / "godot_logo.svg"
        @property
        def cpp_logo(self)        -> Path: return self.res / "cpp_logo.svg"
        @property
        def python_wallpaper(self) -> Path: return self.res / "python_free_wallpaper.png"


    @dataclass
    class Widget1:
        """Widget 1 config"""
        QlineEditQSS: str = """
        QLineEdit {
            font-size: 12px;
            min-width: 140px;
            border: 2px solid rgb(65, 65, 63);
            border-radius: 5px;
            background-color: rgb(30, 30, 28);
            color: rgb(220, 220, 220);
        }
        QLineEdit:hover {
            border: 2px solid rgb(150, 60, 105);      /* dawn pink */
            background-color: rgb(38, 38, 36);        /* light pink */
        }
        QLineEdit:focus {
            border: 2px solid rgb(236, 100, 175);     /* full pink */
            background-color: rgb(44, 44, 42);
        }
        """
        QlineTopTextQSS: str            = "font-size:10px; margin-top:0px; margin-bottom:6px;"
        github_box_top_label: str       = "Import a project from GitHub"
        github_box_placeholder_txt: str = "COMING SOON " #insert a repo URL
        path_box_top_label: str         = "Project Location:"
        path_box_placeholder_txt: str   = "Project Path...?"
        sample_box_top_label: str       = "Boilerplates:"
        boilerplates_box_placeholder_txt: str = "COMING SOON"
        browse_button_text: str         = "Browse"
        select_editor_Combobox_top_label: str = ""

        # plain class variable — accessible directly on the class without instantiation
        select_editor_Combobox_entry: list[str] = field(
            default_factory=lambda: LogicVariables.EditorCmd.get_all_editors())
        #select_editor_Combobox_entry = LogicVariables.EditorCmd.get_all_editors()


        """[
            "VSCode", "Pycharm", "Godot",
            "Intellij IDEA", "Clion", "Zed",
            "Sublime Text", "Notepad++", "nVim"
                                        ]"""

    @dataclass
    class LangBtnWidget:
        """Widget 2: language selector buttons"""
        images: "MwConfig.Images" = field(default_factory=lambda: MwConfig.Images())
        enabled_btns: list[int]   = field(default_factory=lambda: [0])
        cw_height:     int = 120
        max_btn_x_row: int = 3 #ex 5
        lang_btns_qss: str = ("QPushButton {\n"
                              "    background-color: qlineargradient(\n"
                              "        x1:0, y1:0, x2:0, y2:1,\n"
                              "        stop:0 #66676b,\n"
                              "        stop:0.45 #5f6063,\n"
                              "        stop:1 #57585a\n"
                              "    );\n"
                              "\n"
                              "    color: #f3eaf0;\n"
                              "\n"
                              "    border-top: 1.25px solid #c28cb7;\n"
                              "    border-left: 1px solid #9e8299;\n"
                              "    border-right: 1px solid #9e8299;\n"
                              "    border-bottom: 2px solid #736473;\n"
                              "\n"
                              "    border-radius: 7px;\n"
                              "    padding: 6px 18px;\n"
                              "}\n"
                              "\n"
                              "QPushButton:hover {\n"
                              "    background-color: qlineargradient(\n"
                              "        x1:0, y1:0, x2:0, y2:1,\n"
                              "        stop:0 #96788f,\n"
                              "        stop:0.5 #896d84,\n"
                              "        stop:1 #80637a\n"
                              "    );\n"
                              "\n"
                              "    color: #ffd9e9;\n"
                              "\n"
                              "    border-top: 1px solid #ffc5df;\n"
                              "    border-left: 1px solid #f0a2c5;\n"
                              "    border-right: 1px solid #d989b0;\n"
                              "    border-bottom: 2px solid #8d627d;\n"
                              "}\n"
                              "\n"
                              "QPushButton:pressed {\n"
                              "    background-color: qlineargradient(\n"
                              "        x1:0, y1:0, x2:0, y2:1,\n"
                              "        stop:0 #4d424b,\n"
                              "        stop:1 #433841\n"
                              "    );\n"
                              "\n"
                              "    color: #ffe3ef;\n"
                              "\n"
                              "    border-top: 1px solid #6d5565;\n"
                              "    border-left: 1px solid #8e647d;\n"
                              "    border-right: 1px solid #8e647d;\n"
                              "    border-bottom: 1px solid #b97e9e;\n"
                              "\n"
                              "    padding-top: 7px;\n"
                              "    padding-bottom: 5px;\n"
                              "}\n"
                              "\n"
                              "QPushButton:checked {\n"
                              "    background-color: qlineargradient(\n"
                              "        x1:0, y1:0, x2:0, y2:1,\n"
                              "        stop:0 #734860,\n"
                              "        stop:0.5 #643a52,\n"
                              "        stop:1 #593047\n"
                              "    );\n"
                              "\n"
                              "    color: #ffe0ec;\n"
                              "\n"
                              "    border-top: 1px solid #ffc8de;\n"
                              "    border-left: 1px solid #f1a5c8;\n"
                              "    border-right: 1px solid #d887ad;\n"
                              "    border-bottom: 2px solid #8d5c77;\n"
                              "}\n"
                              "\n"
                              "QPushButton:checked:hover {\n"
                              "    background-color: qlineargradient(\n"
                              "        x1:0, y1:0, x2:0, y2:1,\n"
                              "        stop:0 #81506a,\n"
                              "        stop:0.5 #74455e,\n"
                              "        stop:1 #673a53\n"
                              "    );\n"
                              "\n"
                              "    color: #fff0f7;\n"
                              "\n"
                              "    border-top: 1px solid #ffd9ea;\n"
                              "    border-left: 1px solid #ffb7d3;\n"
                              "    border-right: 1px solid #e092b7;\n"
                              "    border-bottom: 2px solid #99657f;\n"
                              "}\n"
                              "\n"
                              "QPushButton:disabled {\n"
                              "    background-color: qlineargradient(\n"
                              "        x1:0, y1:0, x2:0, y2:1,\n"
                              "        stop:0 #444548,\n"
                              "        stop:1 #37383b\n"
                              "    );\n"
                              "\n"
                              "    color: #7f7178;\n"
                              "    border: 1px solid #534a52;\n"
                              "}\n"
                              "\n"
                              "QPushButton[selected=\"true\"]:disabled {\n"
                              "    background-color: qlineargradient(\n"
                              "        x1:0, y1:0, x2:0, y2:1,\n"
                              "        stop:0 #734860,\n"
                              "        stop:0.5 #643a52,\n"
                              "        stop:1 #593047\n"
                              "    );\n"
                              "\n"
                              "    color: #ffe0ec;\n"
                              "\n"
                              "    border-top: 1px solid #ffc8de;\n"
                              "    border-left: 1px solid #f1a5c8;\n"
                              "    border-right: 1px solid #d887ad;\n"
                              "    border-bottom: 2px solid #8d5c77;\n"
                              "}\n")

        # built once at init instead of being recreated on every access
        button_dict: dict = field(init=False)

        def __post_init__(self):
            img = self.images
            self.button_dict = {
                "Python":        ["PY",       img.python_logo],
                "Rust (W.I.P.)":          ["RUST",     img.rust_logo],
                ".NET (W.I.P.)":          ["DOTNET",   img.dotnet_logo],
                "Kotlin/Java (W.I.P.)":   ["KT",       img.kotlin_logo],
                "Ts/JavaScript (W.I.P.)": ["TSJS",     img.javascript_logo],
            }

            """self.button_dict = {
                "Python":        ["PY",       img.python_logo],
                "Rust":          ["RUST",     img.rust_logo],
                ".NET":          ["DOTNET",   img.dotnet_logo],
                "Kotlin/Java":   ["KT",       img.kotlin_logo],
                "C/C++":         ["CPP",      img.cpp_logo],
                "Ts/JavaScript": ["TSJS",     img.javascript_logo],
                "GO":            ["GO",       img.go_logo],
                "Lua":           ["LUA",      img.lua_logo],
                "GDScript":      ["GDSCRIPT", img.godot_logo],
            }"""


    @dataclass
    class Widget3:
        """Widget 3: per language widgets"""
        widget3_qss: str = ("\n"
                            "            QStackedWidget {\n"
                            "                border-radius: 10px;\n"
                            "                background-color: transparent;\n"
                            "            }\n"
                            "        ")

        """python"""
        py_qlabel_txt: str = "Please Setup Your Python Workspace! (^-^)/"
        py_interp_qcbox_top_txt: str = "locally installed interpreters"
        py_unb_interp_qlinedit_top_txt: str = "exact Interp. version\n(only uv & conda dervivatives)"
        py_unb_interp_qlinedit_inner_txt: str = "e.g. 3.13.5"

        py_qlabel_qss: str = (
            ""
            "QLabel { \n"
            "    font-family: \"Times New Roman\" ;\n"
            "    letter-spacing: 1.5px; \n"
            "    font-style: bold; \n"
            "    font-weight: 200;\n"
            "    font-size: 25pt;\n"
            "    padding: 20px;\n"
            "    qproperty-alignment: AlignCenter; \n"
            "}"
        )

        py_radiobutton_qss: str = (
            "QRadioButton {\n"
            "    spacing: -1px;\n"
            "    padding: 4px 14px;\n"
            "    border: 2px solid rgba(0, 0, 0, 0.3);\n"
            "    border-radius: 7px;\n"
            "    background: qlineargradient(\n"
            "        x1:0, y1:0,\n"
            "        x2:0, y2:1,\n"
            "        stop:0 rgba(50, 50, 50, 180),\n"
            "        stop:1 rgba(30, 30, 30, 200)\n"
            "    );\n"
            "    color: rgba(235, 235, 235, 220);\n"
            "    font-size: 13px;\n"
            "    min-width: 90px;\n"
            "}\n"
            "\n"
            "QRadioButton:hover {\n"
            "    border: 1px solid rgba(255, 255, 255, 0.18);\n"
            "    background: qlineargradient(\n"
            "        x1:0, y1:0,\n"
            "        x2:0, y2:1,\n"
            "        stop:0 rgba(70, 70, 70, 200),\n"
            "        stop:1 rgba(40, 40, 40, 220)\n"
            "    );\n"
            "}\n"
            "\n"
            "QRadioButton:disabled {\n"
            "    border: 2px solid rgba(0, 0, 0, 0.18);\n"
            "    background: qlineargradient(\n"
            "        x1:0, y1:0,\n"
            "        x2:0, y2:1,\n"
            "        stop:0 rgba(38, 38, 38, 120),\n"
            "        stop:1 rgba(24, 24, 24, 140)\n"
            "    );\n"
            "    color: rgba(180, 180, 180, 95);\n"
            "}\n"
            "\n"
            "QRadioButton:checked {\n"
            "  \n"
            "    border: 2px solid rgba(0, 0, 0, 0.3);\n"
            "    \n"
            "    /* Reversed gradient (darker at the top) to create an internal shadow effect */\n"
            "\n"
            "\n"
            "    /* A touch of very muted pink, just to highlight the selection */\n"
            "    color: rgba(230, 190, 255, 0.90); \n"
            "    font-weight: 500; \n"
            "}"
        )
        py_MAX_RBTNS_PER_ROW: int = 4
        py_RBTNS_ENTRIES: list[tuple[str, str, str]] = field(default_factory=lambda: [
            ("PY:UV", "uv", "uv_logo.png"),
            ("PY:VENV", "Venv", "python_logo.png"),
            ("PY:POETRY", "poetry", "poetry_logo.png"),
            ("PY:HATCH", "Hatch", "pip_logo.png"),
            ("PY:GENERIC_CONDA", "conda*", "conda_logo.png"),
            ("PY:PIXI", "Pixi", "pixi_logo.png"),
            ("PY:MAMBA", "Mamba", "mamba_logo.png"),
            ("PY:PIPENV", "PipEnv", "pipenv_logo.png"),
            ("PY:VIRTUALENV", "VirtualEnv", "virtualenv_logo.png"),
            ("PY:PDM", "PDM", "pdm_logo.png"),
            ("PY:MOJO", "Mojo (W.I.P.)", "mojo_logo.png"),
                                                         ])
        py_python_qlabel_coords: tuple[int, int] = (0, 0)
        py_pkg_manager_rbtns_coords: tuple[int, int] = (2, 0)
        py_interpreter_qcombobox_coords: tuple[int, int] = (0, 4)
        py_unb_interpreter_box_coords: tuple[int, int] = (4, 4)
        py_pkg_manager_rbtns_spacing: int = 4
        QlineEditQSS: str = ("\n"
                             "                QLineEdit {\n"
                             "                    font-size: 12px;\n"
                             "                    border: 2px solid rgb(65, 65, 63);\n"
                             "                    border-radius: 5px;\n"
                             "                    background-color: rgb(30, 30, 28);\n"
                             "                    color: rgb(220, 220, 220);\n"
                             "                }\n"
                             "                QLineEdit:hover {\n"
                             "                    border: 2px solid rgb(150, 60, 105);      /* dawn pink */\n"
                             "                    background-color: rgb(38, 38, 36);        /* light pink */\n"
                             "                }\n"
                             "                QLineEdit:focus {\n"
                             "                    border: 2px solid rgb(236, 100, 175);     /* full pink */\n"
                             "                    background-color: rgb(44, 44, 42);\n"
                             "                }\n"
                             "                ")

#@dataclass()
class LogicVariables:
    class EditorCmd:
        @staticmethod
        def get_cmd(editor: str) -> str:
            """reads from config.toml reading th openin command for each editor"""
            key = editor.lower().replace(" ", "_") + "_cmd"
            return TomlHandler.toml_get(CONFIG_PATH, "editors", key) or ""

        @staticmethod
        def get_all_editors() -> list[str]:
            """
                Reads available editors from the [editors] section of config.toml.
                Only reads keys ending in '_cmd' (e.g. 'vscode_cmd', 'nvim_cmd').
                For each editor, looks for an optional '_display' key for the human-readable name
                (e.g. 'nvim_display = "nVim"'). If not found, falls back to .title() on the base name.
                Adding a new editor only requires a new '_cmd' line in the TOML — no code changes needed.
                :rtype: list[str]
                :return:

            """
            try:
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    data = tomlkit.load(f)
                editors = data.get("editors", {})
                result: list[str] = []
                for key in editors:
                    if not key.endswith("_cmd"):
                        continue
                    base = key.removesuffix("_cmd")
                    display_name = TomlHandler.toml_get(CONFIG_PATH, "editors", f"{base}_display") or base.replace("_",
                                                                                                                   " ").title()
                    result.append(display_name)
                return result
            except FileNotFoundError:
                return []


    class PythonVars:
        py_uv_path: str = TomlHandler.toml_get(CONFIG_PATH, "python", "uv_path") or shutil.which("uv") or "" # noqa "" avoids crashes or None by returning an empy string which is falsy
        py_poetry_path: str = TomlHandler.toml_get(CONFIG_PATH, "python", "poetry_path") or shutil.which( "poetry") or ""# noqa
        py_hatch_path: str = TomlHandler.toml_get(CONFIG_PATH, "python", "hatch_path") or shutil.which("hatch") or ""  # noqa
        py_pdm_path: str = TomlHandler.toml_get(CONFIG_PATH, "python", "pdm_path") or shutil.which("pdm") or ""# noqa

        py_pipenv_path: str = TomlHandler.toml_get(CONFIG_PATH, "python", "pipenv_path") or shutil.which("pipenv") or ""# noqa
        py_virtualenv_path: str = TomlHandler.toml_get(CONFIG_PATH, "python", "virtualenv_path") or shutil.which("virtualenv") or ""# noqa
        py_conda_path: str = TomlHandler.toml_get(CONFIG_PATH, "python", "conda_path") or shutil.which("conda") or ""# noqa
        py_mamba_path: str = TomlHandler.toml_get(CONFIG_PATH, "python", "mamba_path") or shutil.which("mamba") or ""# noqa
        py_pixi_path: str = TomlHandler.toml_get(CONFIG_PATH, "python", "pixi_path") or shutil.which("pixi") or ""# noqa #todo have a look here before push
            #----- iCmd stands for Init(ialise) Command -----#
        py_venv_icmd: list[str] = ["python", "-m", "venv", ".venv"]  # python -m venv .venv (dentro proj_path)
        py_uv_icmd: list[str] = [py_uv_path, "init"]  # uv init <proj_path>
        py_poetry_icmd: list[str] = [py_poetry_path, "new"]  # poetry new <proj_path>
        py_hatch_icmd: list[str] = [py_hatch_path, "new"]  # hatch new <proj_path>
        py_pdm_icmd: list[str] = [py_pdm_path, "init"]  # pdm init (cdw=proj_path)
        py_pipenv_icmd: list[str] = [py_pipenv_path, "install"]  # pipenv install (cdw=proj_path)
        py_virtualenv_icmd: list[str] = [py_virtualenv_path, ".venv"]  # virtualenv .venv (cdw=proj_path)
        py_conda_icmd: list[str] = [py_conda_path, "create", "-p"]  # conda create -p <proj_path>
        py_mamba_icmd: list[str] = [py_mamba_path, "create", "-p"]  # mamba create -p <proj_path>
        py_pixi_icmd: list[str] = [py_pixi_path, "init"]  # pixi init <proj_path>



