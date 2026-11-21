"""Pruebas de encapsulación, interfaces, integridad y errores (unittest)."""
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from smartcommerce.contratos import RepositorioTienda
from smartcommerce.errores import ErrorValidacion, EstadoInvalido, NoEncontrado, SinExistencias
from smartcommerce.modelos import Carrito, Producto
from smartcommerce.repositorio_sqlite import RepositorioSQLite
from smartcommerce.servicios import ServicioTienda


class TestDominio(unittest.TestCase):
    def test_encapsulacion_y_validacion_precio(self):
        p = Producto(1, "Mouse", "Tecnología", 1250, 5)
        self.assertEqual(p.precio_centavos, 1250)
        with self.assertRaises(ErrorValidacion):
            p.cambiar_precio(-1)
        with self.assertRaises(AttributeError):
            p.stock = -5

    def test_carrito_usa_diccionario_encapsulado(self):
        c = Carrito()
        c.agregar(1, 2)
        c.agregar(1, 3)
        self.assertEqual(c.lineas[0]["cantidad"], 5)
        c.lineas[0]["cantidad"] = 100
        self.assertEqual(c.lineas[0]["cantidad"], 5)

    def test_interfaz_abstracta_no_instanciable(self):
        with self.assertRaises(TypeError):
            RepositorioTienda()


class TestServicio(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = RepositorioSQLite(Path(self.tmp.name) / "prueba.db")
        self.s = ServicioTienda(self.repo)

    def test_catalogo_categorias(self):
        self.assertEqual(len(self.s.productos()), 8)
        self.assertEqual(len(self.s.categorias()), 3)

    def test_crear_producto_y_stock(self):
        nuevo = self.s.agregar_producto("Monitor", 1, 12500, 4)
        self.assertEqual(nuevo["stock"], 4)
        actualizado = self.s.actualizar_stock(nuevo["id"], 9)
        self.assertEqual(actualizado["stock"], 9)
        with self.assertRaises(ErrorValidacion):
            self.s.actualizar_stock(nuevo["id"], -1)

    def test_compra_aprobada_resta_stock_y_total(self):
        antes = self.s.productos()[0]["stock"]
        pedido = self.s.confirmar_compra("Cliente Demo", [{"producto_id": 1, "cantidad": 2}], "APROBADO")
        self.assertEqual(pedido["estado"], "CONFIRMADO")
        self.assertEqual(pedido["total_centavos"], 4590 * 2)
        self.assertEqual(self.s.productos()[0]["stock"], antes - 2)
        self.assertEqual(self.s.resumen()["ventas_centavos"], 9180)

    def test_pago_rechazado_no_descontar(self):
        antes = self.s.productos()[0]["stock"]
        pedido = self.s.confirmar_compra("Cliente Demo", [{"producto_id": 1, "cantidad": 1}], "RECHAZADO")
        self.assertEqual(pedido["estado"], "RECHAZADO")
        self.assertEqual(self.s.productos()[0]["stock"], antes)
        self.assertEqual(self.s.resumen()["ventas_centavos"], 0)

    def test_stock_insuficiente_rollback(self):
        antes = len(self.s.pedidos())
        with self.assertRaises(SinExistencias):
            self.s.confirmar_compra("Cliente Demo", [{"producto_id": 1, "cantidad": 99}], "APROBADO")
        self.assertEqual(len(self.s.pedidos()), antes)
        self.assertEqual(self.s.productos()[0]["stock"], 12)

    def test_cancelacion_repone_una_sola_vez(self):
        pedido = self.s.confirmar_compra("Cliente Demo", [{"producto_id": 1, "cantidad": 2}], "APROBADO")
        self.s.cancelar(pedido["id"])
        self.assertEqual(self.s.productos()[0]["stock"], 12)
        self.assertEqual(self.s.resumen()["ventas_centavos"], 0)
        with self.assertRaises(EstadoInvalido):
            self.s.cancelar(pedido["id"])
        self.assertEqual(self.s.productos()[0]["stock"], 12)

    def test_validaciones_solicitudes(self):
        with self.assertRaises(ErrorValidacion):
            self.s.confirmar_compra("X", [{"producto_id": 1, "cantidad": 1}], "APROBADO")
        with self.assertRaises(ErrorValidacion):
            self.s.confirmar_compra("Cliente", [{"producto_id": 1, "cantidad": True}], "APROBADO")
        with self.assertRaises(NoEncontrado):
            self.s.cancelar(9999)
        with self.assertRaises(ErrorValidacion):
            self.s.agregar_producto("Mesa", 1, -5, 4)

    def test_dos_compras_simultaneas_no_sobrevenden(self):
        """Dos compradores de 4 unidades compiten por un stock de 5."""
        self.s.actualizar_stock(1, 5)

        def comprar(indice):
            try:
                self.s.confirmar_compra(f"Cliente {indice}",
                                        [{"producto_id": 1, "cantidad": 4}], "APROBADO")
                return "confirmado"
            except SinExistencias:
                return "rechazado_stock"

        with ThreadPoolExecutor(max_workers=2) as executor:
            resultados = list(executor.map(comprar, [1, 2]))
        self.assertCountEqual(resultados, ["confirmado", "rechazado_stock"])
        self.assertEqual(self.s.productos()[0]["stock"], 1)
        self.assertEqual(self.s.resumen()["pedidos_confirmados"], 1)

    def test_precios_historicos_conservados(self):
        pedido = self.s.confirmar_compra("Cliente", [{"producto_id": 1, "cantidad": 1}], "APROBADO")
        detalles = self.s.pedidos()[0]["detalles"]
        self.assertEqual(detalles[0]["precio_centavos"], 4590)
        self.assertEqual(pedido["total_centavos"], 4590)


if __name__ == "__main__":
    unittest.main(verbosity=2)
