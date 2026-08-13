import sqlite3
import shutil
from datetime import datetime

# Conectar base de datos
def conectar():
    return sqlite3.connect("inventario.db")

# Crear todas las tablas si no existen
def crear_tablas():
    conn = conectar()
    c = conn.cursor()

    # Tabla de USUARIOS (NUEVA)
    c.execute("""
    CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL UNIQUE,
        contrasena TEXT NOT NULL,
        nombre_completo TEXT,
        correo TEXT,
        fecha_registro TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS cliente (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        telefono TEXT,
        direccion TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS producto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL,
        stock INTEGER NOT NULL DEFAULT 0
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS factura (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        total REAL NOT NULL
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS detalle_factura (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_factura INTEGER NOT NULL,
        id_producto INTEGER NOT NULL,
        cantidad INTEGER NOT NULL,
        precio_unitario REAL NOT NULL,
        subtotal REAL NOT NULL
    )
    """)

    conn.commit()
    conn.close()

# Copia de seguridad
def respaldo():
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    origen = "inventario.db"
    destino = f"respaldo_inventario_{fecha}.db"
    try:
        shutil.copy2(origen, destino)
        print(f"💾 Copia de seguridad: {destino}")
    except Exception as e:
        print(f"⚠️ Error al crear respaldo: {e}")