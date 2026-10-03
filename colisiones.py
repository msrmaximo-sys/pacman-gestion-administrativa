"""El maestro guarda los extremos; cada colisión guarda anterior y siguiente."""

from datetime import datetime
import config
from usuarios import obtener_usuario
from archivos_fijos import leer_registro, escribir_registro, contar_registros, codificar, decodificar


def guardar_colision(codigo, numero, evento):
    """Agrega la colisión y enlaza directamente la última del usuario."""
    usuario = obtener_usuario(codigo)
    anterior = usuario["final"]
    if numero < 1:
        raise ValueError("La partida debe comenzar en 1.")
    validar_objetos(evento)
    with (config.DATOS / "colisiones.txt").open("r+b") as archivo:
        posicion = contar_registros(archivo, config.TAMANO_COLISION) + 1
        # Comprueba la última colisión antes de modificar archivos.
        if anterior != 0:
            datos = leer_registro(archivo, anterior, config.TAMANO_COLISION)
            ultimo = decodificar(datos, config.CAMPOS_COLISION)
            if ultimo["codigo"] != codigo or ultimo["id"] != anterior or ultimo["siguiente"] != 0:
                raise ValueError("El último enlace de colisiones está dañado.")
        elif usuario["inicial"] != 0:
            raise ValueError("La cadena tiene inicio pero no tiene final.")
        registro = dict(evento)
        registro.update({"id": posicion, "codigo": codigo, "usuario": usuario["usuario"],
                         "numero": numero, "anterior": anterior, "siguiente": 0})
        datos = codificar(registro, config.CAMPOS_COLISION)
        escribir_registro(archivo, posicion, config.TAMANO_COLISION, datos)
        if anterior == 0:
            usuario["inicial"] = posicion
        else:
            # No recorre el historial: salta al registro anterior y actualiza su enlace.
            ultimo["siguiente"] = posicion
            datos = codificar(ultimo, config.CAMPOS_COLISION)
            escribir_registro(archivo, anterior, config.TAMANO_COLISION, datos)
    usuario["final"] = posicion
    with (config.DATOS / "maestro_usuarios.txt").open("r+b") as maestro:
        datos = codificar(usuario, config.CAMPOS_USUARIO)
        escribir_registro(maestro, codigo, config.TAMANO_USUARIO, datos)


def historial_usuario(codigo):
    """Lee el maestro y sigue solamente la cadena del usuario con seek()."""
    usuario = obtener_usuario(codigo)
    posicion = usuario["inicial"]
    anterior = 0
    historial = []
    with (config.DATOS / "colisiones.txt").open("rb") as archivo:
        while posicion != 0:
            datos = leer_registro(archivo, posicion, config.TAMANO_COLISION)
            registro = decodificar(datos, config.CAMPOS_COLISION)
            if registro["codigo"] != codigo or registro["id"] != posicion or registro["anterior"] != anterior:
                raise ValueError("La cadena contiene una colisión o enlace incorrecto.")
            validar_objetos(registro)
            historial.append(registro)
            siguiente = registro["siguiente"]
            if siguiente != 0 and siguiente <= posicion:
                raise ValueError("Cadena de colisiones dañada.")
            anterior = posicion
            posicion = siguiente
    if anterior != usuario["final"]:
        raise ValueError("La cadena no termina en la posición final del usuario.")
    return historial


def validar_objetos(evento):
    """Comprueba que cada contacto tenga los dos objetos correctos."""
    if evento["origen"] != config.OBJ_PACMAN:
        raise ValueError("El origen de estos contactos debe ser Pac-Man.")
    destino = evento["destino"]
    tipo = evento["evento"]
    if tipo in ("CHOQUE", "ENEMIGO_COMIDO"):
        if destino not in (config.OBJ_ROJO, config.OBJ_ROSA, config.OBJ_CELESTE, config.OBJ_NARANJA):
            raise ValueError("El destino debe ser un fantasma.")
    else:
        destinos = {"PELLET": config.OBJ_PELLET, "POWER": config.OBJ_POWER, "PARED": config.OBJ_PARED}
        if tipo not in destinos or destino != destinos[tipo]:
            raise ValueError("El objeto no corresponde al tipo de evento.")


def crear_evento(fila, columna, tipo, observacion, destino=None):
    """Conserva hora, coordenada y participantes para los informes posteriores."""
    destinos = {"PELLET": config.OBJ_PELLET, "POWER": config.OBJ_POWER, "PARED": config.OBJ_PARED}
    if tipo in destinos:
        destino = destinos[tipo]
    x = str(columna).zfill(config.ANCHO_COLUMNA)
    y = str(fila).zfill(config.ANCHO_FILA)
    evento = {"fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
              "coordenada": f"({x} : {y})", "evento": tipo, "observacion": observacion,
              "origen": config.OBJ_PACMAN, "destino": destino}
    validar_objetos(evento)
    return evento
