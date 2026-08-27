from base_datos import conectar

conn = conectar()
c = conn.cursor()

# ✅ Agregar columna numero_factura si no existe
try:
    c.execute("ALTER TABLE pedidos ADD COLUMN numero_factura TEXT UNIQUE")
    print("✅ numero_factura agregada")
except Exception as e:
    print(f"ℹ️ numero_factura ya existe: {e}")

# ✅ Agregar columna estado si no existe
try:
    c.execute("ALTER TABLE pedidos ADD COLUMN estado TEXT DEFAULT 'PENDIENTE'")
    print("✅ estado agregada")
except Exception as e:
    print(f"ℹ️ estado ya existe: {e}")

conn.commit()
conn.close()
print("\n✅ BASE DE DATOS ACTUALIZADA — ¡Listo para funcionar!")