# Tkinter App

A minimal Tkinter desktop GUI generated with **ReapySet**.

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

## Tkinter and ttk

Tkinter is Python's standard graphical user interface toolkit.

This starter project uses `ttk` widgets where possible:

```python
import tkinter as tk
from tkinter import ttk
```

The main application window is created with:

```python
class App(tk.Tk):
    ...
```

while interface components use themed `ttk` widgets such as:

```python
ttk.Frame
ttk.Label
ttk.Entry
ttk.Button
```

`ttk` widgets use the native Tk theme available on the operating system.

## Adding Widgets

Create widgets and attach them to the application window or to a frame:

```python
button = ttk.Button(
    parent,
    text="Click me",
    command=callback,
)
```

Widgets can be positioned using Tkinter geometry managers such as:

```python
.grid()
.pack()
.place()
```

This starter project uses `grid()` to provide a resizable layout.

## CustomTkinter

Tkinter and CustomTkinter use a similar event-driven architecture, but they are different toolkits.

Tkinter provides the standard Python GUI components:

```python
ttk.Button(...)
ttk.Entry(...)
ttk.Label(...)
```

CustomTkinter provides styled replacements with additional appearance and theme features:

```python
ctk.CTkButton(...)
ctk.CTkEntry(...)
ctk.CTkLabel(...)
```

Use the CustomTkinter template in ReapySet if you want built-in dark/light appearance modes and more modern styled widgets.

## Documentation

For more information, see the official Python Tkinter documentation:

https://docs.python.org/3/library/tkinter.html