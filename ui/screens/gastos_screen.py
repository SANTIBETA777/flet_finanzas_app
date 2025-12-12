# ui/screens/gastos_screen.py
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


class GastosScreen(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

        # Campos del formulario
        self.fecha = DateField("Fecha del gasto")
        self.descripcion = InputField("Descripción")
        self.monto = NumberField("Monto")
        self.dropdown_categoria = ft.Dropdown(label="Categoría")

        # Botón guardar
        self.btn_guardar = ft.ElevatedButton(
            text="Registrar gasto",
            icon=ft.icons.ADD,
            on_click=self.guardar_gasto,
        )

        # Tabla de gastos
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Fecha")),
                ft.DataColumn(ft.Text("Descripción")),
                ft.DataColumn(ft.Text("Monto")),
                ft.DataColumn(ft.Text("Categoría")),
                ft.DataColumn(ft.Text("Eliminar")),
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
    # Cargar categorías en dropdown
    # ---------------------------------------------------------
    def cargar_categorias(self):
        categorias = obtener_categorias()
        self.dropdown_categoria.options = [
            ft.dropdown.Option(str(c.id), c.nombre) for c in categorias
        ]
        self.dropdown_categoria.update()

    # ---------------------------------------------------------
    # Guardar gasto
    # ---------------------------------------------------------
    def guardar_gasto(self, e):
        fecha = self.fecha.get_value()
        descripcion = self.descripcion.get_value()
        monto = self.monto.get_value()
        tipo = "gasto"
        categoria_id = self.dropdown_categoria.value

        ok, msg = validar_transaccion(fecha, descripcion, monto, tipo, categoria_id)
        if not ok:
            self.page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor="red")
            self.page.snack_bar.open = True
            self.page.update()
            return

        crear_transaccion(
            tipo=tipo,
            monto=float(monto),
            fecha=fecha,
            descripcion=descripcion,
            categoria_id=int(categoria_id),
        )

        self.page.snack_bar = ft.SnackBar(ft.Text("Gasto registrado."), bgcolor="green")
        self.page.snack_bar.open = True
        self.page.update()

        self.cargar_tabla()

    # ---------------------------------------------------------
    # Cargar tabla de gastos
    # ---------------------------------------------------------
    def cargar_tabla(self):
        gastos = [t for t in obtener_transacciones() if t.tipo == "gasto"]

        self.tabla.rows = []

        for t in gastos:
            btn_eliminar = ft.IconButton(
                icon=ft.icons.DELETE,
                tooltip="Eliminar",
                icon_color="red",
                on_click=lambda e, trans_id=t.id: self.confirmar_eliminar(trans_id),
            )

            self.tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(t.fecha)),
                        ft.DataCell(ft.Text(t.descripcion)),
                        ft.DataCell(ft.Text(f"${t.monto:.0f}")),
                        ft.DataCell(ft.Text(t.categoria_nombre or "—")),
                        ft.DataCell(btn_eliminar),
                    ]
                )
            )

        self.tabla.update()

    # ---------------------------------------------------------
    # Confirmar eliminación
    # ---------------------------------------------------------
    def confirmar_eliminar(self, trans_id: int):
        dialogo = ConfirmDialog(
            mensaje="¿Desea eliminar este gasto?",
            on_confirm=lambda: self.eliminar(trans_id),
        )
        self.page.dialog = dialogo
        dialogo.open = True
        self.page.update()

    def eliminar(self, trans_id: int):
        eliminar_transaccion(trans_id)
        self.page.snack_bar = ft.SnackBar(ft.Text("Gasto eliminado."), bgcolor="orange")
        self.page.snack_bar.open = True
        self.page.update()
        self.cargar_tabla()

    # ---------------------------------------------------------
    # Render principal
    # ---------------------------------------------------------
    def build(self):
        return ft.Column(
            [
                SectionTitle("Gestión de Gastos"),

                ft.Text("Registrar nuevo gasto", size=18, weight="bold"),
                self.fecha,
                self.descripcion,
                self.monto,
                self.dropdown_categoria,
                self.btn_guardar,

                ft.Divider(),

                ft.Text("Historial de gastos", size=18, weight="bold"),
                self.tabla,
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
