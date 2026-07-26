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

Think of it as a **developer launcher + project initialiser**, with a focus on clarity and usability.

---

## Current Features

### Project Setup
- Default Location: Projects are created by default in user/projects/....
-	Dynamic Directory Creation: Any missing nested directories will be created on the fly. Please note that creating deeply nested structures may slightly increase initial setup time.
**Editor Integration**
-(currently PyCharm, VSCode, Zed, CLion, IntelliJ IDEA, Notepad++, Godot's editor, nVim & Sublime text are enabled by default but any editor  can be removed or added  or edited the startup command, via config file, just  make sure to follow there given instruction)
~(a No editor option is available as well)~
- Optional boilerplates support *(WIP)*

- Customisation: You can easily add, remove, or modify the startup commands for any editor via the configuration file. Please ensure you follow the specific instructions provided within the file.

### Multi-language support *(planned / partial)*
| Feature | Status |
|----------|--------|
| python | ⚠️ In progress |
| JavaScript/typescript | ⏳ Next|
| .NET | 🚧 Planned |
| rust | 🚧 Planned |
| Mojo | 📝 Considered  |
| Docker | 📝 Condidered |
| Kotlin/java |  TBD  |
| C/C++ |  TBD  |
| lua |  TBD  |
| GO |  TBD  |
| GDSsript |  TBD  |

### Python Workspace Configuration
**available python package managers**

- `uv`
- `pip`
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

<img width="882" height="510" alt="Screenshot 2026-07-06 at 20 48 24" src="https://github.com/user-attachments/assets/9720e487-dbf1-4191-8e09-03104efb31ed" />
06/07(2026

---

## Installation

### Requirements

- Python 3.13.5+
- PySide6
- pyobjc on OS X (on legacy versions)
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


---

## Roadmap

- [X] Better UI and UX
- [ ] Python frameworks support
- [ ] keyboard navigation
- [ ] GitHub project import (It's surprisignly extremely harder than expected)
- [ ] CookieCutter Boilerplates support (i hate writing those)
- [X] Per-language configuration presets
- [ ] JavaScript support
- [ ] Better view on Linux / Windows 
- [ ] Command line version

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

ReapySet is my first major project, and as a beginner/junior developer, I know there is always room for optimization, refactoring, and improvements. The code isn't perfect, but it works, and I'm proud of it 

If you see something that can be improved, written better, or optimized:
* Feel free to open an Issue to discuss it.
* Submit a PR!❤️ I’m highly open to feedback, code reviews, and learning from more experienced developers. (@ _ @)ゝ


---

## License & Commercial Usage

ReapySet is a **source-available** project. 

* **Non-Commercial Use:** You are free to view, modify, and compile the software from source for personal, educational, or non-commercial purposes.
* **Commercial Use:** If you are using ReapySet within a company, for commercial projects, or to generate revenue, you are required to purchase a commercial license.


* **Software Integrity & Visual Assets Protection:**
All graphical user interface (GUI) elements, visual assets, brand identifiers, and hardcoded artistic or identity displays—including, but not limited to, the flag rendered via QPainter, or the icon are protected components of this software.
 You are strictly prohibited from removing, hiding, obscuring, or altering these visual elements in any modification, fork, or compiled version of the software.
 Any attempt to bypass, comment out, or disable the code responsible for rendering these assets will result in the immediate and automatic revocation of your license to use, view, or modify this software. Any subsequent use will be treated as an intentional copyright infringement and a violation of technical protection measures.


Pre-compiled binaries are available for a symbolic price to support the development and maintenance of the project.:)

* ~~[Buy a Pre-compiled Binary / Commercial License here]~~ (Coming Soon)

*Note on Qt:* ReapySet is built using PySide6. The source code of ReapySet is distributed under a proprietary source-available license, while the PySide6/Qt binaries adhere to the **LGPLv3** license.
---

## Why Source-Available and not fully Open Source? (FAQ)

**TL;DR:** I’m testing if software development can become my full-time career, or if I should go back to medical school. Buying a license directly supports this journey.

Here is the long story:
ReadySet is my first major, serious software project. I poured time and passion into crafting this tool  

Instead of going the traditional FOSS (Free and Open Source) route, I chose a **source-available / paid binary model** for two main reasons:

1. **Sustainability & Career Pivot:** I want to see if independent software development can be a viable career path for me. If this experiment fails, I’ll likely have to pivot back to medical school -_-.
 Charging a symbolic price helps me measure the actual market value of my work and maybe sustain development❤️.
2. **Transparency:** If you just want to review the code, learn from it, or use it for your personal indie projects, you can compile it from source for free. But if you use it to make your commercial workflow faster, contributing a small fee keeps the project alive.

I believe developers should be compensated for building good tools. If you share this vision, thank you for supporting an independent EU developer!

