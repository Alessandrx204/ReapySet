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
- Initialize environments
- Select package managers
- Generate language-specific project structures
- Open projects directly in your preferred editor
- Apply boilerplates/templates

Think of it as a **developer launcher + project initializer**, with a focus on speed and usability.

---

## Current Features

### Project Setup
- Create projects in a chosen location
- Editor integration (currently VSCode, pycharm, clion, intellij idea, notepad++, godot's editor, sublime text)
- Optional boilerplates support *(WIP)*

### Multi-language support *(planned / partial)*
- Python 🐍 (almost 90% functional)
- Rust 🦀 - soon
- .NET - soon
- Kotlin / Java ☕ - possibly
- C / C++ - possibly
- TypeScript / JavaScript - possibly
- Go - possibly
- Lua - possibly
- GDScript - possibly

### Python Workspace Configuration
Choose your preferred environment/package manager:

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

Interpreter selection is supported for locally installed Python versions.

---

## development Screenshots

<img width="882" height="790" alt="Screenshot 2026-06-05 at 16 46 04" src="https://github.com/user-attachments/assets/49f8e7d4-1630-414e-9d32-575f7b219288" /> to 05/06/2026




---

## Installation

### Requirements

- Python 3.13.5+
- PySide6
- pyobjc on osx
- qtdarktheme

### Clone the project

```bash
git clone https://github.com/yourname/reapyset.git
cd reapyset
```

### Install dependencies

```bash
uv sync
```

or

```bash
pip install -r requirements.txt
```

### Run

```bash
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

- [ ] Better interpreter detection
- [ ] GitHub project import
- [ ] Boilerplate marketplace
- [ ] Per-language configuration presets
- [ ] Project templates
- [ ] Better macOS / Windows native styling
- [ ] Terminal integration
- [ ] Plugin system *(maybe)*

---

## Philosophy

ReapySet tries to stay:

- **Fast** → minimal clicks
- **Simple** → opinionated defaults
- **Modern** → clean desktop UX
- **Developer-first** → less setup, more coding

---

## Contributing

This project is experimental and evolving quickly.  
Issues, ideas and feedback are welcome.

---

## License
arr/lgpl

