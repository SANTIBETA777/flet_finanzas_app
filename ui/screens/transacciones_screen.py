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


class TransaccionesScreen(ft.Column):
    def __init__(self, page: ft.Page):
        print(">>> TransaccionesScreen se está creando")
        super().__init__(scroll=ft.ScrollMode.AUTO, expand=True)
        self.page = page

        # -----------------------------
        # FILTROS PROFESIONALES
        # -----------------------------
        self.filtro_descripcion = InputField("Buscar descripción")
        self.filtro_categoria = ft.Dropdown(
            label="Categoría",
            width=250,
            border_radius=8,
        )
        self.filtro_tipo = ft.Dropdown(
            label="Tipo",
            width=200,
            border_radius=8,
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
            style=ft.ButtonStyle(
                bgcolor=ft.colors.BLUE,
                color=ft.colors.WHITE,
                padding=12,
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
            on_click=self.aplicar_filtros,
        )

        # -----------------------------
        # TABLA PROFESIONAL
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
            heading_row_color=ft.colors.with_opacity(0.1, ft.colors.BLUE_100),
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=8,
        )

        # -----------------------------
        # LAYOUT PRINCIPAL
        # -----------------------------
        self.controls = [
            SectionTitle("Historial de Transacciones"),

            ft.Container(
                padding=20,
                bgcolor=ft.colors.with_opacity(0.05, ft.colors.BLUE_100),
                border_radius=12,
                content=ft.Column(
                    [
                        ft.Text("Filtros", size=18, weight="bold"),

                        ft.Row(
                            [
                                self.filtro_descripcion,
                                self.filtro_tipo,
                            ],
                            spacing=20,
                        ),

                        ft.Row(
                            [
                                self.filtro_categoria,
                            ],
                            spacing=20,
                        ),

                        ft.Row(
                            [
                                self.filtro_fecha_desde,
                                self.filtro_fecha_hasta,
                            ],
                            spacing=20,
                        ),

                        self.btn_filtrar,
                    ],
                    spacing=15,
                ),
            ),

            ft.Divider(),

            ft.Text("Resultados", size=18, weight="bold"),
            self.tabla,
        ]

    # ---------------------------------------------------------
    # Se ejecuta cuando el control YA está en la página
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
                data=t.id,
                on_click=self.confirmar_eliminar,
            )

            self.tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(t.fecha)),
                        ft.DataCell(ft.Text(t.tipo)),
                        ft.DataCell(ft.Text(f"${t.monto:,.0f}")),
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
    def confirmar_eliminar(self, e):
        trans_id = e.control.data

        dialogo = ConfirmDialog(
            mensaje="¿Desea eliminar esta transacción?",
            on_confirm=lambda: self.eliminar(trans_id),
        )
        self.page.dialog = dialogo
        dialogo.open = True
        self.page.update()

    def eliminar(self, trans_id: int):
        eliminar_transaccion(trans_id)

        self.page.snack_bar = ft.SnackBar(
            ft.Text("Transacción eliminada."),
            bgcolor="orange",
            duration=2000,
        )
        self.page.snack_bar.open = True
        self.page.update()

        self.cargar_tabla()
