import sqlite3
import os

# ============================================================
#   RUTA ABSOLUTA FIJA A LA BASE DE DATOS
# ============================================================

DB_PATH = r"C:\Users\Santiago\Desktop\flet_finanzas_app\finanzas.db"


# ============================================================
#   CONEXIÓN A LA BASE DE DATOS
# ============================================================

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ============================================================
#   CREACIÓN DE TABLAS
# ============================================================

def init_db():
    print(">>> Inicializando base de datos en:", DB_PATH)

    conn = get_conn()
    cur = conn.cursor()

    # ------------------ CATEGORÍAS ------------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL
        )
    """)

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

    # ------------------ PRESUPUESTOS ------------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS presupuestos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria_id INTEGER NOT NULL,
            monto_maximo REAL NOT NULL,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        )
    """)

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

    conn.commit()
    conn.close()
    print(">>> Tablas listas.")


# ============================================================
#   RESETEAR BASE DE DATOS
# ============================================================

def reset_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(">>> Base de datos eliminada.")

    init_db()
    print(">>> Base de datos nueva creada.")
