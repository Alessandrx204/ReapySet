import os
import subprocess
import sys
from subprocess import CompletedProcess


def init_macos_term_path() -> None:
    if sys.platform != "darwin":
        return

    shell: str = os.environ.get("SHELL", "/bin/zsh")

    try:
        result: CompletedProcess[str] = subprocess.run(
            [
                shell,
                "-lic", #-lc instead of -lic if you want to disable zshrc
                'printf "__REAPYSET_PATH_START__%s__REAPYSET_PATH_END__" "$PATH"',
            ],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )

        output: str = result.stdout

        start_marker: str = "__REAPYSET_PATH_START__"
        end_marker: str = "__REAPYSET_PATH_END__"

        start: int = output.find(start_marker)
        end: int = output.find(end_marker, start + len(start_marker))

        if start != -1 and end != -1:
            shell_path: str = output[
                start + len(start_marker):end
            ].strip()

            if result.returncode == 0 and shell_path:
                os.environ["PATH"] = shell_path

    except (OSError, subprocess.TimeoutExpired):
        pass