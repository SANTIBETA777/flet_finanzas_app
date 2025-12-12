# ui/screens/categorias_screen.py
import flet as ft
from models import (
    obtener_categorias,
    crear_categoria,
    editar_categoria,
    eliminar_categoria,
)
from ui.components import (
    InputField,
    SectionTitle,
    ConfirmDialog,
)
from validators import validar_texto


class CategoriasScreen(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

        # Campo para crear/editar
        self.campo_nombre = InputField("Nombre de la categoría")

        # Botón guardar
        self.btn_guardar = ft.ElevatedButton(
            text="Guardar categoría",
            icon=ft.icons.SAVE,
            on_click=self.guardar_categoria,
        )

        # Tabla de categorías
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Editar")),
                ft.DataColumn(ft.Text("Eliminar")),
            ],
            rows=[],
        )

        # ID en edición (None = crear)
        self.editando_id = None

    # ---------------------------------------------------------
    # Al montar la pantalla
    # ---------------------------------------------------------
    def did_mount(self):
        self.cargar_tabla()

    # ---------------------------------------------------------
    # Guardar categoría (crear o editar)
    # ---------------------------------------------------------
    def guardar_categoria(self, e):
        nombre = self.campo_nombre.get_value()

        ok, msg = validar_texto(nombre)
        if not ok:
            self.page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor="red")
            self.page.snack_bar.open = True
            self.page.update()
            return

        if self.editando_id is None:
            # Crear
            crear_categoria(nombre)
            mensaje = "Categoría creada."
        else:
            # Editar
            editar_categoria(self.editando_id, nombre)
            mensaje = "Categoría actualizada."
            self.editando_id = None
            self.btn_guardar.text = "Guardar categoría"

        self.page.snack_bar = ft.SnackBar(ft.Text(mensaje), bgcolor="green")
        self.page.snack_bar.open = True
        self.page.update()

        self.campo_nombre.set_value("")
        self.cargar_tabla()

    # ---------------------------------------------------------
    # Cargar tabla
    # ---------------------------------------------------------
    def cargar_tabla(self):
        categorias = obtener_categorias()
        self.tabla.rows = []

        for c in categorias:
            btn_editar = ft.IconButton(
                icon=ft.icons.EDIT,
                tooltip="Editar",
                icon_color="blue",
                on_click=lambda e, cat=c: self.editar(cat),
            )

            btn_eliminar = ft.IconButton(
                icon=ft.icons.DELETE,
                tooltip="Eliminar",
                icon_color="red",
                on_click=lambda e, cat=c: self.confirmar_eliminar(cat.id),
            )

            self.tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(c.id))),
                        ft.DataCell(ft.Text(c.nombre)),
                        ft.DataCell(btn_editar),
                        ft.DataCell(btn_eliminar),
                    ]
                )
            )

        self.tabla.update()

    # ---------------------------------------------------------
    # Editar categoría
    # ---------------------------------------------------------
    def editar(self, categoria):
        self.editando_id = categoria.id
        self.campo_nombre.set_value(categoria.nombre)
        self.btn_guardar.text = "Actualizar categoría"
        self.update()

    # ---------------------------------------------------------
    # Confirmar eliminación
    # ---------------------------------------------------------
    def confirmar_eliminar(self, cat_id: int):
        dialogo = ConfirmDialog(
            mensaje="¿Desea eliminar esta categoría?",
            on_confirm=lambda: self.eliminar(cat_id),
        )
        self.page.dialog = dialogo
        dialogo.open = True
        self.page.update()

    def eliminar(self, cat_id: int):
        eliminar_categoria(cat_id)

        self.page.snack_bar = ft.SnackBar(ft.Text("Categoría eliminada."), bgcolor="orange")
        self.page.snack_bar.open = True
        self.page.update()

        self.cargar_tabla()

    # ---------------------------------------------------------
    # Render principal
    # ---------------------------------------------------------
    def build(self):
        return ft.Column(
            [
                SectionTitle("Gestión de Categorías"),

                ft.Text("Crear o editar categoría", size=18, weight="bold"),
                self.campo_nombre,
                self.btn_guardar,

                ft.Divider(),

                ft.Text("Listado de categorías", size=18, weight="bold"),
                self.tabla,
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
