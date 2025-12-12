import flet as ft
from database import init_db

# Importar pantallas
from ui.screens.dashboard_screen import DashboardScreen
from ui.screens.ingresos_screen import IngresosScreen
from ui.screens.gastos_screen import GastosScreen
from ui.screens.categorias_screen import CategoriasScreen
from ui.screens.transacciones_screen import TransaccionesScreen


# ============================================================
#   APLICACIÓN PRINCIPAL
# ============================================================

def main(page: ft.Page):
    page.title = "Finanzas Personales"
    page.window.width = 1100
    page.window.height = 700
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO

    # Inicializar base de datos
    init_db()

    # Contenedor donde se cargan las pantallas
    contenido = ft.Container(expand=True)

    # ---------------------------------------------------------
    # Función para cambiar de pantalla
    # ---------------------------------------------------------
    def navegar(ruta):
        if ruta == "dashboard":
            contenido.content = DashboardScreen(page)
        elif ruta == "ingresos":
            contenido.content = IngresosScreen(page)
        elif ruta == "gastos":
            contenido.content = GastosScreen(page)
        elif ruta == "categorias":
            contenido.content = CategoriasScreen(page)
        elif ruta == "transacciones":
            contenido.content = TransaccionesScreen(page)

        page.update()

    # ---------------------------------------------------------
    # Menú lateral
    # ---------------------------------------------------------
    menu = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=80,
        min_extended_width=200,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.DASHBOARD,
                label="Dashboard",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.ADD_CHART,
                label="Ingresos",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.REMOVE_CIRCLE_OUTLINE,
                label="Gastos",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.CATEGORY,
                label="Categorías",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.LIST,
                label="Transacciones",
            ),
        ],
        on_change=lambda e: navegar(
            ["dashboard", "ingresos", "gastos", "categorias", "transacciones"][e.control.selected_index]
        ),
    )

    # Cargar pantalla inicial
    navegar("dashboard")

    # Layout principal con altura definida para NavigationRail
    page.add(
        ft.Row(
            [
                ft.Container(
                    content=menu,
                    height=page.window.height,
                ),
                ft.VerticalDivider(width=1),
                contenido,
            ],
            expand=True,
        )
    )


# Ejecutar app
ft.app(target=main)
