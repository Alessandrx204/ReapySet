# CustomTkinter GUI

A minimal CustomTkinter desktop GUI generated with **ReapySet**.

## Getting Started

Run the application from the project directory:

```bash
python main.py
```

If you are using `uv`:

```bash
uv run python main.py
```

## Project Structure

```text
.
├── main.py
├── app.py
└── README.md
```

- `main.py` — Application entry point.
- `app.py` — Main application window and user interface.
- `../../../../../../README.md` — Project documentation.

## Appearance

The starter application follows the operating system appearance mode:

```python
ctk.set_appearance_mode("system")
```

You can also force a specific mode:

```python
ctk.set_appearance_mode("dark")
```

or:

```python
ctk.set_appearance_mode("light")
```

The default color theme can be changed with:

```python
ctk.set_default_color_theme("blue")
```

Available built-in themes include `blue`, `green`, and `dark-blue`.

## Adding Widgets

CustomTkinter widgets can be added to the main application window or to frames:

```python
button = ctk.CTkButton(
    parent,
    text="Click me",
    command=callback,
)
```

## Documentation

For more information, see the official CustomTkinter documentation:

https://customtkinter.tomschimansky.com/