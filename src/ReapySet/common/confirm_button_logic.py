import os
import shlex
import shutil
import subprocess
from _collections_abc import Iterable
from pathlib import Path
from subprocess import CompletedProcess
from typing import Any

from PySide6.QtCore import QThread, Signal, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QMessageBox, QPushButton
from cookiecutter.exceptions import CookiecutterException
from cookiecutter.main import cookiecutter
from tomlkit import TOMLDocument

from ReapySet.common.init_frameworks import InitFrameworks
from ReapySet.common.logging import logger
from ReapySet.common.toml_handler import TomlHandler, CONFIG_PATH
from ReapySet.config import LogicVariables as LcFg
from ReapySet.config import MwConfig as Mwc

NTV_POSIX: bool = LcFg.ConstantUtils.IS_POSIX

#common/confirm_button.py


class ConfirmButton2ndThread(QThread):
    status_emitted = Signal(str, str)

    def __init__(
        self,
        p_data: dict[str, Any],
        p_proj_path: str,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.data = p_data
        self.proj_path = p_proj_path
        self.cc_project_already = False


    @staticmethod
    def _make_clear_term_env() -> dict[str, str]:



        clean_env = os.environ.copy()

        var_2b_removed: list[str] = [

            "VIRTUAL_ENV",

            "PYTHONHOME",

            "PYTHONPATH",

            "CONDA_PREFIX",

            "CONDA_DEFAULT_ENV",

            "UV_PROJECT_ENVIRONMENT",

            "UV_ACTIVE",

            "PIPENV_ACTIVE",

            "POETRY_ACTIVE",

        ]

        for var in var_2b_removed:
            clean_env.pop(var, None)

        return clean_env

    def _run_cmd(
            self,
            cmd: list[str],
            cwd: str | None = None,
    ) -> CompletedProcess[str]:
        try:
            return subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=cwd,
                env=self._make_clear_term_env(),
                check=False,
            )
        except OSError as exc:
            return CompletedProcess(
                args=cmd,
                returncode = -1,
                stdout="",
                stderr=str(exc),
            )
    def _run_cmd_list(
            self,
            cmd_list: list[list[str]],
            p_error_code: str,
            *,
            p_first_cmd_outside_project: bool = True,
    ) -> bool:
        """
        Execute commands sequentially and stop at the first failure.

        If p_first_cmd_outside_project is True, the first command runs
        without a project working directory because it is expected to
        create the project itself.
        
        basically       for each cmd:
                            run it
                            if fails:
                            return False

                        if alll successful:
                            return True
        """
        for index, cmd in enumerate(cmd_list):
            runs_outside_project = (
                    index == 0 and p_first_cmd_outside_project
            )

            cwd: str | None = None if runs_outside_project else self.proj_path

            result: CompletedProcess[str] = self._run_cmd(cmd, cwd=cwd)

            if result.returncode != 0:
                error_message = (
                        result.stderr.strip()
                        or result.stdout.strip()
                        or f"Command failed with exit code {result.returncode}"
                )

                self.status_emitted.emit(
                    p_error_code,
                    error_message,
                )
                return False

        return True
    def setup_python(self, p_py_config: dict[str, Any], p_proj_path: str, *,
                     p_project_already: bool = False) -> bool:
        current_proj_toml_path: Path = TomlHandler._dest_path()

            # post conditional mkdir
        pm: str = p_py_config["package_manager"]
        interp: str = p_py_config["interpreter_path"]
        disable_poetry_centralised_venvs: bool = bool(
            TomlHandler.toml_get(
                CONFIG_PATH,
                "python",
                "disable_poetry_centralised_venvs"
            )
        )
        if TomlHandler.toml_get(current_proj_toml_path, "languages", "selected_framework", "python") in {"PY:PYSCRIPT",}:
            return True # NO venv option

        interp_ver: str | None = TomlHandler.toml_get(
            current_proj_toml_path,
            "languages",
            "interpreter_version",
            "python"
        )

        unb_interp_ver: str | None = TomlHandler.toml_get(
            current_proj_toml_path,
            "languages",
            "unb_interpreter_version",
            "python"
        )  # unbound interpreter

        # pm_python_ver: used by conda / mamba / pixi, which can download the interpreter themselves. they  need a string value son it have to be extracted first
        # eitehr user gets fooled, by passint them a version extracted from the path so already installed, even if the versuin needs o be downlaoded
        #   - passes a version string like "3.11" if available, otherwise None (they'll use their default).
        pm_python_ver: str | None = unb_interp_ver or interp_ver
        # uv on the otehr hanbd acceps a path or a specifice version (unboud indeed)
        # uvs_python: used by uv, which accepts both a version string AND an absolute path.
        #   - always has a value: prefers unbound version > bound version > interpreter path.
        #   - the interpreter path is a valid fallback because uv knows how to handle it.
        uvs_python: str = unb_interp_ver or interp_ver or interp

        Path(p_proj_path).mkdir(parents=True, exist_ok=True)
        match pm:
            case "PY:UV":
                uv_bin: str = LcFg.PythonVars.py_uv_path

                uv_cmds: list[list[str]] = (
                    [
                        LcFg.PythonVars.py_uv_icmd
                        + ["--python", uvs_python, p_proj_path]
                    ]
                    if not p_project_already
                    else [
                        [uv_bin, "sync"],
                    ]
                )

                return self._run_cmd_list(
                    uv_cmds,
                    p_error_code="uverror",
                    p_first_cmd_outside_project=not p_project_already
                )  # uv init and uv sync to make the venv if



            case "PY:POETRY":
                poetry_bin: str = LcFg.PythonVars.py_poetry_path

                poetry_cmds: list[list[str]] = []
                if not p_project_already:
                    poetry_cmds.append(
                        LcFg.PythonVars.py_poetry_icmd + [p_proj_path]
                    )

                if disable_poetry_centralised_venvs:
                    poetry_cmds.append(
                        [
                            poetry_bin,
                            "config",
                            "virtualenvs.in-project",
                            "true",
                            "--local",
                        ]
                    )

                poetry_cmds.append(
                    [poetry_bin, "env", "use", interp]
                )

                if p_project_already:
                    poetry_cmds.append(
                        [poetry_bin, "install"]
                    )

                return self._run_cmd_list(
                    poetry_cmds,
                    p_error_code="poetryerror",
                    p_first_cmd_outside_project=not p_project_already,
                )



            case "PY:PIXI":
                pixi_bin: str = LcFg.PythonVars.py_pixi_path

                if p_project_already:
                    pixi_cmds: list[list[str]] = [
                        [pixi_bin, "install"],
                    ]
                else:
                    pixi_cmds = [
                        LcFg.PythonVars.py_pixi_icmd + [p_proj_path],
                    ]

                    if pm_python_ver:
                        pixi_cmds.append(
                            [pixi_bin, "add", f"python={pm_python_ver}"]
                        )
                return self._run_cmd_list(
                    pixi_cmds,
                    p_error_code="pixierror",
                    p_first_cmd_outside_project=not p_project_already,
                )



            case "PY:CONDA":


                return self._run_cmd_list(
                    [
                        LcFg.PythonVars.py_conda_icmd
                        + [str(Path(p_proj_path) / ".conda")]
                        + ([f"python={pm_python_ver}"] if pm_python_ver else [])
                    ],
                    p_error_code="condaerror",
                    p_first_cmd_outside_project=False
                )



            case "PY:MAMBA":

                return self._run_cmd_list(
                    [
                        LcFg.PythonVars.py_mamba_icmd
                        + [str(Path(p_proj_path) / ".mamba")]
                        + ([f"python={pm_python_ver}"] if pm_python_ver else [])
                    ],
                    p_error_code="mambaerror",
                    p_first_cmd_outside_project=False

                )

            case "PY:HATCH":
                hatch_bin = LcFg.PythonVars.py_hatch_path

                hatch_cmds: list[list[str]] = (
                    [[hatch_bin, "new", "--init"]]
                    if not p_project_already
                    else [[hatch_bin, "env", "create"]]
                )

                return self._run_cmd_list(
                    hatch_cmds,
                    p_error_code="hatcherror",
                    p_first_cmd_outside_project=False,
                )

            case "PY:VENV":
                return self._run_cmd_list(
                    [[interp, "-m", "venv", ".venv"]],
                    p_error_code="venverror",
                    p_first_cmd_outside_project=False
                )

            case "PY:PDM":
                pdm_bin = LcFg.PythonVars.py_pdm_path

                pdm_cmds: list[list[str]] = (
                    [
                        LcFg.PythonVars.py_pdm_icmd
                        + ["--python", interp],
                    ]
                    if not p_project_already
                    else [
                        [pdm_bin, "install"],
                    ]
                )

                return self._run_cmd_list(
                    pdm_cmds,
                    "pdmerror",
                    p_first_cmd_outside_project=False,
                )

            case "PY:PIPENV":
                return self._run_cmd_list(
                    [LcFg.PythonVars.py_pipenv_icmd + ["--python", interp]],
                    p_error_code="pipenverror",
                    p_first_cmd_outside_project=False
                )

            case "PY:VIRTUALENV":
                return self._run_cmd_list(
                    [LcFg.PythonVars.py_virtualenv_icmd + [interp, ".venv"]],
                    p_error_code="virtualenverror",
                    p_first_cmd_outside_project=False
                )

        return True

    from collections.abc import Iterable
    from pathlib import Path

    def package_install(
            self,
            p_packages: str | Iterable[str],
            p_proj_path: str | Path,
            *,
            p_dev: bool = False,
    ) -> bool:
        """
        Installs one or more packages in an existing Python project.

        Args:
           :param p_packages:
                A package name or an iterable of package names.

                Examples:
                    "django"
                    ("django", "requests")
                    ["pytest>=8", "ruff"]

            :param p_proj_path:
                Path of the project in which the command is executed.

            :param p_dev:
                If True, records the packages as development dependencies
                when supported by the selected package manager.

        Returns:
            True if the installation succeeds, otherwise False.

        Raises:
            TypeError:
                If a package name is not a string.

            ValueError:
                If no package manager is configured, the package manager is
                unsupported, or development dependencies are not supported.
        """
        errcode: str = "packageinstallerror"
        def _venv_python_path(_p_proj_path: str | Path) -> Path:
            venv_path: Path = Path(_p_proj_path) / ".venv"

            if os.name == "nt":
                return venv_path / "Scripts" / "python.exe"

            return venv_path / "bin" / "python"

        project_path = Path(p_proj_path)
        current_proj_toml_path: Path = TomlHandler._dest_path()

        pm: str | None = TomlHandler.toml_get(
            current_proj_toml_path,
            "languages",
            "package_manager",
            "python",
        )

        if pm is None:
            raise ValueError(
                "No Python package manager is configured for the project."
            )

        if isinstance(p_packages, str):
            raw_packages: Iterable[str] = (p_packages,)
        else:
            raw_packages = p_packages

        normalised_packages: list[str] = []

        for package in raw_packages:
            if not isinstance(package, str):
                raise TypeError(
                    "Every package name must be a string, "
                    f"not {type(package).__name__}."
                )

            package = package.strip()

            if package:
                normalised_packages.append(package)

        # Removes duplicates while preserving insertion order.
        packages: tuple[str, ...] = tuple(
            dict.fromkeys(normalised_packages)
        )

        if not packages:
            return True

        command: list[str]

        match pm:
            case "PY:UV":
                command = [
                    LcFg.PythonVars.py_uv_path,
                    "add",
                ]

                if p_dev:
                    command.append("--dev")

                command.extend(packages) # extend is like append with *

            case "PY:POETRY":
                command = [
                    LcFg.PythonVars.py_poetry_path,
                    "add",
                ]

                if p_dev:
                    command.extend(["--group", "dev"])

                command.extend(packages)

            case "PY:PDM":
                command = [
                    LcFg.PythonVars.py_pdm_path,
                    "add",
                ]

                if p_dev:
                    command.append("--dev")

                command.extend(packages)

            case "PY:PIPENV":
                command = [
                    LcFg.PythonVars.py_pipenv_path,
                    "install",
                ]

                if p_dev:
                    command.append("--dev")

                command.extend(packages)

            case "PY:PIXI":
                if p_dev:
                    raise ValueError(
                        "Pixi has no implicit development dependency group. "
                        "A dedicated feature and environment must be configured."
                    )

                command = [
                    LcFg.PythonVars.py_pixi_path,
                    "add",
                    "--pypi",
                    *packages,
                ]

            case "PY:CONDA":
                if p_dev:
                    raise ValueError(
                        "Conda does not distinguish normal dependencies "
                        "from development dependencies."
                    )

                command = [
                    LcFg.PythonVars.py_conda_path,
                    "install",
                    "--yes",
                    "--prefix",
                    str(project_path / ".conda"),
                    *packages,
                ]

            case "PY:MAMBA":
                if p_dev:
                    raise ValueError(
                        "Mamba does not distinguish normal dependencies "
                        "from development dependencies."
                    )

                command = [
                    LcFg.PythonVars.py_mamba_path,
                    "install",
                    "--yes",
                    "--prefix",
                    str(project_path / ".mamba"),
                    *packages,
                ]

            case "PY:VENV" | "PY:VIRTUALENV":
                venv_python: Path = _venv_python_path(project_path)

                if not venv_python.is_file():
                    raise FileNotFoundError(
                        f"Virtual environment not found: {venv_python}"
                    )

                command = [
                    str(venv_python),
                    "-m",
                    "pip",
                    "install",
                    *packages,
                ]

            case "PY:HATCH":
                errcode: str = "hatcherr_pkg"
                command = []
                """raise ValueError(
                    "Hatch does not provide a general command equivalent "
                    "to 'add dependency'. Dependencies must be declared "
                    "in pyproject.toml."
                )"""



            case _:
                raise ValueError(
                    f"Unsupported Python package manager: {pm!r}"
                )

        return self._run_cmd_list(
            [command],
            p_error_code=errcode,
            p_first_cmd_outside_project=False,
        )


    def setup_cookiecutter(self) -> str | None:
        """
        Generates a project from a Cookiecutter template.
        Returns the generated project path, or None if generation fails.
        """
        cookiecutter_config = self.data.get("cookiecutter", {})
        template_path = Path(cookiecutter_config.get("template_path", "")).expanduser()
        output_dir_path = Path(self.proj_path).expanduser()

        # --- CONTROL 1: Template not found ---
        if not template_path.is_dir():
            self.status_emitted.emit("cc_template_missing", "")
            return None

        # --- if JSON missing ---
        if not (template_path / 'cookiecutter.json').is_file():
            self.status_emitted.emit("cc_json_missing", "")
            return None

        # mkdir
        output_dir_path.mkdir(parents=True, exist_ok=True)

        # --- EXEC COOKIECUTTER ---
        try:
            raw_proj_path = cookiecutter(
                template=str(template_path),
                output_dir=str(output_dir_path),
                no_input=True,
                overwrite_if_exists=False,
            )
        except (CookiecutterException, OSError) as e:
            # signal
            self.status_emitted.emit("cc_generation_failed", str(e))
            return None

        return str(raw_proj_path)
    @staticmethod
    def setup_javascript() -> bool:
        # TODO: implement
        return True
    @staticmethod
    def setup_dotnet() -> bool:
        # TODO: implement
        return True

    def _setup_selected_language(self) -> bool:
        languages = self.data["languages"]

        if languages["python"]["enabled"]:
            return self.setup_python(
                languages["python"],
                self.proj_path,
                p_project_already=self.cc_project_already,
            )

        if languages["javascript"]["enabled"]:
            return self.setup_javascript()

        if languages["dotnet"]["enabled"]:
            return self.setup_dotnet()

        self.status_emitted.emit(
            "language_missing",
            "No programming language is enabled.",
        )
        return False

    def _setup_cc_project(self) -> bool:
        cookiecutter_config = self.data.get("cookiecutter", {})
        template_path = cookiecutter_config.get("template_path")

        if not template_path:
            return True

        generated_path = self.setup_cookiecutter()

        if generated_path is None:
            return False

        self.proj_path = generated_path
        self.cc_project_already = True

        return True

    def _setup_selected_framework(self) -> bool:
        py_config = self.data["languages"]["python"]  # Python frameworks

        if not py_config["enabled"]:
            return True

        selected_framework = py_config.get("selected_framework") # python fmks

        if not selected_framework:
            return True

        install_packages = (
                TomlHandler.toml_get(
                    CONFIG_PATH,
                    "advanced",
                    "install_packages_on_project_creation",
                )
                is not False
        )

        try:
            match selected_framework:
                case "PY:JUPYTER":
                    python_version = (
                            py_config.get("unb_interpreter_version")
                            or py_config.get("interpreter_version")
                    )

                    InitFrameworks.init_jupyter_notebook(
                        self.proj_path,
                        python_version,
                    )

                    if install_packages:
                        if not self.package_install(
                                ("jupyterlab",),
                                self.proj_path,
                        ):
                            return False

                case "PY:PYSIDE6":
                    InitFrameworks.init_pyside6(self.proj_path)

                    if install_packages:
                        if not self.package_install(
                                ("pyside6",),
                                self.proj_path,
                        ):
                            return False


                case "PY:PYSCRIPT":
                    InitFrameworks.init_pyscript(self.proj_path)

                    # PyScript does not use the local Python environment.

                case _:
                    return True

        except (
                OSError,
                subprocess.SubprocessError,
                ValueError,
        ) as exc:
            self.status_emitted.emit(
                "frameworkerror",
                str(exc),
            )
            return False

        return True
    def run(self) -> None:
        if not self._setup_cc_project():
            return

        if not self._setup_selected_language():
            return

        if not self._setup_selected_framework():
            return

        self.status_emitted.emit("success", "")
