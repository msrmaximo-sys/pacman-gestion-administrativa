"""Constantes del formato en disco y de la ventana del juego."""

from pathlib import Path

DATOS = Path(__file__).resolve().parent / "datos"
# Anchos en bytes, no en cantidad de caracteres.
ANCHO_CODIGO = 3
MAX_CODIGO = 999
ANCHO_NOMBRE = 30
ANCHO_USUARIO = 10
ANCHO_CLAVE = 8
ANCHO_ID = 5
ANCHO_NUMERO = 5
ANCHO_PUNTAJE = 6
ANCHO_FECHA = 19
ANCHO_RESULTADO = 8
ANCHO_FILA = 2
ANCHO_COLUMNA = 2
ANCHO_COORDENADA = ANCHO_COLUMNA + ANCHO_FILA + 5  # (XX : YY)
ANCHO_EVENTO = 15
ANCHO_OBSERVACION = 40
ANCHO_PUNTERO = 5
ANCHO_OBJETO = 2
# Cada objeto tiene un ID del 1 al 8 para ubicarlo en las matrices.
OBJ_PACMAN = 1
OBJ_ROJO = 2
OBJ_ROSA = 3
OBJ_CELESTE = 4
OBJ_NARANJA = 5
OBJ_PELLET = 6
OBJ_POWER = 7
OBJ_PARED = 8
NOMBRES_OBJETOS = ["Pac-Man", "Rojo", "Rosa", "Celeste", "Naranja", "Pellet", "Power", "Pared"]
CANTIDAD_OBJETOS = len(NOMBRES_OBJETOS)
MESES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
         "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
# Cada campo indica: nombre, ancho y si es numérico.
CAMPOS_USUARIO = [
    ("codigo", ANCHO_CODIGO, True),
    ("nombre", ANCHO_NOMBRE, False),
    ("usuario", ANCHO_USUARIO, False),
    ("clave", ANCHO_CLAVE, False),
    ("inicial", ANCHO_PUNTERO, True),
    ("final", ANCHO_PUNTERO, True),
]
CAMPOS_PARTIDA = [
    ("id", ANCHO_ID, True),
    ("codigo", ANCHO_CODIGO, True),
    ("numero", ANCHO_NUMERO, True),
    ("puntaje_a", ANCHO_PUNTAJE, True),
    ("puntaje_b", ANCHO_PUNTAJE, True),
    ("fecha", ANCHO_FECHA, False),
    ("resultado", ANCHO_RESULTADO, False),
]
CAMPOS_COLISION = [
    ("id", ANCHO_ID, True),
    ("codigo", ANCHO_CODIGO, True),
    ("usuario", ANCHO_USUARIO, False),
    ("numero", ANCHO_NUMERO, True),
    ("fecha", ANCHO_FECHA, False),
    ("coordenada", ANCHO_COORDENADA, False),
    ("evento", ANCHO_EVENTO, False),
    ("observacion", ANCHO_OBSERVACION, False),
    ("origen", ANCHO_OBJETO, True),
    ("destino", ANCHO_OBJETO, True),
    ("anterior", ANCHO_PUNTERO, True),
    ("siguiente", ANCHO_PUNTERO, True),
]
CAMPOS_ACUMULADOR = [
    ("codigo", ANCHO_CODIGO, True),
    ("usuario", ANCHO_USUARIO, False),
    ("numero", ANCHO_NUMERO, True),
]
# Cada línea termina en LF (un byte), también contado por seek().
FIN_REGISTRO = b"\n"

# Etiquetas abreviadas para que cada título entre en su campo.
ETIQUETAS = {
    "codigo": "#cu", "nombre": "#nombre", "usuario": "#usuario", "clave": "#clave",
    "inicial": "#ini", "final": "#fin", "id": "#id", "numero": "#part",
    "puntaje_a": "#pta", "puntaje_b": "#ptb", "fecha": "#fecha",
    "resultado": "#res", "coordenada": "#coord", "evento": "#evento",
    "observacion": "#observacion", "origen": "#o", "destino": "#d",
    "anterior": "#ant", "siguiente": "#sig",
}


def tamano_registro(campos):
    """Suma campos, espacios separadores y salto de línea."""
    tamano = len(FIN_REGISTRO)
    for nombre, ancho, numerico in campos:
        tamano += ancho + 1
    return tamano


TAMANO_USUARIO = tamano_registro(CAMPOS_USUARIO)
TAMANO_PARTIDA = tamano_registro(CAMPOS_PARTIDA)
TAMANO_COLISION = tamano_registro(CAMPOS_COLISION)
TAMANO_ACUMULADOR = tamano_registro(CAMPOS_ACUMULADOR)

ANCHO_VENTANA = 1280
ALTO_VENTANA = 900
CELDA = 48
ORIGEN_X = 184
ORIGEN_Y = 110
FPS = 60
PASO_JUGADOR_MS = 140
PASO_ENEMIGO_MS = 280
POWER_MS = 7000
PUNTOS_PELLET = 10
PUNTOS_ENEMIGO = 200
NEGRO = (12, 14, 24)
AMARILLO = (255, 215, 30)
BLANCO = (240, 240, 230)
COLOR_POWER = (80, 150, 255)
COLORES_ENEMIGOS = [(255, 70, 70), (255, 150, 200), (50, 220, 220), (255, 160, 60)]
