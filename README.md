# SmartCommerce 🛍️ — Final

**UIDE · Ingeniería en Software · Programación orientada a objetos**  
**Autor:** Christian Daniel Alcocer Marroquín  
**Proyecto:** Sistema de Gestión de E-commerce  
**Versión:** 0.2 — prototipo funcional local (no producción)

## ¿Qué se desarrolló?

Este proyecto continúa la planeación de SmartCommerce presentada en la Unidad 1 y agrega un **avance funcional real** con Python orientado a objetos, una interfaz web y una base de datos SQLite persistente.

**Puedes demostrar:** catálogo, filtrado, carrito, pago ficticio aprobado/rechazado, registro de pedidos, descuento de inventario, cancelación con devolución de stock, altas de productos y dashboard de ventas simuladas.

![Estado](https://img.shields.io/badge/Estado-prototipo%20acad%C3%A9mico-790a41?style=flat-square) ![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square)

> **Seguridad y alcance:** funciona **solo en tu equipo** (`127.0.0.1`). No tiene cuentas ni permisos de administrador implementados, pasarela de pago, facturación o despacho. Los botones del panel administrativo son de uso demostrativo; **no lo publiques en Internet**.

## 🚀 Ejecutarlo en Windows

**Requisito:** Python 3.10 o posterior, instalado y disponible en el comando `python`.

1. Descarga o clona el repositorio de GitHub.
2. Abre la carpeta `SmartCommerce` en tu equipo.
3. Haz doble clic en **`run.bat`** (o ejecuta `python backend/servidor.py` en una terminal).
4. Abre **http://127.0.0.1:8000** en tu navegador.
5. Para detenerlo, regresa a la terminal y presiona **Ctrl+C**.

**No necesitas instalar paquetes externos.** En el primer inicio se crea `backend/datos_smartcommerce.db` con ocho productos de prueba. El archivo de datos está excluido de Git mediante `.gitignore`.

### Probar el avance

1. Abre **Catálogo** y busca / filtra un producto.
2. Haz clic en **+** para agregarlo al carrito.
3. Abre **Carrito**, ingresa un nombre y elige pago ficticio **APROBADO**. Confirma.
4. Ve a **Administración**: observa el pedido, el ingreso simulado y el stock reducido.
5. Cancela el pedido: la cantidad debe reponerse y dejar de contar como venta.
6. Agrega un producto nuevo y modifica su inventario.
7. Crea otra compra con pago **RECHAZADO**: el stock no debe reducirse.

**Pruebas automáticas:** ejecuta `test.bat` o `python -m unittest discover -s backend/tests -p "test_*.py" -v`.

## 🧩 Programación orientada a objetos

| Elemento | Clase / archivo | Evidencia |
|---|---|---|
| Clase y encapsulación | `Producto`, `backend/smartcommerce/modelos.py` | atributos privados y métodos validados |
| Estructura de datos | `Carrito` | diccionario privado `{producto_id: cantidad}` con protección contra cambios externos |
| Interfaz abstracta | `RepositorioTienda`, `contratos.py` | métodos abstractos con `ABC` y `abstractmethod` |
| Polimorfismo | `RepositorioSQLite` implementa `RepositorioTienda` | el servicio depende del contrato, no de la clase concreta |
| Lógica de negocio | `ServicioTienda`, `servicios.py` | coordina validaciones y flujo del caso de uso |
| Excepciones | `ErrorValidacion`, `SinExistencias`, etc. | mensajes controlados y respuestas 400/404/409 |
| Interfaz gráfica | `frontend/index.html`, `app.js`, `styles.css` | catálogo, carrito y administración web |
| Persistencia | `repositorio_sqlite.py` | pedidos, productos e inventario en SQLite |
| Regla compleja | `RepositorioSQLite.comprar` | compra y reducción de stock en transacción |

## 🗂️ Archivos principales

```text
SmartCommerce/
├── README.md
├── run.bat                        # iniciar el prototipo
├── test.bat                       # ejecutar pruebas
├── backend/
│   ├── servidor.py                # servidor local HTTP y API JSON
│   ├── smartcommerce/
│   │   ├── modelos.py             # Producto y Carrito
│   │   ├── contratos.py           # interfaz abstracta del repositorio
│   │   ├── errores.py             # excepciones de negocio
│   │   ├── servicios.py           # lógica de aplicación
│   │   └── repositorio_sqlite.py  # persistencia y transacciones
│   └── tests/test_smartcommerce.py
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── docs/
│   └── Registro_Pruebas.md
└── diagramas/                    # diagramas de la Unidad 1 (si están presentes)
```

## 🔄 Relación con la Unidad 1

La **planificación inicial** propuso React + TypeScript, Django REST Framework y PostgreSQL. Para esta **entrega intermedia de POO**, se implementó un **prototipo autónomo con Python estándar, JavaScript y SQLite**, priorizando clases, encapsulación, errores y una demostración reproducible. **No se afirma que el stack de producción esté terminado**. En una próxima etapa se podría conservar el núcleo de negocio y migrar a la arquitectura propuesta inicialmente.

**Funcionalidades pendientes:** usuarios y autorización real, edición/eliminación de catálogo, flujo logístico, integración React/Django/PostgreSQL, pruebas de seguridad y despliegue seguro.

## 📌 Documentación de referencia

- [Python — ABC / Abstract Base Classes](https://docs.python.org/3/library/abc.html)
- [Python — sqlite3](https://docs.python.org/3/library/sqlite3.html)
- [OWASP Top 10:2025](https://owasp.org/projects/Top-Ten)
