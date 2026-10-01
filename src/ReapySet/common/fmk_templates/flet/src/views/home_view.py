import flet as ft


class HomeView(ft.Container):

    def __init__(self) -> None:
        self.message = ft.Text(
            "Welcome to your Flet application.",
            size=18,
        )

        super().__init__(
            expand=True,
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.Text(
                        "Flet App",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                    ),
                    self.message,
                    ft.Button(
                        content="Get started",
                        icon=ft.Icons.ROCKET_LAUNCH,
                        on_click=self._on_get_started,
                    ),
                ],
            ),
        )

    def _on_get_started(self, _) -> None:
        self.message.value = "Your Flet project is ready."