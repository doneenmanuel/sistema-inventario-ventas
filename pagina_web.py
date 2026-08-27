import streamlit as st
from base_datos import conectar

# ==================================================
# CONFIGURACIÓN DE LA PÁGINA
# ==================================================
st.set_page_config(
    page_title="Mi Tienda - Productos Disponibles",
    page_icon="🛒",
    layout="wide"
)

st.markdown("""
    <h1 style='text-align: center; color: #2E86AB;'>🛒 CATÁLOGO DE PRODUCTOS</h1>
    <p style='text-align: center; font-size: 18px;'>Consulta nuestros productos disponibles y precios</p>
    <hr style='border: 2px solid #2E86AB;'>
""", unsafe_allow_html=True)

# ==================================================
# MOSTRAR PRODUCTOS DESDE TU BASE DE DATOS
# ==================================================
conn = conectar()
c = conn.cursor()
c.execute("SELECT nombre, precio, stock FROM producto WHERE stock > 0 ORDER BY nombre")
productos = c.fetchall()
conn.close()

if not productos:
    st.info("📦 No hay productos disponibles por el momento.")
else:
    col1, col2, col3 = st.columns(3)
    columnas = [col1, col2, col3]
    contador = 0

    for prod in productos:
        nombre, precio, stock = prod
        with columnas[contador % 3]:
            st.markdown(f"""
            <div style='border: 1px solid #ddd; border-radius: 10px; padding: 15px; margin: 10px 0; background-color: #f9f9f9;'>
                <h3 style='color: #333;'>{nombre}</h3>
                <p style='font-size: 22px; font-weight: bold; color: #E63946;'>RD$ {precio:,.2f}</p>
                <p style='color: #555;'>📦 Disponible: {stock} unidades</p>
            </div>
            """, unsafe_allow_html=True)
        contador += 1

st.markdown("---")
st.markdown("""
<p style='text-align: center;'>📍 Página generada desde tu Sistema de Inventario y Ventas</p>
<p style='text-align: center; font-size: 12px;'>Actualizado automáticamente desde tu sistema</p>
""", unsafe_allow_html=True)