class ConfirmButtonLogic:
    def __init__(self) -> None:
        self.worker: ConfirmButton2ndThread | None = None
        self.editor: str = "None"
    #todo should execute the env creation,
    # reads from the toml_cc the temp configs
    # and from config.py (editable in future via config.toml)
    # setup_python, setup_dotnet, setup_rust
    # and a list of commands that will be called via subprpcess.Popen(py_uv/py_poetry/py_venv_init_cmd:set[set[str]]
    # rs_cargo dotnet else with a match case)
    @staticmethod
    def _make_clear_term_env1() -> dict[str, str]:

        import os

        clean_env = os.environ.copy()

        var_2b_removed = [

            "VIRTUAL_ENV",

            "PYTHONHOME",

            "PYTHONPATH",

            "CONDA_PREFIX",

            "CONDA_DEFAULT_ENV",

            "UV_PROJECT_ENVIRONMENT",

            "UV_ACTIVE",

            "PIPENV_ACTIVE",

            "POETRY_ACTIVE",

        ]

        for var in var_2b_removed:
            clean_env.pop(var, None)

        return clean_env

    @staticmethod
    def _warn_missing_popup(p_tool_name: str,
                            p_popup_icon: QMessageBox.Icon = QMessageBox.Icon.Critical,
                            p_learn_more_url: str = "about:blank",
                            p_window_title: str = "Tool Not Found",
                            p_download_button: dict[str, str] | None = None,
                            p_download_button_txt: str = "Download",
                            p_msg_txt: str = "not found or not installed.",
                            p_info_txt: str = "Make sure it is installed and the path is correct in config.toml"
                            ) -> None:
        """

        :rtype: None
        """
        logger.warning(f"{p_window_title}: {p_tool_name} {p_msg_txt} | {p_info_txt}")
        msg = QMessageBox()
        msg.setIcon(p_popup_icon)
        msg.setWindowTitle(p_window_title)
        msg.setText(f" {p_tool_name} {p_msg_txt}")
        msg.setInformativeText(p_info_txt)

        msg.addButton("OK", QMessageBox.ButtonRole.AcceptRole)
        if p_download_button:
            msg.addButton(
                p_download_button_txt,
                QMessageBox.ButtonRole.ActionRole)


        if p_learn_more_url:
            learn_more: QPushButton = msg.addButton(f"{Mwc.learn_more_txt}", QMessageBox.ButtonRole.HelpRole)
            msg.exec()
            if msg.clickedButton() == learn_more:
                QDesktopServices.openUrl(QUrl(p_learn_more_url))
        else:
            msg.exec()


    def _check_editor(self, p_editor: str) -> bool:
        cmd = LcFg.EditorCmd.get_cmd(p_editor)

        if cmd == "NOEDITOR":
            return True
        elif not cmd:
            self._warn_missing_popup(p_editor)
            return False

        executable = shlex.split(cmd, posix=NTV_POSIX)[0]

        resolved = (
                shutil.which(executable) # noqa it'll never run on 3.12
                or (executable if Path(executable).is_file() else None)
        )

        if not resolved:
            self._warn_missing_popup(p_editor)
            return False

        return True

    def _openin_editor(
            self,
            p_editor: str,
            p_proj_path: str,
    ) -> None:
        cmd = LcFg.EditorCmd.get_cmd(p_editor)

        if not cmd or cmd.upper() == "NOEDITOR":
            return

        editor_openin_cmd = cmd.format(path=p_proj_path)

        try:
            subprocess.Popen(
                shlex.split(
                    editor_openin_cmd,
                    posix=NTV_POSIX,
                ),
                env=self._make_clear_term_env1()
            )
        except OSError as exc:
            self._warn_missing_popup(
                p_editor,
                p_info_txt=str(exc),
            )
    def handle_2thread_outcomes(self, outcome: str, error_info: str):
        match outcome:
            # --- CCOOKIECUTTER OUTCOMES---
            case "cc_template_missing":
                self._warn_missing_popup(
                    "Cookiecutter",
                    p_msg_txt="template was not found",
                    p_info_txt=f"{Mwc.Widget1.cookiecutter_error_msg}",
                    p_learn_more_url="https://cookiecutter.readthedocs.io/en/stable/README.html"
                )
                return
            case "cc_json_missing":
                self._warn_missing_popup(
                    "Cookiecutter.json",
                    p_msg_txt="Template is invalid :(",
                    p_info_txt="It looks like the selected directory does not contain any cookiecutter.json.",
                    p_learn_more_url="https://cookiecutter.readthedocs.io/en/stable/tutorials/tutorial2.html#step-2-create-cookiecutter-json"
                )
                return
            case "cc_generation_failed":
                self._warn_missing_popup(
                    "cookiecutter",
                    p_msg_txt="Project generation failed :(",
                    p_info_txt=f"{Mwc.Widget1.cookiecutter_error_msg}: {error_info}",
                    p_learn_more_url="https://cookiecutter.readthedocs.io/en/stable/troubleshooting.html#i-created-a-cookiecutter-but-it-doesn-t-work-and-i-can-t-figure-out-why"
                )
                return

            # --- PYTHON OUTCOMES ---
            case "uverror":
                self._warn_missing_popup(
                    "uv: project initialisation or sync failed!",
                    p_learn_more_url="https://docs.astral.sh/uv/guides/projects/",
                    p_msg_txt="",
                    p_info_txt=(
                        f"{Mwc.Widget3.uv_error_msg}: {error_info}"
                    )
                )
                return

            case "poetryerror":
                self._warn_missing_popup(
                    "poetry: project initialisation failed!",
                    p_learn_more_url="https://python-poetry.org/docs/configuration/",
                    p_msg_txt="",
                    p_info_txt=(
                        ":( \nNote: make sure Poetry is installed, the Python interpreter is valid "
                        f"and the project path is usable.\n\nDetails: {error_info}"
                    )
                )
                return

            case "pixierror":
                self._warn_missing_popup(
                    "pixi: project initialisation failed!",
                    p_learn_more_url="https://pixi.sh/latest/getting_started/",
                    p_msg_txt="",
                    p_info_txt=(
                        ":( \nNote: make sure Pixi is installed and the Python version is valid "
                        f"and the project path is usable.\n\nDetails: {error_info}"
                    )
                )
                return

            case "condaerror":
                self._warn_missing_popup(
                    "conda: environment creation failed!",
                    p_learn_more_url="https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html",
                    p_msg_txt="",
                    p_info_txt=(
                        ":( \nNote: make sure conda is installed and you've entered "
                        f"a valid Python interpreter version.\n\nDetails: {error_info}"
                    )
                )
                return

            case "mambaerror":
                self._warn_missing_popup(
                    "mamba: environment creation failed!",
                    p_learn_more_url="https://mamba.readthedocs.io/en/latest/user_guide/mamba.html",
                    p_msg_txt="",
                    p_info_txt=(
                        ":( \nNote: make sure mamba is installed and you've entered "
                        f"a valid Python interpreter version.\n\nDetails: {error_info}"
                    )
                )
                return

            case "hatcherror":
                self._warn_missing_popup(
                    "Hatch",
                    p_learn_more_url="https://hatch.pypa.io/latest/environment/",
                )
                return
            case "hatcherr_pkg":
                self._warn_missing_popup(
                    p_popup_icon=QMessageBox.Icon.Information,
                    p_window_title="Hatch information",
                    p_tool_name="Hatch",
                    p_msg_txt="Hatch does not provide a general command equivalent to 'pip install dependency'.\n Dependencies must be declared only in pyproject.toml manully",
                    p_learn_more_url="https://github.com/pypa/hatch/issues/1599"#https://hatch.pypa.io/latest/cli/reference/#hatch-dep
                )

            case "venverror":
                self._warn_missing_popup(
                    "venv",
                    p_learn_more_url="https://docs.python.org/3/library/venv.html"
                )
                return

            case "pdmerror":
                self._warn_missing_popup(
                    "pdm",
                    p_learn_more_url="https://pdm-project.org/en/latest/usage/project/",
                )
                return

            case "pipenverror":
                self._warn_missing_popup(
                    "pipenv",
                    p_learn_more_url="https://pipenv.pypa.io/en/latest/basics/",
                )
                return

            case "virtualenverror":
                self._warn_missing_popup(
                    "virtualenv",
                    p_learn_more_url="https://virtualenv.pypa.io/en/latest/user_guide.html",
                )
                return

            case "success":
                if self.worker is not None:
                    final_path = self.worker.proj_path
                    if self.editor != "None":
                        self._openin_editor(self.editor, final_path)
                        logger.success(f"Project created! Opened in editor: {self.editor} | Path: {final_path}")

    def on_confirm_clicked(self) -> None:
        if self.worker is not None and self.worker.isRunning():
            return

        data: TOMLDocument = TomlHandler._toml_read()

        project_path: str = data["global"]["project_path"]
        editor: str = data["global"]["fav_editor"]

        if not self._check_editor(editor):
            return

        self.editor: str = editor

        worker = ConfirmButton2ndThread(
            p_data=data,
            p_proj_path=project_path,
        )

        worker.status_emitted.connect(
            self.handle_2thread_outcomes
        )

        self.worker = worker
        worker.start()
