# (WIP) ReadySet
developer environment initialiser wrote in pyside6 still eavily in development


# ReapySet 🚀

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
- Editor integration (currently VSCode)
- Optional boilerplates support *(WIP)*

### Multi-language support *(planned / partial)*
- Python 🐍
- Rust 🦀
- .NET
- Kotlin / Java ☕
- C / C++
- TypeScript / JavaScript
- Go
- Lua
- GDScript

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

## Screenshots

![ReapySet UI](docs/images/main-ui.png)

---

## Installation

### Requirements

- Python 3.12+
- PySide6
- Supported package managers installed locally
  (`uv`, `poetry`, `pixi`, `conda`, etc.)

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

MIT License
