"""Pruebas aisladas del modelo: no modifican los datos de ejecución."""
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config
import archivos_fijos as af
import usuarios
import partidas
import colisiones
import informes
from objetos import Jugador, actualizar_dibujo


class ModeloAislado(unittest.TestCase):
    def setUp(self):
        self.temporal = TemporaryDirectory(prefix='pacman_estudio_')
        self.datos_originales = config.DATOS
        config.DATOS = Path(self.temporal.name) / 'datos'
        af.inicializar_archivos()

    def tearDown(self):
        config.DATOS = self.datos_originales
        self.temporal.cleanup()

    def usuario(self, nombre='José', username='demo'):
        return usuarios.registrar_usuario(nombre, username, 'prueba')

    def evento(self, tipo='PELLET', fecha='2024-02-29 12:00:00'):
        evento = colisiones.crear_evento(7, 2, tipo, 'Ejemplo ficticio')
        evento['fecha'] = fecha
        return evento

    def test_bytes_utf8_y_offset(self):
        self.assertEqual((config.TAMANO_USUARIO, config.TAMANO_ACUMULADOR,
                          config.TAMANO_PARTIDA, config.TAMANO_COLISION), (68, 22, 60, 133))
        self.usuario()
        self.usuario('Ejemplo B', 'demo_b')
        tercero = self.usuario('Ejemplo C', 'demo_c')
        ruta = config.DATOS / 'maestro_usuarios.txt'
        self.assertEqual(ruta.stat().st_size, 272)
        self.assertEqual(af.posicion_registro(3, 68), 204)
        with ruta.open('rb') as archivo:
            self.assertEqual(af.decodificar(af.leer_registro(archivo, 3, 68), config.CAMPOS_USUARIO), tercero)
        self.assertEqual(len('José'.encode('utf-8')), 5)
        self.assertEqual(usuarios.obtener_usuario(1)['nombre'], 'José')
        with self.assertRaises(ValueError):
            self.usuario('á' * 16, 'demolargo')

    def test_cadenas_intercaladas_y_enlace_roto(self):
        self.usuario()
        self.usuario('Ejemplo B', 'demo_b')
        for codigo in (1, 2, 1):
            colisiones.guardar_colision(codigo, 1, self.evento())
        historial = colisiones.historial_usuario(1)
        self.assertEqual([r['id'] for r in historial], [1, 3])
        self.assertEqual([(r['anterior'], r['siguiente']) for r in historial], [(0, 3), (1, 0)])
        self.assertEqual([r['id'] for r in colisiones.historial_usuario(2)], [2])
        maestro = usuarios.obtener_usuario(1)
        self.assertEqual((maestro['inicial'], maestro['final']), (1, 3))
        historial[-1]['siguiente'] = 1
        with (config.DATOS / 'colisiones.txt').open('r+b') as archivo:
            af.escribir_registro(archivo, 3, 133, af.codificar(historial[-1], config.CAMPOS_COLISION))
        with self.assertRaises(ValueError):
            colisiones.historial_usuario(1)

    def test_inicio_sin_resultado_y_actualizacion(self):
        self.usuario()
        self.usuario('Ejemplo B', 'demo_b')
        self.assertEqual(partidas.nueva_partida(1), 1)
        self.assertEqual(partidas.nueva_partida(2), 1)
        self.assertEqual(partidas.nueva_partida(1), 2)
        self.assertEqual(partidas.listar_partidas(), [])
        partidas.guardar_partida(1, 2, 10, 0, 'derrota')
        partidas.guardar_partida(1, 2, 20, 200, 'victoria')
        registros = partidas.listar_partidas()
        self.assertEqual(len(registros), 1)
        self.assertEqual((registros[0]['id'], registros[0]['numero'], registros[0]['puntaje_b']), (1, 2, 200))

    def test_matrices_eventos_y_participaciones(self):
        eventos = [dict(self.evento(), numero=1), dict(self.evento('POWER'), numero=3)]
        eventos.append(dict(self.evento(fecha='2025-01-01 00:00:00'), numero=3))
        contactos = informes.matriz_contactos(eventos[:2])
        self.assertEqual(sum(map(sum, contactos)), 2)
        calendario = informes.matriz_calendario(eventos, 2024)
        self.assertEqual(calendario[28][1], 2)
        self.assertEqual(sum(map(sum, calendario)), 2)
        matriz = informes.matriz_intervenciones(eventos, 2024, 3)
        self.assertEqual(sum(sum(map(sum, partida)) for partida in matriz), 4)
        self.assertEqual(sum(map(sum, matriz[1])), 0)
        independiente = informes.crear_matriz(2, 2)
        independiente[0][0] = 9
        self.assertEqual(independiente[1][0], 0)

    def test_movimiento_logico_y_visual(self):
        jugador = Jugador(7, 1)
        jugador.mover((0, 1))
        self.assertEqual((jugador.fila, jugador.columna), (7, 2))
        self.assertEqual(jugador.columna_visual, 1.0)
        actualizar_dibujo(jugador, 70, 140)
        self.assertEqual(jugador.columna_visual, 1.5)
        actualizar_dibujo(jugador, 1000, 140)
        self.assertEqual(jugador.columna_visual, 2.0)
        jugador.mover((-1, 0))  # Pared arriba: sigue hacia la derecha.
        self.assertEqual((jugador.fila, jugador.columna), (7, 3))


if __name__ == '__main__':
    unittest.main(verbosity=2)
