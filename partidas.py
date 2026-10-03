"""El acumulador reserva partidas; el detalle guarda sus resultados finales."""

from datetime import datetime
import config
from usuarios import obtener_usuario
from archivos_fijos import leer_registro, escribir_registro, contar_registros, codificar, decodificar


def nueva_partida(codigo):
    """Incrementa el acumulador global y devuelve la próxima partida del usuario."""
    usuario = obtener_usuario(codigo)
    with (config.DATOS / "acumulador_partidas.txt").open("r+b") as archivo:
        cantidad = contar_registros(archivo, config.TAMANO_ACUMULADOR)
        numero = 1
        if cantidad > 0:
            datos = leer_registro(archivo, cantidad, config.TAMANO_ACUMULADOR)
            numero = decodificar(datos, config.CAMPOS_ACUMULADOR)["numero"] + 1
        # Contar los inicios del usuario evita reutilizar una partida interrumpida.
        numero_usuario = 1
        for posicion in range(1, cantidad + 1):
            datos = leer_registro(archivo, posicion, config.TAMANO_ACUMULADOR)
            inicio = decodificar(datos, config.CAMPOS_ACUMULADOR)
            if inicio["codigo"] == codigo:
                numero_usuario += 1
        datos = codificar({"codigo": codigo, "usuario": usuario["usuario"], "numero": numero}, config.CAMPOS_ACUMULADOR)
        escribir_registro(archivo, cantidad + 1, config.TAMANO_ACUMULADOR, datos)
    return numero_usuario


def guardar_partida(codigo, numero, puntaje_a, puntaje_b, resultado):
    """Guarda el resultado final con un identificador de registro propio."""
    if resultado not in ("victoria", "derrota"):
        raise ValueError("Resultado inválido.")
    obtener_usuario(codigo)
    if numero < 1:
        raise ValueError("El número de partida debe comenzar en 1.")
    with (config.DATOS / "partida_jugador.txt").open("r+b") as archivo:
        posicion = contar_registros(archivo, config.TAMANO_PARTIDA) + 1
        # Si ya existe ese usuario y partida, conserva su ID y actualiza el detalle.
        for partida in listar_partidas(codigo):
            if partida["numero"] == numero:
                posicion = partida["id"]
                break
        registro = {"id": posicion, "codigo": codigo, "numero": numero,
                    "puntaje_a": puntaje_a, "puntaje_b": puntaje_b,
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "resultado": resultado}
        datos = codificar(registro, config.CAMPOS_PARTIDA)
        escribir_registro(archivo, posicion, config.TAMANO_PARTIDA, datos)


def listar_partidas(codigo=None):
    """Devuelve todas las partidas o solamente las de un usuario."""
    partidas = []
    with (config.DATOS / "partida_jugador.txt").open("rb") as archivo:
        cantidad = contar_registros(archivo, config.TAMANO_PARTIDA)
        for posicion in range(1, cantidad + 1):
            datos = leer_registro(archivo, posicion, config.TAMANO_PARTIDA)
            registro = decodificar(datos, config.CAMPOS_PARTIDA)
            if registro["id"] != posicion:
                raise ValueError("El ID de partida no coincide con su posición.")
            if codigo is None or registro["codigo"] == codigo:
                partidas.append(registro)
    return partidas
