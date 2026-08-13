from base_datos import conectar
from datetime import datetime
import hashlib

# Cifrar contraseña
def cifrar_clave(clave):
    return hashlib.sha256(clave.encode()).hexdigest()

# Registrar nuevo usuario
def registrar_usuario(usuario, contrasena, nombre_completo="", correo=""):
    conn = conectar()
    c = conn.cursor()
    fecha_reg = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    clave_cifrada = cifrar_clave(contrasena)
    try:
        c.execute("""
            INSERT INTO usuario (usuario, contrasena, nombre_completo, correo, fecha_registro)
            VALUES (?, ?, ?, ?, ?)
        """, (usuario, clave_cifrada, nombre_completo, correo, fecha_reg))
        conn.commit()
        print(f"✅ Usuario registrado correctamente! ID: {c.lastrowid}")
        return True
    except sqlite3.IntegrityError:
        print("❌ Ese nombre de usuario YA EXISTE. Usa otro.")
        return False
    finally:
        conn.close()

# Iniciar sesión
def iniciar_sesion(usuario, contrasena):
    conn = conectar()
    c = conn.cursor()
    clave_cifrada = cifrar_clave(contrasena)
    c.execute("""
        SELECT id, usuario, nombre_completo, correo FROM usuario
        WHERE usuario = ? AND contrasena = ?
    """, (usuario, clave_cifrada))
    usuario_encontrado = c.fetchone()
    conn.close()
    if usuario_encontrado:
        print(f"✅ ¡Bienvenido/a {usuario_encontrado[2]}!")
        return usuario_encontrado
    else:
        print("❌ Usuario o contraseña INCORRECTOS.")
        return None