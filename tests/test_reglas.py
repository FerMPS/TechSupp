# tests/test_reglas.py
# Pruebas básicas para el motor de reglas

import sys
import os
import unittest

# Añadir directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from motor import MotorReglas


class TestMotorReglas(unittest.TestCase):
    def setUp(self):
        self.motor = MotorReglas()

    def test_carga_kb(self):
        self.assertIsInstance(self.motor.base_conocimiento, dict)
        self.assertIn("reglas", self.motor.base_conocimiento)
        self.assertIn("preguntas", self.motor.base_conocimiento)

    def test_inferir_sin_hechos(self):
        self.motor.limpiar_hechos()
        diag = self.motor.inferir()
        self.assertEqual(len(diag), 0)

    def test_regla_no_enciende_sin_alimentacion(self):
        self.motor.limpiar_hechos()
        self.motor.establecer_hecho("encendido", "no")
        self.motor.establecer_hecho("bateria", "no")
        self.motor.establecer_hecho("luces", "no")
        self.motor.establecer_hecho("ventilador", "no")
        diag = self.motor.inferir()
        self.assertTrue(len(diag) > 0)
        self.assertIn(diag[0]["regla_id"], ["r01"])

    def test_sin_imagen_tras_encender(self):
        self.motor.limpiar_hechos()
        self.motor.establecer_hecho("encendido", "si")
        self.motor.establecer_hecho("ventilador", "si")
        self.motor.establecer_hecho("pantalla", "no")
        self.motor.establecer_hecho("post", "no")
        diag = self.motor.inferir()
        # Debe disparar alguna regla relacionada (r04 o r12)
        ids = [d["regla_id"] for d in diag]
        self.assertTrue(any(x in ["r04", "r12"] for x in ids))

    def test_wifi_problema(self):
        self.motor.limpiar_hechos()
        self.motor.establecer_hecho("wifi", "si")
        diag = self.motor.inferir()
        ids = [d["regla_id"] for d in diag]
        self.assertIn("r10", ids)

    def test_siguiente_pregunta_existe(self):
        self.motor.limpiar_hechos()
        # Sin hechos, hay preguntas faltantes
        self.assertTrue(self.motor.hay_preguntas_faltantes())
        sig = self.motor.siguiente_pregunta()
        self.assertIsNotNone(sig)
        self.assertIn("id", sig)
        self.assertIn("texto", sig)


if __name__ == "__main__":
    unittest.main()