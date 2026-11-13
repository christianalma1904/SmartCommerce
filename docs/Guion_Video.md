# Guion del video — SmartCommerce

**Actividad:** Unidad 1, planeación del software.  
**Duración sugerida:** 4 minutos.  
**Formato recomendado:** 6 diapositivas con portada, problema, módulos, proceso, arquitectura y cierre.  
**Estado real:** la solución está **planificada**, no desarrollada.

## Escena 1 — Presentación (0:00–0:30)

**Visual:** Título SmartCommerce, nombre y asignatura.

> Buenos días. Presentaré la planeación de SmartCommerce, un sistema de gestión de comercio electrónico dirigido a pequeñas tiendas. En esta primera etapa explicaré el problema, los objetivos, el alcance, los módulos y la arquitectura propuesta para orientar un desarrollo posterior.

## Escena 2 — Problema y solución (0:30–1:05)

**Visual:** Catálogo, inventario y pedidos separados → sistema centralizado.

> En el caso de estudio, la tienda administra su catálogo, inventario y pedidos mediante herramientas separadas. Eso puede generar diferencias entre las existencias publicadas y las reales. SmartCommerce propone centralizar esa información en una aplicación web que permita comprar de forma demostrativa y administrar el negocio con mayor consistencia. Se trata de un escenario académico hipotético.

## Escena 3 — Usuarios, módulos y alcance (1:05–1:55)

**Visual:** Visitante, cliente, administrador; nueve módulos resumidos.

> Existen tres perfiles de uso: visitante, cliente registrado y administrador. Los nueve módulos previstos son acceso y roles, catálogo, categorías, inventario, perfil de cliente, carrito, pedidos, pagos simulados y dashboard. La primera versión contempla una tienda física con un único inventario. Quedan excluidos los cobros reales, la facturación electrónica oficial, la logística externa y la inteligencia artificial, para mantener un alcance alcanzable.

## Escena 4 — Flujo de compra y transferencia (1:55–2:45)

**Visual:** [Flujo de compra](../diagramas/Diagramas_SmartCommerce.md).

> El cliente busca un producto, lo añade al carrito y solicita confirmar su compra. En ese momento, el servidor verifica nuevamente los precios y las existencias. El pago se simula como aprobado o rechazado. Si se aprueba y todavía hay inventario, el pedido se confirma y las unidades se descuentan mediante una transacción. Si falla, no se descuenta stock. Por ejemplo, si hay cinco unidades y dos clientes intentan comprar tres y cuatro, el sistema no debería confirmar ambas compras. Esta regla aplica conocimientos de software, bases de datos y gestión comercial para resolver un problema realista.

## Escena 5 — Arquitectura y datos (2:45–3:25)

**Visual:** Diagrama de tres capas y ejemplo de dashboard.

> Se propone React con TypeScript para la interfaz, Django REST Framework para la API y las reglas de negocio, y PostgreSQL para almacenar datos relacionados. Los permisos se verificarán en el servidor. Con pedidos confirmados y registros íntegros, un dashboard permitirá observar ventas simuladas, productos de mayor movimiento y alertas de bajo stock, apoyando decisiones comerciales.

## Escena 6 — Evidencia en GitHub y conclusión (3:25–4:00)

**Visual:** Captura **real** del repositorio, README y documentación.

> El repositorio de GitHub reúne la planificación, los diagramas, las reglas del sistema y este guion. En etapas futuras se implementará el software y se realizarán pruebas de acceso, inventario y pedidos. En conclusión, SmartCommerce integra varias disciplinas para planificar una solución digital con alcance controlado, reglas verificables y posibilidades de crecimiento. Muchas gracias.

## Recomendaciones

1. Muestra la portada y tu nombre completo.
2. Usa capturas del **repositorio real** y de los diagramas.
3. Evita afirmar que el sistema funciona: es **una propuesta**.
4. No leas todas las tablas; explica un ejemplo concreto de inventario.
5. Comprueba audio, ritmo y duración antes de subir el video.
6. Sube el video donde indique la plataforma; GitHub puede alojar el guion y la documentación, pero no sustituye la grabación.