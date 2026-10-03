# Pac-Man con gestión administrativa

Proyecto académico desarrollado entre cuatro compañeros como trabajo de facultad. Integra un juego inspirado en Pac-Man, realizado con Python y Pygame, con un sistema de gestión de usuarios, partidas, colisiones e informes.

## Contexto y propósito

La propuesta del trabajo fue desarrollar un videojuego con Pygame e incorporar una gestión administrativa que permitiera registrar y consultar lo ocurrido en las partidas. El proyecto reúne programación orientada a objetos, manejo de archivos, acceso directo mediante punteros lógicos, vectores y matrices en una aplicación completa.

El desarrollo pasó por distintos prototipos hasta llegar a esta versión final. Las tareas se distribuyeron entre los cuatro integrantes y el resultado se presenta como un trabajo de autoría colectiva, con igual reconocimiento para todos.

El uso de herramientas de inteligencia artificial estuvo permitido como apoyo al desarrollo. La definición de los problemas, la elección de soluciones y la comprensión de los métodos utilizados formaron parte del trabajo del equipo.

## Enfoque del proyecto

La gestión administrativa parte de una propuesta de palas y pelotas, adaptada a la dinámica de Pac-Man. Los usuarios, las partidas y los contactos entre objetos se relacionan para producir un historial consultable, totales de puntajes, rankings y matrices de actividad.

La implementación combina clases para representar los personajes con módulos de funciones para los archivos y las consultas. Pygame proporciona la ventana, los eventos y el dibujo; el código del proyecto define el movimiento, las reglas y la organización de los datos.

Las principales decisiones técnicas son:

- **Registros de longitud fija:** permiten calcular la posición de un registro a partir de su número y acceder con `seek()`. Los anchos se definen en bytes para conservar posiciones consistentes.
- **Listas enlazadas en archivos:** el maestro de usuarios conserva los extremos de cada historial y las colisiones incluyen enlaces al registro anterior y siguiente. Estos punteros representan números de registro.
- **Estado en memoria y persistencia en disco:** posiciones, alimentos y eventos se mantienen en RAM durante la partida; los archivos conservan los inicios y los resultados entre ejecuciones. Los eventos se escriben al finalizar normalmente.
- **Matrices para las consultas:** los contactos se agrupan por objetos, fechas y partidas. La presentación se organiza en tablas que permiten consultar los totales sin modificar el orden físico de los registros.

## Funcionalidades

- Movimiento por un laberinto con pellets, poderes y cuatro enemigos.
- Registro de usuarios e inicio de sesión.
- Puntajes separados por alimentos y enemigos.
- Persistencia en archivos de registros de longitud fija.
- Historial de colisiones mediante listas enlazadas por usuario.
- Informes de partidas, movimientos, puntajes y ranking.
- Matrices de contactos, calendario e intervenciones por partida, mes y objeto.

## Instalación

Requiere Python 3 y un entorno gráfico. La dependencia externa es `pygame-ce==2.5.8`, importada como `pygame`.

Desde la carpeta del proyecto, en PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

Al iniciar se crean los archivos de datos faltantes. Desde el menú se puede registrar un usuario, iniciar sesión, jugar y acceder a las consultas administrativas.

## Controles y reglas

| Acción | Control o comportamiento |
| --- | --- |
| Movimiento | W, A, S, D |
| Giro bloqueado | Se intenta nuevamente al llegar a un camino válido |
| Pellet | Suma 10 al puntaje A |
| Power | Activa poder durante 7 segundos |
| Enemigo comido con poder | Suma 200 al puntaje B |
| Victoria | Consumir todos los pellets y powers |
| Derrota | Contacto con un enemigo sin poder o cierre de la ventana |

Los enemigos eligen caminos vecinos al azar. La ventana mide 1280 × 900 y el dibujo se limita a 60 FPS.

## Organización del código

| Módulo | Responsabilidad |
| --- | --- |
| `main.py` | Menú, sesión y coordinación de la partida |
| `config.py` | Constantes y definición de campos |
| `archivos_fijos.py` | Codificación, validación y acceso mediante seek |
| `usuarios.py` | Registro y autenticación |
| `partidas.py` | Numeración y resultados |
| `colisiones.py` | Eventos y enlaces del historial |
| `laberinto.py` | Tablero y caminos |
| `objetos.py` | Clases Jugador y Enemigo |
| `juego.py` | Entrada, movimiento, contactos y dibujo |
| `informes.py` | Consultas, tablas y matrices |

## Persistencia

Los archivos usan campos de longitud fija en bytes UTF-8, un separador por campo y un salto LF. Cada encabezado ocupa el mismo tamaño que un registro.

| Archivo | Bytes por registro |
| --- | ---: |
| `maestro_usuarios.txt` | 68 |
| `acumulador_partidas.txt` | 22 |
| `partida_jugador.txt` | 60 |
| `colisiones.txt` | 133 |

El acceso directo utiliza `seek()`. El maestro conserva el inicio y final de la cadena de cada usuario; las colisiones guardan los números de registro anterior y siguiente. Los informes ordenan los datos en memoria sin cambiar las posiciones físicas.

Los datos de ejecución y los informes generados no se incluyen en el repositorio. Cada instalación comienza con sus propios usuarios e historial.

## Informes

Las consultas se muestran en terminal y pueden guardarse como texto al responder `s`. Incluyen padrón de usuarios, detalle de partidas, movimientos, puntajes generales y ranking.

Las matrices permiten consultar contactos entre objetos, eventos por día y mes y participaciones por partida, mes y objeto. Cada contacto genera dos participaciones, una por objeto.

## Verificación

```powershell
python -B tools/verificar_modelo.py
```

Las pruebas usan datos ficticios en una carpeta temporal y comprueban tamaños y offsets, enlaces, numeración, matrices y movimiento lógico y visual. No modifican los datos de ejecución.

## Limitaciones

El programa está previsto para una instancia a la vez. Reserva el inicio de una partida antes de jugar y guarda sus eventos y resultado al finalizar normalmente. No implementa transacciones ni recuperación de partidas interrumpidas.

Las claves se almacenan en texto plano y aparecen en el padrón. La autenticación corresponde al alcance de un proyecto educativo local, no a un servicio de producción.
