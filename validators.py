# validators.py
import re
from datetime import datetime


# ============================================================
#   VALIDACIÓN DE MONTOS
# ============================================================

def validar_monto(valor: str):
    """
    Valida que el monto sea numérico y mayor a 0.
    Retorna (True, "") si es válido.
    Retorna (False, "mensaje") si es inválido.
    """
    if not valor or valor.strip() == "":
        return False, "El monto no puede estar vacío."

    # Solo números y punto decimal
    if not re.match(r"^[0-9]+(\.[0-9]+)?$", valor):
        return False, "El monto debe ser un número válido."

    monto = float(valor)
    if monto <= 0:
        return False, "El monto debe ser mayor que 0."

    return True, ""


# ============================================================
#   VALIDACIÓN DE FECHAS
# ============================================================

def validar_fecha(fecha: str):
    """
    Valida que la fecha tenga formato YYYY-MM-DD.
    """
    if not fecha:
        return False, "Debe seleccionar una fecha."

    try:
        datetime.strptime(fecha, "%Y-%m-%d")
        return True, ""
    except ValueError:
        return False, "La fecha debe tener formato YYYY-MM-DD."


# ============================================================
#   VALIDACIÓN DE TEXTO (DESCRIPCIÓN)
# ============================================================

def validar_texto(texto: str, minimo=3, maximo=200):
    """
    Valida longitud mínima y máxima.
    No permite solo espacios.
    """
    if not texto or texto.strip() == "":
        return False, "El texto no puede estar vacío."

    if len(texto) < minimo:
        return False, f"El texto debe tener al menos {minimo} caracteres."

    if len(texto) > maximo:
        return False, f"El texto no puede superar {maximo} caracteres."

    return True, ""


# ============================================================
#   VALIDACIÓN DE CATEGORÍA
# ============================================================

def validar_categoria(cat_id):
    if not cat_id:
        return False, "Debe seleccionar una categoría."
    return True, ""


# ============================================================
#   VALIDACIÓN COMPLETA DE TRANSACCIÓN
# ============================================================

def validar_transaccion(fecha, descripcion, monto, tipo, categoria_id):
    """
    Valida todos los campos de una transacción.
    Retorna (True, "") si todo está bien.
    Retorna (False, "mensaje") si algo falla.
    """

    ok, msg = validar_fecha(fecha)
    if not ok:
        return False, msg

    ok, msg = validar_texto(descripcion)
    if not ok:
        return False, msg

    ok, msg = validar_monto(monto)
    if not ok:
        return False, msg

    if tipo not in ("ingreso", "gasto"):
        return False, "Debe seleccionar un tipo válido."

    # Solo validar categoría si es gasto
    if tipo == "gasto":
        ok, msg = validar_categoria(categoria_id)
        if not ok:
            return False, msg

    return True, ""
