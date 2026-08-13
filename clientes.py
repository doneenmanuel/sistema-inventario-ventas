from base_datos import conectar

def agregar_cliente(nombre, telefono="", direccion=""):
    conn = conectar()
    c = conn.cursor()
    c.execute("INSERT INTO cliente VALUES (NULL, ?, ?, ?)",
              (nombre, telefono, direccion))
    conn.commit()
    ultimo_id = c.lastrowid
    conn.close()
    print(f"✅ Cliente agregado | ID: {ultimo_id} | {nombre}")

def consultar_cliente(id_cliente):
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT * FROM cliente WHERE id=?", (id_cliente,))
    cli = c.fetchone()
    conn.close()
    if cli:
        print(f"\n👤 Cliente ID: {cli[0]}")
        print(f"   Nombre: {cli[1]}")
        print(f"   Teléfono: {cli[2]}")
        print(f"   Dirección: {cli[3]}")
    else:
        print("❌ Cliente no encontrado.")

def buscar_cliente(nombre_parcial):
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT id, nombre, telefono FROM cliente WHERE nombre LIKE ? ORDER BY nombre",
              (f"%{nombre_parcial}%",))
    lista = c.fetchall()
    conn.close()
    if lista:
        print("\n🔍 Clientes encontrados:")
        print("-"*50)
        print(f"{'ID':<5} | {'Nombre':<30} | {'Teléfono'}")
        print("-"*50)
        for c in lista:
            print(f"{c[0]:<5} | {c[1]:<30} | {c[2]}")
    else:
        print("❌ Sin resultados.")

def editar_cliente(id_cliente, nombre_nuevo, tel_nuevo, dir_nueva):
    conn = conectar()
    c = conn.cursor()
    c.execute("UPDATE cliente SET nombre=?, telefono=?, direccion=? WHERE id=?",
              (nombre_nuevo, tel_nuevo, dir_nueva, id_cliente))
    conn.commit()
    ok = c.rowcount > 0
    conn.close()
    print("✅ Cliente actualizado!" if ok else "❌ Cliente no encontrado.")

def eliminar_cliente(id_cliente):
    conn = conectar()
    c = conn.cursor()
    c.execute("DELETE FROM cliente WHERE id=?", (id_cliente,))
    conn.commit()
    ok = c.rowcount > 0
    conn.close()
    print("✅ Cliente eliminado!" if ok else "❌ Cliente no encontrado.")

def ver_todos_clientes():
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT id, nombre, telefono FROM cliente ORDER BY nombre")
    lista = c.fetchall()
    conn.close()
    print("\n" + "="*55)
    print(f"{'ID':<5} | {'Nombre':<35} | {'Teléfono'}")
    print("-"*55)
    for c in lista:
        print(f"{c[0]:<5} | {c[1]:<35} | {c[2]}")
    print("="*55)