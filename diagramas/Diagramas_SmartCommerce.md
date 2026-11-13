# Diagramas de diseño propuestos — SmartCommerce

Estos esquemas son **conceptuales** y se renderizan directamente en GitHub mediante Mermaid. No indican que exista código funcional.

## 1. Arquitectura general

```mermaid
flowchart TB
  U[Visitante / Cliente / Administrador] --> FE[Frontend: React + TypeScript]
  FE -->|Solicitudes HTTPS / API REST| BE[Backend: Django REST Framework]
  BE --> AUTH[Autenticación y permisos]
  BE --> RULES[Pedidos e inventario]
  BE --> DB[(PostgreSQL)]
  DB --> DASH[Datos para dashboard]
```

## 2. Flujo de compra y stock

```mermaid
flowchart TD
  A[Consultar catálogo] --> B[Agregar productos al carrito]
  B --> C[Solicitar confirmación]
  C --> D{¿Precios y stock vigentes?}
  D -->|No| E[Notificar cambios]
  D -->|Sí| F[Crear pedido pendiente]
  F --> G[Simular pago]
  G --> H{¿Pago simulado aprobado?}
  H -->|No| I[Registrar rechazo sin descontar stock]
  H -->|Sí| J[Revalidar stock en transacción]
  J --> K{¿Hay existencias?}
  K -->|No| L[No confirmar y notificar]
  K -->|Sí| M[Confirmar pedido y descontar existencias]
  M --> N[Actualizar indicadores de venta simulada]
```

**Regla crítica:** pedido e inventario se actualizan de modo **atómico**. Un pago rechazado no reduce unidades; una cancelación confirmada repone una sola vez.

## 3. Modelo entidad–relación conceptual

```mermaid
erDiagram
  USUARIO ||--o| PERFIL_CLIENTE : posee
  USUARIO ||--o| CARRITO : gestiona
  USUARIO ||--o{ PEDIDO : realiza
  CATEGORIA ||--o{ PRODUCTO : clasifica
  PRODUCTO ||--|| INVENTARIO : registra
  CARRITO ||--o{ ITEM_CARRITO : contiene
  PRODUCTO ||--o{ ITEM_CARRITO : se_agrega
  PEDIDO ||--|{ DETALLE_PEDIDO : contiene
  PRODUCTO ||--o{ DETALLE_PEDIDO : aparece
  PEDIDO ||--o| PAGO_SIMULADO : registra
```

## 4. Ciclo del pedido

```mermaid
stateDiagram-v2
  [*] --> Pendiente
  Pendiente --> Confirmado: Pago simulado aprobado
  Pendiente --> Cancelado: Cancelación
  Confirmado --> EnPreparacion: Iniciar preparación
  Confirmado --> Cancelado: Cancelar y reponer una sola vez
  EnPreparacion --> Entregado: Finalizar proceso
  Entregado --> [*]
  Cancelado --> [*]
```

**Nota:** el flujo mostrado es un modelo simplificado para esta etapa académica. Los estados definitivos se refinarán al diseñar el backend.