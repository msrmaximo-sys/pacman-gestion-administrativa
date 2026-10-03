"""Consultas de solo lectura: una tabla común y un único guardado con aprobación."""

from datetime import datetime
from calendar import monthrange
import config
from pathlib import Path
from operator import itemgetter

from usuarios import listar_usuarios, obtener_usuario
from partidas import listar_partidas
from colisiones import historial_usuario

CARPETA_INFORMES = Path(__file__).resolve().parent / "informes"


def tabla(titulo, encabezados, filas):
    """Arma celdas con el ancho del texto más largo de cada columna."""
    # Primero mide caracteres visibles; las tildes no desplazan las celdas.
    anchos = []
    for columna, encabezado in enumerate(encabezados):
        ancho = len(encabezado)
        for fila in filas:
            ancho = max(ancho, len(str(fila[columna])))
        anchos.append(ancho)
    borde = "+"
    for ancho in anchos:
        borde += "-" * (ancho + 2) + "+"
    lineas = [titulo, borde]
    # Se reutiliza el mismo dibujo para encabezados, datos y totales.
    for fila in [encabezados] + filas:
        linea = "|"
        for valor, ancho in zip(fila, anchos):
            texto = str(valor)
            if isinstance(valor, int):
                texto = texto.rjust(ancho)
            else:
                texto = texto.ljust(ancho)
            linea += " " + texto + " |"
        lineas.extend([linea, borde])
    if not filas:
        lineas.append("Sin registros.")
    return "\n".join(lineas)


def publicar_informe(nombre, contenido):
    """Muestra siempre el informe y lo guarda solamente si se responde s."""
    fecha = datetime.now()
    texto = contenido + "\n\nGenerado: " + fecha.strftime("%Y-%m-%d %H:%M:%S") + "\n"
    print("\n\n" + texto)
    while True:
        respuesta = input("¿Querés guardar el informe en disco? (s/n): ").strip().lower()
        if respuesta == "n":
            print("Informe no guardado.\n")
            return None
        if respuesta == "s":
            break
        print("Respuesta inválida. Escribí s o n.")
    # Recién después de responder s se crea la carpeta y se escribe el archivo.
    CARPETA_INFORMES.mkdir(exist_ok=True)
    ruta = CARPETA_INFORMES / (nombre + "_" + fecha.strftime("%Y%m%d_%H%M%S_%f") + ".txt")
    ruta.write_text(texto, encoding="utf-8")
    print(f"Informe guardado en: {ruta}\n")
    return ruta


def elegir_usuario(opcional=False):
    """Pide un código; Enter permite la vista general cuando corresponde."""
    mensaje = "Código de usuario: "
    if opcional:
        mensaje = "Código de usuario (Enter = general): "
    texto = input("\n" + mensaje).strip()
    if opcional and texto == "":
        return None
    return obtener_usuario(int(texto))["codigo"]


def mostrar_padron():
    """Genera el padrón y su cantidad total, según la planilla solicitada."""
    usuarios = sorted(listar_usuarios(), key=itemgetter("codigo"))
    filas = []
    for usuario in usuarios:
        filas.append([f"{usuario['codigo']:03d}", usuario["nombre"], usuario["usuario"], usuario["clave"]])
    texto = tabla("PADRÓN DE USUARIOS DEL JUEGO", ["Cód. usuario", "Nombre y apellido", "Usuario", "Clave"], filas)
    texto += f"\n\nTotal jugadores: {len(usuarios)}"
    return publicar_informe("padron_usuarios", texto)


def tabla_partidas(partidas):
    """Ordena el detalle por usuario y número de partida."""
    filas = []
    for partida in sorted(partidas, key=itemgetter("codigo", "numero")):
        filas.append([partida["id"], f"{partida['codigo']:03d}", partida["numero"],
                      partida["puntaje_a"], partida["puntaje_b"], partida["fecha"], partida["resultado"]])
    return tabla("DETALLE POR PARTIDA Y JUGADOR",
                 ["ID", "Cód.", "Partida", "Puntaje A", "Puntaje B", "Fecha última partida", "Resultado"], filas)


