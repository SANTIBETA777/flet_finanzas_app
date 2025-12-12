import flet as ft
from database import init_db
from ui.screens import Screens


def main(page: ft.Page):
    # Inicializar base de datos
    init_db()

    page.title = "Finanzas App"
    page.window_width = 1100
    page.window_height = 700
    page.window_resizable = False

    # IMPORTANTE: permitir drawer
    page.drawer = None

    # Control principal de pantallas
    screens = Screens(page)
    page.add(screens)


if __name__ == "__main__":
    ft.app(target=main)
