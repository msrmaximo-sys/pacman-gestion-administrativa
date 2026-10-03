"""Único lugar que calcula desplazamientos de registros en los archivos binarios."""

import config


def posicion_registro(numero_registro, tamano_registro):
    """Convierte el número de registro a una posición en bytes después del título."""
    if numero_registro < 1:
        raise ValueError("La posición debe ser mayor que cero.")
    # El encabezado ocupa exactamente lo mismo que una línea de datos.
    tamano_encabezado = tamano_registro
    registros_anteriores = numero_registro - 1
    pos = tamano_encabezado + registros_anteriores * tamano_registro
    return pos


def crear_encabezado(campos):
    """Alinea los títulos sobre sus columnas sin convertirlos en datos."""
    encabezado = b""
    for nombre, ancho, numerico in campos:
        etiqueta = config.ETIQUETAS[nombre].encode("utf-8")
        if len(etiqueta) > ancho:
            raise ValueError("El título no entra en el ancho del campo.")
        encabezado += etiqueta.ljust(ancho, b" ") + b" "
    return encabezado + config.FIN_REGISTRO


def leer_registro(archivo, num_registro, tamano_registro):
    """Lee una posición desde 1; el cero significa puntero vacío."""
    if num_registro < 1:
        raise ValueError("La posición debe ser mayor que cero.")
    pos = posicion_registro(num_registro, tamano_registro)
    archivo.seek(pos)  # Posición en bytes, después del encabezado.
    datos = archivo.read(tamano_registro)
    if datos and len(datos) != tamano_registro:
        raise ValueError("Registro incompleto.")
    return datos


def escribir_registro(archivo, num_registro, tamano_registro, datos):
    """Escribe exactamente un registro en la posición indicada."""
    if num_registro < 1 or len(datos) != tamano_registro:
        raise ValueError("Posición o tamaño de registro incorrecto.")
    # Solo se permite reemplazar o agregar al final; nunca dejar huecos.
    cantidad = contar_registros(archivo, tamano_registro)
    if num_registro > cantidad + 1:
        raise ValueError("No se pueden dejar posiciones vacías entre registros.")
    # Sitúa el cursor al comienzo del registro que se quiere reemplazar.
    pos = posicion_registro(num_registro, tamano_registro)
    archivo.seek(pos)
    archivo.write(datos)


def contar_registros(archivo, tamano_registro):
    """Calcula la cantidad a partir del tamaño del archivo."""
    archivo.seek(0, 2)  # Desplazamiento cero desde el final del archivo.
    tamano_archivo = archivo.tell()
    tamano_encabezado = tamano_registro
    tamano_datos = tamano_archivo - tamano_encabezado
    if tamano_datos < 0 or tamano_datos % tamano_registro != 0:
        raise ValueError("El archivo tiene un registro incompleto.")
    return tamano_datos // tamano_registro


def codificar(registro, campos):
    """Codifica primero y rellena después; no corta caracteres UTF-8."""
    resultado = b""
    for nombre, ancho, numerico in campos:
        valor = registro[nombre]
        if numerico:
            if not isinstance(valor, int) or valor < 0:
                raise ValueError(f"{nombre}: se esperaba un entero no negativo.")
        texto = str(valor)
        if texto and not texto.isprintable():
            raise ValueError("No se permiten saltos, tabulaciones ni caracteres de control.")
        dato = texto.encode("utf-8")
        if len(dato) > ancho:
            raise ValueError(f"{nombre}: máximo {ancho} bytes UTF-8.")
        if numerico:
            dato = dato.rjust(ancho, b"0")
        else:
            dato = dato.ljust(ancho, b" ")
        resultado += dato + b" "
    return resultado + config.FIN_REGISTRO


def decodificar(datos, campos):
    """Separa por bytes antes de decodificar cada campo."""
    if len(datos) != config.tamano_registro(campos):
        raise ValueError("Registro inexistente o de longitud incorrecta.")
    if not datos.endswith(config.FIN_REGISTRO):
        raise ValueError("El registro debe terminar con un salto LF.")
    registro = {}
    inicio = 0
    for nombre, ancho, numerico in campos:
        fin = inicio + ancho
        if datos[fin:fin + 1] != b" ":
            raise ValueError("Falta un espacio separador entre campos.")
        texto = datos[inicio:fin].decode("utf-8")
        if numerico:
            registro[nombre] = int(texto)
        else:
            registro[nombre] = texto.rstrip(" ")
        inicio += ancho + 1  # También salta el espacio separador.
    # La ida y vuelta comprueba ceros, rellenos y caracteres sin modificar el archivo.
    if codificar(registro, campos) != datos:
        raise ValueError("El registro no respeta el relleno de longitud fija.")
    return registro


def inicializar_archivos():
    """Crea archivos faltantes y valida el formato de las líneas existentes."""
    config.DATOS.mkdir(exist_ok=True)
    archivos = [
        ("maestro_usuarios.txt", config.CAMPOS_USUARIO),
        ("partida_jugador.txt", config.CAMPOS_PARTIDA),
        ("colisiones.txt", config.CAMPOS_COLISION),
        ("acumulador_partidas.txt", config.CAMPOS_ACUMULADOR)]
    for nombre, campos in archivos:
        tamano = config.tamano_registro(campos)
        ruta = config.DATOS / nombre
        if not ruta.exists():
            with ruta.open("wb") as archivo:
                archivo.write(crear_encabezado(campos))
        with ruta.open("rb") as archivo:
            if archivo.read(tamano) != crear_encabezado(campos):
                raise ValueError(f"Encabezado incorrecto en {nombre}.")
            cantidad = contar_registros(archivo, tamano)
            for posicion in range(1, cantidad + 1):
                datos = leer_registro(archivo, posicion, tamano)
                try:
                    decodificar(datos, campos)
                except ValueError as error:
                    raise ValueError(f"{nombre}, registro {posicion}: {error}") from error
