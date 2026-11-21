"""Casos de uso. Dependen de la INTERFAZ, no de SQLite: facilita las pruebas."""
from .contratos import RepositorioTienda
from .errores import ErrorValidacion
from .modelos import Carrito, es_entero


class ServicioTienda:
    def __init__(self, repositorio: RepositorioTienda):
        if not isinstance(repositorio, RepositorioTienda):
            raise TypeError("El repositorio debe implementar RepositorioTienda.")
        self.__repo = repositorio

    def productos(self) -> list[dict]:
        return self.__repo.listar_productos()

    def categorias(self) -> list[dict]:
        return self.__repo.listar_categorias()

    def agregar_producto(self, nombre, categoria_id, precio_centavos, stock) -> dict:
        if not isinstance(nombre, str) or not nombre.strip() or len(nombre) > 90:
            raise ErrorValidacion("Escribe un nombre válido de máximo 90 caracteres.")
        if not es_entero(categoria_id) or categoria_id < 1:
            raise ErrorValidacion("La categoría debe ser válida.")
        if not es_entero(precio_centavos) or precio_centavos < 1:
            raise ErrorValidacion("El precio debe ser positivo en centavos.")
        if not es_entero(stock) or stock < 0:
            raise ErrorValidacion("Las existencias no pueden ser negativas.")
        return self.__repo.crear_producto(nombre.strip(), categoria_id, precio_centavos, stock)

    def actualizar_stock(self, identificador, cantidad) -> dict:
        if not es_entero(identificador) or identificador < 1:
            raise ErrorValidacion("Identificador incorrecto.")
        if not es_entero(cantidad) or cantidad < 0:
            raise ErrorValidacion("El stock no puede ser negativo.")
        return self.__repo.cambiar_stock(identificador, cantidad)

    def confirmar_compra(self, cliente, lineas, pago) -> dict:
        if not isinstance(cliente, str) or not (2 <= len(cliente.strip()) <= 70):
            raise ErrorValidacion("Escribe el nombre del cliente (2 a 70 caracteres).")
        if not isinstance(lineas, list) or not lineas or len(lineas) > 30:
            raise ErrorValidacion("El carrito debe tener entre 1 y 30 líneas.")
        if pago not in ("APROBADO", "RECHAZADO"):
            raise ErrorValidacion("El pago simulado debe ser APROBADO o RECHAZADO.")
        carrito = Carrito()
        for linea in lineas:
            if not isinstance(linea, dict):
                raise ErrorValidacion("Hay una línea inválida en el carrito.")
            carrito.agregar(linea.get("producto_id"), linea.get("cantidad"))
        return self.__repo.comprar(cliente.strip(), carrito.lineas, pago)

    def pedidos(self) -> list[dict]:
        return self.__repo.listar_pedidos()

    def cancelar(self, pedido_id) -> dict:
        if not es_entero(pedido_id) or pedido_id < 1:
            raise ErrorValidacion("Identificador de pedido incorrecto.")
        return self.__repo.cancelar_pedido(pedido_id)

    def resumen(self) -> dict:
        return self.__repo.indicadores()
