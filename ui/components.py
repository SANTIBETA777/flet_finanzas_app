# ui/components.py
import flet as ft
from validators import (
    validar_monto,
    validar_fecha,
    validar_texto,
)


# ============================================================
#   TÍTULO DE SECCIÓN
# ============================================================

class SectionTitle(ft.UserControl):
    def __init__(self, texto: str):
        super().__init__()
        self.texto = texto

    def build(self):
        return ft.Text(
            self.texto,
            size=24,
            weight="bold",
            color=ft.colors.BLUE_700,
        )


# ============================================================
#   INPUT DE TEXTO GENERAL
# ============================================================

class InputField(ft.UserControl):
    def __init__(self, label: str, width=300):
        super().__init__()
        self.label = label
        self.width = width
        self.field = ft.TextField(label=label, width=width)

    def build(self):
        return self.field

    def get_value(self):
        return self.field.value

    def set_value(self, value):
        self.field.value = value
        self.update()


# ============================================================
#   INPUT NUMÉRICO (VALIDADO)
# ============================================================

class NumberField(ft.UserControl):
    def __init__(self, label: str, width=300):
        super().__init__()
        self.label = label
        self.width = width
        self.field = ft.TextField(
            label=label,
            width=width,
            keyboard_type=ft.KeyboardType.NUMBER,
        )

    def build(self):
        return self.field

    def get_value(self):
        return self.field.value

    def validate(self):
        ok, msg = validar_monto(self.field.value)
        return ok, msg


# ============================================================
#   INPUT DE FECHA (OBLIGATORIO)
# ============================================================

class DateField(ft.UserControl):
    def __init__(self, label="Fecha", width=300):
        super().__init__()
        self.label = label
        self.width = width

        self.field = ft.TextField(
            label=label,
            width=width,
            read_only=True,
            suffix_icon=ft.icons.CALENDAR_MONTH,
            on_click=self.abrir_datepicker,
        )

        self.datepicker = ft.DatePicker(
            on_change=self.seleccionar_fecha,
        )

    def build(self):
        return ft.Column([self.field, self.datepicker])

    def abrir_datepicker(self, e):
        self.datepicker.open = True
        self.update()

    def seleccionar_fecha(self, e):
        if self.datepicker.value:
            self.field.value = self.datepicker.value.strftime("%Y-%m-%d")
            self.update()

    def get_value(self):
        return self.field.value

    def validate(self):
        ok, msg = validar_fecha(self.field.value)
        return ok, msg


# ============================================================
#   DIÁLOGO DE CONFIRMACIÓN
# ============================================================

class ConfirmDialog(ft.AlertDialog):
    def __init__(self, mensaje: str, on_confirm):
        super().__init__()
        self.mensaje = mensaje
        self.on_confirm = on_confirm

        self.title = ft.Text("Confirmación")
        self.content = ft.Text(mensaje)

        self.actions = [
            ft.TextButton("Cancelar", on_click=self.cerrar),
            ft.ElevatedButton("Confirmar", on_click=self.confirmar),
        ]

    def confirmar(self, e):
        if self.on_confirm:
            self.on_confirm()
        self.open = False

    def cerrar(self, e):
        self.open = False


# ============================================================
#   TARJETA DE RESUMEN (Dashboard)
# ============================================================

class SummaryCard(ft.UserControl):
    def __init__(self, titulo: str, valor: str, color="black"):
        super().__init__()
        self.titulo = titulo
        self.valor = valor
        self.color = color

    def build(self):
        return ft.Container(
            padding=20,
            bgcolor=ft.colors.BLUE_50,
            border_radius=10,
            content=ft.Column(
                [
                    ft.Text(self.titulo, size=16, weight="bold"),
                    ft.Text(self.valor, size=22, weight="bold", color=self.color),
                ]
            ),
        )
