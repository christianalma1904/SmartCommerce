# Frontend del prototipo SmartCommerce v0.2

**Estado:** interfaz web **funcional de demostración**, en HTML, CSS y JavaScript sin librerías externas.

## Archivos implementados
- `index.html`: vistas de catálogo, carrito y administración.
- `styles.css`: diseño adaptable y estilos.
- `app.js`: búsqueda, filtros, carrito con `Map`, peticiones JSON, pedidos, inventario y dashboard.

## Cómo probar
Desde la raíz, inicia `run.bat` o `python backend/servidor.py`, luego abre <http://127.0.0.1:8000>. No abras `index.html` directamente: se requieren las rutas API del servidor Python.

## Alcance y próxima etapa
Se usa JavaScript simple para que el avance de POO sea ejecutable sin instalar Node. La planificación original propone **React + TypeScript** para una versión posterior. Las acciones de administración no están autenticadas, por lo que **solo puede usarse localmente**.

Consulta el [informe de avance](../docs/Autonomo2_Avance.md) y el [guion de demostración](../docs/Guiones_Autonomo2.md).