def mostrar_partidas(partidas):
    """Guarda el listado general o el del usuario elegido."""
    texto = tabla_partidas(partidas)
    texto += f"\n\nTotal partidas: {len(partidas)}"
    return publicar_informe("partidas", texto)


def consultar_detalle():
    """Selecciona usuario y partida, y sigue su cadena de colisiones."""
    codigo = elegir_usuario()
    usuario = obtener_usuario(codigo)
    partidas = listar_partidas(codigo)
    if not partidas:
        return publicar_informe(f"movimientos_{codigo:03d}", f"Usuario {codigo:03d} - {usuario['nombre']}\nSin partidas.")
    print("\n" + tabla_partidas(partidas) + "\n")
    numero = int(input("Número de partida de la lista: "))
    elegida = None
    for partida in partidas:
        if partida["numero"] == numero:
            elegida = partida
    if elegida is None:
        raise ValueError("La partida no pertenece al usuario.")
    filas = []
    eventos = historial_usuario(codigo)
    eventos.sort(key=itemgetter("fecha", "id"))
    for evento in eventos:
        if evento["numero"] == numero:
            observacion = evento["evento"] + ": " + evento["observacion"]
            filas.append([evento["fecha"], evento["coordenada"], observacion])
    texto = f"Cód. usuario: {codigo:03d}    Nombre y apellido: {usuario['nombre']}\n"
    texto += f"Núm. partida: {numero}\n\n"
    texto += tabla("INFORME DE MOVIMIENTOS POR USUARIO Y PARTIDA", ["Fecha", "Coordenada X,Y", "Observación"], filas)
    texto += f"\n\nTotal general colisiones: {len(filas)}"
    texto += f"\nPuntaje A: {elegida['puntaje_a']}    Puntaje B: {elegida['puntaje_b']}"
    return publicar_informe(f"movimientos_{codigo:03d}_{numero:05d}", texto)


def resumen_usuarios():
    """Suma los dos puntajes de todas las partidas de cada usuario."""
    resumen = []
    partidas = listar_partidas()
    for usuario in sorted(listar_usuarios(), key=itemgetter("codigo")):
        total_a = 0
        total_b = 0
        cantidad = 0
        for partida in partidas:
            if partida["codigo"] == usuario["codigo"]:
                total_a += partida["puntaje_a"]
                total_b += partida["puntaje_b"]
                cantidad += 1
        resumen.append({"codigo": usuario["codigo"], "nombre": usuario["nombre"],
                        "a": total_a, "b": total_b, "total": total_a + total_b, "cantidad": cantidad})
    return resumen


def mostrar_puntajes():
    """Genera totales por jugador, total del sistema y el mejor usuario."""
    resumen = resumen_usuarios()
    filas = []
    total_a = 0
    total_b = 0
    mejor = None
    for usuario in resumen:
        filas.append([f"{usuario['codigo']:03d}", usuario["nombre"], usuario["a"], usuario["b"], usuario["total"]])
        total_a += usuario["a"]
        total_b += usuario["b"]
        if usuario["cantidad"] > 0:
            if mejor is None or usuario["total"] > mejor["total"]:
                mejor = usuario
    filas.append(["", "TOTAL GENERAL", total_a, total_b, total_a + total_b])
    titulo = "PLANILLA PUNTAJE DE JUGADORES"
    nombre = "puntajes_generales"
    texto = tabla(titulo, ["Cód. usuario", "Nombre y apellido", "Tot. Punt. A", "Tot. Punt. B", "T. Gral. puntos"], filas)
    if mejor is None:
        texto += "\n\nSin partidas: todavía no hay mejor usuario."
    else:
        texto += f"\n\nEl mejor usuario es: {mejor['codigo']:03d} - {mejor['nombre']}"
        texto += f"\nCon el puntaje: {mejor['total']}"
    texto += "\nEmpates: se prioriza el menor código de usuario."
    return publicar_informe(nombre, texto)


