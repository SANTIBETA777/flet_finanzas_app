import flet as ft
from validators import (
    validar_monto,
    validar_fecha,
    validar_texto,
)
from datetime import date, datetime

# ============================================================
#   TÍTULO DE SECCIÓN
# ============================================================

class SectionTitle(ft.Text):
    def __init__(self, texto: str):
        super().__init__(
            value=texto,
            size=24,
            weight="bold",
            color=ft.colors.BLUE_700,
        )


# ============================================================
#   INPUT DE TEXTO GENERAL
# ============================================================

class InputField(ft.Column):
    def __init__(self, label: str, width=300):
        super().__init__()
        self.field = ft.TextField(label=label, width=width)
        self.controls = [self.field]

    def get_value(self):
        return self.field.value

    def set_value(self, value):
        self.field.value = value


# ============================================================
#   INPUT NUMÉRICO (VALIDADO)
# ============================================================

class NumberField(ft.Column):
    def __init__(self, label: str, width=300):
        super().__init__()
        self.field = ft.TextField(
            label=label,
            width=width,
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        self.controls = [self.field]

    def get_value(self):
        return self.field.value

    def validate(self):
        ok, msg = validar_monto(self.field.value)
        return ok, msg


# ============================================================
#   INPUT DE FECHA — PROFESIONAL, VALIDADO, SIN ERRORES
# ============================================================

class DateField(ft.Column):
    def __init__(self, label="Fecha", width=300, value=None, page=None):
        super().__init__()

        self.page = page

        if value is None:
            value = str(date.today())

        # Campo editable + placeholder profesional
        self.field = ft.TextField(
            label=label,
            width=width,
            value=value,
            hint_text="AAAA-MM-DD",
            suffix_icon=ft.icons.CALENDAR_MONTH,
            on_click=self.abrir_datepicker,
            on_change=self.validar_manual,
        )

        # DatePicker con rango amplio (evita OUT OF RANGE)
        self.datepicker = ft.DatePicker(
            first_date=date(2000, 1, 1),
            last_date=date(2035, 12, 31),
            on_change=self.seleccionar_fecha,
        )

        self.controls = [self.field]

    def did_mount(self):
        if self.page and self.datepicker not in self.page.overlay:
            self.page.overlay.append(self.datepicker)
            self.page.update()

    def abrir_datepicker(self, e):
        self.datepicker.open = True
        if self.page:
            self.page.update()

    def seleccionar_fecha(self, e):
        if self.datepicker.value:
            self.field.value = self.datepicker.value.strftime("%Y-%m-%d")
            self.field.error_text = None
            self.update()

    # Validación del texto escrito manualmente
    def validar_manual(self, e):
        texto = self.field.value.strip()

        if texto == "":
            self.field.error_text = None
            self.update()
            return

        try:
            # Validar formato
            fecha = datetime.strptime(texto, "%Y-%m-%d").date()

            # Validar rango
            if fecha < date(2000, 1, 1) or fecha > date(2035, 12, 31):
                self.field.error_text = "Fecha fuera del rango permitido (2000–2035)."
            else:
                self.field.error_text = None

        except ValueError:
            self.field.error_text = "Formato inválido. Use AAAA-MM-DD."

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
#   TARJETA DE RESUMEN PROFESIONAL (Dashboard)
# ============================================================

class SummaryCard(ft.Container):
    def __init__(self, titulo: str, valor: str, color=ft.colors.BLUE, icono=ft.icons.INFO):
        super().__init__(
            padding=20,
            border_radius=12,
            bgcolor=ft.colors.with_opacity(0.9, color),
            expand=True,
        )

        self.titulo = titulo
        self.valor = valor

        self.content = ft.Column(
            [
                ft.Icon(icono, size=40, color="white"),
                ft.Text(titulo, size=16, weight="bold", color="white"),
                ft.Text(valor, size=22, weight="bold", color="white"),
            ],
            spacing=8,
        )

    def set_value(self, nuevo_valor: str):
        self.content.controls[2].value = nuevo_valor
        self.update()
