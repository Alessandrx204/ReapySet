import os
import sys
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path


from PySide6.QtCore import QEasingCurve


def _get_root() -> Path:
    if hasattr(sys, "frozen"):
        return Path(os.path.dirname(sys.executable))
    return Path(__file__).resolve().parent


@dataclass
class MwConfig:
    """Main Window configs"""
    mw_title: str = "ReapySet"

    mw_width: int = 765
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
        sample_box_placeholder_txt: str = "Leave Blank for None"
        browse_button_text: str         = "Browse"
        select_editor_Combobox_top_label: str = ""

        # plain class variable — accessible directly on the class without instantiation
        select_editor_Combobox_entry = [
            "VSCode", "Pycharm", "Godot",
            "Intellij IDEA", "Clion", "Zed",
            "Sublime Text", "Notepad++", "nVim"
                                        ]

    @dataclass
    class LangBtnWidget:
        """Widget 2: language selector buttons"""
        images: "MwConfig.Images" = field(default_factory=lambda: MwConfig.Images())
        enabled_btns: list[int]   = field(default_factory=lambda: [0])
        cw_height:     int = 120
        max_btn_x_row: int = 5

        # built once at init instead of being recreated on every access
        button_dict: dict = field(init=False)

        def __post_init__(self):
            img = self.images
            self.button_dict = {
                "Python":        ["PY",       img.python_logo],
                "Rust":          ["RUST",     img.rust_logo],
                ".NET":          ["DOTNET",   img.dotnet_logo],
                "Kotlin/Java":   ["KT",       img.kotlin_logo],
                "C/C++":         ["CPP",      img.cpp_logo],
                "Ts/JavaScript": ["TSJS",     img.javascript_logo],
                "GO":            ["GO",       img.go_logo],
                "Lua":           ["LUA",      img.lua_logo],
                "GDScript":      ["GDSCRIPT", img.godot_logo],
            }


    @dataclass
    class Widget3:
        """Widget 3: per language widgets"""

        """python"""
        py_qlabel_txt: str = "Please Setup Your Python Workspace! (^-^)/"
        py_qlabel_qss: str = """QLabel { 
            font-family: "Times New Roman" ;
            letter-spacing: 1.5px; 
            font-style: bold; 
            font-weight: 200;
            font-size: 25pt;
            padding: 20px;
            qproperty-alignment: AlignCenter; 
        }"""
        py_radiobutton_qss: str = """QRadioButton {
    spacing: -1px;
    padding: 4px 14px;
    border: 2px solid rgba(0, 0, 0, 0.3);
    border-radius: 7px;
    background: qlineargradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:0 rgba(50, 50, 50, 180),
        stop:1 rgba(30, 30, 30, 200)
    );
    color: rgba(235, 235, 235, 220);
    font-size: 13px;
    min-width: 90px;
}

QRadioButton:hover {
    border: 1px solid rgba(255, 255, 255, 0.18);
    background: qlineargradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:0 rgba(70, 70, 70, 200),
        stop:1 rgba(40, 40, 40, 220)
    );
}


QRadioButton:checked {
  
    border: 2px solid rgba(0, 0, 0, 0.3);
    
    /* Reversed gradient (darker at the top) to create an internal shadow effect */


    /* A touch of very muted pink, just to highlight the selection */
    color: rgba(230, 190, 255, 0.90); 
    font-weight: 500; 
}"""
        py_MAX_RBTNS_PER_ROW: int = 4
        py_RBTNS_ENTRIES: list[tuple[str, str, str]] = field(default_factory=lambda: [
            ("PY:UV", "uv", "uv_logo.png"),
            ("PY:VENV", "Venv(default)", "python_logo.png"),
            ("PY:POETRY", "poetry", "poetry_logo.png"),
            ("PY:HATCH", "Hatch", "pip_logo.png"),
            ("PY:GENERIC_CONDA", "conda*", "conda_logo.png"),
            ("PY:PIXI", "Pixi", "pixi_logo.png"),
            ("PY:MAMBA", "Mamba", "mamba_logo.png"),
            ("PY:PIPENV", "PipEnv", "pipenv_logo.png"),
            ("PY:VIRTUALENV", "VirtualEnv", "virtualenv_logo.png"),
            ("PY:PDM", "PDM", "pdm_logo.png"),
                                                         ])
        py_python_qlabel_coords: tuple[int, int] = (0, 0)
        py_pkg_manager_rbtns_coords: tuple[int, int] = (2, 0)
        py_interpreter_qcombobox_coords: tuple[int, int] = (0, 4)
        py_pkg_manager_rbtns_spacing: int = 4
        py_uv_path: str = "/opt/homebrew/bin/uv"
        py_poetry_path: str = ""
        py_hatch_path: str = ""
        py_pdm_path: str = ""
        py_pipenv_path: str = ""
        py_virtualenv_path: str = ""
        py_conda_path: str = ""
        py_mamba_path: str = ""
        py_pixi_path: str = ""