def puntaje_total(partida):
    """Devuelve A + B para comparar partidas."""
    return partida["puntaje_a"] + partida["puntaje_b"]


def fila_ranking(partida, etiqueta, general, usuarios):
    """Prepara las mismas columnas para una partida o para el resumen final."""
    fila = [etiqueta, partida["puntaje_a"], partida["puntaje_b"],
            puntaje_total(partida), partida["fecha"]]
    if general:
        usuario = usuarios[partida["codigo"]]
        fila = [f"{usuario['codigo']:03d}", usuario["nombre"]] + fila
    return fila


def mostrar_ranking():
    """Lista partidas y calcula totales, mejor y peor del conjunto elegido."""
    codigo = elegir_usuario(opcional=True)
    general = codigo is None
    # listar_partidas lee registros fijos mediante leer_registro y seek().
    partidas = sorted(listar_partidas(codigo), key=itemgetter("codigo", "numero"))
    # El segundo orden conserva el anterior en empates (ordenamiento estable).
    partidas.sort(key=puntaje_total, reverse=True)
    usuarios = {}
    for partida in partidas:
        cod_usuario = partida["codigo"]
        if cod_usuario not in usuarios:
            # Acceso directo al maestro: posición = código del usuario.
            usuarios[cod_usuario] = obtener_usuario(cod_usuario)
    encabezados = ["Núm. partida", "Tot. Puntaje A", "Tot. Puntaje B", "T. Gral. puntos", "Fecha última partida"]
    nombre = "ranking_general"
    titulo = "PLANILLA PUNTAJE DE JUGADORES - TODAS LAS PARTIDAS"
    if general:
        encabezados = ["Cód.", "Nombre y apellido"] + encabezados
    else:
        usuario = obtener_usuario(codigo)
        titulo = f"PLANILLA PUNTAJE DE JUGADORES - Usuario: {codigo:03d} - NyA: {usuario['nombre']}"
        nombre = f"ranking_{codigo:03d}"
    filas = []
    total_a = 0
    total_b = 0
    for partida in partidas:
        filas.append(fila_ranking(partida, partida["numero"], general, usuarios))
        total_a += partida["puntaje_a"]
        total_b += partida["puntaje_b"]
    totales = ["TOTAL GENERAL", total_a, total_b, total_a + total_b, ""]
    if general:
        totales = ["", ""] + totales
    filas.append(totales)
    # Estas dos filas son resúmenes: no vuelven a sumarse en los totales.
    if partidas:
        mejor = max(partidas, key=puntaje_total)
        peor = min(partidas, key=puntaje_total)
        filas.append(fila_ranking(mejor, f"MEJOR: {mejor['numero']}", general, usuarios))
        filas.append(fila_ranking(peor, f"PEOR: {peor['numero']}", general, usuarios))
    texto = tabla(titulo, encabezados, filas)
    if not partidas:
        texto += "\n\nSin partidas: no hay mejor ni peor partida."
    texto += "\nOrden: puntos A + B de mayor a menor."
    texto += "\nEmpates: menor código de usuario y luego menor número de partida."
    return publicar_informe(nombre, texto)



def crear_matriz(filas, columnas):
    """Crea filas independientes: cambiar una celda no cambia otra fila."""
    matriz = []
    for fila in range(filas):
        nueva_fila = []
        for columna in range(columnas):
            nueva_fila.append(0)
        matriz.append(nueva_fila)
    return matriz


def crear_matriz_3d(partidas):
    """Cada partida contiene doce meses y cada mes contiene ocho objetos."""
    matriz = []
    for partida in range(partidas):
        matriz.append(crear_matriz(12, config.CANTIDAD_OBJETOS))
    return matriz


def totales_matriz(matriz, columnas):
    """Calcula sumas por fila, por columna y general sin modificar la matriz."""
    totales_filas = []
    totales_columnas = [0] * columnas
    total_general = 0
    for fila in matriz:
        total_fila = 0
        for columna in range(columnas):
            total_fila += fila[columna]
            totales_columnas[columna] += fila[columna]
        totales_filas.append(total_fila)
        total_general += total_fila
    return totales_filas, totales_columnas, total_general


