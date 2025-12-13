import flet as ft
from models import obtener_transacciones, obtener_alertas, obtener_categorias
from ui.components import SectionTitle, SummaryCard


class DashboardScreen(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__(scroll=ft.ScrollMode.AUTO, expand=True)
        self.page = page

        self.card_ingresos = SummaryCard("Total Ingresos", "$0", color=ft.colors.GREEN, icono=ft.icons.TRENDING_UP)
        self.card_gastos = SummaryCard("Total Gastos", "$0", color=ft.colors.RED, icono=ft.icons.TRENDING_DOWN)
        self.card_saldo = SummaryCard("Saldo Actual", "$0", color=ft.colors.BLUE, icono=ft.icons.ACCOUNT_BALANCE)

        self.chart = ft.BarChart(
            bar_groups=[],
            border=ft.border.all(1, ft.colors.GREY_400),
            left_axis=ft.ChartAxis(labels_size=40, title=ft.Text("Monto")),
            bottom_axis=ft.ChartAxis(labels_size=40),
            expand=True,
            height=250,
        )

        self.chart_saldo = ft.BarChart(
            bar_groups=[],
            border=ft.border.all(1, ft.colors.GREY_400),
            left_axis=ft.ChartAxis(labels_size=40, title=ft.Text("Saldo")),
            bottom_axis=ft.ChartAxis(labels_size=40),
            expand=True,
            height=250,
        )

        self.piechart = ft.PieChart(
            sections=[],
            sections_space=2,
            center_space_radius=40,
            expand=True,
            height=260,
        )

        self.piechart_mensaje = ft.Text("", size=14, italic=True, color=ft.colors.GREY_600)

        self.transacciones_column = ft.Column()
        self.alertas_column = ft.Column()

        self.controls = [
            SectionTitle("Dashboard Financiero"),
            ft.Row([self.card_ingresos, self.card_gastos, self.card_saldo], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(),
            ft.Text("Ingresos vs Gastos por mes", size=18, weight="bold"),
            self.chart,
            ft.Divider(),
            ft.Text("Saldo mensual", size=18, weight="bold"),
            self.chart_saldo,
            ft.Divider(),
            ft.Text("Distribución de gastos por categoría", size=18, weight="bold"),
            self.piechart,
            self.piechart_mensaje,
            ft.Divider(),
            ft.Text("Últimas transacciones", size=18, weight="bold"),
            self.transacciones_column,
            ft.Divider(),
            ft.Text("Alertas recientes", size=18, weight="bold"),
            self.alertas_column,
        ]

    def did_mount(self):
        self.page.run_task(self._inicializar)

    async def _inicializar(self):
        self.actualizar_resumen()
        self.actualizar_grafico()
        self.actualizar_grafico_saldo()
        self.actualizar_piechart()
        self.cargar_transacciones()
        self.cargar_alertas()
        self.page.update()

    def actualizar_resumen(self):
        trans = obtener_transacciones()
        ingresos = sum(t.monto for t in trans if t.tipo == "ingreso")
        gastos = sum(t.monto for t in trans if t.tipo == "gasto")
        saldo = ingresos - gastos
        self.card_ingresos.set_value(f"${ingresos:,.0f}")
        self.card_gastos.set_value(f"${gastos:,.0f}")
        self.card_saldo.set_value(f"${saldo:,.0f}")

    def actualizar_grafico(self):
        trans = obtener_transacciones()
        ingresos_por_mes = {}
        gastos_por_mes = {}

        for t in trans:
            mes = t.fecha[:7]
            if t.tipo == "ingreso":
                ingresos_por_mes[mes] = ingresos_por_mes.get(mes, 0) + t.monto
            else:
                gastos_por_mes[mes] = gastos_por_mes.get(mes, 0) + t.monto

        meses = sorted(set(ingresos_por_mes.keys()) | set(gastos_por_mes.keys()))
        bar_groups = []

        for i, mes in enumerate(meses):
            bar_groups.append(
                ft.BarChartGroup(
                    x=i,
                    bar_rods=[
                        ft.BarChartRod(from_y=0, to_y=ingresos_por_mes.get(mes, 0), width=20, color=ft.colors.GREEN),
                        ft.BarChartRod(from_y=0, to_y=gastos_por_mes.get(mes, 0), width=20, color=ft.colors.RED),
                    ],
                )
            )

        self.chart.bar_groups = bar_groups
        self.chart.bottom_axis = ft.ChartAxis(
            labels=[ft.ChartAxisLabel(value=i, label=ft.Text(mes)) for i, mes in enumerate(meses)]
        )
        self.chart.update()

    def actualizar_grafico_saldo(self):
        trans = obtener_transacciones()
        saldo_por_mes = {}

        for t in trans:
            mes = t.fecha[:7]
            saldo_por_mes[mes] = saldo_por_mes.get(mes, 0)
            if t.tipo == "ingreso":
                saldo_por_mes[mes] += t.monto
            else:
                saldo_por_mes[mes] -= t.monto

        meses = sorted(saldo_por_mes.keys())
        bar_groups = []

        for i, mes in enumerate(meses):
            bar_groups.append(
                ft.BarChartGroup(
                    x=i,
                    bar_rods=[
                        ft.BarChartRod(from_y=0, to_y=saldo_por_mes[mes], width=20, color=ft.colors.BLUE),
                    ],
                )
            )

        self.chart_saldo.bar_groups = bar_groups
        self.chart_saldo.bottom_axis = ft.ChartAxis(
            labels=[ft.ChartAxisLabel(value=i, label=ft.Text(mes)) for i, mes in enumerate(meses)]
        )
        self.chart_saldo.update()

    def actualizar_piechart(self):
        trans = obtener_transacciones()
        gastos = [t for t in trans if t.tipo == "gasto"]
        totales = {}

        for t in gastos:
            nombre = t.categoria_nombre or "Sin categoría"
            totales[nombre] = totales.get(nombre, 0) + t.monto

        total_gastos = sum(totales.values())
        colores = [
            "#FF8A80", "#FFB74D", "#FFD54F", "#81C784",
            "#4FC3F7", "#9575CD", "#F06292", "#A1887F",
            "#90A4AE", "#DCE775", "#BA68C8", "#7986CB",
        ]

        secciones = []
        for i, (cat, monto) in enumerate(totales.items()):
            porcentaje = (monto / total_gastos) * 100 if total_gastos else 0
            secciones.append(
                ft.PieChartSection(
                    value=monto,
                    title=f"{cat} — {porcentaje:.0f}%",
                    color=colores[i % len(colores)],
                    radius=60,
                )
            )

        self.piechart.sections = secciones
        self.piechart.update()

        if len(secciones) == 1:
            self.piechart_mensaje.value = f"Actualmente todos los gastos están asignados a la categoría '{secciones[0].title.split(' —')[0]}'."
        else:
            self.piechart_mensaje.value = ""

    def cargar_transacciones(self):
        trans = obtener_transacciones()
        recientes = sorted(trans, key=lambda t: t.fecha, reverse=True)[:5]
        self.transacciones_column.controls = []

        for t in recientes:
            color = ft.colors.GREEN if t.tipo == "ingreso" else ft.colors.RED
            self.transacciones_column.controls.append(
                ft.Container(
                    padding=10,
                    bgcolor=ft.colors.with_opacity(0.05, color),
                    border_radius=6,
                    content=ft.Text(f"{t.fecha} — {t.tipo.upper()} — ${t.monto:.0f} — {t.descripcion}", size=14),
                )
            )

    def cargar_alertas(self):
        alertas = obtener_alertas()
        self.alertas_column.controls = []

        for a in alertas[:5]:
            color = ft.colors.ORANGE if a.tipo == "warning" else ft.colors.RED
            self.alertas_column.controls.append(
                ft.Container(
                    bgcolor=color,
                    padding=10,
                    border_radius=8,
                    content=ft.Text(f"{a.fecha} — {a.mensaje}", color="white"),
                )
            )
