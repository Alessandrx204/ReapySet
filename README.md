# (WIP) ReapySet
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
- Initialise environments
- Select package managers
- Generate language-specific project structures
- Open projects directly in your preferred editor
- Apply boilerplates/templates

Think of it as a **developer launcher + project initialiser**, with a focus on speed and usability.

---

## Current Features

### Project Setup
- Default Location: Projects are created by default in user/projects/....
-	Dynamic Directory Creation: Any missing nested directories will be created on the fly. Please note that creating deeply nested structures may slightly increase initial setup time.
**Editor Integration**
-(currently PyCharm, VSCode, Zed, CLion, IntelliJ IDEA, Notepad++, Godot's editor, nVim & Sublime text are enabled by default but any editor  can be removed or added  or edited the startup command, via config file, just  make sure to follow there given instruction)

- Optional boilerplates support *(WIP)*

- Customisation: You can easily add, remove, or modify the startup commands for any editor via the configuration file. Please ensure you follow the specific instructions provided within the file.

### Multi-language support *(planned / partial)*
| Feature | Status |
|----------|--------|
| python | ⚠️ In progress |
| rust | 🚧 Planned |
| .NET | 🚧 Planned |
| Typescript/Javascript/TSX/JSX | 📝 Considered  |
| Mojo | 📝 Considered  |
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


<img width="1705" height="970" alt="Screenshot 2026-06-17 at 15 50 10" src="https://github.com/user-attachments/assets/67850eb0-0b2d-420c-bad2-2f522630ce0d" />

<img width="882" height="790" alt="Screenshot 2026-06-17 at 15 44 42" src="https://github.com/user-attachments/assets/16cf70d1-8e58-4a51-b825-4e7e40a8b126" />

17/06/26

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
using uv (recommended)
```bash/zsh
uv sync
```

or using pip (make sure to activate your virtual environment first)

```bash/zsh
pip install -r requirements.txt
```

### Run
using uv (recommended)
```bash/zsh
uv run main.py
```

or

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
- [ ] keyboard navigation
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
but you're free to build yourself from source for non commercial usage :)