def matriz_contactos(eventos):
    """Dos índices: objeto de origen y objeto de destino. Un evento suma una vez."""
    matriz = crear_matriz(config.CANTIDAD_OBJETOS, config.CANTIDAD_OBJETOS)
    for evento in eventos:
        # Los IDs comienzan en 1; los índices de las listas comienzan en 0.
        origen = evento["origen"] - 1
        destino = evento["destino"] - 1
        matriz[origen][destino] += 1
    return matriz


def matriz_calendario(eventos, anio):
    """Dos índices: día y mes. Cuenta una colisión en su día y mes."""
    matriz = crear_matriz(31, 12)
    for evento in eventos:
        fecha = datetime.strptime(evento["fecha"], "%Y-%m-%d %H:%M:%S")
        if fecha.year == anio:
            matriz[fecha.day - 1][fecha.month - 1] += 1
    return matriz


def matriz_intervenciones(eventos, anio, cantidad_partidas):
    """Tres índices: partida, mes y objeto. Cuenta participaciones, no puntajes."""
    matriz = crear_matriz_3d(cantidad_partidas)
    for evento in eventos:
        fecha = datetime.strptime(evento["fecha"], "%Y-%m-%d %H:%M:%S")
        if fecha.year == anio:
            # Restamos uno para convertir los números a índices de las listas.
            partida = evento["numero"] - 1
            mes = fecha.month - 1
            origen = evento["origen"] - 1
            destino = evento["destino"] - 1
            # Una colisión suma una participación a cada uno de sus dos objetos.
            matriz[partida][mes][origen] += 1
            matriz[partida][mes][destino] += 1
    return matriz


def encabezado_matriz(usuario):
    """Identifica al usuario leído directamente del maestro."""
    return f"Usuario: {usuario['codigo']:03d}    Nombre y apellido: {usuario['nombre']}\n\n"


def pedir_anio():
    """Valida el año que se utilizará para filtrar las fechas de los eventos."""
    anio = int(input("Año: "))
    if anio < 1 or anio > 9999:
        raise ValueError("El año debe estar entre 1 y 9999.")
    return anio


def informe_contactos():
    """Matriz 8 x 8 de contactos del usuario en una partida elegida."""
    codigo = elegir_usuario()
    usuario = obtener_usuario(codigo)
    partidas = listar_partidas(codigo)
    if not partidas:
        return publicar_informe(f"matriz_contactos_{codigo:03d}", encabezado_matriz(usuario) + "Sin partidas.")
    print("\n" + tabla_partidas(partidas) + "\n")
    numero = int(input("Número de partida: "))
    existe = False
    for partida in partidas:
        if partida["numero"] == numero:
            existe = True
    if not existe:
        raise ValueError("La partida no pertenece al usuario.")
    eventos = []
    # historial_usuario sigue los enlaces, no escanea colisiones de otros usuarios.
    for evento in historial_usuario(codigo):
        if evento["numero"] == numero:
            eventos.append(evento)
    matriz = matriz_contactos(eventos)
    por_fila, por_columna, general = totales_matriz(matriz, config.CANTIDAD_OBJETOS)
    filas = []
    for origen in range(config.CANTIDAD_OBJETOS):
        filas.append([config.NOMBRES_OBJETOS[origen]] + matriz[origen] + [por_fila[origen]])
    filas.append(["TOTAL GENERAL"] + por_columna + [general])
    texto = encabezado_matriz(usuario) + f"Partida: {numero}\n\n"
    titulos = ["Origen / destino"] + config.NOMBRES_OBJETOS + ["Total"]
    texto += tabla("MATRIZ 2D - CONTACTOS ENTRE OBJETOS", titulos, filas)
    texto += f"\nTotal de eventos de la partida: {len(eventos)}"
    if general:
        # Compara las siete parejas posibles de este juego: Pac-Man contra otro objeto.
        cantidades = matriz[config.OBJ_PACMAN - 1][1:]
        mayor = cantidades.index(max(cantidades)) + 1
        menor = cantidades.index(min(cantidades)) + 1
        texto += f"\nMayor contacto: Pac-Man -> {config.NOMBRES_OBJETOS[mayor]}: {max(cantidades)}"
        texto += f"\nMenor contacto: Pac-Man -> {config.NOMBRES_OBJETOS[menor]}: {min(cantidades)}"
        texto += "\nSe incluyen ceros; en empates se toma el objeto de menor ID."
    else:
        texto += "\nSin contactos para comparar."
    texto += "\nCada contacto se cuenta una vez; mayor cantidad no significa mejor puntaje."
    return publicar_informe(f"matriz_contactos_{codigo:03d}_{numero:05d}", texto)


