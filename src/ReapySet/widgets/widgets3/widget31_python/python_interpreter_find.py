import pathlib
import shutil
import subprocess
import os
import sys
from pathlib import Path
from subprocess import CompletedProcess
from typing import Any

from PySide6.QtCore import Qt

"""
python_interpreter_find.py
------------------------
Utilities for detecting Python interpreters installed on the current machine.

get_python_interpreters()
    Scans three sources in order:
      1. PATH  – runs `shutil.which` for common python/python3.6-20 names,
                 resolves symlinks to avoid duplicates, and probes each
                 candidate with `--version`.
      2. Windows Python Launcher (`py`)  – queries `py -0` to list every
                 version registered with the official Windows installer,
                 then retrieves the real executable path for each one.
      3. pyenv  – walks ~/.pyenv/versions/ (or %PYENV_ROOT%) and collects
                 every interpreter found under bin/python (Unix) or
                 python.exe (Windows).

    Deduplication is handled via a dict keyed on the resolved absolute path,
    so two names pointing to the same file are counted only once.
    Returns a list of (path, label) tuples.

populate_interpreter_combobox(combobox)
    Convenience wrapper for Qt UIs: clears a QComboBox and fills it with
    the results of get_python_interpreters(). Each item stores the
    executable path as Qt userData so callers can retrieve it with
    combobox.currentData().
"""
def get_python_interpreters() -> list[tuple[str, str]]:
    """Returns a list of (label, path) pairs for the found Python interpreters."""
    found: dict[str, str] = {}
    is_windows: bool = sys.platform == "win32"

    # 1. looks for the PATH
    candidates: list[str] = ["python", "python3"] if not is_windows else ["python"]
    if not is_windows:# makes a list of possible canditates from 3.6 to 3.20
        candidates += [f"python3.{v}" for v in range(6, 20)] #note may need to work around and remove the limit

    for cmd in candidates:
        path: str | None = shutil.which(cmd) # looks for those
        if path is None:
            continue
        real_path: str = str(Path(path).resolve())  # ← avoids symlink
        if real_path in found:
            continue
        try:
            r: CompletedProcess[str] = subprocess.run([real_path, "--version"], capture_output=True, text=True, timeout=2)
            version: str = (r.stdout or r.stderr).strip() # make them run --version and capture the output
            found[real_path] = f"{version}"
        except (OSError, subprocess.TimeoutExpired, subprocess.SubprocessError):
            pass

    # 2. macOS: searches into macos standard directories
    if sys.platform == "darwin": # otherwise the bundled app couldn't locate interpreters on macos
        osx_python_paths: list[pathlib.Path] = [
            Path("/opt/homebrew/bin"),  # Homebrew Apple Silicon
            Path("/usr/local/bin"),  # Homebrew Intel
            Path.home() / ".local" / "bin",
        ]
        valid_names: set[str | str] = {"python", "python3",
                       *{f"python3.{version}" for version in range(6, 50)},}

        for directory in osx_python_paths:
            if not directory.is_dir():
                continue

            for path_obj in directory.glob("python3*"):
                if path_obj.name not in valid_names:
                    continue

                try:
                    real_path: str = str(path_obj.resolve())

                    if real_path in found:
                        continue

                    result = subprocess.run([ real_path,
                        "-c",
                        (
                            "import sys; "
                            "print(f'Python {sys.version_info.major}."
                            "{sys.version_info.minor}."
                            "{sys.version_info.micro}')"
                        ),
                    ],
                    capture_output=True,
                    text=True,
                    timeout=2,)


                    if result.returncode != 0:
                        continue

                    version = result.stdout.strip()
                    if version.startswith("Python "):
                        found[real_path] = version

                except (
                        OSError,
                        subprocess.TimeoutExpired,
                        subprocess.SubprocessError,
                ):
                    pass

    # 2. Windows: Python Launcher
    if is_windows:
        py_launcher = shutil.which("py")
        if py_launcher is not None:
            try:
                r = subprocess.run(["py", "-0"], capture_output=True, text=True, timeout=2)
                for line in r.stdout.splitlines():
                    line = line.strip().lstrip("-")
                    if not line:
                        continue
                    tag = line.split()[0]
                    version_tag = tag.split("-")[0]
                    try:
                        r2 = subprocess.run(
                            ["py", f"-{version_tag}", "--version"],
                            capture_output=True, text=True, timeout=2
                        )
                        r3 = subprocess.run(
                            ["py", f"-{version_tag}", "-c", "import sys; print(sys.executable)"],
                            capture_output=True, text=True, timeout=2
                        )
                        version = (r2.stdout or r2.stderr).strip()
                        path = r3.stdout.strip()
                        real_path = str(Path(path).resolve())  # ← fixes symlink
                        if path and real_path not in found:
                            found[real_path] = f"{version}  "#({real_path})
                    except (OSError, subprocess.TimeoutExpired, subprocess.SubprocessError):
                        pass
            except (OSError, subprocess.TimeoutExpired, subprocess.SubprocessError):
                pass

    # 3. pyenv
    pyenv_root_env = os.environ.get("PYENV_ROOT") or os.environ.get("PYENV")
    if pyenv_root_env is not None:
        pyenv_root = Path(pyenv_root_env)
    elif is_windows:
        pyenv_root = Path.home() / ".pyenv" / "pyenv-win"
    else:
        pyenv_root = Path.home() / ".pyenv"

    versions_dir = pyenv_root / "versions"
    if versions_dir.is_dir():
        for ver in sorted(versions_dir.iterdir()):

            python_exe = Path("python.exe") if is_windows else Path("bin") / "python"
            path_obj = ver / python_exe
            path = str(path_obj)
            if path_obj.is_file() and path not in found:
                found[path] = f"Python {ver.name}  (pyenv)  ({path})"

    return [(path, label) for path, label in found.items()]


def populate_interpreter_combobox(combobox) -> None:  # type: ignore[no-untyped-def]
    """Populates a QComboBox with the found interpreters."""
    combobox.clear()
    interpreters: list[tuple[str, str]] = get_python_interpreters()
    if interpreters:
        for path, label in interpreters:
            combobox.addItem(label, userData=path)
            combobox.setItemData(combobox.count() - 1,
                                 path,
                                 Qt.ItemDataRole.ToolTipRole)
            combobox.setToolTip(str(combobox.currentData()))
            combobox.currentIndexChanged.connect(
                lambda: combobox.setToolTip(str(combobox.currentData())))

    else:
        combobox.addItem("No interpreter was found")
        combobox.setToolTip("")