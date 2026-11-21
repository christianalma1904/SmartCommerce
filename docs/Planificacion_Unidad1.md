# SmartCommerce — Planeación del software

**Universidad Internacional del Ecuador (UIDE)** · Ingeniería en Software  
**Actividad:** Unidad 1 / Etapa 1: Planeación del software  
**Estudiante:** [Completar nombre] · **Asignatura:** [Completar] · **Docente:** [Completar]  
**Fecha:** 13 de noviembre de 2026 · **Versión:** 1.0  
**Estado:** Documento de propuesta. El sistema aún no está implementado.

## 1. Resumen ejecutivo

**SmartCommerce** es la propuesta de una aplicación web de e-commerce para **una pequeña tienda de una sola sede**. Centralizará la administración de productos, categorías, existencias, clientes, carritos, pedidos y pagos simulados. También ofrecerá un tablero con indicadores de ventas *demostrativas*. Se plantea una interfaz para clientes y un panel para administradores.

**Problema de estudio:** En una tienda pequeña que administra por separado el catálogo, las existencias y los pedidos, puede haber información contradictoria, seguimiento manual y dificultades para identificar productos que deben reponerse. El escenario es hipotético: no se atribuyen resultados medidos a una empresa real.

**Solución:** una fuente de datos centralizada, procesos comerciales verificables y acceso diferenciado por rol.

## 2. Objetivos

**Objetivo general:** Planificar un sistema web de gestión de e-commerce para pequeñas tiendas, definiendo funcionalidades, alcance, arquitectura, reglas de negocio y criterios de aceptación que guíen su implementación posterior.

**Objetivos específicos:**

1. Identificar actores, necesidades y restricciones del proyecto.
2. Organizar nueve módulos funcionales y sus interacciones.
3. Definir requisitos funcionales y no funcionales verificables.
4. Diseñar conceptualmente las capas del sistema, sus datos y el flujo de compra.
5. Establecer pruebas de aceptación, riesgos y fases de desarrollo.
6. Documentar la propuesta en GitHub y explicarla mediante un video académico.

## 3. Relaciones con otras disciplinas

| Disciplina | Aplicación concreta | Contribución |
|---|---|---|
| Ingeniería de Software | requisitos, módulos, versiones y pruebas | evolución y mantenimiento |
| Bases de datos | claves foráneas, transacciones y consistencia | evitar pedidos y stock contradictorios |
| Gestión comercial | precios, pedidos, estados y reposición | representar el proceso de venta |
| UX/UI | búsqueda, formularios, diseño adaptable | reducir errores y esfuerzo del usuario |
| Seguridad informática | permisos por rol y validación en backend | proteger datos y operaciones |
| Análisis de datos | indicadores derivados de pedidos | apoyar decisiones de inventario |

**Síntesis interdisciplinaria:** un indicador comercial fiable depende de datos íntegros; para conseguirlos, las reglas de venta deben definirse con criterios de negocio y ejecutarse mediante transacciones en la base de datos, mientras la seguridad y la experiencia de usuario limitan errores y accesos indebidos. Por esta razón, SmartCommerce prioriza la **consistencia del pedido y del inventario** antes de añadir inteligencia artificial.

**Ejemplo de transferencia:** con cinco unidades en existencia, dos clientes intentan confirmar compras de tres y cuatro unidades. Añadir al carrito no reserva stock. En el momento de confirmar, el servidor vuelve a validar existencias dentro de una transacción: no pueden aprobarse compras que, sumadas, superen las cinco unidades.

## 4. Usuarios y responsabilidades

| Perfil | Acciones autorizadas |
|---|---|
| Visitante | consultar catálogo y categorías; registrarse |
| Cliente registrado | actualizar su perfil, gestionar carrito, simular pago y consultar **sus** pedidos |
| Administrador | mantener productos y categorías, actualizar stock, gestionar pedidos y consultar dashboard |

Existen **dos roles autenticados** (cliente y administrador). El visitante no requiere cuenta.

## 5. Alcance del proyecto

### 5.1 Incluye en el MVP

- Plataforma **web adaptable**, para una tienda que vende productos físicos.
- Registro e inicio de sesión de clientes; autorización administrativa.
- Productos y categorías; catálogo con búsqueda y filtros.
- Inventario por producto con umbrales de stock bajo.
- Perfil del cliente, carrito, creación de pedidos e historial.
- **Pago exclusivamente simulado**, con resultados aprobado/rechazado.
- Dashboard con pedidos, ventas simuladas, productos destacados y bajo stock.
- Moneda de referencia: **USD**; cantidades enteras; una sede y un inventario.

### 5.2 Fuera del alcance

- Transferencias, tarjetas, cobros reales o pasarelas bancarias.
- Facturación electrónica oficial y conexión al SRI.
- Logística de transportistas, seguimiento de envíos y múltiples sucursales.
- Marketplace con vendedores independientes, app móvil nativa e inteligencia artificial.
- Importación automática de un catálogo externo o ERP.

