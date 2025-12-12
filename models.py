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


def eliminar_categoria(cat_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM categorias WHERE id = ?", (cat_id,))
    conn.commit()
    conn.close()


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

    cur.execute("""
        INSERT INTO transacciones (tipo, monto, fecha, descripcion, categoria_id)
        VALUES (?, ?, ?, ?, ?)
    """, (tipo, monto, fecha, descripcion, categoria_id))

    conn.commit()
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

    cur.execute("""
        INSERT INTO alertas (categoria_id, tipo, mensaje, fecha)
        VALUES (?, ?, ?, ?)
    """, (categoria_id, tipo, mensaje, fecha))

    conn.commit()
    conn.close()
