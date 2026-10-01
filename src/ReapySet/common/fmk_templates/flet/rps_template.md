# Flet App

A minimal Flet application generated with **ReapySet**.

## Getting Started

Run the application from the project directory:

on windows:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

```bash
flet run
```

If you are using `uv`:

```bash
uv run flet run
```

The application entry point is configured through:

```toml
[tool.flet.app]
path = "src"
```

## Project Structure

```text
.
├── src/
│   ├── main.py
│   ├── views/
│   │   ├── __init__.py
│   │   └── home_view.py
│   └── assets/
│       └── .gitkeep
├── pyproject.toml
└── README.md
```

- `src/main.py` — Main application entry point.
- `src/views/` — Application views and UI screens.
- `src/assets/` — Images, icons, fonts, and other static resources.
- `pyproject.toml` — Project and Flet configuration.

## Development

Flet automatically reloads the application when source files change.

Stop the application with:

```text
Ctrl+C
```

## Adding a New View

Create a new module inside `src/views/`:

```text
src/views/
├── home_view.py
└── settings_view.py
```

Then import and use the new view from `main.py` or from another view.

## Assets

Place application resources inside:

```text
src/assets/
```

For example:

```text
src/assets/
├── icon.png
├── images/
└── fonts/
```

## Documentation

For more information, see the official Flet documentation:

https://flet.dev/docs/