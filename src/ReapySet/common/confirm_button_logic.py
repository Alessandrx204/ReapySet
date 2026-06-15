import shlex
import shutil
import subprocess
from pathlib import Path
from typing import Any

from PySide6.QtCore import QThread, Signal, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QMessageBox

from ReapySet.config import LogicVariables as LcFg
from common.toml_handler import TomlHandler, DEST_PATH

#common/confirm_button.py
TomlHandler.toml_get(DEST_PATH, "languages", "interpreter_version", "python")

class SetupWorker(QThread):
    finished = Signal()

    def __init__(self, p_cmds: list, p_proj_path: str, p_editor_cmd: str):
        super().__init__()
        self.cmds = p_cmds
        self.proj_path = p_proj_path
        self.editor_cmd = p_editor_cmd

    def run(self):
        subprocess.run(self.cmds)
        subprocess.Popen(self.editor_cmd.split())
        self.finished.emit()
class ConfirmButtonLogic:
    ...
    #todo should execute the env creation,
    # reads from the toml_cc the temp configs
    # and from config.py (editable in future via config.toml)
    # setup_python, setup_dotnet, setup_rust
    # and a list of commands that will be called via subprpcess.Popen(py_uv/py_poetry/py_venv_init_cmd:set[set[str]]
    # rs_cargo dotnet else with a match case)
    @staticmethod
    def _warn_missing_popup(p_tool_name: str,
                           p_learn_more_url: str = "about:blank",
                           p_window_title: str = "Tool Not Found",
                           p_msg_txt: str = "not found or not installed.",
                           p_info_txt: str = "Make sure it is installed and the path is correct in config.toml"
                           ) -> None:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle(p_window_title)
        msg.setText(f" {p_tool_name} {p_msg_txt}")
        msg.setInformativeText(p_info_txt)

        msg.addButton("OK", QMessageBox.ButtonRole.AcceptRole)

        if p_learn_more_url:
            learn_more = msg.addButton("Learn More", QMessageBox.ButtonRole.HelpRole)
            msg.exec()
            if msg.clickedButton() == learn_more:
                QDesktopServices.openUrl(QUrl(p_learn_more_url))
        else:
            msg.exec()

    def _check_editor(self, p_editor: str) -> bool:
        cmd = LcFg.EditorCmd.get_cmd(p_editor)

        if not cmd:
            self._warn_missing_popup(p_editor)
            return False

        executable = cmd.split()[0]

        resolved = (
                shutil.which(executable) # noqa it'll never run on 3.12
                or (executable if Path(executable).is_file() else None)
        )

        if not resolved:
            self._warn_missing_popup(p_editor)
            return False

        return True

    def _openin_editor(self, p_editor: str, p_proj_path: str) -> None:

        cmd = LcFg.EditorCmd.get_cmd(p_editor)

        editor_openin_cmd = cmd.format(path=p_proj_path)

        try:

            subprocess.Popen(

                shlex.split(editor_openin_cmd),

                env=self._get_sterile_env()

            )

        except Exception:

            self._warn_missing_popup(p_editor)

        except Exception:
            self._warn_missing_popup(p_editor)

    def _get_sterile_env(self) -> dict[str, str]:

        import os

        clean_env = os.environ.copy()

        for env_var in [

            "VIRTUAL_ENV",

            "PYTHONHOME",

            "PYTHONPATH",

            "CONDA_PREFIX",

            "CONDA_DEFAULT_ENV",

            "UV_PROJECT_ENVIRONMENT",

            "UV_ACTIVE",

            "PIPENV_ACTIVE",

            "POETRY_ACTIVE",

        ]:
            clean_env.pop(env_var, None)

        return clean_env

    def _run_cmd(self, cmd: list[str], cwd: str | None = None) -> subprocess.CompletedProcess | None:
        try:
            return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, env=self._get_sterile_env())
        except FileNotFoundError:
            return None

    def setup_python(self, p_py_config: dict[str, Any], p_proj_path: str, p_editor: str) -> None:
        import os
        for env_var in ["VIRTUAL_ENV", "PYTHONHOME", "PYTHONPATH", "CONDA_PREFIX"]:
            os.environ.pop(env_var, None)
        if not self._check_editor(p_editor):
            return  # if editor is not to be found or cli is not functioning it doesnt even create the venv
            # post conditional mkdir
        pm: str = p_py_config["package_manager"]
        interp: str = p_py_config["interpreter_path"]

        interp_ver: str | None = TomlHandler.toml_get(
            DEST_PATH,
            "languages",
            "interpreter_version",
            "python"
        )

        unb_interp_ver: str | None = TomlHandler.toml_get(
            DEST_PATH,
            "languages",
            "unb_interpreter_version",
            "python"
        ) # unbound interpreter

        # for conda / mamba / pixi unbound version if any else specific path's version
        pm_python_ver: str | None = unb_interp_ver or interp_ver

        # for uv unbound version if any else path
        uvs_python: str = unb_interp_ver or interp_ver or interp

        match pm:
            case "PY:UV":
                result = self._run_cmd(
                    LcFg.PythonVars.py_uv_icmd + [p_proj_path, "--python", uvs_python]
                )
                if result is None:
                    self._warn_missing_popup("uv")
                    return
                if result.returncode != 0:
                    self._warn_missing_popup("uv: invalid interpretr version!",
                                             p_learn_more_url="https://docs.astral.sh/uv/guides/projects/",
                                             p_msg_txt="",
                                             p_info_txt=result.stderr + ":( \nNote: Make sure the one you've entered a valid python interpreter version")
                    return
                Path(p_proj_path).mkdir(parents=True, exist_ok=True)

            case "PY:POETRY":
                Path(p_proj_path).mkdir(parents=True, exist_ok=True)
                try:
                    subprocess.Popen(
                        LcFg.PythonVars.py_poetry_icmd + [p_proj_path],
                              env=self._get_sterile_env()

                    )
                except Exception:
                    self._warn_missing_popup("poetry")
                    return

            case "PY:PIXI":
                result = self._run_cmd(
                    LcFg.PythonVars.py_pixi_icmd + [p_proj_path]
                )
                if result is None:
                    self._warn_missing_popup("pixi")
                    return
                if result.returncode != 0:
                    self._warn_missing_popup("Pixi: invalid interpretr version!",
                                             p_learn_more_url="https://pixi.prefix.dev/latest/getting_started/#creating-a-new-project",
                                             p_msg_txt="",
                                             p_info_txt=result.stderr + ":( \nNote: Make sure the one you've entered a valid python interpreter version")
                    return
                Path(p_proj_path).mkdir(parents=True, exist_ok=True)
                if pm_python_ver:
                    result2 = self._run_cmd(
                        [LcFg.PythonVars.py_pixi_path, "add", f"python={pm_python_ver}"],
                        cwd=p_proj_path
                    )
                    if result2 is None:
                        self._warn_missing_popup("pixi")
                        return
                    if result2.returncode != 0:
                        self._warn_missing_popup("Pixi: invalid interpretr version!",
                                                 p_learn_more_url="https://pixi.prefix.dev/latest/getting_started/#creating-a-new-project",
                                                 p_msg_txt="",
                                                 p_info_txt=result2.stderr + ":( \nNote: Make sure the one you've entered a valid python interpreter version")
                        return

            case "PY:GENERIC_CONDA":
                result = self._run_cmd(
                    LcFg.PythonVars.py_conda_icmd
                    + [str(Path(p_proj_path) / ".conda")]
                    + ([f"python={pm_python_ver}"] if pm_python_ver else [])
                )
                if result is None:
                    self._warn_missing_popup("conda")
                    return
                if result.returncode != 0:
                    self._warn_missing_popup("Conda: invalid interpretr version!",
                                             p_learn_more_url="https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html",
                                             p_msg_txt="",
                                             p_info_txt=result.stderr + ":( \nNote: Make sure the one you've entered a valid python interpreter version")
                    return
                Path(p_proj_path).mkdir(parents=True, exist_ok=True)

            case "PY:MAMBA":
                result = self._run_cmd(
                    LcFg.PythonVars.py_mamba_icmd
                    + [str(Path(p_proj_path) / ".mamba")]
                    + ([f"python={pm_python_ver}"] if pm_python_ver else [])
                )
                if result is None:
                    self._warn_missing_popup("mamba")
                    return
                if result.returncode != 0:
                    self._warn_missing_popup("Mamba: invalid interpretr version!",
                                             p_learn_more_url="https://mamba.readthedocs.io/en/latest/user_guide/mamba.html",
                                             p_msg_txt="",
                                             p_info_txt=result.stderr + ":( \nNote: Make sure the one you've entered a valid python interpreter version")
                    return
                Path(p_proj_path).mkdir(parents=True, exist_ok=True)

            case "PY:HATCH":
                Path(p_proj_path).mkdir(parents=True, exist_ok=True)
                try:
                    subprocess.Popen(
                        LcFg.PythonVars.py_hatch_icmd + [p_proj_path],env=self._get_sterile_env()
                    )
                except Exception:
                    self._warn_missing_popup("hatch",
                                             p_learn_more_url="https://hatch.pypa.io/latest/intro/#initialization")
                    return

            case "PY:VENV":
                Path(p_proj_path).mkdir(parents=True, exist_ok=True)
                try:
                    subprocess.Popen(
                        [interp, "-m", "venv", ".venv"],
                        cwd=p_proj_path,
                        env=self._get_sterile_env()
                    )
                except Exception:
                    self._warn_missing_popup("pip", p_learn_more_url="https://docs.python.org/3/library/venv.html")
                    return

            case "PY:PDM":
                Path(p_proj_path).mkdir(parents=True, exist_ok=True)
                try:
                    subprocess.Popen(
                        LcFg.PythonVars.py_pdm_icmd + ["--python", interp],
                        cwd=p_proj_path,
                        env=self._get_sterile_env()
                    )
                except Exception:
                    self._warn_missing_popup("pdm", p_learn_more_url="//pdm-project.org/en/latest/usage/project/")
                    return

            case "PY:PIPENV":
                Path(p_proj_path).mkdir(parents=True, exist_ok=True)
                try:
                    subprocess.Popen(
                        LcFg.PythonVars.py_pipenv_icmd + ["--python", interp],
                        cwd=p_proj_path,
                        env=self._get_sterile_env()
                    )
                except Exception:
                    self._warn_missing_popup("pipenv", p_learn_more_url="https://pipenv.pypa.io/en/latest/basics/")
                    return

            case "PY:VIRTUALENV":
                Path(p_proj_path).mkdir(parents=True, exist_ok=True)
                try:
                    subprocess.Popen(
                        [LcFg.PythonVars.py_virtualenv_path, "-p", interp, ".venv"],
                        cwd=p_proj_path,
                        env=self._get_sterile_env()
                    )
                except Exception:
                    self._warn_missing_popup("virtualenv",
                                             p_learn_more_url="https://virtualenv.pypa.io/en/latest/user_guide.html")
                    return

        self._openin_editor(p_editor, p_proj_path)
    def setup_rust(self, p_rs_config: dict[str, Any], p_proj_path: str, p_editor:str) -> None:
        ...
    def setup_dotnet(self, p_dnet_config: dict[str, Any], p_proj_path: str, p_editor:str) -> None:
        ...

    def on_confirm_clicked(self) -> None:

        data = TomlHandler._toml_read() # noqa
        proj_path = data["global"]["project_path"]
        editor = data["global"]["fav_editor"]

        if data["languages"]["python"]["enabled"]:
            self.setup_python(data["languages"]["python"], proj_path, editor)
        elif data["languages"]["rust"]["enabled"]:
            self.setup_rust(data["languages"]["rust"], proj_path, editor)
        elif data["languages"]["dotnet"]["enabled"]:
            self.setup_dotnet(data["languages"]["dotnet"], proj_path, editor)

