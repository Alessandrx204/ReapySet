import tkinter as tk
from tkinter import ttk


class App(tk.Tk):

    def __init__(self) -> None:
        super().__init__()

        self.title("Tkinter App Template")
        self.geometry("720x420")
        self.minsize(600, 360)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.main_frame = ttk.Frame(
            self,
            padding=24,
        )
        self.main_frame.grid(
            row=0,
            column=0,
            padx=24,
            pady=24,
            sticky="nsew",
        )

        self.main_frame.columnconfigure(0, weight=1)

        self.title_label = ttk.Label(
            self.main_frame,
            text="Tkinter App Template",
            font=("TkDefaultFont", 24, "bold"),
        )
        self.title_label.grid(
            row=0,
            column=0,
            padx=24,
            pady=(32, 8),
        )

        self.description_label = ttk.Label(
            self.main_frame,
            text="A Tkinter GUI generated with ReapySet.",
        )
        self.description_label.grid(
            row=1,
            column=0,
            padx=24,
            pady=(0, 24),
        )

        self.name_entry = ttk.Entry(
            self.main_frame,
            width=32,
        )
        self.name_entry.grid(
            row=2,
            column=0,
            padx=24,
            pady=8,
        )

        self.name_entry.insert(
            0,
            "Enter your name",
        )

        self.submit_button = ttk.Button(
            self.main_frame,
            text="Continue",
            command=self._on_submit,
        )
        self.submit_button.grid(
            row=3,
            column=0,
            padx=24,
            pady=8,
        )

        self.message_label = ttk.Label(
            self.main_frame,
            text="",
        )
        self.message_label.grid(
            row=4,
            column=0,
            padx=24,
            pady=(8, 24),
        )

    def _on_submit(self) -> None:
        name = self.name_entry.get().strip()

        if name and name != "Enter your name":
            self.message_label.configure(
                text=f"Hello, {name}!"
            )
        else:
            self.message_label.configure(
                text="Please enter your name."
            )