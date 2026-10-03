# Relación entre consignas y decisiones

Se contrastaron los archivos finales con dos materiales entregados por el equipo: **Ejercicio_ Lista Enlazada con Archivos Planos.docx** y **01.01 Asignar Gestión Administrativa al Juego.docx**. Son fuentes de requisitos y ejemplos, no instrucciones para modificar automáticamente el juego terminado.

La lectura incluyó el texto, las once tablas nativas del documento administrativo y las dos imágenes del ejercicio de punteros. No se pudo generar una vista paginada de Word porque el conversor LibreOffice del entorno no estaba disponible; por eso se citan títulos y tablas, no páginas supuestas. Los enlaces a videos del material no se revisaron y no se usan para afirmar características de esta implementación.

## Qué aporta cada documento

El ejercicio explica el método de puntero primero con clientes y facturas y luego lo adapta expresamente a usuarios y colisiones. El maestro guarda posición inicial y final; cada novedad guarda anterior y siguiente. Proporciona pseudocódigo y ejemplos con `struct` y `seek`.

El documento administrativo plantea un juego de palas y pelotas, al menos cinco objetos, usuarios, un acumulador, detalle de partidas y colisiones, cuatro consultas y matrices 2D y 3D. Sus tablas justifican los campos y las relaciones de los informes del proyecto. Pac-Man es una adaptación de ese dominio.

## Matriz de correspondencia

| Pedido o ejemplo del material | Implementación local | Evaluación para la defensa |
| --- | --- | --- |
| Un registro por usuario con código, nombre, usuario y clave | `registrar_usuario`, maestro fijo, username único sin distinguir mayúsculas | Correspondencia; el maestro añade extremos de cadena |
| Al menos cinco objetos que colisionan | Pac-Man, cuatro fantasmas, pellets, power y paredes | Hay al menos cinco personajes y ocho IDs por tipo/color; no se simulan contactos entre todas las parejas |
| Acumulador de un solo registro, con ID y acumulación | Una línea por inicio con código, username y contador global | Diferencia explícita; no afirmar que reproduce el archivo de un solo registro |
| Un resultado por usuario y partida, A, B y fecha | `guardar_partida` crea o actualiza conservando ID; añade resultado | Correspondencia estructural con adaptación de puntajes |
| A y B por palas, con restas ante fallos | A por pellets, B por enemigos; no se restan puntos | Adaptación de reglas, pendiente de confirmar como aceptada |
| Generar archivos mientras se juega | Reserva inicio antes; eventos en RAM y guardado al terminar | Persistencia diferida; no registro continuo de cada contacto en disco |
| Detalle de colisiones con fecha, X/Y y observación | Añade evento, origen, destino y enlaces | Correspondencia ampliada; objetos explícitos alimentan matrices |
| Padrón y cantidad de jugadores | `mostrar_padron` | Incluye las columnas solicitadas y las claves |
| Puntajes generales, A, B, total y mejor usuario | `mostrar_puntajes` | Suma resultados por usuario; excluye sin partidas al elegir mejor |
| Movimientos por usuario y partida | `consultar_detalle` | Sigue la cadena del usuario y filtra la partida |
| Ranking individual, totales, mejor y peor | `mostrar_ranking` | Añade opción general y desempates definidos |
| Matriz 2D de palas y pelotas, con “Total Pta.” | `matriz_contactos`, 8 × 8 | Cuenta contactos; no puntajes ni mejor pala. Es una reinterpretación de la medida |
| Día y mes del año, totales y mejor/peor día | `matriz_calendario`, 31 × 12 | Suma eventos por número de día; distingue fechas imposibles |
| 3D por partida, mes y objeto | `matriz_intervenciones` | Cuenta ambos participantes, adapta a ocho IDs y muestra doce tablas |
| Maestro con extremos y novedad con enlaces | `guardar_colision` y `historial_usuario` | Implementa la estructura doblemente enlazada del ejercicio |
| Acceso por `seek` con registros fijos | `archivos_fijos.py` | Conserva el método, con otra codificación y encabezados |

“Correspondencia” describe lo observado, no certifica una calificación ni la aceptación de las adaptaciones. El significado de “objetos que colisionan entre sí” y de “Total Pta.” merece confirmación si el docente exige interpretación literal.

## Cómo se traduce el método de puntero

