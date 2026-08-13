from base_datos import conectar
from datetime import datetime
from fpdf import FPDF
import os

# ==================================================
# ✅ Registrar Venta
# ==================================================
def registrar_venta(id_cliente, items):
    conn = conectar()
    c = conn.cursor()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total = 0
    c.execute("INSERT INTO factura VALUES (NULL, ?, ?, 0)", (id_cliente, fecha))
    id_factura = c.lastrowid

    for id_prod, cant in items:
        c.execute("SELECT nombre, precio, stock FROM producto WHERE id=?", (id_prod,))
        prod = c.fetchone()
        if not prod:
            print(f"⚠️ Producto ID {id_prod} no existe → omitido")
            continue
        nombre, precio, stock = prod
        if stock < cant:
            print(f"⚠️ Sin stock: {nombre} → Disponible: {stock}")
            continue
        subtotal = precio * cant
        total += subtotal
        c.execute("INSERT INTO detalle_factura VALUES (NULL, ?, ?, ?, ?, ?)",
                  (id_factura, id_prod, cant, precio, subtotal))
        c.execute("UPDATE producto SET stock=? WHERE id=?", (stock - cant, id_prod))
        print(f"📦 {nombre}: Stock {stock} → {stock - cant}")

    c.execute("UPDATE factura SET total=? WHERE id=?", (total, id_factura))
    conn.commit()
    conn.close()
    print(f"\n✅ Venta registrada! Factura N° {id_factura} | Total: RD$ {total:,.2f}")
    return id_factura

# ==================================================
# ✅ Ver Factura en Pantalla
# ==================================================
def ver_factura(id_factura):
    conn = conectar()
    c = conn.cursor()
    c.execute("""
        SELECT f.id, f.fecha, f.total, c.nombre, c.telefono
        FROM factura f JOIN cliente c ON f.id_cliente=c.id WHERE f.id=?
    """, (id_factura,))
    cab = c.fetchone()
    if not cab:
        print("❌ Factura no encontrada.")
        conn.close()
        return
    c.execute("""
        SELECT p.nombre, d.cantidad, d.precio_unitario, d.subtotal
        FROM detalle_factura d JOIN producto p ON d.id_producto=p.id WHERE d.id_factura=?
    """, (id_factura,))
    det = c.fetchall()
    conn.close()

    print("\n" + "="*60)
    print("                F A C T U R A")
    print("="*60)
    print(f"N° {cab[0]:<6}         Fecha: {cab[1]}")
    print(f"Cliente: {cab[3]}")
    print(f"Teléfono: {cab[4]}")
    print("-"*60)
    print(f"{'Producto':<25} | {'Cant':<4} | {'Precio':<10} | {'Subtotal'}")
    print("-"*60)
    for d in det:
        print(f"{d[0]:<25} | {d[1]:<4} | RD$ {d[2]:<7,.2f} | RD$ {d[3]:,.2f}")
    print("-"*60)
    print(f"{'TOTAL':<43} RD$ {cab[2]:,.2f}")
    print("="*60)

# ==================================================
# ✅ Historial de Ventas
# ==================================================
def historial_ventas():
    conn = conectar()
    c = conn.cursor()
    c.execute("""
        SELECT f.id, f.fecha, c.nombre, f.total
        FROM factura f JOIN cliente c ON f.id_cliente=c.id ORDER BY f.id DESC
    """)
    lista = c.fetchall()
    conn.close()
    if not lista:
        print("📋 Sin ventas registradas.")
        return
    print("\n" + "="*70)
    print("             📋 HISTORIAL DE VENTAS")
    print("="*70)
    print(f"{'N°':<5} | {'Fecha y Hora':<20} | {'Cliente':<25} | {'Total'}")
    print("-"*70)
    for f in lista:
        print(f"{f[0]:<5} | {f[1]:<20} | {f[2]:<25} | RD$ {f[3]:,.2f}")
    print("="*70)

# ==================================================
# ✅ Ventas del Día
# ==================================================
def ventas_del_dia():
    hoy = datetime.now().strftime("%Y-%m-%d")
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT SUM(total), COUNT(*) FROM factura WHERE fecha LIKE ?", (f"{hoy}%",))
    total, cant = c.fetchone()
    conn.close()
    total = total or 0
    cant = cant or 0
    print(f"\n💰 Ventas del día ({hoy}):")
    print(f"   Facturas: {cant}")
    print(f"   Total: RD$ {total:,.2f}")

