# ui/screens/transacciones_screen.py
import flet as ft
from models import (
    obtener_transacciones,
    obtener_categorias,
    eliminar_transaccion,
)
from ui.components import (
    DateField,
    InputField,
    SectionTitle,
    ConfirmDialog,
)
from validators import validar_fecha


class TransaccionesScreen(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

        # -----------------------------
        # FILTROS
        # -----------------------------
        self.filtro_descripcion = InputField("Buscar descripción")
        self.filtro_categoria = ft.Dropdown(label="Categoría")
        self.filtro_tipo = ft.Dropdown(
            label="Tipo",
            options=[
                ft.dropdown.Option("ingreso"),
                ft.dropdown.Option("gasto"),
            ],
        )

        self.filtro_fecha_desde = DateField("Fecha desde")
        self.filtro_fecha_hasta = DateField("Fecha hasta")

        self.btn_filtrar = ft.ElevatedButton(
            "Aplicar filtros",
            icon=ft.icons.SEARCH,
            on_click=self.aplicar_filtros,
        )

        # -----------------------------
        # TABLA
        # -----------------------------
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Fecha")),
                ft.DataColumn(ft.Text("Tipo")),
                ft.DataColumn(ft.Text("Monto")),
                ft.DataColumn(ft.Text("Categoría")),
                ft.DataColumn(ft.Text("Descripción")),
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
        self.filtro_categoria.options = [
            ft.dropdown.Option(str(c.id), c.nombre) for c in categorias
        ]
        self.filtro_categoria.options.insert(0, ft.dropdown.Option("", "Todas"))
        self.filtro_categoria.update()

    # ---------------------------------------------------------
    # Cargar tabla sin filtros
    # ---------------------------------------------------------
    def cargar_tabla(self):
        trans = obtener_transacciones()
        self._poblar_tabla(trans)

    # ---------------------------------------------------------
    # Aplicar filtros
    # ---------------------------------------------------------
    def aplicar_filtros(self, e):
        trans = obtener_transacciones()

        # Filtro descripción
        desc = self.filtro_descripcion.get_value()
        if desc:
            trans = [t for t in trans if desc.lower() in t.descripcion.lower()]

        # Filtro tipo
        if self.filtro_tipo.value:
            trans = [t for t in trans if t.tipo == self.filtro_tipo.value]

        # Filtro categoría
        if self.filtro_categoria.value:
            cat_id = int(self.filtro_categoria.value)
            trans = [t for t in trans if t.categoria_id == cat_id]

        # Filtro fecha desde
        fecha_desde = self.filtro_fecha_desde.get_value()
        if fecha_desde:
            ok, _ = validar_fecha(fecha_desde)
            if ok:
                trans = [t for t in trans if t.fecha >= fecha_desde]

        # Filtro fecha hasta
        fecha_hasta = self.filtro_fecha_hasta.get_value()
        if fecha_hasta:
            ok, _ = validar_fecha(fecha_hasta)
            if ok:
                trans = [t for t in trans if t.fecha <= fecha_hasta]

        self._poblar_tabla(trans)

    # ---------------------------------------------------------
    # Poblar tabla
    # ---------------------------------------------------------
    def _poblar_tabla(self, trans):
        self.tabla.rows = []

        for t in trans:
            btn_eliminar = ft.IconButton(
                icon=ft.icons.DELETE,
                icon_color="red",
                tooltip="Eliminar",
                on_click=lambda e, trans_id=t.id: self.confirmar_eliminar(trans_id),
            )

            self.tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(t.fecha)),
                        ft.DataCell(ft.Text(t.tipo)),
                        ft.DataCell(ft.Text(f"${t.monto:.0f}")),
                        ft.DataCell(ft.Text(t.categoria_nombre or "—")),
                        ft.DataCell(ft.Text(t.descripcion)),
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
            mensaje="¿Desea eliminar esta transacción?",
            on_confirm=lambda: self.eliminar(trans_id),
        )
        self.page.dialog = dialogo
        dialogo.open = True
        self.page.update()

    def eliminar(self, trans_id: int):
        eliminar_transaccion(trans_id)

        self.page.snack_bar = ft.SnackBar(ft.Text("Transacción eliminada."), bgcolor="orange")
        self.page.snack_bar.open = True
        self.page.update()

        self.cargar_tabla()

    # ---------------------------------------------------------
    # Render principal
    # ---------------------------------------------------------
    def build(self):
        return ft.Column(
            [
                SectionTitle("Historial de Transacciones"),

                ft.Text("Filtros", size=18, weight="bold"),
                ft.Row([self.filtro_descripcion, self.filtro_tipo]),
                ft.Row([self.filtro_categoria]),
                ft.Row([self.filtro_fecha_desde, self.filtro_fecha_hasta]),
                self.btn_filtrar,

                ft.Divider(),

                ft.Text("Resultados", size=18, weight="bold"),
                self.tabla,
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
