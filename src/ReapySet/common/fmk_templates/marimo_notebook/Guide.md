# How to Run & Edit Marimo Notebooks

This project uses **Marimo**, a reactive Python notebook framework where files are saved as standard `.py` scripts.

---

## 1. Installation

Ensure Python is installed, then install Marimo:
(it should be handled by ReapySet by default )

```bash/zsh
pip install marimo or uv add marimo (for other package managers you can easily follow their documentation)
```

---

## 2. Editing the Notebook (Interactive UI)

### Option A: VS Code (Recommended)

1. Install the official **[Marimo Extension](https://marketplace.visualstudio.com/items?itemName=marimo-team.vscode-marimo)**.
2. Open your notebook file (e.g. `marimo_template.py`).
3. Click the **"Open in Marimo Editor"** icon in the top-right corner (or press `Ctrl+Shift+P` / `Cmd+Shift+P` and select `Marimo: Open Editor`).

### Option B: Terminal & Browser

Navigate to the project folder and run:

```bash/zsh
marimo edit marimo_template.py
```

This launches a local server and opens the cell editor in your default browser (`http://localhost:2718`).

---

## 3. Running as an App / Dashboard

To display outputs and UI widgets without showing the code:

```bash/zsh
marimo run marimo_template.py
```

---

## 4. Running as a Python Script

Since it is a standard Python file, you can also execute it directly:

```bash/zsh
python marimo_template.py or uv run marimo_template.py
```

---

## Recommended  Extensions

* **[Marimo notebooks' extension for VSCode](https://marketplace.visualstudio.com/items?itemName=marimo-team.vscode-marimo):** Edit and run notebooks directly inside VS Code.
* **[Marimo notebooks' extension for JetBrains IDEs](https://plugins.jetbrains.com/plugin/32416-marimo):** Edit and run notebooks directly inside JetBrains IDEs.
