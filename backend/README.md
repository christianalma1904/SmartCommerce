# Backend SmartCommerce v0.2 — Programación Orientada a Objetos

**Estado:** backend **funcional de demostración local** con Python estándar y SQLite, sin dependencias externas.

## Clases implementadas
- `Producto`: encapsulación de precio, existencias y propiedades.
- `Carrito`: estructura privada `{id: cantidad}` y validación.
- `RepositorioTienda`: contrato abstracto con `ABC`.
- `RepositorioSQLite`: implementa el contrato, SQL y transacciones.
- `ServicioTienda`: aplicación de reglas de negocio.
- `ErrorNegocio` y subclases: errores controlados.
- `Manejador`: servidor HTTP y traducción de excepciones a JSON.

## Endpoints realmente implementados
| Método | Ruta | Función |
|---|---|---|
| GET | `/api/productos` | lista productos y stock |
| GET | `/api/categorias` | lista categorías |
| GET | `/api/pedidos` | historial de pedidos |
| GET | `/api/indicadores` | resumen de ventas simuladas |
| POST | `/api/productos` | alta de producto (solo uso local) |
| PATCH | `/api/productos/{id}/stock` | modificación de existencias (solo uso local) |
| POST | `/api/pedidos` | compra ficticia aprobada/rechazada |
| POST | `/api/pedidos/{id}/cancelar` | cancelación y reintegro del stock |

## Pruebas
`python -m unittest discover -s backend/tests -p "test_*.py" -v`

## Diferencias con el plan de Unidad 1
El plan propuso **Django REST Framework + PostgreSQL**; el prototipo intermedio implementa los mismos principios esenciales en **Python estándar + SQLite** para facilitar una demostración de POO. Falta autenticación, controles administrativos por rol, integración y seguridad de producción. Escucha **solo en 127.0.0.1**: **no desplegar públicamente**.
