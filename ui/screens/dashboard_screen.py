# ui/screens/dashboard_screen.py
import flet as ft
from models import obtener_transacciones, obtener_alertas
from ui.components import SectionTitle, SummaryCard


class DashboardScreen(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

        # Tarjetas resumen
        self.card_ingresos = SummaryCard("Total Ingresos", "$0", color="green")
        self.card_gastos = SummaryCard("Total Gastos", "$0", color="red")
        self.card_saldo = SummaryCard("Saldo Actual", "$0", color="blue")

        # Lista de alertas
        self.alertas_column = ft.Column()

    # ---------------------------------------------------------
    # Al montar la pantalla
    # ---------------------------------------------------------
    def did_mount(self):
        self.actualizar_resumen()
        self.cargar_alertas()

    # ---------------------------------------------------------
    # Calcular resumen financiero
    # ---------------------------------------------------------
    def actualizar_resumen(self):
        trans = obtener_transacciones()

        ingresos = sum(t.monto for t in trans if t.tipo == "ingreso")
        gastos = sum(t.monto for t in trans if t.tipo == "gasto")
        saldo = ingresos - gastos

        self.card_ingresos.valor = f"${ingresos:,.0f}"
        self.card_gastos.valor = f"${gastos:,.0f}"
        self.card_saldo.valor = f"${saldo:,.0f}"

        self.card_ingresos.update()
        self.card_gastos.update()
        self.card_saldo.update()

    # ---------------------------------------------------------
    # Cargar alertas recientes
    # ---------------------------------------------------------
    def cargar_alertas(self):
        alertas = obtener_alertas()
        self.alertas_column.controls = []

        for a in alertas[:5]:  # Solo mostrar las 5 más recientes
            color = ft.colors.ORANGE if a.tipo == "warning" else ft.colors.RED
            self.alertas_column.controls.append(
                ft.Container(
                    bgcolor=color,
                    padding=10,
                    border_radius=8,
                    content=ft.Text(f"{a.fecha} — {a.mensaje}", color="white"),
                )
            )

        self.alertas_column.update()

    # ---------------------------------------------------------
    # Render principal
    # ---------------------------------------------------------
    def build(self):
        return ft.Column(
            [
                SectionTitle("Resumen Financiero"),

                ft.Row([self.card_ingresos, self.card_gastos, self.card_saldo]),

                ft.Divider(),

                ft.Text("Alertas recientes", size=18, weight="bold"),
                self.alertas_column,
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
