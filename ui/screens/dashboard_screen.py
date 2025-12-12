import flet as ft
from datetime import datetime
from collections import defaultdict
from models import obtener_transacciones


class DashboardScreen(ft.UserControl):
    """
    Dashboard principal:
    - Resumen de ingresos, gastos y saldo
    - BarChart: ingresos vs gastos
    - PieChart: distribución por categorías
    - LineChart: tendencia últimos 6 meses
    - Últimas transacciones
    """

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

        # Widgets del resumen
        self.txt_ingresos = ft.Text("0", size=22, weight="bold", color="green")
        self.txt_gastos = ft.Text("0", size=22, weight="bold", color="red")
        self.txt_saldo = ft.Text("0", size=24, weight="bold")

        # Gráficos
        self.barchart = ft.BarChart(bar_groups=[], max_y=100, expand=True)
        self.piechart = ft.PieChart(sections=[], expand=True)
        self.linechart = ft.LineChart(data_series=[], max_y=100, min_y=0, expand=True)

        # Tabla de últimas transacciones
        self.tabla_ultimos = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Fecha")),
                ft.DataColumn(ft.Text("Tipo")),
                ft.DataColumn(ft.Text("Monto")),
                ft.DataColumn(ft.Text("Categoría")),
            ],
            rows=[]
        )

    # ---------------------------------------------------------
    # Al montar la pantalla, cargar datos
    # ---------------------------------------------------------
    def did_mount(self):
        self.cargar_resumen()
        self.cargar_barchart()
        self.cargar_piechart()
        self.cargar_linechart()
        self.cargar_ultimos()

    # ---------------------------------------------------------
    # Resumen ingresos / gastos / saldo
    # ---------------------------------------------------------
    def cargar_resumen(self):
        datos = obtener_transacciones()

        ingresos = sum(t.monto for t in datos if t.tipo == "ingreso")
        gastos = sum(t.monto for t in datos if t.tipo == "gasto")
        saldo = ingresos - gastos

        self.txt_ingresos.value = f"${ingresos:,.0f}"
        self.txt_gastos.value = f"${gastos:,.0f}"
        self.txt_saldo.value = f"${saldo:,.0f}"

        self.update()

    # ---------------------------------------------------------
    # BarChart: ingresos vs gastos
    # ---------------------------------------------------------
    def cargar_barchart(self):
        datos = obtener_transacciones()

        ingresos = sum(t.monto for t in datos if t.tipo == "ingreso")
        gastos = sum(t.monto for t in datos if t.tipo == "gasto")

        self.barchart.max_y = max(ingresos, gastos, 1)

        self.barchart.bar_groups = [
            ft.BarChartGroup(
                x=1,
                bar_rods=[ft.BarChartRod(from_y=0, to_y=ingresos, color="green")]
            ),
            ft.BarChartGroup(
                x=2,
                bar_rods=[ft.BarChartRod(from_y=0, to_y=gastos, color="red")]
            ),
        ]

        self.barchart.update()

    # ---------------------------------------------------------
    # PieChart: distribución de gastos por categoría
    # ---------------------------------------------------------
    def cargar_piechart(self):
        datos = obtener_transacciones()
        gastos = [t for t in datos if t.tipo == "gasto"]

        total = sum(t.monto for t in gastos) or 1

        categorias = defaultdict(float)
        for t in gastos:
            categorias[t.categoria_nombre or "Sin categoría"] += t.monto

        colores = ["#ff6b6b", "#ffa36c", "#ffd93d", "#6bcf63", "#4d96ff", "#845ec2"]

        self.piechart.sections = [
            ft.PieChartSection(
                value=(monto / total) * 100,
                title=f"{nombre} ({monto:.0f})",
                color=colores[i % len(colores)],
                radius=60,
            )
            for i, (nombre, monto) in enumerate(categorias.items())
        ]

        self.piechart.update()

    # ---------------------------------------------------------
    # LineChart: tendencia últimos 6 meses
    # ---------------------------------------------------------
    def cargar_linechart(self):
        datos = obtener_transacciones()

        meses = defaultdict(float)

        for t in datos:
            try:
                fecha = datetime.strptime(t.fecha, "%Y-%m-%d")
            except:
                continue

            clave = fecha.strftime("%Y-%m")
            if t.tipo == "gasto":
                meses[clave] += t.monto

        ultimos = sorted(meses.items())[-6:]

        self.linechart.max_y = max((m for _, m in ultimos), default=1)

        self.linechart.data_series = [
            ft.LineChartData(
                data_points=[
                    ft.LineChartDataPoint(i, monto)
                    for i, (_, monto) in enumerate(ultimos)
                ],
                color="red",
                stroke_width=3,
            )
        ]

        self.linechart.update()

    # ---------------------------------------------------------
    # Últimas transacciones
    # ---------------------------------------------------------
    def cargar_ultimos(self):
        datos = obtener_transacciones()[:5]

        self.tabla_ultimos.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(t.fecha)),
                    ft.DataCell(ft.Text(t.tipo)),
                    ft.DataCell(ft.Text(f"${t.monto}")),
                    ft.DataCell(ft.Text(t.categoria_nombre or "—")),
                ]
            )
            for t in datos
        ]

        self.tabla_ultimos.update()

    # ---------------------------------------------------------
    # Render principal
    # ---------------------------------------------------------
    def build(self):
        return ft.Column(
            [
                ft.Text("Dashboard Financiero", size=28, weight="bold"),

                ft.Row(
                    [
                        ft.Column([ft.Text("Ingresos"), self.txt_ingresos]),
                        ft.Column([ft.Text("Gastos"), self.txt_gastos]),
                        ft.Column([ft.Text("Saldo"), self.txt_saldo]),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                ),

                ft.Divider(),

                ft.Text("Ingresos vs Gastos", size=20, weight="bold"),
                self.barchart,

                ft.Divider(),

                ft.Text("Distribución de Gastos", size=20, weight="bold"),
                self.piechart,

                ft.Divider(),

                ft.Text("Tendencia de Gastos (6 meses)", size=20, weight="bold"),
                self.linechart,

                ft.Divider(),

                ft.Text("Últimas Transacciones", size=20, weight="bold"),
                self.tabla_ultimos,
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
