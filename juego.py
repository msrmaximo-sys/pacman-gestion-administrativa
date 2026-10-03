"""Pygame dibuja y reúne eventos; main.py se encarga de persistir la partida."""

import pygame
import config
from objetos import Jugador, Enemigo, actualizar_dibujo
from laberinto import MAPA, INICIO_JUGADOR, INICIOS_ENEMIGOS, crear_pellets
from colisiones import crear_evento


def centro(fila, columna):
    """Convierte una celda en coordenadas de dibujo."""
    x = config.ORIGEN_X + columna * config.CELDA + config.CELDA // 2
    y = config.ORIGEN_Y + fila * config.CELDA + config.CELDA // 2
    return x, y


def dibujar_pacman(ventana, jugador):
    """Dibuja grande y reduce para suavizar los bordes del personaje."""
    sprite = pygame.Surface((96, 96), pygame.SRCALPHA)
    pygame.draw.circle(sprite, (255, 180, 15), (48, 50), 40)
    pygame.draw.circle(sprite, config.AMARILLO, (48, 46), 38)
    # Alterna dos aperturas de boca; el triángulo transparente recorta el círculo.
    apertura = 12
    if pygame.time.get_ticks() // 120 % 2 == 0:
        apertura = 30
    pygame.draw.polygon(sprite, (0, 0, 0, 0),
                        [(48, 48), (96, 48 - apertura), (96, 48 + apertura)])
    pygame.draw.circle(sprite, (40, 30, 15), (54, 25), 5)
    angulos = {(0, 1): 0, (-1, 0): 90, (0, -1): 180, (1, 0): 270}
    sprite = pygame.transform.rotate(sprite, angulos[jugador.direccion])
    # Reduce el dibujo grande para que el borde se vea suave.
    sprite = pygame.transform.smoothscale(sprite, (config.CELDA, config.CELDA))
    ventana.blit(sprite, sprite.get_rect(center=centro(jugador.fila_visual, jugador.columna_visual)))


def dibujar_fantasma(ventana, enemigo, power):
    """Forma de fantasma con falda, ojos y expresión de miedo durante el poder."""
    sprite = pygame.Surface((96, 96), pygame.SRCALPHA)
    color = enemigo.color
    if power:
        color = config.COLOR_POWER
    pygame.draw.circle(sprite, color, (48, 42), 36)
    pygame.draw.rect(sprite, color, (12, 40, 72, 34))
    for x in (12, 36, 60):
        pygame.draw.polygon(sprite, color, [(x, 70), (x + 12, 86), (x + 24, 70)])
    for x in (34, 62):
        pygame.draw.ellipse(sprite, config.BLANCO, (x - 12, 29, 23, 30))
        pygame.draw.ellipse(sprite, (20, 35, 85), (x - 4, 38, 11, 16))
    if power:
        pygame.draw.lines(sprite, config.BLANCO, False,
                          [(24, 69), (32, 63), (40, 69), (48, 63), (56, 69), (64, 63), (72, 69)], 4)
    # Reduce el dibujo grande para que el borde se vea suave.
    sprite = pygame.transform.smoothscale(sprite, (config.CELDA, config.CELDA))
    ventana.blit(sprite, sprite.get_rect(center=centro(enemigo.fila_visual, enemigo.columna_visual)))


def dibujar(ventana, fuente, jugador, enemigos, pellets, powers, estado, power):
    """Dibuja el tablero con contornos luminosos y contadores separados."""
    ventana.fill(config.NEGRO)
    titulo = fuente.render("PAC-MAN", True, config.AMARILLO)
    ventana.blit(titulo, (config.ORIGEN_X, 38))
    texto = f"PELLETS  {estado['a']:06d}       ENEMIGOS  {estado['b']:06d}"
    ventana.blit(fuente.render(texto, True, config.BLANCO), (510, 38))
    marco = (config.ORIGEN_X - 10, config.ORIGEN_Y - 10,
             len(MAPA[0]) * config.CELDA + 20, len(MAPA) * config.CELDA + 20)
    pygame.draw.rect(ventana, (30, 44, 80), marco, 2, border_radius=18)
    for fila in range(len(MAPA)):
        for columna in range(len(MAPA[fila])):
            if MAPA[fila][columna] == "#":
                x = config.ORIGEN_X + columna * config.CELDA
                y = config.ORIGEN_Y + fila * config.CELDA
                pared = (x + 3, y + 3, config.CELDA - 6, config.CELDA - 6)
                pygame.draw.rect(ventana, (18, 29, 63), pared, border_radius=10)
                pygame.draw.rect(ventana, (60, 105, 240), pared, 2, border_radius=10)
    for fila, columna in pellets:
        pygame.draw.circle(ventana, (90, 67, 38), centro(fila, columna), 6)
        pygame.draw.circle(ventana, (255, 224, 165), centro(fila, columna), 3)
    for fila, columna in powers:
        radio = 10 + pygame.time.get_ticks() // 200 % 2
        pygame.draw.circle(ventana, (100, 75, 25), centro(fila, columna), radio + 5)
        pygame.draw.circle(ventana, config.AMARILLO, centro(fila, columna), radio)
    dibujar_pacman(ventana, jugador)
    for enemigo in enemigos:
        dibujar_fantasma(ventana, enemigo, power)
    texto = "W A S D   /   MOVER"
    if power:
        segundos = max(0, (estado["power_hasta"] - pygame.time.get_ticks()) / 1000)
        texto = f"POWER ACTIVO   {segundos:.1f} s   /   COME FANTASMAS"
    ventana.blit(fuente.render(texto, True, config.BLANCO), (config.ORIGEN_X, 855))
    pygame.display.flip()


