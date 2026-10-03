# Verificación de la documentación y del modelo

Revisión realizada el 3 de octubre de 2026. Se conservaron la lógica del juego y los datos existentes. Se prepararon Markdown, reglas de exclusión para Git y un script didáctico de comprobación. No se inicializó ni publicó el repositorio.

## Comprobaciones ejecutadas

| Comprobación | Resultado |
| --- | --- |
| Lectura de los diez módulos Python | Flujo, contratos y funciones contrastados |
| Análisis sintáctico de los diez módulos con `ast.parse` | Correcto |
| Encabezados, tamaños y decodificación de archivos actuales, en modo de lectura | Correctos |
| Usuarios existentes | 2, sin reproducir identidades ni claves |
| Acumulador | 1 inicio |
| Detalle de partidas | 1 resultado legible |
| Colisiones | 57 registros y 57 eventos alcanzados por las cadenas de los dos usuarios |
| Recorrido de cadenas y validación de objetos | Sin error en los datos revisados |
| SHA-256 antes y después de la revisión de datos | Idénticos; la lectura no los modificó |
| Cinco pruebas aisladas del modelo | Las cinco finalizaron correctamente |

Entorno de estas comprobaciones: Python 3.14.3 en Windows. No se afirma una versión mínima soportada a partir de esta única ejecución. La dependencia gráfica está declarada en `requirements.txt`; estas cinco pruebas no requieren abrir Pygame.

## Pruebas reproducibles

Desde la raíz del proyecto:

```powershell
python -B tools/verificar_modelo.py
```

El script crea una carpeta temporal, redirige `config.DATOS` solo dentro de ese proceso y restaura su valor al terminar cada prueba. Trabaja con nombres y claves ficticios. Comprueba:

1. Tamaños 68/22/60/133, offset 204 del tercer usuario, lectura directa, UTF-8 y rechazo de un nombre que excede el ancho en bytes.
2. Eventos intercalados de dos usuarios, enlaces 1→3 para el primero, extremos del maestro y detección de un ciclo introducido en la copia ficticia.
3. Inicios sin resultado, numeración individual no reutilizada y actualización de un resultado sin duplicar su ID.
4. Contactos y participaciones, filtro de año, 29 de febrero, huecos de partidas y filas independientes de matriz.
5. Movimiento por celda, giro bloqueado, avance visual intermedio y límite que evita sobrepasar el destino.

Estas comprobaciones apoyan los ejemplos de estudio. No prueban toda entrada posible, concurrencia, recuperación ante cortes ni cumplimiento literal de toda la consigna.

## Fuentes revisadas

Se extrajo el texto de ambos DOCX suministrados, se inspeccionaron las once tablas del documento administrativo y las dos imágenes incrustadas del ejercicio de punteros. No se copiaron los originales a la documentación versionable.

La conversión a páginas falló por ausencia de `soffice.exe` en el entorno de documentos; no se instaló otro conversor. Por eso la comparación usa estructura de texto, tablas e imágenes originales, sin afirmar una comprobación de paginación.

El ejemplo de `struct` del material comenta 42 bytes para `i30sii`; `struct.calcsize('i30sii')` devolvió 44 en el intérprete de esta revisión. Es una advertencia sobre alineación del ejemplo, no un cambio en los tamaños del juego, que no utiliza ese formato.

## Alcance que queda fuera de esta revisión

No se hizo una partida manual completa ni una revisión visual de la ventana. No se certifica que las adaptaciones de acumulador, puntajes y matrices hayan sido aprobadas por el profesor. No se reconstruyeron prototipos ausentes ni una cronología histórica no documentada.

Para la defensa práctica conviene demostrar registro e inicio de sesión, giro pendiente, pellet y power, encuentro con fantasma, cierre normal y consulta de sus informes. Si se quiere conservar intacto el historial del grupo, hacerlo en una copia de trabajo con datos ficticios.

## Datos locales de demostración

El 3 de octubre de 2026 se sustituyeron las identidades guardadas por valores ficticios, también en los usernames del acumulador y de las colisiones:

| Nombre | Usuario | Clave de demostración |
| --- | --- | --- |
| Jugador 001 | jugador001 | demo001 |
| Jugador 002 | jugador002 | demo002 |

Se conservaron IDs, enlaces, fechas, puntajes e historial. Se verificaron los dos accesos y las cadenas después del cambio. Estas claves son públicas de demostración, sin uso fuera de este juego. Los datos siguen excluidos de Git; en un clon nuevo se registran usuarios desde el menú. No se modificaron los documentos originales de la consigna.