| Paso del ejercicio | Código final |
| --- | --- |
| A: contar novedades | `contar_registros(...) + 1` calcula la posición nueva |
| B: buscar usuario y extremos | `obtener_usuario(codigo)` y `usuario['final']` |
| C: ingresar colisiones | El juego produce `crear_evento`, no un input manual de factura |
| D: nuevo registro con anterior=final y siguiente=0 | Diccionario del registro y `escribir_registro` |
| E: primera novedad | Asigna inicial a la posición nueva |
| E: usuario con novedades | Verifica el último registro y cambia su siguiente |
| E: actualizar maestro | Asigna final y reescribe el usuario |

La versión final verifica la última colisión antes de agregar una nueva, mientras el texto didáctico presenta parte de esa comprobación después de grabar. Es una diferencia defendible: evita agregar a partir de un extremo ya conocido como inconsistente. No transforma el conjunto de escrituras en transacción.

## Diferencias de representación respecto del ejemplo Python

El ejemplo utiliza `struct` para empaquetar números y cadenas en registros binarios y no tiene encabezado. El proyecto utiliza texto UTF-8 de longitud fija, separadores y LF, pero abre en modo binario. Por eso su fórmula incluye el encabezado:

```text
Ejemplo sin título: (n - 1) × T
Proyecto con título: H + (n - 1) × T
```

No copiar el tamaño comentado del ejemplo a este proyecto. El formato `i30sii` del ejemplo usa el modo nativo implícito de `struct`; puede introducir relleno por alineación, por lo que sumar 4+30+4+4 no sustituye a `struct.calcsize`. Aquí los tamaños se calculan explícitamente con los anchos y separadores de `config.py`.

La primera imagen del ejercicio muestra enlaces intercalados. En su última fila, el enlace anterior visible parece apuntar al propio registro 7; siguiendo la cadena 1→5→7 debería apuntar a 5. La segunda imagen tiene texto deformado. Para estudiar la lógica conviene usar el procedimiento textual y reconstruir ejemplos coherentes, sin memorizar errores de las imágenes.

Tampoco es necesario repetir afirmaciones generales del material sobre todos los sistemas COBOL o Arduino. Lo comprobado aquí es una técnica de archivos y enlaces. Un lenguaje no obliga por sí mismo a utilizar o evitar un gestor de bases de datos.

## Problemas y soluciones que el código permite defender

| Problema | Resolución implementada | Compromiso |
| --- | --- | --- |
| Hallar un registro sin escanear lo anterior | Longitud fija y offset | Anchos limitados y migración al cambiar formato |
| Distinguir bytes de caracteres | Codificar UTF-8 antes de medir | Menos caracteres si ocupan varios bytes |
| Saltos de línea distintos en Windows | Modo binario y LF explícito | Datos no deben editarse como texto libre |
| Encontrar eventos de un usuario | Extremos en maestro y enlaces por registro | Coherencia depende de varias escrituras |
| No repetir un número tras una interrupción | Reservar inicio antes de jugar | Puede haber inicios sin resultados |
| Separar entrada y movimiento continuo | Dirección solicitada y movimiento efectivo | Debe explicarse el giro pendiente |
| Evitar movimiento visual a saltos | Posición visual decimal | Dibujo y lógica no coinciden exactamente durante transición |
| Diferenciar contactos por objeto | IDs origen/destino | Agrupa pellets y paredes por tipo |
| Mostrar matriz 3D en terminal | Una tabla por mes y resúmenes | Presentación distinta del esquema ancho original |
| Conservar identidad al ordenar ranking | Ordenar solo en RAM | Carga datos para la consulta |

Estas explicaciones se basan en el comportamiento final. Para convertirlas en historia del desarrollo faltan los prototipos o recuerdos colectivos concretos.

## Qué queda por confirmar con el docente o el grupo

- Si se aprobó el acumulador como historial de inicios en lugar de un solo registro.
- Si la adaptación de A/B, sin restas, y de la matriz de puntajes a contactos corresponde al alcance acordado.
- Si bastaba persistir al terminar normalmente o se exigía escritura durante el juego.
- Cómo se interpretó el mínimo de objetos y las parejas de colisión.
- Si las filas hasta 31 del ejemplo 3D eran ilustrativas; el programa soporta números de partida mayores dentro de sus anchos.

No se cambia el juego para resolver estas dudas: se documentan para poder explicarlo con precisión.
