import sqlite3
from database import get_conn


# ==============================
#   CATEGORÍAS
# ==============================

def crear_categoria(nombre: str) -> int:
    """Crea una categoría si no existe. Devuelve su ID."""
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id FROM categorias WHERE nombre = ?", (nombre,))
    row = cur.fetchone()
    if row:
        conn.close()
        return row[0]

    cur.execute("INSERT INTO categorias (nombre) VALUES (?)", (nombre,))
    conn.commit()

    nuevo_id = cur.lastrowid
    conn.close()
    return nuevo_id


def listar_categorias():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id, nombre FROM categorias ORDER BY nombre ASC")
    rows = cur.fetchall()

    conn.close()
    return [dict(row) for row in rows]


def editar_categoria(cat_id: int, nuevo_nombre: str):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE categorias
        SET nombre = ?
        WHERE id = ?
    """, (nuevo_nombre, cat_id))

    conn.commit()
    conn.close()


def eliminar_categoria(cat_id: int):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("DELETE FROM categorias WHERE id = ?", (cat_id,))
    conn.commit()
    conn.close()



# ==============================
#   TRANSACCIONES
# ==============================

def crear_transaccion(tipo: str, monto: float, fecha: str, descripcion: str, categoria_id=None):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO transacciones (tipo, monto, fecha, descripcion, categoria_id)
        VALUES (?, ?, ?, ?, ?)
    """, (tipo, monto, fecha, descripcion, categoria_id))

    conn.commit()
    conn.close()


def listar_transacciones():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            t.id,
            t.fecha,
            t.descripcion,
            t.tipo,
            c.nombre AS categoria,
            t.monto
        FROM transacciones t
        LEFT JOIN categorias c ON t.categoria_id = c.id
        ORDER BY t.fecha DESC
    """)

    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]

