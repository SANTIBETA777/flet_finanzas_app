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


class CategoriasScreen(ft.Column):
    def __init__(self, page: ft.Page):
        print(">>> CategoriasScreen se está creando")
        super().__init__(scroll=ft.ScrollMode.AUTO, expand=True)
        self.page = page

        # ID en edición (None = crear)
        self.editando_id = None

        # -----------------------------
        # FORMULARIO PROFESIONAL
        # -----------------------------
        self.campo_nombre = InputField("Nombre de la categoría")

        self.btn_guardar = ft.ElevatedButton(
            text="Guardar categoría",
            icon=ft.icons.SAVE,
            style=ft.ButtonStyle(
                bgcolor=ft.colors.BLUE,
                color=ft.colors.WHITE,
                padding=15,
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
            on_click=self.guardar_categoria,
        )

        self.btn_cancelar = ft.TextButton(
            text="Cancelar edición",
            icon=ft.icons.CANCEL,
            visible=False,
            on_click=self.cancelar_edicion,
        )

        # -----------------------------
        # TABLA PROFESIONAL
        # -----------------------------
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Editar")),
                ft.DataColumn(ft.Text("Eliminar")),
            ],
            rows=[],
            heading_row_color=ft.colors.with_opacity(0.1, ft.colors.BLUE_100),
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=8,
        )

        # -----------------------------
        # LAYOUT PRINCIPAL
        # -----------------------------
        self.controls = [
            SectionTitle("Gestión de Categorías"),

            ft.Container(
                padding=20,
                bgcolor=ft.colors.with_opacity(0.05, ft.colors.BLUE_100),
                border_radius=12,
                content=ft.Column(
                    [
                        ft.Text("Crear o editar categoría", size=18, weight="bold"),
                        self.campo_nombre,
                        ft.Row(
                            [
                                self.btn_guardar,
                                self.btn_cancelar,
                            ],
                            spacing=10,
                        ),
                    ],
                    spacing=15,
                ),
            ),

            ft.Divider(),

            ft.Text("Listado de categorías", size=18, weight="bold"),
            self.tabla,
        ]

    # ---------------------------------------------------------
    # Se ejecuta cuando el control YA está en la página
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
            self._snackbar(msg, "red")
            return

        if self.editando_id is None:
            crear_categoria(nombre)
            mensaje = "Categoría creada."
        else:
            editar_categoria(self.editando_id, nombre)
            mensaje = "Categoría actualizada."
            self.editando_id = None
            self._actualizar_estado_boton()

        self._snackbar(mensaje, "green")

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
                icon_color=ft.colors.BLUE,
                data=c,
                on_click=self.iniciar_edicion,
            )

            btn_eliminar = ft.IconButton(
                icon=ft.icons.DELETE,
                tooltip="Eliminar",
                icon_color=ft.colors.RED,
                data=c.id,
                on_click=self.confirmar_eliminar,
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
    # Iniciar edición
    # ---------------------------------------------------------
    def iniciar_edicion(self, e):
        categoria = e.control.data
        self.editando_id = categoria.id
        self.campo_nombre.set_value(categoria.nombre)
        self._actualizar_estado_boton()
        self.page.update()

    # ---------------------------------------------------------
    # Cancelar edición
    # ---------------------------------------------------------
    def cancelar_edicion(self, e):
        self.editando_id = None
        self.campo_nombre.set_value("")
        self._actualizar_estado_boton()
        self.page.update()

    def _actualizar_estado_boton(self):
        if self.editando_id is None:
            self.btn_guardar.text = "Guardar categoría"
            self.btn_guardar.icon = ft.icons.SAVE
            self.btn_guardar.style.bgcolor = ft.colors.BLUE
            self.btn_cancelar.visible = False
        else:
            self.btn_guardar.text = "Actualizar categoría"
            self.btn_guardar.icon = ft.icons.EDIT
            self.btn_guardar.style.bgcolor = ft.colors.ORANGE
            self.btn_cancelar.visible = True

    # ---------------------------------------------------------
    # Confirmar eliminación
    # ---------------------------------------------------------
    def confirmar_eliminar(self, e):
        cat_id = e.control.data
        dialogo = ConfirmDialog(
            mensaje="¿Desea eliminar esta categoría?",
            on_confirm=lambda: self.eliminar(cat_id),
        )
        self.page.dialog = dialogo
        dialogo.open = True
        self.page.update()

    def eliminar(self, cat_id: int):
        ok = eliminar_categoria(cat_id)

        if ok:
            self._snackbar("Categoría eliminada.", "orange")
        else:
            self._snackbar("No se puede eliminar: categoría en uso.", "red")

        self.cargar_tabla()

    # ---------------------------------------------------------
    # Snackbar profesional
    # ---------------------------------------------------------
    def _snackbar(self, mensaje, color):
        self.page.snack_bar = ft.SnackBar(
            ft.Text(mensaje),
            bgcolor=color,
            duration=2000,
        )
        self.page.snack_bar.open = True
        self.page.update()
