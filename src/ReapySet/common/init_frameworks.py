import json
import os
import shutil
from pathlib import Path


class InitFrameworks:
    @staticmethod
    def init_pyside6(p_path: str | Path) -> None :
        #app_path = Path(p_path)
        #app_path = app_path / "src" / "app"
        p_path = Path(p_path)
        file_to_remove: Path = p_path / "main.py"
        file_to_remove.unlink(missing_ok=True) # doesnt crash if not found
        source: Path = Path(__file__).parent / "fmk_templates" / "pyside6"


        shutil.copytree(

            source,

            p_path,

            dirs_exist_ok=True,
        )
        

    @staticmethod
    def init_jupyter_notebook(p_path: str, p_py_ver):
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

        full_path = Path(p_path) / "jupyter.ipynb"

        full_path.parent.mkdir(parents=True, exist_ok=True)

        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(template_notebook, f, indent=2)
