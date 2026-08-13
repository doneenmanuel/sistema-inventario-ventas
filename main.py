from base_datos import crear_tablas, respaldo
from usuarios import registrar_usuario, iniciar_sesion
from productos import *
from clientes import *
from ventas import registrar_venta, ver_factura, historial_ventas, ventas_del_dia, generar_pdf_factura
from ventas import registrar_venta, ver_factura, historial_ventas, ventas_del_dia, generar_pdf_factura, dashboard_resumen, grafico_ventas_por_mes, grafico_productos_top

# ==================================================
# PANTALLA DE INICIO DE SESIÓN / REGISTRO
# ==================================================
def pantalla_acceso():
    print("\n╔" + "═"*60 + "╗")
    print("║" + " "*8 + "🔐  SISTEMA DE INVENTARIO Y VENTAS" + " "*9 + "║")
    print("╚" + "═"*60 + "╝")
    print("\n¿Qué deseas hacer?")
    print("1. 🔑 Iniciar sesión")
    print("2. 📝 Registrarse (usuario nuevo)")
    print("0. ❌ Salir")

    while True:
        op = input("\nSelecciona una opción: ")
        if op == "2":
            print("\n── 📝 REGISTRAR NUEVO USUARIO ──")
            usuario = input("Nombre de usuario: ")
            clave = input("Contraseña: ")
            nombre = input("Tu nombre completo: ")
            correo = input("Tu correo electrónico: ")
            if registrar_usuario(usuario, clave, nombre, correo):
                print("✅ Ahora puedes iniciar sesión con tus datos.")
        elif op == "1":
            print("\n── 🔑 INICIAR SESIÓN ──")
            usuario = input("Usuario: ")
            clave = input("Contraseña: ")
            datos_usuario = iniciar_sesion(usuario, clave)
            if datos_usuario:
                return datos_usuario  # ✅ Entra al sistema
        elif op == "0":
            print("👋 Hasta pronto.")
            exit()
        else:
            print("⚠️ Opción no válida.")

# ==================================================
# INICIO DEL SISTEMA
# ==================================================
if __name__ == "__main__":
    # Crear tablas y respaldo
    crear_tablas()
    respaldo()

    # 🔐 Pedir inicio de sesión
    usuario_actual = pantalla_acceso()

    # Menú principal
    while True:
        print("\n" + "═"*65)
        print(f"👤 Usuario: {usuario_actual[2]}")
        print("--- 📦 PRODUCTOS ---")
        print(" 1. Agregar producto")
        print(" 2. Ver todos los productos")
        print(" 3. Buscar producto por nombre")
        print(" 4. Editar producto")
        print(" 5. Eliminar producto")
        print(" 6. Reporte de stock bajo")
        print("\n--- 👤 CLIENTES ---")
        print(" 7. Agregar cliente")
        print(" 8. Consultar cliente por ID")
        print(" 9. Buscar cliente por nombre")
        print("10. Editar cliente")
        print("11. Eliminar cliente")
        print("12. Ver todos los clientes")
        print("\n--- 🧾 VENTAS Y FACTURAS ---")
        print("13. Registrar venta (baja stock)")
        print("14. Ver factura en pantalla")
        print("15. 🖨️ Generar Factura en PDF")
        print("16. Ver historial de ventas")
        print("17. Ver ventas totales del día")
        print("18. Dashboard - Resumen General")
        print("19. Gráfico - Ventas por Mes")
        print("20. Gráfico - Productos Más Vendidos")
        print(" 0. Salir y cerrar sistema")
        print("═"*65)

        op = input("Selecciona una opción: ")

        if op == "1":
            agregar_producto(input("Nombre: "), input("Precio: "), input("Stock: "))
        elif op == "2":
            ver_productos()
        elif op == "3":
            buscar_producto(input("Nombre a buscar: "))
        elif op == "4":
            editar_producto(int(input("ID: ")), input("Nuevo nombre: "), input("Nuevo precio: "), input("Nuevo stock: "))
        elif op == "5":
            eliminar_producto(int(input("ID: ")))
        elif op == "6":
            lim = input("Límite de stock [10]: ")
            reporte_stock_bajo(int(lim) if lim else 10)
        elif op == "7":
            agregar_cliente(input("Nombre: "), input("Teléfono: "), input("Dirección: "))
        elif op == "8":
            consultar_cliente(int(input("ID: ")))
        elif op == "9":
            buscar_cliente(input("Nombre a buscar: "))
        elif op == "10":
            editar_cliente(int(input("ID: ")), input("Nuevo nombre: "), input("Teléfono: "), input("Dirección: "))
        elif op == "11":
            eliminar_cliente(int(input("ID: ")))
        elif op == "12":
            ver_todos_clientes()
        elif op == "13":
            id_cli = int(input("ID del cliente: "))
            print("👉 Escribe 0 en ID para terminar")
            items = []
            while True:
                pid = input("ID Producto: ")
                if pid == "0": break
                items.append((int(pid), int(input("Cantidad: "))))
            registrar_venta(id_cli, items)
        elif op == "14":
            ver_factura(int(input("N° Factura: ")))
        elif op == "15":
            generar_pdf_factura(int(input("N° Factura: ")))
        elif op == "16":
            historial_ventas()
        elif op == "17":
            ventas_del_dia()
        elif op == "18":
            dashboard_resumen()
        elif op == "19":
            grafico_ventas_por_mes()
        elif op == "20":
            grafico_productos_top()
        elif op == "0":
            print("\n💾 Guardando respaldo...")
            respaldo()
            print("👋 ¡Gracias por usar el sistema!")
            break
        else:
            print("⚠️ Opción no válida.")