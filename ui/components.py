import flet as ft
from validators import (
    validar_monto,
    validar_texto,
    validar_fecha,
)


# ---------------------------------------------------------
# COMPONENTE: Texto de error reutilizable
# ---------------------------------------------------------
class ErrorText(ft.Text):
    def __init__(self, value=""):
        super().__init__(value=value, color="red", size=12, visible=False)

    def show(self, msg: str):
        self.value = msg
        self.visible = True
        self.update()

    def hide(self):
        self.visible = False
        self.update()


# ---------------------------------------------------------
# COMPONENTE: Campo de texto validado
# ---------------------------------------------------------
class InputField(ft.Column):
    def __init__(self, label: str, validator=None, multiline=False):
        super().__init__()
        self.validator = validator
        self.input = ft.TextField(label=label, multiline=multiline)
        self.error = ErrorText()

        self.controls = [self.input, self.error]

    def get_value(self):
        return self.input.value

    def validate(self):
        if self.validator:
            ok, msg = self.validator(self.input.value)
            if not ok:
                self.error.show(msg)
                return False
        self.error.hide()
        return True


# ---------------------------------------------------------
# COMPONENTE: Campo numérico validado
# ---------------------------------------------------------
class NumberField(InputField):
    def __init__(self, label="Monto"):
        super().__init__(label, validator=validar_monto)


# ---------------------------------------------------------
# COMPONENTE: Selector de fecha con DatePicker
# ---------------------------------------------------------
class DateField(ft.Column):
    def __init__(self, label="Fecha"):
        super().__init__()

        self.date_picker = ft.DatePicker()
        self.input = ft.TextField(
            label=label,
            read_only=True,
            suffix=ft.IconButton(
                icon=ft.icons.CALENDAR_MONTH,
                on_click=lambda e: self.date_picker.pick_date(),
            ),
        )
        self.error = ErrorText()

        self.date_picker.on_change = self._on_date_selected

        self.controls = [self.date_picker, self.input, self.error]

    def _on_date_selected(self, e):
        self.input.value = self.date_picker.value.strftime("%Y-%m-%d")
        self.input.update()

    def get_value(self):
        return self.input.value

    def validate(self):
        ok, msg = validar_fecha(self.input.value)
        if not ok:
            self.error.show(msg)
            return False
        self.error.hide()
        return True


# ---------------------------------------------------------
# COMPONENTE: Botón con ícono
# ---------------------------------------------------------
class IconButtonPrimary(ft.ElevatedButton):
    def __init__(self, text, icon, on_click):
        super().__init__(
            text=text,
            icon=icon,
            on_click=on_click,
            style=ft.ButtonStyle(
                bgcolor="#4d96ff",
                color="white",
                padding=15,
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
        )


# ---------------------------------------------------------
# COMPONENTE: Título de sección
# ---------------------------------------------------------
class SectionTitle(ft.Text):
    def __init__(self, text):
        super().__init__(text, size=22, weight="bold")


# ---------------------------------------------------------
# COMPONENTE: Contenedor tipo tarjeta
# ---------------------------------------------------------
class CardContainer(ft.Container):
    def __init__(self, content):
        super().__init__(
            content=content,
            padding=15,
            border_radius=10,
            bgcolor="#f5f5f5",
        )


# ---------------------------------------------------------
# COMPONENTE: Diálogo de confirmación
# ---------------------------------------------------------
class ConfirmDialog(ft.AlertDialog):
    def __init__(self, title, message, on_confirm):
        super().__init__(
            modal=True,
            title=ft.Text(title),
            content=ft.Text(message),
            actions=[
                ft.TextButton("Cancelar", on_click=self._close),
                ft.TextButton("Confirmar", on_click=lambda e: self._confirm(on_confirm)),
            ],
        )

    def _close(self, e):
        self.open = False
        self.update()

    def _confirm(self, callback):
        callback()
        self.open = False
        self.update()
