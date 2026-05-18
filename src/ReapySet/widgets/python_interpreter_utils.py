import shutil
import subprocess
import os
import sys
from pathlib import Path


def get_python_interpreters() -> list[tuple[str, str]]:
    """Restituisce lista di (label, path) degli interpreter Python trovati."""
    found: dict[str, str] = {}
    is_windows = sys.platform == "win32"

    # 1. Cerca nel PATH
    candidates: list[str] = ["python", "python3"] if not is_windows else ["python"]
    if not is_windows:
        candidates += [f"python3.{v}" for v in range(8, 15)]

    for cmd in candidates:
        path = shutil.which(cmd)
        if path is None:
            continue
        if path in found:
            continue
        try:
            r = subprocess.run([path, "--version"], capture_output=True, text=True, timeout=2)
            version = (r.stdout or r.stderr).strip()
            found[path] = f"{version}" #({path})
        except (OSError, subprocess.TimeoutExpired, subprocess.SubprocessError):
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
                        if path and path not in found:
                            found[path] = f"{version}  ({path})"
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
            # ✅ Path invece di os.path.join
            python_exe = Path("python.exe") if is_windows else Path("bin") / "python"
            path_obj = ver / python_exe
            path = str(path_obj)
            if path_obj.is_file() and path not in found:
                found[path] = f"Python {ver.name}  (pyenv)  ({path})"

    return [(path, label) for path, label in found.items()]


def populate_interpreter_combobox(combobox) -> None:  # type: ignore[no-untyped-def]
    """Popola un QComboBox con gli interpreter trovati."""
    combobox.clear()
    interpreters = get_python_interpreters()
    if interpreters:
        for path, label in interpreters:
            combobox.addItem(label, userData=path)
    else:
        combobox.addItem("Nessun interprete trovato")