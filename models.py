import sqlite3
from dataclasses import dataclass
from typing import Optional, List
from database import get_conn


# ============================================================
#   MODELOS (POO)
# ============================================================

@dataclass
class Categoria:
    id: int
    nombre: str

    @staticmethod
    def from_row(row):
        return Categoria(id=row["id"], nombre=row["nombre"])


@dataclass
class Transaccion:
    id: int
    tipo: str
    monto: float
    fecha: str
    descripcion: str
    categoria_id: Optional[int]
    categoria_nombre: Optional[str] = None

    @staticmethod
    def from_row(row):
        return Transaccion(
            id=row["id"],
            tipo=row["tipo"],
            monto=row["monto"],
            fecha=row["fecha"],
            descripcion=row["descripcion"],
            categoria_id=row["categoria_id"],
            categoria_nombre=row["categoria"],
        )


@dataclass
class Presupuesto:
    id: int
    categoria_id: int
    monto_maximo: float

    @staticmethod
    def from_row(row):
        return Presupuesto(
            id=row["id"],
            categoria_id=row["categoria_id"],
            monto_maximo=row["monto_maximo"],
        )


@dataclass
class Alerta:
    id: int
    categoria_id: Optional[int]
    tipo: str
    mensaje: str
    fecha: str

    @staticmethod
    def from_row(row):
        return Alerta(
            id=row["id"],
            categoria_id=row["categoria_id"],
            tipo=row["tipo"],
            mensaje=row["mensaje"],
            fecha=row["fecha"],
        )


# ============================================================
#   HELPERS INTERNOS
# ============================================================

def _mes_desde_fecha(fecha: str) -> str:
    # fecha en formato YYYY-MM-DD -> devuelve YYYY-MM
    return fecha[:7]


def _existe_alerta_en_mes(tipo: str, mes: str, categoria_id: Optional[int] = None) -> bool:
    """
    Verifica si ya existe una alerta de un tipo dado en un mes concreto.
    Para evitar spam de alertas, solo se genera UNA por mes y tipo.
    """
    conn = get_conn()
    cur = conn.cursor()

    if categoria_id is None:
        cur.execute(
            """
            SELECT COUNT(*) AS total
            FROM alertas
            WHERE tipo = ?
              AND substr(fecha, 1, 7) = ?
              AND categoria_id IS NULL
            """,
            (tipo, mes,),
        )
    else:
        cur.execute(
            """
            SELECT COUNT(*) AS total
            FROM alertas
            WHERE tipo = ?
              AND substr(fecha, 1, 7) = ?
              AND categoria_id = ?
            """,
            (tipo, mes, categoria_id),
        )

    total = cur.fetchone()[0]
    conn.close()
    return total > 0


# ============================================================
#   CATEGORÍAS
# ============================================================

def obtener_categorias() -> List[Categoria]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre FROM categorias ORDER BY nombre ASC")
    rows = cur.fetchall()
    conn.close()
    return [Categoria.from_row(row) for row in rows]


