"""Alta y consulta del maestro. Sin bajas, código y posición son iguales."""

import config
from archivos_fijos import leer_registro, escribir_registro, contar_registros, codificar, decodificar


def listar_usuarios():
    """Lee el padrón en orden de código."""
    usuarios = []
    with (config.DATOS / "maestro_usuarios.txt").open("rb") as archivo:
        cantidad = contar_registros(archivo, config.TAMANO_USUARIO)
        for posicion in range(1, cantidad + 1):
            datos = leer_registro(archivo, posicion, config.TAMANO_USUARIO)
            usuario = decodificar(datos, config.CAMPOS_USUARIO)
            if usuario["codigo"] != posicion:
                raise ValueError("El maestro de usuarios está fuera de orden.")
            usuarios.append(usuario)
    return usuarios


def registrar_usuario(nombre, usuario, clave):
    """Agrega el usuario con inicio y final vacíos dentro del mismo maestro."""
    nombre = nombre.strip()
    usuario = usuario.strip()
    clave = clave.strip()
    if not nombre or not usuario or not clave:
        raise ValueError("Todos los campos son obligatorios.")
    usuarios = listar_usuarios()
    for existente in usuarios:
        if existente["usuario"].casefold() == usuario.casefold():
            raise ValueError("Ese usuario ya existe.")
    codigo = len(usuarios) + 1
    if codigo > config.MAX_CODIGO:
        raise ValueError("Se alcanzó el límite de usuarios: códigos 001 a 999.")
    registro = {"codigo": codigo, "nombre": nombre, "usuario": usuario, "clave": clave, "inicial": 0, "final": 0}
    datos = codificar(registro, config.CAMPOS_USUARIO)
    with (config.DATOS / "maestro_usuarios.txt").open("r+b") as archivo:
        escribir_registro(archivo, codigo, config.TAMANO_USUARIO, datos)
    return registro


def iniciar_sesion(usuario, clave):
    """Comprueba las credenciales del archivo de usuarios."""
    for registro in listar_usuarios():
        if registro["usuario"].casefold() == usuario.strip().casefold():
            if registro["clave"] == clave.strip():
                return registro
    return None


def obtener_usuario(codigo):
    """Lee directamente el usuario: su código coincide con la posición."""
    if codigo < 1 or codigo > config.MAX_CODIGO:
        raise ValueError("Código de usuario inválido.")
    with (config.DATOS / "maestro_usuarios.txt").open("rb") as archivo:
        datos = leer_registro(archivo, codigo, config.TAMANO_USUARIO)
    if not datos:
        raise ValueError("Usuario inexistente.")
    usuario = decodificar(datos, config.CAMPOS_USUARIO)
    if usuario["codigo"] != codigo:
        raise ValueError("El código no coincide con la posición del maestro.")
    return usuario
