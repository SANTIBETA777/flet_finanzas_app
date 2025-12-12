import os
from datetime import datetime
from typing import List
from models import Transaccion, Categoria
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# ---------------------------------------------------------
# EXPORTAR A EXCEL
# ---------------------------------------------------------
def exportar_transacciones_excel(transacciones: List[Transaccion], ruta: str):
    """
    Exporta una lista de transacciones a un archivo Excel (.xlsx)
    usando openpyxl.
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "Transacciones"

    # Encabezados
    ws.append(["ID", "Tipo", "Monto", "Fecha", "Descripción", "Categoría"])

    # Datos
    for t in transacciones:
        ws.append([
            t.id,
            t.tipo,
            t.monto,
            t.fecha,
            t.descripcion,
            t.categoria_nombre or "Sin categoría",
        ])

    wb.save(ruta)
    return ruta


# ---------------------------------------------------------
# EXPORTAR A PDF
# ---------------------------------------------------------
def exportar_transacciones_pdf(transacciones: List[Transaccion], ruta: str):
    """
    Exporta una lista de transacciones a un archivo PDF
    usando reportlab.
    """
    c = canvas.Canvas(ruta, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Reporte de Transacciones")

    c.setFont("Helvetica", 10)
    y = height - 90

    for t in transacciones:
        linea = f"{t.fecha} | {t.tipo.upper()} | ${t.monto} | {t.descripcion} | {t.categoria_nombre}"
        c.drawString(50, y, linea)
        y -= 15

        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 10)
            y = height - 50

    c.save()
    return ruta


# ---------------------------------------------------------
# FILTROS DE EXPORTACIÓN
# ---------------------------------------------------------
def filtrar_transacciones(
    transacciones: List[Transaccion],
    fecha_inicio: str = None,
    fecha_fin: str = None,
    categoria_id: int = None,
    tipo: str = None,
):
    """
    Filtra transacciones por fecha, categoría o tipo.
    """
    resultado = transacciones

    if fecha_inicio:
        resultado = [t for t in resultado if t.fecha >= fecha_inicio]

    if fecha_fin:
        resultado = [t for t in resultado if t.fecha <= fecha_fin]

    if categoria_id:
        resultado = [t for t in resultado if t.categoria_id == categoria_id]

    if tipo:
        resultado = [t for t in resultado if t.tipo == tipo]

    return resultado


# ---------------------------------------------------------
# GENERAR NOMBRE AUTOMÁTICO DE ARCHIVO
# ---------------------------------------------------------
def generar_nombre_archivo(prefijo: str, extension: str) -> str:
    """
    Genera un nombre de archivo único basado en fecha y hora.
    """
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefijo}_{fecha}.{extension}"
