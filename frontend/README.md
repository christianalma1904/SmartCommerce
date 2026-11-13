# Frontend — SmartCommerce

**Estado:** planeado; no existe aún una aplicación ejecutable.

## Tecnología propuesta
- React
- TypeScript
- CSS adaptable (estilos a definir durante el diseño de interfaz)
- Consumo de API REST del backend

## Pantallas previstas
| Vista | Usuario | Propósito |
|---|---|---|
| Inicio y catálogo | visitante / cliente | consultar y buscar productos |
| Detalle del producto | visitante / cliente | conocer precio y disponibilidad |
| Registro / inicio de sesión | visitante | crear cuenta y acceder |
| Carrito | cliente | revisar productos, cantidades y totales |
| Confirmación de compra | cliente | efectuar pago simulado |
| Mis pedidos | cliente | consultar historial y estados |
| Perfil | cliente | actualizar datos propios |
| Panel administrativo | administrador | ver métricas generales |
| Gestión de productos | administrador | crear, actualizar, desactivar |
| Inventario y pedidos | administrador | ajustar stock y administrar estados |

## Reglas de interacción
- Las acciones administrativas deben estar restringidas **también en backend**.
- La interfaz debe mostrar mensajes cuando cambie el precio o las existencias.
- Agregar al carrito no reserva stock.
- Las métricas y pagos serán **simulados**, no cobros reales.

## Criterios preliminares
Diseño adaptable desde 360 px, navegación mediante teclado en acciones principales y estados de carga/error explícitos.

Ver los [diagramas](../diagramas/Diagramas_SmartCommerce.md).