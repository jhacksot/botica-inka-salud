import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import core


class Pruebas(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.ruta = Path(self.tmp.name) / "registros.json"
        self.registros = []

    def alta(self, fecha="2026-10-22"):
        return core.registrar(self.registros, self.ruta, "Reclamo", fecha,
                              "Ejemplo ficticio", "Descripción de prueba sin datos personales.")

    def test_persistencia_y_codigo_tras_reabrir(self):
        primero = self.alta()
        self.registros = core.cargar(self.ruta)
        segundo = self.alta()
        self.assertEqual(primero["codigo"], "IS-000001")
        self.assertEqual(segundo["codigo"], "IS-000002")
        self.assertEqual(len(core.cargar(self.ruta)), 2)

    def test_validacion(self):
        for datos in [("Otro", "2026-10-22", "Caso", "Descripción ficticia"),
                      ("Queja", "2026-02-30", "Caso", "Descripción ficticia"),
                      ("Queja", "22/10/2026", "Caso", "Descripción ficticia"),
                      ("Queja", "2026-10-22", "  ", "Descripción ficticia"),
                      ("Queja", "2026-10-22", "Caso", "Corto")]:
            with self.subTest(datos=datos), self.assertRaises(ValueError):
                core.validar_datos(*datos)
        self.assertFalse(self.ruta.exists())

    def test_limites_y_acentos(self):
        datos = core.validar_datos("Recomendación", "2024-02-29", "á"*100, "é"*1000, "x"*60)
        self.assertEqual(len(datos["descripcion"]), 1000)
        for asunto, desc, ref in [("a"*101,"d"*10,""),("abc","d"*1001,""),("abc","d"*10,"r"*61)]:
            with self.assertRaises(ValueError):
                core.validar_datos("Queja", "2026-10-22", asunto, desc, ref)

    def test_busqueda(self):
        self.alta()
        self.assertIsNotNone(core.buscar(self.registros, " is-000001 "))
        self.assertIsNone(core.buscar(self.registros, "IS-999999"))

    def test_orden_y_desempate_sin_mutacion(self):
        self.alta("2026-10-22")
        self.alta("2026-09-01")
        self.alta("2026-09-01")
        ordenados = core.ordenar(self.registros, "fecha")
        self.assertEqual([r["codigo"] for r in ordenados], ["IS-000002", "IS-000003", "IS-000001"])
        self.assertEqual(self.registros[0]["codigo"], "IS-000001")
        self.assertEqual(core.ordenar(list(reversed(self.registros))), self.registros)

    def test_archivo_ausente_y_lista_vacia(self):
        self.assertEqual(core.cargar(self.ruta), [])
        self.assertEqual(core.ordenar([]), [])

    def test_archivo_corrupto_se_conserva(self):
        self.ruta.write_text("{JSON roto", encoding="utf-8")
        with self.assertRaises(ValueError):
            core.cargar(self.ruta)
        self.assertEqual(self.ruta.read_text(encoding="utf-8"), "{JSON roto")

    def test_esquema_y_duplicados(self):
        r = self.alta()
        for datos in [{}, [r, r], [dict(r, ficticio=False)], [dict(r, estado="Otro")], [dict(r, fecha="2026-02-30")]]:
            self.ruta.write_text(json.dumps(datos), encoding="utf-8")
            with self.subTest(datos=datos), self.assertRaises(ValueError):
                core.cargar(self.ruta)

    def test_fallo_guardado_no_confirma(self):
        self.alta()
        anterior = self.ruta.read_bytes()
        with patch("core.os.replace", side_effect=PermissionError("Prueba de fallo")):
            with self.assertRaises(OSError):
                self.alta()
        self.assertEqual(self.ruta.read_bytes(), anterior)
        self.assertEqual(len(self.registros), 1)
        self.assertEqual(list(self.ruta.parent.glob("*.tmp")), [])

    def test_estado_persistente_y_error(self):
        r = self.alta()
        core.cambiar_estado(self.registros, self.ruta, r["codigo"], "En revisión")
        self.assertEqual(core.cargar(self.ruta)[0]["estado"], "En revisión")
        with self.assertRaises(ValueError):
            core.cambiar_estado(self.registros, self.ruta, "IS-999999", "Cerrado")
        with patch("core.os.replace", side_effect=OSError("Prueba")):
            with self.assertRaises(OSError):
                core.cambiar_estado(self.registros, self.ruta, r["codigo"], "Cerrado")
        self.assertEqual(self.registros[0]["estado"], "En revisión")

    @unittest.skipUnless(os.name == "nt", "Bloqueo específico de Windows")
    def test_doble_instancia(self):
        a = core.BloqueoSesion(self.ruta.with_suffix(".lock"))
        b = core.BloqueoSesion(self.ruta.with_suffix(".lock"))
        a.adquirir()
        try:
            with self.assertRaises(OSError):
                b.adquirir()
        finally:
            a.liberar()
        b.adquirir()
        b.liberar()


if __name__ == "__main__":
    unittest.main(verbosity=2)
