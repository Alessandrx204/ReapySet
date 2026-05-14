import os
import sys
from dataclasses import dataclass, field
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

    # Base sizes
    mw_width: int = 700
    mw_height: int = 350

    # Expansion
    mw_height_expansion: int = 280
    mw_expanded_height: int = mw_height + mw_height_expansion  # 580

    # Animation
    mw_expansion_time: int = 600
    mw_collapse_time: int = 450
    mw_expand_curve: QEasingCurve.Type = QEasingCurve.Type.OutExpo
    mw_collapse_curve: QEasingCurve.Type = QEasingCurve.Type.OutCubic

    # Internal timers
    mw_widget_enable_delay: int = 45
    mw_fix_size_delay: int = mw_collapse_time + 10

    mw_y_offset: int = -150

    # ── nested classes ──────────────────────────────────

    @dataclass
    class Images:
        """Config images src/resources"""
        root: Path = field(default_factory=_get_root)



        @property
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
        def cpp_logo(self) -> Path: return self.res / "cpp_logo.svg"

    @dataclass
    class Widget1:
        """Widget 1 config"""
        #w1_height: int = 38
        QlineEditQSS: str = """QLineEdit{ font-size: 12px; min-width: 140px; border: 2px solid rgb(65, 65, 63); border-radius: 5px; background-color: rgb(37, 37, 36);}
              QLineEdit:hover {border: 2px solid rgb(236, 100, 175); background-color:rgb(44,44,42);}"""

    @dataclass
    class LangBtnWidget:
        """Widget 2: central widget con i bottoni lingua"""
        images: "MwConfig.Images" = field(default_factory=lambda: MwConfig.Images())


        @property
        def button_dict(self) -> dict[str, list]:
            img = self.images
            return {
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

        enabled_btns:   list[int] = field(default_factory=lambda: [0])
        cw_height:      int = 120
        max_btn_x_row:  int = 5
