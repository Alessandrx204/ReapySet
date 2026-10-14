import customtkinter as ctk


ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):

    def __init__(self) -> None:
        super().__init__()

        self.title("CustomTkinter App Template")
        self.geometry("720x420")
        self.minsize(600, 360)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(
            self,
            corner_radius=12,
        )
        self.main_frame.grid(
            row=0,
            column=0,
            padx=24,
            pady=24,
            sticky="nsew",
        )

        self.main_frame.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="CustomTkinter App Template",
            font=ctk.CTkFont(
                size=28,
                weight="bold",
            ),
        )
        self.title_label.grid(
            row=0,
            column=0,
            padx=24,
            pady=(32, 8),
        )

        self.description_label = ctk.CTkLabel(
            self.main_frame,
            text="A CustomTkinter GUI generated with ReapySet.",
        )
        self.description_label.grid(
            row=1,
            column=0,
            padx=24,
            pady=(0, 24),
        )

        self.name_entry = ctk.CTkEntry(
            self.main_frame,
            width=280,
            placeholder_text="Enter your name",
        )
        self.name_entry.grid(
            row=2,
            column=0,
            padx=24,
            pady=8,
        )

        self.submit_button = ctk.CTkButton(
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

        self.message_label = ctk.CTkLabel(
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

        if name:
            self.message_label.configure(
                text=f"Hello, {name}!"
            )
        else:
            self.message_label.configure(
                text="Please enter your name."
            )