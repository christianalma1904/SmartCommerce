# Informe de avance: Aprendizaje Autónomo 2

**Actividad:** Desarrollo del Sistema de Gestión (SmartCommerce)  
**Asignatura:** Programación orientada a objetos — UIDE  
**Estudiante:** Christian Daniel Alcocer Marroquín  
**Corte de documentación:** 20 de noviembre de 2026  
**Versión de avance:** 0.2 — prototipo funcional local

## 1. Continuación del plan (Paso 1)

El proyecto mantiene el problema de la Unidad 1: una pequeña tienda necesita controlar productos, existencias y pedidos sin información contradictoria. La planeación inicial definía nueve módulos; en este avance se priorizó un **flujo completo verificable**, en vez de simular que todos están terminados.

### 1.1 Revisión y evaluación de fuentes

**Fuente A: Python, `abc` — Abstract Base Classes.** La documentación oficial define mecanismos para especificar métodos abstractos y contratos entre clases: <https://docs.python.org/3/library/abc.html>. **Interpretación:** una interfaz de repositorio permite que el servicio no dependa de SQLite directamente. **Evaluación crítica:** la abstracción tiene un costo en número de archivos y niveles; en un ejercicio mínimo sería excesiva, pero la rúbrica evalúa interfaces y el proyecto contempla una futura migración de base de datos, por lo que aquí se justifica. **Evidencia:** `RepositorioTienda` y `RepositorioSQLite`.

**Fuente B: Python, `sqlite3`.** La documentación oficial explica el uso de SQLite y la gestión de conexiones y transacciones: <https://docs.python.org/3/library/sqlite3.html>. **Interpretación:** se puede comprobar persistencia e integridad sin configurar servicios de infraestructura. **Evaluación crítica:** SQLite es adecuado para el prototipo local, **no es suficiente por sí solo para justificar un despliegue empresarial multiusuario**. Si la aplicación crece, deben medirse la concurrencia y migrar la persistencia al PostgreSQL propuesto en la Unidad 1. **Evidencia:** `BEGIN IMMEDIATE` y validación de stock en `RepositorioSQLite.comprar`.

**Fuente C: OWASP Top 10:2025.** El proyecto OWASP prioriza riesgos como el control de acceso deficiente: <https://owasp.org/projects/Top-Ten>. **Interpretación:** mostrar una pantalla de administración no constituye seguridad; los permisos deben verificarse en el servidor. **Evaluación crítica:** el prototipo **no tiene autenticación**, por eso solo se sirve en `127.0.0.1`, no debe publicarse ni utilizar datos reales. Se priorizó el ciclo de compra y se reconoce explícitamente el control de acceso como deuda técnica antes de usarlo fuera del laboratorio.

**Síntesis y cuestionamiento:** las fuentes no imponen una única tecnología ideal. Una interfaz abstracta aumenta flexibilidad, pero también complejidad; SQLite reduce preparación, pero limita la proyección a producción; y los estándares de seguridad recuerdan que demostrar una pantalla no equivale a tener un sistema listo para usuarios reales. Se eligió una implementación **pequeña, comprobable y honesta sobre sus límites**.

### 1.2 Posición y tesis del estudiante

**Tesis:** para demostrar POO con evidencias verificables, es más útil implementar un **recorrido de compra completo** con clases, validaciones, almacenamiento y pruebas que declarar los nueve módulos como concluidos sin poder ejecutarlos.

**Complejidad y límites reconocidos:** la seguridad de roles, la integración React/Django y la base PostgreSQL del plan original no están implementadas. El prototipo utiliza Python estándar y SQLite para eliminar dependencias externas; la decisión facilita replicar el ejercicio en un ordenador Windows y no representa un reemplazo definitivo de la arquitectura planificada.

**Perspectiva contraria:** podría argumentarse que un prototipo con todas las pantallas pero sin lógica real impresiona más en la exposición. Sin embargo, las pruebas de stock, rollback y cancelación aportan evidencia superior de funcionamiento y manejo de errores, que son criterios explícitos de esta actividad.

### 1.3 Alcance implementado y pendiente

| Módulo Unidad 1 | Avance demostrable Unidad 2 | Estado |
|---|---|---|
| Acceso y roles | ninguna autenticación real; local únicamente | pendiente |
| Productos | listar, crear, filtrar; lectura de precio y existencias | parcial |
| Categorías | consultar y filtrar | parcial |
| Inventario | cambiar stock, impedir saldo negativo y alertar stock bajo | funcional en prototipo |
| Perfil de clientes | capturar nombre al simular compra, sin cuentas | parcial |
| Carrito | agregar, ajustar y quitar productos; total estimado | funcional en prototipo |
| Pedidos | crear, listar y cancelar con reintegro de stock | parcial |
| Pagos | aprobar/rechazar pagos **ficticios**, sin cobro | funcional en prototipo |
| Dashboard | total de productos, pedidos confirmados, ingreso simulado y alertas | funcional en prototipo |

## 2. Clases, estructuras de datos e interfaces

