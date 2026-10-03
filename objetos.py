"""Posiciones de la grilla y movimiento; estas clases no escriben archivos."""

import random
from laberinto import es_camino, DIRECCIONES


class Jugador:
    def __init__(self, fila, columna):
        """Guarda la posición en celdas."""
        self.fila = fila
        self.columna = columna
        self.direccion = (0, 1)  # Orientación de la boca, incluso estando quieto.
        self.movimiento = (0, 0)
        # La posición visual puede estar entre dos celdas; la lógica usa enteros.
        self.fila_visual = float(fila)
        self.columna_visual = float(columna)

    def mover(self, direccion):
        """Guarda el giro posible y sigue avanzando sin mantener la tecla."""
        fila_pedida = self.fila + direccion[0]
        columna_pedida = self.columna + direccion[1]
        if direccion != (0, 0):
            if es_camino(fila_pedida, columna_pedida):
                self.movimiento = direccion
                self.direccion = direccion
        # Si el giro pedido está bloqueado, conserva el movimiento anterior.
        fila = self.fila + self.movimiento[0]
        columna = self.columna + self.movimiento[1]
        if es_camino(fila, columna):
            self.fila = fila
            self.columna = columna
        elif self.movimiento != (0, 0):
            self.movimiento = (0, 0)  # Registra la pared una vez, no en cada cuadro.
            return "PARED"
        return None


class Enemigo:
    def __init__(self, fila, columna, color, codigo_objeto):
        """Conserva su inicio para reaparecer después de ser comido."""
        self.fila = fila
        self.columna = columna
        self.inicio = (fila, columna)
        self.color = color
        self.codigo_objeto = codigo_objeto  # ID usado en las matrices, no en el movimiento.
        self.fila_visual = float(fila)
        self.columna_visual = float(columna)

    def mover(self):
        """Elige al azar entre los caminos vecinos disponibles."""
        opciones = []
        for cambio_fila, cambio_columna in DIRECCIONES:
            fila = self.fila + cambio_fila
            columna = self.columna + cambio_columna
            if es_camino(fila, columna):
                opciones.append((fila, columna))
        if opciones:
            self.fila, self.columna = random.choice(opciones)

    def reaparecer(self, jugador):
        """Evita reaparecer encima del jugador si ocupa su inicio."""
        self.fila, self.columna = self.inicio
        if (self.fila, self.columna) == (jugador.fila, jugador.columna):
            self.mover()
        self.fila_visual = float(self.fila)
        self.columna_visual = float(self.columna)


def actualizar_dibujo(objeto, milisegundos, duracion_paso):
    """Acerca el dibujo a la celda destino en cada cuadro para evitar saltos."""
    avance = milisegundos / duracion_paso
    objeto.fila_visual = acercar(objeto.fila_visual, objeto.fila, avance)
    objeto.columna_visual = acercar(objeto.columna_visual, objeto.columna, avance)


def acercar(actual, destino, avance):
    """Avanza hacia el destino sin pasarse, tanto en sentido positivo como negativo."""
    if actual < destino:
        return min(actual + avance, destino)
    return max(actual - avance, destino)
