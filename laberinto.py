# Símbolos: # pared, . pellet, o power y espacio vacío.
# Grilla del escenario; las matrices administrativas quedan para otra etapa.
MAPA = [
    "###################",
    "# .......#....... #",
    "#.##.###.#.###.##.#",
    "#.................#",
    "#.##.#.#####.#.##.#",
    "#....#...#...#....#",
    "####.###.#.###.####",
    "#........o........#",
    "####.#.#####.#.####",
    "#....#...#...#....#",
    "#.##.###.#.###.##.#",
    "#.................#",
    "#.##.#.#####.#.##.#",
    "# ...#.......#... #",
    "###################",
]
INICIO_JUGADOR = (7, 1)
INICIOS_ENEMIGOS = [(1, 1), (1, 17), (13, 1), (13, 17)]
DIRECCIONES = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def es_camino(fila, columna):
    """Comprueba los límites y luego la pared de la celda."""
    if fila < 0 or fila >= len(MAPA):
        return False
    if columna < 0 or columna >= len(MAPA[fila]):
        return False
    return MAPA[fila][columna] != "#"


def crear_pellets():
    """Crea los alimentos nuevamente en cada partida."""
    # Los conjuntos permiten buscar y retirar una posición sin duplicados.
    pellets = set()
    powers = set()
    for fila in range(len(MAPA)):
        for columna in range(len(MAPA[fila])):
            if MAPA[fila][columna] == ".":
                pellets.add((fila, columna))
            elif MAPA[fila][columna] == "o":
                powers.add((fila, columna))
    pellets.discard(INICIO_JUGADOR)
    return pellets, powers
