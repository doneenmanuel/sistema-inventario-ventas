from base_datos import conectar

def agregar_producto(nombre, precio, stock):
    conn = conectar()
    c = conn.cursor()
    c.execute("INSERT INTO producto VALUES (NULL, ?, ?, ?)",
              (nombre, float(precio), int(stock)))
    conn.commit()
    ultimo_id = c.lastrowid
    conn.close()
    print(f"✅ Producto agregado | ID: {ultimo_id} | {nombre}")

def ver_productos():
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT * FROM producto ORDER BY nombre")
    lista = c.fetchall()
    conn.close()
    print("\n" + "="*65)
    print(f"{'ID':<5} | {'Nombre':<30} | {'Precio':<12} | {'Stock':<8}")
    print("-"*65)
    for p in lista:
        print(f"{p[0]:<5} | {p[1]:<30} | RD$ {p[2]:<9,.2f} | {p[3]:<8}")
    print("="*65)

def buscar_producto(nombre_parcial):
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT * FROM producto WHERE nombre LIKE ? ORDER BY nombre",
              (f"%{nombre_parcial}%",))
    lista = c.fetchall()
    conn.close()
    if lista:
        print("\n🔍 Productos encontrados:")
        print("-"*55)
        print(f"{'ID':<5} | {'Nombre':<30} | {'Precio':<10} | {'Stock'}")
        print("-"*55)
        for p in lista:
            print(f"{p[0]:<5} | {p[1]:<30} | RD$ {p[2]:,.2f} | {p[3]}")
    else:
        print("❌ Sin resultados.")

def editar_producto(id_prod, nombre_nuevo, precio_nuevo, stock_nuevo):
    conn = conectar()
    c = conn.cursor()
    c.execute("UPDATE producto SET nombre=?, precio=?, stock=? WHERE id=?",
              (nombre_nuevo, float(precio_nuevo), int(stock_nuevo), id_prod))
    conn.commit()
    filas = c.rowcount
    conn.close()
    print("✅ Producto actualizado!" if filas > 0 else "❌ Producto no encontrado.")

def eliminar_producto(id_prod):
    conn = conectar()
    c = conn.cursor()
    c.execute("DELETE FROM producto WHERE id=?", (id_prod,))
    conn.commit()
    filas = c.rowcount
    conn.close()
    print("✅ Producto eliminado!" if filas > 0 else "❌ Producto no encontrado.")

def reporte_stock_bajo(limite=10):
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT * FROM producto WHERE stock <= ? ORDER BY stock", (limite,))
    lista = c.fetchall()
    conn.close()
    print(f"\n⚠️ Productos con stock ≤ {limite}:")
    if lista:
        print("-"*50)
        print(f"{'ID':<5} | {'Nombre':<30} | {'Stock'}")
        print("-"*50)
        for p in lista:
            print(f"{p[0]:<5} | {p[1]:<30} | {p[3]}")
    else:
        print("✅ Todos tienen buen stock.")