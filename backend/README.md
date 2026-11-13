# Backend — SmartCommerce

**Estado:** planificado; todavía no hay endpoints ni servicio en ejecución.

## Tecnologías propuestas
- Python y Django
- Django REST Framework (API)
- PostgreSQL (base de datos relacional)

## Responsabilidades
- Autenticación y permisos de **cliente** y **administrador**.
- Validación de productos, categorías, precios y existencias.
- Gestión de inventario, carrito y pedidos.
- Registro de resultado de **pago simulado**.
- Confirmación de pedido y descuento de stock **en una misma transacción**.
- Cancelación idempotente y actualización de indicadores administrativos.

## Endpoints conceptuales (no implementados)
| Método | Ruta de ejemplo | Función |
|---|---|---|
| POST | /api/auth/register | registrar cliente |
| POST | /api/auth/login | autenticar usuario |
| GET | /api/products | buscar o listar catálogo |
| POST | /api/products | crear producto (admin) |
| GET | /api/categories | consultar categorías |
| GET | /api/cart | consultar carrito |
| POST | /api/orders | crear pedido pendiente |
| POST | /api/orders/{id}/simulate-payment | simular resultado y, si corresponde, confirmar |
| GET | /api/orders | listar pedidos propios |
| GET | /api/admin/dashboard | indicadores (admin) |

Las rutas se revisarán al definir el contrato de API y **no constituyen endpoints existentes**.

## Reglas críticas
1. El backend revalida el precio y stock del carrito antes de confirmar.
2. La compra nunca debe generar cantidades negativas ni confirmar ventas superiores a las existencias.
3. Si el pago ficticio falla, no se reduce el inventario.
4. El total definitivo y el precio histórico se determinan en el servidor.
5. Una cancelación autorizada repone el stock una sola vez.
6. Se aplica control de acceso en cada operación sensible.
7. No se guardan datos de tarjetas ni secretos en el repositorio.

## Entidades
Usuario, PerfilCliente, Categoria, Producto, Inventario, Carrito, ItemCarrito, Pedido, DetallePedido y PagoSimulado.

Ver [modelo conceptual](../diagramas/Diagramas_SmartCommerce.md).