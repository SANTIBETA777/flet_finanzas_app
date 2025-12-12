import flet as ft

from ui.screens.dashboard_screen import DashboardScreen
from ui.screens.ingresos_screen import IngresosScreen
from ui.screens.gastos_screen import GastosScreen
from ui.screens.categorias_screen import CategoriasScreen
from ui.screens.alertas_screen import AlertasScreen


class Screens(ft.UserControl):
    """
    Controlador principal de navegación.
    Compatible con Flet 0.25.2 (sin ThemeMode ni Theme).
    """

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

        # Contenedor donde se cargan las pantallas
        self.content = ft.Container(expand=True)

        # Drawer de navegación
        self.drawer = ft.NavigationDrawer(
            controls=[
                ft.NavigationDrawerDestination(
                    label="Dashboard",
                    icon=ft.icons.DASHBOARD,
                ),
                ft.NavigationDrawerDestination(
                    label="Ingresos",
                    icon=ft.icons.TRENDING_UP,
                ),
                ft.NavigationDrawerDestination(
                    label="Gastos",
                    icon=ft.icons.TRENDING_DOWN,
                ),
                ft.NavigationDrawerDestination(
                    label="Categorías",
                    icon=ft.icons.CATEGORY,
                ),
                ft.NavigationDrawerDestination(
                    label="Alertas",
                    icon=ft.icons.WARNING,
                ),
                ft.Divider(),
                ft.NavigationDrawerDestination(
                    label="Cambiar tema",
                    icon=ft.icons.BRIGHTNESS_6,
                ),
            ],
            on_change=self._on_drawer_change,
        )

        # AppBar superior con botón de menú
        self.appbar = ft.AppBar(
            title=ft.Text("Finanzas App"),
            leading=ft.IconButton(
                icon=ft.icons.MENU,
                on_click=self._toggle_drawer,
            ),
        )

        # Asignar AppBar directamente a la página (no dentro de Column)
        self.page.appbar = self.appbar

        # Asignar Drawer directamente a la página
        self.page.drawer = self.drawer

        # Layout principal
        self.layout = ft.Column(
            [
                self.content,
            ],
            expand=True,
        )

        # Cargar pantalla inicial
        self._cargar_pantalla("Dashboard")

    # ---------------------------------------------------------
    # Drawer: abrir/cerrar
    # ---------------------------------------------------------
    def _toggle_drawer(self, e):
        self.drawer.open = True
        self.page.update()

    # ---------------------------------------------------------
    # Drawer: manejar selección
    # ---------------------------------------------------------
    def _on_drawer_change(self, e):
        index = e.control.selected_index

        opciones = [
            "Dashboard",
            "Ingresos",
            "Gastos",
            "Categorías",
            "Alertas",
            "Tema",
        ]

        if index is None:
            return

        seleccion = opciones[index]

        if seleccion == "Tema":
            self._cambiar_tema()
        else:
            self._cargar_pantalla(seleccion)

        self.drawer.open = False
        self.page.update()

    # ---------------------------------------------------------
    # Cambiar tema (desactivado en esta versión)
    # ---------------------------------------------------------
    def _cambiar_tema(self):
        # Flet 0.25.2 no soporta ThemeMode, así que esta función queda vacía
        pass

    # ---------------------------------------------------------
    # Cargar pantallas por nombre
    # ---------------------------------------------------------
    def _cargar_pantalla(self, nombre: str):
        if nombre == "Dashboard":
            self.content.content = DashboardScreen(self.page)

        elif nombre == "Ingresos":
            self.content.content = IngresosScreen(self.page)

        elif nombre == "Gastos":
            self.content.content = GastosScreen(self.page)

        elif nombre == "Categorías":
            self.content.content = CategoriasScreen(self.page)

        elif nombre == "Alertas":
            self.content.content = AlertasScreen(self.page)

        self.update()

    # ---------------------------------------------------------
    # Render principal
    # ---------------------------------------------------------
    def build(self):
        return self.layout
