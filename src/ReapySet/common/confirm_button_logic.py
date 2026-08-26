import os
import shlex
import shutil
import subprocess
from _collections_abc import Iterable
from pathlib import Path
from subprocess import CompletedProcess
from typing import Any

from PySide6.QtCore import QThread, Signal, QUrl, QRegularExpression
from PySide6.QtGui import QDesktopServices, QRegularExpressionValidator
from PySide6.QtWidgets import QMessageBox, QPushButton, QLineEdit, QGridLayout
from cookiecutter.exceptions import CookiecutterException
from cookiecutter.main import cookiecutter
from tomlkit import TOMLDocument

from ReapySet.common.MwFunctions import MwFuncs as Mwf
from ReapySet.common.init_frameworks import InitFrameworks
from ReapySet.common.logging import logger
from ReapySet.common.toml_handler import TomlHandler, CONFIG_PATH
from ReapySet.config import LogicVariables as LcFg
from ReapySet.config import MwConfig as Mwc
from ReapySet.common.download_pkg import DownloadPkg

NTV_POSIX: bool = LcFg.ConstantUtils.IS_POSIX

#common/confirm_button.py


class ConfirmButton2ndThread(QThread):
    status_emitted = Signal(str, str)

    def __init__(
        self,
        p_data: dict[str, Any], # toml
        p_proj_path: str , # | None
        parent=None,
        p_package_to_install: dict[str, str] | None = None,
    ) -> None:
        super().__init__(parent)

        self.data = p_data
        self.proj_path = p_proj_path
        self.cc_project_already = False
        self.package_to_install = p_package_to_install


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
        if TomlHandler.toml_get(current_proj_toml_path, "languages", "selected_framework", "common") in {"PY:PYSCRIPT",}:
            return True # NO venv option
        """project_path = Path(p_proj_path)

        source_path = (
            project_path / "src"
            if TomlHandler.toml_get(
                current_proj_toml_path,
                "global",
                "add_src_to_path",
            )# == true
            else project_path
        )"""

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

    #from collections.abc import Iterable

    def python_package_install(
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

    def run_project_command(
            self,
            p_command: str | Iterable[str],
            p_proj_path: str | Path,
            *,
            p_error_code: str = "projectcommanderror",
    ) -> bool:
        """
        Runs a command inside the Python environment of an existing project.

        The correct execution method is selected automatically according to
        the package manager configured for the project.

        Examples:
            ["python", "-m", "django", "startproject", "myapp", "."]
            ["python", "manage.py", "migrate"]
            ["pytest"]
            ("python", "-m", "ruff", "check", ".")

        Args:
            :param p_command:
                Command to execute.

                It may be passed as a single string or as an iterable of
                command arguments.

                Prefer an iterable when arguments are already separated.

            :param p_proj_path:
                Path of the project in which the command must be executed.

            :param p_error_code:
                Error code emitted if command execution fails.

        Returns:
            True if the command succeeds, otherwise False.

        Raises:
            TypeError:
                If command arguments are not strings.

            ValueError:
                If the command is empty, no package manager is configured,
                or the configured package manager is unsupported.

            FileNotFoundError:
                If a local virtual environment executable cannot be found.
        """

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

        # Normalise the command.
        if isinstance(p_command, str):
            raw_command: Iterable[str] = (p_command,)
        else:
            raw_command = p_command

        normalised_command: list[str] = []

        for argument in raw_command:
            if not isinstance(argument, str):
                raise TypeError(
                    "Every command argument must be a string, "
                    f"not {type(argument).__name__}."
                )

            if argument:
                normalised_command.append(argument)

        if not normalised_command:
            raise ValueError(
                "The project command cannot be empty."
            )

        command: list[str]

        match pm:

            case "PY:UV":
                command = [
                    LcFg.PythonVars.py_uv_path,
                    "run",
                    *normalised_command,
                ]

            case "PY:POETRY":
                command = [
                    LcFg.PythonVars.py_poetry_path,
                    "run",
                    *normalised_command,
                ]

            case "PY:PDM":
                command = [
                    LcFg.PythonVars.py_pdm_path,
                    "run",
                    *normalised_command,
                ]

            case "PY:PIPENV":
                command = [
                    LcFg.PythonVars.py_pipenv_path,
                    "run",
                    *normalised_command,
                ]

            case "PY:PIXI":
                command = [
                    LcFg.PythonVars.py_pixi_path,
                    "run",
                    "--manifest-path",
                    str(project_path),
                    "--executable",
                    *normalised_command,
                ]

            case "PY:CONDA":
                conda_env_path = project_path / ".conda"

                if not conda_env_path.is_dir():
                    raise FileNotFoundError(
                        f"Conda environment not found: {conda_env_path}"
                    )

                command = [
                    LcFg.PythonVars.py_conda_path,
                    "run",
                    "--prefix",
                    str(conda_env_path),
                    "--",
                    *normalised_command,
                ]

            case "PY:MAMBA":
                mamba_env_path = project_path / ".mamba"

                if not mamba_env_path.is_dir():
                    raise FileNotFoundError(
                        f"Mamba environment not found: {mamba_env_path}"
                    )

                command = [
                    LcFg.PythonVars.py_mamba_path,
                    "run",
                    "--prefix",
                    str(mamba_env_path),
                    *normalised_command,
                ]

            case "PY:VENV" | "PY:VIRTUALENV":
                venv_path = project_path / ".venv"

                if os.name == "nt":
                    bin_path = venv_path / "Scripts"
                    python_path = bin_path / "python.exe"
                else:
                    bin_path = venv_path / "bin"
                    python_path = bin_path / "python"

                if not python_path.is_file():
                    raise FileNotFoundError(
                        f"Virtual environment Python not found: {python_path}"
                    )

                executable = normalised_command[0]

                # "python ..." must explicitly use the project's interpreter.
                if executable in {
                    "python",
                    "python3",
                    "python.exe",
                }:
                    command = [
                        str(python_path),
                        *normalised_command[1:],
                    ]

                else:
                    # Try to run an executable installed in the venv,
                    # e.g. pytest, django-admin, ruff, etc.
                    if os.name == "nt":
                        executable_path = bin_path / (
                            executable
                            if executable.lower().endswith(".exe")
                            else f"{executable}.exe"
                        )
                    else:
                        executable_path = bin_path / executable

                    if executable_path.is_file():
                        command = [
                            str(executable_path),
                            *normalised_command[1:],
                        ]

                    else:
                        raise FileNotFoundError(
                            f"Executable {executable!r} was not found "
                            f"in the virtual environment: {bin_path}"
                        )

            case "PY:HATCH":
                command = [
                    LcFg.PythonVars.py_hatch_path,
                    "run",
                    *normalised_command,
                ]

            case _:
                raise ValueError(
                    f"Unsupported Python package manager: {pm!r}"
                )

        return self._run_cmd_list(
            [command],
            p_error_code=p_error_code,
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
        py_config = self.data["languages"]["python"]

        if not py_config["enabled"]:
            return True

        selected_framework = self.data["languages"]["common"].get(
            "selected_framework" # common fmks
        )

        if not selected_framework:
            return True

        install_packages_on_project_creation: bool = (
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

                    if install_packages_on_project_creation:
                        if not self.python_package_install(("jupyterlab",), self.proj_path):
                            return False

                case "PY:PYSIDE6":
                    InitFrameworks.init_pyside6(self.proj_path)

                    if install_packages_on_project_creation:
                        if not self.python_package_install(("pyside6",), self.proj_path):
                            return False



                case "PY:MARIMO":
                    InitFrameworks.init_marimo(self.proj_path)

                    if install_packages_on_project_creation:
                        if not self.python_package_install(("marimo",), self.proj_path):
                            return False

                case "PY:DJANGO":
                    """
                    Django project initialisation flow.

                    Django requires some additional handling compared with the other supported frameworks
                    because the project name is provided by the user at confirmation time
                    and Django commands MUST be executed inside the environment managed by
                    the currently selected Python package manager.

                    The flow is as follows:

                    1. When the user confirms project creation and Django happens to be the selected
                       framework, an option popup is displayed containing a QLineEdit.
                       (NOTE: it cannot use windows/macos/wayland... native style
                        as message boxes natively dont support qilinedits
                         so if the window has little to no animation and acts funny that's why)

                    2. The value entered in the QLineEdit is validated and, when the user presses
                       OK, is temporarily stored in the current project TOML as
                       `languages.common.project_app_name`.

                    3. The normal project creation worker starts and creates the Python
                       environment using the selected package manager.

                    4. If automatic framework package installation is enabled, Django is installed
                       through `package_install()`. This keeps dependency installation independent
                       of the specific package manager.

                    5. The temporary `project_app_name` value is read from the project TOML and
                       passed to `InitFrameworks.init_django()`.

                    6. `InitFrameworks.init_django()` defines the Django-specific initialisation
                       steps, such as removing the generic `main.py`, running `django startproject`,
                       and applying the initial database migrations.

                    7. Django commands are not executed directly by `init_django()`. They are
                       delegated to `run_project_command()`, which translates a generic command
                       into the correct execution method for the selected package manager
                       (for example uv, Poetry, PDM, Pipenv, Pixi, Conda, Mamba, Hatch, venv or
                       virtualenv).

                    8. Once the Django setup attempt has completed, the temporary
                       `languages.common.project_app_name` value is always cleared from
                       the project TOML, regardless of whether the initialisation succeeds
                       or fails.

                    This separation keeps each component responsible for a single concern:
                    the popup collects temporary user input, `package_install()` installs
                    dependencies, `run_project_command()` handles package-manager-specific command
                    execution, and `InitFrameworks.init_django()` contains only Django-specific
                    initialisation logic.
                    """
                    try:

                        if install_packages_on_project_creation:
                            if not self.python_package_install(("django",), self.proj_path):
                                return False

                        app_name: str | None = TomlHandler.toml_get(

                            TomlHandler._dest_path(),

                            "languages",

                            "project_app_name",

                            "common",

                        )

                        if not InitFrameworks.init_django(
                                self.proj_path,

                                app_name if app_name else "NAME_NOT_PROVIDED",

                                self.run_project_command,
                        ):
                            return False

                    finally: # whatever is the outcome clear it

                        TomlHandler.toml_edit(

                            "languages",

                            "project_app_name",

                            "",

                            "common",

                        )


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

    def run(self) -> None:  # params are passed from the init here because qt handles them this way
        if self.package_to_install: # oif the pkg is specified run this
            install_outcome = DownloadPkg.install_package(
                self.package_to_install
            )

            if install_outcome:
                self.status_emitted.emit(
                    "package_install_success",
                    "",
                )
            else:
                self.status_emitted.emit(
                    "package_install_error",
                    "",
                )

            return

        if not self._setup_cc_project():
            return

        if not self._setup_selected_language():
            return

        if not self._setup_selected_framework():
            return

        if (
                self.data["languages"]["common"]["unit_test_lib"] == "PY:PYTEST"
                and TomlHandler.toml_get(
            CONFIG_PATH,
            "advanced",
            "install_packages_on_project_creation",
        ) is not False
        ):
            InitFrameworks.init_pytest(self.proj_path)

            try:
                if not self.python_package_install(
                        "pytest",
                        self.proj_path,
                        p_dev=True,
                ):
                    return

            except ValueError:
                if not self.python_package_install(
                        "pytest",
                        self.proj_path,
                        p_dev=False,
                ):
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
    def _option_popup(p_tool_name: str,
                            p_popup_icon: QMessageBox.Icon = QMessageBox.Icon.Information,
                            p_learn_more_url: str = "about:blank",
                            p_window_title: str = "Tool Not Found",
                            p_qlidedit_placeholder_txt: str = "app name is..?",
                            p_qlinedit_top_txt: str = "top text",
                            p_msg_txt: str = "insert value",
                            p_info_txt: str = "Make sure it is installed and the path is correct in config.toml"
                            ) -> None:
        """

        :rtype: None
        """
        logger.info(f"{p_window_title}: {p_tool_name} {p_msg_txt} | {p_info_txt}")
        msg = QMessageBox()
        msg.setIcon(p_popup_icon)
        msg.setWindowTitle(p_window_title)
        msg.setText(f" {p_tool_name} {p_msg_txt}")
        msg.setInformativeText(p_info_txt)
        msg.setOption(

            QMessageBox.Option.DontUseNativeDialog,

            True # i doesnt support the qlinedit otherwise

        )


        qlinedit = QLineEdit(placeholderText=p_qlidedit_placeholder_txt)
        labeled_widget = Mwf.labeled_field(widget=qlinedit, label_txt=p_qlinedit_top_txt)

        regex_: QRegularExpressionValidator =\
            QRegularExpressionValidator(
            QRegularExpression(r"^[a-z_][a-z0-9_]*$"  )
        )
        qlinedit.setValidator(regex_)

        layout = msg.layout()
        if isinstance(layout, QGridLayout):

            layout.addWidget(
                labeled_widget if labeled_widget else qlinedit,
                layout.rowCount(),  # new row
                0,  # col 0
                1,  # row 1
                layout.columnCount()  # all thr colums
            )

        ok_button = msg.addButton("OK", QMessageBox.ButtonRole.AcceptRole)

        learn_more: QPushButton | None = None


        if p_learn_more_url:
            learn_more: QPushButton = msg.addButton(f"{Mwc.learn_more_txt}", QMessageBox.ButtonRole.HelpRole)


        msg.exec()

        if learn_more is not None and msg.clickedButton() == learn_more:
            QDesktopServices.openUrl(QUrl(p_learn_more_url))
            return None


        clicked_btn = msg.clickedButton()
        if clicked_btn == ok_button:
            TomlHandler.toml_edit(


                "languages",

                "project_app_name",

                f"{qlinedit.text()}",

                "common",



            )




    def _window_popup(self,p_tool_name: str,
                            p_popup_icon: QMessageBox.Icon = QMessageBox.Icon.Critical,
                            p_learn_more_url: str = "about:blank",
                            p_window_title: str = "Tool Not Found",
                            p_has_download_button: bool = False,
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
        download_btn: QPushButton | None = None

        learn_more: QPushButton | None = None
        if p_has_download_button:
            download_btn: QPushButton = msg.addButton(
                p_download_button_txt,
                QMessageBox.ButtonRole.ActionRole)


        if p_learn_more_url:
            learn_more: QPushButton = msg.addButton(f"{Mwc.learn_more_txt}", QMessageBox.ButtonRole.HelpRole)


        msg.exec()

        if learn_more is not None and msg.clickedButton() == learn_more:
            QDesktopServices.openUrl(QUrl(p_learn_more_url))

        elif download_btn is not None and msg.clickedButton() == download_btn:
            self._start_2thread_worker(data=None, project_path=None, package_name=p_tool_name) # type: ignore



    def _check_editor(self, p_editor: str) -> bool:
        cmd = LcFg.EditorCmd.get_cmd(p_editor)

        if cmd == "NOEDITOR":
            return True
        elif not cmd:
            self._window_popup(p_editor)
            return False

        executable = shlex.split(cmd, posix=NTV_POSIX)[0]

        resolved = (
                shutil.which(executable) # noqa it'll never run on 3.12
                or (executable if Path(executable).is_file() else None)
        )

        if not resolved:
            self._window_popup(p_editor)
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
            self._window_popup(p_editor, p_info_txt=str(exc))
    def handle_2thread_outcomes(self, outcome: str, error_info: str):
        match outcome:
            # --- CCOOKIECUTTER OUTCOMES---
            case "cc_template_missing":
                self._window_popup("Cookiecutter",
                                   p_learn_more_url="https://cookiecutter.readthedocs.io/en/stable/README.html",
                                   p_msg_txt="template was not found",
                                   p_info_txt=f"{Mwc.Widget1.cookiecutter_error_msg}")
                return
            case "cc_json_missing":
                self._window_popup("Cookiecutter.json",
                                   p_learn_more_url="https://cookiecutter.readthedocs.io/en/stable/tutorials/tutorial2.html#step-2-create-cookiecutter-json",
                                   p_msg_txt="Template is invalid :(",
                                   p_info_txt="It looks like the selected directory does not contain any cookiecutter.json.")
                return
            case "cc_generation_failed":
                self._window_popup("cookiecutter",
                                   p_learn_more_url="https://cookiecutter.readthedocs.io/en/stable/troubleshooting.html#i-created-a-cookiecutter-but-it-doesn-t-work-and-i-can-t-figure-out-why",
                                   p_msg_txt="Project generation failed :(",
                                   p_info_txt=f"{Mwc.Widget1.cookiecutter_error_msg}: {error_info}")
                return

            # --- PYTHON OUTCOMES ---
            case "uverror":
                self._window_popup("uv", p_learn_more_url="https://docs.astral.sh/uv/guides/projects/",
                                   p_window_title="uv: project initialisation or sync failed!", p_msg_txt="",
                                   p_info_txt=(
                                       f"{Mwc.Widget3.uv_error_msg}: {error_info}"
                                   ))
                return

            case "poetryerror":
                self._window_popup("poetry", p_learn_more_url="https://python-poetry.org/docs/configuration/",
                                   p_window_title="poetry: project initialisation failed!", p_has_download_button=True,
                                   p_info_txt=(
                                       ":( \nNote: make sure Poetry is installed, the Python interpreter is valid "
                                       f"and the project path is usable.\nDetails:\n {error_info}"
                                   ))
                return

            case "pixierror":
                self._window_popup("pixi", p_learn_more_url="https://pixi.sh/latest/getting_started/",
                                   p_window_title="pixi: project initialisation failed!", p_msg_txt="", p_info_txt=(
                        ":( \nNote: make sure Pixi is installed and the Python version is valid "
                        f"and the project path is usable.\nDetails: \n{error_info}"
                    ))
                return

            case "condaerror":
                self._window_popup("conda",
                                   p_learn_more_url="https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html",
                                   p_window_title="conda: environment creation failed!", p_msg_txt="", p_info_txt=(
                        ":( \nNote: make sure conda is installed and you've entered "
                        f"a valid Python interpreter version.\n\nDetails: {error_info}"
                    ))
                return

            case "mambaerror":
                self._window_popup("mamba",
                                   p_learn_more_url="https://mamba.readthedocs.io/en/latest/user_guide/mamba.html",
                                   p_window_title="mamba: environment creation failed!", p_msg_txt="", p_info_txt=(
                        ":( \nNote: make sure mamba is installed and you've entered "
                        f"a valid Python interpreter version.\n\nDetails: {error_info}"
                    ))
                return

            case "hatcherror":
                self._window_popup("Hatch", p_learn_more_url="https://hatch.pypa.io/latest/environment/",
                                   p_window_title="Hatch: environment creation failed!")
                return
            case "hatcherr_pkg":
                self._window_popup(p_tool_name="Hatch", p_popup_icon=QMessageBox.Icon.Information,
                                   p_learn_more_url="https://github.com/pypa/hatch/issues/1599",
                                   p_window_title="Hatch information",
                                   p_msg_txt="Hatch does not provide a general command equivalent to 'pip install dependency'.\n Dependencies must be declared only in pyproject.toml manully")

            case "venverror":
                self._window_popup("venv", p_learn_more_url="https://docs.python.org/3/library/venv.html")
                return

            case "pdmerror":
                self._window_popup("pdm", p_learn_more_url="https://pdm-project.org/en/latest/usage/project/",
                                   p_has_download_button=True)
                return

            case "pipenverror":
                self._window_popup("pipenv", p_learn_more_url="https://pipenv.pypa.io/en/latest/basics/",
                                   p_window_title="pipenv: project initialisation failed!", p_has_download_button=True)
                return

            case "virtualenverror":
                self._window_popup("virtualenv",
                                   p_learn_more_url="https://virtualenv.pypa.io/en/latest/user_guide.html",
                                   p_has_download_button=True)
                return
            case "package_install_success":
                self._window_popup("", p_popup_icon=QMessageBox.Icon.Information,
                                   p_learn_more_url="https://python-poetry.org/docs/basic-usage/",
                                   p_msg_txt="tool Installation was successfull"
                                             "\nrestart ReapySet to see changes!")
                return
            case "package_install_error":
                self._window_popup("", p_popup_icon=QMessageBox.Icon.Warning,
                                   p_learn_more_url="https://python-poetry.org/docs/1.8#installation",
                                   p_msg_txt="tool Installation failed!"
                                             "\nTry again later or try a different tool.")
                return

            case "success":
                if self.worker is not None:
                    final_path = self.worker.proj_path
                    if self.editor != "None":
                        self._openin_editor(self.editor, final_path)
                        logger.success(f"Project created! Opened in editor: {self.editor} | Path: {final_path}")

    def _start_2thread_worker(
            self,
            data: TOMLDocument,
            project_path: str,
            package_name: str | None = None,
    ) -> None:
        if self.worker is not None and self.worker.isRunning():
            return

        worker = ConfirmButton2ndThread(
            p_data=data,
            p_proj_path=project_path,
            p_package_to_install=LcFg.package_names.get(package_name) if package_name else None,# .get doesnt like | None
        )

        worker.status_emitted.connect(
            self.handle_2thread_outcomes
        )

        self.worker = worker
        worker.start()

    def on_confirm_clicked(self) -> None:
        if self.worker is not None and self.worker.isRunning():
            return

        data: TOMLDocument = TomlHandler._toml_read()

        project_path: str = data["global"]["project_path"]
        editor: str = data["global"]["fav_editor"]
        active_framework: str = data["languages"]["common"]["selected_framework"]
        if active_framework == "PY:DJANGO":
            self._option_popup(p_window_title="Django", p_tool_name="Django",
                               p_qlinedit_top_txt="Enter the name of the Django app:", p_qlidedit_placeholder_txt="App Name...?", p_msg_txt="",
                               p_info_txt="Using snake_case is recommended.", p_learn_more_url="https://www.djangoproject.com/start/")



        if not self._check_editor(editor):
            return

        self.editor: str = editor

        self._start_2thread_worker(data=data, project_path=project_path)
