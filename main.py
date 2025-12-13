import flet as ft
from database import init_db

from ui.screens.dashboard_screen import DashboardScreen
from ui.screens.ingresos_screen import IngresosScreen
from ui.screens.gastos_screen import GastosScreen
from ui.screens.categorias_screen import CategoriasScreen
from ui.screens.transacciones_screen import TransaccionesScreen


def main(page: ft.Page):
    page.title = "Finanzas Personales"
    page.window.width = 1100
    page.window.height = 700
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO

    # Inicializar BD UNA SOLA VEZ
    init_db()

    # CONTENEDOR PRINCIPAL QUE SE ACTUALIZA
    contenido = ft.Column(expand=True)

    # ---------------------------------------------------------
    # Cambiar tema
    # ---------------------------------------------------------
    def cambiar_tema(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            switch_tema.label = "Tema claro"
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            switch_tema.label = "Tema oscuro"
        page.update()

    switch_tema = ft.Switch(
        label="Tema oscuro",
        value=False,
        on_change=cambiar_tema,
    )

    # ---------------------------------------------------------
    # Navegación entre pantallas
    # ---------------------------------------------------------
    def navegar(index: int):
        rutas = ["dashboard", "ingresos", "gastos", "categorias", "transacciones"]
        ruta = rutas[index]

        if ruta == "dashboard":
            pantalla = DashboardScreen(page)
        elif ruta == "ingresos":
            pantalla = IngresosScreen(page)
        elif ruta == "gastos":
            pantalla = GastosScreen(page)
        elif ruta == "categorias":
            pantalla = CategoriasScreen(page)
        elif ruta == "transacciones":
            pantalla = TransaccionesScreen(page)

        contenido.controls = [
            ft.Container(
                expand=True,
                padding=20,
                content=pantalla
            )
        ]
        contenido.update()

    # ---------------------------------------------------------
    # Menú lateral
    # ---------------------------------------------------------
    class MenuLateral(ft.Column):
        def __init__(self, page, navegar_callback):
            super().__init__(spacing=10, alignment=ft.MainAxisAlignment.START)
            self.page = page
            self.navegar = navegar_callback

            botones = [
                ("Dashboard", ft.icons.DASHBOARD),
                ("Ingresos", ft.icons.ADD_CHART),
                ("Gastos", ft.icons.REMOVE_CIRCLE_OUTLINE),
                ("Categorías", ft.icons.CATEGORY),
                ("Transacciones", ft.icons.LIST),
            ]

            self.controls = [
                self._crear_boton(i, texto, icono)
                for i, (texto, icono) in enumerate(botones)
            ]

        def _crear_boton(self, index, texto, icono):
            return ft.Container(
                padding=12,
                border_radius=8,
                ink=True,
                bgcolor=ft.colors.with_opacity(0.05, ft.colors.GREY_200),
                on_click=lambda e: self.navegar(index),
                content=ft.Row(
                    spacing=10,
                    controls=[
                        ft.Icon(icono, size=22),
                        ft.Text(texto, size=16),
                    ],
                ),
            )

    menu = MenuLateral(page, navegar)

    # ---------------------------------------------------------
    # LAYOUT GENERAL
    # ---------------------------------------------------------
    layout = ft.Row(
        expand=True,
        vertical_alignment=ft.CrossAxisAlignment.START,
        controls=[
            ft.Container(
                width=220,
                padding=10,
                bgcolor=ft.colors.with_opacity(0.03, ft.colors.GREY_300),
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.START,
                    spacing=20,
                    controls=[
                        switch_tema,
                        menu,
                    ],
                ),
            ),
            ft.Container(width=1, bgcolor=ft.colors.GREY_300),
            contenido,  # ESTE ES EL CONTENEDOR QUE SE ACTUALIZA
        ],
    )

    # PRIMERO AGREGAMOS EL LAYOUT A LA PÁGINA
    page.add(layout)

    # AHORA SÍ PODEMOS NAVEGAR
    navegar(0)


ft.app(target=main, view=ft.AppView.WEB_BROWSER)