def informe_calendario():
    """Presenta 31 días por 12 meses y distingue fechas inexistentes de ceros."""
    codigo = elegir_usuario()
    usuario = obtener_usuario(codigo)
    anio = pedir_anio()
    matriz = matriz_calendario(historial_usuario(codigo), anio)
    por_dia, por_mes, general = totales_matriz(matriz, 12)
    filas = []
    for dia in range(31):
        fila = [dia + 1]
        for mes in range(12):
            ultimo_dia = monthrange(anio, mes + 1)[1]
            if dia + 1 > ultimo_dia:
                fila.append("—")
            else:
                fila.append(matriz[dia][mes])
        fila.append(por_dia[dia])
        filas.append(fila)
    filas.append(["TOTALES"] + por_mes + [general])
    titulos = ["Día / mes"]
    for mes in config.MESES:
        titulos.append(mes[:3])
    titulos.append("Total")
    texto = encabezado_matriz(usuario) + f"Año: {anio}\n\n"
    texto += tabla("MATRIZ 2D - COLISIONES POR DÍA Y MES", titulos, filas)
    if general:
        mejor = por_dia.index(max(por_dia)) + 1
        peor = por_dia.index(min(por_dia)) + 1
        texto += f"\nDía de mayor total: {mejor} ({max(por_dia)} colisiones)."
        texto += f"\nDía de menor total: {peor} ({min(por_dia)} colisiones)."
        texto += "\nSe suman los meses por número de día; incluye ceros. Empates: menor día."
    else:
        texto += "\nSin intervenciones durante el año; no hay mayor ni menor día."
    texto += "\n— = fecha inexistente. Cada evento cuenta una sola colisión."
    return publicar_informe(f"matriz_calendario_{codigo:03d}_{anio}", texto)


def tablas_intervenciones(matriz, numeros):
    """Muestra la matriz 3D por meses para no imprimir 96 columnas juntas."""
    secciones = []
    total_objetos = [0] * config.CANTIDAD_OBJETOS
    resumen = crear_matriz(len(numeros), 12)
    for mes in range(12):
        filas = []
        total_mes = [0] * config.CANTIDAD_OBJETOS
        for fila, numero in enumerate(numeros):
            valores = matriz[numero - 1][mes]
            total_partida_mes = sum(valores)
            resumen[fila][mes] = total_partida_mes
            filas.append([numero] + valores + [total_partida_mes])
            for objeto in range(config.CANTIDAD_OBJETOS):
                total_mes[objeto] += valores[objeto]
                total_objetos[objeto] += valores[objeto]
        filas.append(["TOTAL MES"] + total_mes + [sum(total_mes)])
        titulos = ["Partida"] + config.NOMBRES_OBJETOS + ["Total"]
        secciones.append(tabla(config.MESES[mes].upper(), titulos, filas))
    por_partida, por_mes, general = totales_matriz(resumen, 12)
    filas = []
    for fila, numero in enumerate(numeros):
        filas.append([numero] + resumen[fila] + [por_partida[fila]])
    filas.append(["TOTAL GENERAL"] + por_mes + [general])
    titulos = ["Partida / mes"]
    for mes in config.MESES:
        titulos.append(mes[:3])
    secciones.append(tabla("TOTALES POR PARTIDA Y MES", titulos + ["Total"], filas))
    secciones.append(tabla("TOTAL ANUAL POR OBJETO", config.NOMBRES_OBJETOS, [total_objetos]))
    return "\n\n".join(secciones), general


