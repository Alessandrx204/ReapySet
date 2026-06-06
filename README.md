# (WIP) ReadySet
developer environment initialiser wrote in pyside6 still eavily in development


# ReapySet/ReadySet (haven't decided the name yet) 🚀

**A modern, lightweight and opinionated project bootstrapper for developers.**

ReapySet is a desktop application designed to quickly scaffold development workspaces for multiple programming languages with minimal setup friction.

> ⚠️ **Work in Progress (WIP)**  
> ReapySet is currently under active development. Features may be incomplete, unstable, or subject to breaking changes.

---

## ✨ Vision

The goal of ReapySet is to provide a clean and fast way to:

- Create development workspaces
- Configure interpreters automatically
- Initialise environments
- Select package managers
- Generate language-specific project structures
- Open projects directly in your preferred editor
- Apply boilerplates/templates

Think of it as a **developer launcher + project initialiser**, with a focus on speed and usability.

---

## Current Features

### Project Setup
- Create projects in a chosen location
- Editor integration (currently VSCode, pycharm, clion, intellij idea, notepad++, godot's editor, sublime text)
- Optional boilerplates support *(WIP)*

### Multi-language support *(planned / partial)*
| Feature | Status |
|----------|--------|
| python | ⚠️ In progress |
| rust | 🚧 Planned |
| .NET | 🚧 Planned |
| Typescript/Javascript |  TBD  |
| Kotlin/java |  TBD  |
| C/C++ |  TBD  |
| lua |  TBD  |
| GO |  TBD  |
| GDSsript |  TBD  |

### Python Workspace Configuration
**available python package managers**

- `venv`
- `uv`
- `poetry`
- `hatch`
- `pixi`
- `conda`
- `mamba`
- `pipenv`
- `virtualenv`
- `pdm`



---

## development Screenshots

<img width="882" height="790" alt="Screenshot 2026-06-05 at 16 46 04" src="https://github.com/user-attachments/assets/49f8e7d4-1630-414e-9d32-575f7b219288" /> to 05/06/2026




---

## Installation

### Requirements

- Python 3.13.5+
- PySide6
- pyobjc on OS X
- qtdarktheme
- tomlkit

### Clone the project

```bash/zsh
git clone https://github.com/yourname/reapyset.git
cd reapyset
```

### Install dependencies

```bash/zsh
uv sync
```

or

```bash/zsh
pip install -r requirements.txt
```

### Run

```bash/zsh
python main.py
```

---

## Project Status

Current development state:

| Feature | Status |
|----------|--------|
| GUI foundation | ✅ |
| Python setup | ⚠️ In progress |
| Boilerplates | ⚠️ Partial |
| Multi-language support | 🚧 Planned |
| GitHub import | 🚧 Coming soon |
| Cross-platform polish | 🚧 Ongoing |

---

## Roadmap

- [ ] Better UI and UX
- [ ] GitHub project import
- [ ] Boilerplates' repo (i hate writing those)
- [ ] Per-language configuration presets
- [ ] Better macOS / Windows native styling
- [ ] Terminal Command line version

---

## Philosophy

ReapySet tries to stay:

- **fast** → minimal clicks
- **Simple** → opinionated defaults
- **Modern** → clean desktop UX across platforms, eliminating the pain of having different commands for pwsh and bash
- **Developer-first** → less setup, more coding
- **Sovreign** →  Made by EU Developers mainly for EU developers
- **Cozy** →  cute greetings, about IT, European and lgbtq civil rights and history, always comfy ✨

---

## Contributing

feel free to submit a pr,

---

## License
source code is all right reserved/Qt binaries are available in concordance to Qt's LGPLv3 License