# ==================================================
# ✅ Generar Factura en PDF
# ==================================================
def generar_pdf_factura(id_factura):
    conn = conectar()
    c = conn.cursor()

    c.execute("""
        SELECT f.id, f.fecha, f.total, c.nombre, c.telefono, c.direccion
        FROM factura f JOIN cliente c ON f.id_cliente = c.id WHERE f.id = ?
    """, (id_factura,))
    cab = c.fetchone()
    if not cab:
        print("❌ Factura no encontrada.")
        conn.close()
        return None

    c.execute("""
        SELECT p.nombre, d.cantidad, d.precio_unitario, d.subtotal
        FROM detalle_factura d JOIN producto p ON d.id_producto = p.id
        WHERE d.id_factura = ?
    """, (id_factura,))
    detalles = c.fetchall()
    conn.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)

    pdf.cell(0, 10, txt="F A C T U R A", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", size=10)

    pdf.cell(95, 8, txt=f"N° Factura: {cab[0]}")
    pdf.cell(95, 8, txt=f"Fecha: {cab[1]}", ln=True)
    pdf.cell(95, 8, txt=f"Cliente: {cab[3]}")
    pdf.cell(95, 8, txt=f"Teléfono: {cab[4]}", ln=True)
    pdf.cell(95, 8, txt=f"Dirección: {cab[5]}", ln=True)
    pdf.ln(5)

    pdf.set_fill_color(230, 230, 230)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(80, 10, txt="Producto", border=1, fill=True)
    pdf.cell(25, 10, txt="Cant", border=1, fill=True, align="C")
    pdf.cell(40, 10, txt="Precio", border=1, fill=True, align="C")
    pdf.cell(45, 10, txt="Subtotal", border=1, fill=True, align="C")
    pdf.ln()

    pdf.set_font("Arial", size=10)
    for d in detalles:
        pdf.cell(80, 8, txt=str(d[0]), border=1)
        pdf.cell(25, 8, txt=str(d[1]), border=1, align="C")
        pdf.cell(40, 8, txt=f"RD$ {d[2]:,.2f}", border=1, align="C")
        pdf.cell(45, 8, txt=f"RD$ {d[3]:,.2f}", border=1, align="C")
        pdf.ln()

    pdf.ln(3)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(145, 10, txt="TOTAL:")
    pdf.cell(45, 10, txt=f"RD$ {cab[2]:,.2f}", align="C")

    nombre_archivo = f"Factura_N{id_factura}.pdf"
    pdf.output(nombre_archivo)
    ruta_completa = os.path.abspath(nombre_archivo)
    print(f"\n✅ PDF generado exitosamente!")
    print(f"📄 Archivo: {ruta_completa}")
    return nombre_archivo
import matplotlib.pyplot as plt

# ==================================================
# 📊 DASHBOARD — RESUMEN GENERAL
# ==================================================
def dashboard_resumen():
    conn = conectar()
    c = conn.cursor()

    # Total de productos
    c.execute("SELECT COUNT(*), SUM(stock) FROM producto")
    prod = c.fetchone()
    total_prod = prod[0] or 0
    total_stock = prod[1] or 0

    # Total de clientes
    c.execute("SELECT COUNT(*) FROM cliente")
    total_clientes = c.fetchone()[0] or 0

    # Total de facturas y monto global
    c.execute("SELECT COUNT(*), SUM(total) FROM factura")
    fac = c.fetchone()
    total_facturas = fac[0] or 0
    total_global = fac[1] or 0

    conn.close()

    print("\n" + "═"*60)
    print("                📊 DASHBOARD — RESUMEN GENERAL")
    print("═"*60)
    print(f"📦 Productos registrados: {total_prod}")
    print(f"📦 Unidades en stock:     {total_stock}")
    print(f"👤 Clientes registrados:  {total_clientes}")
    print(f"🧾 Facturas emitidas:     {total_facturas}")
    print(f"💰 TOTAL VENDIDO:         RD$ {total_global:,.2f}")
    print("═"*60)
    return total_prod, total_clientes, total_facturas, total_global

# ==================================================
# 📈 GRÁFICO: Ventas por Mes
# ==================================================
def grafico_ventas_por_mes():
    conn = conectar()
    c = conn.cursor()
    c.execute("""
        SELECT strftime('%Y-%m', fecha) as mes, SUM(total)
        FROM factura
        GROUP BY mes
        ORDER BY mes
    """)
    datos = c.fetchall()
    conn.close()

    if not datos:
        print("📋 No hay ventas registradas para graficar.")
        return

    meses = [d[0] for d in datos]
    totales = [d[1] for d in datos]

    plt.figure(figsize=(10, 6))
    plt.bar(meses, totales, color='#2E86AB')
    plt.title('📊 VENTAS POR MES', fontsize=16, fontweight='bold')
    plt.xlabel('Mes', fontsize=12)
    plt.ylabel('Total Vendido (RD$)', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()

# ==================================================
# 🏆 GRÁFICO: Productos Más Vendidos
# ==================================================
def grafico_productos_top():
    conn = conectar()
    c = conn.cursor()
    c.execute("""
        SELECT p.nombre, SUM(d.cantidad) as cant
        FROM detalle_factura d
        JOIN producto p ON d.id_producto = p.id
        GROUP BY d.id_producto
        ORDER BY cant DESC
        LIMIT 5
    """)
    datos = c.fetchall()
    conn.close()

    if not datos:
        print("📋 No hay ventas registradas para graficar.")
        return

    nombres = [d[0] for d in datos]
    cantidades = [d[1] for d in datos]
    colores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']

    plt.figure(figsize=(10, 6))
    plt.barh(nombres, cantidades, color=colores)
    plt.title('🏆 TOP 5 PRODUCTOS MÁS VENDIDOS', fontsize=16, fontweight='bold')
    plt.xlabel('Cantidad Vendida', fontsize=12)
    plt.tight_layout()
    plt.show()