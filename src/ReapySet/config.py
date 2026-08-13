from __future__ import annotations
import os
import shutil
import sys
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path

import tomlkit
from PySide6.QtCore import QEasingCurve

import lang
from ReapySet.common.toml_handler import TomlHandler, CONFIG_PATH

def _get_root() -> Path:
    if hasattr(sys, "frozen"):
        return Path(os.path.dirname(sys.executable))
    return Path(__file__).resolve().parent


@dataclass
class MwConfig:
    """Main Window configs"""

    mw_title: str = lang.MwConfig.mw_title # ReapySet
    default_label: str = lang.MwConfig.default_label # (default)
    #------ general configs --------#
    file_menu: str = lang.MwConfig.file_menu
    view_menu: str = lang.MwConfig.view_menu
    help_menu: str = lang.MwConfig.help_menu
    settings_menu: str = lang.MwConfig.settings_menu
    quit_action: str = lang.MwConfig.quit_action
    locate_config_file_action_txt: str = lang.MwConfig.locate_config_file_action_txt
    locate_input_cache_file_action_txt: str = lang.MwConfig.locate_input_cache_file_action_txt
    locate_log_file_action_txt: str = lang.MwConfig.locate_log_file_action_txt

    reset_window_pos_action_txt: str = lang.MwConfig.reset_window_pos_action_txt
    github_action: str = lang.MwConfig.github_action
    license_action: str = lang.MwConfig.license_action
    third_party_licenses_action: str = lang.MwConfig.third_party_licenses_action
    about_action: str = lang.MwConfig.about_action
    about_txt_title: str = lang.MwConfig.about_txt_title
    about_txt: str = lang.MwConfig.about_txt

    toml_error_txt: str = lang.MwConfig.toml_error_txt
    toml_error_txt_title: str = lang.MwConfig.toml_error_txt_title
    toml_settings_window_title: str = lang.MwConfig.toml_settings_window_title
    toml_settings_window_save_button: str= lang.MwConfig.toml_settings_window_save_button
    toml_settings_window_close_button: str = lang.MwConfig.toml_settings_window_close_button

    mw_width: int = 770
    _mw_height: int = 380 # cos ill be got from config
    mw_height_expansion: int = 280

    @classmethod
    def mw_height(cls) -> int:
        return TomlHandler.toml_get(CONFIG_PATH, "advanced", "main_window_height") or cls._mw_height

    @classmethod
    def mw_expanded_height(cls) -> int:
        return cls.mw_height() + cls.mw_height_expansion


    mw_expansion_time: int = 600
    mw_collapse_time: int = 450
    mw_expand_curve: QEasingCurve.Type = QEasingCurve.Type.OutExpo
    mw_collapse_curve: QEasingCurve.Type = QEasingCurve.Type.OutCubic

    mw_widget_enable_delay: int = 45
    mw_fix_size_delay: int = mw_collapse_time + 10

    mw_y_offset: int = -150

    #----pop-ups------#
    learn_more_txt: str = lang.MwConfig.learn_more_txt
    download_btn_txt: str = lang.MwConfig.download_btn_txt
    NONE_editor_display: str = lang.MwConfig.NONE_editor_display

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
        def cc_logo_path(self) -> Path: return self.res / "cookiecutter-logo.svg"
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
        github_box_top_label: str       = lang.MwConfig.Widget1.github_box_top_label
        github_box_placeholder_txt: str = lang.MwConfig.Widget1.github_box_placeholder_txt #insert a repo URL
        path_box_top_label: str         = lang.MwConfig.Widget1.path_box_top_label
        path_box_placeholder_txt: str   = lang.MwConfig.Widget1.path_box_placeholder_txt
        sample_box_top_label: str       = lang.MwConfig.Widget1.sample_box_top_label
        ccboilerplates_box_placeholder_txt: str = lang.MwConfig.Widget1.ccboilerplates_box_placeholder_txt
        cookiecutter_error_msg: str = lang.MwConfig.Widget1.cookiecutter_error_msg
        browse_button_text: str         = "Browse"
        select_editor_Combobox_top_label: str = ""

        # plain class variable — accessible directly on the class without instantiation
        select_editor_Combobox_entry: tuple[str] = field(
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
        images: MwConfig.Images = field(default_factory=lambda: MwConfig.Images()) # aving future i can usw MwConfig.Images
        enabled_btns: set[int]   = field(default_factory=lambda: {0})
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
                "Python":                 ["PY",       img.python_logo],
                "Ts/JavaScript (W.I.P.)": ["TSJS",     img.javascript_logo],
                "Rust (W.I.P.)":          ["RUST",     img.rust_logo],
                ".NET (W.I.P.)":          ["DOTNET",   img.dotnet_logo],
                "Kotlin/Java (W.I.P.)":   ["KT",       img.kotlin_logo],
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
        py_qlabel_txt: str = lang.MwConfig.Widget3.py_qlabel_txt
        py_interp_qcbox_top_txt: str = lang.MwConfig.Widget3.py_interp_qcbox_top_txt
        py_unb_interp_qlinedit_top_txt: str = lang.MwConfig.Widget3.py_unb_interp_qlinedit_top_txt
        py_unb_interp_qlinedit_inner_txt: str = lang.MwConfig.Widget3.py_unb_interp_qlinedit_inner_txt
        py_frameworks_sep_label_txt: str = lang.MwConfig.Widget3.py_frameworks_sep_label_txt

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
            "    padding: 3px 14px;\n"
            "    border: 2px solid rgba(0, 0, 0, 0.3);\n"
            "    border-radius: 7px;\n"
            "    background: qlineargradient(\n"
            "        x1:0, y1:0,\n"
            "        x2:0, y2:1,\n"
            "        stop:0 rgba(50, 50, 50, 180),\n"
            "        stop:1 rgba(30, 30, 30, 200)\n"
            "    );\n"
            "    color: rgba(235, 235, 235, 220);\n"
            "    font-size: 12px;\n"
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
        uv_error_msg: str = lang.MwConfig.Widget3.uv_error_msg
        conda_mamaba_error_msg: str = lang.MwConfig.Widget3.conda_mamba_error_msg

        py_MAX_RBTNS_PER_ROW: int = 4
        py_PM_RBTNS_ENTRIES: tuple[tuple[str, str, str, str], ...] = field(default_factory=lambda: (
            ("PY:UV", "uv", "uv_logo.png",
             lang.MwConfig.Widget3.py_uv_tooltip),

            ("PY:VENV", "Venv", "python_logo.png",
             lang.MwConfig.Widget3.py_pip_tooltip),

            ("PY:POETRY", "Poetry", "poetry_logo.png",
             lang.MwConfig.Widget3.py_poetry_tooltip),

            ("PY:HATCH", "Hatch", "pip_logo.png",
             lang.MwConfig.Widget3.py_hatch_tooltip),

            ("PY:CONDA", "Conda", "conda_logo.png",
             lang.MwConfig.Widget3.py_conda_tooltip),

            ("PY:PIXI", "Pixi", "pixi_logo.png",
             lang.MwConfig.Widget3.py_pixi_tooltip),

            ("PY:MAMBA", "Mamba", "mamba_logo.png",
             lang.MwConfig.Widget3.py_mamba_tooltip),

            ("PY:PIPENV", "Pipenv", "pipenv_logo.png",
             lang.MwConfig.Widget3.py_pipenv_tooltip),

            ("PY:VIRTUALENV", "Virtualenv", "virtualenv_logo.png",
             lang.MwConfig.Widget3.py_virtualenv_tooltip),

            ("PY:PDM", "PDM", "pdm_logo.png",
             lang.MwConfig.Widget3.py_pdm_tooltip),
            #("PY:MOJO", "Mojo (W.I.P.)", "mojo_logo.png", ""),
                                                                ))
        py_FMK_RBTNS_ENTRIES: tuple[tuple[str, str, str, str], ...] = field(default_factory=lambda: (
            ("PY:DJANGO", f"Django{" "*6}", "django_logo.png",
             lang.MwConfig.Widget3.py_django_tooltip),

            ("PY:FLASK", "Flask", "flask_logo.png",
             lang.MwConfig.Widget3.py_flask_tooltip),

            ("PY:FASTAPI", "FastAPI", "fastapi_logo.png",
             lang.MwConfig.Widget3.py_fastapi_tooltip),

            ("PY:STREAMLIT", "Streamlit", "streamlit_logo.png",
             lang.MwConfig.Widget3.py_streamlit_tooltip),

            ("PY:PYSCRIPT", "PyScript", "pyscript_logo.png",
             lang.MwConfig.Widget3.py_pyscript_tooltip),

            ("PY:PYSIDE6", "PySide6", "pyside6_logo.png",
             lang.MwConfig.Widget3.py_pyside6_tooltip),

            ("PY:JUPYTER", "Jupyter N.book", "jupyter_logo.png",
             lang.MwConfig.Widget3.py_jupyter_tooltip),
        ))
        py_python_qlabel_coords: tuple[int, int] = (0, 0)
        py_pkg_manager_rbtns_coords: tuple[int, int] = (2, 0)
        py_frameworks_sep_label_coords: tuple[int, int] = (4, 0)
        py_fmk_rbtns_coords: tuple[int, int] = (5, 0)

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
    class ConstantUtils:
        IS_POSIX: bool = sys.platform != "win32"

    class EditorCmd:
        @staticmethod
        def get_cmd(p_editor: str) -> str:
            """reads from config.toml reading th openin command for each editor"""
            key = p_editor.lower().replace(" ", "_") + "_cmd"
            return TomlHandler.toml_get(CONFIG_PATH, "editors", key) or ""

        @staticmethod
        def get_all_editors() -> tuple[str, ...]:
            """
                        Reads available editors from the [editors] section of config.toml.
                        Only reads keys ending in '_cmd' (e.g. 'vscode_cmd', 'nvim_cmd').
                        For each editor, looks for an optional '_display' key for the human-readable name.
            """
            try:
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    data: tomlkit.TOMLDocument = tomlkit.load(f)

                editors = data.get("editors", {})
                result = []

                for key in editors:
                    if key.endswith("_cmd"):
                        base = key.removesuffix("_cmd")
                        display_name: str = (
                                editors.get(f"{base}_display") # if has got banana_cmd it looks for a banana_display in case its spelled funny alike 90% of code editors like BånaNà
                                or base.replace("_", " ").title()# if  none it capitalises each word in the base name and replaces underscores with spaces, e.g. "vscode" becomes "Vscode"
                                if base != "none".upper() else f"{MwConfig.NONE_editor_display}" #No editor option for localisation



                        )
                        result.append(display_name)

                return tuple(result) # converts to tuple to hold less ram

            except FileNotFoundError:
                return ()

    class PythonVars:
        py_uv_path: str = TomlHandler.toml_get(CONFIG_PATH, "python", "uv_path") or shutil.which("uv") or "" # noqa "" avoids crashes or None by returning an empy string which is falsy
        py_poetry_path: str = TomlHandler.toml_get(CONFIG_PATH, "python", "poetry_path") or shutil.which( "poetry") or ""# noqa
        py_hatch_path: str = TomlHandler.toml_get(CONFIG_PATH, "python", "hatch_path") or shutil.which("hatch") or ""  # noqa
        py_pdm_path: str = TomlHandler.toml_get(CONFIG_PATH, "python", "pdm_path") or shutil.which("pdm") or ""# noqa

        py_pipenv_path: str = TomlHandler.toml_get(CONFIG_PATH, "python", "pipenv_path") or shutil.which("pipenv") or ""# noqa
        py_virtualenv_path: str = TomlHandler.toml_get(CONFIG_PATH, "python", "virtualenv_path") or shutil.which("virtualenv") or ""# noqa
        py_conda_path: str = TomlHandler.toml_get(CONFIG_PATH, "python", "conda_path") or shutil.which("conda") or ""# noqa
        py_mamba_path: str = TomlHandler.toml_get(CONFIG_PATH, "python", "mamba_path") or shutil.which("mamba") or ""# noqa
        py_pixi_path: str = TomlHandler.toml_get(CONFIG_PATH, "python", "pixi_path") or shutil.which("pixi") or ""# noqa
            #----- iCmd stands for Init(ialise) Command -----#
        py_uv_icmd: list[str] = [py_uv_path, "init"]  # uv init <proj_path>
        py_poetry_icmd: list[str] = [py_poetry_path, "new"]  # poetry new <proj_path>
        py_hatch_icmd: list[str] = [py_hatch_path, "new"]  # hatch new <proj_path>
        py_pdm_icmd: list[str] = [py_pdm_path, "init"]  # pdm init (cdw=proj_path)
        py_pipenv_icmd: list[str] = [py_pipenv_path, "install"]  # pipenv install (cdw=proj_path)
        py_virtualenv_icmd: list[str] = [py_virtualenv_path,
                                         "--python"]  # virtualenv -p <python_interpreter> .venv (cdw=proj_path)
        py_conda_icmd: list[str] = [py_conda_path, "create",
                                    "--yes",
                                    "--prefix"]  # conda create --prefix <proj_path>/.conda
        py_mamba_icmd: list[str] = [py_mamba_path, "create",
                                    "--yes",
                                    "--prefix"]  # mamba create --prefix <proj_path>

        py_pixi_icmd: list[str] = [py_pixi_path, "init"]  # pixi init <proj_path>

    package_names: dict[str, dict[str, str]] = {
        "pipenv": {
            "brew": "pipenv",
            "apt": "pipenv",
        },

        "poetry": {
            "brew": "poetry",
            "apt": "python3-poetry",
        },

        "pdm": {
            "brew": "pdm",
            "apt": "python3-pdm",
        },

        "hatch": {
            "winget": "PyPA.Hatch",
            "brew": "hatch",
        },

        "uv": {
            "winget": "astral-sh.uv",
            "choco": "uv",
            "brew": "uv",
            "snap": "astral-uv",
        },

        "virtualenv": {
            "brew": "virtualenv",
            "apt": "virtualenv",
        },

        "pixi": {
            "winget": "prefix-dev.pixi",
            "brew": "pixi",
        },

        "conda": {
            # too difficult to implement rn

        },

        "mamba": {
            # too difficult to implement rn
        },
    }



