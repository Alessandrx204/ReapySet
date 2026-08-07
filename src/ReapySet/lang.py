from typing import cast
from tomlkit import TOMLDocument
from ReapySet.common.toml_handler import TomlHandler, I18N_FILE_PATH, CONFIG_PATH


_I18N: TOMLDocument = TomlHandler._toml_read(I18N_FILE_PATH)
_LANGUAGE: str = cast(str, lang # the linter thinks it knows it may be nonìe but its false
    if (lang := TomlHandler.toml_get(CONFIG_PATH, "personal", "language")) in _I18N
    else "en"# := assigns a temp val
)
_CONFIG_DOC = TomlHandler._toml_read(CONFIG_PATH)

# 2. Extracts the language from the documentin memory :
_raw_lang = _CONFIG_DOC.get("personal", {}).get("language") or "en"
_LANGUAGE: str = _raw_lang if _raw_lang in _I18N else "en"

# 3. Saves the current i18n section:
_lang = _I18N[_LANGUAGE]

class MwConfig:
    """Localisable Main Window strings and styles."""


    _section = _lang["MwConfig"] # type: ignore


    mw_title: str = _section["mw_title"]
    default_label: str = _section["default_label"]

    file_menu: str = _section["file_menu"]
    view_menu: str = _section["view_menu"]
    help_menu: str = _section["help_menu"]
    settings_menu: str = _section["settings_menu"]
    quit_action: str = _section["quit_action"]
    locate_config_file_action_txt: str = _section["locate_config_file_action_txt"]
    locate_input_cache_file_action_txt: str = _section["locate_input_cache_file_action_txt"]
    reset_window_pos_action_txt: str = _section["reset_window_pos_action_txt"]
    github_action: str = _section["github_action"]
    license_action: str = _section["license_action"]
    third_party_licenses_action: str = _section["third_party_licenses_action"]
    about_action: str = _section["about_action"]
    about_txt_title: str = _section["about_txt_title"]
    about_txt: str = _section["about_txt"]
    toml_error_txt: str = _section["toml_error_txt"]
    toml_error_txt_title: str = _section["toml_error_txt_title"]
    toml_settings_window_title: str = _section["toml_settings_window_title"]
    toml_settings_window_save_button: str = _section["toml_settings_window_save_button"]
    toml_settings_window_close_button: str = _section["toml_settings_window_close_button"]
    #------ pop ups-------#
    learn_more_txt: str = _section["learn_more_txt"]


    class Widget1:
        """Project configuration widget strings and styles."""

        _section = _lang["MwConfig"]["Widget1"]

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
            border: 2px solid rgb(150, 60, 105);
            background-color: rgb(38, 38, 36);
        }

        QLineEdit:focus {
            border: 2px solid rgb(236, 100, 175);
            background-color: rgb(44, 44, 42);
        }
        """

        QlineTopTextQSS: str = (
            "font-size: 10px;"
            "margin-top: 0px;"
            "margin-bottom: 6px;"
        )

        github_box_top_label: str = _section["github_box_top_label"]
        github_box_placeholder_txt: str = _section[
            "github_box_placeholder_txt"
        ]

        path_box_top_label: str = _section["path_box_top_label"]
        path_box_placeholder_txt: str = _section[
            "path_box_placeholder_txt"
        ]

        sample_box_top_label: str = _section["sample_box_top_label"]
        ccboilerplates_box_placeholder_txt: str = _section[
            "ccboilerplates_box_placeholder_txt"
        ]
        cookiecutter_error_msg: str = _section["cookiecutter_error_msg"]

        browse_button_text: str = _section["browse_button_text"]
        select_editor_Combobox_top_label: str = _section[
            "select_editor_Combobox_top_label"
        ]

    class LangBtnWidget:
        """Programming-language selector strings and styles."""

        _section = _lang["MwConfig"]["LangBtnWidget"]

        lang_btns_qss: str = """
        QPushButton {
            background-color: qlineargradient(
                x1: 0,
                y1: 0,
                x2: 0,
                y2: 1,
                stop: 0 #66676b,
                stop: 0.45 #5f6063,
                stop: 1 #57585a
            );

            color: #f3eaf0;

            border-top: 1.25px solid #c28cb7;
            border-left: 1px solid #9e8299;
            border-right: 1px solid #9e8299;
            border-bottom: 2px solid #736473;

            border-radius: 7px;
            padding: 6px 18px;
        }

        QPushButton:hover {
            background-color: qlineargradient(
                x1: 0,
                y1: 0,
                x2: 0,
                y2: 1,
                stop: 0 #96788f,
                stop: 0.5 #896d84,
                stop: 1 #80637a
            );

            color: #ffd9e9;

            border-top: 1px solid #ffc5df;
            border-left: 1px solid #f0a2c5;
            border-right: 1px solid #d989b0;
            border-bottom: 2px solid #8d627d;
        }

        QPushButton:pressed {
            background-color: qlineargradient(
                x1: 0,
                y1: 0,
                x2: 0,
                y2: 1,
                stop: 0 #4d424b,
                stop: 1 #433841
            );

            color: #ffe3ef;

            border-top: 1px solid #6d5565;
            border-left: 1px solid #8e647d;
            border-right: 1px solid #8e647d;
            border-bottom: 1px solid #b97e9e;

            padding-top: 7px;
            padding-bottom: 5px;
        }

        QPushButton:checked {
            background-color: qlineargradient(
                x1: 0,
                y1: 0,
                x2: 0,
                y2: 1,
                stop: 0 #734860,
                stop: 0.5 #643a52,
                stop: 1 #593047
            );

            color: #ffe0ec;

            border-top: 1px solid #ffc8de;
            border-left: 1px solid #f1a5c8;
            border-right: 1px solid #d887ad;
            border-bottom: 2px solid #8d5c77;
        }

        QPushButton:checked:hover {
            background-color: qlineargradient(
                x1: 0,
                y1: 0,
                x2: 0,
                y2: 1,
                stop: 0 #81506a,
                stop: 0.5 #74455e,
                stop: 1 #673a53
            );

            color: #fff0f7;

            border-top: 1px solid #ffd9ea;
            border-left: 1px solid #ffb7d3;
            border-right: 1px solid #e092b7;
            border-bottom: 2px solid #99657f;
        }

        QPushButton:disabled {
            background-color: qlineargradient(
                x1: 0,
                y1: 0,
                x2: 0,
                y2: 1,
                stop: 0 #444548,
                stop: 1 #37383b
            );

            color: #7f7178;
            border: 1px solid #534a52;
        }

        QPushButton[selected="true"]:disabled {
            background-color: qlineargradient(
                x1: 0,
                y1: 0,
                x2: 0,
                y2: 1,
                stop: 0 #734860,
                stop: 0.5 #643a52,
                stop: 1 #593047
            );

            color: #ffe0ec;

            border-top: 1px solid #ffc8de;
            border-left: 1px solid #f1a5c8;
            border-right: 1px solid #d887ad;
            border-bottom: 2px solid #8d5c77;
        }
        """

        python_button_text: str = _section["python_button_text"]
        javascript_button_text: str = _section[
            "javascript_button_text"
        ]
        rust_button_text: str = _section["rust_button_text"]
        dotnet_button_text: str = _section["dotnet_button_text"]
        kotlin_button_text: str = _section["kotlin_button_text"]

        cpp_button_text: str = _section["cpp_button_text"]
        go_button_text: str = _section["go_button_text"]
        lua_button_text: str = _section["lua_button_text"]
        gdscript_button_text: str = _section["gdscript_button_text"]

    class Widget3:
        """Per-language workspace configuration strings and styles."""

        _section = _lang["MwConfig"]["Widget3"]
        _package_managers = _section["PackageManagers"]
        _frameworks = _section["Frameworks"]

        widget3_qss: str = """
        QStackedWidget {
            border-radius: 10px;
            background-color: transparent;
        }
        """

        # Python section

        py_qlabel_txt: str = _section["py_qlabel_txt"]

        py_interp_qcbox_top_txt: str = _section[
            "py_interp_qcbox_top_txt"
        ]

        py_unb_interp_qlinedit_top_txt: str = _section[
            "py_unb_interp_qlinedit_top_txt"
        ]

        py_unb_interp_qlinedit_inner_txt: str = _section[
            "py_unb_interp_qlinedit_inner_txt"
        ]

        py_frameworks_sep_label_txt: str = _section[
            "py_frameworks_sep_label_txt"
        ]

        py_qlabel_qss: str = """
        QLabel {
            font-family: "Times New Roman";
            letter-spacing: 1.5px;
            font-style: bold;
            font-weight: 200;
            font-size: 25pt;
            padding: 20px;
            qproperty-alignment: AlignCenter;
        }
        """

        py_radiobutton_qss: str = """
        QRadioButton {
            spacing: -1px;
            padding: 3px 14px;
            border: 2px solid rgba(0, 0, 0, 0.3);
            border-radius: 7px;

            background: qlineargradient(
                x1: 0,
                y1: 0,
                x2: 0,
                y2: 1,
                stop: 0 rgba(50, 50, 50, 180),
                stop: 1 rgba(30, 30, 30, 200)
            );

            color: rgba(235, 235, 235, 220);
            font-size: 12px;
            min-width: 90px;
        }

        QRadioButton:hover {
            border: 1px solid rgba(255, 255, 255, 0.18);

            background: qlineargradient(
                x1: 0,
                y1: 0,
                x2: 0,
                y2: 1,
                stop: 0 rgba(70, 70, 70, 200),
                stop: 1 rgba(40, 40, 40, 220)
            );
        }

        QRadioButton:disabled {
            border: 2px solid rgba(0, 0, 0, 0.18);

            background: qlineargradient(
                x1: 0,
                y1: 0,
                x2: 0,
                y2: 1,
                stop: 0 rgba(38, 38, 38, 120),
                stop: 1 rgba(24, 24, 24, 140)
            );

            color: rgba(180, 180, 180, 95);
        }

        QRadioButton:checked {
            border: 2px solid rgba(0, 0, 0, 0.3);
            color: rgba(230, 190, 255, 0.90);
            font-weight: 500;
        }
        """
        uv_error_msg: str = _package_managers["uv"]["error_msg"]
        conda_mamba_error_msg: str =_package_managers["conda"]["conda_mamba_error_msg"]





        QlineEditQSS: str = """
        QLineEdit {
            font-size: 12px;
            border: 2px solid rgb(65, 65, 63);
            border-radius: 5px;
            background-color: rgb(30, 30, 28);
            color: rgb(220, 220, 220);
        }

        QLineEdit:hover {
            border: 2px solid rgb(150, 60, 105);
            background-color: rgb(38, 38, 36);
        }

        QLineEdit:focus {
            border: 2px solid rgb(236, 100, 175);
            background-color: rgb(44, 44, 42);
        }
        """

        # Package managers

        py_uv_name: str = _package_managers["uv"]["name"]
        py_uv_tooltip: str = _package_managers["uv"]["tooltip"]

        py_pip_name: str = _package_managers["venv"]["name"]
        py_pip_tooltip: str = _package_managers["venv"]["tooltip"]

        py_poetry_name: str = _package_managers["poetry"]["name"]
        py_poetry_tooltip: str = _package_managers["poetry"]["tooltip"]

        py_hatch_name: str = _package_managers["hatch"]["name"]
        py_hatch_tooltip: str = _package_managers["hatch"]["tooltip"]

        py_conda_name: str = _package_managers["conda"]["name"]
        py_conda_tooltip: str = _package_managers["conda"]["tooltip"]

        py_pixi_name: str = _package_managers["pixi"]["name"]
        py_pixi_tooltip: str = _package_managers["pixi"]["tooltip"]

        py_mamba_name: str = _package_managers["mamba"]["name"]
        py_mamba_tooltip: str = _package_managers["mamba"]["tooltip"]

        py_pipenv_name: str = _package_managers["pipenv"]["name"]
        py_pipenv_tooltip: str = _package_managers["pipenv"]["tooltip"]

        py_virtualenv_name: str = _package_managers["virtualenv"]["name"]
        py_virtualenv_tooltip: str = _package_managers["virtualenv"]\
        ["tooltip"]

        py_pdm_name: str = _package_managers["pdm"]["name"]
        py_pdm_tooltip: str = _package_managers["pdm"]["tooltip"]

        # Frameworks and project templates

        py_django_name: str = _frameworks["django"]["name"]
        py_django_tooltip: str = _frameworks["django"]["tooltip"]

        py_flask_name: str = _frameworks["flask"]["name"]
        py_flask_tooltip: str = _frameworks["flask"]["tooltip"]

        py_fastapi_name: str = _frameworks["fastapi"]["name"]
        py_fastapi_tooltip: str = _frameworks["fastapi"]["tooltip"]

        py_streamlit_name: str = _frameworks["streamlit"]["name"]
        py_streamlit_tooltip: str = _frameworks["streamlit"]["tooltip"]

        py_pyscript_name: str = _frameworks["pyscript"]["name"]
        py_pyscript_tooltip: str = _frameworks["pyscript"]["tooltip"]

        py_pyside6_name: str = _frameworks["pyside6"]["name"]
        py_pyside6_tooltip: str = _frameworks["pyside6"]["tooltip"]

        py_jupyter_name: str = _frameworks["jupyter"]["name"]
        py_jupyter_tooltip: str = _frameworks["jupyter"]["tooltip"]