def comer_pellets(jugador, pellets, powers, estado, ahora):
    """Suma A o activa el poder y registra su colisión."""
    posicion = (jugador.fila, jugador.columna)
    if posicion in pellets:
        pellets.remove(posicion)
        estado["a"] += config.PUNTOS_PELLET
        estado["eventos"].append(crear_evento(*posicion, "PELLET", "Come pellet normal: +10 puntos A"))
    if posicion in powers:
        powers.remove(posicion)
        estado["power_hasta"] = ahora + config.POWER_MS
        estado["eventos"].append(crear_evento(*posicion, "POWER", "Come power pellet"))


def comprobar_enemigos(jugador, enemigos, estado, ahora):
    """Resuelve contactos después de cada movimiento para detectar cruces."""
    for enemigo in enemigos:
        if jugador.fila == enemigo.fila and jugador.columna == enemigo.columna:
            if ahora < estado["power_hasta"]:
                estado["b"] += config.PUNTOS_ENEMIGO
                evento = crear_evento(jugador.fila, jugador.columna, "ENEMIGO_COMIDO", "Come enemigo con power activo", enemigo.codigo_objeto)
                estado["eventos"].append(evento)
                enemigo.reaparecer(jugador)
            else:
                evento = crear_evento(jugador.fila, jugador.columna, "CHOQUE", "Choque sin power: derrota", enemigo.codigo_objeto)
                estado["eventos"].append(evento)
                return True
    return False


def ejecutar_juego():
    """Ejecuta una partida y devuelve los datos que guardará la consola."""
    pygame.init()
    try:
        ventana = pygame.display.set_mode((config.ANCHO_VENTANA, config.ALTO_VENTANA))
        pygame.display.set_caption("Pac-Man")
        fuente = pygame.font.Font(None, 32)
        reloj = pygame.time.Clock()
        jugador = Jugador(*INICIO_JUGADOR)
        enemigos = []
        for indice, posicion in enumerate(INICIOS_ENEMIGOS):
            enemigos.append(Enemigo(*posicion, config.COLORES_ENEMIGOS[indice], config.OBJ_ROJO + indice))
        pellets, powers = crear_pellets()
        # A: pellets; B: enemigos; power_hasta: instante de vencimiento en ms.
        estado = {"a": 0, "b": 0, "power_hasta": 0, "eventos": []}
        teclas = {pygame.K_w: (-1, 0), pygame.K_s: (1, 0),
                  pygame.K_a: (0, -1), pygame.K_d: (0, 1)}
        ultimo_jugador = pygame.time.get_ticks()
        ultimo_enemigo = ultimo_jugador
        resultado = "derrota"
        jugando = True
        direccion = (0, 0)  # Última tecla pedida; se conserva entre cuadros.
        while jugando:
            # Limita el dibujo a 60 FPS; la velocidad por celda usa otros intervalos.
            milisegundos = reloj.tick(config.FPS)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    jugando = False
                elif evento.type == pygame.KEYDOWN and evento.key in teclas:
                    direccion = teclas[evento.key]
            if not jugando:
                break
            ahora = pygame.time.get_ticks()
            # 1. Mover jugador, consumir alimento y resolver contactos.
            if ahora - ultimo_jugador >= config.PASO_JUGADOR_MS:
                contacto = jugador.mover(direccion)
                if contacto == "PARED":
                    estado["eventos"].append(crear_evento(jugador.fila, jugador.columna, "PARED", "Se detiene frente a una pared"))
                ultimo_jugador = ahora
                comer_pellets(jugador, pellets, powers, estado, ahora)
                if comprobar_enemigos(jugador, enemigos, estado, ahora):
                    break
            # 2. Mover cada enemigo y comprobar su contacto antes de seguir.
            if ahora - ultimo_enemigo >= config.PASO_ENEMIGO_MS:
                ultimo_enemigo = ahora
                for enemigo in enemigos:
                    enemigo.mover()
                    if comprobar_enemigos(jugador, [enemigo], estado, ahora):
                        jugando = False
                        break
            if jugando and not pellets and not powers:
                resultado = "victoria"
                jugando = False
            # 3. Acercar los dibujos a sus celdas y presentar el cuadro.
            actualizar_dibujo(jugador, milisegundos, config.PASO_JUGADOR_MS)
            for enemigo in enemigos:
                actualizar_dibujo(enemigo, milisegundos, config.PASO_ENEMIGO_MS)
            dibujar(ventana, fuente, jugador, enemigos, pellets, powers, estado, ahora < estado["power_hasta"])
        return estado["a"], estado["b"], resultado, estado["eventos"]
    finally:
        # Cierra Pygame incluso si ocurre un error dentro del juego.
        pygame.quit()
