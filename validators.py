import re
from datetime import datetime


# -----------------------------
# VALIDACIÓN DE NÚMEROS
# -----------------------------
def validar_monto(valor: str) -> tuple[bool, str]:
    """
    Valida que el monto sea un número válido.
    Retorna (True, "") si es válido.
    Retorna (False, "mensaje") si es inválido.
    """
    if not valor.strip():
        return False, "El monto no puede estar vacío."

    try:
        monto = float(valor)
        if monto <= 0:
            return False, "El monto debe ser mayor a 0."
    except ValueError:
        return False, "El monto debe ser un número válido."

    return True, ""


# -----------------------------
# VALIDACIÓN DE TEXTO
# -----------------------------
def validar_texto(texto: str, minimo=3, maximo=50) -> tuple[bool, str]:
    """
    Valida textos como descripciones, nombres, etc.
    """
    if not texto.strip():
        return False, "El texto no puede estar vacío."

    if len(texto) < minimo:
        return False, f"Debe tener al menos {minimo} caracteres."

    if len(texto) > maximo:
        return False, f"No puede superar los {maximo} caracteres."

    # No permitir caracteres peligrosos
    if re.search(r"[<>/{}$%#@]", texto):
        return False, "El texto contiene caracteres no permitidos."

    return True, ""


# -----------------------------
# VALIDACIÓN DE FECHAS
# -----------------------------
def validar_fecha(fecha: str) -> tuple[bool, str]:
    """
    Valida que la fecha esté en formato YYYY-MM-DD.
    """
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
        return True, ""
    except ValueError:
        return False, "La fecha no es válida. Use el formato YYYY-MM-DD."


# -----------------------------
# VALIDACIÓN DE CATEGORÍAS
# -----------------------------
def validar_categoria(categoria_id) -> tuple[bool, str]:
    """
    Valida que se haya seleccionado una categoría.
    """
    if categoria_id is None:
        return False, "Debe seleccionar una categoría."

    try:
        categoria_id = int(categoria_id)
        if categoria_id <= 0:
            return False, "Categoría inválida."
    except ValueError:
        return False, "Categoría inválida."

    return True, ""


# -----------------------------
# VALIDACIÓN GENERAL
# -----------------------------
def validar_transaccion(monto, fecha, descripcion, categoria_id):
    """
    Valida todos los campos de una transacción.
    Retorna (True, "") si todo está bien.
    Retorna (False, "mensaje") si algo falla.
    """

    ok, msg = validar_monto(monto)
    if not ok:
        return False, msg

    ok, msg = validar_fecha(fecha)
    if not ok:
        return False, msg

    ok, msg = validar_texto(descripcion, minimo=3, maximo=100)
    if not ok:
        return False, msg

    ok, msg = validar_categoria(categoria_id)
    if not ok:
        return False, msg

    return True, ""
