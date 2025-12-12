import flet as ft
from models import (
    obtener_categorias,
    obtener_transacciones,
    crear_transaccion,
    eliminar_transaccion,
)
from ui.components import (
    NumberField,
    DateField,
    InputField,
    ConfirmDialog,
    SectionTitle,
)
from validators import validar_transaccion


class IngresosScreen(ft.UserControl):
    """
    Pantalla de gestión de ingresos:
    - Registrar ingresos
    - Validación de campos
    - DataTable con ingresos
    - Eliminar ingresos
    """

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

        # Campos del formulario
        self.campo_monto = NumberField("Monto del ingreso")
        self.campo_fecha = DateField("Fecha del ingreso")
        self.campo_desc = InputField("Descripción", multiline=False)

        # Dropdown de categorías
        self.dropdown_categoria = ft.Dropdown(label="Categoría")

        # Tabla de ingresos
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Fecha")),
                ft.DataColumn(ft.Text("Monto")),
                ft.DataColumn(ft.Text("Descripción")),
                ft.DataColumn(ft.Text("Categoría")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[],
        )

    # ---------------------------------------------------------
    # Al montar la pantalla
    # ---------------------------------------------------------
    def did_mount(self):
        self.cargar_categorias()
        self.cargar_tabla()

    # ---------------------------------------------------------
    # Cargar categorías en el dropdown
    # ---------------------------------------------------------
    def cargar_categorias(self):
        categorias = obtener_categorias()

        self.dropdown_categoria.options = [
            ft.dropdown.Option(str(c.id), c.nombre) for c in categorias
        ]

        self.dropdown_categoria.update()

    # ---------------------------------------------------------
    # Registrar ingreso
    # ---------------------------------------------------------
    def registrar_ingreso(self, e):
        monto = self.campo_monto.get_value()
        fecha = self.campo_fecha.get_value()
        descripcion = self.campo_desc.get_value()
        categoria_id = self.dropdown_categoria.value

        ok, msg = validar_transaccion(monto, fecha, descripcion, categoria_id)
        if not ok:
            self.page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor="red")
            self.page.snack_bar.open = True
            self.page.update()
            return

        crear_transaccion(
            tipo="ingreso",
            monto=float(monto),
            fecha=fecha,
            descripcion=descripcion,
            categoria_id=int(categoria_id),
        )

        self.page.snack_bar = ft.SnackBar(ft.Text("Ingreso registrado"), bgcolor="green")
        self.page.snack_bar.open = True
        self.page.update()

        self.cargar_tabla()

    # ---------------------------------------------------------
    # Cargar tabla de ingresos
    # ---------------------------------------------------------
    def cargar_tabla(self):
        ingresos = [
            t for t in obtener_transacciones() if t.tipo == "ingreso"
        ]

        self.tabla.rows = []

        for t in ingresos:
            self.tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(t.fecha)),
                        ft.DataCell(ft.Text(f"${t.monto}")),
                        ft.DataCell(ft.Text(t.descripcion)),
                        ft.DataCell(ft.Text(t.categoria_nombre or "—")),
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                icon_color="red",
                                on_click=lambda e, trans_id=t.id: self.confirmar_eliminar(trans_id),
                            )
                        ),
                    ]
                )
            )

        self.tabla.update()

    # ---------------------------------------------------------
    # Confirmar eliminación
    # ---------------------------------------------------------
    def confirmar_eliminar(self, trans_id):
        dialog = ConfirmDialog(
            title="Eliminar ingreso",
            message="¿Seguro que deseas eliminar este ingreso?",
            on_confirm=lambda: self.eliminar_ingreso(trans_id),
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    # ---------------------------------------------------------
    # Eliminar ingreso
    # ---------------------------------------------------------
    def eliminar_ingreso(self, trans_id):
        eliminar_transaccion(trans_id)
        self.cargar_tabla()

        self.page.snack_bar = ft.SnackBar(ft.Text("Ingreso eliminado"), bgcolor="orange")
        self.page.snack_bar.open = True
        self.page.update()

    # ---------------------------------------------------------
    # Render principal
    # ---------------------------------------------------------
    def build(self):
        return ft.Column(
            [
                SectionTitle("Gestión de Ingresos"),

                ft.Text("Registrar nuevo ingreso", size=18, weight="bold"),
                self.campo_monto,
                self.campo_fecha,
                self.campo_desc,
                self.dropdown_categoria,

                ft.ElevatedButton(
                    "Registrar ingreso",
                    icon=ft.icons.ADD,
                    on_click=self.registrar_ingreso,
                ),

                ft.Divider(),

                ft.Text("Historial de ingresos", size=18, weight="bold"),
                self.tabla,
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
