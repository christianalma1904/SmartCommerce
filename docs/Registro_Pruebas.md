# Registro de pruebas — SmartCommerce v0.2

**Tipo:** pruebas unitarias y de integración de dominio con `unittest` (biblioteca estándar de Python).  
**Entorno de ejecución verificado:** Python 3.13 en entorno de prueba; en Windows se prevé Python 3.10 o superior.  
**Comando:** `python -m unittest discover -s backend/tests -p "test_*.py" -v`.

## Casos implementados

| Prueba | Verifica |
|---|---|
| `test_encapsulacion_y_validacion_precio` | `Producto` impide cambiar precio o stock sin validar |
| `test_carrito_usa_diccionario_encapsulado` | el carrito consolida cantidades y protege su estructura |
| `test_interfaz_abstracta_no_instanciable` | `RepositorioTienda` exige implementación concreta |
| `test_catalogo_categorias` | lectura del catálogo y categorías persistidas |
| `test_crear_producto_y_stock` | alta y actualización con validación |
| `test_compra_aprobada_resta_stock_y_total` | pedido confirmado y descuento correcto |
| `test_pago_rechazado_no_descontar` | no resta inventario ni suma ingresos |
| `test_stock_insuficiente_rollback` | error controlado, sin pedido parcial |
| `test_cancelacion_repone_una_sola_vez` | reembolso de inventario idempotente |
| `test_validaciones_solicitudes` | errores ante datos inválidos |
| `test_precios_historicos_conservados` | detalle del pedido conserva valor histórico |

## Resultados

En el entorno de elaboración, **11 pruebas de 11 superadas** tras corregir el manejo inicial de transacciones de creación de esquema. Esta corrección es parte del aprendizaje: la ejecución de `executescript` maneja el estado transaccional de forma distinta al uso de `BEGIN IMMEDIATE` empleado en las compras.

**Alcance de la evidencia:** estas pruebas comprueban la capa de dominio y persistencia, no equivalen a un análisis exhaustivo de seguridad, carga, accesibilidad, experiencia de usuario o compatibilidad entre navegadores. Debe grabarse además la interfaz funcionando para completar la entrega del docente.

**Reproducción en la computadora del estudiante:** después de descargar la nueva versión, ejecutar `test.bat` y mostrar en video el resultado obtenido **en su propio equipo**.
