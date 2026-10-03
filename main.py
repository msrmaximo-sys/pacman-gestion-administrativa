"""Punto de entrada: conecta el menú, el juego y la persistencia."""

import config
from archivos_fijos import inicializar_archivos
from usuarios import registrar_usuario, iniciar_sesion
from partidas import nueva_partida, guardar_partida
from colisiones import guardar_colision
from informes import menu_administrativo


def pedir_sesion():
    """Solicita las credenciales por terminal."""
    usuario = input("Usuario: ")
    clave = input("Clave: ")
    sesion = iniciar_sesion(usuario, clave)
    if sesion is None:
        print("Usuario o clave incorrectos.")
    else:
        print(f"Bienvenido/a, {sesion['nombre']}.")
    return sesion


def jugar(sesion):
    """Reserva la partida, abre el juego y guarda lo ocurrido al terminar."""
    # Importación local: los informes y el login no necesitan abrir Pygame.
    from juego import ejecutar_juego
    numero = nueva_partida(sesion["codigo"])
    print(f"Partida {numero}. WASD para moverte. Cerrar la ventana cuenta como derrota.")
    puntaje_a, puntaje_b, resultado, eventos = ejecutar_juego()
    # Conserva el orden real de los contactos dentro de la cadena del usuario.
    for evento in eventos:
        guardar_colision(sesion["codigo"], numero, evento)
    guardar_partida(sesion["codigo"], numero, puntaje_a, puntaje_b, resultado)
    print(f"{resultado.capitalize()} — Puntaje A: {puntaje_a}, Puntaje B: {puntaje_b}")


def main():
    """Muestra el menú principal y conserva la sesión durante la ejecución."""
    inicializar_archivos()
    sesion = None
    while True:
        print("\n=== JUEGO PAC-MAN — MENÚ PRINCIPAL ===")
        print("1. Jugar")
        print("2. Registrar usuario")
        print("3. Iniciar sesión")
        print("4. Datos Administrativos")
        print("5. Salir")
        opcion = input("Opción: ").strip()
        try:
            if opcion == "1":
                if sesion is None:
                    sesion = pedir_sesion()
                if sesion is not None:
                    jugar(sesion)
            elif opcion == "2":
                nombre = input(f"Nombre y apellido ({config.ANCHO_NOMBRE} bytes): ")
                usuario = input(f"Usuario ({config.ANCHO_USUARIO} bytes): ")
                clave = input(f"Clave ({config.ANCHO_CLAVE} bytes): ")
                registro = registrar_usuario(nombre, usuario, clave)
                print(f"Usuario registrado con código {registro['codigo']:03d}.")
            elif opcion == "3":
                sesion = pedir_sesion()
            elif opcion == "4":
                menu_administrativo()
            elif opcion == "5":
                return
            else:
                print("Opción inválida.")
        except (ValueError, OSError) as error:
            print(f"No se pudo completar la operación: {error}")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as error:
        print(f"No se pudo abrir el proyecto: {error}")
    except (EOFError, KeyboardInterrupt):
        print("\nPrograma finalizado.")
