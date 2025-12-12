import sqlite3

DB_NAME = "finanzas.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Tabla de categorías
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        )
        """
    )

    # Tabla de transacciones
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS transacciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,              -- 'ingreso' o 'gasto'
            monto REAL NOT NULL,
            fecha TEXT NOT NULL,             -- YYYY-MM-DD
            descripcion TEXT,
            categoria_id INTEGER,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        )
        """
    )

    # Tabla de alertas
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS alertas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria_id INTEGER,
            tipo TEXT NOT NULL,              -- 'warning' o 'critical'
            mensaje TEXT NOT NULL,
            fecha TEXT NOT NULL,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        )
        """
    )

    # Tabla de presupuestos
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS presupuestos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria_id INTEGER NOT NULL,
            monto_maximo REAL NOT NULL,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        )
        """
    )

    # Índices para optimizar búsquedas
    cur.execute("CREATE INDEX IF NOT EXISTS idx_trans_tipo_fecha ON transacciones (tipo, fecha)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_trans_categoria ON transacciones (categoria_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_alertas_categoria ON alertas (categoria_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_presu_categoria ON presupuestos (categoria_id)")

    # Insertar categorías por defecto si no hay ninguna
    cur.execute("SELECT COUNT(*) as total FROM categorias")
    total = cur.fetchone()["total"]
    if total == 0:
        categorias_default = [
            "Salario",
            "Alimentación",
            "Transporte",
            "Entretenimiento",
            "Servicios",
            "Salud",
            "Otros",
        ]
        for nombre in categorias_default:
            cur.execute("INSERT INTO categorias (nombre) VALUES (?)", (nombre,))

    conn.commit()
    conn.close()