| Clase | Archivo | Responsabilidad | POO / estructura |
|---|---|---|---|
| `Producto` | `backend/smartcommerce/modelos.py` | encapsular precio y stock; proteger invariantes | atributos privados, propiedades, métodos |
| `Carrito` | `modelos.py` | acumular unidades por producto | diccionario privado, validación y copia defensiva |
| `RepositorioTienda` | `contratos.py` | contrato de persistencia | herencia de ABC, métodos abstractos |
| `RepositorioSQLite` | `repositorio_sqlite.py` | datos y transacciones SQL | implementación de interfaz y polimorfismo |
| `ServicioTienda` | `servicios.py` | casos de uso y validaciones | composición e inyección de dependencias |
| `ErrorNegocio` y subclases | `errores.py` | fallos previsibles | jerarquía de excepciones |
| `Manejador` | `backend/servidor.py` | rutas HTTP y mensajes JSON | herencia de BaseHTTPRequestHandler |

**Interfaz de usuario:** `frontend/index.html`, `styles.css` y `app.js`; se comunica con el backend por solicitudes HTTP JSON. 

**Datos:** SQLite guarda `categorias`, `productos`, `pedidos` y `detalle_pedido`. Se usa una lista para productos y pedidos, un diccionario privado para el carrito y registros relacionales para conservar detalles históricos.

### 2.1 Encapsulación (Paso 2)

En `Producto`, los atributos `__precio_centavos` y `__stock` son privados; `cambiar_precio` y `ajustar_stock` evitan valores inválidos. En `Carrito`, el diccionario privado se consulta mediante copias: el código externo no puede modificar el estado interno sin pasar por `agregar`.

### 2.2 Manejo de errores e interfaces (Paso 2)

- `ErrorValidacion` → HTTP 400 por precio, cantidad o solicitud incorrecta.
- `NoEncontrado` → HTTP 404 cuando no existe producto o pedido.
- `SinExistencias` → HTTP 409 cuando la compra excede el stock.
- `EstadoInvalido` → HTTP 409 si se cancela un pedido que no está confirmado.
- Errores inesperados → HTTP 500 con mensaje genérico, detalle solo en registro del servidor.

**Polimorfismo:** `ServicioTienda` recibe el contrato `RepositorioTienda`, pero hoy se inyecta `RepositorioSQLite`. Es posible sustituir la persistencia en otra etapa sin reescribir las reglas del servicio.

### 2.3 Comentarios en operaciones complejas (Paso 2)

Los comentarios del código explican por qué se usa `BEGIN IMMEDIATE` para impedir ventas simultáneas superiores al stock, por qué `UPDATE ... WHERE stock >= cantidad` añade una segunda verificación, por qué una cancelación debe reponer unidades una sola vez y por qué los datos del carrito se devuelven como copias defensivas.

## 3. Pruebas y evaluación

Las **11 pruebas automáticas** de `backend/tests/test_smartcommerce.py` cubren encapsulación, interfaz abstracta, estructura de carrito, catálogo, creación de productos, actualización de stock, compra aprobada/rechazada, insuficiencia de stock, cancelación, validaciones y precio histórico. Se ejecutan con `test.bat` o con `python -m unittest discover -s backend/tests -p 'test_*.py' -v`.

**Evidencias objetivas:** las pruebas no sustituyen las pruebas de carga, seguridad o aceptación de usuarios. Consulta [Registro_Pruebas.md](Registro_Pruebas.md).

## 4. Conclusiones y logros (Paso 1)

1. Se **superó la fase de documentación**: el sistema puede ejecutarse y demuestra un ciclo de compra con datos persistentes.
2. El atributo privado, la estructura de datos y el contrato abstracto evidencian el uso de principios de POO, pero no prueban todavía el comportamiento de un sistema multiusuario completo.
3. Las transacciones y excepciones proporcionan una demostración reproducible de consistencia: cuando falla la compra no se crea un pedido confirmado ni se descuenta inventario.
4. La interfaz web mejora la observación del avance, pero requiere autenticación, pruebas de accesibilidad y controles antes de cualquier despliegue público.
5. **Próxima prioridad:** permisos por rol en backend, cuentas de usuario, y transición gradual a las tecnologías planteadas en la Unidad 1.

## 5. Evidencias correspondientes a la rúbrica

| Criterio (máx. 2 puntos) | Evidencia concreta |
|---|---|
| Evidencia Paso 1 | sección 1.1 con fuentes oficiales, interpretación, comparación y limitaciones |
| Posición del estudiante Paso 1 | sección 1.2: tesis de un recorrido funcional verificable y análisis del contraargumento |
| Conclusiones y logros Paso 1 | sección 4: resultados observables, consecuencias y prioridades |
| Encapsulación Paso 2 | `Producto`, `Carrito` y pruebas `test_encapsulacion*`, `test_carrito*` |
| Codificación, errores e interfaces Paso 2 | `RepositorioTienda`, `ServicioTienda`, GUI y excepciones HTTP controladas |
| Comentarios de funciones complejas | `RepositorioSQLite._transaccion`, `comprar`, `cancelar_pedido` |

**Rúbrica:** 6 criterios × 2 puntos = **12 puntos máximos**. La evidencia está diseñada para alcanzar los descriptores superiores, pero la nota final la asigna el docente.

## 6. Entregables todavía por grabar y enviar

- **Video 1:** explicación de avance, clases, decisiones técnicas y criterios POO.
- **Video 2:** demostración en navegador con compra, inventario, errores y pruebas.
- **GitHub:** código fuente y documentación publicados.

Consultar los [guiones sugeridos](Guiones_Autonomo2.md). No presentar capturas de imágenes estáticas como prueba de ejecución: mostrar la aplicación corriendo realmente.
