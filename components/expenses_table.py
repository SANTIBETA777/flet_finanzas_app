import flet as ft

class ExpensesTable(ft.UserControl):
    def __init__(self, transacciones=None):
        super().__init__()
        self.transacciones = transacciones or []
        self.contenedor = ft.Column()

    def update_data(self, nuevos):
        self.transacciones = nuevos or []
        self._actualizar_contenedor()
        self.update()

    def _actualizar_contenedor(self):
        self.contenedor.controls = []

        # ENCABEZADO
        header_row = ft.Row([
            ft.Text("Fecha", weight="bold", width=110),
            ft.Text("Descripción", weight="bold", width=150),
            ft.Text("Tipo", weight="bold", width=80),
            ft.Text("Categoría", weight="bold", width=100),
            ft.Text("Monto", weight="bold", width=80),
        ])

        self.contenedor.controls.append(header_row)
        self.contenedor.controls.append(ft.Divider())

        # FILAS
        for t in self.transacciones:
            row = ft.Row([
                ft.Text(str(t.get("fecha", "")), width=110),
                ft.Text(str(t.get("descripcion", "")), width=150),
                ft.Text(str(t.get("tipo", "")), width=80),
                ft.Text(str(t.get("categoria", "")), width=100),
                ft.Text(str(t.get("monto", "")), width=80),
            ], alignment=ft.MainAxisAlignment.START)

            self.contenedor.controls.append(row)

    def build(self):
        self._actualizar_contenedor()
        return ft.Container(content=self.contenedor, padding=10)
