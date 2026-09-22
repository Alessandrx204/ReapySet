from __future__ import annotations
import os
import shutil
import sys
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path

import tomlkit
from PySide6.QtCore import QEasingCurve

from ReapySet import lang
from ReapySet.common.toml_handler import TomlHandler, CONFIG_PATH




class ThemeColors:
    DARK: dict[str, str] = {
        #QStatusBar
        "QStatusBar": "#202126",# QPallette only accepts hexes

        # Qlinedits
        "background": "rgb(30, 30, 28)",
        "background_hover": "rgb(38, 38, 36)",
        "background_focus": "rgb(44, 44, 42)",

        # Text
        "text": "rgb(220, 220, 220)",
        "text_strong": "white",
        "text_disabled": "gray",
        "label": "#efebf0",

        # Borders
        "border": "rgb(65, 65, 63)",
        "border_hover": "rgb(150, 60, 105)",
        "border_focus": "rgb(236, 100, 175)",

        # Accent
        "accent": "rgba(255, 170, 220, 1.0)",
        "accent_hover": "rgba(255, 190, 235, 1.0)",
        "accent_soft": "rgba(230, 190, 255, 0.90)",

        # Button surfaces
        "button_top": "#66676b",
        "button_mid": "#5f6063",
        "button_bottom": "#57585a",

        "button_hover_top": "#96788f",
        "button_hover_mid": "#896d84",
        "button_hover_bottom": "#80637a",

        "button_checked_top": "#734860",
        "button_checked_mid": "#643a52",
        "button_checked_bottom": "#593047",

        # Language buttons - normal

        "lang_btn_top": "#66676b",

        "lang_btn_mid": "#5f6063",

        "lang_btn_bottom": "#57585a",

        "lang_btn_text": "#f3eaf0",

        "lang_btn_border_top": "#c28cb7",

        "lang_btn_border_side": "#9e8299",

        "lang_btn_border_bottom": "#736473",

        # Hover

        "lang_btn_hover_top": "#96788f",

        "lang_btn_hover_mid": "#896d84",

        "lang_btn_hover_bottom": "#80637a",

        "lang_btn_hover_text": "#ffd9e9",

        "lang_btn_hover_border_top": "#ffc5df",

        "lang_btn_hover_border_left": "#f0a2c5",

        "lang_btn_hover_border_right": "#d989b0",

        "lang_btn_hover_border_bottom": "#8d627d",

        # Pressed

        "lang_btn_pressed_top": "#4d424b",

        "lang_btn_pressed_bottom": "#433841",

        "lang_btn_pressed_text": "#ffe3ef",

        "lang_btn_pressed_border_top": "#6d5565",

        "lang_btn_pressed_border_side": "#8e647d",

        "lang_btn_pressed_border_bottom": "#b97e9e",

        # Checked

        "lang_btn_checked_top": "#734860",

        "lang_btn_checked_mid": "#643a52",

        "lang_btn_checked_bottom": "#593047",

        "lang_btn_checked_text": "#ffe0ec",

        "lang_btn_checked_border_top": "#ffc8de",

        "lang_btn_checked_border_left": "#f1a5c8",

        "lang_btn_checked_border_right": "#d887ad",

        "lang_btn_checked_border_bottom": "#8d5c77",

        # Checked + hover

        "lang_btn_checked_hover_top": "#81506a",

        "lang_btn_checked_hover_mid": "#74455e",

        "lang_btn_checked_hover_bottom": "#673a53",

        "lang_btn_checked_hover_text": "#fff0f7",

        "lang_btn_checked_hover_border_top": "#ffd9ea",

        "lang_btn_checked_hover_border_left": "#ffb7d3",

        "lang_btn_checked_hover_border_right": "#e092b7",

        "lang_btn_checked_hover_border_bottom": "#99657f",

        # Disabled

        "lang_btn_disabled_top": "#444548",

        "lang_btn_disabled_bottom": "#37383b",

        "lang_btn_disabled_text": "#7f7178",

        "lang_btn_disabled_border": "#534a52",

        "window_background": "#202124",
    }

    LIGHT: dict[str, str] = {

        # QStatusBar
        "QStatusBar": "#a0948a",# QPallette only accepts hexes

        # Qlinedits
        "background": "rgb(246, 246, 250)",#"rgb(216, 206, 192)",
        "background_hover": "rgb(234, 204, 202)",
        "background_focus": "rgb(238, 228, 222)",

        # Text
        "text": "rgb(45, 42, 40)",
        "text_strong": "rgb(25, 23, 22)",
        "text_disabled": "rgb(33, 33, 33)",
        "label": "rgb(48, 43, 46)",

        # Borders
        "border": "rgb(160, 148, 138)",
        "border_hover": "rgb(150, 60, 105)",
        "border_focus": "rgb(210, 70, 145)",

        # Accent
        "accent": "rgb(180, 70, 130)",
        "accent_hover": "rgb(205, 90, 155)",
        "accent_soft": "rgb(205, 90, 155)",


        # Button surfaces
        "button_top": "rgb(232, 223, 212)",
        "button_mid": "rgb(222, 212, 200)",
        "button_bottom": "rgb(210, 199, 186)",

        "button_hover_top": "rgb(228, 198, 214)",
        "button_hover_mid": "rgb(218, 184, 203)",
        "button_hover_bottom": "rgb(205, 171, 190)",

        "button_checked_top": "rgb(190, 135, 164)",
        "button_checked_mid": "rgb(177, 119, 150)",
        "button_checked_bottom": "rgb(162, 104, 136)",
        "lang_btn_top": "rgb(235, 226, 216)",

        "lang_btn_mid": "rgb(224, 214, 202)",

        "lang_btn_bottom": "rgb(212, 201, 188)",

        "lang_btn_text": "rgb(55, 48, 52)",

        "lang_btn_border_top": "rgb(193, 151, 178)",

        "lang_btn_border_side": "rgb(171, 145, 160)",

        "lang_btn_border_bottom": "rgb(145, 122, 136)",

        # Hover

        "lang_btn_hover_top": "rgb(229, 197, 214)",

        "lang_btn_hover_mid": "rgb(218, 181, 202)",

        "lang_btn_hover_bottom": "rgb(205, 166, 190)",

        "lang_btn_hover_text": "rgb(72, 38, 57)",

        "lang_btn_hover_border_top": "rgb(220, 115, 169)",

        "lang_btn_hover_border_left": "rgb(206, 102, 158)",

        "lang_btn_hover_border_right": "rgb(190, 88, 143)",

        "lang_btn_hover_border_bottom": "rgb(153, 92, 125)",

        # Pressed

        "lang_btn_pressed_top": "rgb(184, 158, 172)",

        "lang_btn_pressed_bottom": "rgb(169, 143, 157)",

        "lang_btn_pressed_text": "rgb(55, 30, 45)",

        "lang_btn_pressed_border_top": "rgb(135, 103, 120)",

        "lang_btn_pressed_border_side": "rgb(157, 110, 137)",

        "lang_btn_pressed_border_bottom": "rgb(181, 105, 146)",

        # Checked

        "lang_btn_checked_top": "rgb(190, 135, 164)",

        "lang_btn_checked_mid": "rgb(177, 119, 150)",

        "lang_btn_checked_bottom": "rgb(162, 104, 136)",

        "lang_btn_checked_text": "rgb(54, 28, 43)",

        "lang_btn_checked_border_top": "rgb(220, 123, 173)",

        "lang_btn_checked_border_left": "rgb(207, 105, 160)",

        "lang_btn_checked_border_right": "rgb(190, 88, 143)",

        "lang_btn_checked_border_bottom": "rgb(143, 82, 115)",

        # Checked + hover

        "lang_btn_checked_hover_top": "rgb(204, 148, 177)",

        "lang_btn_checked_hover_mid": "rgb(192, 130, 162)",

        "lang_btn_checked_hover_bottom": "rgb(177, 114, 149)",

        "lang_btn_checked_hover_text": "rgb(45, 22, 35)",

        "lang_btn_checked_hover_border_top": "rgb(229, 137, 183)",

        "lang_btn_checked_hover_border_left": "rgb(216, 118, 171)",

        "lang_btn_checked_hover_border_right": "rgb(199, 98, 153)",

        "lang_btn_checked_hover_border_bottom": "rgb(154, 90, 124)",

        # Disabled

        "lang_btn_disabled_top": "rgb(205, 196, 186)",

        "lang_btn_disabled_bottom": "rgb(192, 182, 171)",

        "lang_btn_disabled_text": "rgb(145, 135, 139)",

        "lang_btn_disabled_border": "rgb(174, 160, 166)",

        "window_background": "rgb(216, 205, 192)",

    }



    @classmethod
    def get(cls, theme: str) -> dict[str, str]:
        return cls.LIGHT if theme == "light" else cls.DARK



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
        def python_wallpaper_dark(self) -> Path: return self.res / "python_free_wallpaper_dark.png"
        @property
        def python_wallpaper_light(self) -> Path: return self.res / "python_free_wallpaper_light.png"

    @dataclass
    class Widget1:
        """Widget 1 config"""

        @staticmethod
        def qlineedit_qss(theme: str) -> str:
            c = ThemeColors.get(theme)

            return f"""
            QLineEdit {{
                font-size: 12px;
                min-width: 140px;
                border: 2px solid {c["border"]};
                border-radius: 5px;
                background-color: {c["background"]};
                color: {c["text"]};
            }}

            QLineEdit:hover {{
                border: 2px solid {c["border_hover"]};
                background-color: {c["background_hover"]};
            }}

            QLineEdit:focus {{
                border: 2px solid {c["border_focus"]};
                background-color: {c["background_focus"]};
            }}
            """

        @staticmethod
        def qcombobox_qss(theme: str) -> str:
            c = ThemeColors.get(theme)

            return f"""
            QComboBox {{
                color: {c["text"]};
                background-color: {c["background"]};
            }}

            QComboBox QAbstractItemView {{
                color: {c["text"]};
                background-color: {c["background"]};
            }}
            """

        @staticmethod
        def qstatusbar_qss(theme: str) -> str:
            c = ThemeColors.get(theme)

            return f"""
                        QStatusBar {{
                        
                            background-color: {c["QStatusBar"]};
                            color: #ffffff;
                            font-size: 12px;
                            border-top: 0.5px solid #555555;
                                    }}
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

        @staticmethod
        def lang_btns_qss(theme: str) -> str:
            c = ThemeColors.get(theme)

            return f"""
            QPushButton {{
                background-color: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 {c["lang_btn_top"]},
                    stop:0.45 {c["lang_btn_mid"]},
                    stop:1 {c["lang_btn_bottom"]}
                );

                color: {c["lang_btn_text"]};

                border-top: 1.25px solid {c["lang_btn_border_top"]};
                border-left: 1px solid {c["lang_btn_border_side"]};
                border-right: 1px solid {c["lang_btn_border_side"]};
                border-bottom: 2px solid {c["lang_btn_border_bottom"]};

                border-radius: 7px;
                padding: 6px 18px;
            }}

            QPushButton:hover {{
                background-color: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 {c["lang_btn_hover_top"]},
                    stop:0.5 {c["lang_btn_hover_mid"]},
                    stop:1 {c["lang_btn_hover_bottom"]}
                );

                color: {c["lang_btn_hover_text"]};

                border-top: 1px solid {c["lang_btn_hover_border_top"]};
                border-left: 1px solid {c["lang_btn_hover_border_left"]};
                border-right: 1px solid {c["lang_btn_hover_border_right"]};
                border-bottom: 2px solid {c["lang_btn_hover_border_bottom"]};
            }}

            QPushButton:pressed {{
                background-color: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 {c["lang_btn_pressed_top"]},
                    stop:1 {c["lang_btn_pressed_bottom"]}
                );

                color: {c["lang_btn_pressed_text"]};

                border-top: 1px solid {c["lang_btn_pressed_border_top"]};
                border-left: 1px solid {c["lang_btn_pressed_border_side"]};
                border-right: 1px solid {c["lang_btn_pressed_border_side"]};
                border-bottom: 1px solid {c["lang_btn_pressed_border_bottom"]};

                padding-top: 7px;
                padding-bottom: 5px;
            }}

            QPushButton:checked {{
                background-color: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 {c["lang_btn_checked_top"]},
                    stop:0.5 {c["lang_btn_checked_mid"]},
                    stop:1 {c["lang_btn_checked_bottom"]}
                );

                color: {c["lang_btn_checked_text"]};

                border-top: 1px solid {c["lang_btn_checked_border_top"]};
                border-left: 1px solid {c["lang_btn_checked_border_left"]};
                border-right: 1px solid {c["lang_btn_checked_border_right"]};
                border-bottom: 2px solid {c["lang_btn_checked_border_bottom"]};
            }}

            QPushButton:checked:hover {{
                background-color: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 {c["lang_btn_checked_hover_top"]},
                    stop:0.5 {c["lang_btn_checked_hover_mid"]},
                    stop:1 {c["lang_btn_checked_hover_bottom"]}
                );

                color: {c["lang_btn_checked_hover_text"]};

                border-top: 1px solid {c["lang_btn_checked_hover_border_top"]};
                border-left: 1px solid {c["lang_btn_checked_hover_border_left"]};
                border-right: 1px solid {c["lang_btn_checked_hover_border_right"]};
                border-bottom: 2px solid {c["lang_btn_checked_hover_border_bottom"]};
            }}

            QPushButton:disabled {{
                background-color: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 {c["lang_btn_disabled_top"]},
                    stop:1 {c["lang_btn_disabled_bottom"]}
                );

                color: {c["lang_btn_disabled_text"]};
                border: 1px solid {c["lang_btn_disabled_border"]};
            }}

            QPushButton[selected="true"]:disabled {{
                background-color: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 {c["lang_btn_checked_top"]},
                    stop:0.5 {c["lang_btn_checked_mid"]},
                    stop:1 {c["lang_btn_checked_bottom"]}
                );

                color: {c["lang_btn_checked_text"]};

                border-top: 1px solid {c["lang_btn_checked_border_top"]};
                border-left: 1px solid {c["lang_btn_checked_border_left"]};
                border-right: 1px solid {c["lang_btn_checked_border_right"]};
                border-bottom: 2px solid {c["lang_btn_checked_border_bottom"]};
            }}
            """

        # built once at init instead of being recreated on every access
        button_dict: dict = field(init=False)

        def __post_init__(self):
            img = self.images
            self.button_dict = {
                "Python":                 ["PY",       img.python_logo],
                "Ts/JavaScript (W.I.P.)": ["JS",     img.javascript_logo],
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

        py_qccombobox_toptxt_qss = f"""
            QLabel {{
                font-family: Arial;
                font-weight: bold;
                font-size: 10px;
                color: white;
            }}
            """

        py_qlabel_qss: str = (
            ""
            "QLabel { \n"
            "    font-family: \"Arial\" ;\n"
            "    letter-spacing: 1.5px; \n"
            "    font-style: normal; \n"
            "    color: white; \n"
            "    font-weight: 200;\n"
            f"    font-size: {23 if os.name != 'nt' else 18}pt;\n"
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
        py_qcheckbox_qss: str = """
                                    QCheckBox {
                                        font-family: "Arial";
                                        font-size: 13pt;
                                        font-weight: 300;
                                        letter-spacing: 2px;
                                        color: white;
                                    
                                        spacing: 5px;
                                        padding: 0px;
                                        margin-left: 57px; /* 7 px on the right to be aligned with the interpt. qcheckbox*/
                                    }
                                    
                                    QCheckBox:hover {
                                        color: rgba(230, 190, 255, 0.90);
                                    }
                                    
                                    QCheckBox:checked {
                                        color: rgba(255, 170, 220, 1.0);
                                    }
                                    
                                    QCheckBox:checked:hover {
                                        color: rgba(255, 190, 235, 1.0);
                                    }
                                    
                                    QCheckBox:disabled {
                                        color: gray;
                                    }
                                                      """
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

            ("PY:FASTAPI", f"FastAPI{" "*6}", "fastapi_logo.png",
             lang.MwConfig.Widget3.py_fastapi_tooltip),

            ("PY:STREAMLIT", f"Streamlit{" "*6}", "streamlit_logo.png",
             lang.MwConfig.Widget3.py_streamlit_tooltip),

            ("PY:PYSCRIPT", "PyScript", "pyscript_logo.png",
             lang.MwConfig.Widget3.py_pyscript_tooltip),

            ("PY:PYSIDE6", "PySide6", "pyside6_logo.png",
             lang.MwConfig.Widget3.py_pyside6_tooltip),

            ("PY:JUPYTER", "Jupyter N.book", "jupyter_logo.png",
             lang.MwConfig.Widget3.py_jupyter_tooltip),
            ("PY:MARIMO", "Marimo N.book", "marimo_logo.png",
             lang.MwConfig.Widget3.py_marimo_tooltip),
        ))
        py_python_qlabel_coords: tuple[int, int] = (0, 0)
        py_pkg_manager_rbtns_coords: tuple[int, int] = (2, 0)
        py_frameworks_sep_label_coords: tuple[int, int] = (4, 0)
        py_fmk_rbtns_coords: tuple[int, int] = (5, 0)
        py_pytest_qcheckbox_coords: tuple[int, int] = (1,4)

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



