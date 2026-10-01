import flet as ft

from views.home_view import HomeView


def main(page: ft.Page) -> None:
    page.title = "Flet App"
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.padding = 0

    page.add(
        HomeView()
    )


if __name__ == "__main__":
    ft.run(main)