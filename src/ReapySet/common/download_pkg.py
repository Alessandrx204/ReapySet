import shutil
import subprocess
import sys
from subprocess import CompletedProcess


class DownloadPkg:
    """it doesnt check if the package exists since its already set"""

    @staticmethod
    def _get_package_manager() -> str | None:

        if sys.platform == "win32":
            if shutil.which("winget"):
                return "winget"

            if shutil.which("choco"):
                return "choco"

            return None

        if sys.platform == "darwin":
            if shutil.which("brew"):
                return "brew"

            return None

        if sys.platform.startswith("linux"):

            distro: str | None = DownloadPkg._get_linux_distro()

            match distro:
                case "ubuntu":
                    if shutil.which("snap"):
                        return "snap"

                    if shutil.which("apt"):
                        return "apt"

                case "debian":
                    if shutil.which("apt"):
                        return "apt"

                case "fedora":
                    if shutil.which("dnf"):
                        return "dnf"

                case "arch" | "manjaro":
                    if shutil.which("pacman"):
                        return "pacman"

                case "opensuse":
                    if shutil.which("zypper"):
                        return "zypper"

            return None

        return None

    @staticmethod
    def _get_linux_distro() -> str | None:

        try:
            with open("/etc/os-release", encoding="utf-8") as file:
                data: dict[str, str] = {}

                for line in file:
                    key, _, value = line.partition("=")

                    if key and value:
                        data[key] = value.strip().strip('"')

            return data.get("ID")

        except OSError:
            return None

    @staticmethod
    def install_package(p_package_names: dict[str, str]) -> bool:

        os_pm = DownloadPkg._get_package_manager()
        if os_pm is None:
            print("No supported package manager found.")
            return False

        package_name = p_package_names.get(os_pm)
        if package_name is None:



            print(f"This package is not configured for "
                    f"the '{os_pm}' package manager."
                  )
            return False



        match os_pm:

            case "winget":
                command = [
                    "winget",
                    "install",
                    "--exact",
                    "--id",
                    package_name,
                ]

            case "choco":
                command = [
                    "choco",
                    "install",
                    package_name,
                    "-y",
                ]

            case "brew":
                command = [
                    "brew",
                    "install",
                    package_name,
                ]

            case "snap":
                command = [
                    "sudo",
                    "snap",
                    "install",
                    package_name,
                ]

            case "apt":
                command = [
                    "sudo",
                    "apt",
                    "install",
                    "-y",
                    package_name,
                ]

            case "dnf":
                command = [
                    "sudo",
                    "dnf",
                    "install",
                    "-y",
                    package_name,
                ]

            case "pacman":
                command = [
                    "sudo",
                    "pacman",
                    "-S",
                    "--noconfirm",
                    package_name,
                ]

            case "zypper":
                command = [
                    "sudo",
                    "zypper",
                    "--non-interactive",
                    "install",
                    package_name,
                ]

            case _:
                return False

        result: CompletedProcess = subprocess.run(command)

        return result.returncode == 0