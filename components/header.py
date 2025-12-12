import flet as ft

class Header(ft.UserControl):
    def build(self):
        return ft.Container(
            bgcolor=ft.colors.BLUE_600,
            padding=20,
            content=ft.Text(
                "Finanzas Personales",
                size=22,
                color=ft.colors.WHITE,
                weight="bold"
            )
        )
