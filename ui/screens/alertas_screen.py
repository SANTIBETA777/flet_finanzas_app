import flet as ft
from datetime import datetime

from models import (
    obtener_categorias,
    obtener_presupuestos,
    guardar_presupuesto,
    obtener_transacciones,
    crear_alerta,
    obtener_alertas,
)
from ui.components import (
    NumberField,
    SectionTitle,
)
from validators import validar_monto


class AlertasScreen(ft.UserControl):
    """
    Pantalla de alertas y presupuestos:
    - Definir presupuesto por categoría
    - Ver consumo vs presupuesto
    - Generar alertas cuando se llega al 80% y 100%
    - Ver historial de alertas
    """

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

        # Dropdown de categorías
        self.dropdown_categoria = ft.Dropdown(label="Categoría")

        # Campo de presupuesto
        self.campo_presupuesto = NumberField("Presupuesto máximo para la categoría")

        # Tabla de presupuestos y consumo
        self.tabla_presupuestos = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Categoría")),
                ft.DataColumn(ft.Text("Presupuesto")),
                ft.DataColumn(ft.Text("Gastado")),
                ft.DataColumn(ft.Text("Porcentaje")),
                ft.DataColumn(ft.Text("Estado")),
            ],
            rows=[],
        )

        # Tabla de historial de alertas
        self.tabla_alertas = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Fecha")),
                ft.DataColumn(ft.Text("Categoría")),
                ft.DataColumn(ft.Text("Tipo")),
                ft.DataColumn(ft.Text("Mensaje")),
            ],
            rows=[],
        )

    # ---------------------------------------------------------
    # Al montar la pantalla
    # ---------------------------------------------------------
    def did_mount(self):
        self.cargar_categorias()
        self.cargar_presupuestos()
        self.cargar_alertas()

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
    # Guardar presupuesto
    # ---------------------------------------------------------
    def guardar_presu(self, e):
        categoria_id = self.dropdown_categoria.value
        monto = self.campo_presupuesto.get_value()

        if not categoria_id:
            self.page.snack_bar = ft.SnackBar(ft.Text("Debe seleccionar una categoría."), bgcolor="red")
            self.page.snack_bar.open = True
            self.page.update()
            return

        ok, msg = validar_monto(monto)
        if not ok:
            self.page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor="red")
            self.page.snack_bar.open = True
            self.page.update()
            return

        guardar_presupuesto(int(categoria_id), float(monto))

        self.page.snack_bar = ft.SnackBar(ft.Text("Presupuesto guardado."), bgcolor="green")
        self.page.snack_bar.open = True
        self.page.update()

        self.cargar_presupuestos()

    # ---------------------------------------------------------
    # Cargar tabla de presupuestos y consumo
    # ---------------------------------------------------------
    def cargar_presupuestos(self):
        categorias = {c.id: c.nombre for c in obtener_categorias()}
        presupuestos = obtener_presupuestos()
        trans = obtener_transacciones()

        # Calcular gastos por categoría
        gastos_por_categoria = {}
        for t in trans:
            if t.tipo == "gasto" and t.categoria_id:
                gastos_por_categoria.setdefault(t.categoria_id, 0)
                gastos_por_categoria[t.categoria_id] += t.monto

        self.tabla_presupuestos.rows = []

        for p in presupuestos:
            gastado = gastos_por_categoria.get(p.categoria_id, 0.0)
            porcentaje = (gastado / p.monto_maximo * 100) if p.monto_maximo > 0 else 0

            if porcentaje >= 100:
                estado = "Límite excedido"
                color = "red"
                tipo_alerta = "critical"
            elif porcentaje >= 80:
                estado = "Cerca del límite"
                color = "orange"
                tipo_alerta = "warning"
            else:
                estado = "Dentro del presupuesto"
                color = "green"
                tipo_alerta = None

            # Generar alerta si está en warning o critical
            if tipo_alerta is not None:
                mensaje = f"La categoría '{categorias.get(p.categoria_id, '')}' ha alcanzado el {porcentaje:.0f}% del presupuesto."
                fecha = datetime.now().strftime("%Y-%m-%d")
                crear_alerta(
                    categoria_id=p.categoria_id,
                    tipo=tipo_alerta,
                    mensaje=mensaje,
                    fecha=fecha,
                )

            self.tabla_presupuestos.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(categorias.get(p.categoria_id, "Desconocida"))),
                        ft.DataCell(ft.Text(f"${p.monto_maximo:.0f}")),
                        ft.DataCell(ft.Text(f"${gastado:.0f}")),
                        ft.DataCell(ft.Text(f"{porcentaje:.0f}%")),
                        ft.DataCell(ft.Text(estado, color=color)),
                    ]
                )
            )

        self.tabla_presupuestos.update()
        self.cargar_alertas()

    # ---------------------------------------------------------
    # Cargar historial de alertas
    # ---------------------------------------------------------
    def cargar_alertas(self):
        alertas = obtener_alertas()
        categorias = {c.id: c.nombre for c in obtener_categorias()}

        self.tabla_alertas.rows = []

        for a in alertas:
            nombre_cat = categorias.get(a.categoria_id, "General")
            color = "orange" if a.tipo == "warning" else "red"

            self.tabla_alertas.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(a.fecha)),
                        ft.DataCell(ft.Text(nombre_cat)),
                        ft.DataCell(ft.Text(a.tipo, color=color)),
                        ft.DataCell(ft.Text(a.mensaje)),
                    ]
                )
            )

        self.tabla_alertas.update()

    # ---------------------------------------------------------
    # Render principal
    # ---------------------------------------------------------
    def build(self):
        return ft.Column(
            [
                SectionTitle("Sistema de Alertas y Presupuestos"),

                ft.Text("Configurar presupuesto por categoría", size=18, weight="bold"),
                self.dropdown_categoria,
                self.campo_presupuesto,
                ft.ElevatedButton(
                    "Guardar presupuesto",
                    icon=ft.icons.SAVE,
                    on_click=self.guardar_presu,
                ),

                ft.Divider(),

                ft.Text("Presupuestos y consumo", size=18, weight="bold"),
                self.tabla_presupuestos,

                ft.Divider(),

                ft.Text("Historial de alertas", size=18, weight="bold"),
                self.tabla_alertas,
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