### 5.3 Restricciones y supuestos

Se supone conectividad a internet y que el administrador dispone de información legítima del catálogo. Los datos de demostración serán ficticios; ninguna cifra del dashboard representará ingresos reales. La implementación dependerá de futuras etapas académicas.

## 6. Estructura de nueve módulos

| ID | Módulo | Usuarios | Funcionalidades | Requisitos |
|---|---|---|---|---|
| M01 | Acceso y roles | cliente, administrador | registro, login, logout, permisos | RF01–RF02 |
| M02 | Catálogo | todos; edición admin | alta, edición, desactivación, consulta y búsqueda | RF03, RF05 |
| M03 | Categorías | todos; edición admin | organizar y filtrar productos | RF04–RF05 |
| M04 | Inventario | administrador | consultar/ajustar cantidades, alertar stock bajo | RF06–RF07, RF13, RF15 |
| M05 | Perfil de cliente | cliente | consulta y edición de datos propios | RF08 |
| M06 | Carrito | cliente | agregar, modificar, quitar y totalizar ítems | RF09–RF10 |
| M07 | Pedidos | cliente, administrador | generar, consultar, cambiar estado y cancelar | RF11, RF14–RF15 |
| M08 | Pago simulado | cliente | registrar resultado aprobado/rechazado | RF12–RF13 |
| M09 | Dashboard | administrador | indicadores basados en pedidos confirmados | RF16 |

### 6.1 Requisitos funcionales verificables

| ID | Requisito |
|---|---|
| RF01 | Permitir al cliente registrarse, iniciar y cerrar sesión. |
| RF02 | Restringir en el servidor todas las acciones administrativas. |
| RF03 | Crear, editar y desactivar productos como administrador. |
| RF04 | Crear y actualizar categorías como administrador. |
| RF05 | Consultar, buscar por nombre y filtrar productos visibles. |
| RF06 | Consultar y ajustar el inventario de cada producto. |
| RF07 | Identificar productos con existencias por debajo del umbral configurable. |
| RF08 | Consultar y actualizar el propio perfil de cliente. |
| RF09 | Añadir, modificar cantidades y quitar productos del carrito. |
| RF10 | Revalidar precios y existencias en el servidor antes de confirmar compra. |
| RF11 | Crear pedidos y consultar su detalle e historial propio. |
| RF12 | Registrar el resultado aprobado o rechazado de un pago **simulado**. |
| RF13 | Confirmar el pedido y descontar stock juntos mediante transacción si se aprueba el pago simulado. |
| RF14 | Cambiar estados de pedidos según transiciones permitidas, solo como administrador. |
| RF15 | Reponer stock **una sola vez** al cancelar un pedido confirmado. |
| RF16 | Presentar indicadores administrativos basados en pedidos confirmados no cancelados. |

### 6.2 Reglas de negocio

1. Añadir al carrito **no** reserva inventario; el precio y stock se revalidan en el servidor.
2. No se acepta una cantidad mayor que el stock disponible ni cantidades menores a uno.
3. El detalle del pedido conserva el **precio unitario histórico**.
4. Un pago ficticio rechazado no descuenta unidades.
5. La confirmación de pedido y reducción de stock se ejecutan **atómicamente**.
6. La cancelación de un pedido confirmado restituye existencias solo una vez.
7. El dashboard excluye pedidos cancelados y etiqueta todas las ventas como *simuladas*.

## 7. Requisitos no funcionales

Estos son **objetivos de pruebas futuras, no resultados ya medidos**.

| ID | Característica | Criterio previsto |
|---|---|---|
| RNF01 | Seguridad | contraseñas con hash robusto y autorización del servidor |
| RNF02 | Comunicación | HTTPS en despliegue; jamás almacenar tarjetas |
| RNF03 | Rendimiento | búsqueda en menos de 2 s con 500 productos y 20 usuarios concurrentes, en prueba definida |
| RNF04 | Usabilidad | vista adaptable desde 360 px y teclado para acciones principales |
| RNF05 | Integridad | validación, claves foráneas y transacciones en pedidos/stock |
| RNF06 | Mantenibilidad | módulos separados, documentación y Git |
| RNF07 | Recuperación | respaldo y restauración verificada en entorno de pruebas |

## 8. Historias de usuario

- **HU01:** Como visitante, quiero filtrar productos por categoría para localizar lo que necesito.
- **HU02:** Como cliente, quiero ver el detalle de mi carrito para conocer el total estimado.
- **HU03:** Como cliente, quiero confirmar una compra simulada para revisar mi pedido en el historial.
- **HU04:** Como administrador, quiero recibir alertas de stock bajo para decidir la reposición.
- **HU05:** Como administrador, quiero comparar pedidos y ventas simuladas para identificar productos de mayor movimiento.

## 9. Arquitectura propuesta