def crear_categoria(nombre: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO categorias (nombre) VALUES (?)", (nombre,))
    conn.commit()
    conn.close()


def editar_categoria(cat_id: int, nombre: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE categorias SET nombre = ? WHERE id = ?", (nombre, cat_id))
    conn.commit()
    conn.close()


def eliminar_categoria(cat_id: int) -> bool:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) AS total FROM transacciones WHERE categoria_id = ?", (cat_id,))
    en_uso = cur.fetchone()[0]

    if en_uso > 0:
        conn.close()
        return False

    cur.execute("DELETE FROM categorias WHERE id = ?", (cat_id,))
    conn.commit()
    conn.close()
    return True


# ============================================================
#   PRESUPUESTOS
# ============================================================

def obtener_presupuestos() -> List[Presupuesto]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM presupuestos")
    rows = cur.fetchall()
    conn.close()
    return [Presupuesto.from_row(row) for row in rows]


def guardar_presupuesto(categoria_id: int, monto: float):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id FROM presupuestos WHERE categoria_id = ?", (categoria_id,))
    row = cur.fetchone()

    if row:
        cur.execute(
            "UPDATE presupuestos SET monto_maximo = ? WHERE categoria_id = ?",
            (monto, categoria_id),
        )
    else:
        cur.execute(
            "INSERT INTO presupuestos (categoria_id, monto_maximo) VALUES (?, ?)",
            (categoria_id, monto),
        )

    conn.commit()
    conn.close()


# ============================================================
#   TRANSACCIONES
# ============================================================

def obtener_transacciones() -> List[Transaccion]:
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            t.id,
            t.tipo,
            t.monto,
            t.fecha,
            t.descripcion,
            t.categoria_id,
            c.nombre AS categoria
        FROM transacciones t
        LEFT JOIN categorias c ON t.categoria_id = c.id
        ORDER BY t.fecha DESC
    """)

    rows = cur.fetchall()
    conn.close()
    return [Transaccion.from_row(row) for row in rows]


def crear_transaccion(tipo: str, monto: float, fecha: str, descripcion: str, categoria_id=None):
    conn = get_conn()
    cur = conn.cursor()

    # Insertar transacción
    cur.execute(
        """
        INSERT INTO transacciones (tipo, monto, fecha, descripcion, categoria_id)
        VALUES (?, ?, ?, ?, ?)
        """,
        (tipo, monto, fecha, descripcion, categoria_id),
    )
    conn.commit()

    # --------------------------------------------------------
    #   LÓGICA DE ALERTAS
    # --------------------------------------------------------
    mes = _mes_desde_fecha(fecha)

    # 1) Cargar presupuestos en memoria
    cur.execute("SELECT * FROM presupuestos")
    rows_pres = cur.fetchall()
    presupuestos = {row["categoria_id"]: Presupuesto.from_row(row) for row in rows_pres}

    # 2) Gastos por categoría en el mes
    cur.execute(
        """
        SELECT categoria_id, SUM(monto) AS total
        FROM transacciones
        WHERE tipo = 'gasto' AND substr(fecha, 1, 7) = ?
        GROUP BY categoria_id
        """,
        (mes,),
    )
    gastos_mes_por_cat = {row["categoria_id"]: row["total"] for row in cur.fetchall()}

    # 3) Ingresos y gastos totales del mes
    cur.execute(
        """
        SELECT 
            SUM(CASE WHEN tipo = 'ingreso' THEN monto ELSE 0 END) AS total_ingresos,
            SUM(CASE WHEN tipo = 'gasto' THEN monto ELSE 0 END) AS total_gastos
        FROM transacciones
        WHERE substr(fecha, 1, 7) = ?
        """,
        (mes,),
    )
    row_totales = cur.fetchone()
    total_ingresos_mes = row_totales["total_ingresos"] or 0
    total_gastos_mes = row_totales["total_gastos"] or 0
    saldo_mes = total_ingresos_mes - total_gastos_mes

    # 4) Gasto repetitivo (mismo monto, misma categoría, mismo mes)
    if tipo == "gasto" and categoria_id is not None:
        cur.execute(
            """
            SELECT COUNT(*) AS total
            FROM transacciones
            WHERE tipo = 'gasto'
              AND categoria_id = ?
              AND monto = ?
              AND substr(fecha, 1, 7) = ?
            """,
            (categoria_id, monto, mes),
        )
        rep_count = cur.fetchone()["total"]
    else:
        rep_count = 0

    # --------------------------------------------------------
    #   4.1) Alertas por presupuesto (por categoría)
    # --------------------------------------------------------
    if tipo == "gasto" and categoria_id is not None:
        total_gastado_cat = gastos_mes_por_cat.get(categoria_id, 0)
        presupuesto_cat = presupuestos.get(categoria_id)

        if presupuesto_cat:
            maximo = presupuesto_cat.monto_maximo

            # Supera presupuesto
            if total_gastado_cat > maximo:
                tipo_alerta = "presupuesto_superado"
                if not _existe_alerta_en_mes(tipo_alerta, mes, categoria_id):
                    mensaje = f"Has superado el presupuesto mensual de la categoría."
                    crear_alerta(categoria_id, tipo_alerta, mensaje, fecha)

            # Llega al 90% del presupuesto
            elif total_gastado_cat >= 0.9 * maximo:
                tipo_alerta = "presupuesto_cercano"
                if not _existe_alerta_en_mes(tipo_alerta, mes, categoria_id):
                    mensaje = f"Estás por alcanzar el presupuesto de la categoría (90%)."
                    crear_alerta(categoria_id, tipo_alerta, mensaje, fecha)
        else:
            # Categoría sin presupuesto definido
            tipo_alerta = "categoria_sin_presupuesto"
            if not _existe_alerta_en_mes(tipo_alerta, mes, categoria_id):
                mensaje = "Esta categoría no tiene presupuesto asignado."
                crear_alerta(categoria_id, tipo_alerta, mensaje, fecha)

    # --------------------------------------------------------
    #   4.2) Alertas globales (mes completo)
    # --------------------------------------------------------

    # Gastos del mes > ingresos del mes
    if total_gastos_mes > total_ingresos_mes:
        tipo_alerta = "gastos_mayores_ingresos"
        if not _existe_alerta_en_mes(tipo_alerta, mes, None):
            mensaje = "En este mes, los gastos totales superan a los ingresos."
            crear_alerta(None, tipo_alerta, mensaje, fecha)

    # Saldo del mes negativo
    if saldo_mes < 0:
        tipo_alerta = "saldo_negativo"
        if not _existe_alerta_en_mes(tipo_alerta, mes, None):
            mensaje = "El saldo de este mes es negativo."
            crear_alerta(None, tipo_alerta, mensaje, fecha)

    # Gasto repetitivo (3 o más veces mismo monto y categoría en el mes)
    if rep_count >= 3:
        tipo_alerta = "gasto_repetitivo"
        if not _existe_alerta_en_mes(tipo_alerta, mes, categoria_id):
            mensaje = "Se han detectado gastos repetitivos en esta categoría este mes."
            crear_alerta(categoria_id, tipo_alerta, mensaje, fecha)

    conn.close()


def eliminar_transaccion(trans_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM transacciones WHERE id = ?", (trans_id,))
    conn.commit()
    conn.close()


# ============================================================
#   ALERTAS
# ============================================================

def obtener_alertas() -> List[Alerta]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM alertas ORDER BY fecha DESC")
    rows = cur.fetchall()
    conn.close()
    return [Alerta.from_row(row) for row in rows]


def crear_alerta(categoria_id: Optional[int], tipo: str, mensaje: str, fecha: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO alertas (categoria_id, tipo, mensaje, fecha)
        VALUES (?, ?, ?, ?)
        """,
        (categoria_id, tipo, mensaje, fecha),
    )
    conn.commit()
    conn.close()
