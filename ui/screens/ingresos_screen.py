import flet as ft
from models import (
    obtener_categorias,
    crear_transaccion,
    eliminar_transaccion,
    obtener_transacciones,
)
from ui.components import (
    DateField,
    NumberField,
    InputField,
    SectionTitle,
    ConfirmDialog,
)
from validators import validar_transaccion
from reports import exportar_transacciones_excel, exportar_transacciones_pdf
import tempfile
import os


class IngresosScreen(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

        # FORMULARIO
        self.fecha = DateField("Fecha del ingreso", page=self.page)
        self.descripcion = InputField("Descripción")
        self.monto = NumberField("Monto")
        self.dropdown_categoria = ft.Dropdown(
            label="Categoría",
            width=300,
            border_radius=8,
        )

        self.btn_guardar = ft.ElevatedButton(
            text="Registrar ingreso",
            icon=ft.icons.ADD,
            style=ft.ButtonStyle(
                bgcolor=ft.colors.GREEN,
                color=ft.colors.WHITE,
                padding=15,
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
            on_click=self.confirmar_guardar,
        )

        # EXPORTACIÓN
        self.btn_exportar_excel = ft.ElevatedButton(
            text="Exportar Excel",
            icon=ft.icons.TABLE_VIEW,
            style=ft.ButtonStyle(
                bgcolor=ft.colors.BLUE_600,
                color=ft.colors.WHITE,
                padding=12,
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
            on_click=self.exportar_excel,
        )

        self.btn_exportar_pdf = ft.ElevatedButton(
            text="Exportar PDF",
            icon=ft.icons.PICTURE_AS_PDF,
            style=ft.ButtonStyle(
                bgcolor=ft.colors.RED_600,
                color=ft.colors.WHITE,
                padding=12,
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
            on_click=self.exportar_pdf,
        )

        # TABLA
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Fecha")),
                ft.DataColumn(ft.Text("Descripción")),
                ft.DataColumn(ft.Text("Monto")),
                ft.DataColumn(ft.Text("Categoría")),
                ft.DataColumn(ft.Text("Eliminar")),
            ],
            rows=[],
            heading_row_color=ft.colors.with_opacity(0.1, ft.colors.BLUE_100),
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=8,
        )

    # ---------------------------------------------------------
    # SE EJECUTA AUTOMÁTICAMENTE AL MONTAR EL CONTROL
    # ---------------------------------------------------------
    def did_mount(self):
        self.cargar_categorias()
        self.cargar_tabla()

    # ---------------------------------------------------------
    # UI PRINCIPAL
    # ---------------------------------------------------------
    def build(self):
        return ft.Column(
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            controls=[
                SectionTitle("Gestión de Ingresos"),

                ft.Container(
                    padding=20,
                    bgcolor=ft.colors.with_opacity(0.05, ft.colors.BLUE_100),
                    border_radius=12,
                    content=ft.Column(
                        [
                            ft.Text("Registrar nuevo ingreso", size=18, weight="bold"),
                            self.fecha,
                            self.descripcion,
                            self.monto,
                            self.dropdown_categoria,
                            self.btn_guardar,
                        ],
                        spacing=15,
                    ),
                ),

                ft.Divider(),

                ft.Text("Historial de ingresos", size=18, weight="bold"),
                self.tabla,

                ft.Row(
                    [
                        self.btn_exportar_excel,
                        self.btn_exportar_pdf,
                    ],
                    spacing=20,
                ),
            ],
        )

    # ---------------------------------------------------------
    # Cargar categorías
    # ---------------------------------------------------------
    def cargar_categorias(self):
        categorias = obtener_categorias()
        self.dropdown_categoria.options = [
            ft.dropdown.Option(str(c.id), c.nombre) for c in categorias
        ]

        if categorias:
            self.dropdown_categoria.value = str(categorias[0].id)

        self.update()

    # ---------------------------------------------------------
    # Confirmar antes de guardar
    # ---------------------------------------------------------
    def confirmar_guardar(self, e):
        dialogo = ConfirmDialog(
            mensaje="¿Desea registrar este ingreso?",
            on_confirm=self.guardar_ingreso,
        )
        self.page.dialog = dialogo
        dialogo.open = True
        self.page.update()

    # ---------------------------------------------------------
    # Guardar ingreso
    # ---------------------------------------------------------
    def guardar_ingreso(self):
        fecha = self.fecha.get_value()
        descripcion = self.descripcion.get_value()
        monto = self.monto.get_value()
        tipo = "ingreso"
        categoria_id = self.dropdown_categoria.value

        ok, msg = validar_transaccion(fecha, descripcion, monto, tipo, categoria_id)
        if not ok:
            self._snack(msg, "red")
            return

        crear_transaccion(
            tipo=tipo,
            monto=float(monto),
            fecha=fecha,
            descripcion=descripcion,
            categoria_id=int(categoria_id),
        )

        self._snack("Ingreso registrado.", "green")
        self.cargar_tabla()

    # ---------------------------------------------------------
    # Cargar tabla
    # ---------------------------------------------------------
    def cargar_tabla(self):
        ingresos = [t for t in obtener_transacciones() if t.tipo == "ingreso"]

        self.tabla.rows = []

        for t in ingresos:
            btn_eliminar = ft.IconButton(
                icon=ft.icons.DELETE,
                tooltip="Eliminar",
                icon_color="red",
                data=t.id,
                on_click=self.confirmar_eliminar,
            )

            self.tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(t.fecha)),
                        ft.DataCell(ft.Text(t.descripcion)),
                        ft.DataCell(ft.Text(f"${t.monto:,.0f}")),
                        ft.DataCell(ft.Text(t.categoria_nombre or "—")),
                        ft.DataCell(btn_eliminar),
                    ]
                )
            )

        self.update()

    # ---------------------------------------------------------
    # Confirmar eliminación
    # ---------------------------------------------------------
    def confirmar_eliminar(self, e):
        trans_id = e.control.data

        dialogo = ConfirmDialog(
            mensaje="¿Desea eliminar este ingreso?",
            on_confirm=lambda: self.eliminar(trans_id),
        )
        self.page.dialog = dialogo
        dialogo.open = True
        self.page.update()

    def eliminar(self, trans_id: int):
        eliminar_transaccion(trans_id)
        self._snack("Ingreso eliminado.", "orange")
        self.cargar_tabla()

    # ---------------------------------------------------------
    # Exportar Excel
    # ---------------------------------------------------------
    def exportar_excel(self, e):
        ruta = os.path.join(tempfile.gettempdir(), "ingresos.xlsx")
        exportar_transacciones_excel(ruta)
        self.page.launch_url(ruta)

    # ---------------------------------------------------------
    # Exportar PDF
    # ---------------------------------------------------------
    def exportar_pdf(self, e):
        ruta = os.path.join(tempfile.gettempdir(), "ingresos.pdf")
        exportar_transacciones_pdf(ruta)
        self.page.launch_url(ruta)

    # ---------------------------------------------------------
    # Snackbar
    # ---------------------------------------------------------
    def _snack(self, mensaje, color):
        self.page.snack_bar = ft.SnackBar(
            ft.Text(mensaje),
            bgcolor=color,
            duration=2000,
        )
        self.page.snack_bar.open = True
        self.page.update()
