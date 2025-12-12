import flet as ft

class AddExpenseForm(ft.UserControl):
    def __init__(self, on_save):
        super().__init__()
        self.on_save = on_save

    def build(self):
        self.fecha = ft.TextField(
            label="Fecha (YYYY-MM-DD)",
            hint_text="2025-01-10",
            width=300
        )

        self.descripcion = ft.TextField(
            label="Descripción",
            width=300
        )

        self.monto = ft.TextField(
            label="Monto",
            width=300,
            keyboard_type=ft.KeyboardType.NUMBER
        )

        # NUEVO: dropdown para tipo de transacción
        self.tipo = ft.Dropdown(
            label="Tipo",
            width=300,
            options=[
                ft.dropdown.Option("ingreso"),
                ft.dropdown.Option("gasto"),
            ]
        )

        btn_guardar = ft.ElevatedButton(
            text="Guardar",
            on_click=self.guardar
        )

        return ft.Column(
            controls=[
                self.fecha,
                self.descripcion,
                self.monto,
                self.tipo,
                btn_guardar
            ]
        )

    def guardar(self, e):
        if self.on_save:
            self.on_save(
                self.fecha.value,
                self.descripcion.value,
                self.monto.value,
                self.tipo.value
            )