def informe_intervenciones():
    """Filtra un año y presenta participaciones por partida, mes y objeto."""
    codigo = elegir_usuario()
    usuario = obtener_usuario(codigo)
    anio = pedir_anio()
    eventos = []
    numeros = set()
    for evento in historial_usuario(codigo):
        fecha = datetime.strptime(evento["fecha"], "%Y-%m-%d %H:%M:%S")
        if fecha.year == anio:
            eventos.append(evento)
            numeros.add(evento["numero"])
    # Incluye también partidas del año sin contactos. No inventa partidas en los huecos.
    for partida in listar_partidas(codigo):
        fecha = datetime.strptime(partida["fecha"], "%Y-%m-%d %H:%M:%S")
        if fecha.year == anio:
            numeros.add(partida["numero"])
    texto = encabezado_matriz(usuario) + f"Año: {anio}\n\n"
    texto += "MATRIZ 3D - PARTIDA, MES Y OBJETO\n\n"
    if numeros:
        numeros = sorted(numeros)
        matriz = matriz_intervenciones(eventos, anio, max(numeros))
        tablas, total = tablas_intervenciones(matriz, numeros)
        texto += tablas
        texto += f"\n\nTotal de colisiones: {len(eventos)}"
        texto += f"\nTotal de participaciones: {total}"
    else:
        texto += "Sin partidas ni intervenciones durante el año."
    texto += "\nCada colisión tiene dos participantes. No se cuentan puntos."
    return publicar_informe(f"matriz_intervenciones_{codigo:03d}_{anio}", texto)


def menu_matrices():
    """Tres actividades separadas; todos los informes mantienen la pregunta s/n."""
    while True:
        print("\n=== INFORMES CON MATRICES ===")
        print("1. 2D: contactos entre objetos por partida")
        print("2. 2D: día y mes de un año")
        print("3. 3D: partida, mes y objeto")
        print("4. Volver a Datos Administrativos")
        opcion = input("\nOpción: ").strip()
        try:
            if opcion == "1":
                informe_contactos()
            elif opcion == "2":
                informe_calendario()
            elif opcion == "3":
                informe_intervenciones()
            elif opcion == "4":
                return
            else:
                print("Opción inválida.")
        except (ValueError, OSError) as error:
            print(f"No se pudo generar la matriz: {error}")
        input("\nPresioná Enter para volver a Matrices...")


def menu_administrativo():
    """Separa cada informe del menú y espera Enter antes de volver."""
    while True:
        print("\n\n" + "=" * 60)
        print("DATOS ADMINISTRATIVOS - INFORMES")
        print("=" * 60)
        print("1. Partidas (general y por usuario)")
        print("2. Padrón de Usuarios")
        print("3. Movimientos por usuario y número de partida")
        print("4. Consulta de puntajes de todos los usuarios")
        print("5. Ranking por usuario (Enter vacío = general)")
        print("6. Informes con matrices")
        print("7. Volver al menú principal\n")
        opcion = input("Opción: ").strip()
        try:
            if opcion == "1":
                mostrar_partidas(listar_partidas(elegir_usuario(opcional=True)))
            elif opcion == "2":
                mostrar_padron()
            elif opcion == "3":
                consultar_detalle()
            elif opcion == "4":
                mostrar_puntajes()
            elif opcion == "5":
                mostrar_ranking()
            elif opcion == "6":
                menu_matrices()
                continue
            elif opcion == "7":
                return
            else:
                print("\nOpción inválida.")
        except (ValueError, OSError) as error:
            print(f"\nNo se pudo generar el informe: {error}")
        input("\nPresioná Enter para volver a Datos Administrativos...")
