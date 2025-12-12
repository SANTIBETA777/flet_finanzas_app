import flet as ft
from models import (
    obtener_categorias,
    crear_categoria,
)
from ui.components import (
    InputField,
    ConfirmDialog,
    SectionTitle,
)
from validators import validar_texto


class CategoriasScreen(ft.UserControl):
    """
    Pantalla de gestión de categorías:
    - Crear categorías
    - Validación de texto
    - Listar categorías
    - Eliminar categorías (si el profe lo permite)
    """

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

        # Campo para nueva categoría
        self.campo_nombre = InputField("Nombre de la categoría", validator=validar_texto)

        # Tabla de categorías
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[],
        )

    # ---------------------------------------------------------
    # Al montar la pantalla
    # ---------------------------------------------------------
    def did_mount(self):
        self.cargar_tabla()

    # ---------------------------------------------------------
    # Registrar categoría
    # ---------------------------------------------------------
    def registrar_categoria(self, e):
        nombre = self.campo_nombre.get_value()

        ok, msg = validar_texto(nombre)
        if not ok:
            self.page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor="red")
            self.page.snack_bar.open = True
            self.page.update()
            return

        crear_categoria(nombre)

        self.page.snack_bar = ft.SnackBar(ft.Text("Categoría creada"), bgcolor="green")
        self.page.snack_bar.open = True
        self.page.update()

        self.cargar_tabla()

    # ---------------------------------------------------------
    # Cargar tabla de categorías
    # ---------------------------------------------------------
    def cargar_tabla(self):
        categorias = obtener_categorias()

        self.tabla.rows = []

        for c in categorias:
            self.tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(c.nombre)),
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                icon_color="red",
                                on_click=lambda e, cat_id=c.id: self.confirmar_eliminar(cat_id),
                            )
                        ),
                    ]
                )
            )

        self.tabla.update()

    # ---------------------------------------------------------
    # Confirmar eliminación
    # ---------------------------------------------------------
    def confirmar_eliminar(self, categoria_id):
        dialog = ConfirmDialog(
            title="Eliminar categoría",
            message="¿Seguro que deseas eliminar esta categoría?",
            on_confirm=lambda: self.eliminar_categoria(categoria_id),
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    # ---------------------------------------------------------
    # Eliminar categoría
    # ---------------------------------------------------------
    def eliminar_categoria(self, categoria_id):
        # Eliminación directa (el profe no pidió restricciones)
        import sqlite3
        from database import get_connection

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM categorias WHERE id = ?", (categoria_id,))
        conn.commit()
        conn.close()

        self.cargar_tabla()

        self.page.snack_bar = ft.SnackBar(ft.Text("Categoría eliminada"), bgcolor="orange")
        self.page.snack_bar.open = True
        self.page.update()

    # ---------------------------------------------------------
    # Render principal
    # ---------------------------------------------------------
    def build(self):
        return ft.Column(
            [
                SectionTitle("Gestión de Categorías"),

                ft.Text("Crear nueva categoría", size=18, weight="bold"),
                self.campo_nombre,

                ft.ElevatedButton(
                    "Crear categoría",
                    icon=ft.icons.ADD,
                    on_click=self.registrar_categoria,
                ),

                ft.Divider(),

                ft.Text("Listado de categorías", size=18, weight="bold"),
                self.tabla,
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