**Frontend:** React + TypeScript, responsable de vistas, formularios, carrito e indicadores.  
**Backend:** Python + Django REST Framework, responsable de API REST, autenticación, permisos y reglas comerciales.  
**Persistencia:** PostgreSQL, con claves, restricciones y transacciones.  
**Colaboración:** Git y GitHub.

Ver [diagramas técnicos](../diagramas/Diagramas_SmartCommerce.md).

### 9.1 Modelo conceptual de datos

- **Usuario:** id, nombre, email único, hash de contraseña, rol.
- **PerfilCliente:** usuario_id, teléfono opcional, dirección de entrega.
- **Categoria:** id, nombre.
- **Producto:** id, categoria_id, nombre, descripción, precio, activo.
- **Inventario:** producto_id, cantidad_disponible, umbral_bajo.
- **Carrito / ItemCarrito:** cliente, producto y cantidad.
- **Pedido / DetallePedido:** cliente, estado, fecha, total, producto, cantidad y precio histórico.
- **PagoSimulado:** pedido_id, resultado y fecha; **sin** información financiera.

Relaciones: categoría 1:N producto; producto 1:1 inventario; cliente 1:N pedido; pedido 1:N detalle; pedido 1:0..1 pago simulado.

### 9.2 Flujo y estados

**Compra:** catálogo → carrito → validación de cantidades, precios y stock → pedido pendiente → simulación de pago → (aprobación y stock disponible) confirmación y descuento atómicos → indicadores.

**Estados propuestos:** Pendiente de pago → Confirmado → En preparación → Entregado. Cancelación permitida desde pendiente o confirmado, pero no después de entregado; si estaba confirmado, restitución idempotente de stock.

## 10. Plan de desarrollo

| Fase | Actividades | Evidencia |
|---|---|---|
| 1. Planeación | problema, requisitos, alcance, módulos, diagramas | esta documentación |
| 2. Diseño | prototipos, modelo relacional, contrato de API | mockups y diagramas revisados |
| 3. Desarrollo base | acceso, catálogo, categorías y perfil | primeras funcionalidades |
| 4. Proceso comercial | inventario, carrito, pedidos, pago simulado | flujo integral |
| 5. Calidad y análisis | pruebas, dashboard, corrección y demostración | resultados medidos y video |

La metodología sugerida combina **iteraciones cortas** y seguimiento mediante incidencias en GitHub. Se prioriza el flujo central antes que funciones opcionales.

## 11. Criterios de aceptación y pruebas diseñadas

| Prueba | Condición / acción | Resultado esperado |
|---|---|---|
| PA01 (RF02) | un cliente solicita una acción admin | servidor rechaza |
| PA02 (RF10) | stock 2; cliente intenta confirmar 3 | no confirma, stock permanece 2 |
| PA03 (RF12–RF13) | pago simulado aprobado con stock | confirma pedido y descuenta exactamente una vez |
| PA04 (RF15) | se intenta cancelar dos veces pedido confirmado | el inventario se repone una sola vez |
| PA05 (RF16) | existen pedidos confirmados y cancelados | el dashboard excluye cancelados |
| PA06 (RF08) | cliente intenta editar perfil ajeno | se rechaza la operación |

**No son pruebas ejecutadas:** describen cómo verificar la futura implementación.

## 12. Riesgos y mitigación

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Ampliación excesiva de alcance | alto | MVP de una tienda con pagos ficticios |
| Ventas de unidades inexistentes | alto | revalidación y transacciones |
| Accesos no autorizados | alto | roles comprobados en backend |
| Pérdida de datos | medio | respaldo y pruebas de restauración |
| Retrasos | medio | desarrollo por prioridades e iteraciones |

## 13. Evaluación conforme a la rúbrica

- **Relaciones con la disciplina:** sección 3 conecta software, negocio, UX, seguridad, bases de datos y analítica y extrae una conclusión de su integración.
- **Transferencia:** el escenario de compras simultáneas, reglas transaccionales y pruebas aplica esos conocimientos a un problema nuevo.
- **Comunicación integrada:** tablas, requisitos numerados, diagramas Mermaid, lenguaje consistente, README y un guion audiovisual forman una presentación coordinada.

Se persigue el descriptor **Alcanzado** en los tres criterios (4 puntos cada uno), pero **la calificación la determina el docente**.

## 14. Conclusión

SmartCommerce es una propuesta acotada y viable de gestión de e-commerce para una pequeña tienda. Su aporte principal no es aparentar un sistema terminado, sino definir un proceso comercial coherente con controles de acceso, integridad de inventario y datos útiles para gestionar el negocio. Esta planeación constituye la base de las fases de diseño, implementación y pruebas.

---

**Nota de entrega:** para obtener el PDF solicitado, abre este documento en una vista Markdown imprimible o expórtalo a PDF, verifica el formato y agrega nombre, materia y docente. El video debe grabarse a partir del [guion](Guion_Video.md).