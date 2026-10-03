# Pac-Man y gestión administrativa

Proyecto educativo realizado por **cuatro compañeros con autoría colectiva y participación de igual valor**, con asistencia de IA permitida. Este repositorio conserva la versión final y documenta el flujo, las decisiones, la POO, las estructuras de datos y la persistencia para estudiar y defender el código. No se publican identidades ni se atribuyen módulos a personas.

El juego utiliza Python y Pygame. La administración funciona en terminal: usuarios, partidas, historial de contactos, puntajes, ranking y matrices. Los datos se conservan en archivos de registros de longitud fija, mediante `seek()` y cadenas por usuario.

## Documentación para estudiar

1. [Guía de defensa oral](docs/GUIA_DEFENSA.md): arquitectura, recorrido de una partida, POO, memoria, movimiento y preguntas.
2. [Datos, bytes y seek](docs/DATOS_Y_SEEK.md): campos, fórmulas, enlaces y ejemplos resueltos.
3. [Relación con las consignas](docs/CONSIGNAS_Y_DECISIONES.md): requisitos, implementación, adaptaciones y aspectos por confirmar.
4. [Historia colectiva](docs/HISTORIA_Y_EQUIPO.md): contexto confirmado y reconstrucción de decisiones sin inventar una cronología.
5. [Repositorio privado](docs/REPOSITORIO.md): comandos que ejecutará el usuario.
6. [Verificación](docs/VERIFICACION.md): alcance y resultados de las comprobaciones.

## Instalación y ejecución

Se requiere Python 3 y un entorno gráfico. `requirements.txt` fija `pygame-ce==2.5.8`, importado como `pygame`. Las otras dependencias son módulos de la biblioteca estándar. No aparecen otros frameworks ni un gestor de base de datos en esta versión.

Desde la carpeta del proyecto, en PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

En un clon limpio, el programa crea `datos/` y sus cuatro archivos con encabezados. Registrar un usuario desde el menú y luego iniciar sesión o elegir Jugar. Registrar no inicia automáticamente la sesión. Los datos de uso, los informes y los respaldos se excluyen de Git.

## Cómo se juega

- Ventana de 1280 × 900, con dibujo limitado a 60 FPS.
- W, A, S, D solicitan una dirección. Una pulsación mantiene el movimiento; un giro bloqueado queda pendiente hasta que haya camino.
- Cada pellet suma 10 a A. El power activa siete segundos de poder; comer un enemigo suma 200 a B.
- Se gana al consumir todos los pellets y powers. Chocar sin poder o cerrar la ventana termina en derrota. Cerrar no inventa un evento de choque.
- Los enemigos eligen vecinos transitables al azar; no implementan persecución ni IA generativa.

## Estructura

| Módulo | Responsabilidad |
| --- | --- |
| `main.py` | Menú, sesión y coordinación del guardado |
| `config.py` | Constantes y contratos de campos |
| `archivos_fijos.py` | Codificación, validación y posiciones en bytes |
| `usuarios.py` | Altas, autenticación y maestro |
| `partidas.py` | Inicios y resultados |
| `colisiones.py` | Eventos y cadenas enlazadas por usuario |
| `laberinto.py` | Tablero y caminos transitables |
| `objetos.py` | Clases Jugador y Enemigo y movimiento visual |
| `juego.py` | Entrada, simulación, contactos y dibujo |
| `informes.py` | Consultas, tablas, ranking y matrices |

## Datos y consultas

| Archivo | Bytes por registro, incluido LF |
| --- | ---: |
| `maestro_usuarios.txt` | 68 |
| `acumulador_partidas.txt` | 22 |
| `partida_jugador.txt` | 60 |
| `colisiones.txt` | 133 |

Cada archivo comienza con un encabezado del mismo tamaño que un registro. Los anchos se miden en bytes UTF-8. Se abre en binario para conservar offsets y LF de un byte. No reordenar ni editar manualmente los datos: los códigos y enlaces dependen de las posiciones físicas.

Los informes se muestran siempre en terminal y solo se guardan en `informes/` si se responde `s`. El menú administrativo incluye padrón, partidas, movimientos, puntajes y ranking. Las matrices cuentan contactos entre objetos, eventos por día y mes, y participaciones por partida, mes y objeto. Un contacto equivale a dos participaciones; no son puntos.

## Alcance y límites

Los punteros son **números de registro**, no direcciones de RAM. El proyecto utiliza clases e instancias, pero no una jerarquía propia de herencia. Python administra la memoria de sus objetos.

Los inicios se escriben antes de jugar. Los eventos se acumulan en RAM y se guardan después del retorno normal del juego; el resultado se guarda al final. No hay recuperación de partidas interrumpidas ni transacciones para operaciones de varias escrituras. Se contempla una instancia del programa a la vez.

El padrón conserva y muestra claves en texto plano, como el modelo administrativo aportado. No es autenticación para producción; los datos actuales se mantienen fuera del repositorio, incluso privado.

La versión adapta una consigna de palas y pelotas a Pac-Man. Ver las diferencias en [consignas y decisiones](docs/CONSIGNAS_Y_DECISIONES.md); esta documentación no certifica aprobación docente.

## Comprobación aislada

```powershell
python -B tools/verificar_modelo.py
```

Utiliza datos ficticios en una carpeta temporal; no modifica `datos/` ni sustituye una prueba manual de jugabilidad.

## Autoría y evolución

El equipo indicó que hubo prototipos previos. La copia revisada no los incluía ni tenía historial Git. El futuro primer commit representa esta versión final; no reconstruye fechas ni contribuciones individuales. El repositorio será privado y sus comandos los ejecutará el usuario. La licencia queda para acuerdo colectivo.
