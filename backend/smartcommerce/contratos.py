"""Interfaz abstracta del repositorio (polimorfismo e inversión de dependencias)."""
from abc import ABC, abstractmethod


class RepositorioTienda(ABC):
    @abstractmethod
    def listar_productos(self) -> list[dict]: ...

    @abstractmethod
    def listar_categorias(self) -> list[dict]: ...

    @abstractmethod
    def crear_producto(self, nombre: str, categoria_id: int,
                      precio_centavos: int, stock: int) -> dict: ...

    @abstractmethod
    def cambiar_stock(self, identificador: int, cantidad: int) -> dict: ...

    @abstractmethod
    def comprar(self, cliente: str, lineas: tuple[dict, ...], pago: str) -> dict: ...

    @abstractmethod
    def listar_pedidos(self) -> list[dict]: ...

    @abstractmethod
    def cancelar_pedido(self, pedido_id: int) -> dict: ...

    @abstractmethod
    def indicadores(self) -> dict: ...
