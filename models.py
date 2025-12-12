from dataclasses import dataclass
from typing import Optional, List
from database import get_connection


# ---------- Clases de datos ----------

@dataclass
class Categoria:
    id: Optional[int]
    nombre: str


@dataclass
class Transaccion:
    id: Optional[int]
    tipo: str              # 'ingreso' o 'gasto'
    monto: float
    fecha: str             # 'YYYY-MM-DD'
    descripcion: str
    categoria_id: Optional[int]
    categoria_nombre: Optional[str] = None


@dataclass
class Alerta:
    id: Optional[int]
    categoria_id: Optional[int]
    tipo: str              # 'warning' o 'critical'
    mensaje: str
    fecha: str             # 'YYYY-MM-DD'


@dataclass
class Presupuesto:
    id: Optional[int]
    categoria_id: int
    monto_maximo: float


# ---------- Categorías ----------

def obtener_categorias() -> list[Categoria]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre FROM categorias ORDER BY nombre")
    filas = cur.fetchall()
    conn.close()
    return [Categoria(id=f["id"], nombre=f["nombre"]) for f in filas]


def crear_categoria(nombre: str) -> Categoria:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO categorias (nombre) VALUES (?)", (nombre,))
    conn.commit()
    cat_id = cur.lastrowid
    conn.close()
    return Categoria(id=cat_id, nombre=nombre)


# ---------- Transacciones ----------

def crear_transaccion(
    tipo: str,
    monto: float,
    fecha: str,
    descripcion: str,
    categoria_id: int | None,
) -> Transaccion:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO transacciones (tipo, monto, fecha, descripcion, categoria_id)
        VALUES (?, ?, ?, ?, ?)
        """,
        (tipo, monto, fecha, descripcion, categoria_id),
    )
    conn.commit()
    trans_id = cur.lastrowid
    conn.close()
    return Transaccion(
        id=trans_id,
        tipo=tipo,
        monto=monto,
        fecha=fecha,
        descripcion=descripcion,
        categoria_id=categoria_id,
    )


def obtener_transacciones() -> list[Transaccion]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT t.id, t.tipo, t.monto, t.fecha, t.descripcion,
               t.categoria_id, c.nombre AS categoria_nombre
        FROM transacciones t
        LEFT JOIN categorias c ON t.categoria_id = c.id
        ORDER BY t.fecha DESC, t.id DESC
        """
    )
    filas = cur.fetchall()
    conn.close()
    return [
        Transaccion(
            id=f["id"],
            tipo=f["tipo"],
            monto=f["monto"],
            fecha=f["fecha"],
            descripcion=f["descripcion"] or "",
            categoria_id=f["categoria_id"],
            categoria_nombre=f["categoria_nombre"],
        )
        for f in filas
    ]


def eliminar_transaccion(trans_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM transacciones WHERE id = ?", (trans_id,))
    conn.commit()
    conn.close()


# ---------- Presupuestos ----------

def obtener_presupuestos() -> list[Presupuesto]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, categoria_id, monto_maximo FROM presupuestos")
    filas = cur.fetchall()
    conn.close()
    return [
        Presupuesto(
            id=f["id"],
            categoria_id=f["categoria_id"],
            monto_maximo=f["monto_maximo"],
        )
        for f in filas
    ]


def guardar_presupuesto(categoria_id: int, monto_maximo: float) -> Presupuesto:
    conn = get_connection()
    cur = conn.cursor()

    # Si ya existe presupuesto para esa categoría, lo actualizamos
    cur.execute(
        "SELECT id FROM presupuestos WHERE categoria_id = ?",
        (categoria_id,),
    )
    fila = cur.fetchone()
    if fila:
        cur.execute(
            "UPDATE presupuestos SET monto_maximo = ? WHERE id = ?",
            (monto_maximo, fila["id"]),
        )
        presu_id = fila["id"]
    else:
        cur.execute(
            "INSERT INTO presupuestos (categoria_id, monto_maximo) VALUES (?, ?)",
            (categoria_id, monto_maximo),
        )
        presu_id = cur.lastrowid

    conn.commit()
    conn.close()

    return Presupuesto(id=presu_id, categoria_id=categoria_id, monto_maximo=monto_maximo)


# ---------- Alertas ----------

def crear_alerta(
    categoria_id: int | None,
    tipo: str,
    mensaje: str,
    fecha: str,
) -> Alerta:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO alertas (categoria_id, tipo, mensaje, fecha)
        VALUES (?, ?, ?, ?)
        """,
        (categoria_id, tipo, mensaje, fecha),
    )
    conn.commit()
    alerta_id = cur.lastrowid
    conn.close()
    return Alerta(
        id=alerta_id,
        categoria_id=categoria_id,
        tipo=tipo,
        mensaje=mensaje,
        fecha=fecha,
    )


def obtener_alertas() -> list[Alerta]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, categoria_id, tipo, mensaje, fecha
        FROM alertas
        ORDER BY fecha DESC, id DESC
        """
    )
    filas = cur.fetchall()
    conn.close()
    return [
        Alerta(
            id=f["id"],
            categoria_id=f["categoria_id"],
            tipo=f["tipo"],
            mensaje=f["mensaje"],
            fecha=f["fecha"],
        )
        for f in filas
    ]
