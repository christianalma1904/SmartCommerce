# SmartCommerce 🛒

**Sistema de Gestión de E-commerce para pequeñas empresas**  
**Universidad Internacional del Ecuador · Ingeniería en Software · Unidad 1**  
**Estado:** Etapa 1 — Planeación del software (**implementación pendiente**).

## ¿Qué es SmartCommerce?

SmartCommerce propone una aplicación web para una pequeña tienda de una sola sede. Permitirá centralizar catálogo, categorías, inventario, clientes, carrito de compras, pedidos, pagos **simulados** e indicadores administrativos.

**Situación problemática:** cuando los datos de productos, existencias y pedidos se llevan por separado, aumenta el riesgo de inconsistencias y se dificulta el seguimiento. Se plantea como caso académico hipotético, no como un estudio de una empresa real.

**Objetivo general:** definir alcance, módulos, arquitectura y reglas verificables para orientar un desarrollo posterior.

## Documentación de la Unidad 1

| Archivo | Contenido |
|---|---|
| [Planificación del software](docs/Planificacion_Unidad1.md) | problema, objetivos, disciplinas, 9 módulos, requisitos, alcance, arquitectura, pruebas y riesgos |
| [Diagramas](diagramas/Diagramas_SmartCommerce.md) | arquitectura, flujo de compra, datos y estados del pedido |
| [Guion de video](docs/Guion_Video.md) | narración sugerida de 4 minutos en 6 escenas |
| [Evidencias de rúbrica](docs/Evidencias_Rubrica.md) | correspondencia con los criterios de evaluación |
| [Preparar la entrega](docs/Como_Entregar.md) | exportación a PDF, grabación y verificación final |
| [Propuesta de frontend](frontend/README.md) | interfaces, navegación y tecnología |
| [Propuesta de backend](backend/README.md) | endpoints conceptuales, entidades y reglas críticas |

> **Pendiente para entregar en el aula virtual:** exportar la planificación a **PDF**, personalizar los datos académicos y grabar el **video**. Los archivos Markdown publicados son documentación fuente; no reemplazan automáticamente el formato PDF solicitado.

## Usuarios

- **Visitante:** ve catálogo y categorías.
- **Cliente:** mantiene perfil, carrito e historial de pedidos; realiza un pago ficticio.
- **Administrador:** gestiona productos, categorías, inventario, pedidos e indicadores.

## Nueve módulos

| Código | Módulo | Función principal |
|---|---|---|
| M01 | Acceso y roles | registro, inicio de sesión y permisos |
| M02 | Productos | catálogo, edición y búsquedas |
| M03 | Categorías | organización y filtrado |
| M04 | Inventario | cantidades y alertas |
| M05 | Clientes | perfil propio |
| M06 | Carrito | selección y cantidades |
| M07 | Pedidos | creación, consulta y estados |
| M08 | Pago simulado | aprobación o rechazo ficticio |
| M09 | Dashboard | ventas simuladas y alertas |

## Alcance

**Incluye:** una tienda, dos roles autenticados, productos físicos, USD, catálogo, carrito, inventario, pedidos, pago ficticio y dashboard básico.

**No incluye:** dinero real, datos de tarjetas, facturación electrónica oficial, transporte, múltiples sucursales, marketplace, app móvil nativa ni IA.

## Arquitectura propuesta

- **Frontend:** React + TypeScript.
- **Backend:** Python + Django REST Framework.
- **Base de datos:** PostgreSQL.
- **Versionado:** Git y GitHub.

**Regla central:** añadir al carrito no reserva stock. El backend revalida precios y existencias al confirmar. Solo una aprobación **simulada** con inventario disponible puede confirmar un pedido y descontar unidades en la misma transacción. Una cancelación repone stock como máximo una vez.

## Estructura

```text
SmartCommerce/
├── README.md
├── .gitignore
├── docs/
│   ├── Planificacion_Unidad1.md
│   ├── Guion_Video.md
│   ├── Evidencias_Rubrica.md
│   └── Como_Entregar.md
├── diagramas/
│   └── Diagramas_SmartCommerce.md
├── frontend/
│   └── README.md
└── backend/
    └── README.md
```

## Etapas futuras

1. Planeación y especificación (actual).
2. Prototipos, diseño de datos y API.
3. Implementación de acceso y catálogo.
4. Implementación de inventario y flujo de compra.
5. Pruebas funcionales, seguridad y dashboard.
6. Demostración y revisión académica.

## Información académica

**Estudiante:** [Completar]  
**Asignatura:** [Completar]  
**Docente:** [Completar]  
**Institución:** Universidad Internacional del Ecuador (UIDE).

**Aviso:** este repositorio documenta la planeación. No afirma que la aplicación esté programada, desplegada ni validada con usuarios reales.
