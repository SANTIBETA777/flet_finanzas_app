# database.py
import sqlite3
import os

DB_PATH = "finanzas.db"


# ============================================================
#   CONEXIÓN A LA BASE DE DATOS
# ============================================================

def get_conn():
    """Retorna una conexión a SQLite con filas tipo diccionario."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ============================================================
#   CREACIÓN DE TABLAS (si no existen)
# ============================================================

def init_db():
    """Crea todas las tablas necesarias para la app."""
    conn = get_conn()
    cur = conn.cursor()

    # ------------------ CATEGORÍAS ------------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL
        )
    """)

    # Índice para búsquedas rápidas
    cur.execute("CREATE INDEX IF NOT EXISTS idx_categorias_nombre ON categorias(nombre)")

    # ------------------ TRANSACCIONES ------------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS transacciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL CHECK(tipo IN ('ingreso', 'gasto')),
            monto REAL NOT NULL,
            fecha TEXT NOT NULL,
            descripcion TEXT,
            categoria_id INTEGER,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        )
    """)

    cur.execute("CREATE INDEX IF NOT EXISTS idx_transacciones_fecha ON transacciones(fecha)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_transacciones_tipo ON transacciones(tipo)")

    # ------------------ PRESUPUESTOS ------------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS presupuestos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria_id INTEGER NOT NULL,
            monto_maximo REAL NOT NULL,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        )
    """)

    cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_presupuesto_categoria ON presupuestos(categoria_id)")

    # ------------------ ALERTAS ------------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS alertas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria_id INTEGER,
            tipo TEXT NOT NULL CHECK(tipo IN ('warning', 'critical')),
            mensaje TEXT NOT NULL,
            fecha TEXT NOT NULL,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        )
    """)

    cur.execute("CREATE INDEX IF NOT EXISTS idx_alertas_fecha ON alertas(fecha)")

    conn.commit()
    conn.close()


# ============================================================
#   RESETEAR BASE DE DATOS (opcional para desarrollo)
# ============================================================

def reset_db():
    """Elimina la base de datos y la crea de nuevo (solo para desarrollo)."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    init_db()
