import re
from datetime import datetime

# ============================================================
#   VALIDACIÓN DE MONTOS
# ============================================================

def validar_monto(valor: str):
    """
    Valida que el monto sea numérico y mayor a 0.
    Acepta formatos como:
    - 800
    - 800.50
    - 800.000
    - 1.200.000
    """

    if not valor or valor.strip() == "":
        return False, "El monto no puede estar vacío."

    # Quitar puntos de miles
    valor_limpio = valor.replace(".", "")

    # Debe ser número
    if not re.match(r"^[0-9]+(\,[0-9]+)?$", valor_limpio.replace(",", ".")):
        return False, "El monto debe ser un número válido."

    # Convertir a float
    try:
        monto = float(valor_limpio.replace(",", "."))
    except:
        return False, "El monto debe ser un número válido."

    if monto <= 0:
        return False, "El monto debe ser mayor que 0."

    return True, ""


# ============================================================
#   VALIDACIÓN DE FECHAS
# ============================================================

def validar_fecha(fecha: str):
    if not fecha:
        return False, "Debe seleccionar una fecha."

    try:
        datetime.strptime(fecha, "%Y-%m-%d")
        return True, ""
    except ValueError:
        return False, "La fecha debe tener formato YYYY-MM-DD."


# ============================================================
#   VALIDACIÓN DE TEXTO
# ============================================================

def validar_texto(texto: str, minimo=3, maximo=200):
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

    # Categoría solo obligatoria en gastos
    if tipo == "gasto":
        ok, msg = validar_categoria(categoria_id)
        if not ok:
            return False, msg

    return True, ""
