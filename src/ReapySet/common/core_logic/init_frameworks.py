import json
import shutil
from pathlib import Path
from ReapySet.common.core_logic.logging import logger


class InitFrameworks:


    #----------- GUIS ----------#
    @staticmethod
    def init_pyside6(p_path: str | Path) -> None:
        # app_path = Path(p_path)
        # app_path = app_path / "src" / "app"
        p_path = Path(p_path)
        (p_path / "main.py").unlink(missing_ok=True)  # File to remove; doesn't crash if not found
        source: Path = Path(__file__).parents[1] / "fmk_templates" / "pyside6"

        shutil.copytree(

            source,

            p_path,

            dirs_exist_ok=True,
        )
        logger.info("init_pyside6 called")

    @staticmethod
    def init_tkinter(p_path: str | Path) -> None:
        p_path = Path(p_path)
        (p_path / "main.py").unlink(missing_ok=True)  # File to remove; doesn't crash if not found
        source: Path = Path(__file__).parents[1] / "fmk_templates" / "ctk_and_tkinter" / "Tkinter"

        shutil.copytree(

            source,

            p_path,

            dirs_exist_ok=True,
        )

        logger.info("init_tkinter called")

    @staticmethod
    def init_ctk(p_path: str | Path) -> None:
        p_path = Path(p_path)
        (p_path / "main.py").unlink(missing_ok=True)  # File to remove;doesn't crash if not found
        source: Path = Path(__file__).parents[1] / "fmk_templates" / "ctk_and_tkinter" / "ctk"

        shutil.copytree(

            source,

            p_path,

            dirs_exist_ok=True,
        )

        logger.info("init_ctk called")

    @staticmethod
    def init_flet(p_path: str | Path) -> None:
        p_path = Path(p_path)
        (p_path / "main.py").unlink(missing_ok=True)  # File to remove;doesn't crash if not found
        source: Path = Path(__file__).parents[1] / "fmk_templates" / "flet"

        shutil.copytree(

            source,

            p_path,

            dirs_exist_ok=True,
        )

        logger.info("init_flet called")


    #----------- WEB ----------#


    @staticmethod
    def init_flask(p_path: str | Path) -> None:
        p_path = Path(p_path)
        (p_path / "main.py").unlink(missing_ok=True)  # File to remove;doesn't crash if not found
        source: Path = Path(__file__).parents[1] / "fmk_templates" / "flask"

        shutil.copytree(

            source,

            p_path,

            dirs_exist_ok=True,
        )

        logger.info("init_flask called")

    @staticmethod
    def init_django(
            p_path: str | Path,
            p_app_name: str,
            p_runner,
    ) -> bool:
        p_path = Path(p_path)

        logger.info("init_Django called")

        (p_path / "main.py").unlink(missing_ok=True)
        if not p_runner(
                [
                    "python",
                    "-m",
                    "django",
                    "startproject",
                    p_app_name,
                    ".",
                ],
                p_path,
                p_error_code="djangoerror",
        ):
            return False

        if not p_runner(
                [
                    "python",
                    "manage.py",
                    "migrate",
                ],
                p_path,
                p_error_code="djangoerror",
        ):
            logger.info("init_Django failed")

            return False

        logger.info("init_Django succeded")

        return True


    @staticmethod
    def init_fastapi(p_path: str | Path) -> None:
        p_path = Path(p_path)
        (p_path / "main.py").unlink(missing_ok=True)  # File to remove;doesn't crash if not found
        source: Path = Path(__file__).parents[1] / "fmk_templates" / "fastapi"

        shutil.copytree(

            source,

            p_path,

            dirs_exist_ok=True,
        )
        logger.info("init_fastapi called")

    @staticmethod
    def init_streamlit(p_path: str | Path) -> None:
        p_path = Path(p_path)
        (p_path / "main.py").unlink(missing_ok=True)  # File to remove;doesn't crash if not found
        source: Path = Path(__file__).parents[1] / "fmk_templates" / "streamlit"

        shutil.copytree(

            source,

            p_path,

            dirs_exist_ok=True,
        )
        logger.info("init_streamlit called")

    @staticmethod
    def init_pyscript(p_path: str | Path) -> None:
        p_path = Path(p_path)
        (p_path / "main.py").unlink(missing_ok=True)  # File to remove;doesn't crash if not found
        source: Path = Path(__file__).parents[1] / "fmk_templates" / "pyscript"


        shutil.copytree(

            source,

            p_path,

            dirs_exist_ok=True,
        )

        logger.info("pyscript called")



    #----------- NOTEBOOKS ----------#


    @staticmethod
    def init_jupyter_notebook(
            p_path: str | Path,
            p_py_ver: str,
    ) -> None:
        template_notebook = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        "# Starter Template\n",
                        "This notebook was automatically generated using ReapySet.\n"
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": [
                        "def main():\n",
                        "    print(\"Running main programme...\")\n",
                        "    \n",
                        "    # A trivial example calculation\n",
                        "    result = sum_numbers(10, 20)\n",
                        "    print(f\"The result is: {result}\")\n",
                        "\n",
                        "def sum_numbers(a, b):\n",
                        "    return a + b\n",
                        "\n",
                        "# Entry point\n",
                        "if __name__ == \"__main__\":\n",
                        "    main()"
                    ]
                }
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": f"Python {p_py_ver}",
                    "language": "python",
                    "name": "python3"
                },
                "language_info": {
                    "name": "python"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 5
        }

        nb_path = Path(p_path) / "jupyter.ipynb"

        nb_path.parent.mkdir(parents=True, exist_ok=True)

        with open(nb_path, "w", encoding="utf-8") as f:
            json.dump(template_notebook, f, indent=2)

        logger.info("init_jupyter called")

    @staticmethod
    def init_marimo(p_path: str | Path) -> None:
        p_path = Path(p_path)
        (p_path / "main.py").unlink(missing_ok=True)  # File to remove;doesn't crash if not found
        source: Path = Path(__file__).parents[1] / "fmk_templates" / "marimo_notebook"

        shutil.copytree(

            source,

            p_path,

            dirs_exist_ok=True,
        )
        logger.info("init_marimo called")
    #----------- BOTS ----------#

    @staticmethod
    def init_ptb(p_path: str | Path) -> None:
        p_path = Path(p_path)
        (p_path / "main.py").unlink(missing_ok=True)  # File to remove;doesn't crash if not found
        source: Path = Path(__file__).parents[1] / "fmk_templates" / "ptb"

        shutil.copytree(

            source,

            p_path,

            dirs_exist_ok=True,
        )
        logger.info("init_ptb called")

    @staticmethod
    def init_discordpy(p_path: str | Path) -> None:
        p_path = Path(p_path)
        (p_path / "main.py").unlink(missing_ok=True)  # File to remove; doesn't crash if not found
        source: Path = Path(__file__).parents[1] / "fmk_templates" / "discordpy"

        shutil.copytree(

            source,

            p_path,

            dirs_exist_ok=True,
        )
        logger.info("init_discordpy called")

    @staticmethod
    def init_pytest(p_path: str | Path) -> None:
        # if pytest is enabled
        p_path = Path(p_path)
        test_path = p_path / "tests"
        test_path.mkdir(parents=True, exist_ok=True)

        for filename in ("test_main.py", "__init__.py"):
            with open(test_path / filename, "w", encoding="utf-8") as f:
                if filename == "test_main.py":
                    f.write("""
def add(a: int, b: int) -> int:

    return a + b

def test_add() -> None:

    \"\"\"Test the add function.\"\"\"

    assert add(2, 3) == 5

                            """)
        logger.info("init_pytest called")