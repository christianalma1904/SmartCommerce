"""Entidades de dominio: encapsulación, propiedades y estructuras de datos."""
from __future__ import annotations

from .errores import ErrorValidacion


def es_entero(valor):
    return isinstance(valor, int) and not isinstance(valor, bool)


class Producto:
    """Entidad con atributos privados: el precio y stock no se alteran libremente."""

    def __init__(self, identificador: int, nombre: str, categoria: str,
                 precio_centavos: int, stock: int):
        if not es_entero(identificador) or identificador < 1:
            raise ErrorValidacion("El identificador del producto es inválido.")
        if not isinstance(nombre, str) or not nombre.strip():
            raise ErrorValidacion("El nombre es obligatorio.")
        if not isinstance(categoria, str) or not categoria.strip():
            raise ErrorValidacion("La categoría es obligatoria.")
        self.__id = identificador
        self.__nombre = nombre.strip()
        self.__categoria = categoria.strip()
        self.__precio_centavos = 0
        self.__stock = 0
        self.cambiar_precio(precio_centavos)
        self.ajustar_stock(stock)

    @property
    def id(self) -> int:
        return self.__id

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def categoria(self) -> str:
        return self.__categoria

    @property
    def precio_centavos(self) -> int:
        return self.__precio_centavos

    @property
    def stock(self) -> int:
        return self.__stock

    def cambiar_precio(self, valor: int) -> None:
        if not es_entero(valor) or valor < 1:
            raise ErrorValidacion("El precio debe ser un entero positivo en centavos.")
        self.__precio_centavos = valor

    def ajustar_stock(self, cantidad: int) -> None:
        if not es_entero(cantidad) or cantidad < 0:
            raise ErrorValidacion("El stock debe ser un entero igual o mayor a cero.")
        self.__stock = cantidad

    def como_dict(self) -> dict:
        return {"id": self.id, "nombre": self.nombre, "categoria": self.categoria,
                "precio_centavos": self.precio_centavos, "stock": self.stock}


class Carrito:
    """Mapa privado producto_id -> cantidad, combina entradas duplicadas."""

    def __init__(self):
        self.__lineas: dict[int, int] = {}

    def agregar(self, producto_id: int, cantidad: int) -> None:
        if not es_entero(producto_id) or producto_id < 1:
            raise ErrorValidacion("El producto es inválido.")
        if not es_entero(cantidad) or cantidad < 1 or cantidad > 99:
            raise ErrorValidacion("La cantidad debe estar entre 1 y 99.")
        nueva = self.__lineas.get(producto_id, 0) + cantidad
        if nueva > 99:
            raise ErrorValidacion("No se permiten más de 99 unidades por producto.")
        self.__lineas[producto_id] = nueva

    @property
    def lineas(self) -> tuple[dict, ...]:
        # Copias: nadie puede modificar directamente el diccionario encapsulado.
        return tuple({"producto_id": p, "cantidad": c}
                     for p, c in self.__lineas.items())

    def __len__(self) -> int:
        return len(self.__lineas)
